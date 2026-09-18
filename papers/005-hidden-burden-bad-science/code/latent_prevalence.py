#!/usr/bin/env python3
"""Bayesian measurement-error prevalence model for ARIS4C005.

This model uses two fallible binary AI adjudicators as noisy measurements of a
latent severe article state. It estimates prevalence separately by sampling
stratum, then aggregates using known target-universe stratum population sizes.

Measurement model (primary version):
- Z_i ~ Bernoulli(p_h) for stratum h;
- adjudicator A/B conditionally independent given Z_i;
- Se/Sp uncertainty sampled from Beta posteriors built from calibration anchors;
- unresolved/indeterminate AI states are treated as missing measurements, not
  negative labels.

The conditional-independence assumption is explicit and requires sensitivity
analysis because AI model errors can be correlated.
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


def beta_log_prior(p: float, a: float, b: float) -> float:
    if not (0.0 < p < 1.0):
        return float("-inf")
    return (a - 1.0) * math.log(p) + (b - 1.0) * math.log1p(-p)


def test_prob(y: int | None, z: int, se: float, sp: float) -> float:
    if y is None:
        return 1.0
    if z == 1:
        return se if y == 1 else (1.0 - se)
    return (1.0 - sp) if y == 1 else sp


def pattern_prob(
    p: float,
    a: int | None,
    b: int | None,
    se_a: float,
    sp_a: float,
    se_b: float,
    sp_b: float,
) -> float:
    pos = test_prob(a, 1, se_a, sp_a) * test_prob(b, 1, se_b, sp_b)
    neg = test_prob(a, 0, se_a, sp_a) * test_prob(b, 0, se_b, sp_b)
    return p * pos + (1.0 - p) * neg


def parse_binary(value: str | None) -> int | None:
    v = (value or "").strip()
    if v == "":
        return None
    if v == "1":
        return 1
    if v == "0":
        return 0
    raise ValueError(f"Invalid binary measurement: {value!r}")


def local_widths(grid: list[float]) -> list[float]:
    widths: list[float] = []
    for i, p in enumerate(grid):
        if i == 0:
            width = (grid[1] - p) / 2.0
        elif i == len(grid) - 1:
            width = (p - grid[i - 1]) / 2.0
        else:
            width = (grid[i + 1] - grid[i - 1]) / 2.0
        widths.append(width)
    return widths


def make_grid(points: int, p_max: float) -> list[float]:
    if points < 50:
        raise ValueError("grid points must be >=50")
    if not 0 < p_max < 1:
        raise ValueError("p_max must be between 0 and 1")
    # Quadratic spacing gives extra resolution near zero for rare outcomes.
    eps = 1e-9
    return [
        eps + (p_max - eps) * (i / (points - 1)) ** 2
        for i in range(points)
    ]


def posterior_mass(
    pattern_counts: Counter[tuple[int | None, int | None]],
    *,
    se_a: float,
    sp_a: float,
    se_b: float,
    sp_b: float,
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
            q = pattern_prob(p, a, b, se_a, sp_a, se_b, sp_b)
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


def sample_discrete(
    rng: random.Random,
    values: list[float],
    probs: list[float],
) -> float:
    u = rng.random()
    cumulative = 0.0
    for value, prob in zip(values, probs):
        cumulative += prob
        if u <= cumulative:
            return value
    return values[-1]


def quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("No posterior draws")
    xs = sorted(values)
    if q <= 0:
        return xs[0]
    if q >= 1:
        return xs[-1]
    pos = q * (len(xs) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return xs[lo]
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def summarize_draws(values: list[float]) -> dict[str, float]:
    return {
        "mean": sum(values) / len(values),
        "median": quantile(values, 0.5),
        "q025": quantile(values, 0.025),
        "q975": quantile(values, 0.975),
    }


def calibration_beta(
    calibration: dict[str, Any],
    adjudicator: str,
    metric: str,
    rng: random.Random,
    pseudo: float,
) -> float:
    c = calibration[adjudicator]
    if metric == "se":
        success = float(c["tp"])
        failure = float(c["fn"])
    elif metric == "sp":
        success = float(c["tn"])
        failure = float(c["fp"])
    else:
        raise ValueError(metric)
    return rng.betavariate(success + pseudo, failure + pseudo)


def fit(
    rows: list[dict[str, str]],
    calibration: dict[str, Any],
    *,
    draws: int = 2000,
    seed: int = 20260918,
    grid_points: int = 1200,
    p_max: float = 0.10,
    prior_a: float = 0.5,
    prior_b: float = 0.5,
    calibration_pseudo: float = 0.5,
) -> dict[str, Any]:
    by_stratum: dict[
        str, Counter[tuple[int | None, int | None]]
    ] = defaultdict(Counter)
    stratum_N: dict[str, int] = {}
    stratum_rows: Counter[str] = Counter()
    both_missing: Counter[str] = Counter()

    for row in rows:
        h = (row.get("audit_stratum") or "").strip()
        if not h:
            raise ValueError("Missing audit_stratum")
        N = int(row["stratum_population_N"])
        if h in stratum_N and stratum_N[h] != N:
            raise ValueError(f"Inconsistent stratum_population_N for {h}")
        stratum_N[h] = N

        a = parse_binary(row.get("a_binary_severe"))
        b = parse_binary(row.get("b_binary_severe"))
        by_stratum[h][(a, b)] += 1
        stratum_rows[h] += 1
        if a is None and b is None:
            both_missing[h] += 1

    if set(calibration) < {"AI_A", "AI_B"}:
        raise ValueError("Calibration JSON must contain AI_A and AI_B")

    total_N = sum(stratum_N.values())
    population_weights = {h: N / total_N for h, N in stratum_N.items()}

    grid = make_grid(grid_points, p_max)
    widths = local_widths(grid)
    rng = random.Random(seed)

    global_draws: list[float] = []
    stratum_draws: dict[str, list[float]] = {h: [] for h in stratum_N}
    measurement_draws = {
        "se_a": [],
        "sp_a": [],
        "se_b": [],
        "sp_b": [],
    }

    for _ in range(draws):
        se_a = calibration_beta(
            calibration, "AI_A", "se", rng, calibration_pseudo
        )
        sp_a = calibration_beta(
            calibration, "AI_A", "sp", rng, calibration_pseudo
        )
        se_b = calibration_beta(
            calibration, "AI_B", "se", rng, calibration_pseudo
        )
        sp_b = calibration_beta(
            calibration, "AI_B", "sp", rng, calibration_pseudo
        )
        measurement_draws["se_a"].append(se_a)
        measurement_draws["sp_a"].append(sp_a)
        measurement_draws["se_b"].append(se_b)
        measurement_draws["sp_b"].append(sp_b)

        global_p = 0.0
        for h in sorted(stratum_N):
            mass = posterior_mass(
                by_stratum[h],
                se_a=se_a,
                sp_a=sp_a,
                se_b=se_b,
                sp_b=sp_b,
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
        "classification": "CALIBRATED_DUAL_AI_LATENT_PREVALENCE_MODEL",
        "model": {
            "latent_state": "binary severe article-level scientific failure",
            "positive_measurement_state": "SEVERE_SUPPORTED",
            "conditional_independence_A_B_given_Z": True,
            "measurement_error": "Se/Sp sampled from anchor-calibration Beta posteriors",
            "prior": {"a": prior_a, "b": prior_b},
            "p_max": p_max,
            "grid_points": grid_points,
            "posterior_draws": draws,
            "calibration_beta_pseudocount": calibration_pseudo,
        },
        "sample": {
            "rows": len(rows),
            "stratum_sample_rows": dict(stratum_rows),
            "stratum_population_N": stratum_N,
            "population_weights": population_weights,
            "both_measurements_missing_by_stratum": dict(both_missing),
            "observed_patterns_by_stratum": {
                h: {
                    f"A{a if a is not None else '?'}B{b if b is not None else '?'}": n
                    for (a, b), n in counts.items()
                }
                for h, counts in by_stratum.items()
            },
        },
        "measurement_posterior": {
            k: summarize_draws(v) for k, v in measurement_draws.items()
        },
        "global_prevalence": summarize_draws(global_draws),
        "stratum_prevalence": {
            h: summarize_draws(v) for h, v in stratum_draws.items()
        },
        "warnings": [
            "AI adjudicators are fallible measurements, not truth labels.",
            "Conditional independence of AI_A and AI_B errors is an explicit primary-model assumption and may be optimistic.",
            "SERIOUS_UNRESOLVED/INDETERMINATE are missing measurements, not negatives.",
            "If missingness depends on latent severity, a separate missing-not-at-random sensitivity analysis is required.",
            "p_max truncates the numerical prevalence prior support and must be sensitivity-tested.",
            "The final manuscript must report prior, p_max, calibration anchors, and alternative dependence/missingness scenarios.",
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
    p.add_argument("--draws", type=int, default=2000)
    p.add_argument("--seed", type=int, default=20260918)
    p.add_argument("--grid-points", type=int, default=1200)
    p.add_argument("--p-max", type=float, default=0.10)
    p.add_argument("--prior-a", type=float, default=0.5)
    p.add_argument("--prior-b", type=float, default=0.5)
    args = p.parse_args()

    rows = read_csv(args.latent_input_csv)
    calibration = json.loads(args.calibration_json.read_text(encoding="utf-8"))
    result = fit(
        rows,
        calibration,
        draws=args.draws,
        seed=args.seed,
        grid_points=args.grid_points,
        p_max=args.p_max,
        prior_a=args.prior_a,
        prior_b=args.prior_b,
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
