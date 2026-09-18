#!/usr/bin/env python3
"""Create blinded reviewer packets from an ARIS4C005 Pilot B seed frame.

Outputs:
1) reviewer packet: article identity + blank adjudication fields; detector and
   sampling-risk metadata hidden.
2) manager linkage: sampling probabilities, detector features, and reviewer
   assignment linkage retained for later design-weighted analysis.

This script does not adjudicate papers.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import random
from pathlib import Path

REVIEW_FIELDS = [
    "reviewer_id",
    "review_round",
    "scientific_state",
    "materiality",
    "misconduct_evidence",
    "publication_process_state",
    "review_confidence",
    "fulltext_seen",
    "notice_seen",
    "formal_finding_seen",
    "evidence_locator",
    "adjudication_note",
]

IDENTITY_FIELDS = [
    "paper_id",
    "doi",
    "openalex_id",
    "publication_year",
    "work_type",
    "primary_domain",
    "primary_field",
    "primary_subfield",
]

HIDDEN_PREFIXES = ("det_", "aris_")
HIDDEN_EXACT = {"selected_via", "rw_enrichment_stratum"}


def assignment_id(paper_id: str, reviewer_id: str, round_id: int) -> str:
    raw = f"{paper_id}|{reviewer_id}|{round_id}".encode("utf-8")
    return "A" + hashlib.sha256(raw).hexdigest()[:16]


def choose_double_coded(
    paper_ids: list[str],
    fraction: float,
    seed: int,
) -> set[str]:
    if not 0 <= fraction <= 1:
        raise ValueError("double-code fraction must be between 0 and 1")
    rng = random.Random(seed)
    n = round(len(paper_ids) * fraction)
    return set(rng.sample(paper_ids, n)) if n else set()


def make_packets(
    rows: list[dict[str, str]],
    reviewers: list[str],
    double_fraction: float,
    seed: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    if not reviewers:
        raise ValueError("At least one reviewer is required")

    paper_ids = [row["paper_id"] for row in rows]
    double_ids = choose_double_coded(paper_ids, double_fraction, seed)
    rng = random.Random(seed + 1)

    reviewer_rows: list[dict[str, str]] = []
    manager_rows: list[dict[str, str]] = []

    for row in rows:
        primary = rng.choice(reviewers)
        assignments = [(primary, 1)]
        if row["paper_id"] in double_ids:
            alternatives = [r for r in reviewers if r != primary]
            if not alternatives:
                raise ValueError("Double coding requested but only one reviewer supplied")
            assignments.append((rng.choice(alternatives), 1))

        for reviewer_id, round_id in assignments:
            aid = assignment_id(row["paper_id"], reviewer_id, round_id)
            visible = {"assignment_id": aid}
            for field in IDENTITY_FIELDS:
                visible[field] = row.get(field, "")
            visible["reviewer_id"] = reviewer_id
            visible["review_round"] = str(round_id)
            for field in REVIEW_FIELDS[2:]:
                visible[field] = ""
            reviewer_rows.append(visible)

            hidden = {
                "assignment_id": aid,
                "paper_id": row["paper_id"],
                "reviewer_id": reviewer_id,
                "review_round": str(round_id),
                "planned_double_code": "1" if row["paper_id"] in double_ids else "0",
            }
            for key, value in row.items():
                if key in HIDDEN_EXACT or key.startswith(HIDDEN_PREFIXES):
                    hidden[key] = value
            manager_rows.append(hidden)

    reviewer_rows.sort(key=lambda r: (r["reviewer_id"], r["assignment_id"]))
    manager_rows.sort(key=lambda r: r["assignment_id"])
    return reviewer_rows, manager_rows


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("seed_csv", type=Path)
    parser.add_argument("reviewer_csv", type=Path)
    parser.add_argument("manager_csv", type=Path)
    parser.add_argument("--reviewer", action="append", default=[])
    parser.add_argument("--double-fraction", type=float, default=0.20)
    parser.add_argument("--seed", type=int, default=20260918)
    args = parser.parse_args()

    with args.seed_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    reviewers = args.reviewer or ["R1", "R2"]
    reviewer_rows, manager_rows = make_packets(
        rows, reviewers, args.double_fraction, args.seed
    )
    write_rows(args.reviewer_csv, reviewer_rows)
    write_rows(args.manager_csv, manager_rows)

    print(f"Seed works: {len(rows)}")
    print(f"Reviewer assignments: {len(reviewer_rows)}")
    print(f"Manager linkage rows: {len(manager_rows)}")
    print("Reviewer packet excludes detector flags, enrichment strata and design weights.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
