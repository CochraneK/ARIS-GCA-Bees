#!/usr/bin/env python3
"""Merge two blinded AI adjudication passes and build an arbitration queue.

AI outputs remain fallible measurement records. This script does not convert
model agreement into ground truth."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

STATES = {
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
CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}


def norm(x: str | None) -> str:
    return (x or "").strip().upper()


def validate(row: dict[str, str]) -> list[str]:
    errors = []
    aid = row.get("assignment_id") or "<missing>"
    if not row.get("assignment_id"):
        errors.append("missing assignment_id")
    if not row.get("adjudicator_id"):
        errors.append(f"{aid}: missing adjudicator_id")
    if norm(row.get("scientific_state")) not in STATES:
        errors.append(f"{aid}: invalid scientific_state")
    if norm(row.get("materiality")) not in MATERIALITY:
        errors.append(f"{aid}: invalid materiality")
    if norm(row.get("review_confidence")) not in CONFIDENCE:
        errors.append(f"{aid}: invalid review_confidence")
    return errors


def arbitration_reasons(a: dict[str, str], b: dict[str, str]) -> list[str]:
    reasons = []
    if norm(a.get("scientific_state")) != norm(b.get("scientific_state")):
        reasons.append("SCIENTIFIC_STATE_DISAGREEMENT")
    if norm(a.get("materiality")) != norm(b.get("materiality")):
        reasons.append("MATERIALITY_DISAGREEMENT")
    if "LOW" in {norm(a.get("review_confidence")), norm(b.get("review_confidence"))}:
        reasons.append("LOW_CONFIDENCE")
    if "INDETERMINATE" in {norm(a.get("scientific_state")), norm(b.get("scientific_state"))}:
        reasons.append("INDETERMINATE")
    if norm(a.get("formal_finding_seen")) != norm(b.get("formal_finding_seen")):
        reasons.append("FORMAL_FINDING_EVIDENCE_DISAGREEMENT")
    return reasons


def merge(rows_a: list[dict[str, str]], rows_b: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    errors = []
    for row in rows_a + rows_b:
        errors.extend(validate(row))
    if errors:
        raise ValueError("AI adjudication validation failed:\n" + "\n".join(errors[:100]))

    a_by = {r["assignment_id"]: r for r in rows_a}
    b_by = {r["assignment_id"]: r for r in rows_b}
    if len(a_by) != len(rows_a) or len(b_by) != len(rows_b):
        raise ValueError("Duplicate assignment_id within an adjudicator pass")

    if set(a_by) != set(b_by):
        missing_a = sorted(set(b_by) - set(a_by))
        missing_b = sorted(set(a_by) - set(b_by))
        raise ValueError(f"Assignment mismatch. missing_A={missing_a[:10]} missing_B={missing_b[:10]}")

    consensus = []
    arbitration = []
    for aid in sorted(a_by):
        a, b = a_by[aid], b_by[aid]
        reasons = arbitration_reasons(a, b)
        base = {
            "assignment_id": aid,
            "paper_id": a.get("paper_id") or b.get("paper_id") or "",
            "a_adjudicator_id": a.get("adjudicator_id", ""),
            "b_adjudicator_id": b.get("adjudicator_id", ""),
            "a_scientific_state": norm(a.get("scientific_state")),
            "b_scientific_state": norm(b.get("scientific_state")),
            "a_materiality": norm(a.get("materiality")),
            "b_materiality": norm(b.get("materiality")),
            "a_confidence": norm(a.get("review_confidence")),
            "b_confidence": norm(b.get("review_confidence")),
            "a_model_name": a.get("model_name", ""),
            "b_model_name": b.get("model_name", ""),
            "a_model_version": a.get("model_version_or_snapshot", ""),
            "b_model_version": b.get("model_version_or_snapshot", ""),
            "a_evidence_locator": a.get("evidence_locator", ""),
            "b_evidence_locator": b.get("evidence_locator", ""),
            "arbitration_reasons": "|".join(reasons),
        }
        if reasons:
            arbitration.append(base)
        else:
            consensus.append({
                **base,
                "consensus_scientific_state": norm(a.get("scientific_state")),
                "consensus_materiality": norm(a.get("materiality")),
                "label_provenance": "AI_DUAL_AGREEMENT_NOT_GOLD_STANDARD",
            })

    total = len(a_by)
    summary = {
        "classification": "AI_ADJUDICATION_AGREEMENT_QA_NOT_GOLD_STANDARD",
        "assignments_total": total,
        "automatic_consensus": len(consensus),
        "arbitration_required": len(arbitration),
        "automatic_consensus_fraction": len(consensus) / total if total else None,
        "warning": (
            "Model agreement is repeatability evidence, not proof of correctness. "
            "Final prevalence inference must model or sensitivity-test AI label error."
        ),
    }
    return consensus, arbitration, summary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("pass_a_csv", type=Path)
    p.add_argument("pass_b_csv", type=Path)
    p.add_argument("consensus_csv", type=Path)
    p.add_argument("arbitration_csv", type=Path)
    p.add_argument("summary_json", type=Path)
    args = p.parse_args()
    consensus, arbitration, summary = merge(read_csv(args.pass_a_csv), read_csv(args.pass_b_csv))
    write_csv(args.consensus_csv, consensus)
    write_csv(args.arbitration_csv, arbitration)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
