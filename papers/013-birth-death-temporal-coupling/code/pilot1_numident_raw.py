#!/usr/bin/env python3
"""ARIS4C013 Pilot 1 discovery on raw public-use NUMIDENT death files.

Expected inputs:
  NUMDEATH01-10_PU.zip
  NUMDEATH11-20_PU.zip

Discovery: death years 1988-1996.
Holdout: death years 1997-2005; this script never summarizes it.
"""
from __future__ import annotations

import argparse
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

# Zero-based, half-open slices translated from the published 1-based Stata
# infix positions in hollina/duke-replication, 1_process_raw_data.do.
FIELD_SPECS = {
    "bmonth": (96, 98),
    "bday": (98, 100),
    "byear": (100, 104),
    "sex": (104, 105),
    "proof_death": (116, 117),
    "dob_exception": (136, 137),
    "special_exception": (137, 138),
    "mbr_dob_exception": (138, 139),
    "death_source": (141, 143),
    "verified_edr": (143, 144),
    "dmonth": (144, 146),
    "dday": (146, 148),
    "dyear": (148, 152),
}
NAMES = list(FIELD_SPECS)
COLSPECS = [FIELD_SPECS[n] for n in NAMES]

MONTH_START = np.array(
    [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334],
    dtype=np.int16,
)
DAYS_COMMON = np.array(
    [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    dtype=np.int16,
)


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


def read_member_chunks(fh, chunksize: int):
    yield from pd.read_fwf(
        fh,
        colspecs=COLSPECS,
        names=NAMES,
        dtype="string",
        chunksize=chunksize,
    )


class PhaseAccumulator:
    def __init__(self) -> None:
        self.n = 0
        self.observed = np.zeros(365, dtype=np.int64)
        self.observed_by_year = {
            y: np.zeros(365, dtype=np.int64) for y in DISCOVERY_YEARS
        }
        self.strata = defaultdict(
            lambda: [
                np.zeros(365, dtype=np.int64),
                np.zeros(365, dtype=np.int64),
                0,
            ]
        )

    def add(self, bdoy, ddoy, byear, dyear, sex):
        offsets = (ddoy - bdoy) % 365
        self.observed += np.bincount(offsets, minlength=365)
        self.n += len(offsets)

        for y in np.unique(dyear):
            mask = dyear == y
            self.observed_by_year[int(y)] += np.bincount(
                offsets[mask], minlength=365
            )

        frame = pd.DataFrame(
            {
                "bdec": (byear // 10) * 10,
                "dyear": dyear,
                "sex": sex,
                "bdoy": bdoy,
                "ddoy": ddoy,
            }
        )
        for (bdec, dy, sx), g in frame.groupby(
            ["bdec", "dyear", "sex"], sort=False, dropna=False
        ):
            key = (int(bdec), int(dy), int(sx))
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

    def expected(self, dyear=None):
        out = np.zeros(365, dtype=float)
        for (_bdec, dy, _sx), (b, d, n) in self.strata.items():
            if dyear is not None and dy != dyear:
                continue
            if n:
                out += self._expected_one(b, d, n)
        return out

    def summarize(self):
        exp = self.expected()
        obs = self.observed.astype(float)
        ratio = np.divide(
            obs, exp, out=np.full(365, np.nan), where=exp > 0
        )
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
        return {
            "n": int(self.n),
            "observed_offset0": int(obs[0]),
            "expected_offset0": float(exp[0]),
            "oe_offset0": float(ratio[0]),
            "offset_window": [
                {
                    "offset": int(k),
                    "observed": int(obs[k % 365]),
                    "expected": float(exp[k % 365]),
                    "oe": float(ratio[k % 365]),
                }
                for k in range(-30, 31)
            ],
            "by_death_year": by_year,
        }


def text_members(zf: zipfile.ZipFile) -> list[str]:
    members = [
        x.filename
        for x in zf.infolist()
        if (not x.is_dir())
        and x.filename.upper().endswith("_PU.TXT")
        and "NUMDEATH" in x.filename.upper()
    ]
    if not members:
        raise RuntimeError("No NUMDEATH*_PU.txt members found in archive")
    return sorted(members)


def count_codes(series: pd.Series, dest: dict[str, int]) -> None:
    vals = series.fillna("").astype(str).str.strip()
    for key, n in vals.value_counts(dropna=False).items():
        dest[str(key)] = dest.get(str(key), 0) + int(n)


def process_chunk(chunk, raw, strict, counts, diagnostics):
    counts["rows_read"] += len(chunk)

    numeric = ["byear", "bmonth", "bday", "dyear", "dmonth", "dday", "sex"]
    for c in numeric:
        chunk[c] = pd.to_numeric(chunk[c], errors="coerce")

    discovery = chunk["dyear"].isin(DISCOVERY_YEARS)
    if not discovery.any():
        return
    chunk = chunk.loc[discovery].copy()
    counts["discovery_year_rows"] += len(chunk)

    complete = chunk[
        ["byear", "bmonth", "bday", "dyear", "dmonth", "dday"]
    ].notna().all(axis=1)
    chunk = chunk.loc[complete].copy()
    counts["complete_components"] += len(chunk)
    if chunk.empty:
        return

    for c in [
        "dob_exception",
        "special_exception",
        "mbr_dob_exception",
        "death_source",
        "verified_edr",
        "proof_death",
    ]:
        count_codes(chunk[c], diagnostics[c])

    by = chunk.byear.to_numpy(dtype=np.int32)
    bm = chunk.bmonth.to_numpy(dtype=np.int16)
    bd = chunk.bday.to_numpy(dtype=np.int16)
    dy = chunk.dyear.to_numpy(dtype=np.int32)
    dm = chunk.dmonth.to_numpy(dtype=np.int16)
    dd = chunk.dday.to_numpy(dtype=np.int16)
    sx = chunk.sex.fillna(0).to_numpy(dtype=np.int16)

    valid = valid_gregorian(by, bm, bd) & valid_gregorian(dy, dm, dd)
    by, bm, bd, dy, dm, dd, sx = [
        x[valid] for x in (by, bm, bd, dy, dm, dd, sx)
    ]
    counts["valid_gregorian"] += len(by)
    if not len(by):
        return

    age = dy - by - (
        (dm < bm) | ((dm == bm) & (dd < bd))
    ).astype(np.int32)
    adult = (age >= 18) & (age <= 110)
    by, bm, bd, dy, dm, dd, sx = [
        x[adult] for x in (by, bm, bd, dy, dm, dd, sx)
    ]
    counts["age_18_110"] += len(by)
    if not len(by):
        return

    diagnostics["birth_day_hist"] += np.bincount(bd, minlength=32)[:32]
    diagnostics["death_day_hist"] += np.bincount(dd, minlength=32)[:32]

    feb29 = ((bm == 2) & (bd == 29)) | ((dm == 2) & (dd == 29))
    counts["feb29_excluded"] += int(feb29.sum())
    keep = ~feb29
    by, bm, bd, dy, dm, dd, sx = [
        x[keep] for x in (by, bm, bd, dy, dm, dd, sx)
    ]
    if not len(by):
        return

    bdoy = month_day_to_doy(bm, bd).astype(np.int16)
    ddoy = month_day_to_doy(dm, dd).astype(np.int16)
    raw.add(bdoy, ddoy, by, dy, sx)

    strict_mask = (
        ~np.isin(bd, list(BIRTH_HEAP_DAYS))
        & ~np.isin(dd, list(DEATH_HEAP_DAYS))
    )
    if strict_mask.any():
        idx = np.flatnonzero(strict_mask)
        strict.add(bdoy[idx], ddoy[idx], by[idx], dy[idx], sx[idx])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--zip",
        dest="zips",
        type=Path,
        action="append",
        required=True,
        help="Repeat for each NUMDEATH archive.",
    )
    ap.add_argument("--json-out", type=Path, required=True)
    ap.add_argument("--md-out", type=Path, required=True)
    ap.add_argument("--chunksize", type=int, default=750_000)
    args = ap.parse_args()

    raw = PhaseAccumulator()
    strict = PhaseAccumulator()
    counts = {
        "rows_read": 0,
        "discovery_year_rows": 0,
        "complete_components": 0,
        "valid_gregorian": 0,
        "age_18_110": 0,
        "feb29_excluded": 0,
        "members_read": 0,
    }
    diagnostics = {
        "birth_day_hist": np.zeros(32, dtype=np.int64),
        "death_day_hist": np.zeros(32, dtype=np.int64),
        "dob_exception": {},
        "special_exception": {},
        "mbr_dob_exception": {},
        "death_source": {},
        "verified_edr": {},
        "proof_death": {},
    }

    for archive in args.zips:
        with zipfile.ZipFile(archive) as zf:
            members = text_members(zf)
            print(f"{archive.name}: {len(members)} death-file member(s)")
            for member in members:
                counts["members_read"] += 1
                print(f"Reading {member}", flush=True)
                with zf.open(member) as fh:
                    for chunk in read_member_chunks(fh, args.chunksize):
                        process_chunk(
                            chunk, raw, strict, counts, diagnostics
                        )

    result = {
        "pilot": "ARIS4C013 raw NUMIDENT Pilot 1 discovery",
        "source": "Public-use NUMIDENT Death Files, 1936-2007",
        "discovery_years": [1988, 1996],
        "holdout_years_untouched": [1997, 2005],
        "field_layout": {
            k: {"start0": v[0], "end0_exclusive": v[1]}
            for k, v in FIELD_SPECS.items()
        },
        "counts": counts,
        "prespecified_heaping_flags": {
            "birth_days": sorted(BIRTH_HEAP_DAYS),
            "death_days": sorted(DEATH_HEAP_DAYS),
        },
        "diagnostics": {
            **{
                k: v
                for k, v in diagnostics.items()
                if not isinstance(v, np.ndarray)
            },
            "birth_day_of_month_counts": {
                str(i): int(diagnostics["birth_day_hist"][i])
                for i in range(1, 32)
            },
            "death_day_of_month_counts": {
                str(i): int(diagnostics["death_day_hist"][i])
                for i in range(1, 32)
            },
        },
        "raw": raw.summarize(),
        "strict": strict.summarize(),
        "interpretation_ceiling": (
            "exploratory administrative discovery; no "
            "Bazi/traditional-calendar test"
        ),
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    r, s = result["raw"], result["strict"]
    bh = diagnostics["birth_day_hist"]
    dh = diagnostics["death_day_hist"]
    lines = [
        "# ARIS4C013 · raw NUMIDENT Pilot 1 discovery",
        "",
        "**Discovery only: deaths 1988–1996. The 1997–2005 holdout is not summarized.**",
        "",
        "## Sample",
        f"- fixed-width members read: {counts['members_read']}",
        f"- rows read: {counts['rows_read']:,}",
        f"- rows in discovery death years: {counts['discovery_year_rows']:,}",
        f"- complete valid adult dates before Feb-29 exclusion: {counts['age_18_110']:,}",
        f"- raw phase sample: {r['n']:,}",
        f"- strict phase sample: {s['n']:,}",
        "",
        "## Offset 0 (same Gregorian month/day)",
        f"- raw observed / expected: {r['observed_offset0']:,} / {r['expected_offset0']:.1f}",
        f"- raw O/E: **{r['oe_offset0']:.4f}**",
        f"- strict observed / expected: {s['observed_offset0']:,} / {s['expected_offset0']:.1f}",
        f"- strict O/E: **{s['oe_offset0']:.4f}**",
        "",
        "## Prespecified heaping dates",
        f"- birth day 1: {bh[1]:,}",
        f"- birth day 15: {bh[15]:,}",
        f"- death day 1: {dh[1]:,}",
        f"- death day 4: {dh[4]:,}",
        f"- death day 15: {dh[15]:,}",
        "",
        "## Strict offset-0 O/E by death year",
        "| death year | n | observed | expected | O/E |",
        "|---:|---:|---:|---:|---:|",
    ]
    for y, v in s["by_death_year"].items():
        lines.append(
            f"| {y} | {v['n']:,} | {v['observed_offset0']:,} | "
            f"{v['expected_offset0']:.1f} | {v['oe_offset0']:.4f} |"
        )
    lines += ["", "## Administrative flag distributions", ""]
    for key in [
        "dob_exception",
        "special_exception",
        "mbr_dob_exception",
        "proof_death",
        "death_source",
        "verified_edr",
    ]:
        lines.append(f"### {key}")
        for code, n in sorted(
            diagnostics[key].items(), key=lambda x: (-x[1], x[0])
        ):
            shown = code if code else "(blank)"
            lines.append(f"- {shown}: {n:,}")
        lines.append("")

    lines += [
        "## Interpretation rules",
        "- Raw-to-strict shrinkage is treated as evidence of administrative date artifacts.",
        "- Exception/source fields are reported diagnostically; no post-hoc exclusion rule is promoted after seeing coupling outcomes.",
        "- A strict elevation is only a candidate birthday/anniversary signal if reasonably stable across discovery years.",
        "- No discovery result is called replicated before the frozen 1997–2005 holdout is evaluated once.",
        "- No Bazi or traditional-calendar feature is tested here.",
    ]
    args.md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:34]))
    print(f"Report written to {args.md_out}")


if __name__ == "__main__":
    main()
