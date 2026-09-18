"""Aggregate ARIS4C015 Pilot 1 cohort results across strata.

The aggregator macro-averages stratum-level metrics. It does not pool papers
across fields/eras as if they came from one homogeneous distribution.

This separation matters because:
- outcome prevalence can differ by field/era;
- citation coverage differs by stratum;
- review budgets are applied within strata;
- macro stability is more informative at this stage than one large pooled
  score dominated by high-output fields.
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


METRIC_NAMES = (
    "precision_at_k",
    "recall_at_k",
    "ndcg_at_k",
)


def load_result(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _field_from_filters(filters: str) -> str | None:
    marker = "primary_topic.field.id:"
    for part in filters.split(","):
        part = part.strip()
        if part.startswith(marker):
            return part[len(marker) :]
    return None


def summarize_stratum(result: dict[str, Any]) -> dict[str, Any]:
    """Return compact metadata for one Pilot 1 cohort result."""
    sampling = result["sampling"]
    temporal = result["temporal_design"]
    return {
        "filters": sampling["filters"],
        "field_id": _field_from_filters(sampling["filters"]),
        "sample_size": sampling["sample_size_analyzed"],
        "seed": sampling["seed"],
        "cutoff_year": temporal["feature_cutoff_year"],
        "endpoint_year": temporal["outcome_observation_end_year"],
        "outcome_summary": result["outcome_summary"],
    }


def aggregate_results(results: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(results)
    if not rows:
        raise ValueError("at least one Pilot 1 result is required")

    values: dict[
        tuple[str, str, str],
        list[float],
    ] = defaultdict(list)

    for result in rows:
        matrix = result["outcome_baseline_matrix"]
        for outcome_name, strategy_rows in matrix.items():
            for strategy_row in strategy_rows:
                strategy = str(strategy_row["strategy"])
                for metric in METRIC_NAMES:
                    if metric in strategy_row:
                        values[
                            (outcome_name, strategy, metric)
                        ].append(float(strategy_row[metric]))

    aggregate: dict[str, dict[str, dict[str, Any]]] = {}
    for (outcome, strategy, metric), xs in sorted(values.items()):
        aggregate.setdefault(outcome, {}).setdefault(strategy, {})[
            metric
        ] = {
            "n_strata": len(xs),
            "mean": statistics.fmean(xs),
            "median": statistics.median(xs),
            "min": min(xs),
            "max": max(xs),
            "population_sd": statistics.pstdev(xs) if len(xs) > 1 else 0.0,
        }

    # Winner counts are descriptive only. Ties count for every tied strategy.
    winner_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    for result in rows:
        for outcome_name, strategy_rows in result[
            "outcome_baseline_matrix"
        ].items():
            ndcg_rows = [
                row for row in strategy_rows if "ndcg_at_k" in row
            ]
            if not ndcg_rows:
                continue
            best = max(float(row["ndcg_at_k"]) for row in ndcg_rows)
            for row in ndcg_rows:
                if float(row["ndcg_at_k"]) == best:
                    winner_counts[outcome_name][str(row["strategy"])] += 1

    return {
        "aggregation": "macro across independently sampled strata",
        "claim_boundary": (
            "Exploratory baseline-stability summary. Winner counts and macro "
            "means do not establish a universally superior predictor."
        ),
        "n_strata": len(rows),
        "total_papers_analyzed": sum(
            int(row["sampling"]["sample_size_analyzed"])
            for row in rows
        ),
        "strata": [summarize_stratum(row) for row in rows],
        "metrics": aggregate,
        "ndcg_winner_counts": {
            outcome: dict(counts)
            for outcome, counts in winner_counts.items()
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = aggregate_results(
        load_result(path) for path in args.inputs
    )
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
