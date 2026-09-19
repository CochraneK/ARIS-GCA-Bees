#!/usr/bin/env python3
"""Build blinded reference-review packets from private calibration candidates.

Input candidate CSV may contain screening queue/reason metadata. The output
packets deliberately strip all such fields and expose only neutral bibliography.

Two deterministic reviewer packets are produced. Reviewers must not see each
other's output or AI_A/AI_B adjudication results.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import random
from pathlib import Path
from typing import Any

NEUTRAL_FIELDS = (
    "candidate_id",
    "doi",
    "title",
    "publication_year",
    "journal",
    "publisher",
)


def stable_assignment_id(reviewer: str, candidate_id: str) -> str:
    digest = hashlib.sha256(
        f"{reviewer}|{candidate_id}".encode("utf-8")
    ).hexdigest()[:16]
    return f"{reviewer}_{digest}"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else [
        "assignment_id",
        "candidate_id",
        "paper_id",
        "doi",
        "title",
        "publication_year",
        "journal",
        "publisher",
        "reference_reviewer_id",
        "prompt_version",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def build_packets(
    candidates: list[dict[str, str]],
    *,
    reviewers: tuple[str, ...] = ("REF_A", "REF_B"),
    seed: int = 20260919,
) -> dict[str, list[dict[str, str]]]:
    if len(set(reviewers)) != len(reviewers):
        raise ValueError("reviewer IDs must be unique")

    seen_candidates: set[str] = set()
    base_rows: list[dict[str, str]] = []
    for row in candidates:
        candidate_id = (row.get("candidate_id") or "").strip()
        if not candidate_id:
            raise ValueError("candidate_id required")
        if candidate_id in seen_candidates:
            raise ValueError(f"duplicate candidate_id: {candidate_id}")
        seen_candidates.add(candidate_id)

        # Only rows that could plausibly become calibration anchors need review.
        queue = (row.get("candidate_queue") or "").strip()
        if queue not in {
            "P_HIGH_REVIEW",
            "P_REVIEW",
            "N_PROCESS_REVIEW",
            "N_ERROR_REVIEW",
        }:
            continue

        neutral = {
            "candidate_id": candidate_id,
            "paper_id": (row.get("paper_id") or "").strip(),
        }
        for field in NEUTRAL_FIELDS:
            if field == "candidate_id":
                continue
            neutral[field] = (row.get(field) or "").strip()
        base_rows.append(neutral)

    packets: dict[str, list[dict[str, str]]] = {}
    for reviewer_index, reviewer in enumerate(reviewers):
        rows = []
        for neutral in base_rows:
            rows.append(
                {
                    "assignment_id": stable_assignment_id(
                        reviewer, neutral["candidate_id"]
                    ),
                    **neutral,
                    "reference_reviewer_id": reviewer,
                    "prompt_version": "CAL-REF-V1",
                }
            )

        rng = random.Random(seed + reviewer_index * 1009)
        rng.shuffle(rows)
        packets[reviewer] = rows

    return packets


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("private_candidate_csv", type=Path)
    p.add_argument("output_dir", type=Path)
    p.add_argument("--seed", type=int, default=20260919)
    args = p.parse_args()

    packets = build_packets(
        read_csv(args.private_candidate_csv),
        seed=args.seed,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for reviewer, rows in packets.items():
        write_csv(
            args.output_dir / f"{reviewer}_calibration_reference_packet.csv",
            rows,
        )
        print(f"{reviewer}: {len(rows)} blinded assignments")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
