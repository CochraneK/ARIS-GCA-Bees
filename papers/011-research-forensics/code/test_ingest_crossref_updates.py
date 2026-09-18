import json
from pathlib import Path

from ingest_crossref_updates import extract_assertions, event_summary


HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parent / "data" / "fixtures" / "crossref_updates_seed.json"


def payload():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_separate_notice_points_to_target_article():
    rows = extract_assertions(payload())
    r = next(
        x for x in rows
        if x["crossref_source_work_doi"] == "10.1177/17588359211061903"
        and x["assertion_source"] == "retraction-watch"
    )
    assert r["target_doi"] == "10.1177/1758835919874651"
    assert r["notice_doi"] == "10.1177/17588359211061903"
    assert r["target_metadata_resolved"] == "0"


def test_self_relation_has_no_separate_notice_doi():
    rows = extract_assertions(payload())
    r = next(
        x for x in rows
        if x["crossref_source_work_doi"] == "10.1007/s11277-021-09072-0"
        and x["assertion_source"] == "retraction-watch"
    )
    assert r["target_doi"] == r["crossref_source_work_doi"]
    assert r["notice_doi"] == ""


def test_publisher_and_retraction_watch_assertions_are_preserved():
    rows = extract_assertions(payload())
    same = [
        x for x in rows
        if x["target_doi"] == "10.1177/1758835919874651"
        and x["update_date"] == "2021-12-15"
    ]
    assert {x["assertion_source"] for x in same} == {
        "publisher", "retraction-watch"
    }
    assert len({x["assertion_key"] for x in same}) == 2
    assert len({x["event_key"] for x in same}) == 1


def test_event_summary_collapses_provenance_only_at_event_level():
    events = event_summary(extract_assertions(payload()))
    e = next(x for x in events if x["target_doi"] == "10.1177/1758835919874651")
    assert e["assertion_count"] == "2"
    assert e["assertion_sources"] == "publisher;retraction-watch"
