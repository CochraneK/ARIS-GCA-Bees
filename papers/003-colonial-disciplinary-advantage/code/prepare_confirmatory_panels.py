#!/usr/bin/env python3
"""Prepare frozen confirmatory analysis panels after outcome unlock.

Creates:
1) country × discipline × period panel with explicit zero output cells;
2) CEPII pair × discipline × period panel with explicit zero collaboration cells.

No model is fitted here. Exposure scaling and sample-construction decisions are
implemented exactly as PREREGISTRATION_AMENDMENT_001.
"""

from __future__ import annotations

import argparse
import json
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

IMPERIAL_CENTERS = {"BEL", "GBR", "FRA", "DEU", "NLD", "PRT", "ESP", "ITA"}
PERIODS = ["2007-2010", "2011-2014", "2015-2018", "2019-2022", "2023-2025"]
CONFIRMATORY_PERIODS = set(PERIODS[:4])


def q(path: Path) -> str:
    return str(path).replace("'", "''")


def write_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(database=":memory:")
    con.register("frame", df)
    con.execute(f"COPY frame TO '{q(path)}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    con.close()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--country-cells", type=Path, default=DATA / "derived" / "openalex" / "COUNTRY_DISCIPLINE_WINDOW.parquet")
    p.add_argument("--dyad-positive", type=Path, default=DATA / "derived" / "openalex" / "DYAD_DISCIPLINE_WINDOW_POSITIVE.parquet")
    p.add_argument("--cepii-dyads", type=Path, default=DATA / "derived" / "CEPII_DYADS.csv")
    p.add_argument("--output-dir", type=Path, default=DATA / "analysis")
    args = p.parse_args()

    subprocess.run([sys.executable, str(CODE / "preoutcome_gate.py"), "--strict"], check=True)
    for path in (args.country_cells, args.dyad_positive, args.cepii_dyads):
        if not path.exists():
            raise SystemExit(f"Required outcome/derived file missing: {path}")

    exposure_path = DATA / "derived" / "COLDAT_FORMER_COLONY_EXPOSURE.csv"
    ikes_path = PROCESS / "IKES_FROZEN.csv"
    country_map_path = DATA / "derived" / "COUNTRY_CROSSWALK.csv"

    exposure = pd.read_csv(exposure_path)
    ikes = pd.read_csv(ikes_path)
    country_map = pd.read_csv(country_map_path)
    if set(ikes["concept_id"].astype(str)) != {f"D{i:02d}" for i in range(1, 22)}:
        raise SystemExit("IKES_FROZEN does not contain exactly D01-D21")

    exposure["iso3c"] = exposure["iso3c"].astype(str).str.upper()
    historical_scale = exposure[~exposure["iso3c"].isin(IMPERIAL_CENTERS)].copy()
    exposure_mean = float(historical_scale["years_colonized_total"].mean())
    exposure_sd = float(historical_scale["years_colonized_total"].std(ddof=0))
    if not np.isfinite(exposure_sd) or exposure_sd <= 0:
        raise SystemExit("Invalid source-universe SD for colonial duration")
    exposure["colonial_years_sd"] = (
        exposure["years_colonized_total"] - exposure_mean
    ) / exposure_sd
    exposure["is_coldat_imperial_center"] = exposure["iso3c"].isin(IMPERIAL_CENTERS).astype(int)

    con = duckdb.connect(database=":memory:")
    cells = con.execute(f"SELECT * FROM read_parquet('{q(args.country_cells)}')").fetchdf()
    con.close()
    required_cells = {"iso3c", "concept_id", "period", "fractional_output", "impact_denominator", "fractional_top10"}
    if not required_cells.issubset(cells.columns):
        raise SystemExit(f"Country cells missing {sorted(required_cells-set(cells.columns))}")
    cells["iso3c"] = cells["iso3c"].astype(str).str.upper()

    allowed_country = set(country_map.loc[country_map["status"].eq("RESOLVED"), "iso3c"].astype(str).str.upper())
    allowed_country &= set(exposure["iso3c"])
    cells = cells[cells["iso3c"].isin(allowed_country)].copy()

    # Period eligibility: country has at least one attributed confirmatory-discipline
    # work in that period. This rule is applied before filling field-level zeros.
    active = (
        cells.groupby(["iso3c", "period"], as_index=False)["fractional_output"].sum()
    )
    active = active[active["fractional_output"] > 0][["iso3c", "period"]]
    active = active[active["period"].isin(PERIODS)].drop_duplicates()

    concepts = ikes[["concept_id", "discipline", "IKES", "IKES_median"]].copy()
    grid = active.assign(_k=1).merge(concepts.assign(_k=1), on="_k").drop(columns="_k")
    panel = grid.merge(
        cells,
        on=["iso3c", "concept_id", "period"],
        how="left",
        suffixes=("_ikes", "_openalex"),
        validate="one_to_one",
    )
    for c in ["fractional_output", "impact_denominator", "fractional_top10", "fwci_denominator"]:
        if c in panel.columns:
            panel[c] = panel[c].fillna(0.0)
    # weighted_mean_fwci is undefined when its denominator is zero; retain NA.

    panel = panel.merge(
        exposure[["iso3c", "years_colonized_total", "ever_colonized", "colonial_years_sd", "is_coldat_imperial_center"]],
        on="iso3c",
        how="inner",
        validate="many_to_one",
    )
    panel = panel[panel["is_coldat_imperial_center"] == 0].copy()
    panel["exposure_x_ikes"] = panel["colonial_years_sd"] * panel["IKES"]
    panel["is_primary_mature_window"] = (panel["period"] == "2019-2022").astype(int)
    panel["is_confirmatory_period"] = panel["period"].isin(CONFIRMATORY_PERIODS).astype(int)
    panel["country_period_fe"] = panel["iso3c"] + "__" + panel["period"]
    panel["discipline_period_fe"] = panel["concept_id"] + "__" + panel["period"]
    panel["log_impact_denominator"] = np.where(
        panel["impact_denominator"] > 0,
        np.log(panel["impact_denominator"]),
        np.nan,
    )
    panel = panel.sort_values(["period", "iso3c", "concept_id"]).reset_index(drop=True)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    country_out = args.output_dir / "COUNTRY_DISCIPLINE_PANEL.parquet"
    write_parquet(panel, country_out)

    # Build the dyadic grid in DuckDB to avoid holding a large Cartesian product
    # in Python memory. Pair-periods are eligible only when both endpoints are
    # active in the corresponding country-level period.
    active_path = args.output_dir / "_ACTIVE_COUNTRY_PERIOD.csv"
    active.to_csv(active_path, index=False)
    ikes_temp = args.output_dir / "_IKES_FOR_GRID.csv"
    concepts.to_csv(ikes_temp, index=False)
    dyad_out = args.output_dir / "DYAD_DISCIPLINE_PANEL.parquet"

    dcon = duckdb.connect(database=":memory:")
    dcon.execute(
        f"""
        COPY (
            WITH pairs AS (
                SELECT * FROM read_csv_auto('{q(args.cepii_dyads)}')
            ),
            active AS (
                SELECT upper(iso3c) AS iso3c, period
                FROM read_csv_auto('{q(active_path)}')
            ),
            eligible_pair_period AS (
                SELECT p.*, ai.period
                FROM pairs p
                JOIN active ai ON upper(p.iso3_i) = ai.iso3c
                JOIN active aj ON upper(p.iso3_j) = aj.iso3c AND aj.period = ai.period
            ),
            concepts AS (
                SELECT concept_id, discipline, IKES, IKES_median
                FROM read_csv_auto('{q(ikes_temp)}')
            ),
            grid AS (
                SELECT e.*, c.concept_id, c.discipline, c.IKES, c.IKES_median
                FROM eligible_pair_period e CROSS JOIN concepts c
            ),
            positive AS (
                SELECT * FROM read_parquet('{q(args.dyad_positive)}')
            )
            SELECT
                g.*,
                COALESCE(p.fractional_collaboration_mass, 0.0) AS fractional_collaboration_mass,
                COALESCE(p.raw_coauthored_works, 0) AS raw_coauthored_works,
                g.col_dep_ever * g.IKES AS colonial_tie_x_ikes,
                g.pair_id AS pair_fe,
                g.iso3_i || '__' || g.concept_id || '__' || g.period AS i_discipline_period_fe,
                g.iso3_j || '__' || g.concept_id || '__' || g.period AS j_discipline_period_fe,
                CASE WHEN g.period IN ('2007-2010','2011-2014','2015-2018','2019-2022') THEN 1 ELSE 0 END
                  AS is_confirmatory_period,
                CASE WHEN g.period = '2019-2022' THEN 1 ELSE 0 END AS is_primary_mature_window
            FROM grid g
            LEFT JOIN positive p
              ON g.pair_id = p.pair_id
             AND g.concept_id = p.concept_id
             AND g.period = p.period
        ) TO '{q(dyad_out)}' (FORMAT PARQUET, COMPRESSION ZSTD);
        """
    )
    dcon.close()
    active_path.unlink(missing_ok=True)
    ikes_temp.unlink(missing_ok=True)

    meta = {
        "imperial_centers_excluded_from_country_panel": sorted(IMPERIAL_CENTERS),
        "colonial_years_source_universe_mean": exposure_mean,
        "colonial_years_source_universe_sd_ddof0": exposure_sd,
        "country_panel_rows": int(len(panel)),
        "country_panel_unique_countries": int(panel["iso3c"].nunique()),
        "country_panel_unique_concepts": int(panel["concept_id"].nunique()),
        "country_panel_path": str(country_out),
        "dyad_panel_path": str(dyad_out),
        "zero_fill_rule": "explicit field/pair zeros only inside preregistered eligible country-period/pair-period universe",
    }
    (args.output_dir / "PANEL_BUILD_METADATA.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
