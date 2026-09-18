#!/usr/bin/env python3
"""Validate and merge completed ARIS4C005 adjudication packets.

Reviewer-facing packets are intentionally blinded. This script joins them back
to the manager linkage only after review, validates controlled vocabularies,
preserves unresolved states, and emits an analysis-ready long table plus an
agreement summary.

It never converts unresolved states to negatives.
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
from pathlib import Path
from typing import Any

SCIENTIFIC_STATES = {
    "SEVERE_SUPPORTED",
    "SERIOUS_UNRESOLVED",
    "HONEST_MAJOR_ERROR",
    "MINOR_OR_IMMATERIAL",
    "NO_MATERIAL_PROBLEM_FOUND",
    "INDETERMINATE",
}
MATERIALITY = {
    "MATERIAL",
    "POTENTIALLY_MATERIAL",
    "IMMATERIAL",
    "NOT_ASSESSABLE",
}
MISCONDUCT = {
    "FORMAL_FINDING",
    "STRONG_DOCUMENTED_EVIDENCE",
    "SUSPECTED_NOT_ESTABLISHED",
    "NO_EVIDENCE_OF_MISCONDUCT",
    "NOT_ASSESSABLE",
}
CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalized(value: str | None) -> str:
    return (value or "").strip().upper()


def validate_review(row: dict[str, str]) -> list[str]:
    errors: list[str] = []
    aid = row.get("assignment_id") or "<missing>"

    state = normalized(row.get("scientific_state"))
    if state not in SCIENTIFIC_STATES:
        errors.append(f"{aid}: invalid scientific_state={state!r}")

    materiality = normalized(row.get("materiality"))
    if materiality not in MATERIALITY:
        errors.append(f"{aid}: invalid materiality={materiality!r}")

    misconduct = normalized(row.get("misconduct_evidence"))
    if misconduct not in MISCONDUCT:
        errors.append(f"{aid}: invalid misconduct_evidence={misconduct!r}")

    confidence = normalized(row.get("review_confidence"))
    if confidence not in CONFIDENCE:
        errors.append(f"{aid}: invalid review_confidence={confidence!r}")

    return errors


def merge(
    review_rows: list[dict[str, str]],
    manager_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    manager: dict[str, dict[str, str]] = {}
    for row in manager_rows:
        aid = row.get("assignment_id") or ""
        if not aid:
            raise ValueError("Manager row missing assignment_id")
        if aid in manager:
            raise ValueError(f"Duplicate manager assignment_id: {aid}")
        manager[aid] = row

    seen_reviews: set[str] = set()
    errors: list[str] = []
    output: list[dict[str, str]] = []

    for review in review_rows:
        aid = review.get("assignment_id") or ""
        if not aid:
            errors.append("Reviewer row missing assignment_id")
            continue
        if aid in seen_reviews:
            errors.append(f"Duplicate reviewer assignment_id: {aid}")
            continue
        seen_reviews.add(aid)

        hidden = manager.get(aid)
        if hidden is None:
            errors.append(f"Reviewer assignment not present in manager linkage: {aid}")
            continue

        errors.extend(validate_review(review))

        combined = dict(hidden)
        for key, value in review.items():
            if key == "assignment_id":
                continue
            # Reviewer values are authoritative only for adjudication/identity
            # columns. Sampling/detector columns never come from reviewer files.
            if key.startswith("aris_") or key.startswith("det_"):
                continue
            if key in {"selected_via", "rw_enrichment_stratum"}:
                continue
            combined[key] = value
        output.append(combined)

    missing_reviews = sorted(set(manager) - seen_reviews)
    if missing_reviews:
        errors.append(f"Missing reviewer rows for {len(missing_reviews)} assignments")

    if errors:
        raise ValueError("Adjudication validation failed:\n" + "\n".join(errors[:100]))

    by_paper: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    for row in output:
        by_paper[row["paper_id"]].append(row)

    double_papers = 0
    exact_scientific_agreement = 0
    disagreements: list[dict[str, Any]] = []
    state_counts = collections.Counter()

    for row in output:
        state_counts[normalized(row.get("scientific_state"))] += 1

    for paper_id, rows in by_paper.items():
        if len(rows) < 2:
            continue
        double_papers += 1
        states = [normalized(r.get("scientific_state")) for r in rows]
        if len(set(states)) == 1:
            exact_scientific_agreement += 1
        else:
            disagreements.append(
                {
                    "paper_id": paper_id,
                    "assignment_ids": [r["assignment_id"] for r in rows],
                    "scientific_states": states,
                }
            )

    summary = {
        "classification": "ADJUDICATION_QA_NOT_PREVALENCE_ESTIMATE",
        "assignments_merged": len(output),
        "unique_papers": len(by_paper),
        "double_coded_papers": double_papers,
        "exact_scientific_state_agreement_papers": exact_scientific_agreement,
        "exact_agreement_fraction_among_double_coded": (
            exact_scientific_agreement / double_papers if double_papers else None
        ),
        "scientific_state_assignment_counts": dict(state_counts),
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "warning": (
            "Agreement is QA. It is not evidence that a label is substantively correct; "
            "disagreements require adjudication and unresolved states remain unresolved."
        ),
    }
    return output, summary


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
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
    parser.add_argument("completed_reviewer_csv", type=Path)
    parser.add_argument("manager_linkage_csv", type=Path)
    parser.add_argument("analysis_csv", type=Path)
    parser.add_argument("qa_json", type=Path)
    args = parser.parse_args()

    merged, summary = merge(
        read_csv(args.completed_reviewer_csv),
        read_csv(args.manager_linkage_csv),
    )
    write_csv(args.analysis_csv, merged)
    args.qa_json.parent.mkdir(parents=True, exist_ok=True)
    args.qa_json.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
