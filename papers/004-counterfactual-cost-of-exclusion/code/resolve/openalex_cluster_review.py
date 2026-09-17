#!/usr/bin/env python3
"""Detect likely OpenAlex author fragmentation before ARIS4C004 analysis.

OpenAlex may represent one historical person with multiple Author IDs. This
script consumes `openalex_resolution_audit.jsonl` and creates a conservative
review queue. It does NOT merge identities automatically.

Key design principle:
- coverage asks whether a candidate has enough graph data to be usable;
- identity precision asks whether the graph records truly belong to that person.

A person can have high apparent coverage while still failing identity review.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.casefold()
    value = value.replace("ß", "ss")
    value = re.sub(r"[^\w\s-]", " ", value)
    value = value.replace("_", " ").replace("-", " ")
    return " ".join(value.split())


def plausible_fragment_candidates(
    canonical_name: str,
    search_candidates: list[dict[str, Any]],
    min_name_score: float = 0.92,
) -> list[dict[str, Any]]:
    """Return records plausible enough to require joint identity review.

    This intentionally favors sensitivity for *review queue construction*.
    Inclusion here never means the IDs are accepted as belonging to one person.
    """
    canonical = normalize_name(canonical_name)
    plausible: list[dict[str, Any]] = []
    for candidate in search_candidates:
        display = str(candidate.get("display_name") or "")
        normalized = normalize_name(display)
        name_score = float(candidate.get("name_score") or 0.0)
        if not candidate.get("id"):
            continue
        if name_score >= min_name_score or (canonical and normalized == canonical):
            plausible.append(candidate)
    return plausible


def classify_record(record: dict[str, Any]) -> dict[str, Any]:
    name = str(record.get("canonical_name") or "")
    status = str(record.get("status") or "")
    method = str(record.get("method") or "")
    search_candidates = list(record.get("search_candidates") or [])
    plausible = plausible_fragment_candidates(name, search_candidates)

    ids = [str(item.get("id") or "") for item in plausible]
    works_counts = [int(item.get("works_count") or 0) for item in plausible]
    unique_names = sorted({normalize_name(str(item.get("display_name") or "")) for item in plausible})
    orcids = sorted({str(item.get("orcid")) for item in plausible if item.get("orcid")})

    if not search_candidates:
        review_class = "no_openalex_search_hit"
        action = "retain_in_candidate_frame_but_not_network_analytic_frame"
    elif len(plausible) >= 2:
        review_class = "possible_author_fragmentation"
        action = "manual_cluster_review_required"
    elif len(plausible) == 1 and status == "accepted":
        review_class = "single_plausible_author_record"
        action = "manual_identity_validation_required"
    elif len(plausible) == 1:
        review_class = "single_low_confidence_record"
        action = "manual_identity_validation_required"
    else:
        review_class = "name_collision_or_low_similarity"
        action = "manual_search_or_exclude_from_network_frame"

    # Multiple different non-empty ORCIDs are strong evidence *against* blindly
    # merging the OpenAlex IDs, even when display names match.
    if len(orcids) > 1:
        review_class = "possible_name_collision_conflicting_orcid"
        action = "do_not_merge_without_external_identity_evidence"

    return {
        "person_id": record.get("person_id", ""),
        "canonical_name": name,
        "wikidata_qid": record.get("wikidata_qid", ""),
        "birth_year": record.get("birth_year", ""),
        "death_year": record.get("death_year", ""),
        "resolver_status": status,
        "resolver_method": method,
        "review_class": review_class,
        "recommended_action": action,
        "plausible_openalex_ids_n": len(ids),
        "plausible_openalex_ids": ";".join(ids),
        "plausible_openalex_works_count_sum": sum(works_counts),
        "plausible_openalex_works_count_max": max(works_counts) if works_counts else 0,
        "normalized_name_variants_n": len(unique_names),
        "orcid_variants_n": len(orcids),
        "resolver_score": record.get("score", ""),
        "resolver_margin": record.get("margin", ""),
        "identity_verified": "false",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_jsonl", type=Path)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    args = parser.parse_args()

    records = [
        json.loads(line)
        for line in args.audit_jsonl.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    rows = [classify_record(record) for record in records]

    fields = [
        "person_id",
        "canonical_name",
        "wikidata_qid",
        "birth_year",
        "death_year",
        "resolver_status",
        "resolver_method",
        "review_class",
        "recommended_action",
        "plausible_openalex_ids_n",
        "plausible_openalex_ids",
        "plausible_openalex_works_count_sum",
        "plausible_openalex_works_count_max",
        "normalized_name_variants_n",
        "orcid_variants_n",
        "resolver_score",
        "resolver_margin",
        "identity_verified",
    ]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        key = str(row["review_class"])
        counts[key] = counts.get(key, 0) + 1

    apparent_network_leads = sum(
        int(row["plausible_openalex_works_count_sum"]) > 0 for row in rows
    )
    fragmentation_n = counts.get("possible_author_fragmentation", 0)
    summary = {
        "candidate_records_reviewed": len(rows),
        "review_class_counts": counts,
        "possible_author_fragmentation_n": fragmentation_n,
        "apparent_network_leads_n": apparent_network_leads,
        "apparent_network_leads_rate": apparent_network_leads / len(rows) if rows else 0.0,
        "identity_verified_n": 0,
        "identity_precision": None,
        "note": (
            "No automated row is identity-verified. Final analytic inclusion requires "
            "external/manual identity validation; multiple plausible OpenAlex IDs are "
            "treated as a cluster-review problem rather than selecting the top hit."
        ),
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
