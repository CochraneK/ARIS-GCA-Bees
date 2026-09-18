#!/usr/bin/env python3
"""Stage-1F: repeated family-held-out paired uncertainty analysis.

Primary contrast is pre-specified from earlier stages: tree minus directly optimized
circular Spearman on the SAME top-level-family hold-out split. Low-rank minus circular
is secondary. The goal is to quantify whether the non-periodic advantage is stable or
is driven by a few split draws.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import stage1 as base
import stage1b as robust

HERE = Path(__file__).resolve().parent
SEED = 2031
N_SPLITS = 20
MAX_ATTEMPTS = 80
MIN_EVAL_PAIRS = 100
N_BOOT = 5000


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator) -> dict:
    values = np.asarray(values, dtype=float)
    means = np.empty(N_BOOT, dtype=float)
    n = len(values)
    for i in range(N_BOOT):
        means[i] = rng.choice(values, size=n, replace=True).mean()
    return {
        "mean": float(values.mean()),
        "sd": float(values.std(ddof=1)),
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "win_fraction_gt_zero": float(np.mean(values > 0)),
    }


def main():
    rng = np.random.default_rng(SEED)
    df, features, families = base.load_data()
    runs = []
    attempts = 0

    while len(runs) < N_SPLITS and attempts < MAX_ATTEMPTS:
        attempts += 1
        train_idx, test_idx = base.family_split_indices(families, rng)
        train_sim, _ = base.pairwise_nmi(df.iloc[train_idx], features)
        test_sim, _ = base.pairwise_nmi(df.iloc[test_idx], features)
        mask = base.upper_mask(train_sim, test_sim)
        if int(mask.sum()) < MIN_EVAL_PAIRS:
            continue
        train_mask = robust.all_train_mask(train_sim)
        fits = [
            base.fit_lowrank(train_sim, rank=2),
            base.fit_tree(train_sim, train_mask),
            robust.fit_connected_euclidean(train_sim),
            robust.optimize_circle(train_sim, rng),
        ]
        scores = {f.name: base.score_model(f, test_sim, mask) for f in fits}
        runs.append({
            "split": len(runs),
            "attempt": attempts,
            "n_train": int(len(train_idx)),
            "n_test": int(len(test_idx)),
            "n_eval_pairs": int(mask.sum()),
            "scores": scores,
        })

    if len(runs) < N_SPLITS:
        raise RuntimeError(f"Only {len(runs)} valid splits after {attempts} attempts")

    def arr(model):
        return np.asarray([r["scores"][model]["spearman"] for r in runs], dtype=float)

    circ = arr("circular_optimized")
    tree = arr("tree")
    low = arr("lowrank2")
    euc = arr("euclidean_connected")
    delta_tree = tree - circ
    delta_low = low - circ
    delta_euc = euc - circ

    contrasts = {
        "tree_minus_circular": bootstrap_ci(delta_tree, rng),
        "lowrank_minus_circular": bootstrap_ci(delta_low, rng),
        "euclidean_minus_circular": bootstrap_ci(delta_euc, rng),
    }
    primary = contrasts["tree_minus_circular"]
    if primary["ci95_low"] > 0:
        verdict = "TREE_ADVANTAGE_STABLE"
    elif primary["ci95_high"] < 0:
        verdict = "CIRCULAR_ADVANTAGE_STABLE_OVER_TREE"
    else:
        verdict = "TREE_CIRCULAR_DIFFERENCE_UNCERTAIN"

    model_summary = {}
    for model in ("lowrank2", "tree", "euclidean_connected", "circular_optimized"):
        x = arr(model)
        model_summary[model] = {
            "mean_spearman": float(x.mean()),
            "sd_spearman": float(x.std(ddof=1)),
            "min": float(x.min()),
            "max": float(x.max()),
        }

    results = {
        "seed": SEED,
        "n_splits": N_SPLITS,
        "n_attempts": attempts,
        "n_languages": int(len(df)),
        "n_features": int(len(features)),
        "runs": runs,
        "models": model_summary,
        "paired_contrasts": contrasts,
        "verdict": verdict,
        "claim_boundary": "Bootstrap resamples held-out split results, not languages or phylogenetic trees; it quantifies split sensitivity but is not a full phylogenetic uncertainty model.",
    }
    (HERE / "stage1f-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Stage-1F · Repeated Family-Held-Out Uncertainty",
        "",
        f"**Verdict:** `{verdict}`",
        "",
        f"Valid splits: {N_SPLITS}/{attempts} attempts · features: {len(features)}",
        "",
        "## Model performance",
        "",
        "| Model | Spearman mean ± SD | Range |",
        "|---|---:|---:|",
    ]
    for model, s in model_summary.items():
        lines.append(f"| {model} | {s['mean_spearman']:.3f} ± {s['sd_spearman']:.3f} | {s['min']:.3f} to {s['max']:.3f} |")
    lines += ["", "## Paired contrasts", "", "| Contrast | Mean | 95% bootstrap CI | Win fraction |", "|---|---:|---:|---:|"]
    for name, s in contrasts.items():
        lines.append(f"| {name} | {s['mean']:.3f} | [{s['ci95_low']:.3f}, {s['ci95_high']:.3f}] | {s['win_fraction_gt_zero']:.2f} |")
    lines += [
        "",
        "The primary contrast is tree minus optimized circular performance on the same held-out-family split. A CI wholly above zero supports a stable tree advantage; a CI crossing zero means the ranking remains split-sensitive.",
        "",
        "## Claim boundary",
        "",
        results["claim_boundary"],
        "",
    ]
    (HERE / "STAGE1F_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"verdict": verdict, "primary": primary}, indent=2))


if __name__ == "__main__":
    main()
