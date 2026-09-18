from artifact_safety import assess_track_a_artifact


def test_exact_historical_snapshot_is_track_a_safe():
    q = assess_track_a_artifact(
        artifact_version_date="2020-01-01",
        outcome_date="2022-01-01",
        immutable_or_historical_snapshot=True,
        historical_equivalence="archive_snapshot_of_published_version",
        provenance_source="publisher archive snapshot",
        title="A normal scientific article",
        filename_or_path="paper.pdf",
        leading_text="Abstract\n...",
    )
    assert q.status == "SAFE_EXACT"
    assert q.track_a_eligible is True


def test_preprint_is_proxy_not_primary_track_a():
    q = assess_track_a_artifact(
        artifact_version_date="2020-01-01",
        outcome_date="2022-01-01",
        immutable_or_historical_snapshot=True,
        historical_equivalence="preprint_proxy",
        provenance_source="bioRxiv v1",
        title="A normal scientific article",
        filename_or_path="v1.pdf",
        leading_text="Abstract\n...",
    )
    assert q.status == "PROXY_ONLY"
    assert q.track_a_eligible is False
    assert q.proxy_eligible is True


def test_current_corrected_publisher_page_is_blocked():
    q = assess_track_a_artifact(
        artifact_version_date="2026-07-13",
        outcome_date="2026-07-13",
        immutable_or_historical_snapshot=False,
        historical_equivalence="same_published_version",
        provenance_source="current publisher HTML",
        title="A scientific article",
        leading_text="This article has been corrected. A correction to this article is available.",
    )
    assert q.status == "BLOCKED"
    assert any("not demonstrably earlier" in x for x in q.reasons)
    assert any("status/update marker" in x for x in q.reasons)


def test_retracted_title_is_blocked_even_with_old_date():
    q = assess_track_a_artifact(
        artifact_version_date="2019-01-01",
        outcome_date="2021-12-15",
        immutable_or_historical_snapshot=True,
        historical_equivalence="same_published_version",
        provenance_source="snapshot",
        title="RETRACTED: Example article",
    )
    assert q.status == "BLOCKED"
    assert any("Title contains" in x for x in q.reasons)


def test_label_bearing_dataset_path_is_blocked():
    q = assess_track_a_artifact(
        artifact_version_date="2019-01-01",
        outcome_date="2021-12-15",
        immutable_or_historical_snapshot=True,
        historical_equivalence="same_published_version",
        provenance_source="snapshot",
        title="Example article",
        filename_or_path="test/retracted/paper.pdf",
    )
    assert q.status == "BLOCKED"
    assert any("Filename/path" in x for x in q.reasons)


def test_current_update_relation_is_warning_if_artifact_itself_is_historical():
    q = assess_track_a_artifact(
        artifact_version_date="2019-01-01",
        outcome_date="2021-12-15",
        immutable_or_historical_snapshot=True,
        historical_equivalence="same_published_version",
        provenance_source="historical PDF",
        title="Example article",
        filename_or_path="paper.pdf",
        current_metadata_has_update_relation=True,
    )
    assert q.status == "SAFE_EXACT"
    assert q.warnings
