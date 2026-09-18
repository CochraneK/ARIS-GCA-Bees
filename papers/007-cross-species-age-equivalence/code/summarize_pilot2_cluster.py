#!/usr/bin/env python3
"""Cluster-robust summary for ARIS4C007 Pilot 2 observed-event benchmark.

Resampling unit: source species × Timepoint.

The bootstrap is implemented with multinomial cluster counts and vectorized
weighted medians. This is statistically equivalent to resampling clusters with
replacement while avoiding explicit row replication.

Primary comparison:
    median absolute log10 PCD error(A3) - median absolute log10 PCD error(A1)

Negative values favor A3; positive values favor A1.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


A1 = "A1_relative_lifespan"
A3 = "A3_loglinear"


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
    a1 = np.asarray([float(r["a1_error"]) for r in rows], dtype=float)
    a3 = np.asarray([float(r["a3_error"]) for r in rows], dtype=float)
    d = a3 - a1
    return {
        "n_event_rows": len(rows),
        "n_clusters": len({str(r["cluster_id"]) for r in rows}),
        "median_abs_log10_error_A1": float(np.median(a1)),
        "median_abs_log10_error_A3": float(np.median(a3)),
        "median_error_difference_A3_minus_A1": float(
            np.median(a3) - np.median(a1)
        ),
        "paired_event_win_rate_A3": float(np.mean(d < 0)),
        "paired_event_tie_rate": float(np.mean(d == 0)),
    }


def _weighted_medians(
    errors: np.ndarray,
    row_cluster_idx: np.ndarray,
    cluster_counts: np.ndarray,
) -> np.ndarray:
    """Exact sample median after implicit cluster replication.

    For even replicated sample sizes, average the two central observations to
    match Python/R/NumPy's ordinary median definition.
    """
    order = np.argsort(errors, kind="mergesort")
    sorted_errors = errors[order]
    sorted_cluster_idx = row_cluster_idx[order]

    weights = cluster_counts[:, sorted_cluster_idx]
    cum = np.cumsum(weights, axis=1)
    totals = cum[:, -1]

    p1 = (totals + 1) // 2
    p2 = (totals + 2) // 2

    i1 = np.argmax(cum >= p1[:, None], axis=1)
    i2 = np.argmax(cum >= p2[:, None], axis=1)
    return (sorted_errors[i1] + sorted_errors[i2]) / 2.0


def bootstrap(
    rows: list[dict[str, object]],
    *,
    seed: int,
    reps: int = 10000,
    stratify_species: bool = False,
    chunk_size: int = 500,
) -> dict[str, object]:
    clusters = sorted({str(r["cluster_id"]) for r in rows})
    cluster_index = {c: i for i, c in enumerate(clusters)}
    row_cluster_idx = np.asarray(
        [cluster_index[str(r["cluster_id"])] for r in rows],
        dtype=np.int32,
    )
    a1 = np.asarray([float(r["a1_error"]) for r in rows], dtype=float)
    a3 = np.asarray([float(r["a3_error"]) for r in rows], dtype=float)

    if stratify_species:
        cluster_species = {}
        for r in rows:
            cluster_species[str(r["cluster_id"])] = str(r["source_species_label"])
        strata = []
        for sp in sorted(set(cluster_species.values())):
            idx = np.asarray(
                [
                    cluster_index[c]
                    for c in clusters
                    if cluster_species[c] == sp
                ],
                dtype=np.int32,
            )
            strata.append(idx)
    else:
        strata = [np.arange(len(clusters), dtype=np.int32)]

    rng = np.random.default_rng(seed)
    diffs = np.empty(reps, dtype=float)

    start = 0
    while start < reps:
        m = min(chunk_size, reps - start)
        counts = np.zeros((m, len(clusters)), dtype=np.int16)

        for idx in strata:
            if len(idx) == 1:
                counts[:, idx[0]] = 1
            else:
                draw = rng.multinomial(
                    len(idx),
                    np.full(len(idx), 1.0 / len(idx)),
                    size=m,
                )
                counts[:, idx] = draw.astype(np.int16, copy=False)

        med1 = _weighted_medians(a1, row_cluster_idx, counts)
        med3 = _weighted_medians(a3, row_cluster_idx, counts)
        diffs[start:start + m] = med3 - med1
        start += m

    point = point_summary(rows)
    ci = np.quantile(diffs, [0.025, 0.975])
    return {
        "observed_median_error_difference_A3_minus_A1":
            point["median_error_difference_A3_minus_A1"],
        "bootstrap_reps": reps,
        "cluster_unit": "source_species × Timepoint",
        "species_stratified": stratify_species,
        "bootstrap_95pct_interval": [float(ci[0]), float(ci[1])],
        "bootstrap_probability_A3_lower_median_error":
            float(np.mean(diffs < 0)),
    }


def summarize(
    rows: list[dict[str, object]],
    *,
    seed: int,
    cell: bool = False,
) -> dict[str, object]:
    if not rows:
        return {"n_event_rows": 0, "n_clusters": 0}
    species_n = len({str(r["source_species_label"]) for r in rows})
    out = point_summary(rows)

    # Very small cells are descriptive only. Do not bootstrap <5 independent
    # Timepoint clusters.
    if out["n_clusters"] >= 5:
        out["cluster_bootstrap"] = bootstrap(
            rows,
            seed=seed,
            reps=5000 if cell else 10000,
        )
        if species_n > 1:
            out["cluster_bootstrap_stratified_by_species"] = bootstrap(
                rows,
                seed=seed + 100000,
                reps=5000 if cell else 10000,
                stratify_species=True,
            )
    else:
        out["bootstrap_status"] = "not_run_fewer_than_5_clusters"
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
                rows,
                seed=cell_seed,
                cell=True,
            )
            cell_seed += 1

    result["guardrails"] = [
        "Bootstrap resamples biological Timepoint clusters, not individual sex/statistics rows.",
        "Overall/phase summaries include species-stratified cluster bootstrap to preserve species composition.",
        "Species × phase cells use 5,000 cluster resamples; cells with <5 clusters are descriptive only.",
        "Vectorized multinomial cluster-count bootstrap is equivalent to explicit cluster resampling with replacement.",
        "This remains observed-only; Januel imputation and fitted event-scale predictions are not used.",
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
