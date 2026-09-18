#!/usr/bin/env python3
"""Positive-dependence sensitivity for two AI adjudicators in ARIS4C005.

The primary latent model assumes conditional independence of AI_A and AI_B given
true article state. This module relaxes that assumption with two transparent
parameters:

lambda_se  : shared-error dependence among positive measurements when Z=1
lambda_fpr : shared-error dependence among false-positive measurements when Z=0

For two Bernoulli measurements with marginal positive probabilities pA and pB:

    P(A=1,B=1) =
        pA*pB + lambda * (min(pA,pB) - pA*pB)

lambda=0 -> conditional independence.
lambda=1 -> maximal positive dependence compatible with the marginals.

This parameterization preserves each adjudicator's marginal sensitivity and
specificity while varying how strongly they make the same errors.

It is a sensitivity analysis, not an empirically identified correlation model.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from latent_prevalence import (
    beta_log_prior,
    calibration_beta,
    local_widths,
    make_grid,
    parse_binary,
    quantile,
    sample_discrete,
    summarize_draws,
)


def joint_positive_cells(
    p_a: float,
    p_b: float,
    dependence: float,
) -> dict[tuple[int, int], float]:
    """Joint Bernoulli table preserving marginals under positive dependence."""
    if not (0.0 <= p_a <= 1.0 and 0.0 <= p_b <= 1.0):
        raise ValueError("Marginal probabilities must be in [0,1]")
    if not (0.0 <= dependence <= 1.0):
        raise ValueError("dependence must be in [0,1]")

    q11_ind = p_a * p_b
    q11_max = min(p_a, p_b)
    q11 = q11_ind + dependence * (q11_max - q11_ind)
    q10 = p_a - q11
    q01 = p_b - q11
    q00 = 1.0 - q11 - q10 - q01

    cells = {
        (1, 1): q11,
        (1, 0): q10,
        (0, 1): q01,
        (0, 0): q00,
    }
    # Numerical guard.
    for key, value in cells.items():
        if value < -1e-12 or value > 1.0 + 1e-12:
            raise ValueError(f"Invalid joint probability {key}={value}")
        cells[key] = min(1.0, max(0.0, value))
    if abs(sum(cells.values()) - 1.0) > 1e-9:
        raise ValueError("Joint probabilities do not sum to one")
    return cells


def conditional_pattern_prob(
    a: int | None,
    b: int | None,
    *,
    z: int,
    se_a: float,
    sp_a: float,
    se_b: float,
    sp_b: float,
    lambda_se: float,
    lambda_fpr: float,
) -> float:
    """P(A=a,B=b | Z=z), marginalizing missing measurements."""
    if z not in (0, 1):
        raise ValueError("z must be 0 or 1")

    if z == 1:
        p_a = se_a
        p_b = se_b
        dep = lambda_se
    else:
        p_a = 1.0 - sp_a
        p_b = 1.0 - sp_b
        dep = lambda_fpr

    if a is None and b is None:
        return 1.0
    if a is None:
        return p_b if b == 1 else 1.0 - p_b
    if b is None:
        return p_a if a == 1 else 1.0 - p_a

    return joint_positive_cells(p_a, p_b, dep)[(a, b)]


def pattern_prob_correlated(
    prevalence: float,
    a: int | None,
    b: int | None,
    *,
    se_a: float,
    sp_a: float,
    se_b: float,
    sp_b: float,
    lambda_se: float,
    lambda_fpr: float,
) -> float:
    positive = conditional_pattern_prob(
        a,
        b,
        z=1,
        se_a=se_a,
        sp_a=sp_a,
        se_b=se_b,
        sp_b=sp_b,
        lambda_se=lambda_se,
        lambda_fpr=lambda_fpr,
    )
    negative = conditional_pattern_prob(
        a,
        b,
        z=0,
        se_a=se_a,
        sp_a=sp_a,
        se_b=se_b,
        sp_b=sp_b,
        lambda_se=lambda_se,
        lambda_fpr=lambda_fpr,
    )
    return prevalence * positive + (1.0 - prevalence) * negative


def posterior_mass_correlated(
    pattern_counts: Counter[tuple[int | None, int | None]],
    *,
    se_a: float,
    sp_a: float,
    se_b: float,
    sp_b: float,
    lambda_se: float,
    lambda_fpr: float,
    prior_a: float,
    prior_b: float,
    grid: list[float],
    widths: list[float],
) -> list[float]:
    logs: list[float] = []
    for p, width in zip(grid, widths):
        lp = beta_log_prior(p, prior_a, prior_b) + math.log(width)
        for (a, b), n in pattern_counts.items():
            if n <= 0 or (a is None and b is None):
                continue
            q = pattern_prob_correlated(
                p,
                a,
                b,
                se_a=se_a,
                sp_a=sp_a,
                se_b=se_b,
                sp_b=sp_b,
                lambda_se=lambda_se,
                lambda_fpr=lambda_fpr,
            )
            if q <= 0:
                lp = float("-inf")
                break
            lp += n * math.log(q)
        logs.append(lp)

    m = max(logs)
    weights = [math.exp(x - m) if math.isfinite(x) else 0.0 for x in logs]
    total = sum(weights)
    if total <= 0:
        raise ValueError("Posterior grid has zero mass")
    return [w / total for w in weights]


def fit_one_scenario(
    rows: list[dict[str, str]],
    calibration: dict[str, Any],
    *,
    lambda_se: float,
    lambda_fpr: float,
    draws: int,
    seed: int,
    grid_points: int,
    p_max: float,
    prior_a: float,
    prior_b: float,
    calibration_pseudo: float = 0.5,
) -> dict[str, Any]:
    by_stratum: dict[str, Counter[tuple[int | None, int | None]]] = defaultdict(Counter)
    stratum_N: dict[str, int] = {}

    for row in rows:
        h = (row.get("audit_stratum") or "").strip()
        if not h:
            raise ValueError("Missing audit_stratum")
        N = int(row["stratum_population_N"])
        if h in stratum_N and stratum_N[h] != N:
            raise ValueError(f"Inconsistent stratum population for {h}")
        stratum_N[h] = N
        a = parse_binary(row.get("a_binary_severe"))
        b = parse_binary(row.get("b_binary_severe"))
        by_stratum[h][(a, b)] += 1

    total_N = sum(stratum_N.values())
    population_weights = {h: N / total_N for h, N in stratum_N.items()}
    grid = make_grid(grid_points, p_max)
    widths = local_widths(grid)
    rng = random.Random(seed)

    global_draws: list[float] = []
    stratum_draws: dict[str, list[float]] = {h: [] for h in stratum_N}

    for _ in range(draws):
        se_a = calibration_beta(calibration, "AI_A", "se", rng, calibration_pseudo)
        sp_a = calibration_beta(calibration, "AI_A", "sp", rng, calibration_pseudo)
        se_b = calibration_beta(calibration, "AI_B", "se", rng, calibration_pseudo)
        sp_b = calibration_beta(calibration, "AI_B", "sp", rng, calibration_pseudo)

        global_p = 0.0
        for h in sorted(stratum_N):
            mass = posterior_mass_correlated(
                by_stratum[h],
                se_a=se_a,
                sp_a=sp_a,
                se_b=se_b,
                sp_b=sp_b,
                lambda_se=lambda_se,
                lambda_fpr=lambda_fpr,
                prior_a=prior_a,
                prior_b=prior_b,
                grid=grid,
                widths=widths,
            )
            p_h = sample_discrete(rng, grid, mass)
            stratum_draws[h].append(p_h)
            global_p += population_weights[h] * p_h
        global_draws.append(global_p)

    return {
        "lambda_se": lambda_se,
        "lambda_fpr": lambda_fpr,
        "global_prevalence": summarize_draws(global_draws),
        "stratum_prevalence": {
            h: summarize_draws(draws_h) for h, draws_h in stratum_draws.items()
        },
    }


def run_sensitivity(
    rows: list[dict[str, str]],
    calibration: dict[str, Any],
    *,
    dependence_grid: list[float],
    draws: int = 500,
    seed: int = 20260918,
    grid_points: int = 600,
    p_max: float = 0.10,
    prior_a: float = 0.5,
    prior_b: float = 0.5,
) -> dict[str, Any]:
    scenarios: list[dict[str, Any]] = []
    counter = 0
    for lambda_se in dependence_grid:
        for lambda_fpr in dependence_grid:
            counter += 1
            scenarios.append(
                fit_one_scenario(
                    rows,
                    calibration,
                    lambda_se=lambda_se,
                    lambda_fpr=lambda_fpr,
                    draws=draws,
                    seed=seed + counter * 1009,
                    grid_points=grid_points,
                    p_max=p_max,
                    prior_a=prior_a,
                    prior_b=prior_b,
                )
            )

    medians = [s["global_prevalence"]["median"] for s in scenarios]
    lower = [s["global_prevalence"]["q025"] for s in scenarios]
    upper = [s["global_prevalence"]["q975"] for s in scenarios]
    return {
        "classification": "CORRELATED_AI_ERROR_SENSITIVITY_NOT_IDENTIFIED_FROM_LABELS_ALONE",
        "parameterization": {
            "lambda_se": (
                "0=conditional independence of positive measurements under Z=1; "
                "1=maximal positive dependence preserving marginal sensitivities"
            ),
            "lambda_fpr": (
                "0=conditional independence of false positives under Z=0; "
                "1=maximal positive dependence preserving marginal false-positive rates"
            ),
            "grid": dependence_grid,
        },
        "scenarios": scenarios,
        "global_envelope": {
            "median_min": min(medians),
            "median_max": max(medians),
            "q025_min": min(lower),
            "q975_max": max(upper),
        },
        "warnings": [
            "Dependence parameters are sensitivity settings, not estimated correlations.",
            "Shared model training/data/reasoning can make AI errors positively dependent.",
            "lambda=0 reproduces the primary conditional-independence structure.",
            "If conclusions change materially across plausible dependence settings, the manuscript must report the sensitivity envelope rather than a single prevalence estimate.",
        ],
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("latent_input_csv", type=Path)
    p.add_argument("calibration_json", type=Path)
    p.add_argument("output_json", type=Path)
    p.add_argument("--dependence", action="append", type=float, default=[])
    p.add_argument("--draws", type=int, default=500)
    p.add_argument("--seed", type=int, default=20260918)
    p.add_argument("--grid-points", type=int, default=600)
    p.add_argument("--p-max", type=float, default=0.10)
    args = p.parse_args()

    dependence_grid = args.dependence or [0.0, 0.25, 0.50, 0.75, 1.0]
    rows = read_csv(args.latent_input_csv)
    calibration = json.loads(args.calibration_json.read_text(encoding="utf-8"))
    result = run_sensitivity(
        rows,
        calibration,
        dependence_grid=dependence_grid,
        draws=args.draws,
        seed=args.seed,
        grid_points=args.grid_points,
        p_max=args.p_max,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
