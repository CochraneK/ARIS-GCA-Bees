#!/usr/bin/env python3
"""Build a person-level OpenAlex work corpus for verified ARIS4C004 identities.

The identity decision table is already frozen before mental-health coding. This
step reconstructs works only for VERIFIED_SINGLE / VERIFIED_CLUSTER rows.

The script performs mechanical, auditable operations only:
- fetch works for accepted OpenAlex author IDs;
- tag candidate-lifetime plausibility;
- deduplicate repeated DOI or same normalized-title/year records across fragments;
- preserve every source Author ID contributing to a deduplicated work;
- produce person-level coverage summaries and a manual work-review queue.

It does NOT automatically release a previously held identity into confirmatory
network analysis merely because >=5 works remain. Rows held for contamination or
deduplication require explicit review after this corpus is inspected.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

ACQUIRE = Path(__file__).resolve().parents[1] / "acquire"
sys.path.insert(0, str(ACQUIRE))
from openalex_pilot import OpenAlexClient, normalize_openalex_id  # noqa: E402

VERIFIED = {"VERIFIED_SINGLE", "VERIFIED_CLUSTER"}


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    return " ".join(value.split())


def normalize_doi(value: str | None) -> str:
    value = (value or "").strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix):]
    return value


def parse_year(value: Any) -> int | None:
    try:
        year = int(float(value))
    except (TypeError, ValueError):
        return None
    return year if 1000 <= year <= 2200 else None


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def plausible_career_window(birth: int | None, death: int | None) -> tuple[int | None, int | None]:
    lo = birth + 15 if birth is not None else None
    hi = death + 5 if death is not None else None
    return lo, hi


def temporal_status(year: int | None, lo: int | None, hi: int | None) -> str:
    if year is None:
        return "undated"
    if lo is not None and year < lo:
        return "outside_before"
    if hi is not None and year > hi:
        return "outside_after"
    return "plausible"


def work_dedup_key(work: dict[str, Any]) -> str:
    doi = normalize_doi(str(work.get("doi") or ""))
    if doi:
        return f"doi:{doi}"
    title = normalize_text(str(work.get("display_name") or work.get("title") or ""))
    year = parse_year(work.get("publication_year"))
    wid = normalize_openalex_id(str(work.get("id") or ""))
    if title:
        return f"titleyear:{title}|{year if year is not None else 'na'}"
    return f"openalex:{wid}"


def split_ids(value: str) -> list[str]:
    return [normalize_openalex_id(x) for x in (value or "").split(";") if x.strip()]


def needs_manual_work_review(row: dict[str, str]) -> bool:
    adjudication = (row.get("adjudication_status") or "").casefold()
    notes = (row.get("notes") or "").casefold()
    return any(
        token in adjudication or token in notes
        for token in (
            "work-filter",
            "work-dedup",
            "contamination",
            "work-level",
            "mixed",
            "network-unusable",
        )
    )


def deduplicate_person_works(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        groups[record["dedup_key"]].append(record)

    out: list[dict[str, Any]] = []
    for key, items in groups.items():
        # Prefer the best-populated / highest-cited record as the canonical
        # representation, but retain every contributing source author/work ID.
        best = max(
            items,
            key=lambda x: (
                int(x.get("cited_by_count") or 0),
                bool(x.get("doi")),
                len(x.get("title") or ""),
            ),
        )
        merged = dict(best)
        merged["dedup_key"] = key
        merged["source_author_ids"] = sorted({x["source_author_id"] for x in items})
        merged["source_work_ids"] = sorted({x["openalex_work_id"] for x in items if x.get("openalex_work_id")})
        merged["duplicate_records_n"] = len(items)
        out.append(merged)

    return sorted(
        out,
        key=lambda x: (
            x.get("publication_year") if x.get("publication_year") is not None else 9999,
            x.get("title") or "",
            x.get("dedup_key") or "",
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--fetch-year-min", type=int, default=1800)
    parser.add_argument("--fetch-year-max", type=int, default=2026)
    parser.add_argument("--max-works-per-id", type=int, default=500)
    parser.add_argument("--min-network-works", type=int, default=5)
    parser.add_argument("--sleep-rps", type=float, default=2.0)
    args = parser.parse_args()

    with args.decisions.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get("identity_status") in VERIFIED]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    client = OpenAlexClient(
        api_key=os.getenv("OPENALEX_API_KEY") or None,
        requests_per_second=args.sleep_rps,
    )

    all_deduped: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    review_queue: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for row in rows:
        pid = row["person_id"]
        name = row["canonical_name"]
        birth = parse_year(row.get("birth_year"))
        death = parse_year(row.get("death_year"))
        lo, hi = plausible_career_window(birth, death)
        ids = split_ids(row.get("verified_openalex_ids", ""))
        raw: list[dict[str, Any]] = []

        for aid in ids:
            try:
                for work in client.iter_author_works(
                    aid,
                    args.fetch_year_min,
                    args.fetch_year_max,
                    max_works=args.max_works_per_id,
                ):
                    year = parse_year(work.get("publication_year"))
                    raw.append(
                        {
                            "person_id": pid,
                            "canonical_name": name,
                            "source_author_id": aid,
                            "openalex_work_id": normalize_openalex_id(str(work.get("id") or "")),
                            "doi": normalize_doi(str(work.get("doi") or "")),
                            "title": str(work.get("display_name") or ""),
                            "publication_year": year,
                            "temporal_status": temporal_status(year, lo, hi),
                            "cited_by_count": int(work.get("cited_by_count") or 0),
                            "primary_topic_id": normalize_openalex_id(
                                str((work.get("primary_topic") or {}).get("id") or "")
                            ),
                            "primary_topic_name": str(
                                (work.get("primary_topic") or {}).get("display_name") or ""
                            ),
                            "dedup_key": work_dedup_key(work),
                        }
                    )
            except Exception as exc:
                errors.append(
                    {
                        "person_id": pid,
                        "canonical_name": name,
                        "author_id": aid,
                        "error": f"{type(exc).__name__}:{exc}",
                    }
                )

        deduped = deduplicate_person_works(raw)
        for item in deduped:
            item["candidate_birth_year"] = birth
            item["candidate_death_year"] = death
            item["plausible_career_year_min"] = lo
            item["plausible_career_year_max"] = hi
            item["identity_status"] = row["identity_status"]
            all_deduped.append(item)

        plausible = [x for x in deduped if x["temporal_status"] == "plausible"]
        outside = [x for x in deduped if x["temporal_status"].startswith("outside_")]
        undated = [x for x in deduped if x["temporal_status"] == "undated"]
        duplicate_records_removed = max(0, len(raw) - len(deduped))
        manual_review = needs_manual_work_review(row)
        existing_release = truthy(row.get("network_observable"))
        mechanical_min_met = len(plausible) >= args.min_network_works

        summaries.append(
            {
                "person_id": pid,
                "canonical_name": name,
                "identity_status": row["identity_status"],
                "accepted_author_ids_n": len(ids),
                "raw_work_records_n": len(raw),
                "unique_work_records_n": len(deduped),
                "duplicate_records_removed_n": duplicate_records_removed,
                "plausible_unique_works_n": len(plausible),
                "outside_window_unique_works_n": len(outside),
                "undated_unique_works_n": len(undated),
                "manual_work_review_required": str(manual_review).lower(),
                "mechanical_min_works_met": str(mechanical_min_met).lower(),
                "network_observable_before_work_audit": str(existing_release).lower(),
                "auto_release_after_mechanical_cleaning": "false",
            }
        )

        if manual_review:
            for item in plausible:
                review_queue.append(
                    {
                        "person_id": pid,
                        "canonical_name": name,
                        "openalex_work_id": item["openalex_work_id"],
                        "doi": item["doi"],
                        "title": item["title"],
                        "publication_year": item["publication_year"],
                        "cited_by_count": item["cited_by_count"],
                        "primary_topic_name": item["primary_topic_name"],
                        "source_author_ids": ";".join(item["source_author_ids"]),
                        "reason": "identity verified but work-level contamination/deduplication review required",
                        "manual_decision": "",
                        "manual_reason": "",
                    }
                )

    corpus_path = args.out_dir / "verified_work_corpus.jsonl"
    with corpus_path.open("w", encoding="utf-8") as handle:
        for row in all_deduped:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary_fields = [
        "person_id",
        "canonical_name",
        "identity_status",
        "accepted_author_ids_n",
        "raw_work_records_n",
        "unique_work_records_n",
        "duplicate_records_removed_n",
        "plausible_unique_works_n",
        "outside_window_unique_works_n",
        "undated_unique_works_n",
        "manual_work_review_required",
        "mechanical_min_works_met",
        "network_observable_before_work_audit",
        "auto_release_after_mechanical_cleaning",
    ]
    with (args.out_dir / "verified_work_summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summaries)

    review_fields = [
        "person_id",
        "canonical_name",
        "openalex_work_id",
        "doi",
        "title",
        "publication_year",
        "cited_by_count",
        "primary_topic_name",
        "source_author_ids",
        "reason",
        "manual_decision",
        "manual_reason",
    ]
    with (args.out_dir / "work_review_queue.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=review_fields)
        writer.writeheader()
        writer.writerows(review_queue)

    with (args.out_dir / "verified_work_errors.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["person_id", "canonical_name", "author_id", "error"])
        writer.writeheader()
        writer.writerows(errors)

    overall = {
        "verified_people_n": len(rows),
        "unique_work_records_n": len(all_deduped),
        "manual_review_work_rows_n": len(review_queue),
        "fetch_errors_n": len(errors),
        "min_network_works": args.min_network_works,
        "note": (
            "Mechanical cleaning never auto-promotes network_observable. "
            "Held identities require explicit work-level review."
        ),
    }
    (args.out_dir / "verified_work_overall.json").write_text(
        json.dumps(overall, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(overall, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
