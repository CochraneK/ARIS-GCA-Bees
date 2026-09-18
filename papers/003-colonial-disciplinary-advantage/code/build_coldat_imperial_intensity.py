#!/usr/bin/env python3
"""Reconstruct imperial-center intensity from original COLDAT 3.0 wide data.

Uses the source's per-power maximum/last-date aggregation columns, matching the
preregistered use of OWID's last-date aggregation for the former-colony series.

For each of the eight European overseas colonial powers, derives cumulative
colony-years ruled, distinct colonies, ruler span, active years, and peak
simultaneous colonies. Historical-only: no modern research outcomes are read.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

POWERS = {
    "belgium": ("Belgium", "BEL"),
    "britain": ("United Kingdom", "GBR"),
    "france": ("France", "FRA"),
    "germany": ("Germany", "DEU"),
    "italy": ("Italy", "ITA"),
    "netherlands": ("Netherlands", "NLD"),
    "portugal": ("Portugal", "PRT"),
    "spain": ("Spain", "ESP"),
}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("coldat_tab", type=Path)
    p.add_argument("output_csv", type=Path)
    args = p.parse_args()

    df = pd.read_csv(args.coldat_tab)
    if "country" not in df.columns:
        raise SystemExit("COLDAT original file missing country column")

    rows: list[dict[str, object]] = []
    for key, (label, iso3c) in POWERS.items():
        active_col = f"col.{key}"
        start_col = f"colstart.{key}_max"
        end_col = f"colend.{key}_max"
        missing = [c for c in (active_col, start_col, end_col) if c not in df.columns]
        if missing:
            raise SystemExit(f"COLDAT source missing columns for {key}: {missing}")

        active = df[pd.to_numeric(df[active_col], errors="coerce").fillna(0).eq(1)].copy()
        active[start_col] = pd.to_numeric(active[start_col], errors="coerce")
        active[end_col] = pd.to_numeric(active[end_col], errors="coerce")
        complete = active.dropna(subset=[start_col, end_col]).copy()
        complete = complete[complete[end_col] >= complete[start_col]]

        intervals = [
            (int(round(s)), int(round(e)))
            for s, e in zip(complete[start_col], complete[end_col])
        ]
        if intervals:
            min_year = min(s for s, _ in intervals)
            max_year = max(e for _, e in intervals)
            counts = {
                year: sum(int(s <= year <= e) for s, e in intervals)
                for year in range(min_year, max_year + 1)
            }
            cumulative = int(sum(e - s + 1 for s, e in intervals))
            active_years = int(sum(v > 0 for v in counts.values()))
            peak = int(max(counts.values()))
        else:
            min_year = max_year = np.nan
            cumulative = 0
            active_years = 0
            peak = 0

        rows.append(
            {
                "colonizer_key": key,
                "colonizer": label,
                "iso3c": iso3c,
                "cumulative_colony_years_ruled": cumulative,
                "distinct_colonies": int(len(active)),
                "complete_interval_colonies": int(len(complete)),
                "incomplete_interval_colonies": int(len(active) - len(complete)),
                "ruler_start_year": min_year,
                "ruler_end_year": max_year,
                "active_ruler_years": active_years,
                "peak_simultaneous_colonies": peak,
                "date_aggregation": "COLDAT *_max columns; inclusive year intervals",
            }
        )

    out = pd.DataFrame(rows).sort_values(
        "cumulative_colony_years_ruled", ascending=False
    ).reset_index(drop=True)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print(out.to_string(index=False))
    print(args.output_csv)


if __name__ == "__main__":
    main()
