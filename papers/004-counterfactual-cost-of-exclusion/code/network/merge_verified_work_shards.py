#!/usr/bin/env python3
"""Merge ARIS4C004 verified-work shard artifacts into one P3 corpus."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--expected-shards", type=int, default=8)
    args = parser.parse_args()

    dirs = sorted(
        {p.parent for p in args.shard_root.rglob("verified_work_overall.json")},
        key=lambda p: str(p),
    )
    if len(dirs) != args.expected_shards:
        raise SystemExit(f"expected {args.expected_shards} work shards, found {len(dirs)}")

    corpus: list[dict[str, Any]] = []
    summaries: list[dict[str, str]] = []
    review: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []
    shard_overalls: list[dict[str, Any]] = []

    for directory in dirs:
        corpus.extend(read_jsonl(directory / "verified_work_corpus.jsonl"))
        summaries.extend(read_csv(directory / "verified_work_summary.csv"))
        review.extend(read_csv(directory / "work_review_queue.csv"))
        errors.extend(read_csv(directory / "verified_work_errors.csv"))
        shard_overalls.append(json.loads((directory / "verified_work_overall.json").read_text(encoding="utf-8")))

    person_ids = [row.get("person_id", "") for row in summaries]
    if len(person_ids) != len(set(person_ids)):
        raise SystemExit("person appears in more than one verified-work shard summary")

    corpus_keys = [
        (str(row.get("person_id") or ""), str(row.get("dedup_key") or row.get("openalex_work_id") or ""))
        for row in corpus
    ]
    if len(corpus_keys) != len(set(corpus_keys)):
        raise SystemExit("duplicate person/work keys across verified-work shards")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "verified_work_corpus.jsonl").open("w", encoding="utf-8") as h:
        for row in corpus:
            h.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary_fields = list(summaries[0].keys()) if summaries else []
    review_fields = list(review[0].keys()) if review else [
        "person_id","canonical_name","openalex_work_id","doi","title","publication_year",
        "cited_by_count","primary_topic_name","source_author_ids","reason","manual_decision","manual_reason"
    ]
    error_fields = list(errors[0].keys()) if errors else ["person_id","canonical_name","author_id","error"]
    write_csv(args.out_dir / "verified_work_summary.csv", summaries, summary_fields)
    write_csv(args.out_dir / "work_review_queue.csv", review, review_fields)
    write_csv(args.out_dir / "verified_work_errors.csv", errors, error_fields)

    overall = {
        "verified_people_n": len(summaries),
        "unique_work_records_n": len(corpus),
        "manual_review_work_rows_n": len(review),
        "fetch_errors_n": len(errors),
        "work_shards_n": len(dirs),
        "shard_verified_people_sum": sum(int(x.get("verified_people_n") or 0) for x in shard_overalls),
        "mental_health_information_used": False,
        "note": "Merged person-disjoint P3 work shards; manual-review queue includes all held VERIFIED identities.",
    }
    (args.out_dir / "verified_work_overall.json").write_text(
        json.dumps(overall, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(overall, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
