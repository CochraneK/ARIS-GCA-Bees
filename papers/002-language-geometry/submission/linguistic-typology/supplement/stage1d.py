#!/usr/bin/env python3
"""Stage-1D: standards-inspired circular-Robinson sensitivity.

Armstrong, Guzmán & Sing-Long (2021) show that a dissimilarity matrix is circular
Robinson iff, under a compatible cyclic order, every row read around the circle is
unimodal. They also note that every linear Robinson matrix is circular Robinson, so
circular-Robinson compatibility alone cannot establish genuinely periodic geometry.

This screen therefore evaluates TWO properties on held-out language families:

1. circular-Robinson row-unimodality deviation: how far the TEST dissimilarity
   matrix is from row-wise unimodality under an order learned from TRAIN languages;
2. closure support: whether the wrap-around edge of the learned circular order is
   as similar in TEST data as ordinary adjacent pairs. A line-like order can have
   strong internal adjacency but a weak closure edge.

We compare:
- a directly optimized circular order learned on train languages;
- a hierarchical-tree leaf order learned on train languages;
- random permutations as a null.

This is a standards-inspired sensitivity analysis, not an implementation of the
exact strict circular-seriation recognition algorithm for noisy matrices.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import squareform

import stage1 as base
import stage1b as robust

HERE = Path(__file__).resolve().parent
SEED = 2029
FEATURE_COUNTS = (40, 60)
N_SPLITS = 6
N_RANDOM_ORDERS = 80
MAX_SPLIT_ATTEMPTS = 36
MIN_EVAL_PAIRS = 100
EPS = 1e-12


def dense_dissimilarity(sim: np.ndarray) -> np.ndarray:
    """Convert NMI similarity to finite dissimilarity, using train/test-local median fill."""
    A = np.asarray(sim, dtype=float).copy()
    finite = np.isfinite(A)
    off = finite & ~np.eye(len(A), dtype=bool)
    fill = float(np.nanmedian(A[off])) if np.any(off) else 0.0
    A[~finite] = fill
    A = np.clip(A, 0.0, 1.0)
    np.fill_diagonal(A, 1.0)
    D = 1.0 - A
    np.fill_diagonal(D, 0.0)
    return D


def optimized_circular_order(train_sim: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    fit = robust.optimize_circle(train_sim, rng)
    angles = np.asarray(fit.extra["angles"], dtype=float)
    return np.argsort(angles)


def tree_order(train_sim: np.ndarray) -> np.ndarray:
    D = dense_dissimilarity(train_sim)
    Z = linkage(squareform(D, checks=False), method="average")
    return np.asarray(leaves_list(Z), dtype=int)


def row_unimodality_deviation(sequence: np.ndarray) -> float:
    """Minimum normalized adjacent monotonicity violation over all possible modes.

    For a circular-Robinson-compatible order, reading a row from the focal object
    clockwise around the cycle should rise to a mode and then fall. Zero is exact
    row-wise unimodality (ties allowed); larger values indicate stronger violations.
    """
    x = np.asarray(sequence, dtype=float)
    if len(x) <= 3:
        return 0.0
    total_variation = float(np.sum(np.abs(np.diff(x)))) + EPS
    best = np.inf
    for mode in range(1, len(x) - 1):
        left = x[: mode + 1]
        right = x[mode:]
        # left should be non-decreasing: penalize drops
        left_violation = float(np.sum(np.maximum(0.0, left[:-1] - left[1:])))
        # right should be non-increasing: penalize rises
        right_violation = float(np.sum(np.maximum(0.0, right[1:] - right[:-1])))
        best = min(best, left_violation + right_violation)
    return float(best / total_variation)


def circular_robinson_score(D: np.ndarray, order: np.ndarray) -> dict:
    ordered = D[np.ix_(order, order)]
    row_scores = []
    n = len(order)
    for i in range(n):
        # Start at the focal object and walk clockwise once around the cycle.
        seq = np.array([ordered[i, (i + j) % n] for j in range(n)], dtype=float)
        row_scores.append(row_unimodality_deviation(seq))
    rows = np.asarray(row_scores, dtype=float)
    return {
        "mean_violation": float(rows.mean()),
        "median_violation": float(np.median(rows)),
        "p90_violation": float(np.quantile(rows, 0.90)),
        "exact_unimodal_fraction": float(np.mean(rows <= 1e-10)),
    }


def closure_score(sim: np.ndarray, order: np.ndarray) -> dict:
    S = np.asarray(sim, dtype=float)
    adjacent = []
    for a, b in zip(order[:-1], order[1:]):
        value = S[a, b]
        if np.isfinite(value):
            adjacent.append(float(value))
    closure = float(S[order[-1], order[0]]) if np.isfinite(S[order[-1], order[0]]) else np.nan
    internal = np.asarray(adjacent, dtype=float)
    internal_mean = float(np.mean(internal)) if len(internal) else np.nan
    internal_median = float(np.median(internal)) if len(internal) else np.nan
    ratio = float(closure / (internal_median + EPS)) if np.isfinite(closure) and np.isfinite(internal_median) else np.nan
    return {
        "closure_similarity": closure if np.isfinite(closure) else None,
        "internal_adjacent_mean": internal_mean if np.isfinite(internal_mean) else None,
        "internal_adjacent_median": internal_median if np.isfinite(internal_median) else None,
        "closure_to_internal_median_ratio": ratio if np.isfinite(ratio) else None,
    }


def evaluate_order(test_sim: np.ndarray, order: np.ndarray) -> dict:
    D = dense_dissimilarity(test_sim)
    return {
        "robinson": circular_robinson_score(D, order),
        "closure": closure_score(test_sim, order),
    }


def random_null(test_sim: np.ndarray, rng: np.random.Generator) -> dict:
    n = len(test_sim)
    violations = []
    closure_ratios = []
    for _ in range(N_RANDOM_ORDERS):
        order = rng.permutation(n)
        ev = evaluate_order(test_sim, order)
        violations.append(ev["robinson"]["mean_violation"])
        ratio = ev["closure"]["closure_to_internal_median_ratio"]
        if ratio is not None and np.isfinite(ratio):
            closure_ratios.append(float(ratio))
    v = np.asarray(violations, dtype=float)
    c = np.asarray(closure_ratios, dtype=float)
    return {
        "mean_violation_mean": float(v.mean()),
        "mean_violation_sd": float(v.std(ddof=1)),
        "mean_violation_p05": float(np.quantile(v, 0.05)),
        "closure_ratio_mean": float(c.mean()) if len(c) else None,
        "closure_ratio_p95": float(np.quantile(c, 0.95)) if len(c) else None,
    }


def run_count(df, features: list[str], families, count: int, rng: np.random.Generator) -> dict:
    selected = features[:count]
    runs = []
    attempts = 0
    while len(runs) < N_SPLITS and attempts < MAX_SPLIT_ATTEMPTS:
        attempts += 1
        train_idx, test_idx = base.family_split_indices(families, rng)
        train_sim, _ = base.pairwise_nmi(df.iloc[train_idx], selected)
        test_sim, _ = base.pairwise_nmi(df.iloc[test_idx], selected)
        mask = base.upper_mask(train_sim, test_sim)
        if int(mask.sum()) < MIN_EVAL_PAIRS:
            continue

        circle_order = optimized_circular_order(train_sim, rng)
        hierarchy_order = tree_order(train_sim)
        circle_eval = evaluate_order(test_sim, circle_order)
        tree_eval = evaluate_order(test_sim, hierarchy_order)
        null_eval = random_null(test_sim, rng)

        runs.append(
            {
                "split": len(runs),
                "attempt": attempts,
                "n_train": int(len(train_idx)),
                "n_test": int(len(test_idx)),
                "n_eval_pairs": int(mask.sum()),
                "circular_order": circle_eval,
                "tree_order": tree_eval,
                "random_null": null_eval,
            }
        )

    if len(runs) < N_SPLITS:
        raise RuntimeError(
            f"Only {len(runs)} valid splits for {count} features after {attempts} attempts; "
            f"required {N_SPLITS}."
        )

    def collect(path: tuple[str, ...]) -> np.ndarray:
        vals = []
        for run in runs:
            cur = run
            for key in path:
                cur = cur[key]
            if cur is not None and np.isfinite(cur):
                vals.append(float(cur))
        return np.asarray(vals, dtype=float)

    def stat(arr: np.ndarray) -> dict:
        return {
            "mean": float(arr.mean()),
            "sd": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
            "min": float(arr.min()),
            "max": float(arr.max()),
        }

    circle_v = collect(("circular_order", "robinson", "mean_violation"))
    tree_v = collect(("tree_order", "robinson", "mean_violation"))
    null_v = collect(("random_null", "mean_violation_mean"))
    circle_c = collect(("circular_order", "closure", "closure_to_internal_median_ratio"))
    tree_c = collect(("tree_order", "closure", "closure_to_internal_median_ratio"))

    return {
        "n_features": count,
        "n_valid_runs": len(runs),
        "n_attempts": attempts,
        "runs": runs,
        "summary": {
            "circular_mean_violation": stat(circle_v),
            "tree_mean_violation": stat(tree_v),
            "random_mean_violation": stat(null_v),
            "circular_closure_ratio": stat(circle_c),
            "tree_closure_ratio": stat(tree_c),
            "circle_minus_tree_violation": stat(circle_v - tree_v),
        },
    }


def decide(blocks: dict[str, dict]) -> tuple[str, list[str]]:
    reasons = []
    distinctive = 0
    compatible_only = 0
    unsupported = 0

    for key, block in blocks.items():
        s = block["summary"]
        cv = s["circular_mean_violation"]["mean"]
        tv = s["tree_mean_violation"]["mean"]
        nv = s["random_mean_violation"]["mean"]
        cc = s["circular_closure_ratio"]["mean"]
        reasons.append(
            f"{key} features: circular violation={cv:.3f}, tree={tv:.3f}, random={nv:.3f}; "
            f"circular closure ratio={cc:.3f}."
        )
        beats_random = cv <= nv * 0.80
        beats_tree = cv <= tv - 0.03
        closes = cc >= 0.80
        if beats_random and beats_tree and closes:
            distinctive += 1
        elif beats_random and closes:
            compatible_only += 1
        else:
            unsupported += 1

    if distinctive == len(blocks):
        return "CIRCULAR_STRUCTURE_DISTINCT", reasons
    if distinctive + compatible_only == len(blocks) and unsupported == 0:
        return "CIRCULAR_COMPATIBLE_NOT_DISTINCT", reasons
    if unsupported == len(blocks):
        return "CIRCULAR_ROBINSON_NOT_SUPPORTED", reasons
    return "MIXED_CIRCULAR_ROBINSON", reasons


def write_report(results: dict) -> None:
    (HERE / "stage1d-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Stage-1D · Held-out Circular-Robinson Sensitivity",
        "",
        f"**Verdict:** `{results['verdict']}`",
        "",
        "This test is inspired by the circular-Robinson characterization in Armstrong, Guzmán & Sing-Long (2021): under a compatible cyclic order, each dissimilarity row read around the cycle is unimodal. Because every linear Robinson matrix is also circular Robinson, the report additionally checks whether the wrap-around closure edge is actually supported and compares against a hierarchical-tree order.",
        "",
        "Lower unimodality violation is better. A closure ratio near 1 means the wrap-around pair is about as similar as a typical internal adjacent pair.",
        "",
    ]
    for key, block in results["feature_counts"].items():
        s = block["summary"]
        lines += [
            f"## {key} features",
            "",
            f"Valid family-held-out runs: {block['n_valid_runs']}/{block['n_attempts']} attempts",
            "",
            "| Diagnostic | Circular order | Tree order | Random order |",
            "|---|---:|---:|---:|",
            f"| Mean row-unimodality violation ↓ | {s['circular_mean_violation']['mean']:.3f} ± {s['circular_mean_violation']['sd']:.3f} | {s['tree_mean_violation']['mean']:.3f} ± {s['tree_mean_violation']['sd']:.3f} | {s['random_mean_violation']['mean']:.3f} ± {s['random_mean_violation']['sd']:.3f} |",
            f"| Closure / internal-adjacent ratio | {s['circular_closure_ratio']['mean']:.3f} ± {s['circular_closure_ratio']['sd']:.3f} | {s['tree_closure_ratio']['mean']:.3f} ± {s['tree_closure_ratio']['sd']:.3f} | — |",
            "",
        ]
    lines += ["## Automated interpretation", ""]
    lines.extend(f"- {x}" for x in results["verdict_reasons"])
    lines += [
        "",
        "## Claim boundary",
        "",
        "This is a noisy-data sensitivity based on the row-unimodality characterization, not an exact strict-circular-Robinson recognition proof. Passing it cannot by itself establish a periodic language system because linear Robinson structure is a subset of circular Robinson structure. Failing it would be stronger evidence against the specific circular-order interpretation used here.",
        "",
    ]
    (HERE / "STAGE1D_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rng = np.random.default_rng(SEED)
    df, features, families = base.load_data()
    blocks = {}
    for count in FEATURE_COUNTS:
        blocks[str(count)] = run_count(df, features, families, count, rng)
    verdict, reasons = decide(blocks)
    results = {
        "seed": SEED,
        "dataset": base.TLI_URL,
        "feature_counts": blocks,
        "verdict": verdict,
        "verdict_reasons": reasons,
        "method_note": "Standards-inspired noisy-data diagnostic using the circular-Robinson row-unimodality characterization; not exact strict-seriation recognition.",
        "limitations": [
            "The optimized circular order is learned by the Stage-1B objective, not by the exact strict circular-seriation algorithm.",
            "The row-violation score is a continuous noisy-data deviation measure introduced for this sensitivity analysis.",
            "Linear Robinson structure can satisfy circular Robinson, so compatibility is not proof of genuinely periodic geometry.",
            "Geographic and full phylogenetic controls remain pending.",
        ],
    }
    write_report(results)
    print(json.dumps({"verdict": verdict, "reasons": reasons}, indent=2))


if __name__ == "__main__":
    main()
