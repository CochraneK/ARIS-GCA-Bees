import json
from pathlib import Path
from orchestrator import ForensicContext, run_forensics
from detectors.deterministic import CrossSourceFieldConsistencyDetector

def test_real_plos_pre_correction_cross_source_flag():
    project_root = Path(__file__).resolve().parents[3]
    fixture = json.loads((project_root / "data/pilot/plos_morality_2021_cross_source_safe_exact.json").read_text(encoding="utf-8"))
    context = ForensicContext(
        artifact_id=fixture["artifact_id"],
        mode="track_a",
        artifact_safety={"time_safe":True,"document_safe":True,"title_safe":True},
        content=fixture["structured_detector_inputs"],
        metadata={"target_doi":fixture["target_doi"]},
    )
    out = run_forensics(context, [CrossSourceFieldConsistencyDetector()])
    assert out["review_priority"] == "MODERATE"
    assert out["artifact_safety"]["extraction"]["safe"] is True
    assert out["artifact_safety"]["extraction"]["structured_record_count"] == 1
    f=out["findings"][0]
    expected=fixture["expected_result"]
    assert f["detector_id"] == expected["detector_id"]
    assert f["status"] == expected["status"]
    assert f["evidence_class"] == expected["evidence_class"]
    assert f["evidence"]["matched_fields"] == expected["matched_fields"]
    assert [m["field"] for m in f["evidence"]["mismatches"]] == expected["mismatch_fields"]
    assert f["misconduct_inference"] is False
