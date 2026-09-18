#!/usr/bin/env python3
"""Hard gate for materializing ARIS4C003 confirmatory outcomes.

Design files may be developed without real outcomes. Confirmatory outcome
materialization is blocked until blinded IKES coding is frozen, historical
exposures and country mappings exist locally, and source provenance is recorded.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

PAPER = Path(__file__).resolve().parents[1]
PROCESS = PAPER / "process"
DATA = PAPER / "data"


def check_file(path: Path, label: str, problems: list[str]) -> None:
    if not path.exists() or not path.is_file() or path.stat().st_size == 0:
        problems.append(f"missing: {label} -> {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-root", type=Path)
    parser.add_argument("--strict", action="store_true", help="exit non-zero unless OUTCOME_UNLOCKED")
    parser.add_argument("--require-design-locked", action="store_true", help="exit non-zero unless DESIGN_LOCKED")
    args = parser.parse_args()

    design_problems: list[str] = []
    outcome_problems: list[str] = []

    for rel, label in [
        ("PREREGISTRATION_DRAFT.md", "preregistration"),
        ("ENTANGLEMENT_PROTOCOL.md", "IKES protocol"),
        ("DISCIPLINE_CROSSWALK.csv", "frozen discipline crosswalk"),
        ("COUNTRY_ENTITY_PROTOCOL.md", "country/entity protocol"),
        ("IKES_CODER_A.csv", "IKES Coder A"),
        ("IKES_CODER_B_PACKET.md", "blind Coder B packet"),
        ("SYNTHETIC_PPML_REPORT.md", "synthetic PPML report"),
        ("PREREGISTRATION_AMENDMENT_001.md", "implementation amendment 001"),
        ("PREREGISTRATION_AMENDMENT_002.md", "estimator amendment 002"),
        ("MODEL_SPEC_LOCK.json", "machine-readable model specification lock"),
    ]:
        check_file(PROCESS / rel, label, design_problems)

    crosswalk = PROCESS / "DISCIPLINE_CROSSWALK.csv"
    if crosswalk.exists():
        x = pd.read_csv(crosswalk)
        if len(x) != 21:
            design_problems.append(f"discipline crosswalk should have 21 rows, found {len(x)}")
        if "status" not in x.columns or not x["status"].astype(str).str.startswith("FROZEN").all():
            design_problems.append("not every discipline crosswalk row is FROZEN")

    model_lock = PROCESS / "MODEL_SPEC_LOCK.json"
    if model_lock.exists():
        try:
            lock = json.loads(model_lock.read_text(encoding="utf-8"))
            if lock.get("outcome_seen_at_lock") is not False:
                design_problems.append("MODEL_SPEC_LOCK must state outcome_seen_at_lock=false")
            if lock.get("primary_period") != "2019-2022":
                design_problems.append("MODEL_SPEC_LOCK primary_period must be 2019-2022")
            perm = lock.get("permutation", {})
            if perm.get("reps") != 999 or perm.get("seed") != 20260918:
                design_problems.append("MODEL_SPEC_LOCK permutation settings differ from frozen 999/20260918")
        except Exception as exc:
            design_problems.append(f"MODEL_SPEC_LOCK unreadable: {type(exc).__name__}")

    # These are intentionally external/local gates.
    for path, label in [
        (PROCESS / "IKES_CODER_B.csv", "independent blinded IKES Coder B scores"),
        (PROCESS / "IKES_CODER_B.md", "independent blinded IKES Coder B evidence notes"),
        (PROCESS / "IKES_FROZEN.csv", "adjudicated IKES_FROZEN"),
        (PROCESS / "IKES_FROZEN.provenance.json", "IKES freeze provenance"),
        (DATA / "derived" / "COLDAT_FORMER_COLONY_EXPOSURE.csv", "derived COLDAT exposure table"),
        (DATA / "derived" / "COUNTRY_CROSSWALK.csv", "audited country crosswalk"),
        (DATA / "derived" / "CEPII_DYADS.csv", "derived CEPII historical dyads"),
        (DATA / "manifests" / "CEPII_GRAVITY_V202211.json", "CEPII source manifest"),
        (PROCESS / "HISTORICAL_DATA_AUDIT.json", "historical data audit"),
        (PROCESS / "OPENALEX_SCHEMA_PROBE.json", "OpenAlex schema-only probe"),
    ]:
        check_file(path, label, outcome_problems)

    coder_b_notes = PROCESS / "IKES_CODER_B.md"
    if coder_b_notes.exists():
        notes = coder_b_notes.read_text(encoding="utf-8", errors="replace")
        if "BLINDING DECLARATION" not in notes:
            outcome_problems.append("Coder B notes missing BLINDING DECLARATION")

    frozen = PROCESS / "IKES_FROZEN.csv"
    if frozen.exists():
        try:
            f = pd.read_csv(frozen)
            expected = {f"D{i:02d}" for i in range(1, 22)}
            if "concept_id" not in f.columns or set(f["concept_id"].astype(str)) != expected:
                outcome_problems.append("IKES_FROZEN must contain exactly concept_id D01-D21")
            if "IKES" not in f.columns or f["IKES"].isna().any():
                outcome_problems.append("IKES_FROZEN missing complete IKES values")
        except Exception as exc:
            outcome_problems.append(f"IKES_FROZEN unreadable: {type(exc).__name__}")

    country_crosswalk = DATA / "derived" / "COUNTRY_CROSSWALK.csv"
    if country_crosswalk.exists():
        try:
            cw = pd.read_csv(country_crosswalk)
            if "status" not in cw.columns or not cw["status"].eq("RESOLVED").all():
                outcome_problems.append("COUNTRY_CROSSWALK contains unresolved rows")
            if "iso3c" not in cw.columns or cw["iso3c"].duplicated().any():
                outcome_problems.append("COUNTRY_CROSSWALK iso3c must be unique")
        except Exception as exc:
            outcome_problems.append(f"COUNTRY_CROSSWALK unreadable: {type(exc).__name__}")

    historical_audit = PROCESS / "HISTORICAL_DATA_AUDIT.json"
    if historical_audit.exists():
        try:
            ha = json.loads(historical_audit.read_text(encoding="utf-8"))
            if ha.get("status") != "PASS":
                outcome_problems.append("historical data audit is not PASS")
        except Exception as exc:
            outcome_problems.append(f"HISTORICAL_DATA_AUDIT unreadable: {type(exc).__name__}")

    oa_probe = PROCESS / "OPENALEX_SCHEMA_PROBE.json"
    if oa_probe.exists():
        try:
            oa = json.loads(oa_probe.read_text(encoding="utf-8"))
            if oa.get("safe_to_build_extractor") is not True:
                outcome_problems.append("OpenAlex schema probe did not pass")
            if oa.get("outcomes_materialized") is not False:
                outcome_problems.append("OpenAlex schema probe integrity flag is not outcome-free")
        except Exception as exc:
            outcome_problems.append(f"OPENALEX_SCHEMA_PROBE unreadable: {type(exc).__name__}")

    manifest = DATA / "manifests" / "source_manifest.json"
    check_file(manifest, "source manifest", outcome_problems)
    if manifest.exists():
        try:
            obj = json.loads(manifest.read_text(encoding="utf-8"))
            sources = obj.get("sources", {})
            for key in ("openalex", "coldat_years"):
                if key not in sources:
                    outcome_problems.append(f"source manifest missing {key}")
        except Exception as exc:
            outcome_problems.append(f"source manifest unreadable: {type(exc).__name__}")

    # Snapshot availability is checked only if a root is supplied; the public
    # snapshot is intentionally ignored by git and may live on an external disk.
    if args.snapshot_root:
        root = args.snapshot_root.expanduser().resolve()
        parquet_files = list(root.rglob("*.parquet")) if root.exists() else []
        if not parquet_files:
            outcome_problems.append(f"no OpenAlex Parquet files found under {root}")

    design_status = "DESIGN_LOCKED" if not design_problems else "DESIGN_INCOMPLETE"
    outcome_status = (
        "OUTCOME_UNLOCKED"
        if design_status == "DESIGN_LOCKED" and not outcome_problems
        else "OUTCOME_LOCKED"
    )

    result = {
        "design_status": design_status,
        "outcome_status": outcome_status,
        "design_problems": design_problems,
        "outcome_problems": outcome_problems,
    }
    print(json.dumps(result, indent=2))

    if args.require_design_locked and design_status != "DESIGN_LOCKED":
        raise SystemExit(3)
    if args.strict and outcome_status != "OUTCOME_UNLOCKED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
