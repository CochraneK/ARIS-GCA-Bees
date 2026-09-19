#!/usr/bin/env python3
"""Mechanically gated ARIS4C013 BUNMD temporal holdout."""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
import subprocess

import numpy as np
import pandas as pd

import pilot1_bunmd_discovery as engine
from effect_size import OffsetInference, confirmatory_holdout_classification
from holdout_release_gate import validate_repository_release

HOLDOUT_YEARS = tuple(range(1997, 2006))


def run_holdout(zip_path: Path, chunksize: int):
    engine.DISCOVERY_YEARS = HOLDOUT_YEARS
    raw = engine.PhaseAccumulator()
    strict = engine.PhaseAccumulator()

    counts = {
        "rows_read": 0,
        "holdout_year_rows": 0,
        "complete_components": 0,
        "valid_gregorian": 0,
        "exact_age_18_110_diagnostic": 0,
        "phase_safe_year_gap_19_110": 0,
        "boundary_adult_excluded": 0,
        "feb29_excluded": 0,
    }
    bday_hist = np.zeros(32, dtype=np.int64)
    dday_hist = np.zeros(32, dtype=np.int64)
    usecols = [
        "byear", "bmonth", "bday",
        "dyear", "dmonth", "dday", "sex",
    ]

    with zipfile.ZipFile(zip_path) as zf:
        member = engine.pick_csv_member(zf)
        print(f"Using holdout archive member: {member}", flush=True)
        with zf.open(member) as fh:
            for chunk in pd.read_csv(
                fh,
                usecols=usecols,
                chunksize=chunksize,
                low_memory=False,
            ):
                counts["rows_read"] += len(chunk)
                for col in usecols:
                    chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

                keep_year = chunk["dyear"].isin(HOLDOUT_YEARS)
                if not keep_year.any():
                    continue
                chunk = chunk.loc[keep_year, usecols]
                counts["holdout_year_rows"] += len(chunk)

                complete = chunk[
                    ["byear","bmonth","bday","dyear","dmonth","dday"]
                ].notna().all(axis=1)
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

                valid = (
                    engine.valid_gregorian(by,bm,bd)
                    & engine.valid_gregorian(dy,dm,dd)
                )
                by,bm,bd,dy,dm,dd,sx = [
                    x[valid] for x in (by,bm,bd,dy,dm,dd,sx)
                ]
                counts["valid_gregorian"] += len(by)
                if not len(by):
                    continue

                age = dy - by - (
                    (dm < bm) | ((dm == bm) & (dd < bd))
                ).astype(np.int32)
                exact_adult = (age >= 18) & (age <= 110)
                counts["exact_age_18_110_diagnostic"] += int(
                    exact_adult.sum()
                )

                phase_safe = engine.phase_safe_year_gap(by, dy)
                counts["phase_safe_year_gap_19_110"] += int(
                    phase_safe.sum()
                )
                counts["boundary_adult_excluded"] += int(
                    (exact_adult & ~phase_safe).sum()
                )
                by,bm,bd,dy,dm,dd,sx = [
                    x[phase_safe] for x in (by,bm,bd,dy,dm,dd,sx)
                ]
                if not len(by):
                    continue

                bday_hist += np.bincount(bd, minlength=32)[:32]
                dday_hist += np.bincount(dd, minlength=32)[:32]

                feb29 = (
                    ((bm == 2) & (bd == 29))
                    | ((dm == 2) & (dd == 29))
                )
                counts["feb29_excluded"] += int(feb29.sum())
                keep = ~feb29
                by,bm,bd,dy,dm,dd,sx = [
                    x[keep] for x in (by,bm,bd,dy,dm,dd,sx)
                ]
                if not len(by):
                    continue

                bdoy = engine.month_day_to_doy(bm, bd).astype(np.int16)
                ddoy = engine.month_day_to_doy(dm, dd).astype(np.int16)
                raw.add(bdoy, ddoy, by, dy, sx)

                strict_mask = (
                    ~np.isin(bd, list(engine.BIRTH_HEAP_DAYS))
                    & ~np.isin(dd, list(engine.DEATH_HEAP_DAYS))
                )
                if strict_mask.any():
                    idx = np.flatnonzero(strict_mask)
                    strict.add(
                        bdoy[idx], ddoy[idx], by[idx], dy[idx], sx[idx]
                    )

    return raw, strict, counts, bday_hist, dday_hist


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", type=Path, required=True)
    ap.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "papers/013-birth-death-temporal-coupling/process/"
            "HOLDOUT_RELEASE.json"
        ),
    )
    ap.add_argument("--json-out", type=Path, required=True)
    ap.add_argument("--md-out", type=Path, required=True)
    ap.add_argument("--chunksize", type=int, default=1_000_000)
    args = ap.parse_args()

    # Gate validation occurs before the archive is opened.
    release = validate_repository_release(args.manifest)
    repo_root = Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
        ).strip()
    )
    discovery = json.loads(
        (repo_root / release["discovery_result_path"]).read_text(
            encoding="utf-8"
        )
    )
    if discovery.get("discovery_years") != [1988, 1996]:
        raise RuntimeError("frozen discovery result has unexpected years")
    if (
        discovery.get("strict", {}).get("null_model")
        != "exact birth year × death year × sex"
    ):
        raise RuntimeError("frozen discovery result is not Pilot 1 v2")

    raw, strict, counts, bh, dh = run_holdout(
        args.zip, args.chunksize
    )
    raw_summary = raw.summarize()
    strict_summary = strict.summarize()
    discovery_oe = float(discovery["strict"]["oe_offset0"])
    inf = OffsetInference(**strict_summary["offset0_inference"])
    year_oes = [
        float(strict_summary["by_death_year"][str(y)]["oe_offset0"])
        for y in HOLDOUT_YEARS
    ]
    confirm = confirmatory_holdout_classification(
        discovery_oe, inf, year_oes
    )

    result = {
        "pilot": "ARIS4C013 BUNMD Pilot 1 temporal holdout",
        "release_manifest": release,
        "discovery_result_path": release["discovery_result_path"],
        "discovery_strict_oe": discovery_oe,
        "discovery_years": [1988, 1996],
        "holdout_years": [1997, 2005],
        "counts": counts,
        "birth_day_of_month_counts": {
            str(i): int(bh[i]) for i in range(1, 32)
        },
        "death_day_of_month_counts": {
            str(i): int(dh[i]) for i in range(1, 32)
        },
        "raw": raw_summary,
        "strict": strict_summary,
        "confirmatory_classification": confirm,
        "interpretation_ceiling": (
            "confirmatory H2 birthday/anniversary timing only; "
            "no traditional-calendar/Bazi inference"
        ),
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    ci = strict_summary["offset0_inference"]
    lines = [
        "# ARIS4C013 · BUNMD temporal holdout",
        "",
        "The holdout gate validated before the BUNMD archive was opened.",
        "",
        f"- discovery strict O/E: {discovery_oe:.4f}",
        f"- holdout strict O/E: {strict_summary['oe_offset0']:.4f}",
        f"- holdout fixed-margin 95% interval: [{ci['ci95_lower']:.4f}, {ci['ci95_upper']:.4f}]",
        f"- holdout practical class: {ci['practical_class']}",
        f"- temporal direction fraction: {confirm['temporal_direction_fraction']:.3f}",
        f"- attenuation class: {confirm['attenuation_class']}",
        f"- replicated candidate birthday effect: {confirm['replicated_candidate_birthday_effect']}",
        "",
        "Claim ceiling: an H2 timing association only; no Bazi inference.",
    ]
    args.md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
