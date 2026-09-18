#!/usr/bin/env python3
"""Merge fixed ARIS4C004 identity100 OpenAlex shard outputs.

Shard directories may be nested by actions/download-artifact. JSONL files are
concatenated deterministically by shard directory name.

Important: openalex_pilot.py stores Author and Work payloads inside wrappers:
- author rows: {"person_id": ..., "author": {...}}
- work rows:   {"person_id": ..., "author_id": ..., "work": {...}}

The merger therefore deduplicates by *person + nested OpenAlex ID*, not by a
nonexistent top-level id. This preserves the wrapper shape required by
build_single_author_profiles.py while preventing duplicate manifestations from
multiple artifact paths.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def nested_openalex_id(row: dict[str, Any], payload_field: str) -> str:
    payload = row.get(payload_field) or {}
    value = str(payload.get("id") or payload.get("openalex_id") or "").strip()
    return value.rstrip("/").split("/")[-1]


def wrapper_key(row: dict[str, Any], payload_field: str) -> tuple[str, str]:
    return (
        str(row.get("person_id") or "").strip(),
        nested_openalex_id(row, payload_field),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--expected-shards", type=int, default=10)
    args = parser.parse_args()

    dirs = sorted(
        {
            path.parent
            for path in args.shard_root.rglob("openalex_resolution_audit.jsonl")
        },
        key=lambda p: str(p),
    )
    if len(dirs) != args.expected_shards:
        raise SystemExit(
            f"expected {args.expected_shards} shard outputs, found {len(dirs)}: "
            + ", ".join(str(x) for x in dirs)
        )

    audit: list[dict[str, Any]] = []
    authors_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    works_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    shard_summaries: list[dict[str, Any]] = []

    for directory in dirs:
        audit.extend(read_jsonl(directory / "openalex_resolution_audit.jsonl"))
        for row in read_jsonl(directory / "openalex_authors.jsonl"):
            key = wrapper_key(row, "author")
            if key[0] and key[1]:
                authors_by_key.setdefault(key, row)
        for row in read_jsonl(directory / "openalex_works.jsonl"):
            key = wrapper_key(row, "work")
            if key[0] and key[1]:
                works_by_key.setdefault(key, row)
        summary_path = directory / "openalex_acquisition_summary.json"
        if summary_path.exists():
            shard_summaries.append(json.loads(summary_path.read_text(encoding="utf-8")))

    person_ids = [str(row.get("person_id") or "") for row in audit]
    if len(person_ids) != len(set(person_ids)):
        duplicates = sorted({pid for pid in person_ids if person_ids.count(pid) > 1})
        raise SystemExit(f"candidate audit duplicated across shards: {duplicates[:10]}")
    if len(audit) != 100:
        raise SystemExit(f"expected 100 candidate audit rows, found {len(audit)}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "openalex_resolution_audit.jsonl").open("w", encoding="utf-8") as handle:
        for row in audit:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (args.out_dir / "openalex_authors.jsonl").open("w", encoding="utf-8") as handle:
        for key in sorted(authors_by_key):
            handle.write(json.dumps(authors_by_key[key], ensure_ascii=False) + "\n")
    with (args.out_dir / "openalex_works.jsonl").open("w", encoding="utf-8") as handle:
        for key in sorted(works_by_key):
            handle.write(json.dumps(works_by_key[key], ensure_ascii=False) + "\n")

    summary = {
        "expected_shards": args.expected_shards,
        "shards_found": len(dirs),
        "candidate_audit_rows_n": len(audit),
        "unique_person_author_records_n": len(authors_by_key),
        "unique_person_work_records_n": len(works_by_key),
        "shard_summary_n": len(shard_summaries),
        "mental_health_information_used": False,
        "shard_directories": [str(x) for x in dirs],
    }
    (args.out_dir / "openalex_acquisition_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
