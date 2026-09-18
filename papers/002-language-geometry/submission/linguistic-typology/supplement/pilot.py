#!/usr/bin/env python3
"""Stage-0 feasibility test for the analysis repository language periodic-system idea.

This pilot does NOT test periodicity directly. It asks whether two prerequisites
are present in a dependency-curated cross-linguistic dataset:
1) multivariate compressibility beyond a marginal-preserving shuffle null;
2) residual pairwise feature association beyond a permutation null.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import normalized_mutual_info_score
from sklearn.preprocessing import OneHotEncoder

HERE = Path(__file__).resolve().parent
DATA_URL = (
    "https://raw.githubusercontent.com/annagraff/crossling-curated/main/"
    "curated_data/TLI/statisticalTLI/full/"
    "statisticalTLI_full_densified_small.csv"
)
SEED = 2026
MAX_FEATURES_COMPRESSION = 120
MAX_FEATURES_ASSOCIATION = 80
MIN_SHARED_FOR_NMI = 100
N_NULL_COMPRESSION = 12
N_NULL_NMI = 4


def load_data() -> tuple[pd.DataFrame, list[str]]:
    df = pd.read_csv(
        DATA_URL,
        dtype=str,
        na_values=["?", "NA", "N/A", ""],
        keep_default_na=True,
    )
    feature_cols = [
        c for c in df.columns
        if c != "glottocode" and not str(c).lower().startswith("unnamed")
    ]
    # Keep informative features and rank by empirical coverage.
    usable = []
    for c in feature_cols:
        observed = df[c].dropna()
        if len(observed) >= 100 and observed.nunique() >= 2:
            usable.append(c)
    usable.sort(key=lambda c: df[c].notna().mean(), reverse=True)
    return df, usable


def impute_mode(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    for c in out.columns:
        mode = out[c].mode(dropna=True)
        fill = mode.iloc[0] if len(mode) else "__MISSING__"
        out[c] = out[c].fillna(fill).astype(str)
    return out


def make_encoder() -> OneHotEncoder:
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    except TypeError:  # scikit-learn < 1.2
        return OneHotEncoder(handle_unknown="ignore", sparse=True)


def cumulative_svd(frame: pd.DataFrame, ks: tuple[int, ...] = (10, 20, 50)) -> dict[str, float]:
    enc = make_encoder()
    x = enc.fit_transform(frame)
    max_k = min(max(ks), x.shape[0] - 1, x.shape[1] - 1)
    if max_k < 2:
        raise RuntimeError(f"Matrix too small for SVD: {x.shape}")
    svd = TruncatedSVD(n_components=max_k, random_state=SEED)
    svd.fit(x)
    cumulative = np.cumsum(svd.explained_variance_ratio_)
    result: dict[str, float] = {}
    for k in ks:
        kk = min(k, max_k)
        result[str(k)] = float(cumulative[kk - 1])
    return result


def compression_test(df: pd.DataFrame, features: list[str], rng: np.random.Generator) -> dict:
    selected = features[:MAX_FEATURES_COMPRESSION]
    frame = impute_mode(df[selected])
    observed = cumulative_svd(frame)

    null_runs = []
    for _ in range(N_NULL_COMPRESSION):
        shuffled = frame.copy()
        for c in shuffled.columns:
            shuffled[c] = rng.permutation(shuffled[c].to_numpy())
        null_runs.append(cumulative_svd(shuffled))

    null_summary = {}
    excess = {}
    for k in observed:
        vals = np.array([run[k] for run in null_runs], dtype=float)
        null_summary[k] = {
            "mean": float(vals.mean()),
            "sd": float(vals.std(ddof=1)),
            "p95": float(np.quantile(vals, 0.95)),
        }
        excess[k] = float(observed[k] - vals.mean())

    return {
        "n_features": len(selected),
        "n_languages": int(len(frame)),
        "observed_cumulative_explained_variance": observed,
        "null": null_summary,
        "observed_minus_null_mean": excess,
        "note": "Missing values are mode-imputed feature-wise; null shuffles preserve each imputed feature's marginal distribution.",
    }


def nmi_test(df: pd.DataFrame, features: list[str], rng: np.random.Generator) -> dict:
    selected = features[:MAX_FEATURES_ASSOCIATION]
    observed_scores = []
    null_scores = []
    strongest = []

    for a, b in combinations(selected, 2):
        pair = df[[a, b]].dropna()
        if len(pair) < MIN_SHARED_FOR_NMI:
            continue
        x = pair[a].astype(str).to_numpy()
        y = pair[b].astype(str).to_numpy()
        score = float(normalized_mutual_info_score(x, y, average_method="arithmetic"))
        observed_scores.append(score)
        strongest.append((score, a, b, len(pair)))
        for _ in range(N_NULL_NMI):
            null_scores.append(
                float(normalized_mutual_info_score(x, rng.permutation(y), average_method="arithmetic"))
            )

    if not observed_scores:
        raise RuntimeError("No feature pairs had enough shared observations for NMI test")

    obs = np.array(observed_scores)
    nul = np.array(null_scores)
    strongest.sort(reverse=True)

    def qs(v: np.ndarray) -> dict[str, float]:
        return {
            "median": float(np.quantile(v, 0.50)),
            "p90": float(np.quantile(v, 0.90)),
            "p99": float(np.quantile(v, 0.99)),
            "mean": float(v.mean()),
        }

    return {
        "n_features": len(selected),
        "n_pairs": int(len(obs)),
        "observed": qs(obs),
        "permutation_null": qs(nul),
        "strongest_pairs": [
            {"nmi": s, "feature_a": a, "feature_b": b, "shared_n": n}
            for s, a, b, n in strongest[:10]
        ],
        "note": "Pairwise NMI uses only jointly observed languages. The permutation null shuffles one feature within each observed pair.",
    }


def verdict(results: dict) -> tuple[str, list[str]]:
    comp = results["compression"]
    assoc = results["residual_association"]
    comp20 = comp["observed_minus_null_mean"].get("20", 0.0)
    obs90 = assoc["observed"]["p90"]
    null90 = assoc["permutation_null"]["p90"]

    reasons = []
    signals = 0
    if comp20 >= 0.03:
        signals += 1
        reasons.append(f"20-component compression exceeds shuffled-null mean by {comp20:.3f}.")
    else:
        reasons.append(f"20-component compression excess is only {comp20:.3f}.")

    if obs90 >= max(0.05, 1.5 * null90):
        signals += 1
        reasons.append(
            f"90th-percentile residual NMI ({obs90:.3f}) clearly exceeds permutation null ({null90:.3f})."
        )
    else:
        reasons.append(
            f"90th-percentile residual NMI ({obs90:.3f}) is not clearly separated from null ({null90:.3f})."
        )

    if signals == 2:
        status = "PROMISING_PREREQUISITES"
    elif signals == 1:
        status = "MIXED_SIGNAL"
    else:
        status = "WEAK_PREREQUISITES"
    return status, reasons


def write_report(results: dict) -> None:
    status, reasons = verdict(results)
    results["verdict"] = status
    results["verdict_reasons"] = reasons
    (HERE / "pilot-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    c = results["compression"]
    a = results["residual_association"]
    lines = [
        "# Stage-0 Pilot Report · Language Periodic System",
        "",
        f"**Verdict:** `{status}`",
        "",
        "This is a prerequisite test, **not evidence of periodicity by itself**.",
        "",
        "## Data",
        "",
        "TLI-statistical densified-small from Graff et al. (2025), combining cross-linguistic structural information curated to reduce logical and very strong statistical feature dependencies.",
        "",
        "## Compression test",
        "",
        f"Languages: {c['n_languages']} · selected features: {c['n_features']}",
        "",
        "| Components | Observed cumulative variance | Null mean | Observed − null |",
        "|---:|---:|---:|---:|",
    ]
    for k in ("10", "20", "50"):
        lines.append(
            f"| {k} | {c['observed_cumulative_explained_variance'][k]:.3f} | "
            f"{c['null'][k]['mean']:.3f} | {c['observed_minus_null_mean'][k]:+.3f} |"
        )
    lines += [
        "",
        "## Residual association test",
        "",
        f"Feature pairs tested: {a['n_pairs']}",
        "",
        "| Statistic | Observed NMI | Permutation null |",
        "|---|---:|---:|",
        f"| Median | {a['observed']['median']:.3f} | {a['permutation_null']['median']:.3f} |",
        f"| 90th percentile | {a['observed']['p90']:.3f} | {a['permutation_null']['p90']:.3f} |",
        f"| 99th percentile | {a['observed']['p99']:.3f} | {a['permutation_null']['p99']:.3f} |",
        "",
        "## Interpretation",
        "",
    ]
    lines.extend(f"- {r}" for r in reasons)
    lines += [
        "",
        "Even a strong Stage-0 result would only justify Stage 1: explicit held-out comparison of periodic/circular/toroidal models against factor, hierarchy, graph/manifold, and null alternatives, ideally with phylogenetic and geographic controls.",
        "",
        "## Caveats",
        "",
        "The compression analysis uses mode imputation and is sensitive to missing-data structure. Pairwise NMI does not control for genealogical or geographic non-independence. These are deliberate screening tests; confirmatory claims require the later controlled analysis.",
        "",
    ]
    (HERE / "PILOT_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rng = np.random.default_rng(SEED)
    df, features = load_data()
    results = {
        "dataset_url": DATA_URL,
        "seed": SEED,
        "raw_languages": int(len(df)),
        "usable_features": int(len(features)),
        "compression": compression_test(df, features, rng),
        "residual_association": nmi_test(df, features, rng),
    }
    write_report(results)
    print(json.dumps({"verdict": results["verdict"], "reasons": results["verdict_reasons"]}, indent=2))


if __name__ == "__main__":
    main()
