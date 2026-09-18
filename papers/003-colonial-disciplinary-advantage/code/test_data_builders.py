#!/usr/bin/env python3
"""Outcome-blind smoke tests for ARIS4C003 data builders.

Uses only synthetic rows. It guards source-schema tolerance, country-code
conversion, and CEPII unordered dyad collapse without opening research outcomes.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd

import build_coldat_exposures as coldat
import build_cepii_dyads as cepii
import build_primary_country_crosswalk as cc


def test_countrycode() -> None:
    expected = {"USA": "US", "GBR": "GB", "FRA": "FR", "DZA": "DZ", "NAM": "NA"}
    got = {k: cc.convert(k) for k in expected}
    if got != expected:
        raise AssertionError(f"ISO3->ISO2 conversion mismatch: got={got}, expected={expected}")


def test_owid_extra_metadata() -> None:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "years.csv"
        pd.DataFrame(
            [
                {
                    "Entity": "Alpha",
                    "Code": "AAA",
                    "Year": 2021,
                    "Years a country was an European overseas colony": 10,
                    "World region according to OWID": "X",
                },
                {
                    "Entity": "Alpha",
                    "Code": "AAA",
                    "Year": 2022,
                    "Years a country was an European overseas colony": 11,
                    "World region according to OWID": "X",
                },
                {
                    "Entity": "Beta",
                    "Code": "BBB",
                    "Year": 2022,
                    "Years a country was an European overseas colony": 0,
                    "World region according to OWID": "Y",
                },
            ]
        ).to_csv(p, index=False)
        out = coldat.build_former_colony(p)
        row = out.loc[out["iso3c"].eq("AAA")].iloc[0]
        assert row["years_colonized_total"] == 11
        assert row["ever_colonized"] == 1


def test_empire_count_metadata() -> None:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "counts.csv"
        pd.DataFrame(
            [
                {
                    "Entity": "United Kingdom",
                    "Code": "GBR",
                    "Year": 1900,
                    "Number of colonies": 3,
                    "World region according to OWID": "Europe",
                },
                {
                    "Entity": "United Kingdom",
                    "Code": "GBR",
                    "Year": 1901,
                    "Number of colonies": 4,
                    "World region according to OWID": "Europe",
                },
                {
                    "Entity": "France",
                    "Code": "FRA",
                    "Year": 1900,
                    "Number of colonies": 2,
                    "World region according to OWID": "Europe",
                },
            ]
        ).to_csv(p, index=False)
        out = coldat.build_empire_counts(p)
        uk = out.loc[out["iso3c"].eq("GBR")].iloc[0]
        assert uk["cumulative_colony_years_ruled"] == 7
        assert uk["peak_colonies"] == 4


def test_cepii_unordered_collapse() -> None:
    universe = {"USA", "FRA", "GBR"}
    chunk = pd.DataFrame(
        [
            {
                "year": 1990,
                "iso3_o": "USA",
                "iso3_d": "FRA",
                "col_dep_ever": 1,
                "sibling_ever": 0,
                "comlang_off": 0,
                "dist": 6000.0,
            },
            {
                "year": 1991,
                "iso3_o": "FRA",
                "iso3_d": "USA",
                "col_dep_ever": 1,
                "sibling_ever": 0,
                "comlang_off": 0,
                "dist": 6000.0,
            },
            {
                "year": 1990,
                "iso3_o": "GBR",
                "iso3_d": "FRA",
                "col_dep_ever": 0,
                "sibling_ever": 1,
                "comlang_off": 0,
                "dist": 350.0,
            },
        ]
    )
    part = cepii.collapse_chunk(chunk, universe)
    out = cepii.final_collapse([part])
    assert out["pair_id"].is_unique
    fr_us = out.loc[out["pair_id"].eq("FRA__USA")].iloc[0]
    assert fr_us["col_dep_ever"] == 1
    assert abs(fr_us["dist"] - 6000.0) < 1e-9


def main() -> None:
    test_countrycode()
    test_owid_extra_metadata()
    test_empire_count_metadata()
    test_cepii_unordered_collapse()
    print(
        {
            "status": "PASS",
            "tests": [
                "countrycode vector unwrap",
                "OWID full-CSV metadata tolerance",
                "OWID empire-count metadata tolerance",
                "CEPII unordered chunk collapse",
            ],
            "note": "synthetic only; no contemporary research outcomes",
        }
    )


if __name__ == "__main__":
    main()
