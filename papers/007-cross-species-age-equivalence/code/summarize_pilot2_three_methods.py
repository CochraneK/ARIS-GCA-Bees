#!/usr/bin/env python3
"""ARIS4C007 Pilot 2 three-method benchmark.

Combines:
- A1: maximum-lifespan relative age
- A3: gestation/maturity log-linear age
- A4: Januel-style pairwise smooth spline with leave-one-Timepoint-out CV

All methods are evaluated on the same strict held-out observed event rows.
Cluster bootstrap unit: source species × biological Timepoint.

A4 is a data-rich species-pair learner and therefore has an information
advantage over A1/A3. Results compare predictive event alignment, not universal
biological truth.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


METHODS = [
    "A1_relative_lifespan",
    "A3_loglinear",
    "A4_pairwise_spline_LOTO",
]

COMPARISONS = [
    ("A3_loglinear", "A1_relative_lifespan"),
    ("A4_pairwise_spline_LOTO", "A1_relative_lifespan"),
    ("A4_pairwise_spline_LOTO", "A3_loglinear"),
]


def read_a1_a3(path: Path) -> dict[tuple[str, str, str, str, str], dict[str, object]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    out: dict[tuple[str, str, str, str, str], dict[str, object]] = {}
    for row in rows:
        if row.get("strict_heldout") != "1":
            continue
        key = (
            row["source_species_label"],
            row["timepoint"],
            row["statistics"],
            row["sex"],
            row["human_phase"],
        )
        rec = out.setdefault(
            key,
            {
                "source_species_label": key[0],
                "timepoint": key[1],
                "statistics": key[2],
                "sex": key[3],
                "human_phase": key[4],
                "cluster_id": f"{key[0]}::{key[1]}",
            },
        )
        rec[row["method"]] = float(row["absolute_log10_pcd_error"])
    return out


def merge_a4(
    base: dict[tuple[str, str, str, str, str], dict[str, object]],
    path: Path,
) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    for row in rows:
        key = (
            row["source_species_label"],
            row["timepoint"],
            row["statistics"],
            row["sex"],
            row["human_phase"],
        )
        rec = base.get(key)
        if rec is None:
            continue
        if row.get("fit_ok") != "1":
            continue
        rec["A4_pairwise_spline_LOTO"] = float(row["absolute_log10_pcd_error"])
        rec["A4_extrapolation"] = int(row["extrapolation"])
        rec["A4_author_pairwise_df"] = int(float(row["author_pairwise_df"]))

    merged = []
    for rec in base.values():
        if all(m in rec for m in METHODS):
            merged.append(rec)
    return merged


def point_metrics(rows: list[dict[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {
        "n_event_rows": len(rows),
        "n_clusters": len({str(r["cluster_id"]) for r in rows}),
        "n_species": len({str(r["source_species_label"]) for r in rows}),
    }
    for method in METHODS:
        x = np.asarray([float(r[method]) for r in rows], dtype=float)
        out[method] = {
            "median_abs_log10_error": float(np.median(x)),
            "mean_abs_log10_error": float(np.mean(x)),
            "p75_abs_log10_error": float(np.quantile(x, 0.75)),
            "p90_abs_log10_error": float(np.quantile(x, 0.90)),
            "median_fold_error": float(10 ** np.median(x)),
        }
    out["A4_extrapolation_rows"] = sum(
        int(r.get("A4_extrapolation", 0)) for r in rows
    )
    return out


def _weighted_medians(
    errors: np.ndarray,
    row_cluster_idx: np.ndarray,
    counts: np.ndarray,
) -> np.ndarray:
    order = np.argsort(errors, kind="mergesort")
    values = errors[order]
    idx = row_cluster_idx[order]
    weights = counts[:, idx]
    cum = np.cumsum(weights, axis=1)
    totals = cum[:, -1]
    p1 = (totals + 1) // 2
    p2 = (totals + 2) // 2
    i1 = np.argmax(cum >= p1[:, None], axis=1)
    i2 = np.argmax(cum >= p2[:, None], axis=1)
    return (values[i1] + values[i2]) / 2.0


def cluster_bootstrap(
    rows: list[dict[str, object]],
    *,
    seed: int,
    reps: int,
    stratify_species: bool,
) -> dict[str, object]:
    clusters = sorted({str(r["cluster_id"]) for r in rows})
    cidx = {c: i for i, c in enumerate(clusters)}
    row_cluster_idx = np.asarray(
        [cidx[str(r["cluster_id"])] for r in rows], dtype=np.int32
    )

    if stratify_species:
        cluster_species = {
            str(r["cluster_id"]): str(r["source_species_label"])
            for r in rows
        }
        strata = []
        for sp in sorted(set(cluster_species.values())):
            strata.append(
                np.asarray(
                    [cidx[c] for c in clusters if cluster_species[c] == sp],
                    dtype=np.int32,
                )
            )
    else:
        strata = [np.arange(len(clusters), dtype=np.int32)]

    errors = {
        m: np.asarray([float(r[m]) for r in rows], dtype=float)
        for m in METHODS
    }

    rng = np.random.default_rng(seed)
    diffs = {pair: np.empty(reps, dtype=float) for pair in COMPARISONS}

    chunk = 500
    pos = 0
    while pos < reps:
        n = min(chunk, reps - pos)
        counts = np.zeros((n, len(clusters)), dtype=np.int16)
        for idx in strata:
            if len(idx) == 1:
                counts[:, idx[0]] = 1
            else:
                counts[:, idx] = rng.multinomial(
                    len(idx),
                    np.full(len(idx), 1 / len(idx)),
                    size=n,
                ).astype(np.int16, copy=False)

        med = {
            m: _weighted_medians(errors[m], row_cluster_idx, counts)
            for m in METHODS
        }
        for pair in COMPARISONS:
            diffs[pair][pos:pos+n] = med[pair[0]] - med[pair[1]]
        pos += n

    out: dict[str, object] = {}
    for a, b in COMPARISONS:
        arr = diffs[(a, b)]
        observed = float(np.median(errors[a]) - np.median(errors[b]))
        ci = np.quantile(arr, [0.025, 0.975])
        out[f"{a}_minus_{b}"] = {
            "observed_median_error_difference": observed,
            "bootstrap_95pct_interval": [float(ci[0]), float(ci[1])],
            "probability_first_method_lower_median_error": float(np.mean(arr < 0)),
        }

    return {
        "bootstrap_reps": reps,
        "cluster_unit": "source species × Timepoint",
        "species_stratified": stratify_species,
        "comparisons": out,
    }


def summarize(
    rows: list[dict[str, object]],
    *,
    seed: int,
    reps: int = 10000,
    cell: bool = False,
) -> dict[str, object]:
    if not rows:
        return {"n_event_rows": 0, "n_clusters": 0}
    out = point_metrics(rows)
    if out["n_clusters"] >= 5:
        nreps = 5000 if cell else reps
        out["cluster_bootstrap"] = cluster_bootstrap(
            rows, seed=seed, reps=nreps, stratify_species=False
        )
        if out["n_species"] > 1:
            out["cluster_bootstrap_stratified_by_species"] = cluster_bootstrap(
                rows,
                seed=seed + 100000,
                reps=nreps,
                stratify_species=True,
            )
    else:
        out["bootstrap_status"] = "not_run_fewer_than_5_clusters"
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a1-a3", type=Path, required=True)
    ap.add_argument("--a4", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    base = read_a1_a3(args.a1_a3)
    rows = merge_a4(base, args.a4)
    if not rows:
        raise RuntimeError("No complete three-method rows")

    species = sorted({str(r["source_species_label"]) for r in rows})
    phases = [
        "prenatal",
        "postnatal_0_2",
        "juvenile_2_18",
        "adult_18_60",
        "late_60_plus",
    ]

    no_extrap = [r for r in rows if int(r.get("A4_extrapolation", 0)) == 0]

    result: dict[str, object] = {
        "benchmark": "strict held-out observed homologous events",
        "methods": {
            "A1_relative_lifespan": "gestation-offset maximum-lifespan relative age",
            "A3_loglinear": "Lu et al. gestation/maturity log-linear coordinate",
            "A4_pairwise_spline_LOTO": (
                "Januel-style pairwise smooth spline; all rows sharing held-out "
                "Timepoint excluded from fitting"
            ),
        },
        "information_asymmetry_warning": (
            "A4 learns a species-pair mapping from hundreds of homologous events. "
            "A1/A3 use only broad life-history traits. Better A4 prediction does "
            "not imply a universal biological clock."
        ),
        "complete_three_method_event_rows": len(rows),
        "complete_three_method_clusters": len({str(r["cluster_id"]) for r in rows}),
        "overall": summarize(rows, seed=2026092001),
        "overall_no_A4_extrapolation": summarize(no_extrap, seed=2026092002),
        "by_species": {},
        "by_phase": {},
        "species_by_phase": {},
    }

    for i, sp in enumerate(species):
        x = [r for r in rows if r["source_species_label"] == sp]
        result["by_species"][sp] = summarize(x, seed=2026092010+i)

    for i, phase in enumerate(phases):
        x = [r for r in rows if r["human_phase"] == phase]
        result["by_phase"][phase] = summarize(x, seed=2026092020+i)

    seed = 2026092100
    for sp in species:
        result["species_by_phase"][sp] = {}
        for phase in phases:
            x = [
                r for r in rows
                if r["source_species_label"] == sp
                and r["human_phase"] == phase
            ]
            result["species_by_phase"][sp][phase] = summarize(
                x, seed=seed, cell=True
            )
            seed += 1

    result["interpretation_guardrails"] = [
        "Headline inference should use cluster bootstrap, not naive event-row bootstrap.",
        "Species × phase cells with few Timepoint clusters are descriptive.",
        "A4 is cross-validated by Timepoint but trained on the same species pair; it tests data-rich event translation, not out-of-species generalization.",
        "A1/A3 require no event-pair training and therefore address a harder generalization problem.",
        "The next broad stage must test all candidate mappings on species absent from model fitting and incorporate phylogenetic structure.",
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
