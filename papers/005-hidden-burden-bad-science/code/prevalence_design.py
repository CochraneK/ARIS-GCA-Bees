#!/usr/bin/env python3
"""Prevalence audit design simulation for ARIS4C005.

This is a DESIGN tool, not an empirical prevalence estimator.

For candidate population-random adjudication sample sizes and hypothetical true
severe-failure prevalences, it simulates exact binary gold-standard audits and
summarizes a Jeffreys Beta(1/2,1/2) posterior interval.

The purpose is to answer: how many population-random adjudications are needed
before a rare article-level prevalence is measured with useful precision?

Detector-enriched cases are intentionally excluded from this calculation; they
improve detector calibration, but they do not substitute for the random audit.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from pathlib import Path
from typing import Any


def betacf(a: float, b: float, x: float) -> float:
    max_iter = 200
    eps = 3e-14
    fpmin = 1e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def beta_cdf(x: float, a: float, b: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    ln_bt = (
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + a * math.log(x)
        + b * math.log1p(-x)
    )
    bt = math.exp(ln_bt)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b


def beta_ppf(q: float, a: float, b: float) -> float:
    if q <= 0:
        return 0.0
    if q >= 1:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(70):
        mid = (lo + hi) / 2.0
        if beta_cdf(mid, a, b) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def jeffreys_interval(x: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    a = x + 0.5
    b = n - x + 0.5
    return beta_ppf(alpha / 2.0, a, b), beta_ppf(1.0 - alpha / 2.0, a, b)


def binomial_rare(rng: random.Random, n: int, p: float) -> int:
    """Exact binomial sampler using geometric gaps; efficient for small p."""
    if p <= 0:
        return 0
    if p >= 1:
        return n
    log_q = math.log1p(-p)
    pos = 0
    successes = 0
    while True:
        u = rng.random()
        gap = int(math.floor(math.log(u) / log_q)) + 1
        pos += gap
        if pos > n:
            return successes
        successes += 1


def scenario(
    n: int,
    p: float,
    reps: int,
    seed: int,
) -> dict[str, Any]:
    rng = random.Random(seed)
    cache: dict[int, tuple[float, float]] = {}
    widths: list[float] = []
    lower: list[float] = []
    upper: list[float] = []
    xs: list[int] = []
    covers = 0

    for _ in range(reps):
        x = binomial_rare(rng, n, p)
        xs.append(x)
        if x not in cache:
            cache[x] = jeffreys_interval(x, n)
        lo, hi = cache[x]
        lower.append(lo)
        upper.append(hi)
        widths.append(hi - lo)
        covers += int(lo <= p <= hi)

    widths_sorted = sorted(widths)
    return {
        "n_random": n,
        "true_prevalence": p,
        "replications": reps,
        "expected_positive_count": n * p,
        "probability_zero_positive_exact": (1.0 - p) ** n,
        "simulated_positive_count_median": statistics.median(xs),
        "simulated_positive_count_p05": sorted(xs)[max(0, int(0.05 * reps) - 1)],
        "simulated_positive_count_p95": sorted(xs)[min(reps - 1, int(0.95 * reps))],
        "median_95_posterior_width": statistics.median(widths),
        "median_95_lower": statistics.median(lower),
        "median_95_upper": statistics.median(upper),
        "p90_95_posterior_width": widths_sorted[min(reps - 1, int(0.90 * reps))],
        "simulated_95_interval_coverage": covers / reps,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("output_json", type=Path)
    p.add_argument("--prevalence", action="append", type=float, default=[])
    p.add_argument("--n", action="append", type=int, default=[])
    p.add_argument("--reps", type=int, default=1000)
    p.add_argument("--seed", type=int, default=20260918)
    args = p.parse_args()

    prevalences = args.prevalence or [0.002, 0.005, 0.01, 0.02]
    sample_sizes = args.n or [600, 1000, 2000, 5000, 10000]

    results = []
    for i, prevalence in enumerate(prevalences):
        for j, n in enumerate(sample_sizes):
            results.append(
                scenario(
                    n,
                    prevalence,
                    args.reps,
                    args.seed + i * 1000 + j,
                )
            )

    output = {
        "classification": "DESIGN_SIMULATION_NOT_EMPIRICAL_PREVALENCE",
        "prior": "Jeffreys Beta(0.5, 0.5)",
        "prevalence_scenarios": prevalences,
        "random_audit_sample_sizes": sample_sizes,
        "results": results,
        "interpretation": (
            "Use these results to size the population-random adjudication arm. "
            "Detector-enriched cases serve calibration and cannot replace random auditing."
        ),
        "warnings": [
            "Hypothetical true prevalences are design scenarios, not estimates.",
            "This assumes an error-free binary reference label for the random audit; AI adjudication error is modeled separately.",
            "Field/year heterogeneity and design effects can require larger samples.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
