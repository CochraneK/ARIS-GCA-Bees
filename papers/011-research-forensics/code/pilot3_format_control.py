#!/usr/bin/env python3
"""Execute the Pilot-3 formatting/honest-error control through the real stack.

This is a development-stage negative/control evaluation, not a confirmatory
specificity estimate. Correction metadata is never passed to the detector.
"""

from __future__ import annotations

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


FIXTURE = ROOT / "data" / "pilot" / "plos_aceh_2022_format_control_safe_exact.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute() -> tuple[dict, dict]:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    context = ForensicContext(
        artifact_id=fixture["artifact_id"],
        mode="track_a",
        artifact_safety={
            "time_safe": True,
            "document_safe": True,
            "title_safe": True,
        },
        content=fixture["structured_detector_inputs"],
        metadata={"target_doi": fixture["target_doi"]},
    )
    report = run_forensics(context, [TableArithmeticDetector()])

    findings = report["findings"]
    statuses = sorted({str(x["status"]) for x in findings})
    flags = [x for x in findings if x["status"] == "FLAG"]
    misconduct = any(bool(x.get("misconduct_inference")) for x in findings)
    decimal_styles = sorted({
        str(x.get("evidence", {}).get("decimal_separator_style"))
        for x in findings
        if x.get("evidence", {}).get("decimal_separator_style") is not None
    })

    expected = fixture["expected_result"]
    checks = {
        "track_a_eligible": report["artifact_safety"]["eligible"] is True,
        "extraction_safe": report["artifact_safety"]["extraction"]["safe"] is True,
        "finding_count_expected": len(findings) == int(expected["finding_count"]),
        "statuses_expected": statuses == sorted(expected["statuses"]),
        "review_priority_expected": report["review_priority"] == expected["review_priority"],
        "decimal_style_expected": decimal_styles == [expected["decimal_separator_style"]],
        "zero_flags": len(flags) == 0,
        "no_misconduct_inference": misconduct is False,
    }

    evaluation = {
        "paper": "ARIS4C011",
        "pilot": "Pilot 3 formatting/honest-error control",
        "target_doi": fixture["target_doi"],
        "artifact_id": fixture["artifact_id"],
        "fixture_sha256": sha256(FIXTURE),
        "benchmark_role": "FORMAT_CONTROL",
        "confirmatory_performance_estimate": False,
        "correction_metadata_visible_to_detector": False,
        "detector_families": sorted({
            str(x["family"]) for x in findings
        }),
        "detector_versions": sorted({
            f'{x["detector_id"]}@{x["detector_version"]}' for x in findings
        }),
        "finding_count": len(findings),
        "flag_count": len(flags),
        "statuses": statuses,
        "decimal_separator_styles": decimal_styles,
        "review_priority": report["review_priority"],
        "misconduct_inference": misconduct,
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "interpretation": (
            "Conservative non-escalation passed: locale-formatted Cronbach-alpha "
            "values were parsed as valid 0-1 values, produced PASS findings only, "
            "and generated review priority NONE. This is a development control "
            "and does not estimate confirmatory specificity."
        ),
    }
    return report, evaluation


def main() -> None:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument(
        "--report",
        type=Path,
        default=ROOT / "data" / "results" / "pilot3_format_control_report.json",
    )
    p.add_argument(
        "--evaluation",
        type=Path,
        default=ROOT / "data" / "results" / "pilot3_format_control_evaluation.json",
    )
    args = p.parse_args()

    report, evaluation = execute()
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
        raise SystemExit("Formatting-control non-escalation gate failed")


if __name__ == "__main__":
    main()
