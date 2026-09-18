#!/usr/bin/env python3
"""Split a blinded AI adjudication packet into deterministic model-specific batches."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def checksum_rows(rows, fields):
    h = hashlib.sha256()
    for row in rows:
        payload = "|".join(str(row.get(f, "")) for f in fields)
        h.update(payload.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("reviewer_packet_csv", type=Path)
    p.add_argument("output_dir", type=Path)
    p.add_argument("manifest_json", type=Path)
    p.add_argument("--batch-size", type=int, default=250)
    args = p.parse_args()

    with args.reviewer_packet_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(reader.fieldnames or [])

    by_reviewer = defaultdict(list)
    for row in rows:
        reviewer = (row.get("reviewer_id") or "UNASSIGNED").strip()
        by_reviewer[reviewer].append(row)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "classification": "AI_ADJUDICATION_BATCH_MANIFEST_NO_LABELS",
        "batch_size": args.batch_size,
        "assignments_total": len(rows),
        "reviewers": {},
        "batches": [],
    }

    for reviewer in sorted(by_reviewer):
        reviewer_rows = sorted(by_reviewer[reviewer], key=lambda r: r.get("assignment_id", ""))
        manifest["reviewers"][reviewer] = len(reviewer_rows)
        for idx in range(0, len(reviewer_rows), args.batch_size):
            batch = reviewer_rows[idx:idx + args.batch_size]
            batch_no = idx // args.batch_size + 1
            safe = reviewer.replace("/", "_").replace(" ", "_")
            filename = f"{safe}_batch_{batch_no:03d}.csv"
            path = args.output_dir / filename
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(batch)
            manifest["batches"].append({
                "reviewer_id": reviewer,
                "batch_number": batch_no,
                "filename": filename,
                "assignments": len(batch),
                "assignment_checksum_sha256": checksum_rows(batch, ["assignment_id", "paper_id"]),
            })

    args.manifest_json.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_json.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
