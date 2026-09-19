"""Merge raw Pilot M shards before mechanism classification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

from mechanism_cohort_cli import run_payload
from mechanism_labels import OPENALEX_PROVISIONAL_CALIBRATION


def merge_shards(payloads: Iterable[dict[str, Any]]) -> dict[str, Any]:
    payloads = list(payloads)
    by_id: dict[str, dict[str, Any]] = {}
    duplicate_ids: list[str] = []
    provenance = []

    for payload in payloads:
        papers = payload.get("papers")
        if not isinstance(papers, list):
            raise TypeError("each shard must contain a papers list")
        provenance.append(payload.get("provenance") or {})
        for paper in papers:
            paper_id = str(paper["paper_id"])
            if paper_id in by_id:
                duplicate_ids.append(paper_id)
                continue
            by_id[paper_id] = paper

    merged_papers = list(by_id.values())
    if not merged_papers:
        raise ValueError("no papers after shard merge")

    result = run_payload(
        {
            "papers": merged_papers,
            "provenance": {
                "source": "merged OpenAlex historical shards",
                "shards": provenance,
                "n_shards": len(payloads),
                "n_unique_papers": len(merged_papers),
                "n_duplicate_rows_removed": len(duplicate_ids),
                "duplicate_paper_ids": sorted(set(duplicate_ids)),
            },
        },
        min_stratum_size=min(100, len(merged_papers)),
        min_total_citations=50,
        controls_per_case=1,
        early_percentile_caliper=0.15,
        max_abs_smd=0.10,
        min_primary_match_rate=0.50,
        b_calibration=OPENALEX_PROVISIONAL_CALIBRATION,
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payloads = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in args.inputs
    ]
    result = merge_shards(payloads)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
