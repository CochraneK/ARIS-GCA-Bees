#!/usr/bin/env python3
"""ARIS4C016 Phase-0 structural audit.

Downloads the public Sulpizio et al. OSF CSVs, verifies SHA-256, and emits
de-identified aggregate diagnostics. Raw taboo expressions are never printed.

Usage:
    python code/phase0_audit.py > data/phase0_audit_summary.json
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import urllib.request
from collections import Counter
from itertools import combinations

VIEW_ONLY = "60b964248cc64a8793a9013075132a1c"

FILES = {
    "study1": {
        "guid": "8nyga",
        "sha256": "c725a30913e604e8344f4990c8d63990dcf0271e3a65765ddc3fa591b8cb1387",
    },
    "study2": {
        "guid": "t8wj9",
        "sha256": "617306c5d762586e0426081b13f779d64b30937f2d35cfbe24fdb97ded1f7a5a",
    },
    "participants": {
        "guid": "zsa2e",
        "sha256": "841a6b35f56fcf5e16e91a78a2293993f38ea308beb74f0d562ad285631cfa7b",
    },
}

PARTICIPANT_NAME_MAP = {
    "Australia": "English (AU)", "Canada": "English (CA)",
    "Cantonese": "Cantonese (CN)", "Chile": "Spanish (CL)",
    "Finnish": "Finnish (FI)", "Flemish": "Dutch (BE)",
    "French": "French (FR)", "German": "German (DE)",
    "Italian": "Italian (IT)", "Mandarin": "Mandarin (CN)",
    "Serbian": "Serbian (RS)", "Setswana": "Setswana (BW)",
    "Singapore": "English (SG)", "Slovenian": "Slovenian (SI)",
    "Spanish": "Spanish (ES)", "Thai": "Thai (TH)",
    "UK": "English (GB)", "US": "English (US)",
}


def download(guid: str, expected_sha256: str) -> bytes:
    url = f"https://osf.io/download/{guid}/?view_only={VIEW_ONLY}"
    with urllib.request.urlopen(url, timeout=120) as response:
        blob = response.read()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != expected_sha256:
        raise RuntimeError(
            f"SHA-256 mismatch for {guid}: expected {expected_sha256}, got {digest}"
        )
    return blob


def read_csv(spec: dict[str, str]) -> list[dict[str, str]]:
    blob = download(spec["guid"], spec["sha256"])
    text = blob.decode("utf-8-sig", errors="replace")
    return list(csv.DictReader(io.StringIO(text)))


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3:
        return None
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sx = sum((x - mx) ** 2 for x in xs)
    sy = sum((y - my) ** 2 for y in ys)
    if sx <= 0 or sy <= 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(sx * sy)


def sample_diagnostics(study1: list[dict[str, str]], participants: list[dict[str, str]]) -> list[dict]:
    participant_counts = {
        PARTICIPANT_NAME_MAP[r["lang"]]: int(r["participants"]) for r in participants
    }
    out = []
    for lang in sorted(participant_counts):
        rows = [r for r in study1 if r["lang"] == lang]
        productions = sum(int(float(r["n"])) for r in rows if r["n"])
        raw_labels = set()
        missing_primary = 0
        multilabel = 0
        for row in rows:
            labels = [
                row.get("category", "").strip(),
                row.get("category2", "").strip(),
                row.get("category3", "").strip(),
            ]
            raw_labels.update(x for x in labels if x)
            missing_primary += int(not labels[0])
            multilabel += int(sum(bool(x) for x in labels) >= 2)
        nrows = len(rows)
        npeople = participant_counts[lang]
        out.append({
            "sample": lang,
            "participants": npeople,
            "unique_rows": nrows,
            "production_count": productions,
            "items_per_participant": round(productions / npeople, 3),
            "raw_category_label_count": len(raw_labels),
            "primary_category_missing_rate": round(missing_primary / nrows, 4),
            "multilabel_row_rate": round(multilabel / nrows, 4),
        })
    return out


def label_inventory(study1: list[dict[str, str]]) -> dict:
    return {
        col: dict(Counter((r.get(col) or "<missing>").strip() or "<missing>" for r in study1).most_common())
        for col in ("category", "category2", "category3")
    }


def same_language_correlations(study2: list[dict[str, str]]) -> dict:
    rows = [r for r in study2 if r.get("category", "").strip().lower() != "filler"]
    dims = ("tabooness", "offensiveness", "valence", "arousal", "concreteness", "aoa")
    result = {}
    for prefix in ("English", "Spanish"):
        langs = sorted({r["lang"] for r in rows if r["lang"].startswith(prefix)})
        by_lang = {lang: {r["word_clean"]: r for r in rows if r["lang"] == lang} for lang in langs}
        pair_rows = []
        for a, b in combinations(langs, 2):
            shared = sorted(set(by_lang[a]) & set(by_lang[b]))
            record = {"a": a, "b": b, "shared_items": len(shared)}
            for dim in dims:
                xs, ys = [], []
                for word in shared:
                    try:
                        x = float(by_lang[a][word][dim])
                        y = float(by_lang[b][word][dim])
                    except (TypeError, ValueError):
                        continue
                    if math.isfinite(x) and math.isfinite(y):
                        xs.append(x)
                        ys.append(y)
                value = pearson(xs, ys)
                record[dim] = None if value is None else round(value, 4)
            pair_rows.append(record)
        result[prefix] = pair_rows
    return result


def main() -> None:
    study1 = read_csv(FILES["study1"])
    study2 = read_csv(FILES["study2"])
    participants = read_csv(FILES["participants"])
    result = {
        "project": "ARIS4C016",
        "source": "Sulpizio et al. 2024 / OSF ecr32",
        "source_files": FILES,
        "study1_rows": len(study1),
        "study2_rows": len(study2),
        "study1_samples": len({r["lang"] for r in study1}),
        "study2_samples": len({r["lang"] for r in study2}),
        "sample_diagnostics": sample_diagnostics(study1, participants),
        "raw_label_inventory": label_inventory(study1),
        "same_language_correlations": same_language_correlations(study2),
        "privacy_note": "No raw taboo expressions are emitted by this audit.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
