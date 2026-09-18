import json
from pathlib import Path

from orchestrator import ForensicContext, run_forensics
from detectors.deterministic import DEFAULT_DETERMINISTIC_DETECTORS


def test_safe_exact_jstage_real_manuscript_smoke_abstains_cleanly():
    project_root = Path(__file__).resolve().parents[3]
    fixture_path = project_root / "data/pilot/jstage_2005_safe_exact.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

    content = fixture["structured_detector_inputs"]
    context = ForensicContext(
        artifact_id=fixture["artifact_id"],
        mode="track_a",
        artifact_safety={
            "time_safe": True,
            "document_safe": True,
            "title_safe": True,
        },
        content=content,
        metadata={"target_doi": fixture["target_doi"]},
    )

    out = run_forensics(context, DEFAULT_DETERMINISTIC_DETECTORS)
    assert out["review_priority"] == "NONE"
    assert [finding["status"] for finding in out["findings"]] == fixture[
        "expected_pilot1_outcome"
    ]["finding_statuses"]
    assert all(finding["misconduct_inference"] is False for finding in out["findings"])
    assert out["artifact_safety"]["extraction"]["safe"] is True
    assert out["artifact_safety"]["extraction"]["structured_record_count"] == 0
