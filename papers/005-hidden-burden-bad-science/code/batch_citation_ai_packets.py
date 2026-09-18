#!/usr/bin/env python3
"""Deterministically batch citation-edge AI adjudication assignments."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def checksum(rows: list[dict[str, str]]) -> str:
    h = hashlib.sha256()
    for row in rows:
        h.update(
            f"{row.get('assignment_id','')}|{row.get('edge_id','')}".encode("utf-8")
        )
        h.update(b"\n")
    return h.hexdigest()


def batch_rows(
    rows: list[dict[str, str]],
    batch_size: int,
) -> tuple[dict[str, list[list[dict[str, str]]]], dict]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen: set[str] = set()
    for row in rows:
        aid = row.get("assignment_id") or ""
        adjudicator = row.get("adjudicator_id") or ""
        if not aid or not adjudicator:
            raise ValueError("Every row requires assignment_id and adjudicator_id")
        if aid in seen:
            raise ValueError(f"Duplicate assignment_id: {aid}")
        seen.add(aid)
        groups[adjudicator].append(row)

    batched: dict[str, list[list[dict[str, str]]]] = {}
    manifest = {
        "classification": "CITATION_EDGE_AI_BATCH_MANIFEST_NO_LABELS",
        "batch_size": batch_size,
        "assignments_total": len(rows),
        "adjudicators": {},
        "batches": [],
    }

    for adjudicator in sorted(groups):
        ordered = sorted(groups[adjudicator], key=lambda r: r["assignment_id"])
        chunks = [ordered[i:i + batch_size] for i in range(0, len(ordered), batch_size)]
        batched[adjudicator] = chunks
        manifest["adjudicators"][adjudicator] = len(ordered)
        safe = adjudicator.replace("/", "_").replace(" ", "_")
        for i, chunk in enumerate(chunks, start=1):
            manifest["batches"].append(
                {
                    "adjudicator_id": adjudicator,
                    "batch_number": i,
                    "filename": f"{safe}_batch_{i:03d}.csv",
                    "assignments": len(chunk),
                    "assignment_checksum_sha256": checksum(chunk),
                }
            )
    return batched, manifest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("reviewer_packet_csv", type=Path)
    p.add_argument("output_dir", type=Path)
    p.add_argument("manifest_json", type=Path)
    p.add_argument("--batch-size", type=int, default=100)
    args = p.parse_args()

    with args.reviewer_packet_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(reader.fieldnames or [])

    batched, manifest = batch_rows(rows, args.batch_size)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for entry in manifest["batches"]:
        adjudicator = entry["adjudicator_id"]
        chunk = batched[adjudicator][entry["batch_number"] - 1]
        path = args.output_dir / entry["filename"]
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(chunk)

    args.manifest_json.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_json.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
