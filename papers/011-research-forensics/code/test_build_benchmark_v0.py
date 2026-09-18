import csv
from pathlib import Path

from build_benchmark_v0 import (
    LABEL_PROVENANCE_FIELDS,
    TRACK_A_FEATURE_ALLOWLIST,
    enrich,
    issue_codes,
    normalize_doi,
    track_a_rows,
    write_csv,
)


def row(**extra):
    base = {
        "target_doi": "10.1/x",
        "target_title_safe": "Example paper",
        "target_year": "2024",
        "target_journal": "Journal X",
        "notice_type": "Retraction",
        "notice_date": "2025-01-01",
        "raw_reason": "image duplication",
        "source_url": "https://example.invalid",
        "track_a_title_requires_historical_validation": "0",
        "track_a_document_safe": "1",
    }
    base.update(extra)
    return base


def test_normalize_doi():
    assert normalize_doi("https://doi.org/10.1234/ABC") == "10.1234/abc"


def test_reason_coding_is_candidate_only():
    assert "image_integrity" in issue_codes("Concerns about duplicated image panels")
    assert "authorship_peer_review" in issue_codes("illegal gift authorship case")


def test_enrich_deduplicates_notice_identity():
    rows = enrich([row(), row()])
    assert len(rows) == 1
    assert rows[0]["candidate_issue_codes"] == "image_integrity"
    assert rows[0]["paper_id"].startswith("p_")


def test_track_a_allowlist_excludes_all_label_provenance():
    rows = enrich([row(
        event_key="secret-event",
        notice_doi="10.1/notice",
        target_title_raw_current="RETRACTED: Example paper",
        title_status_marker="1",
    )])
    projected, fields = track_a_rows(rows)
    assert LABEL_PROVENANCE_FIELDS.isdisjoint(fields)
    assert "target_doi" not in fields
    assert "target_journal" not in fields
    assert "target_year" not in fields
    assert set(TRACK_A_FEATURE_ALLOWLIST).issubset(fields)
    assert projected[0]["target_title_safe"] == "Example paper"


def test_track_a_is_ineligible_until_document_is_safe():
    x = enrich([row(track_a_document_safe="0")])[0]
    assert x["track_a_eligible"] == "0"


def test_historical_title_validation_gate_blocks_track_a():
    x = enrich([row(track_a_title_requires_historical_validation="1")])[0]
    assert x["track_a_eligible"] == "0"


def test_track_a_can_be_written_without_label_fields(tmp_path: Path):
    rows = enrich([row()])
    projected, fields = track_a_rows(rows)
    out = tmp_path / "a.csv"
    write_csv(out, projected, fields)
    header = next(csv.reader(out.open(encoding="utf-8")))
    assert LABEL_PROVENANCE_FIELDS.isdisjoint(header)
