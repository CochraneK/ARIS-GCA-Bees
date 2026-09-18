"""Matched-control construction for the ARIS4C015 mechanism track.

The primary causal-comparison intuition is not:
    Sleeping Beauty vs every other paper.

Instead, compare papers that were similar on pre-awakening observables but
followed different later trajectories.

Priority contrasts
------------------
1. SLEEPING_BEAUTY vs FORGOTTEN
   Both start with low attention. Why does one later awaken while the other
   remains ignored?

2. SLEEPING_BEAUTY vs IMMEDIATE_HIT
   Both eventually receive high attention. Why was one recognized immediately
   while the other was delayed?

3. IMMEDIATE_HIT vs FADING
   Secondary contrast useful for separating durable from transient attention.

Matching variables should be measured at publication / early life and must not
contain post-outcome information.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class MechanismPaper:
    paper_id: str
    state: str
    publication_year: int
    field: str
    early_citation_percentile: float
    reference_count: int | None = None
    author_count: int | None = None
    early_citation_count: int | None = None
    source_id: str | None = None

    def as_dict(self) -> dict:
        return {
            "paper_id": self.paper_id,
            "state": self.state,
            "publication_year": self.publication_year,
            "field": self.field,
            "early_citation_percentile": self.early_citation_percentile,
            "reference_count": self.reference_count,
            "author_count": self.author_count,
            "early_citation_count": self.early_citation_count,
            "source_id": self.source_id,
        }


@dataclass(frozen=True)
class Match:
    case_id: str
    control_id: str
    case_state: str
    control_state: str
    distance: float
    exact_year: bool
    exact_field: bool
    reused_control: bool

    def as_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "control_id": self.control_id,
            "case_state": self.case_state,
            "control_state": self.control_state,
            "distance": self.distance,
            "exact_year": self.exact_year,
            "exact_field": self.exact_field,
            "reused_control": self.reused_control,
        }


DEFAULT_WEIGHTS = {
    "early_citation_percentile": 4.0,
    "reference_count": 1.0,
    "author_count": 0.5,
    "early_citation_count": 1.0,
}


def _scaled_abs(
    left: int | float | None,
    right: int | float | None,
    *,
    scale: float,
) -> float:
    if left is None or right is None:
        return 0.0
    if scale <= 0:
        raise ValueError("scale must be positive")
    return abs(float(left) - float(right)) / scale


def matching_distance(
    case: MechanismPaper,
    control: MechanismPaper,
    *,
    weights: Mapping[str, float] = DEFAULT_WEIGHTS,
    reference_scale: float = 30.0,
    author_scale: float = 5.0,
    early_count_scale: float = 10.0,
) -> float:
    """Interpretable early-life distance; lower is more similar.

    Field/year are handled by exact matching upstream and therefore do not
    enter this continuous distance.
    """
    distance = 0.0
    distance += float(weights.get("early_citation_percentile", 0.0)) * abs(
        case.early_citation_percentile
        - control.early_citation_percentile
    )
    distance += float(weights.get("reference_count", 0.0)) * _scaled_abs(
        case.reference_count,
        control.reference_count,
        scale=reference_scale,
    )
    distance += float(weights.get("author_count", 0.0)) * _scaled_abs(
        case.author_count,
        control.author_count,
        scale=author_scale,
    )
    distance += float(weights.get("early_citation_count", 0.0)) * _scaled_abs(
        case.early_citation_count,
        control.early_citation_count,
        scale=early_count_scale,
    )
    return float(distance)


def eligible_control(
    case: MechanismPaper,
    control: MechanismPaper,
    *,
    control_state: str,
    year_tolerance: int = 0,
    require_same_field: bool = True,
    early_percentile_caliper: float = 0.15,
) -> bool:
    """Eligibility gate using only pre-outcome variables."""
    if control.state != control_state:
        return False
    if case.paper_id == control.paper_id:
        return False
    if require_same_field and case.field != control.field:
        return False
    if abs(case.publication_year - control.publication_year) > year_tolerance:
        return False
    if abs(
        case.early_citation_percentile
        - control.early_citation_percentile
    ) > early_percentile_caliper:
        return False
    return True


def nearest_controls(
    cases: Sequence[MechanismPaper],
    controls: Sequence[MechanismPaper],
    *,
    control_state: str,
    controls_per_case: int = 1,
    with_replacement: bool = False,
    year_tolerance: int = 0,
    require_same_field: bool = True,
    early_percentile_caliper: float = 0.15,
) -> tuple[list[Match], list[str]]:
    """Deterministic nearest-neighbour matching with explicit unmatched cases.

    No post-awakening variables are used for matching.
    """
    if controls_per_case < 1:
        raise ValueError("controls_per_case must be >= 1")
    if year_tolerance < 0:
        raise ValueError("year_tolerance must be non-negative")
    if not 0 <= early_percentile_caliper <= 1:
        raise ValueError("early_percentile_caliper must be in [0,1]")

    used: set[str] = set()
    matches: list[Match] = []
    unmatched: list[str] = []

    for case in sorted(cases, key=lambda x: x.paper_id):
        candidates = []
        for control in controls:
            if not eligible_control(
                case,
                control,
                control_state=control_state,
                year_tolerance=year_tolerance,
                require_same_field=require_same_field,
                early_percentile_caliper=early_percentile_caliper,
            ):
                continue
            if not with_replacement and control.paper_id in used:
                continue
            candidates.append(
                (
                    matching_distance(case, control),
                    control.paper_id,
                    control,
                )
            )

        candidates.sort(key=lambda x: (x[0], x[1]))
        chosen = candidates[:controls_per_case]

        if not chosen:
            unmatched.append(case.paper_id)
            continue

        for distance, _, control in chosen:
            reused = control.paper_id in used
            matches.append(
                Match(
                    case_id=case.paper_id,
                    control_id=control.paper_id,
                    case_state=case.state,
                    control_state=control.state,
                    distance=float(distance),
                    exact_year=(
                        case.publication_year
                        == control.publication_year
                    ),
                    exact_field=case.field == control.field,
                    reused_control=reused,
                )
            )
            used.add(control.paper_id)

    return matches, unmatched


def build_priority_contrasts(
    papers: Iterable[MechanismPaper],
    *,
    controls_per_case: int = 1,
    year_tolerance: int = 0,
    early_percentile_caliper: float = 0.15,
) -> dict:
    """Construct the two primary SB mechanism contrasts."""
    rows = list(papers)
    sb = [row for row in rows if row.state == "SLEEPING_BEAUTY"]

    forgotten_matches, forgotten_unmatched = nearest_controls(
        sb,
        rows,
        control_state="FORGOTTEN",
        controls_per_case=controls_per_case,
        year_tolerance=year_tolerance,
        early_percentile_caliper=early_percentile_caliper,
    )

    # SB vs Immediate Hit intentionally relaxes the early-attention caliper:
    # early attention is the defining contrast. Other exact strata remain.
    immediate_matches, immediate_unmatched = nearest_controls(
        sb,
        rows,
        control_state="IMMEDIATE_HIT",
        controls_per_case=controls_per_case,
        year_tolerance=year_tolerance,
        early_percentile_caliper=1.0,
    )

    return {
        "SB_vs_FORGOTTEN": {
            "question": (
                "Both were initially low-attention; why did the SB later "
                "awaken while the control remained forgotten?"
            ),
            "matches": [row.as_dict() for row in forgotten_matches],
            "unmatched_cases": forgotten_unmatched,
        },
        "SB_vs_IMMEDIATE_HIT": {
            "question": (
                "Both ultimately attracted high attention; why was the SB "
                "recognized late while the control was recognized early?"
            ),
            "matches": [row.as_dict() for row in immediate_matches],
            "unmatched_cases": immediate_unmatched,
        },
        "matching_rule": {
            "post_outcome_variables_used": False,
            "same_field": True,
            "year_tolerance": year_tolerance,
            "controls_per_case": controls_per_case,
            "early_percentile_caliper_SB_vs_FORGOTTEN": (
                early_percentile_caliper
            ),
            "early_percentile_caliper_SB_vs_IMMEDIATE_HIT": 1.0,
            "replacement": False,
        },
    }
