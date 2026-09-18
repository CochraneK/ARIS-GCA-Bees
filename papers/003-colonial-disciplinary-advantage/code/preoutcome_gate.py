#!/usr/bin/env python3
"""Hard gate for materializing ARIS4C003 confirmatory outcomes.

Design files may be developed without real outcomes. Confirmatory outcome
materialization is blocked until blinded IKES coding is frozen, historical
exposures and country mappings exist locally, and source provenance is recorded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pandas as pd

PAPER = Path(__file__).resolve().parents[1]
PROCESS = PAPER / "process"
DATA = PAPER / "data"
DIMS = [f"D{i}" for i in range(1, 12)]
EXPECTED_IDS = [f"D{i:02d}" for i in range(1, 22)]


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve_recorded_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PAPER / path


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
        ("PREREGISTRATION_AMENDMENT_003.md", "temporal-profile amendment 003"),
        ("MODEL_SPEC_LOCK.json", "machine-readable model specification lock"),
        ("coder_b_blind/README.md", "Coder B blind bundle README"),
        ("coder_b_blind/WORKBUDDY_HANDOFF.md", "WorkBuddy blinded handoff"),
        ("coder_b_blind/OUTPUT_TEMPLATE.md", "Coder B blank output template"),
        ("coder_b_blind/MANIFEST.json", "Coder B blind bundle manifest"),
    ]:
        check_file(PROCESS / rel, label, design_problems)

    crosswalk = PROCESS / "DISCIPLINE_CROSSWALK.csv"
    if crosswalk.exists():
        x = pd.read_csv(crosswalk)
        if len(x) != 21:
            design_problems.append(f"discipline crosswalk should have 21 rows, found {len(x)}")
        if "status" not in x.columns or not x["status"].astype(str).str.startswith("FROZEN").all():
            design_problems.append("not every discipline crosswalk row is FROZEN")

    blind_manifest = PROCESS / "coder_b_blind" / "MANIFEST.json"
    if blind_manifest.exists():
        try:
            bm = json.loads(blind_manifest.read_text(encoding="utf-8"))
            if bm.get("outcome_seen_when_built") is not False:
                design_problems.append(
                    "Coder B blind manifest must state outcome_seen_when_built=false"
                )
            policy = bm.get("access_policy", {})
            if policy.get("mode") != "whitelist_only":
                design_problems.append(
                    "Coder B blind manifest access policy must be whitelist_only"
                )
            files = bm.get("files", [])
            if len(files) != 3:
                design_problems.append(
                    f"Coder B blind manifest should pin 3 input files, found {len(files)}"
                )
            for entry in files:
                rel = str(entry.get("path", ""))
                digest = str(entry.get("git_blob_sha", ""))
                root = PAPER.parents[1]
                artifact = root / rel
                if not artifact.exists():
                    design_problems.append(
                        f"Coder B blind manifest artifact missing: {rel}"
                    )
                elif git_blob_sha(artifact) != digest:
                    design_problems.append(
                        f"Coder B blind input drift/hash mismatch: {rel}"
                    )
        except Exception as exc:
            design_problems.append(
                f"Coder B blind manifest unreadable: {type(exc).__name__}"
            )

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
            temporal = lock.get("secondary_temporal_profile", {})
            if temporal.get("mature_periods") != [
                "2007-2010", "2011-2014", "2015-2018", "2019-2022"
            ]:
                design_problems.append(
                    "MODEL_SPEC_LOCK temporal mature periods differ from frozen four windows"
                )
            if temporal.get("recent_output_only_period") != "2023-2025":
                design_problems.append(
                    "MODEL_SPEC_LOCK recent output-only period must be 2023-2025"
                )
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
        (DATA / "manifests" / "openalex_works_manifest.json", "official OpenAlex Works manifest"),
    ]:
        check_file(path, label, outcome_problems)

    coder_b_csv = PROCESS / "IKES_CODER_B.csv"
    if coder_b_csv.exists():
        try:
            b = pd.read_csv(coder_b_csv, dtype=str, keep_default_na=False)
            if b["concept_id"].tolist() != EXPECTED_IDS:
                outcome_problems.append(
                    "IKES_CODER_B concept_id order must be exactly D01-D21"
                )
            numeric = pd.DataFrame(index=b.index)
            for dim in DIMS:
                if dim not in b.columns:
                    outcome_problems.append(f"IKES_CODER_B missing {dim}")
                    continue
                s = b[dim].replace({"": pd.NA, "NA": pd.NA})
                vals = pd.to_numeric(s, errors="coerce")
                invalid_text = s.notna() & vals.isna()
                invalid_range = vals.notna() & ~vals.between(0, 3)
                invalid_integer = vals.notna() & ((vals - vals.round()).abs() > 1e-12)
                if invalid_text.any() or invalid_range.any() or invalid_integer.any():
                    outcome_problems.append(
                        f"IKES_CODER_B invalid 0-3/NA values in {dim}"
                    )
                numeric[dim] = vals
            if set(DIMS).issubset(numeric.columns):
                provided = pd.to_numeric(b.get("IKES_B"), errors="coerce")
                recomputed = numeric[DIMS].mean(axis=1, skipna=True)
                if provided.isna().any() or ((provided - recomputed).abs() > 0.011).any():
                    outcome_problems.append(
                        "IKES_CODER_B IKES_B does not match D1-D11 mean"
                    )
        except Exception as exc:
            outcome_problems.append(f"IKES_CODER_B unreadable: {type(exc).__name__}")

    coder_b_notes = PROCESS / "IKES_CODER_B.md"
    if coder_b_notes.exists():
        notes = coder_b_notes.read_text(encoding="utf-8", errors="replace")
        if "BLINDING DECLARATION" not in notes:
            outcome_problems.append("Coder B notes missing BLINDING DECLARATION")
        if notes.count("INDEPENDENCE_STATUS: PASS") != 1:
            outcome_problems.append(
                "Coder B notes must contain exactly one INDEPENDENCE_STATUS: PASS"
            )
        if "INDEPENDENCE_STATUS: FAIL" in notes:
            outcome_problems.append("Coder B declared failed independence/blinding")
        headings = re.findall(r"(?m)^###\s+(D\d{2})\s+—\s+.+$", notes)
        if headings != EXPECTED_IDS:
            outcome_problems.append(
                "Coder B evidence headings must appear exactly once in D01-D21 order"
            )
        for cid in EXPECTED_IDS:
            match = re.search(
                rf"(?ms)^###\s+{cid}\s+—\s+.+?$(.*?)(?=^###\s+D\d{{2}}\s+—|^##\s+BLINDING DECLARATION|\Z)",
                notes,
            )
            if match is None or len(
                re.findall(
                    r"(?mi)^Confidence:\s*(high|medium|low)\s*$",
                    match.group(1) if match else "",
                )
            ) != 1:
                outcome_problems.append(
                    f"Coder B evidence section {cid} missing exactly one confidence label"
                )

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

    freeze_provenance = PROCESS / "IKES_FROZEN.provenance.json"
    if freeze_provenance.exists():
        try:
            prov = json.loads(freeze_provenance.read_text(encoding="utf-8"))
            for key in (
                "coder_a",
                "coder_b",
                "coder_b_notes",
                "coder_b_raw",
                "adjudication",
                "frozen",
            ):
                entry = prov.get(key)
                if not isinstance(entry, dict):
                    outcome_problems.append(
                        f"IKES freeze provenance missing {key}"
                    )
                    continue
                path_value = entry.get("path")
                digest = entry.get("sha256")
                if not path_value or not digest:
                    outcome_problems.append(
                        f"IKES freeze provenance incomplete for {key}"
                    )
                    continue
                artifact = resolve_recorded_path(str(path_value))
                if not artifact.exists():
                    outcome_problems.append(
                        f"IKES freeze provenance artifact missing: {key} -> {artifact}"
                    )
                    continue
                if sha256(artifact) != digest:
                    outcome_problems.append(
                        f"IKES freeze provenance hash mismatch: {key}"
                    )
                if key == "coder_b_raw":
                    raw_root = (PROCESS / "gptpage").resolve()
                    if not artifact.resolve().is_relative_to(raw_root):
                        outcome_problems.append(
                            "Coder B raw response must be preserved under process/gptpage"
                        )
        except Exception as exc:
            outcome_problems.append(
                f"IKES_FROZEN provenance unreadable: {type(exc).__name__}"
            )

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

    openalex_manifest_file = DATA / "manifests" / "openalex_works_manifest.json"
    openalex_manifest_digest = (
        sha256(openalex_manifest_file) if openalex_manifest_file.exists() else None
    )

    manifest = DATA / "manifests" / "source_manifest.json"
    check_file(manifest, "source manifest", outcome_problems)
    if manifest.exists():
        try:
            obj = json.loads(manifest.read_text(encoding="utf-8"))
            sources = obj.get("sources", {})
            for key in ("openalex", "coldat_years"):
                if key not in sources:
                    outcome_problems.append(f"source manifest missing {key}")
            oa_entry = sources.get("openalex", {})
            if oa_entry:
                if oa_entry.get("status") != "manifest_and_schema_probe_pass":
                    outcome_problems.append(
                        "source manifest OpenAlex status is not manifest_and_schema_probe_pass"
                    )
                expected_digest = oa_entry.get("manifest_sha256") or oa_entry.get("sha256")
                if openalex_manifest_digest is None:
                    outcome_problems.append(
                        "official OpenAlex Works manifest file is unavailable"
                    )
                elif expected_digest != openalex_manifest_digest:
                    outcome_problems.append(
                        "OpenAlex Works manifest SHA-256 differs from source ledger"
                    )
                if oa_entry.get("schema_probe_safe_to_build_extractor") is not True:
                    outcome_problems.append(
                        "source ledger does not record a passing OpenAlex schema probe"
                    )
                if oa_entry.get("outcomes_materialized_during_probe") is not False:
                    outcome_problems.append(
                        "source ledger OpenAlex probe is not marked outcome-free"
                    )
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
