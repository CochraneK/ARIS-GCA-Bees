#!/usr/bin/env python3
"""Mechanically gated ARIS4C013 raw-NUMIDENT temporal holdout.

This script refuses to inspect 1997-2005 until the repository release gate
validates a committed discovery result and a separate authorization decision.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import numpy as np

import pilot1_numident_raw as engine
from effect_size import confirmatory_holdout_classification
from holdout_release_gate import validate_repository_release

HOLDOUT_YEARS = tuple(range(1997, 2006))


def run_holdout(zips: list[Path], chunksize: int):
    # The discovery engine is reused only after the release gate passes.
    # Its global year set controls both filtering and year-specific summaries.
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

    # engine.process_chunk writes to discovery_year_rows. Rename only in the
    # final report; internally this key keeps the shared engine simple.
    shared_counts = dict(counts)
    shared_counts["discovery_year_rows"] = 0
    del shared_counts["holdout_year_rows"]

    for archive in zips:
        with zipfile.ZipFile(archive) as zf:
            members = engine.text_members(zf)
            for member in members:
                shared_counts["members_read"] += 1
                print(f"Reading holdout member {member}", flush=True)
                with zf.open(member) as fh:
                    for chunk in engine.read_member_chunks(fh, chunksize):
                        engine.process_chunk(
                            chunk,
                            raw,
                            strict,
                            shared_counts,
                            diagnostics,
                        )

    shared_counts["holdout_year_rows"] = shared_counts.pop(
        "discovery_year_rows"
    )
    return raw, strict, shared_counts, diagnostics


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", dest="zips", type=Path, action="append", required=True)
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
    ap.add_argument("--chunksize", type=int, default=750_000)
    args = ap.parse_args()

    release = validate_repository_release(args.manifest)
    repo_root = Path(
        __import__("subprocess").check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
        ).strip()
    )
    discovery_path = repo_root / release["discovery_result_path"]
    discovery = json.loads(discovery_path.read_text(encoding="utf-8"))

    if discovery.get("discovery_years") != [1988, 1996]:
        raise RuntimeError("frozen discovery result has unexpected years")
    if (
        discovery.get("strict", {}).get("null_model")
        != "exact birth year × death year × sex"
    ):
        raise RuntimeError("frozen discovery result is not Pilot 1 v2")

    raw, strict, counts, diagnostics = run_holdout(
        args.zips, args.chunksize
    )
    raw_summary = raw.summarize()
    strict_summary = strict.summarize()

    discovery_oe = float(discovery["strict"]["oe_offset0"])
    holdout_inf = strict_summary["offset0_inference"]
    from effect_size import OffsetInference

    inf_obj = OffsetInference(**holdout_inf)
    year_oes = [
        float(strict_summary["by_death_year"][str(y)]["oe_offset0"])
        for y in HOLDOUT_YEARS
        if str(y) in strict_summary["by_death_year"]
    ]
    confirm = confirmatory_holdout_classification(
        discovery_oe,
        inf_obj,
        year_oes,
    )

    bh = diagnostics["birth_day_hist"]
    dh = diagnostics["death_day_hist"]
    result = {
        "pilot": "ARIS4C013 raw NUMIDENT Pilot 1 temporal holdout",
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

    s = strict_summary
    ci = s["offset0_inference"]
    lines = [
        "# ARIS4C013 · raw NUMIDENT temporal holdout",
        "",
        "The holdout gate validated before any holdout archive was opened.",
        "",
        "## Frozen comparison",
        f"- discovery strict O/E: {discovery_oe:.4f}",
        f"- holdout strict O/E: {s['oe_offset0']:.4f}",
        f"- holdout fixed-margin 95% interval: [{ci['ci95_lower']:.4f}, {ci['ci95_upper']:.4f}]",
        f"- holdout practical class: {ci['practical_class']}",
        f"- same direction: {confirm['same_direction_as_discovery']}",
        f"- temporal direction fraction: {confirm['temporal_direction_fraction']:.3f}",
        f"- attenuation class: {confirm['attenuation_class']}",
        f"- replicated candidate birthday effect: {confirm['replicated_candidate_birthday_effect']}",
        "",
        "## Claim ceiling",
        "Even a positive confirmatory result supports only a reproducible birthday/anniversary timing association after the locked controls. It is not evidence for Bazi or a supernatural mechanism.",
    ]
    args.md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
