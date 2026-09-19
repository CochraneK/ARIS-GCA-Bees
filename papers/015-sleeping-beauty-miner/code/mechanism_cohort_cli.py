"""CLI for building an ARIS4C015 mechanism cohort from a local export.

Input JSON may be either:
- a list of paper objects; or
- {"papers": [...], "provenance": {...}}

Each paper requires:
    paper_id
    publication_year
    field
    annual_citation_counts

Optional:
    reference_count
    author_count
    source_id

The CLI intentionally consumes an already-bounded export. It does not query a
remote corpus itself. This keeps the empirical cohort reproducible and makes
the exact input slice auditable.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from mechanism_cohort import CorpusPaper, build_mechanism_cohort
from mechanism_labels import (
    SCISCINET_V1_CALIBRATION,
    SourceBCalibration,
)


def _paper(row: dict[str, Any]) -> CorpusPaper:
    required = {
        "paper_id",
        "publication_year",
        "field",
        "annual_citation_counts",
    }
    missing = sorted(required.difference(row))
    if missing:
        raise KeyError("missing required paper fields: " + ", ".join(missing))
    return CorpusPaper(
        paper_id=str(row["paper_id"]),
        publication_year=int(row["publication_year"]),
        field=str(row["field"]),
        annual_citation_counts=tuple(
            int(x) for x in row["annual_citation_counts"]
        ),
        reference_count=(
            int(row["reference_count"])
            if row.get("reference_count") is not None
            else None
        ),
        author_count=(
            int(row["author_count"])
            if row.get("author_count") is not None
            else None
        ),
        source_id=(
            str(row["source_id"])
            if row.get("source_id") is not None
            else None
        ),
    )


def run_payload(
    payload: list[dict[str, Any]] | dict[str, Any],
    *,
    min_stratum_size: int = 20,
    min_total_citations: int = 50,
    controls_per_case: int = 1,
    early_percentile_caliper: float = 0.15,
    max_abs_smd: float = 0.10,
    min_primary_match_rate: float = 0.50,
    b_calibration: SourceBCalibration = SCISCINET_V1_CALIBRATION,
) -> dict[str, Any]:
    if isinstance(payload, list):
        rows = payload
        provenance = {}
    elif isinstance(payload, dict):
        rows = payload.get("papers")
        if not isinstance(rows, list):
            raise TypeError("payload.papers must be a list")
        provenance = payload.get("provenance") or {}
    else:
        raise TypeError("payload must be a list or object")

    papers = [_paper(row) for row in rows]
    result = build_mechanism_cohort(
        papers,
        min_stratum_size=min_stratum_size,
        sb_min_total_citations=min_total_citations,
        controls_per_case=controls_per_case,
        matching_early_percentile_caliper=early_percentile_caliper,
        matching_max_abs_smd=max_abs_smd,
        min_primary_match_rate=min_primary_match_rate,
        b_calibration=b_calibration,
    )
    result["input_provenance"] = provenance
    result["cli_parameters"] = {
        "min_stratum_size": min_stratum_size,
        "min_total_citations": min_total_citations,
        "controls_per_case": controls_per_case,
        "early_percentile_caliper": early_percentile_caliper,
        "max_abs_smd": max_abs_smd,
        "min_primary_match_rate": min_primary_match_rate,
    }
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--min-stratum-size", type=int, default=20)
    parser.add_argument("--min-total-citations", type=int, default=50)
    parser.add_argument("--controls-per-case", type=int, default=1)
    parser.add_argument(
        "--early-percentile-caliper",
        type=float,
        default=0.15,
    )
    parser.add_argument("--max-abs-smd", type=float, default=0.10)
    parser.add_argument(
        "--min-primary-match-rate",
        type=float,
        default=0.50,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = run_payload(
        payload,
        min_stratum_size=args.min_stratum_size,
        min_total_citations=args.min_total_citations,
        controls_per_case=args.controls_per_case,
        early_percentile_caliper=args.early_percentile_caliper,
        max_abs_smd=args.max_abs_smd,
        min_primary_match_rate=args.min_primary_match_rate,
    )
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
