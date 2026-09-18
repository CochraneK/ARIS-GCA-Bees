from artifact_search_manifest import build_rows


def candidate(**overrides):
    base = {
        "target_doi": "10.1000/test",
        "event_date": "2024-03-21",
        "issue_code": "table_error",
        "object_role": "table",
        "candidate_url": "https://example.org/article",
        "archive_query_pattern": "https://example.org/article*",
        "identity_marker": "/article",
        "source_kind": "publisher",
        "equivalence_intent": "same_published_version",
        "current_state": "UNKNOWN",
        "note": "",
    }
    base.update(overrides)
    return base


def test_manifest_uses_fail_closed_cdx_cutoff():
    row = build_rows([candidate()])[0]
    assert "to=20240320" in row["cdx_query_url"]
    assert row["qualification_status"] == "DISCOVERY_ONLY"


def test_manifest_keeps_identity_marker_separate_from_query_pattern():
    row = build_rows([candidate(identity_marker="/54_1_1/")])[0]
    assert row["identity_marker"] == "/54_1_1/"
    assert "identity_marker" not in row["cdx_query_url"]


def test_manifest_rejects_missing_event_date():
    bad = candidate(event_date="")
    try:
        build_rows([bad])
    except ValueError as exc:
        assert "event_date" in str(exc)
    else:
        raise AssertionError("missing event date should fail")
