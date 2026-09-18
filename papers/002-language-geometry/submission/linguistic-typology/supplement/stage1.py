#!/usr/bin/env python3
"""Stage-1 model competition for the analysis repository language periodic-system candidate.

This is a screening analysis, not a confirmatory paper analysis. It asks whether a
low-capacity circular representation of feature-association structure predicts the
same associations in held-out languages better than simple non-periodic alternatives.

Models are fit only to the TRAIN-language feature-association matrix. They predict
the TEST-language feature-association matrix. Two split regimes are used:
1) random language splits (optimistic screening),
2) top-level Glottolog family-held-out splits (harder genealogy-aware screening).

The circular model is intentionally simple: a 2-D spectral embedding of the train
feature-similarity graph is converted to one angle per feature, then train NMI is
regressed on the first two cosine harmonics of wrapped angular distance.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import cophenet, linkage
from scipy.spatial.distance import squareform
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path
from scipy.stats import pearsonr, spearmanr
from sklearn.manifold import SpectralEmbedding
from sklearn.metrics import normalized_mutual_info_score

HERE = Path(__file__).resolve().parent
TLI_URL = (
    "https://raw.githubusercontent.com/annagraff/crossling-curated/main/"
    "curated_data/TLI/statisticalTLI/full/"
    "statisticalTLI_full_densified_small.csv"
)
GLOTTOLOG_URL = (
    "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/"
    "cldf/languages.csv"
)

SEED = 2026
N_FEATURES = 60
MIN_FEATURE_OBS = 180
MAX_CARDINALITY = 15
MIN_PAIR_OBS = 60
N_RANDOM_SPLITS = 8
N_FAMILY_SPLITS = 8
TEST_FRACTION = 0.30
GRAPH_K = 6
EPS = 1e-8


@dataclass
class FitResult:
    name: str
    prediction: np.ndarray
    extra: dict


def load_data() -> tuple[pd.DataFrame, list[str], pd.Series]:
    df = pd.read_csv(
        TLI_URL,
        dtype=str,
        na_values=["?", "NA", "N/A", ""],
        keep_default_na=True,
    )
    df = df.loc[:, ~df.columns.astype(str).str.lower().str.startswith("unnamed")]
    if "glottocode" not in df.columns:
        raise RuntimeError("Expected glottocode column in TLI dataset")

    candidates = []
    for c in df.columns:
        if c == "glottocode":
            continue
        obs = df[c].dropna()
        nunique = obs.nunique()
        if len(obs) >= MIN_FEATURE_OBS and 2 <= nunique <= MAX_CARDINALITY:
            candidates.append(c)

    # Rank by coverage, then prefer lower-cardinality variables to reduce noisy NMI.
    candidates.sort(
        key=lambda c: (df[c].notna().mean(), -df[c].dropna().nunique()),
        reverse=True,
    )
    features = candidates[:N_FEATURES]
    if len(features) < 20:
        raise RuntimeError(f"Too few usable features: {len(features)}")

    glotto = pd.read_csv(GLOTTOLOG_URL, dtype=str, low_memory=False)
    family_map = glotto.set_index("ID")["Family_ID"].to_dict()
    families = []
    for code in df["glottocode"].astype(str):
        fam = family_map.get(code)
        if fam is None or pd.isna(fam) or str(fam).strip() == "":
            # Isolates/non-mapped entries become their own groups rather than one giant NA family.
            fam = f"isolate::{code}"
        families.append(str(fam))
    return df, features, pd.Series(families, index=df.index, name="family")


def pairwise_nmi(frame: pd.DataFrame, features: list[str]) -> tuple[np.ndarray, np.ndarray]:
    n = len(features)
    sim = np.eye(n, dtype=float)
    support = np.zeros((n, n), dtype=int)
    for i in range(n):
        support[i, i] = int(frame[features[i]].notna().sum())
        for j in range(i + 1, n):
            pair = frame[[features[i], features[j]]].dropna()
            m = len(pair)
            support[i, j] = support[j, i] = m
            if m < MIN_PAIR_OBS:
                score = np.nan
            else:
                score = float(
                    normalized_mutual_info_score(
                        pair.iloc[:, 0].astype(str),
                        pair.iloc[:, 1].astype(str),
                        average_method="arithmetic",
                    )
                )
            sim[i, j] = sim[j, i] = score
    return sim, support


def upper_mask(train_sim: np.ndarray, test_sim: np.ndarray) -> np.ndarray:
    iu = np.triu_indices_from(train_sim, k=1)
    valid = np.isfinite(train_sim[iu]) & np.isfinite(test_sim[iu])
    mask = np.zeros_like(train_sim, dtype=bool)
    mask[iu[0][valid], iu[1][valid]] = True
    return mask


def pair_vectors(matrix: np.ndarray, mask: np.ndarray) -> np.ndarray:
    return matrix[mask]


def calibrate_poly(distance: np.ndarray, y: np.ndarray, degree: int = 2) -> np.ndarray:
    cols = [np.ones_like(distance)] + [distance ** k for k in range(1, degree + 1)]
    X = np.column_stack(cols)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def apply_poly(distance: np.ndarray, beta: np.ndarray) -> np.ndarray:
    cols = [np.ones_like(distance)] + [distance ** k for k in range(1, len(beta))]
    return np.column_stack(cols) @ beta


def safe_affinity(sim: np.ndarray) -> np.ndarray:
    out = np.array(sim, dtype=float, copy=True)
    finite = np.isfinite(out)
    fill = float(np.nanmedian(out[finite])) if finite.any() else 0.0
    out[~finite] = fill
    out = np.clip(out, 0.0, None)
    np.fill_diagonal(out, max(1.0, float(np.max(out))))
    return out


def pairwise_euclidean(coords: np.ndarray) -> np.ndarray:
    diff = coords[:, None, :] - coords[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=2))


def circular_distance(angles: np.ndarray) -> np.ndarray:
    delta = np.abs(angles[:, None] - angles[None, :])
    return np.minimum(delta, 2 * np.pi - delta)


def fit_null(train_sim: np.ndarray, mask: np.ndarray) -> FitResult:
    y = pair_vectors(train_sim, mask)
    pred = np.full_like(train_sim, float(np.mean(y)))
    np.fill_diagonal(pred, 1.0)
    return FitResult("null", pred, {"mean": float(np.mean(y))})


def spectral_coords(train_sim: np.ndarray) -> np.ndarray:
    affinity = safe_affinity(train_sim)
    model = SpectralEmbedding(
        n_components=2,
        affinity="precomputed",
        random_state=SEED,
        eigen_solver="arpack",
    )
    return model.fit_transform(affinity)


def fit_euclidean(train_sim: np.ndarray, mask: np.ndarray) -> FitResult:
    coords = spectral_coords(train_sim)
    dist = pairwise_euclidean(coords)
    beta = calibrate_poly(pair_vectors(dist, mask), pair_vectors(train_sim, mask), degree=2)
    pred = apply_poly(dist.ravel(), beta).reshape(dist.shape)
    np.fill_diagonal(pred, 1.0)
    return FitResult(
        "euclidean2d",
        pred,
        {"beta": beta.tolist(), "coords": coords.tolist()},
    )


def fit_circular(train_sim: np.ndarray, mask: np.ndarray) -> FitResult:
    coords = spectral_coords(train_sim)
    center = coords.mean(axis=0, keepdims=True)
    xy = coords - center
    angles = np.mod(np.arctan2(xy[:, 1], xy[:, 0]), 2 * np.pi)

    # Symmetric periodic regression using first two cosine harmonics.
    delta = circular_distance(angles)
    d = pair_vectors(delta, mask)
    X = np.column_stack([np.ones_like(d), np.cos(d), np.cos(2 * d)])
    y = pair_vectors(train_sim, mask)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)

    Xall = np.column_stack(
        [np.ones(delta.size), np.cos(delta.ravel()), np.cos(2 * delta.ravel())]
    )
    pred = (Xall @ beta).reshape(delta.shape)
    np.fill_diagonal(pred, 1.0)
    return FitResult(
        "circular",
        pred,
        {"beta": beta.tolist(), "angles": angles.tolist()},
    )


def fit_lowrank(train_sim: np.ndarray, rank: int = 2) -> FitResult:
    A = safe_affinity(train_sim)
    mean_off = (A.sum() - np.trace(A)) / (A.size - len(A))
    centered = A - mean_off
    vals, vecs = np.linalg.eigh(centered)
    idx = np.argsort(np.abs(vals))[::-1][:rank]
    recon = (vecs[:, idx] * vals[idx]) @ vecs[:, idx].T + mean_off
    np.fill_diagonal(recon, 1.0)
    return FitResult(
        f"lowrank{rank}",
        recon,
        {"eigenvalues": vals[idx].tolist()},
    )


def fit_tree(train_sim: np.ndarray, mask: np.ndarray) -> FitResult:
    A = safe_affinity(train_sim)
    dist = np.clip(1.0 - A, 0.0, None)
    np.fill_diagonal(dist, 0.0)
    condensed = squareform(dist, checks=False)
    Z = linkage(condensed, method="average")
    coph = squareform(cophenet(Z))
    beta = calibrate_poly(pair_vectors(coph, mask), pair_vectors(train_sim, mask), degree=2)
    pred = apply_poly(coph.ravel(), beta).reshape(coph.shape)
    np.fill_diagonal(pred, 1.0)
    return FitResult("tree", pred, {"beta": beta.tolist()})


def fit_graph(train_sim: np.ndarray, mask: np.ndarray) -> FitResult:
    A = safe_affinity(train_sim)
    n = len(A)
    dist = np.clip(1.0 - A, 0.0, None)
    np.fill_diagonal(dist, 0.0)

    graph = np.full((n, n), np.inf, dtype=float)
    np.fill_diagonal(graph, 0.0)
    for i in range(n):
        neigh = np.argsort(dist[i])[1 : GRAPH_K + 1]
        for j in neigh:
            w = max(float(dist[i, j]), EPS)
            graph[i, j] = min(graph[i, j], w)
            graph[j, i] = min(graph[j, i], w)

    finite_edges = np.isfinite(graph)
    sparse = csr_matrix(np.where(finite_edges, graph, 0.0))
    sp = shortest_path(sparse, directed=False, unweighted=False)
    finite = np.isfinite(sp)
    if not finite.all():
        max_finite = float(sp[finite].max()) if finite.any() else 1.0
        sp[~finite] = 1.5 * max_finite

    beta = calibrate_poly(pair_vectors(sp, mask), pair_vectors(train_sim, mask), degree=2)
    pred = apply_poly(sp.ravel(), beta).reshape(sp.shape)
    np.fill_diagonal(pred, 1.0)
    return FitResult("graph", pred, {"beta": beta.tolist(), "k": GRAPH_K})


def score_model(result: FitResult, test_sim: np.ndarray, mask: np.ndarray) -> dict:
    y = pair_vectors(test_sim, mask)
    p = pair_vectors(result.prediction, mask)
    p = np.asarray(p, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(y) < 3:
        return {"n_pairs": int(len(y)), "pearson": None, "spearman": None, "rmse": None, "mae": None}

    pear = float(pearsonr(y, p).statistic) if np.std(p) > EPS and np.std(y) > EPS else 0.0
    spear = float(spearmanr(y, p).statistic) if np.std(p) > EPS and np.std(y) > EPS else 0.0
    rmse = float(np.sqrt(np.mean((y - p) ** 2)))
    mae = float(np.mean(np.abs(y - p)))
    return {
        "n_pairs": int(len(y)),
        "pearson": pear,
        "spearman": spear,
        "rmse": rmse,
        "mae": mae,
    }


def fit_all(train_sim: np.ndarray, test_sim: np.ndarray) -> tuple[dict, np.ndarray | None]:
    mask = upper_mask(train_sim, test_sim)
    if mask.sum() < 100:
        raise RuntimeError(f"Too few common train/test feature pairs: {mask.sum()}")

    fits = [
        fit_null(train_sim, mask),
        fit_lowrank(train_sim, rank=2),
        fit_euclidean(train_sim, mask),
        fit_tree(train_sim, mask),
        fit_graph(train_sim, mask),
        fit_circular(train_sim, mask),
    ]
    scores = {f.name: score_model(f, test_sim, mask) for f in fits}
    circular = next(f for f in fits if f.name == "circular")
    return scores, np.asarray(circular.extra["angles"], dtype=float)


def random_split_indices(n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    perm = rng.permutation(n)
    n_test = max(1, int(round(TEST_FRACTION * n)))
    test = np.sort(perm[:n_test])
    train = np.sort(perm[n_test:])
    return train, test


def family_split_indices(families: pd.Series, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    groups = {}
    for idx, fam in families.items():
        groups.setdefault(str(fam), []).append(int(idx))
    keys = list(groups)
    rng.shuffle(keys)
    target = max(1, int(round(TEST_FRACTION * len(families))))
    test_idx: list[int] = []
    for key in keys:
        if len(test_idx) >= target and test_idx:
            break
        test_idx.extend(groups[key])
    test_set = set(test_idx)
    train_idx = [int(i) for i in families.index if int(i) not in test_set]
    return np.array(sorted(train_idx)), np.array(sorted(test_idx))


def wrapped_distance_vector(angles: np.ndarray) -> np.ndarray:
    d = circular_distance(angles)
    iu = np.triu_indices_from(d, k=1)
    return d[iu]


def circular_stability(reference_angles: np.ndarray, split_angles: np.ndarray) -> float:
    # Rotation/reflection invariant because pairwise wrapped distances are used.
    a = wrapped_distance_vector(reference_angles)
    b = wrapped_distance_vector(split_angles)
    if np.std(a) < EPS or np.std(b) < EPS:
        return 0.0
    return float(spearmanr(a, b).statistic)


def summarize_runs(runs: list[dict]) -> dict:
    names = sorted(runs[0]["scores"].keys())
    out = {}
    for name in names:
        vals = {m: [] for m in ("pearson", "spearman", "rmse", "mae")}
        for run in runs:
            for metric in vals:
                value = run["scores"][name][metric]
                if value is not None and math.isfinite(value):
                    vals[metric].append(float(value))
        out[name] = {}
        for metric, arr in vals.items():
            x = np.array(arr, dtype=float)
            out[name][metric] = {
                "mean": float(x.mean()) if len(x) else None,
                "sd": float(x.std(ddof=1)) if len(x) > 1 else 0.0 if len(x) else None,
                "min": float(x.min()) if len(x) else None,
                "max": float(x.max()) if len(x) else None,
            }
    stab = np.array([r["circular_stability"] for r in runs], dtype=float)
    return {
        "models": out,
        "circular_stability": {
            "mean": float(stab.mean()),
            "sd": float(stab.std(ddof=1)) if len(stab) > 1 else 0.0,
            "min": float(stab.min()),
            "max": float(stab.max()),
        },
    }


def verdict(random_summary: dict, family_summary: dict) -> tuple[str, list[str]]:
    rs = random_summary["models"]
    fs = family_summary["models"]
    circ_r = rs["circular"]["spearman"]["mean"]
    circ_f = fs["circular"]["spearman"]["mean"]
    null_f = fs["null"]["spearman"]["mean"]
    competitors = ["lowrank2", "euclidean2d", "tree", "graph"]
    best_comp_f = max(fs[m]["spearman"]["mean"] for m in competitors)
    stability_f = family_summary["circular_stability"]["mean"]

    reasons = [
        f"Circular Spearman: random={circ_r:.3f}, family-held-out={circ_f:.3f}.",
        f"Best non-periodic family-held-out Spearman={best_comp_f:.3f}; null={null_f:.3f}.",
        f"Mean circular-order stability under family-held-out resampling={stability_f:.3f}.",
    ]

    # This 0.35 stability threshold belongs only to the original Stage-1 global
    # screening verdict. Stage 1C later uses a separate, stricter predeclared
    # local-domain criterion with stability >= 0.40; the two gates are not interchangeable.
    if circ_f >= 0.15 and circ_f >= best_comp_f - 0.03 and stability_f >= 0.35:
        return "GO_PERIODIC_SCREEN", reasons
    if best_comp_f >= max(0.15, circ_f + 0.05):
        return "REFRAME_NONPERIODIC_GEOMETRY", reasons
    if max(best_comp_f, circ_f) < 0.10:
        return "WEAK_GENERALIZATION", reasons
    return "MIXED_STAGE1", reasons


def run_regime(
    df: pd.DataFrame,
    features: list[str],
    families: pd.Series,
    rng: np.random.Generator,
    mode: str,
    n_splits: int,
    reference_angles: np.ndarray,
) -> list[dict]:
    runs = []
    for split_id in range(n_splits):
        if mode == "random":
            train_idx, test_idx = random_split_indices(len(df), rng)
        elif mode == "family":
            train_idx, test_idx = family_split_indices(families, rng)
        else:
            raise ValueError(mode)

        train_sim, _ = pairwise_nmi(df.iloc[train_idx], features)
        test_sim, _ = pairwise_nmi(df.iloc[test_idx], features)
        scores, angles = fit_all(train_sim, test_sim)
        runs.append(
            {
                "split": split_id,
                "n_train": int(len(train_idx)),
                "n_test": int(len(test_idx)),
                "scores": scores,
                "circular_stability": circular_stability(reference_angles, angles),
            }
        )
    return runs


def write_report(results: dict) -> None:
    (HERE / "stage1-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    def metric_row(summary: dict, model: str) -> str:
        m = summary["models"][model]
        return (
            f"| {model} | {m['spearman']['mean']:.3f} | {m['pearson']['mean']:.3f} | "
            f"{m['rmse']['mean']:.3f} | {m['mae']['mean']:.3f} |"
        )

    r = results["random_summary"]
    f = results["family_summary"]
    lines = [
        "# Stage-1 Report · Periodic vs Non-Periodic Geometry",
        "",
        f"**Verdict:** `{results['verdict']}`",
        "",
        "This is a **screening model competition**, not a confirmatory periodicity claim.",
        "",
        "## Data and target",
        "",
        f"Languages: {results['n_languages']} · features: {results['n_features']}",
        "",
        "Each model is fit to the feature-feature NMI matrix computed in training languages and predicts the independently computed NMI matrix in held-out languages.",
        "",
        "## Random language splits",
        "",
        "| Model | Spearman | Pearson | RMSE | MAE |",
        "|---|---:|---:|---:|---:|",
    ]
    for model in ("null", "lowrank2", "euclidean2d", "tree", "graph", "circular"):
        lines.append(metric_row(r, model))
    lines += [
        "",
        f"Circular-order stability vs full-data reference: {r['circular_stability']['mean']:.3f} ± {r['circular_stability']['sd']:.3f}",
        "",
        "## Family-held-out splits",
        "",
        "Entire top-level Glottolog families are assigned to test when sampled, reducing direct genealogical leakage.",
        "",
        "| Model | Spearman | Pearson | RMSE | MAE |",
        "|---|---:|---:|---:|---:|",
    ]
    for model in ("null", "lowrank2", "euclidean2d", "tree", "graph", "circular"):
        lines.append(metric_row(f, model))
    lines += [
        "",
        f"Circular-order stability vs full-data reference: {f['circular_stability']['mean']:.3f} ± {f['circular_stability']['sd']:.3f}",
        "",
        "## Automated interpretation",
        "",
    ]
    lines.extend(f"- {x}" for x in results["verdict_reasons"])
    lines += [
        "",
        "## Claim boundary",
        "",
        "A circular model performing well here would show that a simple periodic representation captures reproducible association structure. It would still **not** establish a chemical-style periodic table, linguistic atoms, causal universals, or independence from geography. A confirmatory paper would need capacity checks, geographic controls, source-domain replications, stronger family/phylogenetic treatment, and an independent ARIS review.",
        "",
        "## Prior-art boundary",
        "",
        "Persistent H1 loops are not treated as novelty because Port et al. (2018, 2022) already applied persistent topology to syntactic-parameter data. The intended novelty is explicit predictive model competition for the periodic-table hypothesis on modern curated global data.",
        "",
    ]
    (HERE / "STAGE1_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rng = np.random.default_rng(SEED)
    df, features, families = load_data()

    full_sim, _ = pairwise_nmi(df, features)
    full_mask = np.isfinite(full_sim)
    np.fill_diagonal(full_mask, False)
    reference = fit_circular(full_sim, full_mask)
    reference_angles = np.asarray(reference.extra["angles"], dtype=float)

    random_runs = run_regime(
        df, features, families, rng, "random", N_RANDOM_SPLITS, reference_angles
    )
    family_runs = run_regime(
        df, features, families, rng, "family", N_FAMILY_SPLITS, reference_angles
    )
    random_summary = summarize_runs(random_runs)
    family_summary = summarize_runs(family_runs)
    status, reasons = verdict(random_summary, family_summary)

    results = {
        "dataset": TLI_URL,
        "glottolog": GLOTTOLOG_URL,
        "seed": SEED,
        "n_languages": int(len(df)),
        "n_features": int(len(features)),
        "features": features,
        "random_runs": random_runs,
        "family_runs": family_runs,
        "random_summary": random_summary,
        "family_summary": family_summary,
        "verdict": status,
        "verdict_reasons": reasons,
        "limitations": [
            "This screen predicts pairwise NMI, not individual language feature values.",
            "Family_ID blocking is a coarse genealogy control, not a full phylogenetic covariance model.",
            "Geographic diffusion is not yet controlled.",
            "Model capacities are intentionally simple but not formally matched by information criteria.",
            "Feature selection favors coverage and bounded cardinality; confirmatory work must test robustness.",
        ],
    }
    write_report(results)
    print(json.dumps({"verdict": status, "reasons": reasons}, indent=2))


if __name__ == "__main__":
    main()
