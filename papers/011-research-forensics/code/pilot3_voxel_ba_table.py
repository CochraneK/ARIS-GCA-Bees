#!/usr/bin/env python3
"""Run the correction-blind voxel/Brodmann-area Table 2 development case.

Only preserved-original Table 2 cells are detector-visible. The later
correction is introduced after detector execution as manager-only evaluation
evidence and cannot affect the finding.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "agent" / "research-forensics" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from orchestrator import ForensicContext, run_forensics  # noqa: E402
from detectors.deterministic import TableArithmeticDetector  # noqa: E402

DEFAULT_FIXTURE = (
    ROOT / "data" / "pilot" /
    "plos_voxel_ba_preserved_original_safe_exact.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(fixture_path: Path) -> tuple[dict, dict]:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    if fixture.get("outcome_or_correction_metadata_included") is not False:
        raise ValueError("Detector fixture contains outcome/correction metadata")

    context = ForensicContext(
        artifact_id=fixture["artifact_id"],
        mode="track_a",
        artifact_safety=fixture["artifact_safety"],
        content=fixture["structured_detector_inputs"],
        metadata={
            "target_doi": fixture["target_doi"],
            "source_url": fixture["source"]["url"],
            "source_role": fixture["source"]["object_role"],
        },
    )
    report = run_forensics(context, [TableArithmeticDetector()])

    findings = report["findings"]
    flags = [x for x in findings if x["status"] == "FLAG"]
    passes = [x for x in findings if x["status"] == "PASS"]
    malformed = [
        x for x in flags
        if x.get("evidence", {}).get("normalized_token") == "9月8日"
    ]

    checks = {
        "track_a_eligible": report["artifact_safety"]["eligible"] is True,
        "extraction_safe": report["artifact_safety"]["extraction"]["safe"] is True,
        "six_original_cells_evaluated": len(findings) == 6,
        "five_passes": len(passes) == 5,
        "exactly_one_flag": len(flags) == 1,
        "malformed_original_token_flagged": len(malformed) == 1,
        "no_misconduct_inference": all(
            x.get("misconduct_inference") is False for x in findings
        ),
    }

    evaluation = {
        "paper": "ARIS4C011",
        "pilot": "Pilot 3 voxel/Brodmann-area preserved-original table token",
        "target_doi": fixture["target_doi"],
        "artifact_id": fixture["artifact_id"],
        "fixture_sha256": sha256(fixture_path),
        "artifact_safety_class": fixture["source"]["qualification"],
        "detector_visible_correction_metadata": False,
        "detector_family": "F3",
        "detector_id": "table_arithmetic@pilot1-0.1.0",
        "development_true_positive_scope": (
            "malformed BA token only; later documented BA row-shift errors "
            "are not counted because they are not independently detectable "
            "by this correction-blind syntax check"
        ),
        "finding_count": len(findings),
        "pass_count": len(passes),
        "flag_count": len(flags),
        "review_priority": report["review_priority"],
        "checks": checks,
        "manager_only_later_outcome": {
            "correction_doi": "10.1371/journal.pone.0170146",
            "published": "2017-01-09",
            "confirmed_original_token": "9月8日",
            "corrected_token": "9/8",
            "used_by_detector": False,
        },
        "status": "PASS" if all(checks.values()) else "FAIL",
        "claim_boundary": (
            "Development feasibility / issue decomposition only. This result "
            "does not estimate sensitivity, precision, specificity, or "
            "misconduct likelihood."
        ),
    }
    return report, evaluation


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    p.add_argument(
        "--report",
        type=Path,
        default=ROOT / "data" / "results" / "pilot3_voxel_ba_report.json",
    )
    p.add_argument(
        "--evaluation",
        type=Path,
        default=ROOT / "data" / "results" / "pilot3_voxel_ba_evaluation.json",
    )
    args = p.parse_args()

    report, evaluation = execute(args.fixture)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.evaluation.write_text(
        json.dumps(evaluation, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(evaluation, ensure_ascii=False, indent=2))
    if evaluation["status"] != "PASS":
        raise SystemExit("Voxel BA development evaluation failed")


if __name__ == "__main__":
    main()
