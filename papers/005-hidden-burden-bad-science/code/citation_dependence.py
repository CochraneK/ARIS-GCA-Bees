#!/usr/bin/env python3
"""Validate and summarize semantically adjudicated citation-dependence edges.

This module never infers semantic dependence from citation existence alone.
It consumes completed edge adjudications and reports exposure, material
dependence, methodological dependence, corrective citations and unresolved
context separately.
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
from pathlib import Path
from typing import Any

SEMANTIC_CLASSES = {
    "BACKGROUND_MENTION",
    "METHOD_REUSE",
    "RESULT_DEPENDENCE",
    "EVIDENCE_SYNTHESIS_INCLUDE",
    "CRITIQUE_OR_CORRECTION",
    "CITATION_ONLY_OR_PERIPHERAL",
    "INDETERMINATE",
}
TRI = {"YES", "NO", "UNKNOWN"}
CONTEXT_ACCESS = {"FULLTEXT", "ABSTRACT_ONLY", "NO_CONTEXT"}
CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}

PRIMARY_MATERIAL_CLASSES = {
    "RESULT_DEPENDENCE",
    "EVIDENCE_SYNTHESIS_INCLUDE",
}


def norm(value: str | None) -> str:
    return (value or "").strip().upper()


def validate_edge(row: dict[str, str]) -> list[str]:
    edge = row.get("edge_id") or "<missing>"
    errors: list[str] = []

    if not row.get("edge_id"):
        errors.append("missing edge_id")

    semantic = norm(row.get("semantic_class"))
    if semantic not in SEMANTIC_CLASSES:
        errors.append(f"{edge}: invalid semantic_class={semantic!r}")

    for field in (
        "component_implicated",
        "material_to_downstream_claim",
        "source_retraction_known_in_text",
    ):
        value = norm(row.get(field))
        if value not in TRI:
            errors.append(f"{edge}: invalid {field}={value!r}")

    access = norm(row.get("context_access"))
    if access not in CONTEXT_ACCESS:
        errors.append(f"{edge}: invalid context_access={access!r}")

    confidence = norm(row.get("review_confidence"))
    if confidence not in CONFIDENCE:
        errors.append(f"{edge}: invalid review_confidence={confidence!r}")

    after = norm(row.get("citation_after_retraction"))
    if after not in TRI:
        errors.append(f"{edge}: invalid citation_after_retraction={after!r}")

    return errors


def is_primary_scf(row: dict[str, str]) -> bool:
    return (
        norm(row.get("semantic_class")) in PRIMARY_MATERIAL_CLASSES
        and norm(row.get("material_to_downstream_claim")) == "YES"
    )


def is_methodological_contamination(row: dict[str, str]) -> bool:
    return (
        norm(row.get("semantic_class")) == "METHOD_REUSE"
        and norm(row.get("component_implicated")) == "YES"
        and norm(row.get("material_to_downstream_claim")) == "YES"
    )


def summarize(rows: list[dict[str, str]]) -> dict[str, Any]:
    errors: list[str] = []
    seen: set[str] = set()
    for row in rows:
        edge_id = row.get("edge_id") or ""
        if edge_id in seen and edge_id:
            errors.append(f"duplicate edge_id={edge_id}")
        seen.add(edge_id)
        errors.extend(validate_edge(row))

    if errors:
        raise ValueError(
            "Citation-edge adjudication validation failed:\n" + "\n".join(errors[:100])
        )

    semantic_counts = collections.Counter(norm(r.get("semantic_class")) for r in rows)
    access_counts = collections.Counter(norm(r.get("context_access")) for r in rows)
    source_ids = {r.get("source_openalex_id") for r in rows if r.get("source_openalex_id")}
    citing_ids = {r.get("citing_openalex_id") for r in rows if r.get("citing_openalex_id")}

    primary_scf_edges = [r for r in rows if is_primary_scf(r)]
    method_edges = [r for r in rows if is_methodological_contamination(r)]
    corrective = [
        r for r in rows
        if norm(r.get("semantic_class")) == "CRITIQUE_OR_CORRECTION"
    ]
    unresolved = [
        r for r in rows
        if norm(r.get("semantic_class")) == "INDETERMINATE"
        or norm(r.get("material_to_downstream_claim")) == "UNKNOWN"
    ]

    post_primary = [
        r for r in primary_scf_edges
        if norm(r.get("citation_after_retraction")) == "YES"
    ]
    known_retraction_primary = [
        r for r in primary_scf_edges
        if norm(r.get("source_retraction_known_in_text")) == "YES"
    ]

    return {
        "classification": "SEMANTIC_CITATION_DEPENDENCE_SUMMARY",
        "adjudicated_edges": len(rows),
        "unique_sources": len(source_ids),
        "unique_citing_works": len(citing_ids),
        "semantic_class_counts": dict(semantic_counts),
        "context_access_counts": dict(access_counts),
        "primary_scf_material_dependence_edges": len(primary_scf_edges),
        "primary_scf_unique_citing_works": len(
            {r.get("citing_openalex_id") for r in primary_scf_edges}
        ),
        "method_reuse_with_implicated_component_edges": len(method_edges),
        "corrective_or_critique_edges": len(corrective),
        "unresolved_or_materiality_unknown_edges": len(unresolved),
        "post_retraction_primary_scf_edges": len(post_primary),
        "primary_scf_edges_explicitly_acknowledging_retraction": len(
            known_retraction_primary
        ),
        "warnings": [
            "This is semantic dependence among adjudicated citation edges, not global prevalence.",
            "Raw citation exposure must be reported separately from SCF.",
            "Critique/correction citations are not contamination.",
            "METHOD_REUSE is kept separate from primary result/evidence dependence.",
            "INDETERMINATE and UNKNOWN materiality are retained rather than recoded as clean.",
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("adjudicated_edges_csv", type=Path)
    p.add_argument("output_json", type=Path)
    args = p.parse_args()

    with args.adjudicated_edges_csv.open(
        "r", encoding="utf-8-sig", newline=""
    ) as f:
        rows = list(csv.DictReader(f))

    result = summarize(rows)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
