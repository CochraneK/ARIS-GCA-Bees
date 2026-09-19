#!/usr/bin/env python3
"""Effect-size and fixed-margin inference helpers for ARIS4C013.

These helpers are intentionally small and deterministic so the same rules can
be used in discovery and holdout without outcome-dependent reinterpretation.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import NormalDist
from typing import Mapping, Sequence

import numpy as np

SESOI_LOWER = 0.99
SESOI_UPPER = 1.01
TEMPORAL_STABILITY_MIN_FRACTION = 7 / 9


@dataclass(frozen=True)
class OffsetInference:
    observed: int
    expected: float
    variance_null: float
    oe: float
    z_null: float
    ci90_lower: float
    ci90_upper: float
    ci95_lower: float
    ci95_upper: float
    practical_class: str


def fixed_margin_mean_variance(
    birth_counts: Sequence[int] | np.ndarray,
    death_counts: Sequence[int] | np.ndarray,
    offset: int = 0,
) -> tuple[float, float]:
    """Exact mean and variance under random pairing with fixed marginals.

    Birth labels are fixed to positions and the multiset of death labels is
    randomly permuted without replacement. The returned variance is for the
    count whose death phase equals birth phase + offset modulo the phase count.
    """
    b = np.asarray(birth_counts, dtype=np.int64)
    d = np.asarray(death_counts, dtype=np.int64)
    if b.ndim != 1 or d.ndim != 1 or len(b) != len(d):
        raise ValueError("birth and death marginals must be 1-D and same length")
    if np.any(b < 0) or np.any(d < 0):
        raise ValueError("marginal counts must be nonnegative")
    n_b = int(b.sum())
    n_d = int(d.sum())
    if n_b != n_d:
        raise ValueError("birth and death marginals must have equal totals")
    if n_b == 0:
        return 0.0, 0.0

    target_d = np.roll(d, -int(offset))

    # Use Python integers for fourth-order count products. Exact-year strata
    # are normally far below int64 limits, but this keeps the implementation
    # safe even if a future source has unusually concentrated date counts.
    b_py = [int(x) for x in b]
    d_py = [int(x) for x in target_d]
    products = [bi * di for bi, di in zip(b_py, d_py)]
    s = sum(products)
    mean = s / n_b
    if n_b == 1:
        variance = mean * (1.0 - mean)
        return float(mean), float(max(variance, 0.0))

    cross_distinct_birth_categories = (
        s * s - sum(x * x for x in products)
    )
    same_birth_category = sum(
        bi * (bi - 1) * di * (di - 1)
        for bi, di in zip(b_py, d_py)
    )
    factorial_second = (
        cross_distinct_birth_categories + same_birth_category
    ) / (n_b * (n_b - 1))
    variance = mean + factorial_second - mean * mean
    return float(mean), float(max(variance, 0.0))


def pooled_fixed_margin_mean_variance(
    strata: Mapping[object, Sequence[object]],
    offset: int = 0,
) -> tuple[float, float]:
    """Sum exact fixed-margin means/variances across independent strata."""
    mean_total = 0.0
    var_total = 0.0
    for entry in strata.values():
        births, deaths, n = entry
        if int(n) == 0:
            continue
        mean, var = fixed_margin_mean_variance(births, deaths, offset=offset)
        mean_total += mean
        var_total += var
    return mean_total, var_total


def practical_classification(
    oe: float,
    ci90_lower: float,
    ci90_upper: float,
    ci95_lower: float,
    ci95_upper: float,
) -> str:
    """Classify an effect using the preregistered +/-1% practical margin."""
    if all(math.isfinite(x) for x in (ci90_lower, ci90_upper)):
        if ci90_lower >= SESOI_LOWER and ci90_upper <= SESOI_UPPER:
            return "practically-null-equivalent"

    statistically_nonnull = ci95_upper < 1.0 or ci95_lower > 1.0
    beyond_sesoi = oe < SESOI_LOWER or oe > SESOI_UPPER

    if statistically_nonnull and beyond_sesoi:
        return "substantive-positive" if oe > 1.0 else "substantive-negative"
    if statistically_nonnull and not beyond_sesoi:
        return "statistically-detectable-practically-trivial"
    return "inconclusive"


def infer_offset(
    observed: int,
    strata: Mapping[object, Sequence[object]],
    offset: int = 0,
) -> OffsetInference:
    """Compute O/E plus a fixed-margin delta-method interval.

    The null mean/variance are exact conditional on the observed marginals and
    random pairing within strata. The O/E interval uses a large-sample delta
    approximation on log(O/E); it is explicitly not called an exact confidence
    interval for a causal parameter.
    """
    expected, var_null = pooled_fixed_margin_mean_variance(
        strata, offset=offset
    )
    if expected <= 0:
        return OffsetInference(
            observed=int(observed),
            expected=float(expected),
            variance_null=float(var_null),
            oe=math.nan,
            z_null=math.nan,
            ci90_lower=math.nan,
            ci90_upper=math.nan,
            ci95_lower=math.nan,
            ci95_upper=math.nan,
            practical_class="inconclusive",
        )

    oe = observed / expected
    sd_null = math.sqrt(var_null)
    z_null = (observed - expected) / sd_null if sd_null > 0 else math.nan

    if observed <= 0 or var_null <= 0:
        ci90 = (math.nan, math.nan)
        ci95 = (math.nan, math.nan)
    else:
        se_log = sd_null / observed
        log_oe = math.log(oe)
        z90 = NormalDist().inv_cdf(0.95)
        z95 = NormalDist().inv_cdf(0.975)
        ci90 = (
            math.exp(log_oe - z90 * se_log),
            math.exp(log_oe + z90 * se_log),
        )
        ci95 = (
            math.exp(log_oe - z95 * se_log),
            math.exp(log_oe + z95 * se_log),
        )

    cls = practical_classification(
        oe, ci90[0], ci90[1], ci95[0], ci95[1]
    )
    return OffsetInference(
        observed=int(observed),
        expected=float(expected),
        variance_null=float(var_null),
        oe=float(oe),
        z_null=float(z_null),
        ci90_lower=float(ci90[0]),
        ci90_upper=float(ci90[1]),
        ci95_lower=float(ci95[0]),
        ci95_upper=float(ci95[1]),
        practical_class=cls,
    )


def attenuation_ratio(discovery_oe: float, holdout_oe: float) -> float:
    """Log-effect retention ratio; negative means sign reversal."""
    d = math.log(discovery_oe)
    h = math.log(holdout_oe)
    if abs(d) < 1e-12:
        return math.nan
    return h / d


def attenuation_class(discovery_oe: float, holdout_oe: float) -> str:
    ratio = attenuation_ratio(discovery_oe, holdout_oe)
    if not math.isfinite(ratio):
        return "undefined"
    if ratio < 0:
        return "sign-reversal"
    if ratio < 0.5:
        return "attenuated"
    if ratio <= 1.5:
        return "magnitude-consistent"
    return "amplified"


def temporal_direction_fraction(
    year_oes: Sequence[float], pooled_oe: float
) -> float:
    vals = [x for x in year_oes if math.isfinite(x) and x > 0]
    if not vals or pooled_oe == 1.0:
        return math.nan
    sign = 1 if pooled_oe > 1.0 else -1
    consistent = sum(1 for x in vals if (x - 1.0) * sign > 0)
    return consistent / len(vals)


def confirmatory_holdout_classification(
    discovery_oe: float,
    holdout: OffsetInference,
    holdout_year_oes: Sequence[float],
) -> dict[str, object]:
    """Apply the locked H2 holdout interpretation rule."""
    same_direction = (
        (discovery_oe - 1.0) * (holdout.oe - 1.0) > 0
    )
    stable_fraction = temporal_direction_fraction(
        holdout_year_oes, holdout.oe
    )
    stable = (
        math.isfinite(stable_fraction)
        and stable_fraction >= TEMPORAL_STABILITY_MIN_FRACTION
    )
    substantive = holdout.practical_class in {
        "substantive-positive",
        "substantive-negative",
    }
    replicated_candidate = bool(same_direction and substantive and stable)

    return {
        "same_direction_as_discovery": bool(same_direction),
        "holdout_practical_class": holdout.practical_class,
        "temporal_direction_fraction": float(stable_fraction),
        "temporal_stability_threshold": TEMPORAL_STABILITY_MIN_FRACTION,
        "temporally_stable": bool(stable),
        "attenuation_ratio_log_scale": float(
            attenuation_ratio(discovery_oe, holdout.oe)
        ),
        "attenuation_class": attenuation_class(
            discovery_oe, holdout.oe
        ),
        "replicated_candidate_birthday_effect": replicated_candidate,
    }
