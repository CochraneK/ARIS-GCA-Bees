#!/usr/bin/env python3
"""Derive compact ARIS4C003 historical exposure tables from OWID/COLDAT CSVs.

This script uses historical exposure data only. It does not read modern research
outcomes. All generated tables are suitable for `data/derived/` and remain
separate from the confirmatory outcome pipeline.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ID_COLS = {"Entity", "Code", "Year", "World region according to OWID"}
EMPIRE_ISO3 = {
    "Belgium": "BEL",
    "United Kingdom": "GBR",
    "France": "FRA",
    "Germany": "DEU",
    "Netherlands": "NLD",
    "Portugal": "PRT",
    "Spain": "ESP",
    "Italy": "ITA",
}


def measure_col(df: pd.DataFrame) -> str:
    candidates = [c for c in df.columns if c not in ID_COLS]
    if len(candidates) != 1:
        raise SystemExit(
            "Expected exactly one OWID measure column besides Entity/Code/Year; "
            f"found {candidates}"
        )
    return candidates[0]


def build_former_colony(years_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(years_csv)
    required = {"Entity", "Code", "Year"}
    if not required.issubset(df.columns):
        raise SystemExit(f"{years_csv} missing {sorted(required - set(df.columns))}")
    m = measure_col(df)
    df = df[df["Code"].notna()].copy()
    df[m] = pd.to_numeric(df[m], errors="coerce")

    latest = (
        df.sort_values(["Code", "Year"])
        .dropna(subset=[m])
        .groupby("Code", as_index=False)
        .tail(1)
    )
    out = latest[["Entity", "Code", "Year", m]].rename(
        columns={
            "Entity": "country",
            "Code": "iso3c",
            "Year": "source_last_year",
            m: "years_colonized_total",
        }
    )
    out["ever_colonized"] = (out["years_colonized_total"] > 0).astype(int)
    # Do NOT create the preregistered one-SD exposure here. Primary scaling is
    # computed only after the eight COLDAT imperial centers are excluded from the
    # confirmatory former-colony sample.
    return out.sort_values("iso3c").reset_index(drop=True)


def mode_without_multiple(values: pd.Series) -> str:
    s = values.astype(str)
    s = s[s != "Multiple colonizers"]
    if s.empty:
        return ""
    modes = s.mode()
    return str(sorted(modes.astype(str).tolist())[0]) if len(modes) else ""


def unique_without_multiple(values: pd.Series) -> str:
    vals = sorted({str(v) for v in values if str(v) != "Multiple colonizers"})
    return "|".join(vals)


def build_colonizer_identity(colonizer_year_csv: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(colonizer_year_csv)
    required = {"Entity", "Code", "Year"}
    if not required.issubset(df.columns):
        raise SystemExit(f"{colonizer_year_csv} missing {sorted(required - set(df.columns))}")
    m = measure_col(df)
    df = df[df["Code"].notna()].copy()
    df[m] = df[m].astype(str).str.strip()
    colonized = df[~df[m].isin(["Not colonized", "nan", "", "None"])].copy()
    colonized["Year"] = pd.to_numeric(colonized["Year"], errors="raise").astype(int)
    colonized = colonized.sort_values(["Code", "Year"])

    state = (
        colonized.groupby(["Entity", "Code"], as_index=False)
        .agg(
            first_colonized_year=("Year", "min"),
            last_colonized_year=("Year", "max"),
            observed_colonial_year_rows=("Year", "size"),
            primary_single_colonizer_mode=(m, mode_without_multiple),
            last_recorded_colonizer_category=(m, "last"),
            has_multiple_colonizer_year=(m, lambda s: int((s == "Multiple colonizers").any())),
            single_colonizers_observed=(m, unique_without_multiple),
        )
        .rename(columns={"Entity": "country", "Code": "iso3c"})
        .sort_values("iso3c")
        .reset_index(drop=True)
    )

    # Lower-bound ruler profile: processed OWID rows labelled "Multiple
    # colonizers" cannot be assigned to a particular ruler without returning to
    # the underlying COLDAT source.
    unique_only = colonized[colonized[m] != "Multiple colonizers"]
    ruler = (
        unique_only.groupby(m)
        .agg(
            unique_colony_year_rows=("Year", "size"),
            distinct_current_states=("Code", "nunique"),
            first_observed_year=("Year", "min"),
            last_observed_year=("Year", "max"),
        )
        .reset_index()
        .rename(columns={m: "colonizer"})
        .sort_values("unique_colony_year_rows", ascending=False)
        .reset_index(drop=True)
    )
    ruler["profile_is_lower_bound"] = True
    return state, ruler


def build_empire_counts(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"Entity", "Year"}
    if not required.issubset(df.columns):
        raise SystemExit(f"{path} missing {sorted(required - set(df.columns))}")
    m = measure_col(df)
    df[m] = pd.to_numeric(df[m], errors="coerce")
    df = df[df[m].notna() & df["Entity"].isin(EMPIRE_ISO3)].copy()
    out = (
        df.groupby("Entity")
        .agg(
            cumulative_colony_years_ruled=(m, "sum"),
            peak_colonies=(m, "max"),
            first_active_year=("Year", lambda s: int(s.min())),
            last_active_year=("Year", lambda s: int(s.max())),
            active_years=(m, lambda s: int((s > 0).sum())),
        )
        .reset_index()
        .rename(columns={"Entity": "colonizer"})
        .sort_values("cumulative_colony_years_ruled", ascending=False)
        .reset_index(drop=True)
    )
    out["iso3c"] = out["colonizer"].map(EMPIRE_ISO3)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", type=Path, required=True)
    parser.add_argument("--colonizer-year", type=Path)
    parser.add_argument("--empire-counts", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    former = build_former_colony(args.years)
    former.to_csv(args.output_dir / "COLDAT_FORMER_COLONY_EXPOSURE.csv", index=False)
    print(f"former-colony rows: {len(former)}")

    if args.colonizer_year:
        state, ruler = build_colonizer_identity(args.colonizer_year)
        state.to_csv(args.output_dir / "COLDAT_COLONIZER_IDENTITY.csv", index=False)
        ruler.to_csv(args.output_dir / "COLDAT_RULER_PROFILE_LOWER_BOUND.csv", index=False)
        print(f"colonized-state identity rows: {len(state)}; ruler rows: {len(ruler)}")

    if args.empire_counts:
        empire = build_empire_counts(args.empire_counts)
        empire.to_csv(args.output_dir / "COLDAT_IMPERIAL_INTENSITY_OWID_CHECK.csv", index=False)
        print(f"imperial-center rows: {len(empire)}")


if __name__ == "__main__":
    main()
