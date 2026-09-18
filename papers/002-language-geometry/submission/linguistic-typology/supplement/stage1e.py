#!/usr/bin/env python3
"""Stage-1E: geography-aware and geography+family joint hold-out validation.

The goal is to test whether geometric predictability survives when an entire geographic
region is unseen, and under a stricter joint block where any top-level Glottolog family
represented in the test region is also removed from training.

Two geography definitions are fixed without looking at linguistic outcomes:
1. Glottolog Macroarea;
2. five clusters formed from latitude/longitude on the unit sphere.

Models are trained on feature-association matrices from training languages and predict
feature associations computed independently in held-out languages.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

import stage1 as base
import stage1b as robust

HERE = Path(__file__).resolve().parent
SEED = 2030
N_SPATIAL_CLUSTERS = 5
MIN_TEST_LANGUAGES = 60
MIN_TRAIN_LANGUAGES = 180
MIN_EVAL_PAIRS = 100


def load_geo():
    df, features, families = base.load_data()
    glotto = pd.read_csv(base.GLOTTOLOG_URL, dtype=str, low_memory=False)
    if "ID" not in glotto.columns:
        raise RuntimeError("Glottolog languages.csv lacks ID")

    meta = glotto.set_index("ID")
    macro_col = next((c for c in ("Macroarea", "Macroareas") if c in meta.columns), None)
    lat_col = next((c for c in ("Latitude", "latitude") if c in meta.columns), None)
    lon_col = next((c for c in ("Longitude", "longitude") if c in meta.columns), None)
    if macro_col is None or lat_col is None or lon_col is None:
        raise RuntimeError(
            f"Expected Macroarea/Latitude/Longitude in Glottolog; columns include {list(glotto.columns)[:25]}"
        )

    codes = df["glottocode"].astype(str)
    macro = codes.map(meta[macro_col].to_dict())
    lat = pd.to_numeric(codes.map(meta[lat_col].to_dict()), errors="coerce")
    lon = pd.to_numeric(codes.map(meta[lon_col].to_dict()), errors="coerce")
    return df, features, families.astype(str), macro, lat, lon


def sphere_xyz(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    latr = np.deg2rad(lat)
    lonr = np.deg2rad(lon)
    return np.column_stack(
        [np.cos(latr) * np.cos(lonr), np.cos(latr) * np.sin(lonr), np.sin(latr)]
    )


def score_split(df, features, train_idx, test_idx, rng):
    if len(train_idx) < MIN_TRAIN_LANGUAGES or len(test_idx) < MIN_TEST_LANGUAGES:
        return None
    train_sim, _ = base.pairwise_nmi(df.iloc[train_idx], features)
    test_sim, _ = base.pairwise_nmi(df.iloc[test_idx], features)
    mask = base.upper_mask(train_sim, test_sim)
    if int(mask.sum()) < MIN_EVAL_PAIRS:
        return None

    train_mask = robust.all_train_mask(train_sim)
    fits = [
        base.fit_lowrank(train_sim, rank=2),
        robust.fit_connected_euclidean(train_sim),
        base.fit_tree(train_sim, train_mask),
        base.fit_graph(train_sim, train_mask),
        robust.optimize_circle(train_sim, rng),
    ]
    scores = {f.name: base.score_model(f, test_sim, mask) for f in fits}
    return {
        "n_train": int(len(train_idx)),
        "n_test": int(len(test_idx)),
        "n_eval_pairs": int(mask.sum()),
        "scores": scores,
    }


def joint_train_indices(all_idx, test_idx, families):
    test_families = set(families.iloc[test_idx].astype(str))
    test_set = set(int(x) for x in test_idx)
    return np.asarray(
        [int(i) for i in all_idx if int(i) not in test_set and str(families.iloc[int(i)]) not in test_families],
        dtype=int,
    )


def run_blocks(df, features, families, labels: pd.Series, rng, kind: str):
    mapped = labels.notna()
    all_idx = np.flatnonzero(mapped.to_numpy())
    out = []
    for label in sorted(labels[mapped].astype(str).unique()):
        test_idx = np.flatnonzero((labels.astype(str) == label).to_numpy() & mapped.to_numpy())
        train_geo = np.asarray([i for i in all_idx if i not in set(test_idx)], dtype=int)
        train_joint = joint_train_indices(all_idx, test_idx, families)

        geo = score_split(df, features, train_geo, test_idx, rng)
        joint = score_split(df, features, train_joint, test_idx, rng)
        if geo is None and joint is None:
            continue
        out.append(
            {
                "block": str(label),
                "kind": kind,
                "n_test": int(len(test_idx)),
                "geo_only": geo,
                "geo_plus_family": joint,
            }
        )
    return out


def summarize(blocks, mode):
    valid = [b[mode] for b in blocks if b.get(mode) is not None]
    if not valid:
        return None
    names = sorted(valid[0]["scores"])
    models = {}
    for name in names:
        models[name] = {}
        for metric in ("spearman", "pearson", "rmse", "mae"):
            vals = np.asarray(
                [x["scores"][name][metric] for x in valid if x["scores"][name][metric] is not None],
                dtype=float,
            )
            models[name][metric] = {
                "mean": float(vals.mean()),
                "sd": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0,
                "n_blocks": int(len(vals)),
            }
    return {"n_blocks": len(valid), "models": models}


def decision(summaries):
    reasons = []
    regime_flags = []
    for label, s in summaries.items():
        if s is None:
            continue
        m = s["models"]
        circ = m["circular_optimized"]["spearman"]["mean"]
        competitors = ["lowrank2", "euclidean_connected", "tree", "graph"]
        best_name = max(competitors, key=lambda x: m[x]["spearman"]["mean"])
        best = m[best_name]["spearman"]["mean"]
        reasons.append(f"{label}: circular={circ:.3f}; best non-periodic={best_name} {best:.3f}; blocks={s['n_blocks']}.")
        if best >= 0.12 and best >= circ + 0.03:
            regime_flags.append("nonperiodic")
        elif circ >= 0.12 and circ >= best - 0.03:
            regime_flags.append("circular")
        elif max(best, circ) < 0.08:
            regime_flags.append("weak")
        else:
            regime_flags.append("mixed")

    if regime_flags and all(x == "nonperiodic" for x in regime_flags):
        return "NONPERIODIC_GEOMETRY_SURVIVES_GEO_BLOCK", reasons
    if regime_flags and all(x == "circular" for x in regime_flags):
        return "CIRCULAR_GEOMETRY_SURVIVES_GEO_BLOCK", reasons
    if regime_flags and all(x == "weak" for x in regime_flags):
        return "GEOGRAPHY_BLOCK_COLLAPSE", reasons
    return "MIXED_GEOGRAPHIC_GENERALIZATION", reasons


def write_report(results):
    (HERE / "stage1e-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Stage-1E · Geography-Aware Validation",
        "",
        f"**Verdict:** `{results['verdict']}`",
        "",
        "Two outcome-blind geographic partitions are used: Glottolog Macroareas and five latitude/longitude clusters on the unit sphere. `geo_plus_family` additionally removes from training every top-level family represented in the test block.",
        "",
    ]
    for scheme in ("macroarea", "spatial_cluster"):
        lines += [f"## {scheme}", ""]
        blocks = results[scheme]["blocks"]
        lines += ["| Block | Test n | Geo-only? | Joint geo+family? |", "|---|---:|---:|---:|"]
        for b in blocks:
            lines.append(
                f"| {b['block']} | {b['n_test']} | {'yes' if b['geo_only'] else 'no'} | {'yes' if b['geo_plus_family'] else 'no'} |"
            )
        lines += [""]
        for mode in ("geo_only", "geo_plus_family"):
            s = results[scheme]["summaries"].get(mode)
            if s is None:
                continue
            lines += [f"### {mode}", "", "| Model | Spearman | Pearson | RMSE | MAE |", "|---|---:|---:|---:|---:|"]
            for model in ("lowrank2", "euclidean_connected", "tree", "graph", "circular_optimized"):
                m = s["models"][model]
                lines.append(
                    f"| {model} | {m['spearman']['mean']:.3f} ± {m['spearman']['sd']:.3f} | "
                    f"{m['pearson']['mean']:.3f} | {m['rmse']['mean']:.3f} | {m['mae']['mean']:.3f} |"
                )
            lines += [""]
    lines += ["## Automated interpretation", ""]
    lines.extend(f"- {x}" for x in results["verdict_reasons"])
    lines += [
        "",
        "## Claim boundary",
        "",
        "Macroarea and coordinate-cluster hold-outs reduce direct areal leakage but do not model contact networks or phylogenetic covariance explicitly. The joint geo+family split is deliberately severe and may reduce training diversity. These are confirmatory-style robustness screens, not a full spatiophylogenetic model.",
        "",
    ]
    (HERE / "STAGE1E_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    rng = np.random.default_rng(SEED)
    df, features, families, macro, lat, lon = load_geo()

    macro_labels = macro.astype("string")
    macro_blocks = run_blocks(df, features, families, macro_labels, rng, "macroarea")

    coord_ok = lat.notna() & lon.notna()
    xyz = sphere_xyz(lat[coord_ok].to_numpy(float), lon[coord_ok].to_numpy(float))
    km = KMeans(n_clusters=N_SPATIAL_CLUSTERS, random_state=SEED, n_init=20)
    labels = pd.Series(pd.NA, index=df.index, dtype="string")
    labels.loc[coord_ok] = [f"cluster_{x}" for x in km.fit_predict(xyz)]
    spatial_blocks = run_blocks(df, features, families, labels, rng, "spatial_cluster")

    summaries = {
        "macroarea_geo": summarize(macro_blocks, "geo_only"),
        "macroarea_joint": summarize(macro_blocks, "geo_plus_family"),
        "spatial_geo": summarize(spatial_blocks, "geo_only"),
        "spatial_joint": summarize(spatial_blocks, "geo_plus_family"),
    }
    verdict, reasons = decision(summaries)
    results = {
        "seed": SEED,
        "n_languages": int(len(df)),
        "n_features": int(len(features)),
        "macroarea": {
            "blocks": macro_blocks,
            "summaries": {
                "geo_only": summaries["macroarea_geo"],
                "geo_plus_family": summaries["macroarea_joint"],
            },
        },
        "spatial_cluster": {
            "n_clusters": N_SPATIAL_CLUSTERS,
            "blocks": spatial_blocks,
            "summaries": {
                "geo_only": summaries["spatial_geo"],
                "geo_plus_family": summaries["spatial_joint"],
            },
        },
        "verdict": verdict,
        "verdict_reasons": reasons,
        "limitations": [
            "Geographic blocks do not explicitly fit a contact network.",
            "Joint geographic+family blocking is severe and can reduce train/test support.",
            "Feature selection was frozen from the Stage-1 coverage rule rather than redone inside every split.",
            "A full Bayesian spatiophylogenetic covariance model remains outside this screening stage.",
        ],
    }
    write_report(results)
    print(json.dumps({"verdict": verdict, "reasons": reasons}, indent=2))


if __name__ == "__main__":
    main()
