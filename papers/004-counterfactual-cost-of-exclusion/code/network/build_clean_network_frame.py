#!/usr/bin/env python3
"""Build the pre-exposure clean network frame for ARIS4C004.

Inputs are already identity-reviewed and work-reviewed. This script does not use
mental-health information and does not infer new identity/work decisions.

For each network-observable person:
- if explicit work decisions exist, retain only KEEP rows;
- otherwise retain candidate-lifetime-plausible works from the verified corpus;
- preserve citation/authorship/institution/topic provenance;
- orient internal citation edges as cited work -> citing work (knowledge-flow direction);
- report metadata coverage and temporal anomalies without hiding them.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

KEEP = {"KEEP_ORIGINAL", "KEEP_POSTHUMOUS_ORIGINAL"}


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def split_ids(value: str | None) -> set[str]:
    return {x.strip().rstrip("/").split("/")[-1] for x in (value or "").split(";") if x.strip()}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def choose_clean_works(
    corpus: list[dict[str, Any]],
    identities: list[dict[str, str]],
    work_decisions: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    identity_by_person = {row["person_id"]: row for row in identities}
    released = {pid for pid, row in identity_by_person.items() if truthy(row.get("network_observable"))}

    decision_by_key: dict[tuple[str, str], dict[str, str]] = {}
    decisions_by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in work_decisions:
        key = (row["person_id"], row["openalex_work_id"])
        decision_by_key[key] = row
        decisions_by_person[row["person_id"]].append(row)

    corpus_by_key = {(str(row.get("person_id") or ""), str(row.get("openalex_work_id") or "")): row for row in corpus}
    clean: list[dict[str, Any]] = []

    for pid in sorted(released):
        identity = identity_by_person[pid]
        focal_ids = split_ids(identity.get("verified_openalex_ids"))
        explicit = decisions_by_person.get(pid, [])
        if explicit:
            keep_ids = {row["openalex_work_id"] for row in explicit if row.get("work_decision") in KEEP and truthy(row.get("include_in_network"))}
            for wid in sorted(keep_ids):
                row = corpus_by_key.get((pid, wid))
                if not row:
                    errors.append(f"{pid}: retained work {wid} missing from verified corpus")
                    continue
                item = dict(row)
                item["clean_selection_basis"] = "explicit_work_decision"
                item["work_decision"] = decision_by_key[(pid, wid)].get("work_decision")
                item["focal_verified_author_ids"] = sorted(focal_ids)
                clean.append(item)
        else:
            rows = [
                row for row in corpus
                if str(row.get("person_id") or "") == pid and row.get("temporal_status") == "plausible"
            ]
            if not rows:
                errors.append(f"{pid}: network_observable=true but no plausible verified works")
            for row in rows:
                item = dict(row)
                item["clean_selection_basis"] = "identity_released_plausible_window"
                item["work_decision"] = "IMPLICIT_KEEP_PLAUSIBLE"
                item["focal_verified_author_ids"] = sorted(focal_ids)
                clean.append(item)

    return clean, errors


def person_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    first = rows[0]
    focal_ids = set(first.get("focal_verified_author_ids") or [])
    years = [int(row["publication_year"]) for row in rows if row.get("publication_year") is not None]
    ref_rows = [row for row in rows if row.get("referenced_work_ids")]
    coauthor_rows = []
    coauthors: set[str] = set()
    institutions: set[str] = set()
    topics: set[str] = set()
    cited_counts: list[int] = []
    for row in rows:
        author_ids = set(row.get("authorship_author_ids") or [])
        external = author_ids - focal_ids
        if external:
            coauthor_rows.append(row)
            coauthors.update(external)
        institutions.update(row.get("institution_ids") or [])
        topics.update(row.get("topic_ids") or [])
        cited_counts.append(int(row.get("cited_by_count") or 0))

    return {
        "person_id": first.get("person_id"),
        "canonical_name": first.get("canonical_name"),
        "clean_work_n": len(rows),
        "publication_year_min": min(years) if years else None,
        "publication_year_max": max(years) if years else None,
        "publication_span_years": (max(years) - min(years)) if len(years) >= 2 else 0,
        "works_with_references_n": len(ref_rows),
        "reference_metadata_coverage": len(ref_rows) / len(rows) if rows else 0.0,
        "outgoing_reference_links_n": sum(len(row.get("referenced_work_ids") or []) for row in rows),
        "works_with_external_coauthors_n": len(coauthor_rows),
        "coauthor_metadata_coverage": len(coauthor_rows) / len(rows) if rows else 0.0,
        "unique_external_coauthors_n": len(coauthors),
        "unique_institutions_n": len(institutions),
        "unique_topics_n": len(topics),
        "cited_by_count_total": sum(cited_counts),
        "cited_by_count_median": statistics.median(cited_counts) if cited_counts else 0,
        "selection_basis_counts": dict(Counter(str(row.get("clean_selection_basis") or "") for row in rows)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--identities", type=Path, required=True)
    parser.add_argument("--work-decisions", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    corpus = read_jsonl(args.corpus)
    identities = read_csv(args.identities)
    work_decisions = read_csv(args.work_decisions)

    clean, errors = choose_clean_works(corpus, identities, work_decisions)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    by_person: dict[str, list[dict[str, Any]]] = defaultdict(list)
    clean_ids: set[str] = set()
    for row in clean:
        by_person[str(row["person_id"])].append(row)
        if row.get("openalex_work_id"):
            clean_ids.add(str(row["openalex_work_id"]))

    internal_edges: list[dict[str, Any]] = []
    temporal_anomalies: list[dict[str, Any]] = []
    year_by_work = {str(row.get("openalex_work_id")): row.get("publication_year") for row in clean}
    owner_by_work = {str(row.get("openalex_work_id")): str(row.get("person_id")) for row in clean}

    for row in clean:
        citing = str(row.get("openalex_work_id") or "")
        citing_year = row.get("publication_year")
        for cited in row.get("referenced_work_ids") or []:
            if cited not in clean_ids:
                continue
            cited_year = year_by_work.get(cited)
            edge = {
                "source_work_id": cited,
                "target_work_id": citing,
                "source_person_id": owner_by_work.get(cited, ""),
                "target_person_id": str(row.get("person_id") or ""),
                "source_year": cited_year,
                "target_year": citing_year,
                "edge_type": "citation_knowledge_flow",
            }
            if cited_year is not None and citing_year is not None and int(cited_year) > int(citing_year):
                temporal_anomalies.append(edge)
                continue
            internal_edges.append(edge)

    person_rows = [person_summary(rows) for _, rows in sorted(by_person.items())]

    with (args.out_dir / "clean_work_corpus.jsonl").open("w", encoding="utf-8") as handle:
        for row in clean:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary_fields = list(person_rows[0].keys()) if person_rows else [
        "person_id", "canonical_name", "clean_work_n"
    ]
    with (args.out_dir / "clean_person_network_summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(person_rows)

    edge_fields = [
        "source_work_id",
        "target_work_id",
        "source_person_id",
        "target_person_id",
        "source_year",
        "target_year",
        "edge_type",
    ]
    with (args.out_dir / "internal_citation_edges.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=edge_fields)
        writer.writeheader()
        writer.writerows(internal_edges)

    with (args.out_dir / "citation_temporal_anomalies.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=edge_fields)
        writer.writeheader()
        writer.writerows(temporal_anomalies)

    clean_n = len(clean)
    works_with_refs = sum(bool(row.get("referenced_work_ids")) for row in clean)
    works_with_topics = sum(bool(row.get("topic_ids")) for row in clean)
    works_with_institutions = sum(bool(row.get("institution_ids")) for row in clean)
    works_with_coauthors = 0
    all_external_coauthors: set[str] = set()
    for row in clean:
        focal = set(row.get("focal_verified_author_ids") or [])
        external = set(row.get("authorship_author_ids") or []) - focal
        if external:
            works_with_coauthors += 1
            all_external_coauthors.update(external)

    overall = {
        "network_observable_people_n": len(by_person),
        "clean_work_n": clean_n,
        "works_with_reference_metadata_n": works_with_refs,
        "reference_metadata_coverage": works_with_refs / clean_n if clean_n else 0.0,
        "works_with_topic_metadata_n": works_with_topics,
        "topic_metadata_coverage": works_with_topics / clean_n if clean_n else 0.0,
        "works_with_institution_metadata_n": works_with_institutions,
        "institution_metadata_coverage": works_with_institutions / clean_n if clean_n else 0.0,
        "works_with_external_coauthors_n": works_with_coauthors,
        "coauthor_metadata_coverage": works_with_coauthors / clean_n if clean_n else 0.0,
        "unique_external_coauthors_n": len(all_external_coauthors),
        "internal_clean_citation_edges_n": len(internal_edges),
        "within_person_internal_citation_edges_n": sum(
            edge["source_person_id"] == edge["target_person_id"] for edge in internal_edges
        ),
        "cross_person_internal_citation_edges_n": sum(
            edge["source_person_id"] != edge["target_person_id"] for edge in internal_edges
        ),
        "internal_citation_temporal_anomalies_n": len(temporal_anomalies),
        "temporal_anomalies_excluded_from_graph": True,
        "build_errors_n": len(errors),
        "errors": errors,
        "interpretation_note": (
            "Internal focal-to-focal citation density is not the intended final CPE graph. "
            "This frame tests whether clean focal works retain enough metadata to support "
            "bounded downstream-neighborhood acquisition."
        ),
    }
    (args.out_dir / "clean_network_overall.json").write_text(
        json.dumps(overall, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(overall, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
