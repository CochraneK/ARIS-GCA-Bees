#!/usr/bin/env python3
"""Build a deterministic person-level work-audit sample for held VERIFIED identities.

Purpose: avoid either extreme of (a) releasing a person from aggregate works_count
alone or (b) manually reading every clean-looking work before a network release
decision.

For each VERIFIED person with network_observable=false:
1. include one representative plausible work from each accepted Author ID when
   such a work exists;
2. include earliest, temporal-median and latest plausible works;
3. fill remaining slots with highest-cited plausible works.

The sample is a triage audit only. Any detected contamination escalates that
person to full work-level review under WORK_CODEBOOK.md.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

VERIFIED = {"VERIFIED_SINGLE", "VERIFIED_CLUSTER"}


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def select_sample(rows: list[dict[str, Any]], max_n: int) -> list[tuple[dict[str, Any], str]]:
    plausible = [
        row for row in rows
        if row.get("temporal_status") == "plausible" and row.get("openalex_work_id")
    ]
    if not plausible or max_n <= 0:
        return []

    selected: list[tuple[dict[str, Any], str]] = []
    seen: set[str] = set()

    def add(row: dict[str, Any], reason: str) -> None:
        wid = str(row.get("openalex_work_id") or "")
        if wid and wid not in seen and len(selected) < max_n:
            selected.append((row, reason))
            seen.add(wid)

    by_author: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in plausible:
        for aid in row.get("source_author_ids") or [row.get("source_author_id")]:
            if aid:
                by_author[str(aid)].append(row)
    for aid in sorted(by_author):
        representative = max(
            by_author[aid],
            key=lambda row: (
                int(row.get("cited_by_count") or 0),
                -(int(row.get("publication_year") or 9999)),
                str(row.get("openalex_work_id") or ""),
            ),
        )
        add(representative, f"accepted_author_fragment:{aid}")

    chronological = sorted(
        plausible,
        key=lambda row: (
            int(row.get("publication_year") or 9999),
            str(row.get("openalex_work_id") or ""),
        ),
    )
    add(chronological[0], "earliest")
    add(chronological[len(chronological)//2], "temporal_median")
    add(chronological[-1], "latest")

    for row in sorted(
        plausible,
        key=lambda row: (
            -int(row.get("cited_by_count") or 0),
            int(row.get("publication_year") or 9999),
            str(row.get("openalex_work_id") or ""),
        ),
    ):
        add(row, "high_citation")
        if len(selected) >= max_n:
            break
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--identities", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--max-per-person", type=int, default=12)
    args = parser.parse_args()

    corpus = read_jsonl(args.corpus)
    identities = {
        row["person_id"]: row
        for row in read_csv(args.identities)
        if row.get("identity_status") in VERIFIED and not truthy(row.get("network_observable"))
    }
    by_person: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in corpus:
        pid = str(row.get("person_id") or "")
        if pid in identities:
            by_person[pid].append(row)

    out: list[dict[str, Any]] = []
    people_with_sample = 0
    for pid, identity in identities.items():
        sample = select_sample(by_person.get(pid, []), args.max_per_person)
        if sample:
            people_with_sample += 1
        for row, reason in sample:
            out.append({
                "person_id": pid,
                "canonical_name": identity.get("canonical_name", ""),
                "identity_status": identity.get("identity_status", ""),
                "openalex_work_id": row.get("openalex_work_id", ""),
                "publication_year": row.get("publication_year", ""),
                "title": row.get("title", ""),
                "cited_by_count": row.get("cited_by_count", 0),
                "primary_topic_name": row.get("primary_topic_name", ""),
                "source_author_ids": ";".join(row.get("source_author_ids") or []),
                "sample_reason": reason,
                "work_belongs_to_focal_person": "",
                "review_reason": "",
                "reviewer": "",
                "mh_blinded_at_work_audit": "",
            })

    fields = [
        "person_id","canonical_name","identity_status","openalex_work_id",
        "publication_year","title","cited_by_count","primary_topic_name",
        "source_author_ids","sample_reason","work_belongs_to_focal_person",
        "review_reason","reviewer","mh_blinded_at_work_audit",
    ]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

    summary = {
        "held_verified_people_n": len(identities),
        "people_with_sample_n": people_with_sample,
        "sample_rows_n": len(out),
        "max_per_person": args.max_per_person,
        "mental_health_information_used": False,
        "note": "Audit sample is deterministic triage. Any contamination escalates the person to full work review; passing the sample does not override the >=5 clean-work network-release rule.",
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
