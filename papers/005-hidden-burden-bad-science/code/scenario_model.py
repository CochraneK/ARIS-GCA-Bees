#!/usr/bin/env python3
"""Transparent Fermi / scenario engine for ARIS4C005.

This module deliberately produces SCENARIOS, not empirical estimates. It is
useful for stress-testing the narrative units requested in the project (for
example researcher-life-years and equivalent PhD/career blocks) while keeping
all assumptions explicit and outside the scientific evidence ledger.

Do not insert researcher-level misconduct survey prevalence as article-level
prevalence. Do not cite outputs from the example parameter file as findings.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Any, Iterable


def triangular(rng: random.Random, spec: dict[str, float]) -> float:
    low = float(spec["low"])
    mode = float(spec["mode"])
    high = float(spec["high"])
    if not low <= mode <= high:
        raise ValueError(f"Invalid triangular range: {spec}")
    return rng.triangular(low, high, mode)


def quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("Cannot compute a quantile from an empty list")
    xs = sorted(values)
    pos = (len(xs) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return xs[lo]
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "p025": quantile(values, 0.025),
        "median": quantile(values, 0.5),
        "p975": quantile(values, 0.975),
        "mean": sum(values) / len(values),
    }


def run_scenario(params: dict[str, Any]) -> dict[str, Any]:
    draws = int(params.get("simulation_draws", 100_000))
    seed = int(params.get("seed", 405))
    if draws <= 0:
        raise ValueError("simulation_draws must be positive")

    n_works = float(params["annual_target_works"])
    if n_works < 0:
        raise ValueError("annual_target_works must be non-negative")

    rng = random.Random(seed)

    output: dict[str, list[float]] = {
        "problematic_works": [],
        "rly_direct": [],
        "rly_followup": [],
        "rly_total": [],
        "equivalent_5yr_phd_blocks": [],
        "equivalent_40yr_careers": [],
    }

    sb = params.get("sleeping_beauty_extension") or {}
    sb_enabled = bool(sb.get("enabled", False))
    if sb_enabled:
        output["candidate_sleeping_beauties"] = []
        output["expected_never_woken_sleeping_beauties"] = []

    for _ in range(draws):
        p_problem = triangular(rng, params["paper_problem_prevalence"])
        direct_effort = triangular(
            rng, params["direct_researcher_years_per_problematic_work"]
        )
        p_followup = triangular(rng, params["followup_probability"])
        followup_effort = triangular(
            rng, params["followup_researcher_years_if_triggered"]
        )

        n_problem = n_works * p_problem
        rly_direct = n_problem * direct_effort
        rly_followup = n_problem * p_followup * followup_effort
        rly_total = rly_direct + rly_followup

        output["problematic_works"].append(n_problem)
        output["rly_direct"].append(rly_direct)
        output["rly_followup"].append(rly_followup)
        output["rly_total"].append(rly_total)
        output["equivalent_5yr_phd_blocks"].append(rly_total / 5.0)
        output["equivalent_40yr_careers"].append(rly_total / 40.0)

        if sb_enabled:
            candidate_rate = triangular(rng, sb["candidate_rate"])
            lost_fraction = triangular(
                rng, sb["counterfactual_awakening_loss_fraction"]
            )
            n_candidates = n_works * candidate_rate
            n_never_woken = n_candidates * lost_fraction
            output["candidate_sleeping_beauties"].append(n_candidates)
            output["expected_never_woken_sleeping_beauties"].append(
                n_never_woken
            )

    return {
        "scenario_name": params.get("scenario_name", "unnamed scenario"),
        "classification": "SCENARIO_NOT_EMPIRICAL_ESTIMATE",
        "simulation_draws": draws,
        "seed": seed,
        "annual_target_works": n_works,
        "metrics": {name: summarize(values) for name, values in output.items()},
        "warning": (
            "All outputs inherit the assumptions supplied in the parameter file. "
            "They are not measurements of global misconduct, waste, or lost discoveries."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("parameters", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    params = json.loads(args.parameters.read_text(encoding="utf-8"))
    result = run_scenario(params)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
