#!/usr/bin/env python3
"""Derive one audited unordered historical dyad row from CEPII Gravity V202211.

The raw Gravity panel repeats bilateral history over years and directions. The
confirmatory scientific-collaboration exposure is time-invariant historical
`col_dep_ever`; this script collapses it to one current-state unordered pair,
restricted to the preregistered COLDAT-anchored country universe.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED = {"iso3_o", "iso3_d", "col_dep_ever"}
OPTIONAL = [
    "sibling_ever",
    "comlang_off",
    "comlang_ethno",
    "contig",
    "dist",
    "col_dep_end_year",
    "col_dep_end_conflict",
    "comcol",
    "col45",
]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("gravity_csv", type=Path)
    p.add_argument("country_crosswalk_csv", type=Path)
    p.add_argument("output_csv", type=Path)
    args = p.parse_args()

    countries = pd.read_csv(args.country_crosswalk_csv)
    if "iso3c" not in countries.columns:
        raise SystemExit("country crosswalk requires iso3c")
    universe = set(countries["iso3c"].dropna().astype(str).str.upper())

    header = pd.read_csv(args.gravity_csv, nrows=0)
    missing = REQUIRED - set(header.columns)
    if missing:
        raise SystemExit(f"CEPII file missing required columns: {sorted(missing)}")
    usecols = [c for c in ["year", "iso3_o", "iso3_d", *OPTIONAL] if c in header.columns]
    for c in REQUIRED:
        if c not in usecols:
            usecols.append(c)

    # Gravity can be very large; select only necessary columns at read time.
    df = pd.read_csv(args.gravity_csv, usecols=usecols, low_memory=False)
    df["iso3_o"] = df["iso3_o"].astype(str).str.upper()
    df["iso3_d"] = df["iso3_d"].astype(str).str.upper()
    df = df[
        df["iso3_o"].isin(universe)
        & df["iso3_d"].isin(universe)
        & (df["iso3_o"] != df["iso3_d"])
    ].copy()

    df["iso3_i"] = df[["iso3_o", "iso3_d"]].min(axis=1)
    df["iso3_j"] = df[["iso3_o", "iso3_d"]].max(axis=1)

    binary_candidates = [
        c for c in ["col_dep_ever", "sibling_ever", "comlang_off", "comlang_ethno", "contig", "comcol", "col45", "col_dep_end_conflict"]
        if c in df.columns
    ]
    for c in binary_candidates:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    agg: dict[str, object] = {c: "max" for c in binary_candidates}
    if "dist" in df.columns:
        df["dist"] = pd.to_numeric(df["dist"], errors="coerce")
        agg["dist"] = "median"
    if "col_dep_end_year" in df.columns:
        df["col_dep_end_year"] = pd.to_numeric(df["col_dep_end_year"], errors="coerce")
        agg["col_dep_end_year"] = "max"
    if "year" in df.columns:
        agg["year"] = ["min", "max"]

    out = df.groupby(["iso3_i", "iso3_j"], as_index=False).agg(agg)
    if isinstance(out.columns, pd.MultiIndex):
        out.columns = [
            "_".join(str(v) for v in tup if v).rstrip("_")
            for tup in out.columns.to_flat_index()
        ]
        out = out.rename(columns={"iso3_i_": "iso3_i", "iso3_j_": "iso3_j"})

    # Normalize expected names after possible MultiIndex aggregation.
    rename = {
        "col_dep_ever_max": "col_dep_ever",
        "sibling_ever_max": "sibling_ever",
        "comlang_off_max": "comlang_off",
        "comlang_ethno_max": "comlang_ethno",
        "contig_max": "contig",
        "comcol_max": "comcol",
        "col45_max": "col45",
        "col_dep_end_conflict_max": "col_dep_end_conflict",
        "dist_median": "dist",
        "col_dep_end_year_max": "col_dep_end_year",
        "year_min": "cepii_first_panel_year",
        "year_max": "cepii_last_panel_year",
    }
    out = out.rename(columns=rename)
    if "col_dep_ever" not in out.columns:
        raise SystemExit("Internal collapse error: no col_dep_ever in output")

    out["col_dep_ever"] = out["col_dep_ever"].fillna(0).astype(int)
    out["pair_id"] = out["iso3_i"] + "__" + out["iso3_j"]
    order = ["pair_id", "iso3_i", "iso3_j"] + [
        c for c in out.columns if c not in {"pair_id", "iso3_i", "iso3_j"}
    ]
    out = out[order].sort_values("pair_id").reset_index(drop=True)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print(f"pairs={len(out)} colonial_ties={int(out['col_dep_ever'].sum())}")
    print(args.output_csv)


if __name__ == "__main__":
    main()
