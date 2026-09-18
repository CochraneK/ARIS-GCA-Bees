#!/usr/bin/env python3
"""Small-N imperial-center corroboration for ARIS4C003.

Hard-gated: reads modern OpenAlex outcome cells only after OUTCOME_UNLOCKED.
See process/IMPERIAL_CORROBORATION_PROTOCOL.md.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

PAPER = Path(__file__).resolve().parents[1]
CODE = PAPER / "code"
PROCESS = PAPER / "process"
DATA = PAPER / "data"

CENTERS = ["BEL", "GBR", "FRA", "DEU", "NLD", "PRT", "ESP", "ITA"]
PERIOD = "2019-2022"
REPS = 999
SEED = 20260918
CONCEPTS = [f"D{i:02d}" for i in range(1, 22)]


def read_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Missing OpenAlex cells: {path}")
    con = duckdb.connect(database=":memory:")
    try:
        return con.execute("SELECT * FROM read_parquet(?)", [str(path)]).fetchdf()
    finally:
        con.close()


def slope(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3:
        return math.nan
    xx, yy = x[mask], y[mask]
    denom = float(np.sum((xx - xx.mean()) ** 2))
    if denom <= 0:
        return math.nan
    return float(np.sum((xx - xx.mean()) * (yy - yy.mean())) / denom)


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3 or np.std(x[mask]) == 0 or np.std(y[mask]) == 0:
        return math.nan
    return float(np.corrcoef(x[mask], y[mask])[0, 1])


def spearman(x: pd.Series, y: pd.Series) -> float:
    if x.notna().sum() < 3 or y.notna().sum() < 3:
        return math.nan
    return float(x.rank(method="average").corr(y.rank(method="average"), method="pearson"))


def empire_profiles(field: pd.DataFrame, ikes_col: str = "IKES") -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for iso3 in CENTERS:
        g = field[field["iso3c"] == iso3].sort_values("concept_id")
        if g["concept_id"].tolist() != CONCEPTS:
            raise ValueError(f"{iso3}: incomplete D01-D21 profile")
        x = g[ikes_col].to_numpy(float)
        y = g["SRCA"].to_numpy(float)
        rows.append(
            {
                "iso3c": iso3,
                "profile_slope_srca_on_ikes": slope(x, y),
                "profile_spearman": spearman(g[ikes_col], g["SRCA"]),
                "mapped_fractional_output": float(g["fractional_output"].sum()),
            }
        )
    return pd.DataFrame(rows)


def across_summary(profiles: pd.DataFrame) -> dict[str, float]:
    x = np.log1p(profiles["cumulative_colony_years_ruled"].to_numpy(float))
    y = profiles["profile_slope_srca_on_ikes"].to_numpy(float)
    return {
        "slope_profile_on_log1p_colony_years": slope(x, y),
        "pearson": pearson(x, y),
        "spearman": spearman(pd.Series(x), pd.Series(y)),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--country-cells",
        type=Path,
        default=DATA / "derived" / "openalex" / "COUNTRY_DISCIPLINE_WINDOW.parquet",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=DATA / "results" / "imperial_corroboration",
    )
    args = p.parse_args()

    subprocess.run(
        [sys.executable, str(CODE / "preoutcome_gate.py"), "--strict"],
        check=True,
    )

    cells = read_parquet(args.country_cells)
    ikes = pd.read_csv(PROCESS / "IKES_FROZEN.csv")[
        ["concept_id", "discipline", "IKES"]
    ].copy()
    intensity = pd.read_csv(DATA / "derived" / "COLDAT_IMPERIAL_INTENSITY.csv")
    cross = pd.read_csv(DATA / "derived" / "COUNTRY_CROSSWALK.csv")
    allowed = set(
        cross.loc[cross["status"].eq("RESOLVED"), "iso3c"].astype(str).str.upper()
    )

    intensity["iso3c"] = intensity["iso3c"].astype(str).str.upper()
    if set(CENTERS) != set(intensity["iso3c"]):
        raise SystemExit("Imperial intensity table must contain exactly the frozen eight centers")

    cells["iso3c"] = cells["iso3c"].astype(str).str.upper()
    c = cells[
        cells["period"].eq(PERIOD)
        & cells["iso3c"].isin(allowed)
    ].copy()

    # Build the 8x21 empire grid and fill genuine missing field cells with zero.
    empire_grid = pd.MultiIndex.from_product(
        [CENTERS, CONCEPTS], names=["iso3c", "concept_id"]
    ).to_frame(index=False)
    empire = empire_grid.merge(
        c[["iso3c", "concept_id", "fractional_output"]],
        on=["iso3c", "concept_id"],
        how="left",
        validate="one_to_one",
    )
    empire["fractional_output"] = empire["fractional_output"].fillna(0.0)
    empire = empire.merge(ikes, on="concept_id", how="left", validate="many_to_one")
    if empire["IKES"].isna().any():
        raise SystemExit("Missing IKES in imperial profile grid")

    # Reference shares use all eligible mapped countries in the primary period.
    field_totals = c.groupby("concept_id")["fractional_output"].sum()
    world_total = float(field_totals.sum())
    if world_total <= 0:
        raise SystemExit("Mapped-world output total is zero")
    world_share = field_totals / world_total

    empire["country_total"] = empire.groupby("iso3c")["fractional_output"].transform("sum")
    if (empire["country_total"] <= 0).any():
        raise SystemExit("At least one imperial center has zero mapped output")
    empire["country_field_share"] = empire["fractional_output"] / empire["country_total"]
    empire["world_field_share"] = empire["concept_id"].map(world_share)
    if empire["world_field_share"].isna().any() or (empire["world_field_share"] <= 0).any():
        raise SystemExit("At least one frozen field has zero mapped-world share")
    empire["RCA"] = empire["country_field_share"] / empire["world_field_share"]
    empire["SRCA"] = (empire["RCA"] - 1.0) / (empire["RCA"] + 1.0)

    profiles = empire_profiles(empire)
    profiles = profiles.merge(
        intensity[
            [
                "iso3c",
                "colonizer",
                "cumulative_colony_years_ruled",
                "distinct_colonies",
                "peak_simultaneous_colonies",
            ]
        ],
        on="iso3c",
        how="left",
        validate="one_to_one",
    )
    summary = across_summary(profiles)

    loo_rows: list[dict[str, object]] = []
    for left_out in CENTERS:
        s = across_summary(profiles[profiles["iso3c"] != left_out])
        loo_rows.append({"left_out_iso3c": left_out, **s})
    loo = pd.DataFrame(loo_rows)

    rng = np.random.default_rng(SEED)
    observed = summary["slope_profile_on_log1p_colony_years"]
    perm_rows: list[dict[str, object]] = []
    failures = 0
    base_map = ikes.set_index("concept_id")["IKES"].loc[CONCEPTS].to_numpy()
    for rep in range(1, REPS + 1):
        mapping = dict(zip(CONCEPTS, rng.permutation(base_map)))
        tmp = empire.copy()
        tmp["_IKES_perm"] = tmp["concept_id"].map(mapping)
        pp = empire_profiles(tmp, "_IKES_perm").merge(
            intensity[["iso3c", "cumulative_colony_years_ruled"]],
            on="iso3c",
            how="left",
            validate="one_to_one",
        )
        stat = across_summary(pp)["slope_profile_on_log1p_colony_years"]
        if not np.isfinite(stat):
            failures += 1
        perm_rows.append({"rep": rep, "statistic": stat})

    perm = pd.DataFrame(perm_rows)
    if failures:
        perm_summary: dict[str, object] = {
            "status": "INVALID_DUE_TO_UNDEFINED_PERMUTATIONS",
            "failed": failures,
            "p_two_sided": None,
        }
    else:
        extreme = int((perm["statistic"].abs() >= abs(observed)).sum())
        perm_summary = {
            "status": "VALID",
            "reps": REPS,
            "seed": SEED,
            "extreme_abs_count": extreme,
            "p_two_sided": (1 + extreme) / (REPS + 1),
        }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    empire.to_csv(args.output_dir / "IMPERIAL_FIELD_PROFILES.csv", index=False)
    profiles.to_csv(args.output_dir / "IMPERIAL_PROFILE_SLOPES.csv", index=False)
    loo.to_csv(args.output_dir / "LEAVE_ONE_EMPIRE_OUT.csv", index=False)
    perm.to_csv(args.output_dir / "IKES_LABEL_PERMUTATION.csv", index=False)
    payload = {
        "period": PERIOD,
        "n_imperial_centers": 8,
        "n_disciplines": 21,
        "across_empire": summary,
        "permutation": perm_summary,
        "interpretation": "small-N corroboration; not large-N causal inference",
    }
    (args.output_dir / "SUMMARY.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
