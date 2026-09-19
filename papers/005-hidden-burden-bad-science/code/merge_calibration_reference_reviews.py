#!/usr/bin/env python3
"""Merge two independent calibration reference reviews into anchor candidates.

This merger is deliberately conservative:
- reviewer IDs must differ;
- prompt must be CAL-REF-V1;
- AI_A/AI_B/CIT adjudicator IDs are forbidden as reference reviewers;
- both reviewers must classify the same candidate identically;
- positive anchors require MATERIAL from both reviewers;
- negative anchors require SCIENTIFICALLY_UNAFFECTED from both reviewers;
- both reviews need primary evidence source/locator;
- final quality is the worse of the two reviewer qualities;
- only A/B consensuses become usable anchors; C remains descriptive;
- disagreements/unresolved cases do not enter Se/Sp calibration.

The merged output is still a machine-assisted reference set and should be
reported as such; it is not equivalent to independent human expert adjudication.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

STATES = {"SEVERE_SUPPORTED", "NON_SEVERE_SUPPORTED", "UNRESOLVED"}
DETAIL_STATES = {
    "SEVERE_SUPPORTED",
    "HONEST_MAJOR_ERROR",
    "MINOR_OR_IMMATERIAL",
    "NO_MATERIAL_PROBLEM_FOUND",
    "SERIOUS_UNRESOLVED",
    "INDETERMINATE",
}
NEGATIVE_DETAIL_STATES = {
    "HONEST_MAJOR_ERROR",
    "MINOR_OR_IMMATERIAL",
    "NO_MATERIAL_PROBLEM_FOUND",
}
UNRESOLVED_DETAIL_STATES = {"SERIOUS_UNRESOLVED", "INDETERMINATE"}
QUALITIES = {"A", "B", "C", "UNRESOLVED"}
MATERIALITY = {"MATERIAL", "IMMATERIAL", "SCIENTIFICALLY_UNAFFECTED", "UNKNOWN"}
ACCESS = {"FULL_PRIMARY", "PARTIAL_PRIMARY", "SECONDARY_ONLY", "NO_ACCESS"}
FORBIDDEN_REFERENCE_IDS = {
    "AI_A",
    "AI_B",
    "CIT_AI_A",
    "CIT_AI_B",
}

QUALITY_RANK = {"A": 1, "B": 2, "C": 3, "UNRESOLVED": 4}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else [
        "anchor_id",
        "candidate_id",
        "paper_id",
        "doi",
        "anchor_family",
        "reference_binary_state",
        "reference_scientific_state",
        "anchor_quality",
        "reviewer_a",
        "reviewer_b",
        "evidence_type",
        "evidence_source",
        "evidence_locator",
        "materiality_basis",
        "adjudication_blinded",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def norm(value: str | None) -> str:
    return (value or "").strip().upper()


def valid_detail_materiality(detail: str, materiality: str) -> bool:
    if detail == "SEVERE_SUPPORTED":
        return materiality == "MATERIAL"
    if detail == "HONEST_MAJOR_ERROR":
        return materiality == "MATERIAL"
    if detail == "MINOR_OR_IMMATERIAL":
        return materiality in {"IMMATERIAL", "SCIENTIFICALLY_UNAFFECTED"}
    if detail == "NO_MATERIAL_PROBLEM_FOUND":
        return materiality == "SCIENTIFICALLY_UNAFFECTED"
    if detail in UNRESOLVED_DETAIL_STATES:
        return materiality in MATERIALITY
    return False


def validate_review(row: dict[str, str]) -> None:
    cid = (row.get("candidate_id") or "").strip()
    if not cid:
        raise ValueError("candidate_id required")

    reviewer = (row.get("reference_reviewer_id") or "").strip()
    if not reviewer:
        raise ValueError(f"{cid}: reference_reviewer_id required")
    if reviewer in FORBIDDEN_REFERENCE_IDS:
        raise ValueError(
            f"{cid}: article/citation adjudicator cannot serve as reference reviewer"
        )
    if (row.get("prompt_version") or "").strip() != "CAL-REF-V1":
        raise ValueError(f"{cid}: prompt_version must be CAL-REF-V1")

    state = norm(row.get("reference_state"))
    detail = norm(row.get("reference_scientific_state_detail"))
    quality = norm(row.get("anchor_quality"))
    materiality = norm(row.get("materiality_assessment"))
    access = norm(row.get("evidence_access"))

    if state not in STATES:
        raise ValueError(f"{cid}: invalid reference_state {state!r}")
    if detail not in DETAIL_STATES:
        raise ValueError(f"{cid}: invalid reference_scientific_state_detail {detail!r}")
    if state == "SEVERE_SUPPORTED" and detail != "SEVERE_SUPPORTED":
        raise ValueError(f"{cid}: severe binary state/detail mismatch")
    if state == "NON_SEVERE_SUPPORTED" and detail not in NEGATIVE_DETAIL_STATES:
        raise ValueError(f"{cid}: non-severe binary state/detail mismatch")
    if state == "UNRESOLVED" and detail not in UNRESOLVED_DETAIL_STATES:
        raise ValueError(f"{cid}: unresolved binary state/detail mismatch")
    if quality not in QUALITIES:
        raise ValueError(f"{cid}: invalid anchor_quality {quality!r}")
    if materiality not in MATERIALITY:
        raise ValueError(f"{cid}: invalid materiality_assessment {materiality!r}")
    if access not in ACCESS:
        raise ValueError(f"{cid}: invalid evidence_access {access!r}")

    if state == "UNRESOLVED":
        if not (row.get("abstain_reason") or "").strip():
            raise ValueError(f"{cid}: UNRESOLVED requires abstain_reason")
        return

    for field in (
        "model_name",
        "model_version_or_snapshot",
        "run_id",
        "evidence_type",
        "evidence_source",
        "evidence_locator",
        "brief_evidence_rationale",
    ):
        if not (row.get(field) or "").strip():
            raise ValueError(f"{cid}: missing required {field}")

    if not valid_detail_materiality(detail, materiality):
        raise ValueError(
            f"{cid}: materiality {materiality!r} is inconsistent with detailed state {detail!r}"
        )


def index_reviews(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        validate_review(row)
        cid = (row.get("candidate_id") or "").strip()
        if cid in out:
            raise ValueError(f"duplicate candidate_id in review file: {cid}")
        out[cid] = row
    return out


def worse_quality(a: str, b: str) -> str:
    return max((a, b), key=lambda q: QUALITY_RANK[q])


def merge_reference_reviews(
    a_rows: list[dict[str, str]],
    b_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    a = index_reviews(a_rows)
    b = index_reviews(b_rows)

    if set(a) != set(b):
        missing_a = sorted(set(b) - set(a))
        missing_b = sorted(set(a) - set(b))
        raise ValueError(
            f"candidate mismatch; missing_a={missing_a[:5]}, missing_b={missing_b[:5]}"
        )

    anchors: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()

    for cid in sorted(a):
        ra, rb = a[cid], b[cid]
        reviewer_a = (ra.get("reference_reviewer_id") or "").strip()
        reviewer_b = (rb.get("reference_reviewer_id") or "").strip()
        if reviewer_a == reviewer_b:
            raise ValueError(f"{cid}: reference reviewers must be independent IDs")

        state_a = norm(ra.get("reference_state"))
        state_b = norm(rb.get("reference_state"))
        detail_a = norm(ra.get("reference_scientific_state_detail"))
        detail_b = norm(rb.get("reference_scientific_state_detail"))
        quality_a = norm(ra.get("anchor_quality"))
        quality_b = norm(rb.get("anchor_quality"))

        if "UNRESOLVED" in {state_a, state_b}:
            status_counts["UNRESOLVED_BY_REVIEW"] += 1
            continue
        if state_a != state_b:
            status_counts["STATE_DISAGREEMENT"] += 1
            continue
        if detail_a != detail_b:
            status_counts["DETAIL_DISAGREEMENT"] += 1
            continue

        final_quality = worse_quality(quality_a, quality_b)
        if final_quality == "UNRESOLVED":
            status_counts["QUALITY_UNRESOLVED"] += 1
            continue
        if final_quality == "C":
            status_counts["CONSENSUS_C_DESCRIPTIVE_ONLY"] += 1
            continue

        materiality_a = norm(ra.get("materiality_assessment"))
        materiality_b = norm(rb.get("materiality_assessment"))

        if (
            not valid_detail_materiality(detail_a, materiality_a)
            or not valid_detail_materiality(detail_b, materiality_b)
        ):
            status_counts["MATERIALITY_MISMATCH"] += 1
            continue

        if state_a == "SEVERE_SUPPORTED":
            family = "P+"
            binary = 1
        else:
            family = "N+"
            binary = 0
        scientific_state = detail_a

        evidence_source = " | ".join(
            sorted(
                {
                    (ra.get("evidence_source") or "").strip(),
                    (rb.get("evidence_source") or "").strip(),
                }
                - {""}
            )
        )
        evidence_locator = " | ".join(
            sorted(
                {
                    (ra.get("evidence_locator") or "").strip(),
                    (rb.get("evidence_locator") or "").strip(),
                }
                - {""}
            )
        )
        evidence_type = " | ".join(
            sorted(
                {
                    (ra.get("evidence_type") or "").strip(),
                    (rb.get("evidence_type") or "").strip(),
                }
                - {""}
            )
        )

        anchor_id = "CAL_" + cid.replace("CALC_", "")
        anchors.append(
            {
                "anchor_id": anchor_id,
                "candidate_id": cid,
                "paper_id": (ra.get("paper_id") or rb.get("paper_id") or "").strip(),
                "doi": (ra.get("doi") or rb.get("doi") or "").strip(),
                "anchor_family": family,
                "reference_binary_state": binary,
                "reference_scientific_state": scientific_state,
                "anchor_quality": final_quality,
                "reviewer_a": reviewer_a,
                "reviewer_b": reviewer_b,
                "evidence_type": evidence_type,
                "evidence_source": evidence_source,
                "evidence_locator": evidence_locator,
                "materiality_basis": materiality_a,
                "adjudication_blinded": 1,
                "notes": (
                    "machine-assisted dual-reference consensus; "
                    "report separately from independent human expert adjudication"
                ),
            }
        )
        status_counts[f"ANCHOR_{family}_{final_quality}"] += 1

    summary = {
        "classification": "DUAL_MACHINE_REFERENCE_CONSENSUS_NOT_HUMAN_GOLD_STANDARD",
        "candidates_input": len(a),
        "anchors_output": len(anchors),
        "status_counts": dict(status_counts),
        "primary_calibration_A_only": sum(
            1 for x in anchors if x["anchor_quality"] == "A"
        ),
        "sensitivity_calibration_A_or_B": len(anchors),
        "warnings": [
            "Dual machine-reference consensus is not equivalent to independent human expert adjudication.",
            "Reference reviewers can share model/data biases even when reviewer IDs differ.",
            "Primary accuracy estimation should use A anchors; A+B is sensitivity analysis.",
            "State disagreements, unresolved reviews and C-quality consensuses are excluded from Se/Sp calibration.",
            "Reference reviewers must remain blinded to AI_A/AI_B outputs and candidate queue labels.",
        ],
    }
    return anchors, summary


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("review_a_csv", type=Path)
    p.add_argument("review_b_csv", type=Path)
    p.add_argument("anchors_csv", type=Path)
    p.add_argument("summary_json", type=Path)
    args = p.parse_args()

    anchors, summary = merge_reference_reviews(
        read_csv(args.review_a_csv),
        read_csv(args.review_b_csv),
    )
    write_csv(args.anchors_csv, anchors)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
