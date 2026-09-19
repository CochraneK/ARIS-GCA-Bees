"""Risk-set matching for ARIS4C015 Sleeping Beauty mechanisms.

Primary mechanism question
--------------------------
At the time a Sleeping Beauty awakens, what distinguishes it from comparable
papers from the same field/year that are still dormant at that time?

This is preferable to requiring controls to be permanently Forgotten. A
control may awaken later; at the case event time it is simply still at risk.

All matching covariates are measured no later than the case awakening time.
Future control outcomes are retained only for later survival/sensitivity
analysis.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from mechanism_matching import MechanismPaper, standardized_mean_difference


@dataclass(frozen=True)
class RiskSetMatch:
    case_id: str
    control_id: str
    case_event_age: int
    case_sleep_rate: float
    control_rate_to_event: float
    control_first_burst_age: int | None
    control_future_state: str
    distance: float

    def as_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "control_id": self.control_id,
            "case_event_age": self.case_event_age,
            "case_sleep_rate": self.case_sleep_rate,
            "control_rate_to_event": self.control_rate_to_event,
            "control_first_burst_age": self.control_first_burst_age,
            "control_future_state": self.control_future_state,
            "distance": self.distance,
        }


def window_rate(
    counts: Sequence[int],
    *,
    start: int,
    years: int,
) -> float | None:
    if start < 0 or years < 1:
        raise ValueError("invalid window")
    stop = start + years
    if stop > len(counts):
        return None
    window = counts[start:stop]
    return sum(float(x) for x in window) / years


def first_burst_age(
    counts: Sequence[int],
    *,
    wake_years: int = 4,
    min_wake_rate: float = 5.0,
) -> int | None:
    """Earliest rolling-window start with mean citation rate > threshold."""
    if wake_years < 1:
        raise ValueError("wake_years must be >= 1")
    for start in range(0, len(counts) - wake_years + 1):
        rate = window_rate(counts, start=start, years=wake_years)
        if rate is not None and rate > min_wake_rate:
            return start
    return None


def rate_to_age(
    paper: MechanismPaper,
    age: int,
) -> float | None:
    if age < 1:
        raise ValueError("age must be >= 1")
    if paper.annual_citation_counts is None:
        return None
    if len(paper.annual_citation_counts) < age:
        return None
    return (
        sum(float(x) for x in paper.annual_citation_counts[:age])
        / age
    )


def is_at_risk_dormant_control(
    case: MechanismPaper,
    control: MechanismPaper,
    *,
    max_sleep_rate: float = 2.0,
    wake_years: int = 4,
    min_wake_rate: float = 5.0,
) -> tuple[bool, float | None, int | None]:
    """Whether control is still dormant immediately before case awakening."""
    if case.robust_sleep_years is None:
        return False, None, None
    if case.paper_id == control.paper_id:
        return False, None, None
    if case.field != control.field:
        return False, None, None
    if case.publication_year != control.publication_year:
        return False, None, None
    if control.annual_citation_counts is None:
        return False, None, None

    event_age = case.robust_sleep_years
    control_rate = rate_to_age(control, event_age)
    if control_rate is None or control_rate > max_sleep_rate:
        return False, control_rate, None

    burst_age = first_burst_age(
        control.annual_citation_counts,
        wake_years=wake_years,
        min_wake_rate=min_wake_rate,
    )

    # A future case is a valid risk-set control provided it has not awakened
    # before or at the index case event age.
    if burst_age is not None and burst_age <= event_age:
        return False, control_rate, burst_age

    return True, control_rate, burst_age


def risk_set_distance(
    case: MechanismPaper,
    control: MechanismPaper,
    *,
    control_rate: float,
) -> float:
    """Transparent pre-event distance for risk-set matching."""
    if case.robust_sleep_rate is None:
        raise ValueError("case robust_sleep_rate is required")

    distance = 4.0 * abs(case.robust_sleep_rate - control_rate)

    if case.reference_count is not None and control.reference_count is not None:
        distance += (
            abs(case.reference_count - control.reference_count) / 30.0
        )

    if case.author_count is not None and control.author_count is not None:
        distance += abs(case.author_count - control.author_count) / 5.0

    return float(distance)


def match_awakening_risk_sets(
    papers: Sequence[MechanismPaper],
    *,
    controls_per_case: int = 1,
    with_replacement: bool = False,
    max_sleep_rate: float = 2.0,
    wake_years: int = 4,
    min_wake_rate: float = 5.0,
) -> tuple[list[RiskSetMatch], list[str]]:
    if controls_per_case < 1:
        raise ValueError("controls_per_case must be >= 1")

    cases = [p for p in papers if p.state == "SLEEPING_BEAUTY"]
    used: set[str] = set()
    matches: list[RiskSetMatch] = []
    unmatched: list[str] = []

    for case in sorted(cases, key=lambda p: p.paper_id):
        candidates = []
        for control in papers:
            if not with_replacement and control.paper_id in used:
                continue
            eligible, control_rate, burst_age = is_at_risk_dormant_control(
                case,
                control,
                max_sleep_rate=max_sleep_rate,
                wake_years=wake_years,
                min_wake_rate=min_wake_rate,
            )
            if not eligible or control_rate is None:
                continue
            candidates.append(
                (
                    risk_set_distance(
                        case,
                        control,
                        control_rate=control_rate,
                    ),
                    control.paper_id,
                    control,
                    control_rate,
                    burst_age,
                )
            )

        candidates.sort(key=lambda row: (row[0], row[1]))
        chosen = candidates[:controls_per_case]
        if not chosen:
            unmatched.append(case.paper_id)
            continue

        for distance, _, control, control_rate, burst_age in chosen:
            matches.append(
                RiskSetMatch(
                    case_id=case.paper_id,
                    control_id=control.paper_id,
                    case_event_age=int(case.robust_sleep_years),
                    case_sleep_rate=float(case.robust_sleep_rate),
                    control_rate_to_event=float(control_rate),
                    control_first_burst_age=burst_age,
                    control_future_state=control.state,
                    distance=float(distance),
                )
            )
            used.add(control.paper_id)

    return matches, unmatched


def risk_set_balance(
    matches: Sequence[RiskSetMatch],
    papers: Sequence[MechanismPaper],
    *,
    max_abs_smd: float = 0.10,
) -> dict:
    by_id = {p.paper_id: p for p in papers}
    if not matches:
        return {
            "n_matches": 0,
            "balance_assessable": False,
            "balance_pass": None,
            "max_abs_smd_threshold": max_abs_smd,
            "covariates": {},
        }

    case_rates = [m.case_sleep_rate for m in matches]
    control_rates = [m.control_rate_to_event for m in matches]

    diagnostics = {}
    rate_smd = standardized_mean_difference(case_rates, control_rates)
    diagnostics["sleep_rate_to_case_event"] = {
        "abs_smd": rate_smd,
        "balanced": None if rate_smd is None else rate_smd < max_abs_smd,
        "n_pairs": len(matches),
    }

    for field in ("reference_count", "author_count"):
        case_values = []
        control_values = []
        for match in matches:
            case = by_id[match.case_id]
            control = by_id[match.control_id]
            left = getattr(case, field)
            right = getattr(control, field)
            if left is None or right is None:
                continue
            case_values.append(float(left))
            control_values.append(float(right))
        smd = (
            standardized_mean_difference(case_values, control_values)
            if len(case_values) >= 2
            else None
        )
        diagnostics[field] = {
            "abs_smd": smd,
            "balanced": None if smd is None else smd < max_abs_smd,
            "n_pairs": len(case_values),
        }

    assessed = [
        x["abs_smd"]
        for x in diagnostics.values()
        if x["abs_smd"] is not None
    ]
    return {
        "n_matches": len(matches),
        "balance_assessable": bool(assessed),
        "balance_pass": (
            all(x < max_abs_smd for x in assessed)
            if assessed
            else None
        ),
        "max_abs_smd_threshold": max_abs_smd,
        "max_observed_abs_smd": max(assessed) if assessed else None,
        "covariates": diagnostics,
        "note": (
            "Risk-set balance is a diagnostic on observed pre-event "
            "covariates, not proof of causal exchangeability."
        ),
    }


def build_awakening_risk_set_contrast(
    papers: Sequence[MechanismPaper],
    *,
    controls_per_case: int = 1,
    with_replacement_across_risk_sets: bool = True,
    max_sleep_rate: float = 2.0,
    wake_years: int = 4,
    min_wake_rate: float = 5.0,
    max_abs_smd: float = 0.10,
) -> dict:
    cases = [p for p in papers if p.state == "SLEEPING_BEAUTY"]
    matches, unmatched = match_awakening_risk_sets(
        papers,
        controls_per_case=controls_per_case,
        with_replacement=with_replacement_across_risk_sets,
        max_sleep_rate=max_sleep_rate,
        wake_years=wake_years,
        min_wake_rate=min_wake_rate,
    )
    matched_cases = {m.case_id for m in matches}
    return {
        "question": (
            "At the index paper's awakening time, what distinguished it "
            "from same-field/year papers that were still dormant and at risk?"
        ),
        "design": "event-time risk-set matching",
        "matches": [m.as_dict() for m in matches],
        "unmatched_cases": unmatched,
        "match_rate": len(matched_cases) / len(cases) if cases else 0.0,
        "balance": risk_set_balance(
            matches,
            papers,
            max_abs_smd=max_abs_smd,
        ),
        "rules": {
            "same_field": True,
            "same_publication_year": True,
            "control_must_be_dormant_at_case_event": True,
            "control_may_awaken_later": True,
            "control_reuse_across_case_risk_sets": (
                with_replacement_across_risk_sets
            ),
            "max_sleep_rate_to_case_event": max_sleep_rate,
            "wake_years": wake_years,
            "min_wake_rate": min_wake_rate,
            "post_event_control_outcomes_used_for_matching": False,
        },
    }
