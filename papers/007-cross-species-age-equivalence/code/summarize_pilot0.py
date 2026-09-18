#!/usr/bin/env python3
"""Summarize ARIS4C007 Pilot 0 mapping disagreement using only stdlib."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def q(values: list[float], p: float) -> float:
    xs = sorted(values)
    if not xs:
        raise ValueError("empty values")
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mapping_csv", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    rows = []
    with args.mapping_csv.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            row["absolute_disagreement_y"] = float(row["absolute_disagreement_y"])
            row["human_age_relative_lifespan_y"] = float(row["human_age_relative_lifespan_y"])
            row["human_age_loglinear_y"] = float(row["human_age_loglinear_y"])
            row["signed_diff_y"] = (
                row["human_age_loglinear_y"] - row["human_age_relative_lifespan_y"]
            )
            rows.append(row)

    by_stage: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_stage[row["stage"]].append(row)

    stages = {}
    for stage, group in sorted(by_stage.items()):
        values = [r["absolute_disagreement_y"] for r in group]
        signed = [r["signed_diff_y"] for r in group]
        stages[stage] = {
            "n_species": len({r["species"] for r in group}),
            "median_absolute_disagreement_y": statistics.median(values),
            "mean_absolute_disagreement_y": statistics.fmean(values),
            "p75_absolute_disagreement_y": q(values, 0.75),
            "p90_absolute_disagreement_y": q(values, 0.90),
            "p95_absolute_disagreement_y": q(values, 0.95),
            "max_absolute_disagreement_y": max(values),
            "median_signed_loglinear_minus_relative_y": statistics.median(signed),
            "proportion_loglinear_gt_relative": sum(x > 0 for x in signed) / len(signed),
        }

    stage50 = by_stage.get("max_fraction_0.50", [])
    high50 = [r for r in stage50 if r["data_quality"] == "high"]
    high50_sorted = sorted(
        high50, key=lambda r: r["absolute_disagreement_y"], reverse=True
    )[:15]

    order_groups: dict[str, list[dict]] = defaultdict(list)
    for row in stage50:
        order_groups[row["order"]].append(row)
    order_summary = []
    for order, group in order_groups.items():
        species_n = len({r["species"] for r in group})
        if species_n < 5:
            continue
        vals = [r["absolute_disagreement_y"] for r in group]
        signed = [r["signed_diff_y"] for r in group]
        order_summary.append(
            {
                "order": order,
                "n_species": species_n,
                "median_absolute_disagreement_y": statistics.median(vals),
                "median_signed_loglinear_minus_relative_y": statistics.median(signed),
            }
        )
    order_summary.sort(
        key=lambda x: x["median_absolute_disagreement_y"], reverse=True
    )

    out = {
        "n_rows": len(rows),
        "n_species": len({r["species"] for r in rows}),
        "data_quality_counts_at_50pct_max": dict(
            Counter(r["data_quality"] for r in stage50)
        ),
        "stage_summary": stages,
        "highest_disagreement_high_quality_at_50pct_max": [
            {
                "species": r["species"],
                "common_name": r["common_name"],
                "order": r["order"],
                "relative_lifespan_human_y": r["human_age_relative_lifespan_y"],
                "loglinear_human_y": r["human_age_loglinear_y"],
                "absolute_disagreement_y": r["absolute_disagreement_y"],
            }
            for r in high50_sorted
        ],
        "order_summary_at_50pct_max_n_ge_5": order_summary,
        "interpretation_guardrail": (
            "This file summarizes disagreement between two candidate coordinate "
            "systems. It does not establish that either coordinate is a true "
            "human-equivalent biological age."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
