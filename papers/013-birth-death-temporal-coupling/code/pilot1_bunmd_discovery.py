#!/usr/bin/env python3
"""ARIS4C013 Pilot 1 discovery analysis on BUNMD.

Locked discovery years: 1988-1996.
Untouched holdout: 1997-2005 (read only to discard; never summarized here).
"""
from __future__ import annotations

import argparse
import calendar
import json
import math
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

DISCOVERY_YEARS = tuple(range(1988, 1997))
BIRTH_HEAP_DAYS = {1, 15}
DEATH_HEAP_DAYS = {1, 4, 15}
PHASE_SAFE_MIN_YEAR_GAP = 19
PHASE_SAFE_MAX_YEAR_GAP = 110

# 0-based day of year for a canonical non-leap year.
MONTH_START = np.array([0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], dtype=np.int16)
DAYS_COMMON = np.array([0,31,28,31,30,31,30,31,31,30,31,30,31], dtype=np.int16)


def is_leap_year(y: np.ndarray) -> np.ndarray:
    return (y % 4 == 0) & ((y % 100 != 0) | (y % 400 == 0))


def valid_gregorian(y: np.ndarray, m: np.ndarray, d: np.ndarray) -> np.ndarray:
    ok_m = (m >= 1) & (m <= 12)
    maxd = np.zeros_like(d)
    idx = np.flatnonzero(ok_m)
    if len(idx):
        maxd[idx] = DAYS_COMMON[m[idx]]
        feb = idx[m[idx] == 2]
        if len(feb):
            maxd[feb] += is_leap_year(y[feb]).astype(maxd.dtype)
    return ok_m & (d >= 1) & (d <= maxd)


def month_day_to_doy(m: np.ndarray, d: np.ndarray) -> np.ndarray:
    return MONTH_START[m] + d - 1


def phase_safe_year_gap(byear: np.ndarray, dyear: np.ndarray) -> np.ndarray:
    """Eligibility independent of birth/death month-day pairing.

    Using exact attained-age filtering at the lower/upper boundary can itself
    induce birth-death phase dependence.  Year gaps 19..110 guarantee that
    every valid month/day pairing corresponds to an attained age of 18..110.
    """
    gap = dyear - byear
    return (gap >= PHASE_SAFE_MIN_YEAR_GAP) & (gap <= PHASE_SAFE_MAX_YEAR_GAP)


class PhaseAccumulator:
    def __init__(self) -> None:
        self.n = 0
        self.observed = np.zeros(365, dtype=np.int64)
        self.observed_by_year = {y: np.zeros(365, dtype=np.int64) for y in DISCOVERY_YEARS}
        # key -> [birth phase counts, death phase counts, n]
        self.strata = defaultdict(lambda: [np.zeros(365, dtype=np.int64), np.zeros(365, dtype=np.int64), 0])

    def add(self, bdoy, ddoy, byear, dyear, sex):
        offsets = (ddoy - bdoy) % 365
        self.observed += np.bincount(offsets, minlength=365)
        self.n += len(offsets)
        for y in np.unique(dyear):
            mask = dyear == y
            self.observed_by_year[int(y)] += np.bincount(offsets[mask], minlength=365)

        frame = pd.DataFrame(
            {
                "byear": byear,
                "dyear": dyear,
                "sex": sex,
                "bdoy": bdoy,
                "ddoy": ddoy,
            }
        )
        for (by, dy, sx), g in frame.groupby(
            ["byear", "dyear", "sex"], sort=False, dropna=False
        ):
            key = (int(by), int(dy), int(sx))
            entry = self.strata[key]
            entry[0] += np.bincount(g["bdoy"].to_numpy(), minlength=365)
            entry[1] += np.bincount(g["ddoy"].to_numpy(), minlength=365)
            entry[2] += len(g)

    @staticmethod
    def _expected_one(births, deaths, n):
        out = np.empty(365, dtype=float)
        for k in range(365):
            out[k] = float(np.dot(births, np.roll(deaths, -k))) / n
        return out

    def expected(self, dyear=None, strata=None):
        out = np.zeros(365, dtype=float)
        source = self.strata if strata is None else strata
        for (_by, dy, _sx), (b, d, n) in source.items():
            if dyear is not None and dy != dyear:
                continue
            if n:
                out += self._expected_one(b, d, n)
        return out

    def birth_decade_strata(self):
        """Aggregate the primary exact-birth-year strata for a coarse sensitivity null."""
        out = defaultdict(
            lambda: [
                np.zeros(365, dtype=np.int64),
                np.zeros(365, dtype=np.int64),
                0,
            ]
        )
        for (by, dy, sx), (b, d, n) in self.strata.items():
            key = ((by // 10) * 10, dy, sx)
            entry = out[key]
            entry[0] += b
            entry[1] += d
            entry[2] += n
        return out

    def summarize(self):
        exp = self.expected()
        decade_strata = self.birth_decade_strata()
        exp_decade = self.expected(strata=decade_strata)
        obs = self.observed.astype(float)
        ratio = np.divide(obs, exp, out=np.full(365, np.nan), where=exp > 0)
        by_year = {}
        for y in DISCOVERY_YEARS:
            ey = self.expected(y)
            oy = self.observed_by_year[y].astype(float)
            by_year[str(y)] = {
                "n": int(oy.sum()),
                "observed_offset0": int(oy[0]),
                "expected_offset0": float(ey[0]),
                "oe_offset0": float(oy[0] / ey[0]) if ey[0] else math.nan,
            }
        decade_by_year = {}
        for y in DISCOVERY_YEARS:
            ey = self.expected(y, strata=decade_strata)
            oy = self.observed_by_year[y].astype(float)
            decade_by_year[str(y)] = {
                "expected_offset0": float(ey[0]),
                "oe_offset0": float(oy[0] / ey[0]) if ey[0] else math.nan,
            }

        return {
            "n": int(self.n),
            "observed_offset0": int(obs[0]),
            "expected_offset0": float(exp[0]),
            "oe_offset0": float(ratio[0]),
            "null_model": "exact birth year × death year × sex",
            "birth_decade_null_sensitivity": {
                "expected_offset0": float(exp_decade[0]),
                "oe_offset0": float(obs[0] / exp_decade[0]) if exp_decade[0] else math.nan,
                "by_death_year": decade_by_year,
            },
            "offset_window": [
                {
                    "offset": k,
                    "observed": int(obs[k % 365]),
                    "expected": float(exp[k % 365]),
                    "oe": float(ratio[k % 365]),
                }
                for k in range(-30, 31)
            ],
            "by_death_year": by_year,
        }


def pick_csv_member(zf: zipfile.ZipFile) -> str:
    members = [x for x in zf.infolist() if not x.is_dir() and x.filename.lower().endswith(".csv")]
    if not members:
        raise RuntimeError("No CSV found in BUNMD archive")
    members.sort(key=lambda x: x.file_size, reverse=True)
    return members[0].filename


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", type=Path, required=True)
    ap.add_argument("--json-out", type=Path, required=True)
    ap.add_argument("--md-out", type=Path, required=True)
    ap.add_argument("--chunksize", type=int, default=1_000_000)
    args = ap.parse_args()

    raw = PhaseAccumulator()
    strict = PhaseAccumulator()

    counts = {
        "rows_read": 0,
        "discovery_year_rows": 0,
        "complete_components": 0,
        "valid_gregorian": 0,
        "exact_age_18_110_diagnostic": 0,
        "phase_safe_year_gap_19_110": 0,
        "boundary_adult_excluded": 0,
        "feb29_excluded": 0,
    }
    bday_hist = np.zeros(32, dtype=np.int64)
    dday_hist = np.zeros(32, dtype=np.int64)

    usecols = ["byear","bmonth","bday","dyear","dmonth","dday","sex"]

    with zipfile.ZipFile(args.zip) as zf:
        member = pick_csv_member(zf)
        info = zf.getinfo(member)
        print(f"Using archive member: {member} ({info.file_size/1024/1024/1024:.2f} GiB uncompressed)")
        with zf.open(member) as fh:
            for chunk_i, chunk in enumerate(pd.read_csv(fh, usecols=usecols, chunksize=args.chunksize, low_memory=False), 1):
                counts["rows_read"] += len(chunk)
                # Convert only the seven required fields; missing values become NaN.
                for c in usecols:
                    chunk[c] = pd.to_numeric(chunk[c], errors="coerce")

                dy = chunk["dyear"]
                discovery = dy.isin(DISCOVERY_YEARS)
                if not discovery.any():
                    continue
                chunk = chunk.loc[discovery, usecols]
                counts["discovery_year_rows"] += len(chunk)

                complete = chunk[["byear","bmonth","bday","dyear","dmonth","dday"]].notna().all(axis=1)
                chunk = chunk.loc[complete]
                counts["complete_components"] += len(chunk)
                if chunk.empty:
                    continue

                by = chunk.byear.to_numpy(dtype=np.int32)
                bm = chunk.bmonth.to_numpy(dtype=np.int16)
                bd = chunk.bday.to_numpy(dtype=np.int16)
                dy = chunk.dyear.to_numpy(dtype=np.int32)
                dm = chunk.dmonth.to_numpy(dtype=np.int16)
                dd = chunk.dday.to_numpy(dtype=np.int16)
                sx = chunk.sex.fillna(0).to_numpy(dtype=np.int16)

                valid = valid_gregorian(by,bm,bd) & valid_gregorian(dy,dm,dd)
                if not valid.any():
                    continue
                by,bm,bd,dy,dm,dd,sx = [x[valid] for x in (by,bm,bd,dy,dm,dd,sx)]
                counts["valid_gregorian"] += len(by)

                age = dy - by - (((dm < bm) | ((dm == bm) & (dd < bd))).astype(np.int32))
                exact_adult = (age >= 18) & (age <= 110)
                counts["exact_age_18_110_diagnostic"] += int(exact_adult.sum())

                phase_safe = phase_safe_year_gap(by, dy)
                counts["phase_safe_year_gap_19_110"] += int(phase_safe.sum())
                counts["boundary_adult_excluded"] += int((exact_adult & ~phase_safe).sum())
                by,bm,bd,dy,dm,dd,sx = [x[phase_safe] for x in (by,bm,bd,dy,dm,dd,sx)]
                if not len(by):
                    continue

                bday_hist += np.bincount(bd, minlength=32)[:32]
                dday_hist += np.bincount(dd, minlength=32)[:32]

                feb29 = ((bm == 2) & (bd == 29)) | ((dm == 2) & (dd == 29))
                counts["feb29_excluded"] += int(feb29.sum())
                keep = ~feb29
                by,bm,bd,dy,dm,dd,sx = [x[keep] for x in (by,bm,bd,dy,dm,dd,sx)]
                if not len(by):
                    continue

                bdoy = month_day_to_doy(bm,bd).astype(np.int16)
                ddoy = month_day_to_doy(dm,dd).astype(np.int16)
                raw.add(bdoy,ddoy,by,dy,sx)

                strict_mask = (~np.isin(bd, list(BIRTH_HEAP_DAYS))) & (~np.isin(dd, list(DEATH_HEAP_DAYS)))
                if strict_mask.any():
                    idx=np.flatnonzero(strict_mask)
                    strict.add(bdoy[idx],ddoy[idx],by[idx],dy[idx],sx[idx])

                if chunk_i % 10 == 0:
                    print(f"chunks={chunk_i} rows_read={counts['rows_read']:,} phase_safe={counts['phase_safe_year_gap_19_110']:,}", flush=True)

    result = {
        "pilot": "ARIS4C013 BUNMD Pilot 1 discovery",
        "discovery_years": [1988,1996],
        "holdout_years_untouched": [1997,2005],
        "counts": counts,
        "eligibility_primary": "valid complete dates with death_year - birth_year in 19..110; inclusion is month/day independent",
        "null_model_primary": "exact birth year × death year × sex marginal independence",
        "null_model_sensitivity": "birth decade × death year × sex marginal independence",
        "prespecified_heaping_flags": {
            "birth_days": sorted(BIRTH_HEAP_DAYS),
            "death_days": sorted(DEATH_HEAP_DAYS),
        },
        "birth_day_of_month_counts": {str(i): int(bday_hist[i]) for i in range(1,32)},
        "death_day_of_month_counts": {str(i): int(dday_hist[i]) for i in range(1,32)},
        "raw": raw.summarize(),
        "strict": strict.summarize(),
        "interpretation_ceiling": "exploratory administrative discovery; no Bazi/traditional-calendar test",
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    r=result["raw"]; s=result["strict"]
    lines=[
        "# ARIS4C013 · BUNMD Pilot 1 discovery",
        "",
        "**Discovery only: deaths 1988–1996. The 1997–2005 temporal holdout was not summarized or tested.**",
        "",
        "## Sample",
        f"- rows in discovery death years: {counts['discovery_year_rows']:,}",
        f"- exact-age 18–110 records (diagnostic only): {counts['exact_age_18_110_diagnostic']:,}",
        f"- phase-safe year-gap 19–110 records before Feb-29 exclusion: {counts['phase_safe_year_gap_19_110']:,}",
        f"- exact-age boundary records excluded to prevent selection-induced phase bias: {counts['boundary_adult_excluded']:,}",
        f"- raw phase sample: {r['n']:,}",
        f"- strict phase sample: {s['n']:,}",
        "",
        "## Offset 0 (same Gregorian month/day)",
        f"- raw observed / expected: {r['observed_offset0']:,} / {r['expected_offset0']:.1f}",
        f"- raw O/E under primary exact-birth-year null: **{r['oe_offset0']:.4f}**",
        f"- raw O/E under birth-decade sensitivity null: **{r['birth_decade_null_sensitivity']['oe_offset0']:.4f}**",
        f"- strict observed / expected: {s['observed_offset0']:,} / {s['expected_offset0']:.1f}",
        f"- strict O/E under primary exact-birth-year null: **{s['oe_offset0']:.4f}**",
        f"- strict O/E under birth-decade sensitivity null: **{s['birth_decade_null_sensitivity']['oe_offset0']:.4f}**",
        "",
        "## Prespecified heaping dates",
        f"- birth day 1: {bday_hist[1]:,}",
        f"- birth day 15: {bday_hist[15]:,}",
        f"- death day 1: {dday_hist[1]:,}",
        f"- death day 4: {dday_hist[4]:,}",
        f"- death day 15: {dday_hist[15]:,}",
        "",
        "## Strict offset-0 O/E by death year",
        "| death year | n | observed | expected | O/E |",
        "|---:|---:|---:|---:|---:|",
    ]
    for y,v in s["by_death_year"].items():
        lines.append(f"| {y} | {v['n']:,} | {v['observed_offset0']:,} | {v['expected_offset0']:.1f} | {v['oe_offset0']:.4f} |")
    lines += [
        "",
        "## Strict ±30-day window",
        "| offset | observed | expected | O/E |",
        "|---:|---:|---:|---:|",
    ]
    for v in s["offset_window"]:
        lines.append(f"| {v['offset']} | {v['observed']:,} | {v['expected']:.1f} | {v['oe']:.4f} |")
    lines += [
        "",
        "## Interpretation rules",
        "- Raw-to-strict shrinkage is treated as evidence of administrative date artifacts.",
        "- A strict elevation is only a candidate birthday/anniversary signal if reasonably stable across discovery years.",
        "- No discovery result is called replicated before the locked 1997–2005 holdout is evaluated once.",
        "- No Bazi or traditional-calendar feature is tested here.",
    ]
    args.md_out.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print("\n".join(lines[:32]))
    print(f"Report written to {args.md_out}")

if __name__ == "__main__":
    main()
