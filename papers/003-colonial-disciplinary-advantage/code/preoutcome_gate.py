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
    ]:
        check_file(PROCESS / rel, label, design_problems)

    crosswalk = PROCESS / "DISCIPLINE_CROSSWALK.csv"
    if crosswalk.exists():
        x = pd.read_csv(crosswalk)
        if len(x) != 21:
            design_problems.append(f"discipline crosswalk should have 21 rows, found {len(x)}")
        if "status" not in x.columns or not x["status"].astype(str).str.startswith("FROZEN").all():
            design_problems.append("not every discipline crosswalk row is FROZEN")

    # These are intentionally external/local gates.
    for path, label in [
        (PROCESS / "IKES_CODER_B.csv", "independent blinded IKES Coder B"),
        (PROCESS / "IKES_FROZEN.csv", "adjudicated IKES_FROZEN"),
        (PROCESS / "IKES_FROZEN.provenance.json", "IKES freeze provenance"),
        (DATA / "derived" / "COLDAT_FORMER_COLONY_EXPOSURE.csv", "derived COLDAT exposure table"),
        (DATA / "derived" / "COUNTRY_CROSSWALK.csv", "audited country crosswalk"),
    ]:
        check_file(path, label, outcome_problems)

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

    if args.strict and outcome_status != "OUTCOME_UNLOCKED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
