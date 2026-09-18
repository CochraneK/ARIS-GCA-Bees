"""Transparent Prince-paper candidate extraction for ARIS4C015.

A Prince candidate is a citing work temporally close to an observed awakening.
This module does *not* infer causality and does not collapse multiple possible
awakening pathways into one winner.

The basic extractor is deliberately conservative:
- candidate must directly cite the target;
- candidate publication year must fall within a declared window around the
  observed awakening;
- optional downstream evidence such as later co-citation count, community
  spread, or semantic similarity is preserved as separate fields.

No weighted Prince score is emitted by default.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PrinceCandidate:
    paper_id: str
    publication_year: int
    temporal_distance: int
    before_or_at_awakening: bool
    later_cocitation_count: int | None = None
    community_spread: int | None = None
    semantic_similarity: float | None = None

    def as_dict(self) -> dict:
        return {
            "paper_id": self.paper_id,
            "publication_year": self.publication_year,
            "temporal_distance": self.temporal_distance,
            "before_or_at_awakening": self.before_or_at_awakening,
            "later_cocitation_count": self.later_cocitation_count,
            "community_spread": self.community_spread,
            "semantic_similarity": self.semantic_similarity,
            "causal_claim": False,
        }


@dataclass(frozen=True)
class CitingWork:
    paper_id: str
    publication_year: int
    later_cocitation_count: int | None = None
    community_spread: int | None = None
    semantic_similarity: float | None = None


def _validate_optional_nonnegative(value: int | None, name: str) -> None:
    if value is not None and int(value) < 0:
        raise ValueError(f"{name} must be non-negative when supplied")


def _validate_similarity(value: float | None) -> None:
    if value is not None and not 0.0 <= float(value) <= 1.0:
        raise ValueError("semantic_similarity must be in [0, 1] when supplied")


def extract_prince_candidates(
    citing_works: Iterable[CitingWork],
    *,
    awakening_year: int,
    years_before: int = 5,
    years_after: int = 2,
) -> list[PrinceCandidate]:
    """Extract direct citing works near the observed awakening.

    Sorting is a review convenience, not a causal ranking:
    1. absolute temporal proximity;
    2. pre-/at-awakening before post-awakening for exact ties;
    3. larger later co-citation count when available;
    4. paper_id for deterministic ties.
    """
    if years_before < 0 or years_after < 0:
        raise ValueError("Prince windows must be non-negative")

    lo = int(awakening_year) - int(years_before)
    hi = int(awakening_year) + int(years_after)
    candidates: list[PrinceCandidate] = []

    for work in citing_works:
        _validate_optional_nonnegative(
            work.later_cocitation_count,
            "later_cocitation_count",
        )
        _validate_optional_nonnegative(
            work.community_spread,
            "community_spread",
        )
        _validate_similarity(work.semantic_similarity)

        year = int(work.publication_year)
        if year < lo or year > hi:
            continue

        candidates.append(
            PrinceCandidate(
                paper_id=str(work.paper_id),
                publication_year=year,
                temporal_distance=abs(year - int(awakening_year)),
                before_or_at_awakening=year <= int(awakening_year),
                later_cocitation_count=(
                    int(work.later_cocitation_count)
                    if work.later_cocitation_count is not None
                    else None
                ),
                community_spread=(
                    int(work.community_spread)
                    if work.community_spread is not None
                    else None
                ),
                semantic_similarity=(
                    float(work.semantic_similarity)
                    if work.semantic_similarity is not None
                    else None
                ),
            )
        )

    def key(candidate: PrinceCandidate) -> tuple:
        cocitations = (
            candidate.later_cocitation_count
            if candidate.later_cocitation_count is not None
            else -1
        )
        return (
            candidate.temporal_distance,
            0 if candidate.before_or_at_awakening else 1,
            -cocitations,
            candidate.paper_id,
        )

    return sorted(candidates, key=key)


def prince_evidence_coverage(
    candidates: Iterable[PrinceCandidate],
) -> dict[str, int | float]:
    """Summarize which optional Prince evidence channels are available."""
    rows = list(candidates)
    n = len(rows)
    if n == 0:
        return {
            "n_candidates": 0,
            "cocitation_coverage": 0.0,
            "community_coverage": 0.0,
            "semantic_coverage": 0.0,
        }

    return {
        "n_candidates": n,
        "cocitation_coverage": sum(
            row.later_cocitation_count is not None for row in rows
        ) / n,
        "community_coverage": sum(
            row.community_spread is not None for row in rows
        ) / n,
        "semantic_coverage": sum(
            row.semantic_similarity is not None for row in rows
        ) / n,
    }
