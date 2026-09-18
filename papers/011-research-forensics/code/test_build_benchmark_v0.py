import csv
from pathlib import Path

from build_benchmark_v0 import enrich, issue_codes, normalize_doi, write_csv


def test_normalize_doi():
    assert normalize_doi("https://doi.org/10.1234/ABC") == "10.1234/abc"


def test_reason_coding_is_candidate_only():
    assert "image_integrity" in issue_codes("Concerns about duplicated image panels")


def test_enrich_deduplicates_notice_identity():
    row = {
        "doi": "10.1/x",
        "title": "x",
        "year": "2024",
        "journal": "j",
        "notice_type": "Retraction",
        "notice_date": "2025-01-01",
        "raw_reason": "image duplication",
        "source_url": "https://example.invalid",
    }
    rows = enrich([row, dict(row)])
    assert len(rows) == 1
    assert rows[0]["candidate_issue_codes"] == "image_integrity"


def test_track_a_can_be_written_without_label_defining_fields(tmp_path: Path):
    rows = [{
        "doi": "10.1/x",
        "title": "x",
        "year": "2024",
        "journal": "j",
        "notice_type": "Retraction",
        "notice_date": "2025-01-01",
        "raw_reason": "image duplication",
        "source_url": "https://example.invalid",
    }]
    rows = enrich(rows)
    forbidden = {
        "raw_reason", "notice_type", "notice_date", "source_url",
        "candidate_issue_codes", "ground_truth_tier",
    }
    fields = [k for k in rows[0] if k not in forbidden]
    out = tmp_path / "a.csv"
    write_csv(out, rows, fields)
    header = next(csv.reader(out.open(encoding="utf-8")))
    assert forbidden.isdisjoint(header)
