import json
from pathlib import Path

from orchestrator import ForensicContext, run_forensics
from detectors.deterministic import TableArithmeticDetector


def test_real_plos_decimal_comma_control_non_escalates():
    project_root = Path(__file__).resolve().parents[3]
    fixture = json.loads(
        (
            project_root
            / "data/pilot/plos_aceh_2022_format_control_safe_exact.json"
        ).read_text(encoding="utf-8")
    )

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
    out = run_forensics(context, [TableArithmeticDetector()])

    expected = fixture["expected_result"]
    assert out["artifact_safety"]["eligible"] is True
    assert out["artifact_safety"]["extraction"]["safe"] is True
    assert out["review_priority"] == expected["review_priority"]
    assert len(out["findings"]) == expected["finding_count"]
    assert {f["status"] for f in out["findings"]} == set(expected["statuses"])
    assert all(
        f["evidence"]["decimal_separator_style"]
        == expected["decimal_separator_style"]
        for f in out["findings"]
    )
    assert all(
        0.0 <= f["evidence"]["parsed_value"] <= 1.0
        for f in out["findings"]
    )
    assert all(
        f["misconduct_inference"] is expected["misconduct_inference"]
        for f in out["findings"]
    )
