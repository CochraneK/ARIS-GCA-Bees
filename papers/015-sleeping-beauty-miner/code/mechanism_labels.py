"""Mechanism-track labels for ARIS4C015.

This module separates three concepts that must never be conflated:

1. Relative benchmark outcomes
   - e.g. top-20% B inside a tiny historical sample.
   - useful for prospective ranking benchmarks.
   - NOT sufficient to call a paper a Sleeping Beauty.

2. Retrospective Sleeping Beauty gates
   - use complete citation histories and source-calibrated thresholds.
   - intended to construct a case-enriched mechanism dataset.

3. Mechanism trajectory states
   - Sleeping Beauty, Forgotten, Immediate Hit, Fading, Ambiguous.
   - defined using field/cohort-normalized early and late attention.

The defaults are literature-informed but remain configurable. Dataset-specific
thresholds are always returned in the output so downstream analyses cannot
silently treat them as universal constants.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from sb_metrics import beauty_coefficient, awakening_time


@dataclass(frozen=True)
class VanRaanGate:
    passed: bool
    mode: str
    sleep_years: int
    wake_years: int
    sleep_citations: int
    wake_citations: int
    sleep_rate: float
    wake_rate: float
    max_sleep_rate: float
    min_wake_rate: float
    min_total_citations: int | None
    total_citations: int
    candidate_windows: int = 1

    def as_dict(self) -> dict:
        return {
            "passed": self.passed,
            "mode": self.mode,
            "sleep_years": self.sleep_years,
            "wake_years": self.wake_years,
            "sleep_citations": self.sleep_citations,
            "wake_citations": self.wake_citations,
            "sleep_rate": self.sleep_rate,
            "wake_rate": self.wake_rate,
            "max_sleep_rate": self.max_sleep_rate,
            "min_wake_rate": self.min_wake_rate,
            "min_total_citations": self.min_total_citations,
            "total_citations": self.total_citations,
            "candidate_windows": self.candidate_windows,
        }


@dataclass(frozen=True)
class SourceBCalibration:
    source: str
    high_b_threshold: float
    extreme_b_threshold: float | None = None
    note: str | None = None

    def as_dict(self) -> dict:
        return {
            "source": self.source,
            "high_b_threshold": self.high_b_threshold,
            "extreme_b_threshold": self.extreme_b_threshold,
            "note": self.note,
        }


SCISCINET_V1_CALIBRATION = SourceBCalibration(
    source="SciSciNet v1",
    high_b_threshold=33.0,
    extreme_b_threshold=307.55,
    note=(
        "SciSciNet reports B>33 as approximately the top 2% of Sleeping "
        "Beauty coefficients in its journal-article corpus, while B>307.55 "
        "corresponds to its top-10,000 high-B group. These are source-specific "
        "reference thresholds, not universal scientific constants."
    ),
)


@dataclass(frozen=True)
class RobustSBResult:
    state: str
    robust_sb: bool
    beauty_coefficient: float
    awakening_age: int
    van_raan: VanRaanGate
    b_high_pass: bool
    b_extreme_pass: bool | None
    later_recognition_pass: bool
    component_passes: int
    required_component_passes: int
    calibration: dict
    warnings: tuple[str, ...]

    def as_dict(self) -> dict:
        return {
            "state": self.state,
            "robust_sb": self.robust_sb,
            "beauty_coefficient": self.beauty_coefficient,
            "awakening_age": self.awakening_age,
            "van_raan": self.van_raan.as_dict(),
            "b_high_pass": self.b_high_pass,
            "b_extreme_pass": self.b_extreme_pass,
            "later_recognition_pass": self.later_recognition_pass,
            "component_passes": self.component_passes,
            "required_component_passes": self.required_component_passes,
            "calibration": self.calibration,
            "warnings": list(self.warnings),
        }


def _counts(values: Sequence[int | float]) -> tuple[int, ...]:
    result = tuple(int(x) for x in values)
    if not result:
        raise ValueError("citation history must be non-empty")
    if any(x < 0 for x in result):
        raise ValueError("citation counts must be non-negative")
    return result


def van_raan_gate(
    counts: Sequence[int | float],
    *,
    sleep_mode: str = "VARIABLE_SLEEP",
    sleep_years: int = 10,
    min_sleep_years: int = 5,
    max_sleep_years: int | None = None,
    wake_years: int = 4,
    max_sleep_rate: float = 1.0,
    min_wake_rate: float = 5.0,
    min_total_citations: int | None = None,
) -> VanRaanGate:
    """Literature-style sleep/depth/awakening gate.

    Defaults represent a conservative deep-sleep formulation:
    - first 10 years average <= 1 citation/year;
    - next 4 years average > 5 citations/year.

    Later field-specific studies sometimes add a total-citation floor (for
    example 100 citations). That floor is optional here and always explicit.
    """
    c = _counts(counts)
    if sleep_years < 1 or wake_years < 1:
        raise ValueError("sleep_years and wake_years must be >= 1")
    if len(c) < sleep_years + wake_years:
        raise ValueError(
            "citation history is too short for requested sleep/wake windows"
        )

    sleep = c[:sleep_years]
    wake = c[sleep_years:sleep_years + wake_years]
    sleep_total = sum(sleep)
    wake_total = sum(wake)
    sleep_rate = sleep_total / sleep_years
    wake_rate = wake_total / wake_years
    total = sum(c)

    passed = (
        sleep_rate <= float(max_sleep_rate)
        and wake_rate > float(min_wake_rate)
        and (
            min_total_citations is None
            or total >= int(min_total_citations)
        )
    )

    return VanRaanGate(
        passed=passed,
        mode="FIXED_SLEEP",
        sleep_years=sleep_years,
        wake_years=wake_years,
        sleep_citations=sleep_total,
        wake_citations=wake_total,
        sleep_rate=sleep_rate,
        wake_rate=wake_rate,
        max_sleep_rate=float(max_sleep_rate),
        min_wake_rate=float(min_wake_rate),
        min_total_citations=min_total_citations,
        total_citations=total,
    )





def variable_van_raan_gate(
    counts: Sequence[int | float],
    *,
    min_sleep_years: int = 5,
    max_sleep_years: int | None = None,
    wake_years: int = 4,
    max_sleep_rate: float = 1.0,
    min_wake_rate: float = 5.0,
    min_total_citations: int | None = None,
) -> VanRaanGate:
    """Search over possible sleep lengths instead of fixing s in advance.

    van Raan's framework treats sleep length s as a tunable dimension. This
    function evaluates every admissible s and, when multiple windows pass,
    reports the longest qualifying sleep. That makes long-sleep classical SBs
    identifiable without forcing them into a 5- or 10-year window.

    A fixed-s gate remains available for direct replication/sensitivity work.
    """
    c = _counts(counts)
    if min_sleep_years < 1 or wake_years < 1:
        raise ValueError("sleep/wake years must be >= 1")

    latest = len(c) - wake_years
    if latest < min_sleep_years:
        raise ValueError(
            "citation history is too short for variable sleep search"
        )
    if max_sleep_years is not None:
        if max_sleep_years < min_sleep_years:
            raise ValueError(
                "max_sleep_years cannot be below min_sleep_years"
            )
        latest = min(latest, int(max_sleep_years))

    evaluated = [
        van_raan_gate(
            c,
            sleep_years=s,
            wake_years=wake_years,
            max_sleep_rate=max_sleep_rate,
            min_wake_rate=min_wake_rate,
            min_total_citations=min_total_citations,
        )
        for s in range(min_sleep_years, latest + 1)
    ]
    passing = [gate for gate in evaluated if gate.passed]

    if passing:
        chosen = max(passing, key=lambda gate: gate.sleep_years)
        return VanRaanGate(
            passed=True,
            mode="VARIABLE_SLEEP",
            sleep_years=chosen.sleep_years,
            wake_years=chosen.wake_years,
            sleep_citations=chosen.sleep_citations,
            wake_citations=chosen.wake_citations,
            sleep_rate=chosen.sleep_rate,
            wake_rate=chosen.wake_rate,
            max_sleep_rate=chosen.max_sleep_rate,
            min_wake_rate=chosen.min_wake_rate,
            min_total_citations=chosen.min_total_citations,
            total_citations=chosen.total_citations,
            candidate_windows=len(passing),
        )

    # For a failed search, expose the strongest wake window for diagnostics
    # without silently turning it into a pass.
    chosen = max(evaluated, key=lambda gate: gate.wake_rate)
    return VanRaanGate(
        passed=False,
        mode="VARIABLE_SLEEP",
        sleep_years=chosen.sleep_years,
        wake_years=chosen.wake_years,
        sleep_citations=chosen.sleep_citations,
        wake_citations=chosen.wake_citations,
        sleep_rate=chosen.sleep_rate,
        wake_rate=chosen.wake_rate,
        max_sleep_rate=chosen.max_sleep_rate,
        min_wake_rate=chosen.min_wake_rate,
        min_total_citations=chosen.min_total_citations,
        total_citations=chosen.total_citations,
        candidate_windows=0,
    )


def robust_sleeping_beauty_gate(
    counts: Sequence[int | float],
    *,
    b_calibration: SourceBCalibration = SCISCINET_V1_CALIBRATION,
    sleep_years: int = 10,
    wake_years: int = 4,
    max_sleep_rate: float = 1.0,
    min_wake_rate: float = 5.0,
    min_total_citations: int = 50,
    required_component_passes: int = 3,
) -> RobustSBResult:
    """Require converging retrospective evidence before calling a robust SB.

    Components:
    1. van-Raan-style sleep/depth/wake pattern;
    2. high source-calibrated Beauty Coefficient;
    3. later-recognition floor via total citations.

    With the default required_component_passes=3, all three must pass.

    This is intentionally stricter than the prospective benchmark's relative
    outcomes. It is designed for mechanism-case enrichment, not for ranking.
    """
    if required_component_passes < 1 or required_component_passes > 3:
        raise ValueError("required_component_passes must be 1..3")

    c = _counts(counts)
    mode = sleep_mode.upper()
    if mode == "VARIABLE_SLEEP":
        vr = variable_van_raan_gate(
            c,
            min_sleep_years=min_sleep_years,
            max_sleep_years=max_sleep_years,
            wake_years=wake_years,
            max_sleep_rate=max_sleep_rate,
            min_wake_rate=min_wake_rate,
            min_total_citations=None,
        )
    elif mode == "FIXED_SLEEP":
        vr = van_raan_gate(
            c,
            sleep_years=sleep_years,
            wake_years=wake_years,
            max_sleep_rate=max_sleep_rate,
            min_wake_rate=min_wake_rate,
            min_total_citations=None,
        )
    else:
        raise ValueError(
            "sleep_mode must be VARIABLE_SLEEP or FIXED_SLEEP"
        )
    b = float(beauty_coefficient(c))
    ta = int(awakening_time(c))
    b_high = b > float(b_calibration.high_b_threshold)
    b_extreme = (
        b > float(b_calibration.extreme_b_threshold)
        if b_calibration.extreme_b_threshold is not None
        else None
    )
    recognition = sum(c) >= int(min_total_citations)

    passes = int(vr.passed) + int(b_high) + int(recognition)
    robust = passes >= required_component_passes

    warnings = []
    if b_calibration.source.lower().startswith("sciscinet"):
        warnings.append(
            "B threshold is calibrated to SciSciNet and should be "
            "re-estimated or sensitivity-tested in another bibliographic source."
        )
    if mode == "FIXED_SLEEP" and ta < sleep_years:
        warnings.append(
            "Geometric awakening occurs before the configured fixed sleep "
            "window; inspect the trajectory manually."
        )
    if mode == "VARIABLE_SLEEP" and abs(ta - vr.sleep_years) > wake_years:
        warnings.append(
            "Geometric awakening time and van-Raan qualifying sleep length "
            "differ materially; retain both as definition sensitivity."
        )

    return RobustSBResult(
        state="ROBUST_SLEEPING_BEAUTY" if robust else "NOT_ROBUST_SB",
        robust_sb=robust,
        beauty_coefficient=b,
        awakening_age=ta,
        van_raan=vr,
        b_high_pass=b_high,
        b_extreme_pass=b_extreme,
        later_recognition_pass=recognition,
        component_passes=passes,
        required_component_passes=required_component_passes,
        calibration=b_calibration.as_dict(),
        warnings=tuple(warnings),
    )


@dataclass(frozen=True)
class MechanismState:
    state: str
    early_percentile: float
    late_percentile: float
    early_low_threshold: float
    early_high_threshold: float
    late_low_threshold: float
    late_high_threshold: float
    robust_sb_required: bool
    robust_sb_passed: bool | None

    def as_dict(self) -> dict:
        return {
            "state": self.state,
            "early_percentile": self.early_percentile,
            "late_percentile": self.late_percentile,
            "early_low_threshold": self.early_low_threshold,
            "early_high_threshold": self.early_high_threshold,
            "late_low_threshold": self.late_low_threshold,
            "late_high_threshold": self.late_high_threshold,
            "robust_sb_required": self.robust_sb_required,
            "robust_sb_passed": self.robust_sb_passed,
        }


def classify_mechanism_state(
    *,
    early_percentile: float,
    late_percentile: float,
    robust_sb: bool | None = None,
    early_count: int | None = None,
    late_count: int | None = None,
    zero_counts_are_low: bool = True,
    early_low_threshold: float = 0.25,
    early_high_threshold: float = 0.75,
    late_low_threshold: float = 0.25,
    late_high_threshold: float = 0.75,
    require_robust_sb_for_sleeping_beauty: bool = True,
) -> MechanismState:
    """Classify four canonical citation-life states using normalized attention.

    States:
    - SLEEPING_BEAUTY: early low, late high, and robust SB gate if required.
    - FORGOTTEN: early low, late low.
    - IMMEDIATE_HIT: early high, late high.
    - FADING: early high, late low.
    - AMBIGUOUS: middle-zone trajectories.

    Percentiles must be field/cohort normalized upstream.
    """
    for name, value in (
        ("early_percentile", early_percentile),
        ("late_percentile", late_percentile),
    ):
        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"{name} must be in [0,1]")

    early_low = early_percentile <= early_low_threshold
    late_low = late_percentile <= late_low_threshold

    # Exact zero attention is substantively low even when a large tied zero
    # group receives an average percentile above the nominal low threshold.
    # This avoids classifying never-cited / no-late-citation papers as
    # middle-attention merely because of tie handling.
    if zero_counts_are_low:
        if early_count == 0:
            early_low = True
        if late_count == 0:
            late_low = True

    early_high = early_percentile >= early_high_threshold
    late_high = late_percentile >= late_high_threshold

    # A zero-count period cannot simultaneously be treated as high attention.
    if early_count == 0:
        early_high = False
    if late_count == 0:
        late_high = False

    if early_low and late_high:
        if require_robust_sb_for_sleeping_beauty:
            state = (
                "SLEEPING_BEAUTY"
                if robust_sb is True
                else "LOW_EARLY_HIGH_LATE_UNCONFIRMED"
            )
        else:
            state = "SLEEPING_BEAUTY"
    elif early_low and late_low:
        state = "FORGOTTEN"
    elif early_high and late_high:
        state = "IMMEDIATE_HIT"
    elif early_high and late_low:
        state = "FADING"
    else:
        state = "AMBIGUOUS"

    return MechanismState(
        state=state,
        early_percentile=float(early_percentile),
        late_percentile=float(late_percentile),
        early_low_threshold=float(early_low_threshold),
        early_high_threshold=float(early_high_threshold),
        late_low_threshold=float(late_low_threshold),
        late_high_threshold=float(late_high_threshold),
        robust_sb_required=require_robust_sb_for_sleeping_beauty,
        robust_sb_passed=robust_sb,
    )


def percentile_ranks(values: Mapping[str, float]) -> dict[str, float]:
    """Empirical percentile ranks with average ranks for ties."""
    if not values:
        return {}
    ordered = sorted(values.items(), key=lambda x: (x[1], x[0]))
    n = len(ordered)
    result: dict[str, float] = {}
    i = 0
    while i < n:
        j = i + 1
        while j < n and ordered[j][1] == ordered[i][1]:
            j += 1
        avg_rank = (i + j - 1) / 2
        p = avg_rank / (n - 1) if n > 1 else 1.0
        for k in range(i, j):
            result[ordered[k][0]] = p
        i = j
    return result


def early_late_percentiles(
    histories: Mapping[str, Sequence[int | float]],
    *,
    early_years: int = 5,
    late_years: int = 5,
) -> dict[str, tuple[float, float]]:
    """Compute within-stratum early and late citation percentiles.

    This helper is for mechanism grouping only. Histories should already be
    restricted to one field/cohort stratum.
    """
    if early_years < 1 or late_years < 1:
        raise ValueError("early_years and late_years must be >=1")

    early_totals: dict[str, float] = {}
    late_totals: dict[str, float] = {}

    for paper_id, counts in histories.items():
        c = _counts(counts)
        if len(c) < max(early_years, late_years):
            raise ValueError(f"history too short for {paper_id}")
        early_totals[paper_id] = float(sum(c[:early_years]))
        late_totals[paper_id] = float(sum(c[-late_years:]))

    early_p = percentile_ranks(early_totals)
    late_p = percentile_ranks(late_totals)
    return {
        paper_id: (early_p[paper_id], late_p[paper_id])
        for paper_id in histories
    }
