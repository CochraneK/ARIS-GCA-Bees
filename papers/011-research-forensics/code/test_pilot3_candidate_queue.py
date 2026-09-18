from pilot3_candidate_queue import build_queue, score_candidate


def base(**overrides):
    row = {
        "candidate_id": "x",
        "target_doi": "10.1000/x",
        "correction_doi": "10.1000/x.c",
        "target_published": "2023-01-01",
        "correction_published": "2025-01-02",
        "issue_code": "table_numeric_error",
        "required_role": "table",
        "detector_family": "F3",
        "verification_mode": "DETERMINISTIC_INTERNAL",
        "artifact_state": "PRE_EVENT_HTML_ONLY",
        "scientific_content": "YES",
        "benchmark_role": "POSITIVE_CASE",
        "candidate_state": "ACTIVE",
        "source_url": "https://example.org",
        "note": "",
    }
    row.update(overrides)
    return row


def test_high_value_table_case_is_priority():
    out = score_candidate(base())
    assert out["priority_score"] == "21"
    assert out["queue_status"] == "PRIORITY"


def test_completed_case_stays_complete_even_with_high_score():
    out = score_candidate(base(
        candidate_state="COMPLETE",
        artifact_state="SAFE_EXACT_READY",
        verification_mode="CROSS_SOURCE",
    ))
    assert out["queue_status"] == "COMPLETE"


def test_format_only_case_is_control_not_priority():
    out = score_candidate(base(
        benchmark_role="FORMAT_CONTROL",
        scientific_content="NO",
        verification_mode="FORMAT_CONTROL",
        artifact_state="SAFE_EXACT_TARGET",
    ))
    assert out["queue_status"] == "CONTROL"


def test_longer_archive_window_scores_higher():
    long_case = score_candidate(base(
        target_published="2020-01-01",
        correction_published="2025-01-01",
    ))
    short_case = score_candidate(base(
        target_published="2024-12-01",
        correction_published="2025-01-01",
    ))
    assert int(long_case["priority_score"]) > int(short_case["priority_score"])


def test_queue_ranks_priority_before_secondary_and_controls():
    rows = [
        base(candidate_id="control", benchmark_role="FORMAT_CONTROL",
             scientific_content="NO", verification_mode="FORMAT_CONTROL",
             artifact_state="SAFE_EXACT_TARGET"),
        base(candidate_id="priority"),
        base(candidate_id="secondary", artifact_state="UNKNOWN",
             verification_mode="STRUCTURED_RECOMPUTE"),
    ]
    out = build_queue(rows)
    assert [r["candidate_id"] for r in out] == [
        "priority", "secondary", "control"
    ]
    assert out[0]["active_rank"] == "1"
    assert out[1]["active_rank"] == "2"
    assert out[2]["active_rank"] == ""
