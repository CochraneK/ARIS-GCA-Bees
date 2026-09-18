#!/usr/bin/env python3
"""Build a deterministic, de-identified ontology audit sample for ARIS4C016.

The output contains row indices/hashes and sampling strata only. It never emits
the taboo expression or translation. Reviewers can regenerate a private sheet
locally by joining against the checksum-verified OSF Study-1 CSV.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import urllib.request
from collections import defaultdict

GUID = "8nyga"
VIEW_ONLY = "60b964248cc64a8793a9013075132a1c"
SHA256 = "c725a30913e604e8344f4990c8d63990dcf0271e3a65765ddc3fa591b8cb1387"

LOW_COVERAGE = {"Setswana (BW)", "Spanish (ES)"}
DEFAULT_N = 15
LOW_COVERAGE_N = 30

ALIASES = {
    "sexualual references": "sexual references",
    "scathological": "scatological",
    "forbiden chemicals": "forbidden chemicals",
    "innapropriate question": "inappropriate question",
    "interjections": "interjection",
}

HIGH_CONFIDENCE_LABELS = {
    "sexual", "sexual references", "sexualbehavior", "sexualrelated",
    "sexualorgan", "genitals", "nipple", "menstruation", "scatological",
    "blasphemy", "religion", "medical", "illness", "disease", "death",
    "stupidity", "physical appearance", "appearance", "violence", "drugs",
    "substance", "forbidden chemicals", "political", "ideology", "wwii",
    "nazi", "yugoslavia", "family", "ancestry", "animal", "insult",
    "curse (wishing bad things to someone)", "curse", "interjection",
    "exclamation", "racial", "lgbtq", "homophobia", "misogyny",
    "disablement", "senior", "euphemism",
}


def load() -> list[dict[str, str]]:
    url = f"https://osf.io/download/{GUID}/?view_only={VIEW_ONLY}"
    with urllib.request.urlopen(url, timeout=120) as response:
        blob = response.read()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != SHA256:
        raise RuntimeError(f"checksum mismatch: {digest}")
    return list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig", errors="replace"))))


def norm(raw: str | None) -> str:
    x = (raw or "").strip().lower()
    return ALIASES.get(x, x)


def row_hash(row: dict[str, str], index: int) -> str:
    # Hash uses private lexical/source fields but output reveals only digest.
    payload = "\x1f".join([
        str(index),
        row.get("lang", ""),
        row.get("word_clean", ""),
        row.get("english_translation", ""),
        row.get("category", ""),
        row.get("category2", ""),
        row.get("category3", ""),
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def classify(row: dict[str, str]) -> dict[str, bool]:
    labels = [norm(row.get(k)) for k in ("category", "category2", "category3")]
    present = [x for x in labels if x]
    return {
        "missing_primary": not bool(labels[0]),
        "multi_label": len(present) >= 2,
        "unresolved": any(x not in HIGH_CONFIDENCE_LABELS for x in present),
    }


def stable_order(records: list[dict], salt: str) -> list[dict]:
    def key(rec: dict) -> str:
        return hashlib.sha256(
            f"{salt}|{rec['sample']}|{rec['row_index']}|{rec['row_hash']}".encode()
        ).hexdigest()
    return sorted(records, key=key)


def take_unique(pool: list[dict], chosen: dict[int, dict], n: int, salt: str) -> None:
    for rec in stable_order(pool, salt):
        if len(chosen) >= n:
            break
        chosen.setdefault(rec["row_index"], rec)


def main() -> None:
    rows = load()
    by_sample: dict[str, list[dict]] = defaultdict(list)
    for idx, row in enumerate(rows, start=1):
        flags = classify(row)
        by_sample[row["lang"]].append({
            "sample": row["lang"],
            "row_index": idx,
            "row_hash": row_hash(row, idx),
            **flags,
        })

    selected = []
    for sample in sorted(by_sample):
        records = by_sample[sample]
        target = LOW_COVERAGE_N if sample in LOW_COVERAGE else DEFAULT_N
        chosen: dict[int, dict] = {}

        pools = [
            ("missing_primary", [r for r in records if r["missing_primary"]]),
            ("unresolved", [r for r in records if r["unresolved"]]),
            ("multi_label", [r for r in records if r["multi_label"]]),
            ("random", records),
        ]

        # Equal quartile targets, with deterministic backfill when a pool is small.
        cumulative_targets = [
            max(1, round(target * 0.25)),
            max(1, round(target * 0.50)),
            max(1, round(target * 0.75)),
            target,
        ]
        for (stratum, pool), cumulative in zip(pools, cumulative_targets):
            before = set(chosen)
            take_unique(pool, chosen, cumulative, f"ARIS4C016-v0-{stratum}")
            for idx in set(chosen) - before:
                chosen[idx]["selection_stratum"] = stratum

        # Final backfill guarantees the target if the sample has enough rows.
        take_unique(records, chosen, target, "ARIS4C016-v0-backfill")
        for rec in chosen.values():
            rec.setdefault("selection_stratum", "backfill")

        selected.extend(sorted(chosen.values(), key=lambda x: x["row_index"]))

    output = {
        "project": "ARIS4C016",
        "source_guid": GUID,
        "source_sha256": SHA256,
        "target_policy": {
            "default_per_sample": DEFAULT_N,
            "low_coverage_per_sample": LOW_COVERAGE_N,
            "low_coverage_samples": sorted(LOW_COVERAGE),
        },
        "n_selected": len(selected),
        "rows": selected,
        "privacy_note": "No taboo expression or translation is emitted.",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
