#!/usr/bin/env python3
"""Prepare one-row-per-paper dual-AI input for ARIS4C005 latent prevalence.

Inputs:
- completed AI_A output CSV;
- completed AI_B output CSV;
- manager linkage CSV from make_adjudication_packet.py.

The manager linkage defines sampling provenance. AI labels are treated as noisy
measurements, not truth.

Binary severe target:
  1 -> SEVERE_SUPPORTED
  0 -> HONEST_MAJOR_ERROR / MINOR_OR_IMMATERIAL / NO_MATERIAL_PROBLEM_FOUND
  missing -> SERIOUS_UNRESOLVED / INDETERMINATE

Missing/unresolved labels are preserved as missing and never recoded negative.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

POSITIVE = {"SEVERE_SUPPORTED"}
NEGATIVE = {
    "HONEST_MAJOR_ERROR",
    "MINOR_OR_IMMATERIAL",
    "NO_MATERIAL_PROBLEM_FOUND",
}
MISSING = {"SERIOUS_UNRESOLVED", "INDETERMINATE"}


def norm(value: str | None) -> str:
    return (value or "").strip().upper()


def binary_state(value: str | None) -> str:
    state = norm(value)
    if state in POSITIVE:
        return "1"
    if state in NEGATIVE:
        return "0"
    if state in MISSING:
        return ""
    raise ValueError(f"Unknown scientific_state: {state!r}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def unique_by_assignment(rows: list[dict[str, str]], label: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        aid = (row.get("assignment_id") or "").strip()
        if not aid:
            raise ValueError(f"{label}: missing assignment_id")
        if aid in out:
            raise ValueError(f"{label}: duplicate assignment_id {aid}")
        # Validate state now so unexpected model output fails closed.
        binary_state(row.get("scientific_state"))
        out[aid] = row
    return out


def prepare(
    rows_a: list[dict[str, str]],
    rows_b: list[dict[str, str]],
    manager_rows: list[dict[str, str]],
    *,
    a_id: str = "AI_A",
    b_id: str = "AI_B",
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    a_by = unique_by_assignment(rows_a, "AI_A")
    b_by = unique_by_assignment(rows_b, "AI_B")

    manager_by_assignment: dict[str, dict[str, str]] = {}
    by_paper_manager: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)

    for row in manager_rows:
        aid = (row.get("assignment_id") or "").strip()
        paper = (row.get("paper_id") or "").strip()
        reviewer = (row.get("reviewer_id") or "").strip()
        if not aid or not paper or not reviewer:
            raise ValueError("Manager linkage requires assignment_id, paper_id, reviewer_id")
        if aid in manager_by_assignment:
            raise ValueError(f"Duplicate manager assignment_id: {aid}")
        manager_by_assignment[aid] = row
        if reviewer in by_paper_manager[paper]:
            raise ValueError(f"Duplicate manager reviewer {reviewer} for paper {paper}")
        by_paper_manager[paper][reviewer] = row

    expected_a = {
        row["assignment_id"]
        for reviewers in by_paper_manager.values()
        for reviewer, row in reviewers.items()
        if reviewer == a_id
    }
    expected_b = {
        row["assignment_id"]
        for reviewers in by_paper_manager.values()
        for reviewer, row in reviewers.items()
        if reviewer == b_id
    }

    if set(a_by) != expected_a:
        raise ValueError(
            f"AI_A assignment mismatch: expected={len(expected_a)} observed={len(a_by)}"
        )
    if set(b_by) != expected_b:
        raise ValueError(
            f"AI_B assignment mismatch: expected={len(expected_b)} observed={len(b_by)}"
        )

    output: list[dict[str, str]] = []
    stratum_counts: Counter[str] = Counter()
    pattern_counts: Counter[str] = Counter()
    unresolved_a = unresolved_b = both_unresolved = 0

    for paper in sorted(by_paper_manager):
        reviewers = by_paper_manager[paper]
        if a_id not in reviewers or b_id not in reviewers:
            raise ValueError(f"Paper {paper} lacks both {a_id}/{b_id} assignments")

        ma = reviewers[a_id]
        mb = reviewers[b_id]
        # Sampling metadata must be identical across the two assignments.
        for key in (
            "openalex_id",
            "audit_stratum",
            "stratum_population_N",
            "stratum_sample_n",
            "aris_inclusion_probability",
            "aris_design_weight",
        ):
            if (ma.get(key) or "") != (mb.get(key) or ""):
                raise ValueError(f"Sampling metadata disagreement for {paper}: {key}")

        ra = a_by[ma["assignment_id"]]
        rb = b_by[mb["assignment_id"]]

        # Model output must identify the same paper and adjudicator.
        if (ra.get("paper_id") or paper) != paper:
            raise ValueError(f"AI_A paper_id mismatch for assignment {ma['assignment_id']}")
        if (rb.get("paper_id") or paper) != paper:
            raise ValueError(f"AI_B paper_id mismatch for assignment {mb['assignment_id']}")

        a_bin = binary_state(ra.get("scientific_state"))
        b_bin = binary_state(rb.get("scientific_state"))
        if not a_bin:
            unresolved_a += 1
        if not b_bin:
            unresolved_b += 1
        if not a_bin and not b_bin:
            both_unresolved += 1

        pattern = f"A{a_bin or '?'}B{b_bin or '?'}"
        pattern_counts[pattern] += 1
        stratum = ma.get("audit_stratum") or ""
        stratum_counts[stratum] += 1

        output.append(
            {
                "paper_id": paper,
                "openalex_id": ma.get("openalex_id", ""),
                "doi": ma.get("doi", ""),
                "publication_year": ma.get("publication_year", ""),
                "primary_domain": ma.get("primary_domain", ""),
                "audit_stratum": stratum,
                "stratum_population_N": ma.get("stratum_population_N", ""),
                "stratum_sample_n": ma.get("stratum_sample_n", ""),
                "aris_inclusion_probability": ma.get("aris_inclusion_probability", ""),
                "aris_design_weight": ma.get("aris_design_weight", ""),
                "a_assignment_id": ma["assignment_id"],
                "b_assignment_id": mb["assignment_id"],
                "a_scientific_state": norm(ra.get("scientific_state")),
                "b_scientific_state": norm(rb.get("scientific_state")),
                "a_binary_severe": a_bin,
                "b_binary_severe": b_bin,
                "a_confidence": norm(ra.get("review_confidence")),
                "b_confidence": norm(rb.get("review_confidence")),
            }
        )

    summary = {
        "classification": "DUAL_AI_MEASUREMENT_INPUT_NOT_TRUTH_LABELS",
        "papers": len(output),
        "a_id": a_id,
        "b_id": b_id,
        "stratum_counts": dict(stratum_counts),
        "observed_binary_pattern_counts": dict(pattern_counts),
        "a_unresolved_or_indeterminate": unresolved_a,
        "b_unresolved_or_indeterminate": unresolved_b,
        "both_unresolved_or_indeterminate": both_unresolved,
        "warnings": [
            "SEVERE_SUPPORTED is the only positive binary severe state.",
            "SERIOUS_UNRESOLVED and INDETERMINATE remain missing measurements.",
            "The output contains noisy AI measurements, not article-level gold truth.",
            "Sampling metadata come from manager linkage, not model outputs.",
        ],
    }
    return output, summary


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("ai_a_csv", type=Path)
    p.add_argument("ai_b_csv", type=Path)
    p.add_argument("manager_linkage_csv", type=Path)
    p.add_argument("output_csv", type=Path)
    p.add_argument("summary_json", type=Path)
    p.add_argument("--a-id", default="AI_A")
    p.add_argument("--b-id", default="AI_B")
    args = p.parse_args()

    rows, summary = prepare(
        read_csv(args.ai_a_csv),
        read_csv(args.ai_b_csv),
        read_csv(args.manager_linkage_csv),
        a_id=args.a_id,
        b_id=args.b_id,
    )
    write_csv(args.output_csv, rows)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
