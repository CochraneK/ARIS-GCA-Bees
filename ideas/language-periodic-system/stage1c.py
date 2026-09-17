#!/usr/bin/env python3
"""Stage-1C: test local periodicity in pre-defined TLI structural domains.

Stage 1B showed feature-count sensitivity. Rather than post-hoc selecting a subset that
favours a circle, this analysis uses the TLI authors' own `grouping` metadata to define
subsystems before looking at their model-comparison results.

Domains:
- Grammar_other
- Grammar_linear_order
- Grammatical_categories
- Lexical (merging official Lexical_* groups)
- Phonology (merging official Phonology_* groups)

The primary evaluation remains top-level Glottolog family hold-out. Periodic candidates
include both a standard equal-spaced spectral circular ordering and the directly optimized
angular model from Stage 1B.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import stage1 as base
import stage1b as robust

HERE = Path(__file__).resolve().parent
PARAMETERS_URL = (
    "https://raw.githubusercontent.com/annagraff/crossling-curated/"
    "255632bc62ce05674f1af195b88efea5aef7afce/"
    "curated_data/TLI/statisticalTLI/cldf/parameters.csv"
)
SEED = 2028
N_SPLITS = 4
MAX_SPLIT_ATTEMPTS = 24
MAX_FEATURES_PER_DOMAIN = 40
MIN_FEATURES_PER_DOMAIN = 12
MIN_FEATURE_OBS = 160
MAX_CARDINALITY = 15


def load_full() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    df = pd.read_csv(
        base.TLI_URL,
        dtype=str,
        na_values=["?", "NA", "N/A", ""],
        keep_default_na=True,
    )
    df = df.loc[:, ~df.columns.astype(str).str.lower().str.startswith("unnamed")]
    glotto = pd.read_csv(base.GLOTTOLOG_URL, dtype=str, low_memory=False)
    family_map = glotto.set_index("ID")["Family_ID"].to_dict()
    families = []
    for code in df["glottocode"].astype(str):
        fam = family_map.get(code)
        if fam is None or pd.isna(fam) or str(fam).strip() == "":
            fam = f"isolate::{code}"
        families.append(str(fam))
    meta = pd.read_csv(PARAMETERS_URL, dtype=str, low_memory=False)
    return df, pd.Series(families, index=df.index, name="family"), meta


def superdomain(grouping: str) -> str | None:
    g = str(grouping)
    if g == "Grammar_other":
        return "Grammar_other"
    if g == "Grammar_linear_order":
        return "Grammar_linear_order"
    if g == "Grammatical_categories":
        return "Grammatical_categories"
    if g.startswith("Lexical"):
        return "Lexical"
    if g.startswith("Phonology"):
        return "Phonology"
    return None


def select_domains(df: pd.DataFrame, meta: pd.DataFrame) -> dict[str, list[str]]:
    mapping: dict[str, str] = {}
    for _, row in meta.iterrows():
        feature = row.get("short.name")
        group = row.get("grouping")
        if pd.isna(feature) or pd.isna(group):
            continue
        dom = superdomain(str(group))
        if dom is not None:
            mapping[str(feature)] = dom

    by_domain: dict[str, list[str]] = {}
    for feature, dom in mapping.items():
        if feature not in df.columns:
            continue
        obs = df[feature].dropna()
        nunique = int(obs.nunique())
        if len(obs) < MIN_FEATURE_OBS or not (2 <= nunique <= MAX_CARDINALITY):
            continue
        by_domain.setdefault(dom, []).append(feature)

    for dom, feats in by_domain.items():
        feats.sort(
            key=lambda c: (df[c].notna().mean(), -df[c].dropna().nunique()),
            reverse=True,
        )
        by_domain[dom] = feats[:MAX_FEATURES_PER_DOMAIN]

    return {
        dom: feats
        for dom, feats in sorted(by_domain.items())
        if len(feats) >= MIN_FEATURES_PER_DOMAIN
    }


def fit_equal_spaced_circle(train_sim: np.ndarray) -> base.FitResult:
    coords, floor = robust.connected_coords(train_sim)
    raw_angles = robust.angles_from_coords(coords)
    order = np.argsort(raw_angles)
    n = len(order)
    equal = np.empty(n, dtype=float)
    equal[order] = 2 * np.pi * np.arange(n) / n
    mask = robust.all_train_mask(train_sim)
    pred, beta = robust.circular_predict(train_sim, equal, mask)
    return base.FitResult(
        "circular_equal_spaced",
        pred,
        {
            "angles": equal.tolist(),
            "beta": beta.tolist(),
            "affinity_floor": floor,
        },
    )


def summarize(runs: list[dict]) -> dict:
    model_names = list(runs[0]["scores"])
    result = {}
    for model in model_names:
        result[model] = {}
        for metric in ("spearman", "pearson", "rmse", "mae"):
            vals = np.asarray([r["scores"][model][metric] for r in runs], dtype=float)
            result[model][metric] = {
                "mean": float(vals.mean()),
                "sd": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0,
            }
    stability = np.asarray([r["optimized_circle_stability"] for r in runs], dtype=float)
    return {
        "models": result,
        "optimized_circle_stability": {
            "mean": float(stability.mean()),
            "sd": float(stability.std(ddof=1)) if len(stability) > 1 else 0.0,
        },
    }


def run_domain(
    df: pd.DataFrame,
    families: pd.Series,
    features: list[str],
    rng: np.random.Generator,
) -> dict:
    full_sim, _ = base.pairwise_nmi(df, features)
    full_opt = robust.optimize_circle(full_sim, rng)
    reference_angles = np.asarray(full_opt.extra["angles"], dtype=float)

    runs = []
    attempts = 0
    rejected_attempts = 0
    while len(runs) < N_SPLITS and attempts < MAX_SPLIT_ATTEMPTS:
        attempts += 1
        train_idx, test_idx = base.family_split_indices(families, rng)
        train_sim, _ = base.pairwise_nmi(df.iloc[train_idx], features)
        test_sim, _ = base.pairwise_nmi(df.iloc[test_idx], features)
        mask = robust.eval_mask(train_sim, test_sim)
        if int(mask.sum()) < 40:
            rejected_attempts += 1
            continue

        train_mask = robust.all_train_mask(train_sim)
        fits = [
            base.fit_lowrank(train_sim, rank=2),
            base.fit_tree(train_sim, train_mask),
            robust.fit_connected_euclidean(train_sim),
            fit_equal_spaced_circle(train_sim),
            robust.optimize_circle(train_sim, rng),
        ]
        scores = {fit.name: base.score_model(fit, test_sim, mask) for fit in fits}
        opt = next(f for f in fits if f.name == "circular_optimized")
        opt_angles = np.asarray(opt.extra["angles"], dtype=float)
        runs.append(
            {
                "split": len(runs),
                "attempt": attempts,
                "n_train": int(len(train_idx)),
                "n_test": int(len(test_idx)),
                "n_eval_pairs": int(mask.sum()),
                "scores": scores,
                "optimized_circle_stability": base.circular_stability(reference_angles, opt_angles),
            }
        )

    if len(runs) < N_SPLITS:
        raise RuntimeError(
            f"Only {len(runs)} valid family-held-out runs after {attempts} attempts; "
            f"required {N_SPLITS}. Refusing to report an under-sampled domain."
        )
    return {
        "runs": runs,
        "n_valid_runs": len(runs),
        "n_attempts": attempts,
        "n_rejected_attempts": rejected_attempts,
        "summary": summarize(runs),
    }


def classify_domain(block: dict) -> tuple[str, dict]:
    s = block["summary"]["models"]
    periodic = max(
        s["circular_equal_spaced"]["spearman"]["mean"],
        s["circular_optimized"]["spearman"]["mean"],
    )
    nonperiodic_names = ["lowrank2", "tree", "euclidean_connected"]
    best_name = max(nonperiodic_names, key=lambda m: s[m]["spearman"]["mean"])
    best = s[best_name]["spearman"]["mean"]
    stability = block["summary"]["optimized_circle_stability"]["mean"]

    if periodic >= 0.15 and periodic >= best - 0.03 and stability >= 0.40:
        status = "LOCAL_PERIODIC_CANDIDATE"
    elif best >= periodic + 0.05:
        status = "NONPERIODIC_DOMAIN"
    else:
        status = "AMBIGUOUS_DOMAIN"
    return status, {
        "best_periodic_spearman": float(periodic),
        "best_nonperiodic_model": best_name,
        "best_nonperiodic_spearman": float(best),
        "optimized_circle_stability": float(stability),
    }


def write_report(results: dict) -> None:
    (HERE / "stage1c-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Stage-1C · Pre-defined Domain Test for Local Periodicity",
        "",
        f"**Overall verdict:** `{results['verdict']}`",
        "",
        "Domains are defined from the TLI authors' `grouping` metadata before model comparison; no domain is selected because it happened to look circular.",
        "",
        f"Every reported domain contains exactly {N_SPLITS} valid family-held-out runs. Invalid draws with too few jointly observed feature pairs are rejected and resampled rather than silently reducing the replicate count.",
        "",
    ]
    for name, block in results["domains"].items():
        lines += [
            f"## {name}",
            "",
            f"Features: {block['n_features']} · valid splits: {block['n_valid_runs']}/{block['n_attempts']} attempts · domain verdict: `{block['domain_verdict']}`",
            "",
            "| Model | Spearman | Pearson | RMSE | MAE |",
            "|---|---:|---:|---:|---:|",
        ]
        s = block["summary"]["models"]
        for model in (
            "lowrank2",
            "euclidean_connected",
            "tree",
            "circular_equal_spaced",
            "circular_optimized",
        ):
            m = s[model]
            lines.append(
                f"| {model} | {m['spearman']['mean']:.3f} ± {m['spearman']['sd']:.3f} | "
                f"{m['pearson']['mean']:.3f} | {m['rmse']['mean']:.3f} | {m['mae']['mean']:.3f} |"
            )
        st = block["summary"]["optimized_circle_stability"]
        lines += [
            "",
            f"Optimized circular-order stability: {st['mean']:.3f} ± {st['sd']:.3f}",
            "",
        ]

    lines += [
        "## Interpretation rule",
        "",
        "A `LOCAL_PERIODIC_CANDIDATE` is only a candidate module for confirmatory testing. It requires periodic Spearman ≥ 0.15, within 0.03 of the best non-periodic baseline, and circular-order stability ≥ 0.40. This deliberately does not call a domain periodic merely because a circular fit is non-zero.",
        "",
        "## Claim boundary",
        "",
        "This is exploratory module-level screening. Multiple-domain testing, geography, full phylogenetic dependence, circular-seriation goodness-of-fit, and replication must be handled before a local-periodicity claim enters a paper.",
        "",
    ]
    (HERE / "STAGE1C_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rng = np.random.default_rng(SEED)
    df, families, meta = load_full()
    domains = select_domains(df, meta)
    if not domains:
        raise RuntimeError("No predefined TLI domains met the feature-count threshold")

    out = {}
    local_candidates = []
    for name, features in domains.items():
        block = run_domain(df, families, features, rng)
        status, comparison = classify_domain(block)
        out[name] = {
            "n_features": len(features),
            "features": features,
            "domain_verdict": status,
            "comparison": comparison,
            **block,
        }
        if status == "LOCAL_PERIODIC_CANDIDATE":
            local_candidates.append(name)

    if local_candidates:
        verdict = "LOCAL_PERIODICITY_WORTH_CONFIRMING"
    else:
        verdict = "NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE"

    results = {
        "seed": SEED,
        "dataset": base.TLI_URL,
        "parameter_metadata": PARAMETERS_URL,
        "n_languages": int(len(df)),
        "n_splits": N_SPLITS,
        "max_split_attempts": MAX_SPLIT_ATTEMPTS,
        "domains": out,
        "local_periodic_candidates": local_candidates,
        "verdict": verdict,
        "limitations": [
            "Four valid family-held-out splits per domain are a screening sample, not a final uncertainty analysis.",
            "The domain threshold is pre-specified in code but was chosen for feasibility rather than preregistered externally.",
            "Multiple-domain screening requires multiplicity-aware confirmation.",
            "Geographic blocking and full phylogenetic covariance are not yet included.",
            "Circular-seriation Robinsonian goodness-of-fit is not yet tested directly.",
        ],
    }
    write_report(results)
    print(json.dumps({"verdict": verdict, "local_periodic_candidates": local_candidates}, indent=2))


if __name__ == "__main__":
    main()
