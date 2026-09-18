#!/usr/bin/env python3
"""Derive one audited unordered historical dyad row from CEPII Gravity V202211.

The official CSV distribution is a ~200 MB zip whose member expands to >1 GB.
This builder therefore reads only the required columns in chunks and collapses
history incrementally. It never loads the full Gravity panel into memory.

The confirmatory scientific-collaboration exposure is time-invariant historical
`col_dep_ever`; raw yearly/directional rows are collapsed to one current-state
unordered pair restricted to the preregistered COLDAT-anchored country universe.
"""

from __future__ import annotations

import argparse
import contextlib
import zipfile
from pathlib import Path
from typing import Iterator, TextIO

import numpy as np
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
BINARY = {
    "col_dep_ever",
    "sibling_ever",
    "comlang_off",
    "comlang_ethno",
    "contig",
    "col_dep_end_conflict",
    "comcol",
    "col45",
}


@contextlib.contextmanager
def open_csv(path: Path) -> Iterator[TextIO]:
    """Open plain CSV or the single/main CSV member of the official CEPII zip."""
    if path.suffix.lower() != ".zip":
        with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
            yield f
        return

    with zipfile.ZipFile(path) as zf:
        members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not members:
            raise SystemExit(f"No CSV member found in {path}")
        preferred = [n for n in members if Path(n).name == "Gravity_V202211.csv"]
        member = preferred[0] if preferred else sorted(members)[0]
        with zf.open(member, "r") as raw:
            import io

            with io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline="") as text:
                yield text


def header_columns(path: Path) -> list[str]:
    with open_csv(path) as f:
        return list(pd.read_csv(f, nrows=0).columns)


def collapse_chunk(chunk: pd.DataFrame, universe: set[str]) -> pd.DataFrame:
    chunk["iso3_o"] = chunk["iso3_o"].astype(str).str.upper()
    chunk["iso3_d"] = chunk["iso3_d"].astype(str).str.upper()
    chunk = chunk[
        chunk["iso3_o"].isin(universe)
        & chunk["iso3_d"].isin(universe)
        & (chunk["iso3_o"] != chunk["iso3_d"])
    ].copy()
    if chunk.empty:
        return pd.DataFrame()

    chunk["iso3_i"] = chunk[["iso3_o", "iso3_d"]].min(axis=1)
    chunk["iso3_j"] = chunk[["iso3_o", "iso3_d"]].max(axis=1)

    for c in BINARY.intersection(chunk.columns):
        chunk[c] = pd.to_numeric(chunk[c], errors="coerce")
    for c in ("dist", "col_dep_end_year", "year"):
        if c in chunk.columns:
            chunk[c] = pd.to_numeric(chunk[c], errors="coerce")

    agg: dict[str, object] = {}
    for c in BINARY.intersection(chunk.columns):
        agg[c] = "max"
    if "dist" in chunk.columns:
        # Distance is intended to be time-invariant. Keep min/max so the final
        # pass can audit that repeated panel rows agree before taking midpoint.
        agg["dist"] = ["min", "max"]
    if "col_dep_end_year" in chunk.columns:
        agg["col_dep_end_year"] = "max"
    if "year" in chunk.columns:
        agg["year"] = ["min", "max"]

    out = chunk.groupby(["iso3_i", "iso3_j"], as_index=False).agg(agg)
    if isinstance(out.columns, pd.MultiIndex):
        out.columns = [
            "_".join(str(v) for v in tup if v).rstrip("_")
            for tup in out.columns.to_flat_index()
        ]
    ren = {f"{c}_max": c for c in BINARY}
    ren.update(
        {
            "dist_min": "_dist_min",
            "dist_max": "_dist_max",
            "col_dep_end_year_max": "col_dep_end_year",
            "year_min": "_year_min",
            "year_max": "_year_max",
        }
    )
    return out.rename(columns=ren)


def final_collapse(partials: list[pd.DataFrame]) -> pd.DataFrame:
    if not partials:
        raise SystemExit("No CEPII rows survived the frozen country universe")
    df = pd.concat(partials, ignore_index=True)

    agg: dict[str, object] = {}
    for c in BINARY.intersection(df.columns):
        agg[c] = "max"
    if "_dist_min" in df.columns:
        agg["_dist_min"] = "min"
    if "_dist_max" in df.columns:
        agg["_dist_max"] = "max"
    if "col_dep_end_year" in df.columns:
        agg["col_dep_end_year"] = "max"
    if "_year_min" in df.columns:
        agg["_year_min"] = "min"
    if "_year_max" in df.columns:
        agg["_year_max"] = "max"

    out = df.groupby(["iso3_i", "iso3_j"], as_index=False).agg(agg)
    if "col_dep_ever" not in out.columns:
        raise SystemExit("Internal collapse error: no col_dep_ever in output")

    out["col_dep_ever"] = out["col_dep_ever"].fillna(0).astype(int)

    if "_dist_min" in out.columns and "_dist_max" in out.columns:
        # CEPII distance should be invariant across panel years/directions after
        # unordered collapse. Tiny floating differences are harmless.
        spread = (out["_dist_max"] - out["_dist_min"]).abs()
        bad = spread[(spread > 1e-6) & spread.notna()]
        if len(bad):
            print(
                f"WARNING: {len(bad)} dyads have time/direction-varying distance; "
                "storing midpoint and max spread for audit"
            )
        out["dist"] = (out["_dist_min"] + out["_dist_max"]) / 2.0
        out["dist_max_spread"] = spread
        out = out.drop(columns=["_dist_min", "_dist_max"])

    if "_year_min" in out.columns:
        out = out.rename(
            columns={
                "_year_min": "cepii_first_panel_year",
                "_year_max": "cepii_last_panel_year",
            }
        )

    out["pair_id"] = out["iso3_i"] + "__" + out["iso3_j"]
    order = ["pair_id", "iso3_i", "iso3_j"] + [
        c for c in out.columns if c not in {"pair_id", "iso3_i", "iso3_j"}
    ]
    return out[order].sort_values("pair_id").reset_index(drop=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("gravity_csv_or_zip", type=Path)
    p.add_argument("country_crosswalk_csv", type=Path)
    p.add_argument("output_csv", type=Path)
    p.add_argument("--chunksize", type=int, default=250_000)
    args = p.parse_args()

    countries = pd.read_csv(args.country_crosswalk_csv)
    if "iso3c" not in countries.columns:
        raise SystemExit("country crosswalk requires iso3c")
    if "status" in countries.columns:
        countries = countries[countries["status"].eq("RESOLVED")]
    universe = set(countries["iso3c"].dropna().astype(str).str.upper())

    columns = header_columns(args.gravity_csv_or_zip)
    missing = REQUIRED - set(columns)
    if missing:
        raise SystemExit(f"CEPII file missing required columns: {sorted(missing)}")
    usecols = [
        c
        for c in ["year", "iso3_o", "iso3_d", *OPTIONAL]
        if c in columns
    ]
    for c in REQUIRED:
        if c not in usecols:
            usecols.append(c)

    partials: list[pd.DataFrame] = []
    rows_read = 0
    rows_survived = 0
    with open_csv(args.gravity_csv_or_zip) as f:
        for chunk in pd.read_csv(
            f,
            usecols=usecols,
            chunksize=args.chunksize,
            low_memory=False,
        ):
            rows_read += len(chunk)
            part = collapse_chunk(chunk, universe)
            if not part.empty:
                rows_survived += len(part)
                partials.append(part)

    out = final_collapse(partials)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print(
        f"raw_panel_rows_read={rows_read} partial_pair_rows={rows_survived} "
        f"final_pairs={len(out)} colonial_ties={int(out['col_dep_ever'].sum())}"
    )
    print(args.output_csv)


if __name__ == "__main__":
    main()
