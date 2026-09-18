from datetime import date

from jsonschema import Draft202012Validator, RefResolver
import json
from pathlib import Path

from open_integrity_agent import ContractRecord, IntegrityCase, SourceRef
from report_builder import build_report


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "agent/public-integrity-forensics/assets"


def case_with_publication(published_at=date(2026, 1, 5)):
    src = SourceRef(
        "synthetic",
        "r1",
        published_at=published_at,
    )
    return IntegrityCase(
        subject_id="case-report",
        contract=ContractRecord(
            contract_id="c1",
            authority_id="a1",
            supplier_ids=("s1",),
            award_date=date(2026, 1, 4),
            bid_count=1,
            source_refs=(src,),
        ),
        source_coverage={"procurement_award", "procurement_competition"},
    )


def test_report_preserves_missing_coverage_and_no_corruption_inference():
    report = build_report(case_with_publication())
    assert report["corruption_inference"] is False
    assert "ownership" in report["source_coverage"]["missing"]
    assert report["evidence_graph"]["corruption_inference"] is False
    assert report["findings"]
    assert all(x["corruption_inference"] is False for x in report["findings"])


def test_graph_finding_ids_match_report_finding_ids():
    report = build_report(case_with_publication())
    report_ids = {x["finding_id"] for x in report["findings"]}
    graph_ids = {
        x["id"] for x in report["evidence_graph"]["nodes"]
        if x["type"] == "detector_finding"
    }
    assert graph_ids == report_ids


def test_track_a_blocks_if_source_is_after_cutoff():
    report = build_report(
        case_with_publication(date(2026, 2, 1)),
        mode="track_a",
        cutoff=date(2026, 1, 31),
    )
    assert report["time_safety"]["eligible"] is False
    assert report["review_priority"] == "BLOCKED"


def test_track_a_blocks_if_publication_time_unknown():
    report = build_report(
        case_with_publication(None),
        mode="track_a",
        cutoff=date(2026, 1, 31),
    )
    assert report["time_safety"]["eligible"] is False
    assert report["review_priority"] == "BLOCKED"


def test_report_validates_against_agent_schema():
    finding_schema = json.loads(
        (ASSETS / "finding.schema.json").read_text(encoding="utf-8")
    )
    report_schema = json.loads(
        (ASSETS / "report.schema.json").read_text(encoding="utf-8")
    )
    resolver = RefResolver.from_schema(
        report_schema,
        store={"finding.schema.json": finding_schema},
    )
    Draft202012Validator(report_schema, resolver=resolver).validate(
        build_report(case_with_publication())
    )
