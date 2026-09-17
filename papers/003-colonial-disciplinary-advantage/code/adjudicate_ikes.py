#!/usr/bin/env python3
"""Compare blinded IKES coding rounds and prepare adjudication files.

The script never looks at contemporary outcomes. It reports agreement and flags
large disagreements (absolute difference >= 2 by default). It does NOT choose a
winner automatically; frozen scores require documented evidence adjudication.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

DIMS = [f"D{i}" for i in range(1, 12)]


def weighted_kappa(a: pd.Series, b: pd.Series, k: int = 4) -> float | None:
    mask = a.notna() & b.notna()
    if mask.sum() < 2:
        return None
    x = a[mask].astype(int).to_numpy()
    y = b[mask].astype(int).to_numpy()
    conf = np.zeros((k, k), dtype=float)
    for xi, yi in zip(x, y):
        if 0 <= xi < k and 0 <= yi < k:
            conf[xi, yi] += 1
    n = conf.sum()
    if n == 0:
        return None
    obs = conf / n
    row = obs.sum(axis=1)
    col = obs.sum(axis=0)
    exp = np.outer(row, col)
    weights = np.zeros((k, k), dtype=float)
    for i in range(k):
        for j in range(k):
            weights[i, j] = ((i - j) / (k - 1)) ** 2
    num = float((weights * obs).sum())
    den = float((weights * exp).sum())
    if den == 0:
        return None
    return 1.0 - num / den


def icc_2_1(matrix: np.ndarray) -> float | None:
    """Two-way random, absolute-agreement single-measure ICC(2,1)."""
    if matrix.ndim != 2 or matrix.shape[1] != 2 or matrix.shape[0] < 3:
        return None
    if np.isnan(matrix).any():
        matrix = matrix[~np.isnan(matrix).any(axis=1)]
    n, k = matrix.shape
    if n < 3:
        return None
    grand = matrix.mean()
    row_means = matrix.mean(axis=1)
    col_means = matrix.mean(axis=0)
    ss_rows = k * ((row_means - grand) ** 2).sum()
    ss_cols = n * ((col_means - grand) ** 2).sum()
    ss_total = ((matrix - grand) ** 2).sum()
    ss_error = ss_total - ss_rows - ss_cols
    ms_rows = ss_rows / (n - 1)
    ms_cols = ss_cols / (k - 1)
    ms_error = ss_error / ((n - 1) * (k - 1))
    den = ms_rows + (k - 1) * ms_error + (k * (ms_cols - ms_error) / n)
    return None if den == 0 else float((ms_rows - ms_error) / den)


def load(path: Path, label: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"discipline", *DIMS}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"{label} missing columns: {sorted(missing)}")
    if df["discipline"].duplicated().any():
        raise SystemExit(f"{label} has duplicate disciplines")
    for d in DIMS:
        df[d] = pd.to_numeric(df[d], errors="coerce")
        bad = df[d].dropna()[~df[d].dropna().between(0, 3)]
        if len(bad):
            raise SystemExit(f"{label} {d} contains scores outside 0-3")
    return df[["discipline", *DIMS]].copy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("coder_a", type=Path)
    parser.add_argument("coder_b", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--large-disagreement", type=float, default=2.0)
    args = parser.parse_args()

    a = load(args.coder_a, "Coder A")
    b = load(args.coder_b, "Coder B")
    merged = a.merge(b, on="discipline", how="outer", suffixes=("_A", "_B"), indicator=True)
    if not (merged["_merge"] == "both").all():
        missing = merged.loc[merged["_merge"] != "both", ["discipline", "_merge"]]
        raise SystemExit("Coder discipline sets differ:\n" + missing.to_string(index=False))

    long_rows = []
    for _, row in merged.iterrows():
        for d in DIMS:
            av = row[f"{d}_A"]
            bv = row[f"{d}_B"]
            diff = abs(av - bv) if pd.notna(av) and pd.notna(bv) else np.nan
            long_rows.append(
                {
                    "discipline": row["discipline"],
                    "dimension": d,
                    "score_A": av,
                    "score_B": bv,
                    "abs_diff": diff,
                    "needs_adjudication": bool(pd.isna(diff) or diff >= args.large_disagreement),
                    "adjudicated_score": "",
                    "adjudication_note": "",
                }
            )
    long = pd.DataFrame(long_rows)

    kappas = {}
    for d in DIMS:
        kappas[d] = weighted_kappa(merged[f"{d}_A"], merged[f"{d}_B"])

    a_mean = merged[[f"{d}_A" for d in DIMS]].mean(axis=1, skipna=False)
    b_mean = merged[[f"{d}_B" for d in DIMS]].mean(axis=1, skipna=False)
    ikes_icc = icc_2_1(np.column_stack([a_mean.to_numpy(), b_mean.to_numpy()]))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    long.to_csv(args.output_dir / "IKES_DISAGREEMENTS.csv", index=False)

    summary = {
        "n_disciplines": int(len(merged)),
        "n_cells": int(len(long)),
        "n_missing_pairs": int(long["abs_diff"].isna().sum()),
        "n_large_disagreements": int(long["needs_adjudication"].sum()),
        "mean_absolute_difference": float(long["abs_diff"].mean()),
        "dimension_quadratic_weighted_kappa": kappas,
        "ikes_mean_icc_2_1": ikes_icc,
        "freeze_rule": "all NA and abs-difference>=2 cells require documented outcome-blind adjudication",
    }
    (args.output_dir / "AGREEMENT_SUMMARY.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    candidate = pd.DataFrame({"discipline": merged["discipline"]})
    for d in DIMS:
        candidate[d] = merged[[f"{d}_A", f"{d}_B"]].mean(axis=1, skipna=False)
    candidate["IKES_unadjudicated_mean"] = candidate[DIMS].mean(axis=1, skipna=False)
    candidate.to_csv(args.output_dir / "IKES_UNADJUDICATED_MEAN.csv", index=False)

    print(json.dumps(summary, indent=2))
    print("No frozen score was created automatically.")


if __name__ == "__main__":
    main()
