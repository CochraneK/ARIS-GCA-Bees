#!/usr/bin/env python3
"""Select a deterministic MH-blind second-review sample for ARIS4C004 identity decisions."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ALWAYS_REVIEW = {
    "VERIFIED_CLUSTER",
    "AMBIGUOUS_COLLISION",
    "EXCLUDED_IDENTITY_ERROR",
}
SAMPLEABLE = {"VERIFIED_SINGLE"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def hash_fraction(person_id: str, seed: str) -> float:
    digest = hashlib.sha256(f"{seed}|{person_id}".encode("utf-8")).digest()
    value = int.from_bytes(digest[:8], "big")
    return value / float(2**64)


def select(rows: list[dict[str, str]], single_fraction: float, seed: str) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for row in rows:
        status = (row.get("identity_status") or "").strip()
        pid = (row.get("person_id") or "").strip()
        if status in ALWAYS_REVIEW:
            reason = f"all_{status.lower()}"
        elif status in SAMPLEABLE and hash_fraction(pid, seed) < single_fraction:
            reason = "deterministic_verified_single_sample"
        else:
            continue

        selected.append(
            {
                "person_id": pid,
                "canonical_name": row.get("canonical_name", ""),
                "birth_year": row.get("birth_year", ""),
                "death_year": row.get("death_year", ""),
                "first_review_identity_status": status,
                "selection_reason": reason,
                "second_review_status": "",
                "second_review_openalex_ids": "",
                "second_reviewer": "",
                "agreement_with_first_review": "",
                "adjudication_required": "",
                "mh_blinded_at_second_review": "",
                "second_review_date": "",
                "notes": "",
            }
        )
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("identity_decisions", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--single-fraction", type=float, default=0.25)
    parser.add_argument("--seed", default="aris4c004-identity-second-review-v1")
    args = parser.parse_args()

    if not 0 <= args.single_fraction <= 1:
        parser.error("--single-fraction must be within [0,1]")

    rows = read_csv(args.identity_decisions)
    selected = select(rows, args.single_fraction, args.seed)

    fields = [
        "person_id",
        "canonical_name",
        "birth_year",
        "death_year",
        "first_review_identity_status",
        "selection_reason",
        "second_review_status",
        "second_review_openalex_ids",
        "second_reviewer",
        "agreement_with_first_review",
        "adjudication_required",
        "mh_blinded_at_second_review",
        "second_review_date",
        "notes",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(selected)

    by_reason: dict[str, int] = {}
    for row in selected:
        reason = row["selection_reason"]
        by_reason[reason] = by_reason.get(reason, 0) + 1
    summary = {
        "identity_rows_n": len(rows),
        "second_review_selected_n": len(selected),
        "single_fraction": args.single_fraction,
        "seed": args.seed,
        "selection_reason_counts": by_reason,
        "mental_health_information_used": False,
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
