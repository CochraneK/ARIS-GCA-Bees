"""Transparent prospective baselines for ARIS4C015.

These baselines are deliberately simple. They establish the minimum standard
that any future learned Sleeping Beauty model must beat under historical-cutoff
evaluation.

No journal, institution, country, author fame, or other prestige proxy is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from sb_metrics import beauty_coefficient


@dataclass(frozen=True)
class CutoffFeatures:
    total_citations: int
    recent_1y: int
    recent_3y: int
    previous_3y: int
    acceleration_3y: float
    zero_citation_years: int
    longest_zero_run: int
    partial_beauty: float

    def as_dict(self) -> dict[str, float | int]:
        return {
            "total_citations": self.total_citations,
            "recent_1y": self.recent_1y,
            "recent_3y": self.recent_3y,
            "previous_3y": self.previous_3y,
            "acceleration_3y": self.acceleration_3y,
            "zero_citation_years": self.zero_citation_years,
            "longest_zero_run": self.longest_zero_run,
            "partial_beauty": self.partial_beauty,
        }


def _nonnegative_ints(citations: Sequence[int | float]) -> list[int]:
    values = [int(x) for x in citations]
    if not values:
        raise ValueError("citations must be non-empty")
    if any(x < 0 for x in values):
        raise ValueError("citation counts must be non-negative")
    return values


def _longest_zero_run(values: Sequence[int]) -> int:
    best = 0
    current = 0
    for value in values:
        if value == 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def cutoff_features(citations: Sequence[int | float]) -> CutoffFeatures:
    """Compute features using only the observed history up to a cutoff."""
    c = _nonnegative_ints(citations)
    recent_1 = c[-1]
    recent_3 = sum(c[-3:])
    previous_3 = sum(c[-6:-3]) if len(c) > 3 else 0

    # Difference in annualized 3-year citation rates.
    recent_den = min(3, len(c))
    previous_len = min(3, max(0, len(c) - 3))
    recent_rate = recent_3 / recent_den
    previous_rate = previous_3 / previous_len if previous_len else 0.0

    return CutoffFeatures(
        total_citations=sum(c),
        recent_1y=recent_1,
        recent_3y=recent_3,
        previous_3y=previous_3,
        acceleration_3y=recent_rate - previous_rate,
        zero_citation_years=sum(1 for x in c if x == 0),
        longest_zero_run=_longest_zero_run(c),
        partial_beauty=beauty_coefficient(c),
    )


def baseline_score(features: CutoffFeatures, strategy: str) -> float:
    """Return one transparent baseline score.

    Supported strategies
    --------------------
    current_citations:
        Total citations visible at cutoff.
    momentum_3y:
        Citations in the most recent three years.
    acceleration_3y:
        Change in annualized citation rate versus the preceding three years.
    partial_beauty:
        Beauty Coefficient computed only on the partial trajectory visible by
        cutoff. This is a geometric baseline, not a future outcome.
    dormancy:
        Longest zero-citation run. Useful as a deliberately naive baseline.
    """
    mapping = {
        "current_citations": float(features.total_citations),
        "momentum_3y": float(features.recent_3y),
        "acceleration_3y": float(features.acceleration_3y),
        "partial_beauty": float(features.partial_beauty),
        "dormancy": float(features.longest_zero_run),
    }
    if strategy not in mapping:
        raise ValueError(
            "Unknown strategy. Choose one of: " + ", ".join(sorted(mapping))
        )
    return mapping[strategy]


def rank_histories(
    histories: Iterable[tuple[str, Sequence[int | float]]],
    *,
    strategy: str,
) -> list[tuple[str, float]]:
    """Rank paper histories descending by one deterministic baseline."""
    scored = [
        (paper_id, baseline_score(cutoff_features(citations), strategy))
        for paper_id, citations in histories
    ]
    return sorted(scored, key=lambda item: (-item[1], item[0]))
