#!/usr/bin/env python3
"""Fast engineering fallback for the ARIS4C006 Chinese surname baseline.

Confirmatory provenance remains the pinned ChineseNames 2025.8 R package export in
00_export_chinesenames.R. This script exists so CI can validate the 26-letter
aggregation quickly from a public plain-CSV mirror of the same familyname table.

Do not silently substitute this fallback for the canonical confirmatory snapshot.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("familyname_csv")
    parser.add_argument("--out", default="data/derived/chinesenames_initial_population_baseline.csv")
    parser.add_argument("--metadata", default="data/metadata/chinesenames_engineering_baseline.json")
    args = parser.parse_args()

    source = Path(args.familyname_csv)
    raw = source.read_bytes()
    rows = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))

    required = {
        "surname", "compound", "initial", "initial.rank",
        "n.1930_2008", "ppm.1930_2008", "surname.uniqueness"
    }
    if not rows or not required.issubset(rows[0]):
        raise SystemExit(f"Unexpected familyname schema; required columns missing: {sorted(required)}")

    grouped: dict[str, dict] = defaultdict(lambda: {
        "surname_count": 0,
        "population_n": 0,
        "compound_surname_population_n": 0,
    })

    for row in rows:
        initial = row["initial"].strip().lower()
        n = int(float(row["n.1930_2008"]))
        grouped[initial]["surname_count"] += 1
        grouped[initial]["population_n"] += n
        if str(row["compound"]).strip() in {"1", "1.0", "TRUE", "True", "true"}:
            grouped[initial]["compound_surname_population_n"] += n

    total = sum(v["population_n"] for v in grouped.values())
    out_rows = []
    for rank, letter in enumerate("abcdefghijklmnopqrstuvwxyz", start=1):
        values = grouped.get(letter, {
            "surname_count": 0,
            "population_n": 0,
            "compound_surname_population_n": 0,
        })
        share = values["population_n"] / total if total else 0.0
        out_rows.append({
            "initial": letter,
            "initial_rank": rank,
            "surname_count": values["surname_count"],
            "population_n": values["population_n"],
            "population_share": f"{share:.12g}",
            "population_ppm": f"{share * 1_000_000:.12g}",
            "compound_surname_population_n": values["compound_surname_population_n"],
        })

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)

    meta = {
        "purpose": "engineering CI fallback only",
        "confirmatory_source": "ChineseNames R package version 2025.8 via 00_export_chinesenames.R",
        "input_rows": len(rows),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "total_population_n": total,
        "output_initial_rows": len(out_rows),
        "warning": "Validate against the pinned canonical R-package export before confirmatory analysis.",
    }
    metadata = Path(args.metadata)
    metadata.parent.mkdir(parents=True, exist_ok=True)
    metadata.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(meta, indent=2, ensure_ascii=False))
    for row in sorted(out_rows, key=lambda r: int(r["population_n"]), reverse=True)[:10]:
        print(row)


if __name__ == "__main__":
    main()
