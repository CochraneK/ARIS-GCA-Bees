"""Prioritise documented correction cases for ARIS4C011 Pilot 3.

This is an acquisition-enrichment queue, not the confirmatory benchmark.
Known correction content may be used to decide which historical objects are
worth recovering, but later correction text is never exposed to Track A
detectors.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List


ARTIFACT_WEIGHTS = {
    "SAFE_EXACT_READY": 8,
    "SAFE_EXACT_TARGET": 6,
    "PRE_EVENT_HTML_ONLY": 3,
    "UNKNOWN": 0,
    "NO_PRE_EVENT_OBJECT": -4,
}

MODE_WEIGHTS = {
    "DETERMINISTIC_INTERNAL": 6,
    "RAW_DATA_RECOMPUTE": 6,
    "CROSS_SOURCE": 5,
    "CROSS_SECTION": 5,
    "STRUCTURED_RECOMPUTE": 4,
    "REANALYSIS": 1,
    "FORMAT_CONTROL": 0,
    "IMAGE": 0,
}

ROLE_WEIGHTS = {
    "table": 4,
    "body_text": 3,
    "references": 3,
    "figure_image": 1,
    "raw_data": 0,
}

SCIENTIFIC_CONTENT_WEIGHTS = {
    "YES": 3,
    "MIXED": 1,
    "NO": -2,
}

BENCHMARK_ROLE_WEIGHTS = {
    "POSITIVE_CASE": 2,
    "HONEST_ERROR_CONTROL": 1,
    "FORMAT_CONTROL": -1,
}


def lag_points(days: int) -> int:
    if days >= 730:
        return 3
    if days >= 365:
        return 2
    if days >= 180:
        return 1
    return 0


def _require(mapping: Dict[str, int], value: str, field: str) -> int:
    if value not in mapping:
        raise ValueError(f"Unknown {field}: {value}")
    return mapping[value]


def score_candidate(row: Dict[str, str]) -> Dict[str, str]:
    target = date.fromisoformat(row["target_published"])
    correction = date.fromisoformat(row["correction_published"])
    lag_days = (correction - target).days
    if lag_days < 0:
        raise ValueError("correction date cannot precede target publication")

    score = (
        _require(ARTIFACT_WEIGHTS, row["artifact_state"], "artifact_state")
        + _require(MODE_WEIGHTS, row["verification_mode"], "verification_mode")
        + _require(ROLE_WEIGHTS, row["required_role"], "required_role")
        + _require(SCIENTIFIC_CONTENT_WEIGHTS, row["scientific_content"], "scientific_content")
        + _require(BENCHMARK_ROLE_WEIGHTS, row["benchmark_role"], "benchmark_role")
        + lag_points(lag_days)
    )

    if row.get("candidate_state") == "COMPLETE":
        queue_status = "COMPLETE"
    elif row["benchmark_role"] == "FORMAT_CONTROL":
        queue_status = "CONTROL"
    elif score >= 15:
        queue_status = "PRIORITY"
    elif score >= 10:
        queue_status = "SECONDARY"
    else:
        queue_status = "DEFER"

    out = dict(row)
    out["lag_days"] = str(lag_days)
    out["priority_score"] = str(score)
    out["queue_status"] = queue_status
    return out


def build_queue(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    scored = [score_candidate(row) for row in rows]
    order = {"PRIORITY": 0, "SECONDARY": 1, "CONTROL": 2, "DEFER": 3, "COMPLETE": 4}
    scored.sort(key=lambda r: (order[r["queue_status"]], -int(r["priority_score"]), r["candidate_id"]))
    active_rank = 0
    for row in scored:
        if row["queue_status"] in {"PRIORITY", "SECONDARY"}:
            active_rank += 1
            row["active_rank"] = str(active_rank)
        else:
            row["active_rank"] = ""
    return scored


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: List[Dict[str, str]], path: Path) -> None:
    if not rows:
        raise ValueError("Refusing to write an empty Pilot 3 queue")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    write_csv(build_queue(read_csv(args.input)), args.output)


if __name__ == "__main__":
    main()
