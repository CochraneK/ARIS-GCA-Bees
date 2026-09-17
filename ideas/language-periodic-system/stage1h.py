#!/usr/bin/env python3
"""Stage-1H: replication under the alternative GBI dependency-curation scheme.

GBI and TLI are not treated as fully independent datasets; they are alternative
curations/representations built on overlapping global typological substrate. This
stage asks whether the family-held-out tree-vs-circular result and geographic
heterogeneity are specific to TLI's curation choices.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

import stage1 as base
import stage1b as robust

HERE = Path(__file__).resolve().parent
GBI_URL = (
    "https://raw.githubusercontent.com/annagraff/crossling-curated/main/"
    "curated_data/GBI/statisticalGBI/statisticalGBI_densified.csv"
)
SEED = 2033
N_FEATURES = 60
MIN_FEATURE_OBS = 180
MAX_CARDINALITY = 15
N_FAMILY_SPLITS = 12
MAX_ATTEMPTS = 50
MIN_EVAL_PAIRS = 100


def load_gbi():
    df = pd.read_csv(
        GBI_URL,
        dtype=str,
        na_values=["?", "NA", "N/A", ""],
        keep_default_na=True,
    )
    df = df.loc[:, ~df.columns.astype(str).str.lower().str.startswith("unnamed")]
    if "glottocode" not in df.columns:
        raise RuntimeError("Expected glottocode in GBI")

    candidates = []
    for c in df.columns:
        if c == "glottocode":
            continue
        obs = df[c].dropna()
        nunique = obs.nunique()
        if len(obs) >= MIN_FEATURE_OBS and 2 <= nunique <= MAX_CARDINALITY:
            candidates.append(c)
    candidates.sort(
        key=lambda c: (df[c].notna().mean(), -df[c].dropna().nunique()), reverse=True
    )
    features = candidates[:N_FEATURES]
    if len(features) < 30:
        raise RuntimeError(f"Too few usable GBI features: {len(features)}")

    glotto = pd.read_csv(base.GLOTTOLOG_URL, dtype=str, low_memory=False)
    meta = glotto.set_index("ID")
    family_map = meta["Family_ID"].to_dict()
    macro_col = next((c for c in ("Macroarea", "Macroareas") if c in meta.columns), None)
    if macro_col is None:
        raise RuntimeError("No Glottolog Macroarea column")
    macro_map = meta[macro_col].to_dict()

    families = []
    macro = []
    for code in df["glottocode"].astype(str):
        fam = family_map.get(code)
        if fam is None or pd.isna(fam) or str(fam).strip() == "":
            fam = f"isolate::{code}"
        families.append(str(fam))
        macro.append(macro_map.get(code))
    return (
        df,
        features,
        pd.Series(families, index=df.index, name="family"),
        pd.Series(macro, index=df.index, name="macroarea"),
    )


def family_screen(df, features, families, rng):
    runs = []
    attempts = 0
    while len(runs) < N_FAMILY_SPLITS and attempts < MAX_ATTEMPTS:
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
            "n_train": int(len(train_idx)),
            "n_test": int(len(test_idx)),
            "n_eval_pairs": int(mask.sum()),
            "scores": scores,
        })
    if len(runs) < N_FAMILY_SPLITS:
        raise RuntimeError(f"Only {len(runs)} valid GBI family splits after {attempts} attempts")

    summary = {}
    for model in ("lowrank2", "tree", "euclidean_connected", "circular_optimized"):
        vals = np.asarray([r["scores"][model]["spearman"] for r in runs], dtype=float)
        summary[model] = {"mean": float(vals.mean()), "sd": float(vals.std(ddof=1))}
    delta = np.asarray(
        [r["scores"]["tree"]["spearman"] - r["scores"]["circular_optimized"]["spearman"] for r in runs],
        dtype=float,
    )
    return {
        "runs": runs,
        "summary": summary,
        "tree_minus_circular_mean": float(delta.mean()),
        "tree_win_fraction": float(np.mean(delta > 0)),
    }


def macroarea_assoc_transfer(df, features, macro):
    mapped = macro.notna()
    all_idx = np.flatnonzero(mapped.to_numpy())
    blocks = []
    for area in sorted(macro[mapped].astype(str).unique()):
        test_idx = np.flatnonzero((macro.astype(str) == area).to_numpy() & mapped.to_numpy())
        if len(test_idx) < base.MIN_PAIR_OBS:
            continue
        test_set = set(int(x) for x in test_idx)
        train_idx = np.asarray([int(i) for i in all_idx if int(i) not in test_set], dtype=int)
        train_sim, _ = base.pairwise_nmi(df.iloc[train_idx], features)
        test_sim, _ = base.pairwise_nmi(df.iloc[test_idx], features)
        mask = base.upper_mask(train_sim, test_sim)
        if int(mask.sum()) < MIN_EVAL_PAIRS:
            continue
        a = train_sim[mask]
        b = test_sim[mask]
        rho = float(spearmanr(a, b).statistic) if np.std(a) > 0 and np.std(b) > 0 else 0.0
        blocks.append({"macroarea": area, "n_test": int(len(test_idx)), "association_transfer_spearman": rho})
    vals = np.asarray([b["association_transfer_spearman"] for b in blocks], dtype=float)
    return {"blocks": blocks, "mean_spearman": float(vals.mean()), "sd": float(vals.std(ddof=1))}


def main():
    rng = np.random.default_rng(SEED)
    df, features, families, macro = load_gbi()
    fam = family_screen(df, features, families, rng)
    geo = macroarea_assoc_transfer(df, features, macro)

    tree = fam["summary"]["tree"]["mean"]
    circ = fam["summary"]["circular_optimized"]["mean"]
    if tree >= circ + 0.04 and fam["tree_win_fraction"] >= 0.75:
        fam_verdict = "TREE_REPLICATES_OVER_CIRCULAR"
    elif circ >= tree + 0.04:
        fam_verdict = "CIRCULAR_REVERSAL"
    else:
        fam_verdict = "GBI_FAMILY_RESULT_MIXED"

    if geo["mean_spearman"] < 0.18:
        geo_verdict = "WEAK_CROSS_MACROAREA_TRANSFER"
    else:
        geo_verdict = "CROSS_MACROAREA_TRANSFER_PRESENT"

    verdict = f"{fam_verdict}__{geo_verdict}"
    results = {
        "seed": SEED,
        "dataset": GBI_URL,
        "n_languages": int(len(df)),
        "n_features": int(len(features)),
        "features": features,
        "family_heldout": fam,
        "macroarea_transfer": geo,
        "verdict": verdict,
        "claim_boundary": "GBI is an alternative dependency-curation/representation, not a fully independent typological source from TLI. Agreement strengthens robustness to curation choice but does not constitute external-dataset replication.",
    }
    (HERE / "stage1h-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Stage-1H · GBI Curation Replication",
        "",
        f"**Verdict:** `{verdict}`",
        "",
        f"Languages: {len(df)} · selected features: {len(features)}",
        "",
        "## Family-held-out model comparison",
        "",
        "| Model | Spearman mean ± SD |",
        "|---|---:|",
    ]
    for model, s in fam["summary"].items():
        lines.append(f"| {model} | {s['mean']:.3f} ± {s['sd']:.3f} |")
    lines += [
        "",
        f"Tree − circular mean difference: **{fam['tree_minus_circular_mean']:.3f}**; tree win fraction: **{fam['tree_win_fraction']:.2f}**.",
        "",
        "## Macroarea association transfer",
        "",
        "| Macroarea | Test n | Train↔test association Spearman |",
        "|---|---:|---:|",
    ]
    for b in geo["blocks"]:
        lines.append(f"| {b['macroarea']} | {b['n_test']} | {b['association_transfer_spearman']:.3f} |")
    lines += [
        "",
        f"Mean cross-macroarea association transfer: **{geo['mean_spearman']:.3f} ± {geo['sd']:.3f}**.",
        "",
        "## Claim boundary",
        "",
        results["claim_boundary"],
        "",
    ]
    (HERE / "STAGE1H_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"verdict": verdict, "tree": tree, "circular": circ, "geo": geo["mean_spearman"]}, indent=2))


if __name__ == "__main__":
    main()
