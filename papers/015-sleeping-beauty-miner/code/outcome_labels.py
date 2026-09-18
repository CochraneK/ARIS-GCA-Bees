"""Future outcome definitions for ARIS4C015 historical backtests.

All functions in this module operate on the *held-out future* portion of a
paper's trajectory or on full-history retrospective metrics. They must never be
used as prospective features.

The module intentionally supports several outcomes because there is no single
universally correct definition of a Sleeping Beauty.

Outcome families
----------------
1. future citation acceleration;
2. full-history Beauty Coefficient percentile;
3. awakening within a future horizon after cutoff;
4. delayed-recognition composite based on multiple prespecified criteria;
5. later-uptake sensitivity, used to distinguish delayed recognition from
   trajectories that remain scarcely cited.

No outcome here is equivalent to "scientific truth", "breakthrough", or
"intrinsic value".
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from sb_metrics import retrospective_summary


@dataclass(frozen=True)
class OutcomeRecord:
    paper_id: str
    publication_year: int
    cutoff_year: int
    observation_end_year: int
    full_counts: tuple[int, ...]
    beauty_coefficient: float
    awakening_year: int
    future_citations: int
    pre_cutoff_citations: int
    future_acceleration: float

    def as_dict(self) -> dict:
        return {
            "paper_id": self.paper_id,
            "publication_year": self.publication_year,
            "cutoff_year": self.cutoff_year,
            "observation_end_year": self.observation_end_year,
            "beauty_coefficient": self.beauty_coefficient,
            "awakening_year": self.awakening_year,
            "future_citations": self.future_citations,
            "pre_cutoff_citations": self.pre_cutoff_citations,
            "future_acceleration": self.future_acceleration,
        }


def _validate_counts(counts: Sequence[int | float]) -> tuple[int, ...]:
    values = tuple(int(x) for x in counts)
    if not values:
        raise ValueError("citation history must be non-empty")
    if any(x < 0 for x in values):
        raise ValueError("citation counts must be non-negative")
    return values


def build_outcome_record(
    *,
    paper_id: str,
    publication_year: int,
    counts: Sequence[int | float],
    cutoff_year: int,
) -> OutcomeRecord:
    """Build held-out future outcomes from a complete observed trajectory."""
    values = _validate_counts(counts)
    observation_end_year = publication_year + len(values) - 1
    if cutoff_year < publication_year:
        raise ValueError("cutoff predates publication")
    if cutoff_year >= observation_end_year:
        raise ValueError("cutoff must precede observation endpoint")

    cutoff_index = cutoff_year - publication_year
    visible = values[: cutoff_index + 1]
    future = values[cutoff_index + 1 :]
    metrics = retrospective_summary(values)

    pre_window = visible[-min(3, len(visible)) :]
    future_window = future[: min(3, len(future))]
    pre_rate = sum(pre_window) / len(pre_window) if pre_window else 0.0
    future_rate = sum(future_window) / len(future_window) if future_window else 0.0

    awakening_year = publication_year + int(metrics["awakening_time"])

    return OutcomeRecord(
        paper_id=str(paper_id),
        publication_year=int(publication_year),
        cutoff_year=int(cutoff_year),
        observation_end_year=int(observation_end_year),
        full_counts=values,
        beauty_coefficient=float(metrics["beauty_coefficient"]),
        awakening_year=awakening_year,
        future_citations=sum(future),
        pre_cutoff_citations=sum(visible),
        future_acceleration=future_rate - pre_rate,
    )


def percentile_ranks(
    values: Mapping[str, float],
) -> dict[str, float]:
    """Empirical percentile ranks in [0, 1] using average ranks for ties."""
    if not values:
        return {}

    ordered = sorted(values.items(), key=lambda item: (item[1], item[0]))
    n = len(ordered)
    result: dict[str, float] = {}

    i = 0
    while i < n:
        j = i + 1
        while j < n and ordered[j][1] == ordered[i][1]:
            j += 1
        avg_rank = (i + (j - 1)) / 2
        percentile = avg_rank / (n - 1) if n > 1 else 1.0
        for index in range(i, j):
            result[ordered[index][0]] = percentile
        i = j

    return result


def top_fraction_binary(
    values: Mapping[str, float],
    *,
    fraction: float,
) -> dict[str, float]:
    """Mark the top prespecified fraction as 1.0, others 0.0.

    Ties at the boundary are resolved deterministically by paper_id so the
    number of positives remains fixed for reproducible benchmark plumbing.
    """
    if not 0 < fraction <= 1:
        raise ValueError("fraction must be in (0, 1]")
    if not values:
        return {}

    ordered = sorted(values.items(), key=lambda item: (-item[1], item[0]))
    n_positive = max(1, math.ceil(len(ordered) * fraction))
    positive = {paper_id for paper_id, _ in ordered[:n_positive]}
    return {
        paper_id: 1.0 if paper_id in positive else 0.0
        for paper_id in values
    }


def beauty_percentile_outcome(
    records: Iterable[OutcomeRecord],
) -> dict[str, float]:
    """Graded outcome: within-cohort percentile of full-history B."""
    rows = list(records)
    return percentile_ranks(
        {row.paper_id: row.beauty_coefficient for row in rows}
    )


def beauty_top_fraction_outcome(
    records: Iterable[OutcomeRecord],
    *,
    fraction: float = 0.20,
) -> dict[str, float]:
    """Binary outcome: top fraction by full-history B."""
    rows = list(records)
    return top_fraction_binary(
        {row.paper_id: row.beauty_coefficient for row in rows},
        fraction=fraction,
    )


def future_acceleration_percentile_outcome(
    records: Iterable[OutcomeRecord],
) -> dict[str, float]:
    """Graded outcome: percentile of immediate post-cutoff acceleration."""
    rows = list(records)
    return percentile_ranks(
        {row.paper_id: row.future_acceleration for row in rows}
    )


def future_uptake_percentile_outcome(
    records: Iterable[OutcomeRecord],
) -> dict[str, float]:
    """Graded outcome: percentile of all held-out post-cutoff citations."""
    rows = list(records)
    return percentile_ranks(
        {row.paper_id: float(row.future_citations) for row in rows}
    )


def future_uptake_top_fraction_outcome(
    records: Iterable[OutcomeRecord],
    *,
    fraction: float = 0.50,
) -> dict[str, float]:
    """Binary later-uptake sensitivity label.

    This is not itself a Sleeping Beauty definition. It is used as a floor to
    distinguish a delayed-looking trajectory from one that remains scarcely
    cited throughout the future observation window.
    """
    rows = list(records)
    return top_fraction_binary(
        {row.paper_id: float(row.future_citations) for row in rows},
        fraction=fraction,
    )


def awakening_within_horizon_outcome(
    records: Iterable[OutcomeRecord],
    *,
    horizon_years: int,
    require_post_cutoff: bool = True,
) -> dict[str, float]:
    """Binary outcome for awakening within H years after the cutoff.

    If require_post_cutoff=True, papers whose retrospective awakening is at or
    before the cutoff are negatives; the target is newly awakening papers.
    """
    if horizon_years < 1:
        raise ValueError("horizon_years must be >= 1")

    result: dict[str, float] = {}
    for row in records:
        lower_ok = (
            row.awakening_year > row.cutoff_year
            if require_post_cutoff
            else row.awakening_year >= row.cutoff_year
        )
        upper_ok = row.awakening_year <= row.cutoff_year + horizon_years
        result[row.paper_id] = 1.0 if lower_ok and upper_ok else 0.0
    return result


def delayed_recognition_consensus_outcome(
    records: Iterable[OutcomeRecord],
    *,
    beauty_fraction: float = 0.20,
    acceleration_fraction: float = 0.20,
    horizon_years: int = 15,
    min_components: int = 2,
) -> dict[str, float]:
    """Binary multi-definition consensus label.

    Components:
    - top beauty_fraction by full-history B;
    - top acceleration_fraction by immediate future acceleration;
    - awakening after cutoff but within horizon_years.

    A paper is positive if at least min_components criteria are met.

    This remains a benchmark definition, not a claim of scientific importance.
    """
    rows = list(records)
    if not rows:
        return {}
    if min_components < 1 or min_components > 3:
        raise ValueError("min_components must be between 1 and 3")

    beauty = beauty_top_fraction_outcome(rows, fraction=beauty_fraction)
    accel = top_fraction_binary(
        {row.paper_id: row.future_acceleration for row in rows},
        fraction=acceleration_fraction,
    )
    awake = awakening_within_horizon_outcome(
        rows,
        horizon_years=horizon_years,
        require_post_cutoff=True,
    )

    return {
        row.paper_id: 1.0
        if (
            int(beauty[row.paper_id])
            + int(accel[row.paper_id])
            + int(awake[row.paper_id])
        )
        >= min_components
        else 0.0
        for row in rows
    }


def delayed_recognition_with_uptake_floor_outcome(
    records: Iterable[OutcomeRecord],
    *,
    beauty_fraction: float = 0.20,
    acceleration_fraction: float = 0.20,
    horizon_years: int = 15,
    uptake_fraction: float = 0.50,
    min_components: int = 2,
) -> dict[str, float]:
    """Consensus delayed-recognition label plus later-uptake floor.

    A paper must first satisfy the delayed-recognition consensus definition and
    then fall in the top uptake_fraction share by total held-out future
    citations.

    This is a sensitivity analysis, not a replacement for the raw B metric and
    not a universal definition of scientific importance.
    """
    rows = list(records)
    consensus = delayed_recognition_consensus_outcome(
        rows,
        beauty_fraction=beauty_fraction,
        acceleration_fraction=acceleration_fraction,
        horizon_years=horizon_years,
        min_components=min_components,
    )
    uptake = future_uptake_top_fraction_outcome(
        rows,
        fraction=uptake_fraction,
    )
    return {
        row.paper_id: 1.0
        if consensus[row.paper_id] and uptake[row.paper_id]
        else 0.0
        for row in rows
    }


def outcome_bundle(
    records: Iterable[OutcomeRecord],
    *,
    beauty_fraction: float = 0.20,
    acceleration_fraction: float = 0.20,
    horizon_years: int = 15,
    uptake_fraction: float = 0.50,
) -> dict[str, dict[str, float]]:
    """Return a standard multi-outcome bundle for one historical cohort."""
    rows = list(records)
    return {
        "beauty_percentile": beauty_percentile_outcome(rows),
        "beauty_top_fraction": beauty_top_fraction_outcome(
            rows,
            fraction=beauty_fraction,
        ),
        "future_acceleration_percentile": future_acceleration_percentile_outcome(
            rows
        ),
        "future_uptake_percentile": future_uptake_percentile_outcome(rows),
        "awakening_within_horizon": awakening_within_horizon_outcome(
            rows,
            horizon_years=horizon_years,
        ),
        "delayed_recognition_consensus": delayed_recognition_consensus_outcome(
            rows,
            beauty_fraction=beauty_fraction,
            acceleration_fraction=acceleration_fraction,
            horizon_years=horizon_years,
        ),
        "delayed_recognition_with_uptake_floor": (
            delayed_recognition_with_uptake_floor_outcome(
                rows,
                beauty_fraction=beauty_fraction,
                acceleration_fraction=acceleration_fraction,
                horizon_years=horizon_years,
                uptake_fraction=uptake_fraction,
            )
        ),
    }
