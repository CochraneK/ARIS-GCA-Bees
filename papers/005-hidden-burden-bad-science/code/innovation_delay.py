#!/usr/bin/env python3
"""Matched event-study / output-equivalent delay estimator for ARIS4C005.

Input is a unit-year panel organized into matched sets. Each matched set contains
at least one treated topic-neighborhood unit and one control unit sharing the same
event year.

For matched set m and event time k:
    D_mk = mean(Y_treated,mk) - mean(Y_control,mk)
    E_mk = D_mk - mean(D_mk over baseline event times)

Aggregate event-time effects are equal-weight means across valid matched sets.
Bootstrap confidence intervals resample matched sets.

For nonnegative count/value outcomes, cumulative negative post-shock effects are
converted into baseline-output-equivalent years:
    delay_m = sum_k max(0, -E_mk) / baseline treated annual outcome_m

This is an output-equivalent delay metric, NOT literal calendar delay of a
discovery and NOT Researcher-Life-Years.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean of empty list")
    return sum(values) / len(values)


def quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("quantile of empty list")
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


def ols_slope(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2 or len(xs) != len(ys):
        return None
    xbar = mean(xs)
    ybar = mean(ys)
    denom = sum((x - xbar) ** 2 for x in xs)
    if denom == 0:
        return None
    return sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denom


def parse_bool(value: str) -> int:
    v = value.strip()
    if v in {"1", "true", "TRUE", "True"}:
        return 1
    if v in {"0", "false", "FALSE", "False"}:
        return 0
    raise ValueError(f"Invalid treated value: {value!r}")


def parse_panel(
    rows: list[dict[str, str]],
    outcome: str,
) -> dict[str, dict[int, dict[str, list[float]]]]:
    panel: dict[str, dict[int, dict[str, list[float]]]] = defaultdict(
        lambda: defaultdict(lambda: {"treated": [], "control": []})
    )
    seen_unit_year: set[tuple[str, str, int]] = set()

    for row in rows:
        matched_set = (row.get("matched_set_id") or "").strip()
        unit = (row.get("unit_id") or "").strip()
        if not matched_set or not unit:
            raise ValueError("matched_set_id and unit_id are required")

        event_year = int(row["event_year"])
        year = int(row["year"])
        event_time = int(row.get("event_time") or (year - event_year))
        if event_time != year - event_year:
            raise ValueError(
                f"Inconsistent event_time for {matched_set}/{unit}/{year}"
            )

        key = (matched_set, unit, year)
        if key in seen_unit_year:
            raise ValueError(f"Duplicate matched_set/unit/year row: {key}")
        seen_unit_year.add(key)

        treated = parse_bool(row["treated"])
        raw = (row.get(outcome) or "").strip()
        if raw == "":
            continue
        value = float(raw)
        if value < 0:
            raise ValueError(
                f"{outcome} contains negative value for {matched_set}/{unit}/{year}"
            )

        bucket = "treated" if treated else "control"
        panel[matched_set][event_time][bucket].append(value)

    return panel


def compute_set_effects(
    panel_set: dict[int, dict[str, list[float]]],
    *,
    baseline_times: list[int],
    post_times: list[int],
) -> tuple[dict[int, float] | None, dict[str, Any]]:
    raw_diff: dict[int, float] = {}
    treated_means: dict[int, float] = {}
    control_means: dict[int, float] = {}

    for k, groups in panel_set.items():
        if groups["treated"] and groups["control"]:
            t = mean(groups["treated"])
            c = mean(groups["control"])
            treated_means[k] = t
            control_means[k] = c
            raw_diff[k] = t - c

    missing_baseline = [k for k in baseline_times if k not in raw_diff]
    if missing_baseline:
        return None, {
            "valid": False,
            "reason": "INCOMPLETE_BASELINE",
            "missing_baseline_times": missing_baseline,
        }

    baseline_diff = mean([raw_diff[k] for k in baseline_times])
    effects = {k: d - baseline_diff for k, d in raw_diff.items()}

    baseline_treated = mean([treated_means[k] for k in baseline_times])
    observed_post = [k for k in post_times if k in effects]

    cumulative_deficit = sum(max(0.0, -effects[k]) for k in observed_post)
    delay_years = (
        cumulative_deficit / baseline_treated
        if baseline_treated > 0
        else None
    )

    return effects, {
        "valid": True,
        "baseline_difference": baseline_diff,
        "baseline_treated_annual_outcome": baseline_treated,
        "post_times_observed": observed_post,
        "cumulative_negative_output_gap": cumulative_deficit,
        "output_equivalent_delay_years": delay_years,
    }


def aggregate_effects(
    set_effects: dict[str, dict[int, float]],
) -> dict[int, dict[str, float | int]]:
    all_times = sorted(
        {k for effects in set_effects.values() for k in effects}
    )
    output: dict[int, dict[str, float | int]] = {}
    for k in all_times:
        vals = [
            effects[k]
            for effects in set_effects.values()
            if k in effects
        ]
        output[k] = {
            "matched_sets": len(vals),
            "effect_mean": mean(vals),
            "effect_median": statistics.median(vals),
        }
    return output


def bootstrap_event_ci(
    set_effects: dict[str, dict[int, float]],
    *,
    reps: int,
    seed: int,
) -> dict[int, dict[str, float]]:
    if reps <= 0:
        return {}
    ids = sorted(set_effects)
    if not ids:
        return {}

    rng = random.Random(seed)
    all_times = sorted(
        {k for effects in set_effects.values() for k in effects}
    )
    draws: dict[int, list[float]] = {k: [] for k in all_times}

    for _ in range(reps):
        sampled_ids = [rng.choice(ids) for _ in ids]
        for k in all_times:
            vals = [
                set_effects[mid][k]
                for mid in sampled_ids
                if k in set_effects[mid]
            ]
            if vals:
                draws[k].append(mean(vals))

    return {
        k: {
            "bootstrap_q025": quantile(vals, 0.025),
            "bootstrap_q975": quantile(vals, 0.975),
        }
        for k, vals in draws.items()
        if vals
    }


def estimate(
    rows: list[dict[str, str]],
    *,
    outcome: str,
    baseline_times: list[int],
    post_times: list[int],
    bootstrap_reps: int = 1000,
    seed: int = 20260918,
) -> dict[str, Any]:
    if not baseline_times:
        raise ValueError("baseline_times cannot be empty")
    if any(k >= 0 for k in baseline_times):
        raise ValueError("baseline_times must be strictly pre-event")
    if any(k < 0 for k in post_times):
        raise ValueError("post_times must be event/post-event")

    panel = parse_panel(rows, outcome)

    valid_effects: dict[str, dict[int, float]] = {}
    set_summaries: dict[str, dict[str, Any]] = {}
    exclusion_reasons: dict[str, int] = defaultdict(int)

    for matched_set, panel_set in panel.items():
        effects, summary = compute_set_effects(
            panel_set,
            baseline_times=baseline_times,
            post_times=post_times,
        )
        set_summaries[matched_set] = summary
        if effects is None:
            exclusion_reasons[summary["reason"]] += 1
        else:
            valid_effects[matched_set] = effects

    if not valid_effects:
        raise ValueError("No matched sets have complete baseline treated/control data")

    aggregate = aggregate_effects(valid_effects)
    ci = bootstrap_event_ci(
        valid_effects,
        reps=bootstrap_reps,
        seed=seed,
    )
    for k, vals in ci.items():
        aggregate[k].update(vals)

    pre_effects = [
        aggregate[k]["effect_mean"]
        for k in baseline_times
        if k in aggregate
    ]
    pre_times = [
        k for k in baseline_times if k in aggregate
    ]

    delay_values = [
        s["output_equivalent_delay_years"]
        for s in set_summaries.values()
        if s.get("valid") and s.get("output_equivalent_delay_years") is not None
    ]
    cumulative_gap_values = [
        s["cumulative_negative_output_gap"]
        for s in set_summaries.values()
        if s.get("valid")
    ]

    result = {
        "classification": "MATCHED_EVENT_STUDY_CAUSAL_CANDIDATE_NOT_AUTOMATIC_CAUSAL_CLAIM",
        "outcome": outcome,
        "baseline_event_times": baseline_times,
        "post_event_times": post_times,
        "matched_sets_input": len(panel),
        "matched_sets_valid": len(valid_effects),
        "matched_sets_excluded": len(panel) - len(valid_effects),
        "exclusion_reasons": dict(exclusion_reasons),
        "event_study": {
            str(k): aggregate[k] for k in sorted(aggregate)
        },
        "pretrend_diagnostics": {
            "pre_event_effect_mean_abs": (
                mean([abs(v) for v in pre_effects]) if pre_effects else None
            ),
            "pre_event_effect_max_abs": (
                max([abs(v) for v in pre_effects]) if pre_effects else None
            ),
            "pre_event_slope": ols_slope(
                [float(k) for k in pre_times],
                [float(v) for v in pre_effects],
            ),
            "interpretation": (
                "Diagnostic only. A materially non-zero pretrend weakens causal interpretation."
            ),
        },
        "output_equivalent_delay": {
            "matched_sets_with_defined_delay": len(delay_values),
            "mean_years": mean(delay_values) if delay_values else None,
            "median_years": (
                statistics.median(delay_values) if delay_values else None
            ),
            "q025_years": quantile(delay_values, 0.025) if delay_values else None,
            "q975_years": quantile(delay_values, 0.975) if delay_values else None,
            "mean_cumulative_negative_output_gap": (
                mean(cumulative_gap_values) if cumulative_gap_values else None
            ),
            "unit": "baseline annual outcome equivalents",
        },
        "warnings": [
            "Output-equivalent delay is not literal discovery delay.",
            "Causal interpretation requires credible pre-shock matching and acceptable pre-trends.",
            "Negative post-shock effects can reflect rational updating, stigma, field correction, or other mechanisms.",
            "This metric must not be added to Researcher-Life-Years.",
            "Matching features must be pre-treatment.",
        ],
    }
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("panel_csv", type=Path)
    p.add_argument("output_json", type=Path)
    p.add_argument("--outcome", default="outcome_articles")
    p.add_argument("--baseline", action="append", type=int, default=[])
    p.add_argument("--post", action="append", type=int, default=[])
    p.add_argument("--bootstrap-reps", type=int, default=1000)
    p.add_argument("--seed", type=int, default=20260918)
    args = p.parse_args()

    baseline = args.baseline or [-3, -2, -1]
    post = args.post or [0, 1, 2, 3, 4, 5]

    with args.panel_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    result = estimate(
        rows,
        outcome=args.outcome,
        baseline_times=baseline,
        post_times=post,
        bootstrap_reps=args.bootstrap_reps,
        seed=args.seed,
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
