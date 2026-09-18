#!/usr/bin/env python3
"""Cluster-robust summary for ARIS4C007 Pilot 2 observed-event benchmark.

Ordinary event-row bootstrap can overstate precision because the same biological
Timepoint can appear under multiple statistics/sex strata. This script treats
(source species × Timepoint) as the resampling cluster.

It reports:
- overall strict held-out benchmark;
- by source species;
- by diagnostic human-age phase;
- source species × phase cells;
- unstratified cluster bootstrap;
- species-stratified cluster bootstrap when >1 species is present.

Primary comparison remains:
    median absolute log10 PCD error(A3) - median absolute log10 PCD error(A1)

Negative values favor A3; positive values favor A1.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import statistics
from collections import defaultdict
from pathlib import Path


A1 = "A1_relative_lifespan"
A3 = "A3_loglinear"


def quantile(values: list[float], p: float) -> float:
    xs = sorted(values)
    if not xs:
        raise ValueError("empty vector")
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def load_pairs(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    keyed: dict[tuple[str, str, str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        if row.get("strict_heldout") != "1":
            continue
        key = (
            row["source_species_label"],
            row["timepoint"],
            row["statistics"],
            row["sex"],
        )
        keyed[key][row["method"]] = row

    pairs = []
    for key, methods in keyed.items():
        if A1 not in methods or A3 not in methods:
            continue
        r1 = methods[A1]
        r3 = methods[A3]
        pairs.append(
            {
                "source_species_label": key[0],
                "timepoint": key[1],
                "statistics": key[2],
                "sex": key[3],
                "human_phase": r1["human_phase"],
                "cluster_id": f"{key[0]}::{key[1]}",
                "a1_error": float(r1["absolute_log10_pcd_error"]),
                "a3_error": float(r3["absolute_log10_pcd_error"]),
            }
        )
    return pairs


def point_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    a1 = [float(r["a1_error"]) for r in rows]
    a3 = [float(r["a3_error"]) for r in rows]
    d = [float(r["a3_error"]) - float(r["a1_error"]) for r in rows]
    return {
        "n_event_rows": len(rows),
        "n_clusters": len({str(r["cluster_id"]) for r in rows}),
        "median_abs_log10_error_A1": statistics.median(a1),
        "median_abs_log10_error_A3": statistics.median(a3),
        "median_error_difference_A3_minus_A1": (
            statistics.median(a3) - statistics.median(a1)
        ),
        "paired_event_win_rate_A3": sum(x < 0 for x in d) / len(d),
        "paired_event_tie_rate": sum(x == 0 for x in d) / len(d),
    }


def _sample_cluster_rows(
    rows: list[dict[str, object]],
    rng: random.Random,
) -> list[dict[str, object]]:
    by_cluster: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_cluster[str(row["cluster_id"])].append(row)
    ids = list(by_cluster)
    sampled = []
    for _ in range(len(ids)):
        cid = ids[rng.randrange(len(ids))]
        sampled.extend(by_cluster[cid])
    return sampled


def _sample_cluster_rows_stratified_species(
    rows: list[dict[str, object]],
    rng: random.Random,
) -> list[dict[str, object]]:
    by_species: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_species[str(row["source_species_label"])].append(row)
    sampled = []
    for species_rows in by_species.values():
        sampled.extend(_sample_cluster_rows(species_rows, rng))
    return sampled


def bootstrap(
    rows: list[dict[str, object]],
    *,
    seed: int,
    reps: int = 10000,
    stratify_species: bool = False,
) -> dict[str, object]:
    rng = random.Random(seed)
    diffs = []
    for _ in range(reps):
        if stratify_species:
            sample = _sample_cluster_rows_stratified_species(rows, rng)
        else:
            sample = _sample_cluster_rows(rows, rng)
        a1 = [float(r["a1_error"]) for r in sample]
        a3 = [float(r["a3_error"]) for r in sample]
        diffs.append(statistics.median(a3) - statistics.median(a1))

    point = point_summary(rows)
    return {
        "observed_median_error_difference_A3_minus_A1":
            point["median_error_difference_A3_minus_A1"],
        "bootstrap_reps": reps,
        "cluster_unit": "source_species × Timepoint",
        "species_stratified": stratify_species,
        "bootstrap_95pct_interval": [quantile(diffs, 0.025), quantile(diffs, 0.975)],
        "bootstrap_probability_A3_lower_median_error":
            sum(x < 0 for x in diffs) / len(diffs),
    }


def summarize(rows: list[dict[str, object]], *, seed: int) -> dict[str, object]:
    if not rows:
        return {"n_event_rows": 0, "n_clusters": 0}
    species_n = len({str(r["source_species_label"]) for r in rows})
    out = point_summary(rows)
    out["cluster_bootstrap"] = bootstrap(rows, seed=seed)
    if species_n > 1:
        out["cluster_bootstrap_stratified_by_species"] = bootstrap(
            rows, seed=seed + 100000, stratify_species=True
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("predictions", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    pairs = load_pairs(args.predictions)
    if not pairs:
        raise RuntimeError("No strict held-out A1/A3 pairs found")

    species = sorted({str(r["source_species_label"]) for r in pairs})
    phases = [
        "prenatal",
        "postnatal_0_2",
        "juvenile_2_18",
        "adult_18_60",
        "late_60_plus",
    ]

    result: dict[str, object] = {
        "primary_comparison": (
            "median absolute log10 PCD error(A3) - "
            "median absolute log10 PCD error(A1)"
        ),
        "sign_interpretation": {
            "negative": "A3 lower median error",
            "positive": "A1 lower median error",
        },
        "cluster_unit": "source species × normalized Timepoint",
        "strict_heldout_event_rows": len(pairs),
        "strict_heldout_clusters": len({str(r["cluster_id"]) for r in pairs}),
        "overall": summarize(pairs, seed=2026091801),
        "by_species": {},
        "by_phase": {},
        "species_by_phase": {},
    }

    for i, sp in enumerate(species):
        rows = [r for r in pairs if r["source_species_label"] == sp]
        result["by_species"][sp] = summarize(rows, seed=2026091810 + i)

    for i, phase in enumerate(phases):
        rows = [r for r in pairs if r["human_phase"] == phase]
        result["by_phase"][phase] = summarize(rows, seed=2026091820 + i)

    cell_seed = 2026091900
    for sp in species:
        result["species_by_phase"][sp] = {}
        for phase in phases:
            rows = [
                r for r in pairs
                if r["source_species_label"] == sp
                and r["human_phase"] == phase
            ]
            result["species_by_phase"][sp][phase] = summarize(
                rows, seed=cell_seed
            )
            cell_seed += 1

    result["guardrails"] = [
        "Bootstrap resamples biological Timepoint clusters, not individual sex/statistics rows.",
        "Overall/phase summaries also include species-stratified cluster bootstrap to preserve species composition.",
        "Species × phase cells with very few clusters are descriptive and should not drive headline inference.",
        "This remains observed-only; Januel imputation and fitted event-scale predictions are not used.",
        "Phylogenetic inference is not applicable to only three source species and will enter the broader mammalian stage.",
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
