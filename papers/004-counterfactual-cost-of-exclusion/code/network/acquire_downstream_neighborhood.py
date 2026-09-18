#!/usr/bin/env python3
"""Acquire bounded one-hop downstream citation neighborhoods for ARIS4C004.

The input clean work corpus is already pre-exposure and mental-health blind.
This pilot asks a narrower feasibility question:

Can OpenAlex provide enough temporally ordered citing works around a deterministic
set of focal works to support later counterfactual propagation modeling?

Anchor selection is deterministic and avoids choosing only famous works:
- earliest clean work;
- temporal median clean work;
- latest clean work;
- then highest-cited remaining works until the requested anchor count is met.

For each anchor, the script queries OpenAlex works that cite it within a fixed
post-publication horizon. Time-reversed records are quarantined as anomalies and
never enter the downstream graph.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ACQUIRE = Path(__file__).resolve().parents[1] / "acquire"
sys.path.insert(0, str(ACQUIRE))
from openalex_pilot import OpenAlexClient, normalize_openalex_id  # noqa: E402


def parse_year(value: Any) -> int | None:
    try:
        year = int(float(value))
    except (TypeError, ValueError):
        return None
    return year if 1000 <= year <= 2200 else None


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def unique(values: list[str]) -> list[str]:
    return sorted({x for x in values if x})


def work_id(work: dict[str, Any]) -> str:
    return normalize_openalex_id(str(work.get("openalex_work_id") or work.get("id") or ""))


def select_anchors(rows: list[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    """Deterministically select temporally spread + high-citation focal works."""
    usable = [row for row in rows if parse_year(row.get("publication_year")) is not None and work_id(row)]
    if not usable or n <= 0:
        return []
    usable = sorted(
        usable,
        key=lambda row: (
            int(row["publication_year"]),
            work_id(row),
        ),
    )

    selected: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(row: dict[str, Any]) -> None:
        wid = work_id(row)
        if wid and wid not in seen and len(selected) < n:
            seen.add(wid)
            selected.append(row)

    add(usable[0])
    add(usable[len(usable) // 2])
    add(usable[-1])

    for row in sorted(
        usable,
        key=lambda row: (
            -int(row.get("cited_by_count") or 0),
            int(row["publication_year"]),
            work_id(row),
        ),
    ):
        add(row)
        if len(selected) >= n:
            break

    return selected


def extract_citing_metadata(work: dict[str, Any]) -> dict[str, Any]:
    authors: list[str] = []
    institutions: list[str] = []
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        aid = normalize_openalex_id(str(author.get("id") or ""))
        if aid:
            authors.append(aid)
        for inst in authorship.get("institutions") or []:
            iid = normalize_openalex_id(str(inst.get("id") or ""))
            if iid:
                institutions.append(iid)

    topics = [
        normalize_openalex_id(str(topic.get("id") or ""))
        for topic in (work.get("topics") or [])
        if topic.get("id")
    ]
    return {
        "citing_author_ids": unique(authors),
        "citing_institution_ids": unique(institutions),
        "citing_topic_ids": unique(topics),
        "primary_topic_id": normalize_openalex_id(
            str((work.get("primary_topic") or {}).get("id") or "")
        ),
        "primary_topic_name": str((work.get("primary_topic") or {}).get("display_name") or ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean-corpus", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--anchors-per-person", type=int, default=6)
    parser.add_argument("--horizon-years", type=int, default=20)
    parser.add_argument("--study-end-year", type=int, default=2026)
    parser.add_argument("--max-citers-per-anchor", type=int, default=50)
    parser.add_argument("--sleep-rps", type=float, default=2.0)
    args = parser.parse_args()

    clean = read_jsonl(args.clean_corpus)
    by_person: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in clean:
        by_person[str(row.get("person_id") or "")].append(row)

    client = OpenAlexClient(
        api_key=os.getenv("OPENALEX_API_KEY") or None,
        requests_per_second=args.sleep_rps,
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)

    edge_rows: list[dict[str, Any]] = []
    anomaly_rows: list[dict[str, Any]] = []
    downstream_by_person_work: dict[tuple[str, str], dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    anchor_summary: list[dict[str, Any]] = []

    for pid, rows in sorted(by_person.items()):
        name = str(rows[0].get("canonical_name") or "")
        anchors = select_anchors(rows, args.anchors_per_person)
        for anchor in anchors:
            aid = work_id(anchor)
            anchor_year = parse_year(anchor.get("publication_year"))
            if anchor_year is None:
                continue
            year_max = min(args.study_end_year, anchor_year + args.horizon_years)
            returned = 0
            valid_edges = 0
            anomaly_n = 0
            try:
                for citing in client.iter_citing_works(
                    aid,
                    year_min=anchor_year,
                    year_max=year_max,
                    max_works=args.max_citers_per_anchor,
                ):
                    returned += 1
                    citing_id = normalize_openalex_id(str(citing.get("id") or ""))
                    citing_year = parse_year(citing.get("publication_year"))
                    if not citing_id or citing_id == aid:
                        continue
                    meta = extract_citing_metadata(citing)
                    edge = {
                        "person_id": pid,
                        "canonical_name": name,
                        "anchor_work_id": aid,
                        "anchor_year": anchor_year,
                        "anchor_cited_by_count": int(anchor.get("cited_by_count") or 0),
                        "citing_work_id": citing_id,
                        "citing_year": citing_year,
                        "citation_lag_years": (
                            citing_year - anchor_year if citing_year is not None else None
                        ),
                        "citing_title": str(citing.get("display_name") or ""),
                        "citing_cited_by_count": int(citing.get("cited_by_count") or 0),
                        "primary_topic_id": meta["primary_topic_id"],
                        "primary_topic_name": meta["primary_topic_name"],
                    }
                    if citing_year is not None and citing_year < anchor_year:
                        anomaly_rows.append(edge)
                        anomaly_n += 1
                        continue

                    edge_rows.append(edge)
                    valid_edges += 1
                    key = (pid, citing_id)
                    record = downstream_by_person_work.get(key)
                    if record is None:
                        record = {
                            "person_id": pid,
                            "canonical_name": name,
                            "citing_work_id": citing_id,
                            "citing_year": citing_year,
                            "citing_title": str(citing.get("display_name") or ""),
                            "citing_cited_by_count": int(citing.get("cited_by_count") or 0),
                            "primary_topic_id": meta["primary_topic_id"],
                            "primary_topic_name": meta["primary_topic_name"],
                            "citing_author_ids": meta["citing_author_ids"],
                            "citing_institution_ids": meta["citing_institution_ids"],
                            "citing_topic_ids": meta["citing_topic_ids"],
                            "anchor_work_ids": [],
                        }
                        downstream_by_person_work[key] = record
                    record["anchor_work_ids"] = unique(record["anchor_work_ids"] + [aid])
            except Exception as exc:
                errors.append(
                    {
                        "person_id": pid,
                        "canonical_name": name,
                        "anchor_work_id": aid,
                        "error": f"{type(exc).__name__}:{exc}",
                    }
                )

            anchor_summary.append(
                {
                    "person_id": pid,
                    "canonical_name": name,
                    "anchor_work_id": aid,
                    "anchor_year": anchor_year,
                    "anchor_cited_by_count": int(anchor.get("cited_by_count") or 0),
                    "window_end_year": year_max,
                    "api_rows_returned_n": returned,
                    "valid_downstream_edges_n": valid_edges,
                    "temporal_anomalies_n": anomaly_n,
                }
            )

    downstream_rows = list(downstream_by_person_work.values())

    person_summaries: list[dict[str, Any]] = []
    for pid, rows in sorted(by_person.items()):
        name = str(rows[0].get("canonical_name") or "")
        anchors = [row for row in anchor_summary if row["person_id"] == pid]
        downstream = [row for row in downstream_rows if row["person_id"] == pid]
        edges = [row for row in edge_rows if row["person_id"] == pid]
        lags = [
            int(row["citation_lag_years"])
            for row in edges
            if row.get("citation_lag_years") is not None
        ]
        authors = {a for row in downstream for a in row.get("citing_author_ids") or []}
        institutions = {a for row in downstream for a in row.get("citing_institution_ids") or []}
        topics = {a for row in downstream for a in row.get("citing_topic_ids") or []}
        person_summaries.append(
            {
                "person_id": pid,
                "canonical_name": name,
                "clean_work_n": len(rows),
                "anchors_n": len(anchors),
                "anchors_with_downstream_n": sum(row["valid_downstream_edges_n"] > 0 for row in anchors),
                "downstream_edge_n": len(edges),
                "downstream_unique_work_n": len(downstream),
                "downstream_unique_author_n": len(authors),
                "downstream_unique_institution_n": len(institutions),
                "downstream_unique_topic_n": len(topics),
                "citation_lag_median_years": statistics.median(lags) if lags else None,
                "citation_lag_max_years": max(lags) if lags else None,
            }
        )

    edge_fields = [
        "person_id",
        "canonical_name",
        "anchor_work_id",
        "anchor_year",
        "anchor_cited_by_count",
        "citing_work_id",
        "citing_year",
        "citation_lag_years",
        "citing_title",
        "citing_cited_by_count",
        "primary_topic_id",
        "primary_topic_name",
    ]
    with (args.out_dir / "downstream_edges.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=edge_fields)
        writer.writeheader()
        writer.writerows(edge_rows)

    with (args.out_dir / "downstream_temporal_anomalies.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=edge_fields)
        writer.writeheader()
        writer.writerows(anomaly_rows)

    with (args.out_dir / "downstream_works.jsonl").open("w", encoding="utf-8") as handle:
        for row in downstream_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    if person_summaries:
        with (args.out_dir / "downstream_person_summary.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(person_summaries[0].keys()))
            writer.writeheader()
            writer.writerows(person_summaries)

    if anchor_summary:
        with (args.out_dir / "downstream_anchor_summary.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(anchor_summary[0].keys()))
            writer.writeheader()
            writer.writerows(anchor_summary)

    with (args.out_dir / "downstream_errors.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["person_id", "canonical_name", "anchor_work_id", "error"],
        )
        writer.writeheader()
        writer.writerows(errors)

    overall = {
        "people_n": len(by_person),
        "anchors_requested_per_person": args.anchors_per_person,
        "anchors_n": len(anchor_summary),
        "anchors_with_downstream_n": sum(row["valid_downstream_edges_n"] > 0 for row in anchor_summary),
        "anchor_downstream_coverage": (
            sum(row["valid_downstream_edges_n"] > 0 for row in anchor_summary) / len(anchor_summary)
            if anchor_summary else 0.0
        ),
        "downstream_edge_n": len(edge_rows),
        "downstream_unique_person_work_pairs_n": len(downstream_rows),
        "people_with_downstream_n": sum(row["downstream_unique_work_n"] > 0 for row in person_summaries),
        "people_with_10plus_downstream_works_n": sum(
            row["downstream_unique_work_n"] >= 10 for row in person_summaries
        ),
        "temporal_anomalies_n": len(anomaly_rows),
        "api_errors_n": len(errors),
        "horizon_years": args.horizon_years,
        "max_citers_per_anchor": args.max_citers_per_anchor,
        "anchor_selection": "earliest + temporal median + latest + highest-cited remaining",
        "mental_health_information_used": False,
    }
    (args.out_dir / "downstream_overall.json").write_text(
        json.dumps(overall, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(overall, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
