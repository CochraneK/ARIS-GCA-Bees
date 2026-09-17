#!/usr/bin/env python3
"""Stage-1G: calibrate the geographic-collapse result against matched-size random tests.

Stage-1E found weak transfer to held-out geographic blocks. This script asks whether
that weakness is simply caused by smaller/noisier test samples. For each pre-defined
macroarea and outcome-blind spatial cluster, it compares train-vs-test feature-association
similarity against random test sets with exactly the same number of languages.

No geometry model is fitted here; the target is the stability of the feature-association
matrix itself. If geographic splits have much lower train/test correlation than matched
random splits, geographic heterogeneity is directly implicated.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.cluster import KMeans

import stage1 as base
import stage1e as geo

HERE = Path(__file__).resolve().parent
SEED = 2032
N_FEATURES = 40
N_RANDOM_MATCHED = 8
MIN_PAIRS = 100


def assoc_corr(train_sim, test_sim):
    mask = base.upper_mask(train_sim, test_sim)
    if int(mask.sum()) < MIN_PAIRS:
        return None
    a = train_sim[mask]
    b = test_sim[mask]
    if np.std(a) < base.EPS or np.std(b) < base.EPS:
        return 0.0
    return float(spearmanr(a, b).statistic)


def evaluate_block(df, features, universe_idx, test_idx, rng):
    test_set = set(int(x) for x in test_idx)
    train_idx = np.asarray([int(i) for i in universe_idx if int(i) not in test_set], dtype=int)
    train_sim, _ = base.pairwise_nmi(df.iloc[train_idx], features)
    test_sim, _ = base.pairwise_nmi(df.iloc[test_idx], features)
    observed = assoc_corr(train_sim, test_sim)
    if observed is None:
        return None

    n_test = len(test_idx)
    random_vals = []
    universe = np.asarray(universe_idx, dtype=int)
    for _ in range(N_RANDOM_MATCHED):
        rt = np.sort(rng.choice(universe, size=n_test, replace=False))
        rt_set = set(int(x) for x in rt)
        rr = np.asarray([int(i) for i in universe if int(i) not in rt_set], dtype=int)
        rtrain, _ = base.pairwise_nmi(df.iloc[rr], features)
        rtest, _ = base.pairwise_nmi(df.iloc[rt], features)
        value = assoc_corr(rtrain, rtest)
        if value is not None:
            random_vals.append(float(value))
    if not random_vals:
        return None
    rv = np.asarray(random_vals, dtype=float)
    return {
        "n_test": int(n_test),
        "observed_geo_correlation": float(observed),
        "random_matched_mean": float(rv.mean()),
        "random_matched_sd": float(rv.std(ddof=1)) if len(rv) > 1 else 0.0,
        "geo_minus_random": float(observed - rv.mean()),
        "random_fraction_le_geo": float(np.mean(rv <= observed)),
        "random_values": rv.tolist(),
    }


def run_scheme(df, features, labels, rng):
    mapped = labels.notna()
    universe = np.flatnonzero(mapped.to_numpy())
    blocks = []
    for label in sorted(labels[mapped].astype(str).unique()):
        test_idx = np.flatnonzero((labels.astype(str) == label).to_numpy() & mapped.to_numpy())
        if len(test_idx) < base.MIN_PAIR_OBS:
            continue
        ev = evaluate_block(df, features, universe, test_idx, rng)
        if ev is not None:
            blocks.append({"block": str(label), **ev})
    return blocks


def summarize(blocks):
    diffs = np.asarray([b["geo_minus_random"] for b in blocks], dtype=float)
    obs = np.asarray([b["observed_geo_correlation"] for b in blocks], dtype=float)
    rnd = np.asarray([b["random_matched_mean"] for b in blocks], dtype=float)
    return {
        "n_blocks": len(blocks),
        "observed_geo_mean": float(obs.mean()),
        "random_matched_mean": float(rnd.mean()),
        "mean_geo_minus_random": float(diffs.mean()),
        "fraction_blocks_geo_below_random": float(np.mean(diffs < 0)),
    }


def main():
    rng = np.random.default_rng(SEED)
    df, all_features, families, macro, lat, lon = geo.load_geo()
    features = all_features[:N_FEATURES]

    macro_labels = macro.astype("string")
    macro_blocks = run_scheme(df, features, macro_labels, rng)

    coord_ok = lat.notna() & lon.notna()
    xyz = geo.sphere_xyz(lat[coord_ok].to_numpy(float), lon[coord_ok].to_numpy(float))
    km = KMeans(n_clusters=geo.N_SPATIAL_CLUSTERS, random_state=geo.SEED, n_init=20)
    spatial_labels = pd.Series(pd.NA, index=df.index, dtype="string")
    spatial_labels.loc[coord_ok] = [f"cluster_{x}" for x in km.fit_predict(xyz)]
    spatial_blocks = run_scheme(df, features, spatial_labels, rng)

    macro_sum = summarize(macro_blocks)
    spatial_sum = summarize(spatial_blocks)
    mean_delta = np.mean([macro_sum["mean_geo_minus_random"], spatial_sum["mean_geo_minus_random"]])
    frac_below = np.mean([
        macro_sum["fraction_blocks_geo_below_random"],
        spatial_sum["fraction_blocks_geo_below_random"],
    ])
    if mean_delta <= -0.08 and frac_below >= 0.8:
        verdict = "GEOGRAPHIC_HETEROGENEITY_CONFIRMED"
    elif mean_delta >= -0.03:
        verdict = "SAMPLE_SIZE_NOISE_PLAUSIBLE"
    else:
        verdict = "MIXED_GEOGRAPHIC_SHIFT"

    results = {
        "seed": SEED,
        "n_features": N_FEATURES,
        "n_random_matched_per_block": N_RANDOM_MATCHED,
        "macroarea": {"blocks": macro_blocks, "summary": macro_sum},
        "spatial_cluster": {"blocks": spatial_blocks, "summary": spatial_sum},
        "verdict": verdict,
        "claim_boundary": "Matched-size random calibration isolates test-set size as a simple alternative explanation, but it does not itself identify causal areal transmission or separate geography from historically correlated population structure.",
    }
    (HERE / "stage1g-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Stage-1G · Geographic Collapse Calibration",
        "",
        f"**Verdict:** `{verdict}`",
        "",
        f"Features: {N_FEATURES} · matched random test sets per block: {N_RANDOM_MATCHED}",
        "",
    ]
    for name, blockset in (("Macroarea", results["macroarea"]), ("Spatial clusters", results["spatial_cluster"])):
        lines += [f"## {name}", "", "| Block | Test n | Geo train↔test Spearman | Matched-random mean | Geo − random |", "|---|---:|---:|---:|---:|"]
        for b in blockset["blocks"]:
            lines.append(
                f"| {b['block']} | {b['n_test']} | {b['observed_geo_correlation']:.3f} | {b['random_matched_mean']:.3f} | {b['geo_minus_random']:.3f} |"
            )
        s = blockset["summary"]
        lines += [
            "",
            f"Across blocks: geographic mean={s['observed_geo_mean']:.3f}; matched-random mean={s['random_matched_mean']:.3f}; mean difference={s['mean_geo_minus_random']:.3f}; fraction geo below random={s['fraction_blocks_geo_below_random']:.2f}.",
            "",
        ]
    lines += ["## Claim boundary", "", results["claim_boundary"], ""]
    (HERE / "STAGE1G_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"verdict": verdict, "macro": macro_sum, "spatial": spatial_sum}, indent=2))


if __name__ == "__main__":
    main()
