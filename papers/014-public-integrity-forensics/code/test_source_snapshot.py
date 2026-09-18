from datetime import date, datetime, timezone

from source_snapshot import make_snapshot, track_a_eligibility


def test_snapshot_hash_is_stable_under_json_key_order():
    a = make_snapshot(
        {"b": 2, "a": 1},
        source_name="synthetic",
        source_record_id="1",
        source_url="",
        parser_version="0.1",
        retrieved_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    b = make_snapshot(
        {"a": 1, "b": 2},
        source_name="synthetic",
        source_record_id="1",
        source_url="",
        parser_version="0.1",
        retrieved_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    assert a.sha256 == b.sha256


def test_track_a_unknown_publication_time_is_not_assumed_safe():
    snap = make_snapshot(
        {"x": 1},
        source_name="synthetic",
        source_record_id="1",
        source_url="",
        parser_version="0.1",
        published_at=None,
    )
    ok, reason = track_a_eligibility(
        snap, datetime(2026, 1, 31, tzinfo=timezone.utc)
    )
    assert ok is False
    assert reason == "publication_time_unknown"


def test_track_a_future_publication_is_excluded():
    snap = make_snapshot(
        {"x": 1},
        source_name="synthetic",
        source_record_id="1",
        source_url="",
        parser_version="0.1",
        published_at=datetime(2026, 2, 1, tzinfo=timezone.utc),
    )
    ok, reason = track_a_eligibility(
        snap, datetime(2026, 1, 31, tzinfo=timezone.utc)
    )
    assert ok is False
    assert reason == "published_after_cutoff"
