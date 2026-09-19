#!/usr/bin/env python3
"""Aggregate Epitran technical-coverage audit for ARIS4C016.

The script downloads the checksum-verified Study-1 CSV and attempts G2P without
printing any lexical item. It is a TECHNICAL coverage audit, not pronunciation
validation.

Special dictionary-backed character G2P for Mandarin/Cantonese is reported as
BLOCKED_BY_DEPENDENCY unless the required resource is explicitly supplied.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

GUID = "8nyga"
VIEW_ONLY = "60b964248cc64a8793a9013075132a1c"
SHA256 = "c725a30913e604e8344f4990c8d63990dcf0271e3a65765ddc3fa591b8cb1387"

DEFAULT_CODES = {
    "Cantonese (CN)": "yue-Hant",
    "Dutch (BE)": "nld-Latn",
    "English (AU)": "eng-Latn",
    "English (CA)": "eng-Latn",
    "English (GB)": "eng-Latn",
    "English (SG)": "eng-Latn",
    "English (US)": "eng-Latn",
    "Finnish (FI)": "fin-Latn",
    "French (FR)": "fra-Latn",
    "German (DE)": "deu-Latn",
    "Italian (IT)": "ita-Latn",
    "Mandarin (CN)": "cmn-Hans",
    "Serbian (RS)": "AUTO_SRP",
    "Setswana (BW)": "tsn-Latn",
    "Slovenian (SI)": "slv-Latn",
    "Spanish (CL)": "spa-Latn",
    "Spanish (ES)": "spa-Latn",
    "Thai (TH)": "tha-Thai",
}

SPECIAL_DEPENDENCIES = {
    "eng-Latn": "Flite + lex_lookup",
    "cmn-Hans": "CC-CEDict",
    "cmn-Hant": "CC-CEDict",
    "yue-Hant": "CC-Canto",
}

CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")


def download() -> list[dict[str, str]]:
    url = f"https://osf.io/download/{GUID}/?view_only={VIEW_ONLY}"
    with urllib.request.urlopen(url, timeout=120) as response:
        blob = response.read()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != SHA256:
        raise RuntimeError(f"Study-1 checksum mismatch: {digest}")
    return list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig", errors="replace"))))


def choose_code(sample: str, word: str) -> str:
    code = DEFAULT_CODES[sample]
    if code == "AUTO_SRP":
        return "srp-Cyrl" if CYRILLIC_RE.search(word or "") else "srp-Latn"
    return code


def has_mixed_letter_scripts(text: str) -> bool:
    scripts = set()
    for ch in text:
        if not ch.isalpha():
            continue
        name = unicodedata.name(ch, "")
        for script in ("LATIN", "CYRILLIC", "THAI", "CJK", "HIRAGANA", "KATAKANA"):
            if script in name:
                scripts.add(script)
                break
    return len(scripts) > 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cedict", default=None, help="Optional CC-CEDict path")
    parser.add_argument("--cccanto", default=None, help="Optional CC-Canto path")
    parser.add_argument(
        "--allow-special",
        action="store_true",
        help="Attempt English/Chinese special backends instead of pre-blocking them.",
    )
    args = parser.parse_args()

    try:
        import epitran
    except ImportError as exc:
        raise SystemExit(
            "Epitran is not installed. Install it in the execution environment "
            "before running this audit."
        ) from exc

    rows = download()
    engines = {}
    engine_errors = {}
    counts = defaultdict(Counter)

    def engine(code: str):
        if code in engines:
            return engines[code]
        if code in engine_errors:
            raise RuntimeError(engine_errors[code])
        kwargs = {}
        if code.startswith("cmn-") and args.cedict:
            kwargs["cedict_file"] = args.cedict
        if code == "yue-Hant" and args.cccanto:
            kwargs["cedict_file"] = args.cccanto
        try:
            engines[code] = epitran.Epitran(code, **kwargs)
            return engines[code]
        except Exception as exc:
            engine_errors[code] = f"{type(exc).__name__}: {exc}"
            raise

    for row in rows:
        sample = row["lang"]
        word = (row.get("word_clean") or "").strip()
        code = choose_code(sample, word)
        c = counts[sample]
        c["rows"] += 1
        if not word:
            c["EMPTY_INPUT"] += 1
            continue
        if any(ch.isspace() for ch in word):
            c["MULTIWORD"] += 1
        if has_mixed_letter_scripts(word):
            c["MIXED_SCRIPT"] += 1

        dependency = SPECIAL_DEPENDENCIES.get(code)
        if dependency and not args.allow_special:
            c["BLOCKED_BY_DEPENDENCY"] += 1
            continue
        if code.startswith("cmn-") and not args.cedict:
            c["BLOCKED_BY_DEPENDENCY"] += 1
            continue
        if code == "yue-Hant" and not args.cccanto:
            c["BLOCKED_BY_DEPENDENCY"] += 1
            continue

        try:
            epi = engine(code)
            ipa = epi.transliterate(word)
            if ipa and any(ch.isalpha() for ch in ipa):
                c["TECHNICAL_SUCCESS"] += 1
            elif ipa:
                c["NONEMPTY_NONLETTER_OUTPUT"] += 1
            else:
                c["EMPTY_OUTPUT"] += 1
        except Exception:
            c["BACKEND_ERROR"] += 1

    output = {
        "project": "ARIS4C016",
        "audit_type": "technical_G2P_coverage_only",
        "source_sha256": SHA256,
        "samples": {},
        "engine_initialization_errors": engine_errors,
        "privacy_note": "No lexical forms or IPA strings are emitted.",
    }
    for sample in sorted(counts):
        d = dict(counts[sample])
        attempted = d.get("rows", 0) - d.get("BLOCKED_BY_DEPENDENCY", 0) - d.get("EMPTY_INPUT", 0)
        d["attempted"] = attempted
        d["technical_success_rate_among_attempted"] = (
            round(d.get("TECHNICAL_SUCCESS", 0) / attempted, 4) if attempted else None
        )
        output["samples"][sample] = d

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
