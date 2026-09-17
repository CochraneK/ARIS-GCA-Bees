#!/usr/bin/env python3
"""Stage-1B robustness: give the periodic hypothesis a fairer test.

The first Stage-1 screen used angles inherited from a 2-D spectral embedding and
emitted a disconnected-graph warning. This robustness analysis addresses the two
most obvious reviewer attacks before interpreting the circular model's loss:

1) force the affinity graph to be connected with a tiny positive off-diagonal floor;
2) directly optimize one angular coordinate per feature for the circular kernel,
   rather than accepting spectral angles as final.

The primary comparison is family-held-out prediction of feature-feature NMI.
This remains exploratory: it is a fairness/sensitivity check, not a manuscript-level
phylogenetic or geographic analysis.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.stats import spearmanr
from sklearn.manifold import SpectralEmbedding

import stage1 as base

HERE = Path(__file__).resolve().parent
FEATURE_COUNTS = (40, 60)
N_SPLITS = 5
MAXITER = 180
N_STARTS = 2
SEED = 2027
EPS = 1e-8


def connected_affinity(sim: np.ndarray) -> tuple[np.ndarray, float]:
    A = base.safe_affinity(sim)
    n = len(A)
    off = ~np.eye(n, dtype=bool)
    positives = A[off & (A > 0)]
    if len(positives):
        floor = max(1e-6, float(np.quantile(positives, 0.05)) * 0.05)
    else:
        floor = 1e-6
    A[off] = np.maximum(A[off], floor)
    np.fill_diagonal(A, max(1.0, float(np.max(A))))
    return A, floor


def connected_coords(sim: np.ndarray) -> tuple[np.ndarray, float]:
    A, floor = connected_affinity(sim)
    model = SpectralEmbedding(
        n_components=2,
        affinity="precomputed",
        random_state=SEED,
        eigen_solver="arpack",
    )
    return model.fit_transform(A), floor


def all_train_mask(train_sim: np.ndarray) -> np.ndarray:
    iu = np.triu_indices_from(train_sim, k=1)
    valid = np.isfinite(train_sim[iu])
    mask = np.zeros_like(train_sim, dtype=bool)
    mask[iu[0][valid], iu[1][valid]] = True
    return mask


def eval_mask(train_sim: np.ndarray, test_sim: np.ndarray) -> np.ndarray:
    return base.upper_mask(train_sim, test_sim)


def angles_from_coords(coords: np.ndarray) -> np.ndarray:
    xy = coords - coords.mean(axis=0, keepdims=True)
    return np.mod(np.arctan2(xy[:, 1], xy[:, 0]), 2 * np.pi)


def circular_predict(train_sim: np.ndarray, angles: np.ndarray, fit_mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    delta = base.circular_distance(angles)
    d = base.pair_vectors(delta, fit_mask)
    X = np.column_stack([np.ones_like(d), np.cos(d), np.cos(2 * d)])
    y = base.pair_vectors(train_sim, fit_mask)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    Xall = np.column_stack(
        [np.ones(delta.size), np.cos(delta.ravel()), np.cos(2 * delta.ravel())]
    )
    pred = (Xall @ beta).reshape(delta.shape)
    np.fill_diagonal(pred, 1.0)
    return pred, beta


def fit_connected_circle(train_sim: np.ndarray) -> tuple[base.FitResult, float]:
    coords, floor = connected_coords(train_sim)
    angles = angles_from_coords(coords)
    mask = all_train_mask(train_sim)
    pred, beta = circular_predict(train_sim, angles, mask)
    return base.FitResult(
        "circular_connected",
        pred,
        {"angles": angles.tolist(), "beta": beta.tolist(), "affinity_floor": floor},
    ), floor


def fit_connected_euclidean(train_sim: np.ndarray) -> base.FitResult:
    coords, floor = connected_coords(train_sim)
    dist = base.pairwise_euclidean(coords)
    mask = all_train_mask(train_sim)
    beta = base.calibrate_poly(
        base.pair_vectors(dist, mask),
        base.pair_vectors(train_sim, mask),
        degree=2,
    )
    pred = base.apply_poly(dist.ravel(), beta).reshape(dist.shape)
    np.fill_diagonal(pred, 1.0)
    return base.FitResult(
        "euclidean_connected",
        pred,
        {"coords": coords.tolist(), "beta": beta.tolist(), "affinity_floor": floor},
    )


def optimize_circle(train_sim: np.ndarray, rng: np.random.Generator) -> base.FitResult:
    spectral, floor = fit_connected_circle(train_sim)
    init_angles = np.asarray(spectral.extra["angles"], dtype=float)
    mask = all_train_mask(train_sim)
    y = base.pair_vectors(train_sim, mask)
    n = len(train_sim)

    # Fix feature 0 at angle 0 to remove rotational non-identifiability.
    rel_init = np.angle(np.exp(1j * (init_angles[1:] - init_angles[0])))

    def unpack(x: np.ndarray) -> np.ndarray:
        angles = np.empty(n, dtype=float)
        angles[0] = 0.0
        angles[1:] = np.mod(x, 2 * np.pi)
        return angles

    def objective(x: np.ndarray) -> float:
        angles = unpack(x)
        pred, _ = circular_predict(train_sim, angles, mask)
        p = base.pair_vectors(pred, mask)
        # Mean squared training error; beta is solved analytically each iteration.
        return float(np.mean((y - p) ** 2))

    starts = [rel_init]
    if N_STARTS > 1:
        starts.append(rel_init + rng.normal(0.0, 0.35, size=len(rel_init)))
    for _ in range(2, N_STARTS):
        starts.append(rng.uniform(-np.pi, np.pi, size=len(rel_init)))

    best = None
    for start in starts:
        result = minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=[(-np.pi, np.pi)] * len(start),
            options={"maxiter": MAXITER, "ftol": 1e-10, "maxls": 30},
        )
        if best is None or float(result.fun) < float(best.fun):
            best = result

    angles = unpack(np.asarray(best.x, dtype=float))
    pred, beta = circular_predict(train_sim, angles, mask)
    return base.FitResult(
        "circular_optimized",
        pred,
        {
            "angles": angles.tolist(),
            "beta": beta.tolist(),
            "train_mse": float(best.fun),
            "optimizer_success": bool(best.success),
            "optimizer_message": str(best.message),
            "optimizer_nit": int(getattr(best, "nit", -1)),
            "affinity_floor": floor,
            "n_angular_parameters": n - 1,
        },
    )


def angle_stability(reference: np.ndarray, other: np.ndarray) -> float:
    return base.circular_stability(reference, other)


def score_fit(fit: base.FitResult, test_sim: np.ndarray, mask: np.ndarray) -> dict:
    return base.score_model(fit, test_sim, mask)


def run_for_feature_count(
    df,
    features: list[str],
    families,
    n_features: int,
    rng: np.random.Generator,
) -> dict:
    selected = features[:n_features]
    full_sim, _ = base.pairwise_nmi(df, selected)
    full_opt = optimize_circle(full_sim, rng)
    reference_angles = np.asarray(full_opt.extra["angles"], dtype=float)

    runs = []
    for split_id in range(N_SPLITS):
        train_idx, test_idx = base.family_split_indices(families, rng)
        train_sim, _ = base.pairwise_nmi(df.iloc[train_idx], selected)
        test_sim, _ = base.pairwise_nmi(df.iloc[test_idx], selected)
        mask = eval_mask(train_sim, test_sim)
        if int(mask.sum()) < 100:
            continue

        tree = base.fit_tree(train_sim, all_train_mask(train_sim))
        lowrank = base.fit_lowrank(train_sim, rank=2)
        euclid = fit_connected_euclidean(train_sim)
        circle_conn, floor = fit_connected_circle(train_sim)
        circle_opt = optimize_circle(train_sim, rng)

        fits = [tree, lowrank, euclid, circle_conn, circle_opt]
        scores = {fit.name: score_fit(fit, test_sim, mask) for fit in fits}
        opt_angles = np.asarray(circle_opt.extra["angles"], dtype=float)
        conn_angles = np.asarray(circle_conn.extra["angles"], dtype=float)
        runs.append(
            {
                "split": split_id,
                "n_train": int(len(train_idx)),
                "n_test": int(len(test_idx)),
                "n_eval_pairs": int(mask.sum()),
                "affinity_floor": float(floor),
                "scores": scores,
                "optimized_circle_stability": angle_stability(reference_angles, opt_angles),
                "connected_circle_vs_optimized_stability": angle_stability(conn_angles, opt_angles),
                "optimizer_success": bool(circle_opt.extra["optimizer_success"]),
                "optimizer_nit": int(circle_opt.extra["optimizer_nit"]),
            }
        )

    if not runs:
        raise RuntimeError(f"No valid family-held-out runs for {n_features} features")

    models = list(runs[0]["scores"])
    summary = {}
    for model in models:
        summary[model] = {}
        for metric in ("spearman", "pearson", "rmse", "mae"):
            vals = np.array([r["scores"][model][metric] for r in runs], dtype=float)
            summary[model][metric] = {
                "mean": float(vals.mean()),
                "sd": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0,
                "min": float(vals.min()),
                "max": float(vals.max()),
            }
    stability = np.array([r["optimized_circle_stability"] for r in runs], dtype=float)
    return {
        "n_features": n_features,
        "n_runs": len(runs),
        "runs": runs,
        "summary": summary,
        "optimized_circle_stability": {
            "mean": float(stability.mean()),
            "sd": float(stability.std(ddof=1)) if len(stability) > 1 else 0.0,
        },
    }


def decide(by_count: dict[str, dict]) -> tuple[str, list[str]]:
    reasons = []
    strong_tree_wins = 0
    competitive = 0
    for key, block in by_count.items():
        s = block["summary"]
        circ = s["circular_optimized"]["spearman"]["mean"]
        tree = s["tree"]["spearman"]["mean"]
        euclid = s["euclidean_connected"]["spearman"]["mean"]
        stab = block["optimized_circle_stability"]["mean"]
        reasons.append(
            f"{key} features: optimized circular Spearman={circ:.3f}, tree={tree:.3f}, "
            f"connected Euclidean={euclid:.3f}, circular stability={stab:.3f}."
        )
        if tree >= circ + 0.05:
            strong_tree_wins += 1
        if circ >= 0.15 and circ >= tree - 0.02:
            competitive += 1

    if competitive == len(by_count):
        return "PERIODIC_REMAINS_COMPETITIVE", reasons
    if strong_tree_wins == len(by_count):
        return "NONPERIODIC_REFRAME_STRENGTHENED", reasons
    return "MIXED_ROBUSTNESS", reasons


def write_report(results: dict) -> None:
    (HERE / "stage1b-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Stage-1B Robustness · Is the Circular Model a Strawman?",
        "",
        f"**Verdict:** `{results['verdict']}`",
        "",
        "This analysis gives the periodic hypothesis a more favorable/fair test before interpreting Stage 1's negative screen.",
        "",
        "## What changed",
        "",
        "- A tiny positive affinity floor forces the spectral graph to be connected.",
        "- A directly optimized circular model learns one angular coordinate per feature and refits a two-harmonic circular kernel.",
        "- Fits use only training-language associations; test-language associations are used only for evaluation.",
        "- Results are repeated at two feature counts under top-level Glottolog family hold-out.",
        "",
    ]
    for key, block in results["feature_counts"].items():
        lines += [
            f"## {key} features",
            "",
            "| Model | Spearman | Pearson | RMSE | MAE |",
            "|---|---:|---:|---:|---:|",
        ]
        for model in (
            "lowrank2",
            "euclidean_connected",
            "tree",
            "circular_connected",
            "circular_optimized",
        ):
            m = block["summary"][model]
            lines.append(
                f"| {model} | {m['spearman']['mean']:.3f} ± {m['spearman']['sd']:.3f} | "
                f"{m['pearson']['mean']:.3f} | {m['rmse']['mean']:.3f} | {m['mae']['mean']:.3f} |"
            )
        st = block["optimized_circle_stability"]
        lines += [
            "",
            f"Optimized circular-order stability: {st['mean']:.3f} ± {st['sd']:.3f}",
            "",
        ]

    lines += ["## Automated interpretation", ""]
    lines.extend(f"- {r}" for r in results["verdict_reasons"])
    lines += [
        "",
        "## Claim boundary",
        "",
        "A negative verdict here strengthens—but does not complete—the case against a simple global periodic geometry. Geographic blocking, stronger phylogenetic treatment, model-capacity analysis, and replication remain necessary before manuscript-level rejection. A positive verdict would only reopen the periodic hypothesis; it would not establish a chemical-style periodic table.",
        "",
    ]
    (HERE / "STAGE1B_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rng = np.random.default_rng(SEED)
    df, features, families = base.load_data()
    if max(FEATURE_COUNTS) > len(features):
        raise RuntimeError(f"Need {max(FEATURE_COUNTS)} features but only {len(features)} available")

    by_count = {}
    for count in FEATURE_COUNTS:
        by_count[str(count)] = run_for_feature_count(df, features, families, count, rng)
    status, reasons = decide(by_count)
    results = {
        "seed": SEED,
        "dataset": base.TLI_URL,
        "glottolog": base.GLOTTOLOG_URL,
        "feature_counts": by_count,
        "verdict": status,
        "verdict_reasons": reasons,
        "limitations": [
            "Only five family-held-out splits per feature-count setting are used in this robustness screen.",
            "Direct angular optimization is non-convex and uses two starts.",
            "Model capacities are still not formally matched by information criteria.",
            "Geographic blocking and full phylogenetic covariance are not included.",
            "The target remains pairwise feature NMI rather than individual-language feature prediction.",
        ],
    }
    write_report(results)
    print(json.dumps({"verdict": status, "reasons": reasons}, indent=2))


if __name__ == "__main__":
    main()
