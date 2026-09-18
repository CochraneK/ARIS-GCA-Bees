from metadata_safety import extract_target_metadata, sanitize_title


def test_strips_retracted_prefix():
    safe, flagged = sanitize_title("RETRACTED: Example paper")
    assert safe == "Example paper"
    assert flagged


def test_strips_retracted_article_prefix():
    safe, flagged = sanitize_title("RETRACTED ARTICLE: Example paper")
    assert safe == "Example paper"
    assert flagged


def test_clean_title_is_unchanged():
    safe, flagged = sanitize_title("Example paper")
    assert safe == "Example paper"
    assert not flagged


def test_extract_target_metadata_flags_current_outcome_leakage():
    payload = {
        "message": {
            "DOI": "10.1/x",
            "title": ["RETRACTED: Example paper"],
            "published": {"date-parts": [[2020, 5, 1]]},
            "container-title": ["Journal X"],
            "type": "journal-article",
            "publisher": "Publisher X",
            "updated-by": [{"type": "retraction"}],
        }
    }
    row = extract_target_metadata(payload, "10.1/x")
    assert row["target_title_safe"] == "Example paper"
    assert row["title_status_marker"] == "1"
    assert row["current_metadata_contains_update_relations"] == "1"
    assert row["track_a_title_requires_historical_validation"] == "1"
