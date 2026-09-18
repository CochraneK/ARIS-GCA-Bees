"""Aggregate non-citation Pilot 1 ablations across historical strata."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


METRICS = ("precision_at_k", "recall_at_k", "ndcg_at_k")


def load_result(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def aggregate_feature_results(
    results: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    rows = list(results)
    if not rows:
        raise ValueError("at least one ablation result is required")

    values: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    coverage = []

    for result in rows:
        coverage.append(
            {
                "target_filters": result["target_cohort"]["filters"],
                "target_seed": result["target_cohort"]["seed"],
                "target_n": result["target_cohort"]["n"],
                "prior_filters": result["prior_corpus"]["provenance"].get(
                    "filters"
                ),
                "prior_seed": result["prior_corpus"]["provenance"].get(
                    "seed"
                ),
                "prior_n": result["prior_corpus"]["n_titles"],
                "known_token_share": result["coverage"][
                    "known_token_share"
                ],
            }
        )
        for outcome, feature_rows in result[
            "feature_outcome_matrix"
        ].items():
            for feature_row in feature_rows:
                feature = str(feature_row["feature"])
                for metric in METRICS:
                    if metric in feature_row:
                        values[(outcome, feature, metric)].append(
                            float(feature_row[metric])
                        )

    aggregate: dict[str, dict[str, dict[str, Any]]] = {}
    for (outcome, feature, metric), xs in sorted(values.items()):
        aggregate.setdefault(outcome, {}).setdefault(feature, {})[
            metric
        ] = {
            "n_strata": len(xs),
            "mean": statistics.fmean(xs),
            "median": statistics.median(xs),
            "min": min(xs),
            "max": max(xs),
            "population_sd": (
                statistics.pstdev(xs) if len(xs) > 1 else 0.0
            ),
        }

    winner_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    for result in rows:
        for outcome, feature_rows in result[
            "feature_outcome_matrix"
        ].items():
            ndcg_rows = [
                row for row in feature_rows if "ndcg_at_k" in row
            ]
            if not ndcg_rows:
                continue
            best = max(float(row["ndcg_at_k"]) for row in ndcg_rows)
            for row in ndcg_rows:
                if float(row["ndcg_at_k"]) == best:
                    winner_counts[outcome][str(row["feature"])] += 1

    return {
        "aggregation": "macro across historical strata",
        "n_strata": len(rows),
        "feature_family": rows[0].get("ablation"),
        "coverage": coverage,
        "metrics": aggregate,
        "ndcg_winner_counts": {
            outcome: dict(counts)
            for outcome, counts in winner_counts.items()
        },
        "claim_boundary": (
            "Exploratory feature-family ablation. Macro scores do not establish "
            "causal scientific value or a universally superior predictor."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = aggregate_feature_results(
        load_result(path) for path in args.inputs
    )
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
