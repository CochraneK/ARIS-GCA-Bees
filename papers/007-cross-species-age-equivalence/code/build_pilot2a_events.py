#!/usr/bin/env python3
"""ARIS4C007 Pilot 2A: held-out Translating Time event benchmark.

This benchmark uses only directly observed homologous events in Januel et al.
2026 Table S1. It does not use Amelia imputation or the authors' event-scale
model, so the evaluation target remains independent of the candidate mappings.

A1 and A3 are constructed from Pilot 0 life-history traits. Events that directly
encode gestation, sexual maturity, or lifespan/maximum-longevity anchors are
excluded from the confirmatory held-out set.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import statistics
import unicodedata
from collections import defaultdict
from pathlib import Path

from age_mappings import map_by_loglinear, map_by_relative_age
from build_pilot1_demography import load_pilot0_species


DAYS_PER_YEAR = 365.25
TABLE_TO_CANONICAL = {
    "Felis": "Felis catus",
    "Mus musculus": "Mus musculus",
    "Pan troglodytes": "Pan troglodytes",
}
HUMAN_TABLE_NAME = "Homo sapiens"

ANCHOR_PATTERNS = [
    re.compile(r"gestation", re.I),
    re.compile(r"sexual maturity", re.I),
    re.compile(r"maximum.*life", re.I),
    re.compile(r"maximal.*life", re.I),
    re.compile(r"maximum longevity", re.I),
    re.compile(r"longevity.*maximum", re.I),
]


def clean_text(value: str) -> str:
    value = value or ""
    value = "".join(
        ch for ch in value
        if unicodedata.category(ch) not in {"Cc", "Cf"}
    )
    return value.replace("\u00a0", " ").strip()


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def median_abs(xs: list[float]) -> float:
    return statistics.median(abs(x) for x in xs)


def quantile(values: list[float], p: float) -> float:
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


def is_anchor_event(timepoint: str) -> bool:
    return any(p.search(timepoint) for p in ANCHOR_PATTERNS)


def stage_for(source_postbirth_y: float, maturity_y: float, max_life_y: float) -> str:
    if source_postbirth_y < 0:
        return "prenatal"
    if source_postbirth_y < maturity_y:
        return "postnatal_pre_maturity"
    if source_postbirth_y < 0.5 * max_life_y:
        return "adult_pre_midlife"
    return "mid_late_life"


def bootstrap_paired_abs_log_error_difference(
    e1: list[float],
    e3: list[float],
    *,
    seed: int,
    reps: int = 10000,
) -> dict[str, object]:
    """Bootstrap median(|err_A3|)-median(|err_A1|), paired by event."""
    if len(e1) != len(e3):
        raise ValueError("paired vectors must have equal length")
    rng = random.Random(seed)
    n = len(e1)
    diffs = []
    for _ in range(reps):
        idx = [rng.randrange(n) for _ in range(n)]
        a = [abs(e1[i]) for i in idx]
        b = [abs(e3[i]) for i in idx]
        diffs.append(statistics.median(b) - statistics.median(a))
    return {
        "observed_median_abs_log10_error_difference_A3_minus_A1": (
            statistics.median(abs(x) for x in e3)
            - statistics.median(abs(x) for x in e1)
        ),
        "bootstrap_reps": reps,
        "bootstrap_95pct_interval": [
            quantile(diffs, 0.025),
            quantile(diffs, 0.975),
        ],
    }


def summarize(group: list[dict[str, object]], *, seed: int) -> dict[str, object]:
    e1 = [float(x["A1_log10_error"]) for x in group]
    e3 = [float(x["A3_log10_error"]) for x in group]

    def one(errs: list[float]) -> dict[str, float]:
        abs_err = [abs(x) for x in errs]
        return {
            "median_abs_log10_error": statistics.median(abs_err),
            "mean_abs_log10_error": statistics.fmean(abs_err),
            "rmse_log10": math.sqrt(statistics.fmean(x * x for x in errs)),
            "median_multiplicative_error_factor": 10 ** statistics.median(abs_err),
            "p90_multiplicative_error_factor": 10 ** quantile(abs_err, 0.90),
        }

    return {
        "n_events": len(group),
        "A1_relative_lifespan": one(e1),
        "A3_loglinear": one(e3),
        "paired_bootstrap": bootstrap_paired_abs_log_error_difference(
            e1, e3, seed=seed
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot0-grid", type=Path, required=True)
    ap.add_argument("--pilot0-coverage", type=Path, required=True)
    ap.add_argument("--table-s1", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("data/pilot2a_events"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    species_times, upstream = load_pilot0_species(
        args.pilot0_grid,
        args.pilot0_coverage,
    )
    human = species_times["Homo sapiens"]

    # Mirror the authors' observed-data preprocessing:
    # group by Species, Timepoint, Statistics, Sex, then mean PCD.
    grouped: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)
    with args.table_s1.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    for row in rows:
        species = clean_text(row.get("Species", ""))
        timepoint = clean_text(row.get("Timepoint", ""))
        stats = clean_text(row.get("Statistics", ""))
        sex = clean_text(row.get("Sex", ""))
        try:
            pcd = float(row["PCD"])
        except (TypeError, ValueError):
            continue
        if pcd <= 0:
            continue
        grouped[(timepoint, stats, species, sex)].append(pcd)

    means = {
        key: mean(values)
        for key, values in grouped.items()
    }

    # Index humans by exactly the same event key excluding Species.
    human_obs: dict[tuple[str, str, str], float] = {}
    for (timepoint, stats, species, sex), pcd in means.items():
        if species == HUMAN_TABLE_NAME:
            human_obs[(timepoint, stats, sex)] = pcd

    output: list[dict[str, object]] = []
    excluded_anchors = 0
    no_human_match = 0

    for (timepoint, stats, species_label, sex), source_pcd_days in means.items():
        canonical = TABLE_TO_CANONICAL.get(species_label)
        if canonical is None:
            continue
        target_pcd_days = human_obs.get((timepoint, stats, sex))
        if target_pcd_days is None:
            no_human_match += 1
            continue
        if is_anchor_event(timepoint):
            excluded_anchors += 1
            continue

        source = species_times.get(canonical)
        if source is None:
            continue

        # Candidate mapping functions operate on post-birth chronological age.
        # Table S1 uses post-conception days, so subtract source gestation before
        # mapping and add human gestation back for the comparison target.
        source_postbirth_y = source_pcd_days / DAYS_PER_YEAR - source.gestation_y
        observed_human_pcd_y = target_pcd_days / DAYS_PER_YEAR

        # Avoid numerical edge cases at exactly conception.
        if source_postbirth_y <= -source.gestation_y:
            continue

        a1_postbirth_y = map_by_relative_age(source_postbirth_y, source, human)
        a3_postbirth_y = map_by_loglinear(source_postbirth_y, source, human)
        a1_human_pcd_y = a1_postbirth_y + human.gestation_y
        a3_human_pcd_y = a3_postbirth_y + human.gestation_y

        if min(observed_human_pcd_y, a1_human_pcd_y, a3_human_pcd_y) <= 0:
            continue

        output.append(
            {
                "source_species": canonical,
                "table_species": species_label,
                "timepoint": timepoint,
                "statistics": stats,
                "sex": sex,
                "stage": stage_for(
                    source_postbirth_y,
                    source.maturity_y,
                    source.max_lifespan_y,
                ),
                "source_observed_pcd_days": source_pcd_days,
                "human_observed_pcd_days": target_pcd_days,
                "human_observed_pcd_y": observed_human_pcd_y,
                "A1_predicted_human_pcd_y": a1_human_pcd_y,
                "A3_predicted_human_pcd_y": a3_human_pcd_y,
                "A1_log10_error": math.log10(a1_human_pcd_y)
                - math.log10(observed_human_pcd_y),
                "A3_log10_error": math.log10(a3_human_pcd_y)
                - math.log10(observed_human_pcd_y),
            }
        )

    if not output:
        raise RuntimeError("No held-out observed event pairs were created")

    out_csv = args.out / "heldout_event_predictions.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

    by_species: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_stage: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in output:
        by_species[str(row["source_species"])].append(row)
        by_stage[str(row["stage"])].append(row)

    summary = {
        "table_s1_input_rows": len(rows),
        "authors_grouped_observed_cells": len(means),
        "heldout_pair_rows": len(output),
        "excluded_anchor_pairs": excluded_anchors,
        "source_cells_without_exact_human_match": no_human_match,
        "species": {
            name: summarize(group, seed=2026091800 + i)
            for i, (name, group) in enumerate(sorted(by_species.items()))
        },
        "stages": {
            name: summarize(group, seed=2026091900 + i)
            for i, (name, group) in enumerate(sorted(by_stage.items()))
        },
        "overall": summarize(output, seed=20260918),
        "upstream_pilot0": upstream,
        "metric_note": (
            "Errors are on log10 post-conception age. A median absolute log10 "
            "error of e corresponds to a multiplicative age error factor 10^e."
        ),
        "heldout_rule": (
            "Events containing gestation, sexual maturity, maximum lifespan or "
            "maximum longevity language are excluded because those constructs "
            "directly contribute to A1/A3."
        ),
        "guardrail": (
            "Exact event-name matching is conservative and avoids imputation, "
            "but repeated observations from the same literature and correlated "
            "events are not independent. Pilot 2B will cluster/leave-source-out "
            "and reproduce the authors' spline/event-scale model."
        ),
    }
    (args.out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
