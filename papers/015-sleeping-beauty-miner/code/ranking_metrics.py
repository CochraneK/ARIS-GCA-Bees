"""Evaluation metrics for ARIS4C015 historical-cutoff benchmarks.

The implementation is dependency-free so Pilot 0 and CI do not require
scikit-learn. Definitions follow standard information-retrieval / probability
scoring conventions.

NDCG here uses:
    DCG@K = sum(relevance_i / log2(rank_i + 1))
and divides by the ideal DCG under perfect ordering.

Brier score for binary outcomes is:
    mean((probability - outcome) ** 2)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class RankedItem:
    paper_id: str
    score: float
    relevance: float


def _rank(items: Iterable[RankedItem]) -> list[RankedItem]:
    """Sort descending score with deterministic paper-id tie break."""
    return sorted(items, key=lambda x: (-float(x.score), x.paper_id))


def _validate_k(k: int, n: int) -> int:
    if k < 1:
        raise ValueError("k must be >= 1")
    return min(k, n)


def precision_at_k(items: Sequence[RankedItem], k: int) -> float:
    """Binary Precision@K, treating relevance > 0 as positive."""
    if not items:
        return 0.0
    ranked = _rank(items)
    k2 = _validate_k(k, len(ranked))
    positives = sum(1 for item in ranked[:k2] if item.relevance > 0)
    return positives / k2


def recall_at_k(items: Sequence[RankedItem], k: int) -> float:
    """Binary Recall@K, treating relevance > 0 as positive."""
    if not items:
        return 0.0
    total_positive = sum(1 for item in items if item.relevance > 0)
    if total_positive == 0:
        return 0.0
    ranked = _rank(items)
    k2 = _validate_k(k, len(ranked))
    retrieved = sum(1 for item in ranked[:k2] if item.relevance > 0)
    return retrieved / total_positive


def dcg_at_k(items: Sequence[RankedItem], k: int) -> float:
    """Discounted cumulative gain using non-negative graded relevance."""
    if not items:
        return 0.0
    if any(item.relevance < 0 for item in items):
        raise ValueError("NDCG relevance must be non-negative")
    ranked = _rank(items)
    k2 = _validate_k(k, len(ranked))
    return sum(
        item.relevance / math.log2(rank + 1)
        for rank, item in enumerate(ranked[:k2], start=1)
    )


def ndcg_at_k(items: Sequence[RankedItem], k: int) -> float:
    """Normalized DCG@K in [0, 1] for non-negative relevance."""
    if not items:
        return 0.0
    actual = dcg_at_k(items, k)
    ideal_items = [
        RankedItem(
            paper_id=item.paper_id,
            score=float(item.relevance),
            relevance=float(item.relevance),
        )
        for item in items
    ]
    ideal = dcg_at_k(ideal_items, k)
    return actual / ideal if ideal > 0 else 0.0


def brier_score(
    outcomes: Sequence[int | bool],
    probabilities: Sequence[float],
) -> float:
    """Binary Brier score; lower is better."""
    if len(outcomes) != len(probabilities):
        raise ValueError("outcomes and probabilities must have equal length")
    if not outcomes:
        raise ValueError("at least one observation is required")

    total = 0.0
    for outcome, probability in zip(outcomes, probabilities):
        y = int(outcome)
        p = float(probability)
        if y not in {0, 1}:
            raise ValueError("outcomes must be binary")
        if not 0.0 <= p <= 1.0:
            raise ValueError("probabilities must be in [0, 1]")
        total += (p - y) ** 2
    return total / len(outcomes)


def calibration_bins(
    outcomes: Sequence[int | bool],
    probabilities: Sequence[float],
    *,
    n_bins: int = 10,
) -> list[dict[str, float | int]]:
    """Return equal-width reliability bins for descriptive calibration audit."""
    if len(outcomes) != len(probabilities):
        raise ValueError("outcomes and probabilities must have equal length")
    if n_bins < 1:
        raise ValueError("n_bins must be >= 1")

    bins: list[list[tuple[int, float]]] = [[] for _ in range(n_bins)]
    for outcome, probability in zip(outcomes, probabilities):
        y = int(outcome)
        p = float(probability)
        if y not in {0, 1}:
            raise ValueError("outcomes must be binary")
        if not 0.0 <= p <= 1.0:
            raise ValueError("probabilities must be in [0, 1]")
        index = min(int(p * n_bins), n_bins - 1)
        bins[index].append((y, p))

    result: list[dict[str, float | int]] = []
    for index, rows in enumerate(bins):
        if not rows:
            continue
        result.append(
            {
                "bin": index,
                "count": len(rows),
                "mean_probability": sum(p for _, p in rows) / len(rows),
                "event_rate": sum(y for y, _ in rows) / len(rows),
            }
        )
    return result


def evaluate_ranking(
    items: Sequence[RankedItem],
    *,
    k: int,
) -> dict[str, float | int]:
    """Convenience wrapper for a fixed human-review budget K."""
    return {
        "n": len(items),
        "k": min(k, len(items)),
        "precision_at_k": precision_at_k(items, k) if items else 0.0,
        "recall_at_k": recall_at_k(items, k) if items else 0.0,
        "ndcg_at_k": ndcg_at_k(items, k) if items else 0.0,
    }
