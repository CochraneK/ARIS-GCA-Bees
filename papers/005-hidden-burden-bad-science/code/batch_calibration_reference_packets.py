#!/usr/bin/env python3
"""Create deterministic batches for dual calibration reference review.

The input is the private calibration-candidate CSV. The output directory
contains blinded REF_A / REF_B batch CSVs plus a manifest. Row-level batch files
must remain private because the source candidate queue can be reputationally
sensitive even though queue labels are stripped from reviewer inputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from make_calibration_reference_packets import build_packets, read_csv


def checksum_rows(rows: list[dict[str, str]]) -> str:
    h = hashlib.sha256()
    for row in sorted(rows, key=lambda r: r["assignment_id"]):
        payload = f"{row.get('assignment_id','')}|{row.get('candidate_id','')}"
        h.update(payload.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def batch_packets(
    candidates: list[dict[str, str]],
    *,
    batch_size: int = 100,
    seed: int = 20260919,
) -> tuple[dict[str, list[tuple[str, list[dict[str, str]]]]], dict[str, Any]]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    packets = build_packets(candidates, seed=seed)
    batches: dict[str, list[tuple[str, list[dict[str, str]]]]] = {}
    manifest_batches = []

    for reviewer in sorted(packets):
        rows = packets[reviewer]
        reviewer_batches = []
        for index in range(0, len(rows), batch_size):
            number = index // batch_size + 1
            chunk = rows[index:index + batch_size]
            filename = f"{reviewer}_batch_{number:03d}.csv"
            reviewer_batches.append((filename, chunk))
            manifest_batches.append(
                {
                    "reference_reviewer_id": reviewer,
                    "batch_number": number,
                    "filename": filename,
                    "assignments": len(chunk),
                    "assignment_checksum_sha256": checksum_rows(chunk),
                }
            )
        batches[reviewer] = reviewer_batches

    reviewer_counts = {k: len(v) for k, v in packets.items()}
    manifest = {
        "classification": "CALIBRATION_REFERENCE_BATCH_MANIFEST_NO_LABELS",
        "batch_size": batch_size,
        "seed": seed,
        "assignments_total": sum(reviewer_counts.values()),
        "reviewers": reviewer_counts,
        "batches": manifest_batches,
        "warnings": [
            "Batch rows are blinded neutral bibliography, not reference truth.",
            "Row-level batch files must remain private and must not be committed to a public repository.",
            "REF_A and REF_B must complete reviews independently.",
            "Manifest/checksum integrity does not establish label correctness.",
        ],
    }
    return batches, manifest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("private_candidate_csv", type=Path)
    p.add_argument("output_dir", type=Path)
    p.add_argument("manifest_json", type=Path)
    p.add_argument("--batch-size", type=int, default=100)
    p.add_argument("--seed", type=int, default=20260919)
    args = p.parse_args()

    batches, manifest = batch_packets(
        read_csv(args.private_candidate_csv),
        batch_size=args.batch_size,
        seed=args.seed,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for reviewer, reviewer_batches in batches.items():
        for filename, rows in reviewer_batches:
            write_csv(args.output_dir / filename, rows)

    args.manifest_json.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_json.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
