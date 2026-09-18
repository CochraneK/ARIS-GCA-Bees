"""Historical-cutoff baseline evaluation for ARIS4C015.

This module deliberately separates:
- features visible at cutoff T; from
- future relevance/outcomes used only for evaluation.

It therefore does not hard-code one definition of a future Sleeping Beauty.
A caller can supply binary or graded future relevance under any prespecified
label definition and compare transparent cutoff-safe baselines.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from baselines import baseline_score, cutoff_features
from ranking_metrics import RankedItem, evaluate_ranking


@dataclass(frozen=True)
class PaperHistory:
    paper_id: str
    publication_year: int
    counts: tuple[int, ...]

    @property
    def end_year(self) -> int:
        return self.publication_year + len(self.counts) - 1

    def counts_through(self, cutoff_year: int) -> tuple[int, ...]:
        if cutoff_year < self.publication_year:
            raise ValueError(
                f"cutoff {cutoff_year} predates {self.paper_id} publication"
            )
        last_index = min(
            cutoff_year - self.publication_year,
            len(self.counts) - 1,
        )
        return self.counts[: last_index + 1]


def score_at_cutoff(
    history: PaperHistory,
    *,
    cutoff_year: int,
    strategy: str,
) -> float:
    """Compute one deterministic baseline from cutoff-visible citations."""
    visible = history.counts_through(cutoff_year)
    features = cutoff_features(visible)
    return baseline_score(features, strategy)


def build_ranked_items(
    histories: Iterable[PaperHistory],
    *,
    cutoff_year: int,
    strategy: str,
    future_relevance: Mapping[str, float],
) -> list[RankedItem]:
    """Build ranked-evaluation items without exposing future relevance to score."""
    items: list[RankedItem] = []
    for history in histories:
        if history.paper_id not in future_relevance:
            continue
        score = score_at_cutoff(
            history,
            cutoff_year=cutoff_year,
            strategy=strategy,
        )
        items.append(
            RankedItem(
                paper_id=history.paper_id,
                score=score,
                relevance=float(future_relevance[history.paper_id]),
            )
        )
    return items


def evaluate_baseline(
    histories: Sequence[PaperHistory],
    *,
    cutoff_year: int,
    strategy: str,
    future_relevance: Mapping[str, float],
    k: int,
) -> dict[str, float | int | str]:
    """Evaluate one baseline at fixed review budget K."""
    items = build_ranked_items(
        histories,
        cutoff_year=cutoff_year,
        strategy=strategy,
        future_relevance=future_relevance,
    )
    metrics = evaluate_ranking(items, k=k)
    return {
        "cutoff_year": cutoff_year,
        "strategy": strategy,
        **metrics,
    }


def evaluate_strategies(
    histories: Sequence[PaperHistory],
    *,
    cutoff_year: int,
    strategies: Sequence[str],
    future_relevance: Mapping[str, float],
    k: int,
) -> list[dict[str, float | int | str]]:
    """Evaluate a prespecified family of transparent baselines."""
    return [
        evaluate_baseline(
            histories,
            cutoff_year=cutoff_year,
            strategy=strategy,
            future_relevance=future_relevance,
            k=k,
        )
        for strategy in strategies
    ]


def evaluate_graded_baseline(
    histories: Sequence[PaperHistory],
    *,
    cutoff_year: int,
    strategy: str,
    future_relevance: Mapping[str, float],
    k: int,
) -> dict[str, float | int | str]:
    """Evaluate a baseline against graded relevance using NDCG@K only.

    Precision@K / Recall@K require a binary relevance definition and are not
    reported here merely by thresholding every positive percentile.
    """
    items = build_ranked_items(
        histories,
        cutoff_year=cutoff_year,
        strategy=strategy,
        future_relevance=future_relevance,
    )
    from ranking_metrics import ndcg_at_k

    return {
        "cutoff_year": cutoff_year,
        "strategy": strategy,
        "n": len(items),
        "k": min(k, len(items)),
        "ndcg_at_k": ndcg_at_k(items, k) if items else 0.0,
        "relevance_type": "graded",
    }


def evaluate_outcome_matrix(
    histories: Sequence[PaperHistory],
    *,
    cutoff_year: int,
    strategies: Sequence[str],
    outcomes: Mapping[str, tuple[str, Mapping[str, float]]],
    k: int,
) -> dict[str, list[dict[str, float | int | str]]]:
    """Evaluate strategies against multiple prespecified future outcomes.

    outcomes maps:
        outcome_name -> ("binary" | "graded", relevance_mapping)

    Future relevance is used only by the evaluator, never by baseline scoring.
    """
    result: dict[str, list[dict[str, float | int | str]]] = {}
    for outcome_name, (kind, relevance) in outcomes.items():
        if kind not in {"binary", "graded"}:
            raise ValueError(
                f"Unsupported outcome relevance type for {outcome_name}: {kind}"
            )
        rows = []
        for strategy in strategies:
            if kind == "binary":
                row = evaluate_baseline(
                    histories,
                    cutoff_year=cutoff_year,
                    strategy=strategy,
                    future_relevance=relevance,
                    k=k,
                )
                row["relevance_type"] = "binary"
            else:
                row = evaluate_graded_baseline(
                    histories,
                    cutoff_year=cutoff_year,
                    strategy=strategy,
                    future_relevance=relevance,
                    k=k,
                )
            rows.append(row)
        result[outcome_name] = rows
    return result
