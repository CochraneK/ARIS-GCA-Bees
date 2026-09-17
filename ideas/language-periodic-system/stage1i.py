#!/usr/bin/env python3
"""Stage-1I: external WALS sanity replication.

WALS is much sparser than TLI/GBI and is not dependency-curated in the same way.
This stage is intentionally modest: use the best-covered categorical WALS parameters
and ask whether the qualitative family-held-out tree-vs-circular ordering reverses,
and whether feature-association structure transports across WALS macroareas.

It is a sanity replication, not an effect-size replication.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import normalized_mutual_info_score

import stage1 as base
import stage1b as robust

HERE = Path(__file__).resolve().parent
VALUES_URL = "https://raw.githubusercontent.com/cldf-datasets/wals/master/cldf/values.csv"
LANGUAGES_URL = "https://raw.githubusercontent.com/cldf-datasets/wals/master/cldf/languages.csv"
SEED = 2034
N_FEATURES = 30
MIN_FEATURE_OBS = 250
MAX_CARDINALITY = 20
MIN_PAIR_OBS = 40
MIN_EVAL_PAIRS = 50
N_FAMILY_SPLITS = 8
MAX_ATTEMPTS = 40


def pairwise_nmi(frame: pd.DataFrame, features: list[str]):
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


def load_wals():
    vals = pd.read_csv(VALUES_URL, dtype=str, low_memory=False)
    langs = pd.read_csv(LANGUAGES_URL, dtype=str, low_memory=False)
    required_v = {"Language_ID", "Parameter_ID"}
    if not required_v.issubset(vals.columns):
        raise RuntimeError(f"Unexpected WALS values columns: {list(vals.columns)}")
    value_col = "Code_ID" if "Code_ID" in vals.columns else "Value"
    wide = vals.pivot_table(index="Language_ID", columns="Parameter_ID", values=value_col, aggfunc="first")

    candidates = []
    for c in wide.columns:
        obs = wide[c].dropna()
        nunique = obs.nunique()
        if len(obs) >= MIN_FEATURE_OBS and 2 <= nunique <= MAX_CARDINALITY:
            candidates.append(str(c))
    candidates.sort(key=lambda c: (wide[c].notna().mean(), -wide[c].dropna().nunique()), reverse=True)
    features = candidates[:N_FEATURES]
    if len(features) < 15:
        raise RuntimeError(f"Only {len(features)} WALS parameters meet coverage/cardinality rules")

    df = wide[features].copy()
    langmeta = langs.set_index("ID")
    common = df.index.intersection(langmeta.index)
    df = df.loc[common].copy()
    meta = langmeta.loc[common].copy()

    if "Family" not in meta.columns or "Macroarea" not in meta.columns:
        raise RuntimeError("WALS language metadata lacks Family/Macroarea")
    families = []
    for lid, fam in meta["Family"].items():
        if fam is None or pd.isna(fam) or str(fam).strip() == "":
            fam = f"isolate::{lid}"
        families.append(str(fam))
    families = pd.Series(families, index=np.arange(len(df)), name="family")
    macro = pd.Series(meta["Macroarea"].to_numpy(), index=np.arange(len(df)), name="macroarea")
    df = df.reset_index(drop=True)
    return df, features, families, macro


def family_split_indices(families, rng):
    groups = {}
    for idx, fam in families.items():
        groups.setdefault(str(fam), []).append(int(idx))
    keys = list(groups)
    rng.shuffle(keys)
    target = max(1, int(round(0.30 * len(families))))
    test = []
    for key in keys:
        if len(test) >= target and test:
            break
        test.extend(groups[key])
    testset = set(test)
    train = [int(i) for i in families.index if int(i) not in testset]
    return np.asarray(sorted(train)), np.asarray(sorted(test))


def common_mask(train_sim, test_sim):
    iu = np.triu_indices_from(train_sim, k=1)
    good = np.isfinite(train_sim[iu]) & np.isfinite(test_sim[iu])
    mask = np.zeros_like(train_sim, dtype=bool)
    mask[iu[0][good], iu[1][good]] = True
    return mask


def family_screen(df, features, families, rng):
    runs = []
    attempts = 0
    while len(runs) < N_FAMILY_SPLITS and attempts < MAX_ATTEMPTS:
        attempts += 1
        tr, te = family_split_indices(families, rng)
        train_sim, _ = pairwise_nmi(df.iloc[tr], features)
        test_sim, _ = pairwise_nmi(df.iloc[te], features)
        mask = common_mask(train_sim, test_sim)
        if int(mask.sum()) < MIN_EVAL_PAIRS:
            continue
        train_mask = robust.all_train_mask(train_sim)
        fits = [
            base.fit_lowrank(train_sim, rank=2),
            base.fit_tree(train_sim, train_mask),
            robust.optimize_circle(train_sim, rng),
        ]
        scores = {f.name: base.score_model(f, test_sim, mask) for f in fits}
        runs.append({
            "split": len(runs),
            "n_train": int(len(tr)),
            "n_test": int(len(te)),
            "n_eval_pairs": int(mask.sum()),
            "scores": scores,
        })
    if len(runs) < max(4, N_FAMILY_SPLITS // 2):
        raise RuntimeError(f"Only {len(runs)} valid WALS family splits after {attempts} attempts")

    models = {}
    for model in ("lowrank2", "tree", "circular_optimized"):
        vals = np.asarray([r["scores"][model]["spearman"] for r in runs], dtype=float)
        models[model] = {"mean": float(vals.mean()), "sd": float(vals.std(ddof=1)) if len(vals)>1 else 0.0}
    delta = np.asarray([
        r["scores"]["tree"]["spearman"] - r["scores"]["circular_optimized"]["spearman"]
        for r in runs
    ], dtype=float)
    return {
        "n_valid_splits": len(runs),
        "n_attempts": attempts,
        "runs": runs,
        "models": models,
        "tree_minus_circular_mean": float(delta.mean()),
        "tree_win_fraction": float(np.mean(delta > 0)),
    }


def macro_transfer(df, features, macro):
    mapped = macro.notna()
    universe = np.flatnonzero(mapped.to_numpy())
    blocks = []
    for area in sorted(macro[mapped].astype(str).unique()):
        te = np.flatnonzero((macro.astype(str) == area).to_numpy() & mapped.to_numpy())
        if len(te) < MIN_PAIR_OBS:
            continue
        teset = set(int(x) for x in te)
        tr = np.asarray([int(i) for i in universe if int(i) not in teset], dtype=int)
        train_sim, _ = pairwise_nmi(df.iloc[tr], features)
        test_sim, _ = pairwise_nmi(df.iloc[te], features)
        mask = common_mask(train_sim, test_sim)
        if int(mask.sum()) < MIN_EVAL_PAIRS:
            continue
        a, b = train_sim[mask], test_sim[mask]
        rho = float(spearmanr(a, b).statistic) if np.std(a)>0 and np.std(b)>0 else 0.0
        blocks.append({"macroarea": area, "n_test": int(len(te)), "association_transfer_spearman": rho, "n_pairs": int(mask.sum())})
    vals = np.asarray([b["association_transfer_spearman"] for b in blocks], dtype=float)
    return {
        "blocks": blocks,
        "mean": float(vals.mean()) if len(vals) else None,
        "sd": float(vals.std(ddof=1)) if len(vals)>1 else 0.0 if len(vals) else None,
    }


def main():
    rng = np.random.default_rng(SEED)
    df, features, families, macro = load_wals()
    fam = family_screen(df, features, families, rng)
    geo = macro_transfer(df, features, macro)

    tree = fam["models"]["tree"]["mean"]
    circ = fam["models"]["circular_optimized"]["mean"]
    if tree >= circ + 0.03 and fam["tree_win_fraction"] >= 0.70:
        family_verdict = "WALS_TREE_OVER_CIRCULAR"
    elif circ >= tree + 0.03:
        family_verdict = "WALS_CIRCULAR_REVERSAL"
    else:
        family_verdict = "WALS_FAMILY_MIXED"

    results = {
        "seed": SEED,
        "n_languages": int(len(df)),
        "n_features": int(len(features)),
        "features": features,
        "family_heldout": fam,
        "macroarea_transfer": geo,
        "verdict": family_verdict,
        "claim_boundary": "WALS is highly sparse and not dependency-curated like TLI/GBI. This stage tests qualitative direction only; estimates are not directly comparable in magnitude to earlier stages.",
    }
    (HERE / "stage1i-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Stage-1I · WALS External Sanity Replication",
        "",
        f"**Verdict:** `{family_verdict}`",
        "",
        f"Languages in pivot: {len(df)} · best-covered parameters used: {len(features)}",
        "",
        "## Family-held-out",
        "",
        "| Model | Spearman mean ± SD |",
        "|---|---:|",
    ]
    for model, s in fam["models"].items():
        lines.append(f"| {model} | {s['mean']:.3f} ± {s['sd']:.3f} |")
    lines += [
        "",
        f"Tree − circular: **{fam['tree_minus_circular_mean']:.3f}**; tree win fraction **{fam['tree_win_fraction']:.2f}** across {fam['n_valid_splits']} valid splits.",
        "",
        "## Macroarea association transfer",
        "",
        "| Macroarea | Test n | Train↔test Spearman | Common pairs |",
        "|---|---:|---:|---:|",
    ]
    for b in geo["blocks"]:
        lines.append(f"| {b['macroarea']} | {b['n_test']} | {b['association_transfer_spearman']:.3f} | {b['n_pairs']} |")
    if geo["mean"] is not None:
        lines += ["", f"Mean macroarea transfer: **{geo['mean']:.3f} ± {geo['sd']:.3f}**."]
    lines += ["", "## Claim boundary", "", results["claim_boundary"], ""]
    (HERE / "STAGE1I_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"verdict": family_verdict, "tree": tree, "circular": circ, "geo": geo["mean"]}, indent=2))


if __name__ == "__main__":
    main()
