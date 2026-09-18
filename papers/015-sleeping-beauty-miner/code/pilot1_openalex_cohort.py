"""ARIS4C015 Pilot 1: reproducible multi-outcome historical cohort benchmark.

This runner evaluates multiple prespecified future outcomes against multiple
transparent baselines on reproducible, non-hand-picked historical cohorts.

It is not prospective-model validation. Its purposes are to:
- verify historical-cutoff separation;
- expose outcome-definition sensitivity;
- quantify how strong simple citation baselines already are;
- create self-contained cohort artifacts that can be re-analysed offline;
- provide a benchmark later semantic/network features must beat.

OpenAlex field assignments are current metadata. They are used here only to
define/evaluate strata, not as predictive features.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from baselines import baseline_score, cutoff_features
from historical_backtest import PaperHistory, evaluate_outcome_matrix
from openalex_adapter import reconstruct_history_from_openalex, sample_works
from outcome_labels import build_outcome_record, outcome_bundle


DEFAULT_FILTERS = (
    "publication_year:1980,type:article,primary_topic.field.id:31"
)
DEFAULT_STRATEGIES = (
    "current_citations",
    "momentum_3y",
    "acceleration_3y",
    "partial_beauty",
    "dormancy",
)

OUTCOME_TYPES = {
    "beauty_percentile": "graded",
    "beauty_top_fraction": "binary",
    "future_acceleration_percentile": "graded",
    "future_uptake_percentile": "graded",
    "awakening_within_horizon": "binary",
    "delayed_recognition_consensus": "binary",
    "delayed_recognition_with_uptake_floor": "binary",
}


def _hash_ids(ids: list[str]) -> str:
    payload = "\n".join(sorted(ids)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def run_cohort(
    *,
    sample_size: int = 20,
    seed: int = 15015,
    filters: str = DEFAULT_FILTERS,
    cutoff_year: int = 1995,
    observation_end_year: int = 2011,
    beauty_fraction: float = 0.20,
    acceleration_fraction: float = 0.20,
    uptake_fraction: float = 0.50,
    awakening_horizon_years: int = 15,
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

    histories: list[PaperHistory] = []
    outcome_records = []
    cases: list[dict] = []

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

        paper_history = PaperHistory(
            paper_id=work.openalex_id,
            publication_year=int(work.publication_year),
            counts=history.counts,
        )
        histories.append(paper_history)

        visible_counts = paper_history.counts_through(cutoff_year)
        features = cutoff_features(visible_counts)
        baseline_scores = {
            strategy: baseline_score(features, strategy)
            for strategy in DEFAULT_STRATEGIES
        }

        outcome = build_outcome_record(
            paper_id=work.openalex_id,
            publication_year=int(work.publication_year),
            counts=history.counts,
            cutoff_year=cutoff_year,
        )
        outcome_records.append(outcome)

        cases.append(
            {
                "paper_id": work.openalex_id,
                "doi": work.doi,
                "title": work.title,
                "publication_year": work.publication_year,
                "primary_topic": work.primary_topic,
                "citations_through_observation_end": history.total_citations,
                "annual_citation_counts": list(history.counts),
                "cutoff_citation_counts": list(visible_counts),
                "cutoff_features": features.as_dict(),
                "baseline_scores": baseline_scores,
                **outcome.as_dict(),
            }
        )

    bundle = outcome_bundle(
        outcome_records,
        beauty_fraction=beauty_fraction,
        acceleration_fraction=acceleration_fraction,
        horizon_years=awakening_horizon_years,
        uptake_fraction=uptake_fraction,
    )
    outcomes = {
        name: (OUTCOME_TYPES[name], relevance)
        for name, relevance in bundle.items()
    }

    matrix = evaluate_outcome_matrix(
        histories,
        cutoff_year=cutoff_year,
        strategies=DEFAULT_STRATEGIES,
        outcomes=outcomes,
        k=review_budget_k,
    )

    case_by_id = {row["paper_id"]: row for row in cases}
    for outcome_name, values in bundle.items():
        for paper_id, value in values.items():
            case_by_id[paper_id].setdefault("outcomes", {})[
                outcome_name
            ] = value

    outcome_summary = {}
    for name, values in bundle.items():
        kind = OUTCOME_TYPES[name]
        summary = {
            "relevance_type": kind,
            "n": len(values),
        }
        if kind == "binary":
            summary["n_positive"] = int(sum(values.values()))
            summary["positive_rate"] = (
                sum(values.values()) / len(values) if values else 0.0
            )
        else:
            summary["mean_relevance"] = (
                sum(values.values()) / len(values) if values else 0.0
            )
        outcome_summary[name] = summary

    analyzed_ids = [row["paper_id"] for row in cases]

    return {
        "benchmark_type": (
            "Pilot 1 non-hand-picked multi-outcome historical cohort"
        ),
        "claim_boundary": (
            "This benchmark evaluates time-safe baselines under multiple "
            "future delayed-recognition definitions. It does not establish "
            "scientific validity, intrinsic importance, or reliable future "
            "breakthrough prediction."
        ),
        "sampling": {
            "source": "OpenAlex live API",
            "filters": filters,
            "sample_size_requested": sample_size,
            "sample_size_analyzed": len(histories),
            "seed": seed,
            "sample_id_sha256": _hash_ids(analyzed_ids),
            "sampling_method": "OpenAlex sample + seed",
            "field_assignment_temporality": (
                "current OpenAlex primary-topic field; stratification only"
            ),
        },
        "temporal_design": {
            "feature_cutoff_year": cutoff_year,
            "outcome_observation_end_year": observation_end_year,
            "future_acceleration_window": (
                "first up-to-3 years after feature cutoff"
            ),
        },
        "outcome_definitions": {
            "beauty_top_fraction": beauty_fraction,
            "future_acceleration_top_fraction": acceleration_fraction,
            "future_uptake_top_fraction": uptake_fraction,
            "awakening_horizon_years": awakening_horizon_years,
            "consensus_min_components": 2,
            "universal_sleeping_beauty_definition": False,
        },
        "outcome_summary": outcome_summary,
        "review_budget_k": review_budget_k,
        "strategies": list(DEFAULT_STRATEGIES),
        "outcome_baseline_matrix": matrix,
        "cases": cases,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=20)
    parser.add_argument("--seed", type=int, default=15015)
    parser.add_argument("--filters", default=DEFAULT_FILTERS)
    parser.add_argument("--cutoff-year", type=int, default=1995)
    parser.add_argument("--observation-end-year", type=int, default=2011)
    parser.add_argument("--beauty-fraction", type=float, default=0.20)
    parser.add_argument("--acceleration-fraction", type=float, default=0.20)
    parser.add_argument("--uptake-fraction", type=float, default=0.50)
    parser.add_argument("--awakening-horizon-years", type=int, default=15)
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
        beauty_fraction=args.beauty_fraction,
        acceleration_fraction=args.acceleration_fraction,
        uptake_fraction=args.uptake_fraction,
        awakening_horizon_years=args.awakening_horizon_years,
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
