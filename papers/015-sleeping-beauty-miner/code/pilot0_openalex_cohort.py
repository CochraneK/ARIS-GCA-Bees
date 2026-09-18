"""Run a small reproducible historical-cutoff cohort benchmark.

This is a benchmark *smoke test*, not prospective-model validation.

Default design
--------------
Sampling frame:
- OpenAlex works
- publication year 1980
- article
- Physics & Astronomy field
- reproducible random sample with fixed seed

Feature cutoff:
- 1995

Outcome observation endpoint:
- 2011

Smoke-test outcome:
- top 20% of the sampled cohort by full-history Beauty Coefficient through 2011

This relative outcome is used only to verify that historical-cutoff baseline
evaluation works on a non-hand-picked cohort. It is not a universal definition
of a Sleeping Beauty or a breakthrough.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Sequence

from historical_backtest import PaperHistory, evaluate_strategies
from openalex_adapter import reconstruct_history_from_openalex, sample_works
from sb_metrics import retrospective_summary


DEFAULT_FILTERS = (
    "publication_year:1980,type:article,topics.field.id:31"
)
DEFAULT_STRATEGIES = (
    "current_citations",
    "momentum_3y",
    "acceleration_3y",
    "partial_beauty",
    "dormancy",
)


def _top_fraction_labels(
    rows: Sequence[tuple[str, float]],
    *,
    fraction: float,
) -> dict[str, float]:
    if not 0 < fraction <= 1:
        raise ValueError("fraction must be in (0, 1]")
    ordered = sorted(rows, key=lambda row: (-row[1], row[0]))
    n_positive = max(1, math.ceil(len(ordered) * fraction))
    positive_ids = {paper_id for paper_id, _ in ordered[:n_positive]}
    return {
        paper_id: 1.0 if paper_id in positive_ids else 0.0
        for paper_id, _ in rows
    }


def run_cohort(
    *,
    sample_size: int = 20,
    seed: int = 15015,
    filters: str = DEFAULT_FILTERS,
    cutoff_year: int = 1995,
    observation_end_year: int = 2011,
    positive_fraction: float = 0.20,
    review_budget_k: int = 5,
    api_key: str | None = None,
) -> dict:
    if cutoff_year >= observation_end_year:
        raise ValueError("cutoff_year must precede observation_end_year")

    sample = sample_works(
        filters=filters,
        sample_size=sample_size,
        seed=seed,
        api_key=api_key,
    )
    if not sample:
        raise RuntimeError("OpenAlex sample returned no works")

    cases: list[dict] = []
    histories: list[PaperHistory] = []
    final_b_rows: list[tuple[str, float]] = []

    for work in sample:
        if work.publication_year is None:
            continue
        _, history = reconstruct_history_from_openalex(
            work.openalex_id,
            publication_year=int(work.publication_year),
            end_year=observation_end_year,
            api_key=api_key,
            max_records=None,
        )
        metrics = retrospective_summary(history.counts)
        paper_id = work.openalex_id
        final_b = float(metrics["beauty_coefficient"])

        histories.append(
            PaperHistory(
                paper_id=paper_id,
                publication_year=int(work.publication_year),
                counts=history.counts,
            )
        )
        final_b_rows.append((paper_id, final_b))
        cases.append(
            {
                "paper_id": paper_id,
                "doi": work.doi,
                "title": work.title,
                "publication_year": work.publication_year,
                "primary_topic": work.primary_topic,
                "citations_through_observation_end": history.total_citations,
                "final_beauty_coefficient": final_b,
                "awakening_year": (
                    int(work.publication_year)
                    + int(metrics["awakening_time"])
                ),
            }
        )

    labels = _top_fraction_labels(
        final_b_rows,
        fraction=positive_fraction,
    )

    baseline_results = evaluate_strategies(
        histories,
        cutoff_year=cutoff_year,
        strategies=DEFAULT_STRATEGIES,
        future_relevance=labels,
        k=review_budget_k,
    )

    for case in cases:
        case["smoke_outcome_top_B"] = bool(labels[case["paper_id"]])

    return {
        "benchmark_type": "non-hand-picked historical cohort smoke test",
        "claim_boundary": (
            "This tests cutoff-safe benchmark plumbing on a reproducible "
            "random cohort. It is not evidence that ARIS4C015 can predict "
            "future breakthroughs."
        ),
        "sampling": {
            "source": "OpenAlex live API",
            "filters": filters,
            "sample_size_requested": sample_size,
            "sample_size_analyzed": len(histories),
            "seed": seed,
            "sampling_method": "OpenAlex sample + seed",
        },
        "temporal_design": {
            "feature_cutoff_year": cutoff_year,
            "outcome_observation_end_year": observation_end_year,
        },
        "outcome": {
            "name": "within-cohort top Beauty Coefficient through endpoint",
            "positive_fraction": positive_fraction,
            "n_positive": int(sum(labels.values())),
            "universal_sleeping_beauty_definition": False,
        },
        "review_budget_k": review_budget_k,
        "strategies": list(DEFAULT_STRATEGIES),
        "baseline_results": baseline_results,
        "cases": cases,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=20)
    parser.add_argument("--seed", type=int, default=15015)
    parser.add_argument("--filters", default=DEFAULT_FILTERS)
    parser.add_argument("--cutoff-year", type=int, default=1995)
    parser.add_argument("--observation-end-year", type=int, default=2011)
    parser.add_argument("--positive-fraction", type=float, default=0.20)
    parser.add_argument("--review-budget-k", type=int, default=5)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_cohort(
        sample_size=args.sample_size,
        seed=args.seed,
        filters=args.filters,
        cutoff_year=args.cutoff_year,
        observation_end_year=args.observation_end_year,
        positive_fraction=args.positive_fraction,
        review_budget_k=args.review_budget_k,
        api_key=args.api_key,
    )
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
