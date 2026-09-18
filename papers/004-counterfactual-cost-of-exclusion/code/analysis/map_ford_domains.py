#!/usr/bin/env python3
"""Map ARIS4C004 source occupations to OECD Frascati/FORD broad fields.

This is a pre-exposure stratification aid. It maps only occupation labels with a
reasonably direct broad-field interpretation. Generic labels remain unclassified
rather than being guessed from fame, later network results, or mental-health data.

FORD broad fields follow OECD Frascati Manual 2015 Table 2.2:
1 Natural sciences
2 Engineering and technology
3 Medical and health sciences
4 Agricultural and veterinary sciences
5 Social sciences
6 Humanities and the arts
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

FIELD = {
    # 1 Natural sciences
    "mathematician": ("1 Natural sciences", "1.1 Mathematics", "direct"),
    "computer_scientist": ("1 Natural sciences", "1.2 Computer and information sciences", "direct"),
    "physicist": ("1 Natural sciences", "1.3 Physical sciences", "direct"),
    "physics": ("1 Natural sciences", "1.3 Physical sciences", "direct"),
    "chemist": ("1 Natural sciences", "1.4 Chemical sciences", "direct"),
    "astronomer": ("1 Natural sciences", "1.3 Physical sciences", "direct"),
    "geologist": ("1 Natural sciences", "1.5 Earth and related environmental sciences", "direct"),
    "palaeontologist": ("1 Natural sciences", "1.5 Earth and related environmental sciences", "direct"),
    "seismologist": ("1 Natural sciences", "1.5 Earth and related environmental sciences", "direct"),
    "biologist": ("1 Natural sciences", "1.6 Biological sciences", "direct"),
    "botanist": ("1 Natural sciences", "1.6 Biological sciences", "direct"),
    "zoologist": ("1 Natural sciences", "1.6 Biological sciences", "direct"),

    # 2 Engineering and technology
    "engineer": ("2 Engineering and technology", "2.x Engineering and technologies", "direct"),
    "inventor": ("2 Engineering and technology", "2.x Engineering and technologies", "broad-applied"),

    # 3 Medical and health sciences
    "nurse": ("3 Medical and health sciences", "3.3 Health sciences", "direct"),
    "dermatologist": ("3 Medical and health sciences", "3.2 Clinical medicine", "direct"),
    "surgeon": ("3 Medical and health sciences", "3.2 Clinical medicine", "direct"),
    "physician": ("3 Medical and health sciences", "3.2 Clinical medicine", "direct"),
    "internist": ("3 Medical and health sciences", "3.2 Clinical medicine", "direct"),
    "psychiatrist": ("3 Medical and health sciences", "3.2 Clinical medicine", "direct"),
    "pharmacist": ("3 Medical and health sciences", "3.x Medical/health sciences", "broad"),

    # 5 Social sciences
    "psychologist": ("5 Social sciences", "5.1 Psychology and cognitive sciences", "direct"),
    "economist": ("5 Social sciences", "5.2 Economics and business", "direct"),
    "education": ("5 Social sciences", "5.3 Education", "direct"),
    "teacher": ("5 Social sciences", "5.3 Education", "occupation-proxy"),
    "sociologist": ("5 Social sciences", "5.4 Sociology", "direct"),
    "sociologue": ("5 Social sciences", "5.4 Sociology", "direct"),
    "political_scientist": ("5 Social sciences", "5.6 Political science", "direct"),
    "anthropologist": ("5 Social sciences", "5.9 Other social sciences", "broad"),

    # 6 Humanities and the arts
    "historian": ("6 Humanities and the arts", "6.1 History and archaeology", "direct"),
    "archaeologist": ("6 Humanities and the arts", "6.1 History and archaeology", "direct"),
    "linguist": ("6 Humanities and the arts", "6.2 Languages and literature", "direct"),
    "sinologist": ("6 Humanities and the arts", "6.2 Languages and literature", "broad"),
    "orientalist": ("6 Humanities and the arts", "6.2 Languages and literature", "broad"),
    "philologist": ("6 Humanities and the arts", "6.2 Languages and literature", "direct"),
    "altphilologe": ("6 Humanities and the arts", "6.2 Languages and literature", "direct"),
    "lexicographer": ("6 Humanities and the arts", "6.2 Languages and literature", "direct"),
    "philosopher": ("6 Humanities and the arts", "6.3 Philosophy, ethics and religion", "direct"),
    "theologian": ("6 Humanities and the arts", "6.3 Philosophy, ethics and religion", "direct"),
    "art_historian": ("6 Humanities and the arts", "6.4 Arts/history of arts", "direct"),
}

GENERIC = {
    "academic",
    "professor",
    "profesor",
    "scientist",
    "research",
    "sailor",
    "intelligence",
}


def classify(label: str) -> tuple[str, str, str]:
    key = (label or "").strip().casefold()
    if key in FIELD:
        return FIELD[key]
    if key in GENERIC or not key:
        return ("unclassified", "unclassified", "generic_or_ambiguous_source_occupation")
    return ("unclassified", "unclassified", "unmapped_source_occupation")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_csv", type=Path)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    args = parser.parse_args()

    with args.candidate_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        candidates = list(csv.DictReader(handle))

    out: list[dict[str, str]] = []
    for row in candidates:
        broad, second, basis = classify(row.get("level3_main_occ", ""))
        out.append(
            {
                "person_id": row.get("person_id", ""),
                "canonical_name": row.get("canonical_name", ""),
                "source_level3_occupation": row.get("level3_main_occ", ""),
                "ford_broad_field": broad,
                "ford_second_level_proxy": second,
                "mapping_basis": basis,
                "mental_health_information_used": "false",
            }
        )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = list(out[0].keys()) if out else [
        "person_id",
        "canonical_name",
        "ford_broad_field",
    ]
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out)

    broad_counts = Counter(row["ford_broad_field"] for row in out)
    unmapped_labels = sorted(
        {
            row["source_level3_occupation"]
            for row in out
            if row["ford_broad_field"] == "unclassified"
        }
    )
    summary = {
        "candidate_n": len(out),
        "ford_broad_field_counts": dict(broad_counts),
        "classified_n": sum(row["ford_broad_field"] != "unclassified" for row in out),
        "unclassified_n": broad_counts.get("unclassified", 0),
        "unclassified_source_labels": unmapped_labels,
        "mental_health_information_used": False,
        "reference": "OECD Frascati Manual 2015 Table 2.2 Fields of R&D classification",
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
