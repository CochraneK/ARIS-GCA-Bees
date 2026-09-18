#!/usr/bin/env python3
"""ARIS4C013 Pilot 0A: birth–death calendar-phase coupling in a Wikidata snapshot.

This is a *method/feasibility* pilot, not a population-representative mortality
study. It uses a third-party 2024-01-01 Wikidata-derived snapshot of humans with
P569 (birth) and P570 (death) claims. The extraction omitted Wikidata
timePrecision metadata, so low-precision/rounded dates remain a major threat.

Primary safeguards:
- require syntactically valid Gregorian day-level dates;
- restrict to CE 1800+ births, 1900–2023 deaths, ages 18–110;
- exclude Feb 29 in the 365-day primary phase analysis;
- estimate the independence null from observed birth/death day-of-year
  marginals within birth-decade × death-decade strata;
- repeat after excluding every record with day-of-month == 1 on either date;
- report date-heaping diagnostics prominently.
"""
from __future__ import annotations

import argparse
import calendar
import gzip
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

DAYMAP = {}
n = 0
for month in range(1, 13):
    for day in range(1, calendar.monthrange(2001, month)[1] + 1):
        DAYMAP[month * 100 + day] = n
        n += 1
assert n == 365

DATE_RE = r"^\+?(?P<year>\d+)-(?P<month>\d{2})-(?P<day>\d{2})"

class Accumulator:
    def __init__(self) -> None:
        self.n = 0
        self.observed = np.zeros(365, dtype=np.int64)
        self.strata = defaultdict(lambda: [np.zeros(365, dtype=np.int64), np.zeros(365, dtype=np.int64), 0])

    def add(self, bday: np.ndarray, dday: np.ndarray, byear: np.ndarray, dyear: np.ndarray) -> None:
        offsets = (dday - bday) % 365
        self.observed += np.bincount(offsets, minlength=365)
        self.n += len(offsets)
        bdec = (byear // 10) * 10
        ddec = (dyear // 10) * 10
        frame = pd.DataFrame({"bdec": bdec, "ddec": ddec, "bd": bday, "dd": dday})
        for (bdc, ddc), g in frame.groupby(["bdec", "ddec"], sort=False):
            entry = self.strata[(int(bdc), int(ddc))]
            entry[0] += np.bincount(g["bd"].to_numpy(), minlength=365)
            entry[1] += np.bincount(g["dd"].to_numpy(), minlength=365)
            entry[2] += len(g)

    def expected(self) -> np.ndarray:
        exp = np.zeros(365, dtype=float)
        for births, deaths, n_s in self.strata.values():
            if n_s == 0:
                continue
            # offset k means death_day = birth_day + k (mod 365)
            for k in range(365):
                exp[k] += float(np.dot(births, np.roll(deaths, -k))) / n_s
        return exp


def parse_parts(series: pd.Series) -> pd.DataFrame:
    parts = series.astype("string").str.extract(DATE_RE)
    return parts.apply(pd.to_numeric, errors="coerce")


def summarize(acc: Accumulator) -> dict:
    expected = acc.expected()
    obs = acc.observed.astype(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(expected > 0, obs / expected, np.nan)
        pearson = np.where(expected > 0, (obs - expected) / np.sqrt(expected), np.nan)

    signed = np.arange(365)
    signed = np.where(signed <= 182, signed, signed - 365)
    window = []
    for k in range(-30, 31):
        idx = k % 365
        window.append({
            "offset_days": int(k),
            "observed": int(obs[idx]),
            "expected": float(expected[idx]),
            "ratio": float(ratio[idx]),
            "pearson_residual": float(pearson[idx]),
        })

    return {
        "n": int(acc.n),
        "observed_same_month_day": int(obs[0]),
        "expected_same_month_day": float(expected[0]),
        "same_month_day_ratio": float(ratio[0]),
        "same_month_day_pearson_residual": float(pearson[0]),
        "phase_chisq_descriptive": float(np.nansum((obs - expected) ** 2 / np.where(expected > 0, expected, np.nan))),
        "offset_window": window,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--json-out", type=Path, required=True)
    ap.add_argument("--md-out", type=Path, required=True)
    ap.add_argument("--chunksize", type=int, default=250_000)
    args = ap.parse_args()

    primary = Accumulator()
    no_day1 = Accumulator()
    total_rows = 0
    valid_claim_dates = 0
    eligible_before_feb29 = 0
    excluded_feb29 = 0
    birth_day1 = death_day1 = both_day1 = 0
    birth_jan1 = death_jan1 = both_jan1 = 0
    samples = []

    usecols = ["id", "P569", "P570", "P27"]
    for chunk in pd.read_csv(args.input, compression="gzip", usecols=usecols, chunksize=args.chunksize, low_memory=False):
        total_rows += len(chunk)
        if len(samples) < 5:
            samples.extend(chunk[["P569", "P570"]].head(5 - len(samples)).fillna("").to_dict("records"))

        bp = parse_parts(chunk["P569"])
        dp = parse_parts(chunk["P570"])
        syntactic = bp.notna().all(axis=1) & dp.notna().all(axis=1)
        if not syntactic.any():
            continue
        bp = bp.loc[syntactic].astype(int)
        dp = dp.loc[syntactic].astype(int)

        # Gregorian validity. pandas supports this date range after our year restrictions.
        range_mask = (
            (bp.year >= 1800) & (bp.year <= 2023) &
            (dp.year >= 1900) & (dp.year <= 2023) &
            (dp.year >= bp.year)
        )
        bp, dp = bp.loc[range_mask], dp.loc[range_mask]
        if bp.empty:
            continue

        bdt = pd.to_datetime(dict(year=bp.year, month=bp.month, day=bp.day), errors="coerce")
        ddt = pd.to_datetime(dict(year=dp.year, month=dp.month, day=dp.day), errors="coerce")
        valid = bdt.notna() & ddt.notna()
        bp, dp = bp.loc[valid], dp.loc[valid]
        if bp.empty:
            continue
        valid_claim_dates += len(bp)

        age = dp.year.to_numpy() - bp.year.to_numpy()
        before_bday = (
            (dp.month.to_numpy() < bp.month.to_numpy()) |
            ((dp.month.to_numpy() == bp.month.to_numpy()) & (dp.day.to_numpy() < bp.day.to_numpy()))
        )
        age = age - before_bday.astype(int)
        age_mask = (age >= 18) & (age <= 110)
        bp, dp = bp.iloc[np.flatnonzero(age_mask)], dp.iloc[np.flatnonzero(age_mask)]
        if bp.empty:
            continue

        eligible_before_feb29 += len(bp)
        b_day1 = bp.day.to_numpy() == 1
        d_day1 = dp.day.to_numpy() == 1
        birth_day1 += int(b_day1.sum())
        death_day1 += int(d_day1.sum())
        both_day1 += int((b_day1 & d_day1).sum())
        b_jan1 = (bp.month.to_numpy() == 1) & b_day1
        d_jan1 = (dp.month.to_numpy() == 1) & d_day1
        birth_jan1 += int(b_jan1.sum())
        death_jan1 += int(d_jan1.sum())
        both_jan1 += int((b_jan1 & d_jan1).sum())

        leap = ((bp.month.to_numpy() == 2) & (bp.day.to_numpy() == 29)) | ((dp.month.to_numpy() == 2) & (dp.day.to_numpy() == 29))
        excluded_feb29 += int(leap.sum())
        keep = ~leap
        bp, dp = bp.iloc[np.flatnonzero(keep)], dp.iloc[np.flatnonzero(keep)]
        if bp.empty:
            continue

        bcode = bp.month.to_numpy() * 100 + bp.day.to_numpy()
        dcode = dp.month.to_numpy() * 100 + dp.day.to_numpy()
        bdoy = np.fromiter((DAYMAP[int(x)] for x in bcode), dtype=np.int16, count=len(bcode))
        ddoy = np.fromiter((DAYMAP[int(x)] for x in dcode), dtype=np.int16, count=len(dcode))
        by = bp.year.to_numpy(dtype=np.int32)
        dy = dp.year.to_numpy(dtype=np.int32)

        primary.add(bdoy, ddoy, by, dy)

        strict = (bp.day.to_numpy() != 1) & (dp.day.to_numpy() != 1)
        if strict.any():
            idx = np.flatnonzero(strict)
            no_day1.add(bdoy[idx], ddoy[idx], by[idx], dy[idx])

    result = {
        "pilot": "ARIS4C013 Wikidata Pilot 0A",
        "source_snapshot": "dalager/wikidata-incarnations; derived from Wikidata 2024-01-01 dump",
        "claim_scope": "method/feasibility only; not population-representative",
        "total_csv_rows": int(total_rows),
        "syntactically_and_gregorian_valid_after_year_range": int(valid_claim_dates),
        "eligible_age_18_110_before_feb29": int(eligible_before_feb29),
        "excluded_any_feb29": int(excluded_feb29),
        "heaping": {
            "birth_day1": int(birth_day1),
            "death_day1": int(death_day1),
            "both_day1": int(both_day1),
            "birth_jan1": int(birth_jan1),
            "death_jan1": int(death_jan1),
            "both_jan1": int(both_jan1),
            "birth_day1_rate": birth_day1 / eligible_before_feb29 if eligible_before_feb29 else math.nan,
            "death_day1_rate": death_day1 / eligible_before_feb29 if eligible_before_feb29 else math.nan,
            "birth_jan1_rate": birth_jan1 / eligible_before_feb29 if eligible_before_feb29 else math.nan,
            "death_jan1_rate": death_jan1 / eligible_before_feb29 if eligible_before_feb29 else math.nan,
        },
        "primary": summarize(primary),
        "sensitivity_exclude_day1_either_date": summarize(no_day1),
        "raw_date_samples": samples,
        "warnings": [
            "Wikidata biographies are a highly selected notable-person sample.",
            "The slim extraction omits Wikidata timePrecision metadata.",
            "Same-day excess can be inflated by rounded or conventionally assigned dates.",
            "The chi-square and Pearson residuals are descriptive here; confirmatory inference requires a prespecified population dataset or richer precision metadata.",
        ],
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    p = result["primary"]
    s = result["sensitivity_exclude_day1_either_date"]
    h = result["heaping"]
    lines = [
        "# ARIS4C013 · Wikidata Pilot 0A",
        "",
        "**Interpretation ceiling:** method/feasibility pilot on a selected notable-person dataset; not population mortality evidence.",
        "",
        "## Sample",
        f"- raw rows: {result['total_csv_rows']:,}",
        f"- eligible age/date records before Feb-29 exclusion: {result['eligible_age_18_110_before_feb29']:,}",
        f"- primary 365-day phase sample: {p['n']:,}",
        f"- sensitivity sample excluding day=1 on either date: {s['n']:,}",
        "",
        "## Same month-day coupling",
        f"- primary observed: {p['observed_same_month_day']:,}",
        f"- primary expected under birth-decade × death-decade marginal independence: {p['expected_same_month_day']:.1f}",
        f"- primary O/E ratio: **{p['same_month_day_ratio']:.4f}**",
        f"- no-day-1 sensitivity O/E ratio: **{s['same_month_day_ratio']:.4f}**",
        "",
        "## Date-heaping diagnostics",
        f"- birth day=1 rate: {h['birth_day1_rate']:.4%}",
        f"- death day=1 rate: {h['death_day1_rate']:.4%}",
        f"- birth Jan-1 rate: {h['birth_jan1_rate']:.4%}",
        f"- death Jan-1 rate: {h['death_jan1_rate']:.4%}",
        f"- records with Jan-1 for both birth and death: {h['both_jan1']:,}",
        "",
        "## ±30-day phase window",
        "| offset | observed | expected | O/E |",
        "|---:|---:|---:|---:|",
    ]
    for row in p["offset_window"]:
        lines.append(f"| {row['offset_days']} | {row['observed']:,} | {row['expected']:.1f} | {row['ratio']:.4f} |")
    lines += [
        "",
        "## Warnings",
        *[f"- {w}" for w in result["warnings"]],
        "",
        "A signal that vanishes after the day=1 sensitivity filter is treated as date-precision/heaping evidence, not a birthday effect.",
    ]
    args.md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:28]))
    print(f"\nFull report: {args.md_out}")

if __name__ == "__main__":
    main()
