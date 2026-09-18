#!/usr/bin/env python3
"""Create blinded dual-AI citation-edge adjudication packets for ARIS4C005.

Input is the private row-level edge CSV produced by build_contamination_exposure.py.
The script never labels an edge. It creates two independent assignment rows per
edge and a manager linkage containing the source sampling/provenance columns.

The reviewer packet exposes identifiers needed to find citation context, but not
any model prediction or semantic label.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

VISIBLE = [
    "edge_id",
    "source_openalex_id",
    "source_doi",
    "source_retraction_date",
    "citing_openalex_id",
    "citing_doi",
    "citing_title",
    "citing_publication_date",
    "citing_work_type",
    "citing_domain",
    "citing_field",
    "citing_subfield",
    "citing_has_fulltext",
    "citing_is_oa",
    "citation_after_retraction",
]

OUTPUT_BLANKS = [
    "semantic_class",
    "component_implicated",
    "material_to_downstream_claim",
    "source_retraction_known_in_text",
    "context_access",
    "review_confidence",
    "evidence_locator",
    "brief_evidence_rationale",
    "abstain_reason",
]


def assignment_id(edge_id: str, adjudicator_id: str) -> str:
    raw = f"{edge_id}|{adjudicator_id}|CIT-EDGE-V1".encode("utf-8")
    return "C" + hashlib.sha256(raw).hexdigest()[:18]


def make_packets(
    rows: list[dict[str, str]],
    adjudicators: list[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, Any]]:
    if len(adjudicators) < 2:
        raise ValueError("At least two adjudicators are required for dual-AI citation review")

    seen_edges: set[str] = set()
    reviewers: list[dict[str, str]] = []
    linkage: list[dict[str, str]] = []

    for row in rows:
        eid = (row.get("edge_id") or "").strip()
        if not eid:
            raise ValueError("Edge missing edge_id")
        if eid in seen_edges:
            raise ValueError(f"Duplicate edge_id: {eid}")
        seen_edges.add(eid)

        for adjudicator in adjudicators:
            aid = assignment_id(eid, adjudicator)
            visible = {
                "assignment_id": aid,
                **{k: row.get(k, "") for k in VISIBLE},
                "adjudicator_id": adjudicator,
                "prompt_version": "CIT-EDGE-V1",
                "model_name": "",
                "model_version_or_snapshot": "",
                "run_id": "",
            }
            for k in OUTPUT_BLANKS:
                visible[k] = ""
            reviewers.append(visible)

            hidden = {
                "assignment_id": aid,
                "edge_id": eid,
                "adjudicator_id": adjudicator,
                "prompt_version": "CIT-EDGE-V1",
            }
            # Preserve every original column for lossless post-review linkage.
            for key, value in row.items():
                hidden[f"source_{key}" if key in hidden else key] = value
            linkage.append(hidden)

    reviewers.sort(key=lambda r: (r["adjudicator_id"], r["assignment_id"]))
    linkage.sort(key=lambda r: r["assignment_id"])

    summary = {
        "classification": "CITATION_EDGE_AI_PACKET_NO_ADJUDICATION_RESULTS",
        "unique_edges": len(rows),
        "adjudicators": adjudicators,
        "assignments_total": len(reviewers),
        "assignments_by_adjudicator": dict(
            Counter(r["adjudicator_id"] for r in reviewers)
        ),
        "fulltext_signal_edges": sum(
            int((r.get("citing_has_fulltext") or "0") == "1") for r in rows
        ),
        "oa_signal_edges": sum(
            int((r.get("citing_is_oa") or "0") == "1") for r in rows
        ),
        "warnings": [
            "This packet contains no semantic contamination labels.",
            "Full-text/OA metadata are access signals, not evidence of dependence.",
            "Two AI passes are repeatability measurements, not gold-standard truth.",
            "Unavailable citation context must remain INDETERMINATE rather than clean.",
        ],
    }
    return reviewers, linkage, summary


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    seen: set[str] = set()
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
    p.add_argument("edges_csv", type=Path)
    p.add_argument("reviewer_csv", type=Path)
    p.add_argument("linkage_csv", type=Path)
    p.add_argument("summary_json", type=Path)
    p.add_argument("--adjudicator", action="append", default=[])
    args = p.parse_args()

    with args.edges_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    adjudicators = args.adjudicator or ["CIT_AI_A", "CIT_AI_B"]
    reviewers, linkage, summary = make_packets(rows, adjudicators)
    write_csv(args.reviewer_csv, reviewers)
    write_csv(args.linkage_csv, linkage)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
