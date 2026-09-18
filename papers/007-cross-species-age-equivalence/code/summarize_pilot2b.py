#!/usr/bin/env python3
"""Summarize ARIS4C007 Pilot 2B with cluster-aware uncertainty."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path


METHODS = {
    "A1_relative_lifespan": "A1_log10_error",
    "A3_loglinear": "A3_log10_error",
    "A4_event_spline_LOTO": "A4_event_spline_log10_error",
}


def quantile(values: list[float], p: float) -> float:
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def metric(errs: list[float]) -> dict[str, float]:
    ae = [abs(x) for x in errs]
    return {
        "n": len(errs),
        "median_abs_log10_error": statistics.median(ae),
        "mean_abs_log10_error": statistics.fmean(ae),
        "rmse_log10": math.sqrt(statistics.fmean(x * x for x in errs)),
        "median_multiplicative_error_factor": 10 ** statistics.median(ae),
        "p90_multiplicative_error_factor": 10 ** quantile(ae, 0.90),
    }


def cluster_bootstrap_difference(
    rows: list[dict[str, object]],
    method_b: str,
    method_a: str,
    *,
    seed: int,
    reps: int = 10000,
) -> dict[str, object]:
    """Median-absolute-error difference B-A; resample Timepoint clusters."""
    cluster_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        cluster_rows[str(row["timepoint"])].append(row)
    clusters = sorted(cluster_rows)
    if not clusters:
        raise ValueError("no clusters")

    def diff(sample_rows: list[dict[str, object]]) -> float:
        eb = [abs(float(r[method_b])) for r in sample_rows]
        ea = [abs(float(r[method_a])) for r in sample_rows]
        return statistics.median(eb) - statistics.median(ea)

    observed = diff(rows)
    rng = random.Random(seed)
    sims = []
    for _ in range(reps):
        selected = [clusters[rng.randrange(len(clusters))] for _ in clusters]
        sample = []
        for key in selected:
            sample.extend(cluster_rows[key])
        sims.append(diff(sample))

    return {
        "difference_definition": "median_abs_error(B) - median_abs_error(A)",
        "method_B": method_b,
        "method_A": method_a,
        "observed_difference_log10": observed,
        "n_timepoint_clusters": len(clusters),
        "bootstrap_reps": reps,
        "cluster_bootstrap_95pct_interval": [
            quantile(sims, 0.025),
            quantile(sims, 0.975),
        ],
    }


def summarize(rows: list[dict[str, object]], seed: int) -> dict[str, object]:
    out = {
        "n_rows": len(rows),
        "n_unique_timepoints": len({str(r["timepoint"]) for r in rows}),
        "methods": {},
        "cluster_bootstrap_pairwise": {},
    }
    for name, col in METHODS.items():
        errs = [float(r[col]) for r in rows]
        out["methods"][name] = metric(errs)

    comparisons = [
        ("A3_vs_A1", "A3_log10_error", "A1_log10_error"),
        ("A4_vs_A1", "A4_event_spline_log10_error", "A1_log10_error"),
        ("A4_vs_A3", "A4_event_spline_log10_error", "A3_log10_error"),
    ]
    for i, (label, b, a) in enumerate(comparisons):
        out["cluster_bootstrap_pairwise"][label] = cluster_bootstrap_difference(
            rows, b, a, seed=seed + i
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("predictions", type=Path)
    ap.add_argument("diagnostics", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    with args.predictions.open("r", encoding="utf-8", newline="") as fh:
        raw = list(csv.DictReader(fh))

    rows = []
    for row in raw:
        try:
            for col in METHODS.values():
                float(row[col])
        except (TypeError, ValueError):
            continue
        rows.append(row)

    if not rows:
        raise RuntimeError("No complete Pilot 2B rows")

    with args.diagnostics.open("r", encoding="utf-8", newline="") as fh:
        diagnostics = list(csv.DictReader(fh))

    by_species: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_stage: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_species[row["source_species"]].append(row)
        by_stage[row["stage"]].append(row)

    summary = {
        "n_complete_rows": len(rows),
        "n_unique_timepoints": len({r["timepoint"] for r in rows}),
        "author_style_full_fit_diagnostics": diagnostics,
        "overall": summarize(rows, 20260918),
        "species": {
            k: summarize(v, 20261000 + i)
            for i, (k, v) in enumerate(sorted(by_species.items()))
        },
        "stages": {
            k: summarize(v, 20262000 + i)
            for i, (k, v) in enumerate(sorted(by_stage.items()))
        },
        "method_definition": {
            "A4": (
                "Januel-style pairwise smooth.spline on log10 post-conception "
                "ages, using df=30 for cat-human and df=12 for mouse-human and "
                "chimp-human, evaluated by leave-one-Timepoint-out CV."
            ),
            "LOTO": (
                "All rows sharing the held-out Timepoint are removed before "
                "fitting, preventing same-name event variants from leaking into "
                "their own prediction."
            ),
        },
        "uncertainty": (
            "Pairwise bootstrap intervals resample Timepoint clusters rather "
            "than individual rows, reducing pseudo-replication from multiple "
            "Statistics/Sex rows per named event."
        ),
        "guardrail": (
            "Closely related Timepoints such as 50%, 60%, 70% milestones can "
            "still share biological information. A stricter event-family-out "
            "sensitivity remains useful."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
