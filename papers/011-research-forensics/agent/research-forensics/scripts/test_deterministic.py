import math

from orchestrator import ForensicContext, run_forensics
from detectors.deterministic import (
    CrossSourceFieldConsistencyDetector,
    DebitStyleBinaryDetector,
    GRIMItemMeanDetector,
    NHSTConsistencyDetector,
    ReferenceMetadataDetector,
    TableArithmeticDetector,
    p_is_consistent,
)


def context(**content):
    return ForensicContext(
        artifact_id="pilot1",
        mode="ad_hoc",
        content=content,
    )


def test_p_rounding_and_inequality():
    assert p_is_consistent(0.0324, ".032")
    assert p_is_consistent(0.0004, "<.001")
    assert not p_is_consistent(0.084, ".032")


def test_nhst_t_pass_and_flag():
    d = NHSTConsistencyDetector()
    ctx = context(nhst_tests=[
        {"test_type": "t", "statistic": 2.0, "df": 30, "reported_p": ".055", "source_locator": "pass"},
        {"test_type": "t", "statistic": 2.0, "df": 30, "reported_p": ".010", "source_locator": "flag"},
    ])
    out = run_forensics(ctx, [d])
    statuses = [x["status"] for x in out["findings"]]
    assert statuses == ["PASS", "FLAG"]


def test_nhst_record_specific_abstain_is_preserved():
    d = NHSTConsistencyDetector()
    ctx = context(nhst_tests=[
        {"test_type": "unsupported", "statistic": 1, "reported_p": ".1", "source_locator": "x"},
        {"test_type": "z", "statistic": 1.96, "reported_p": ".050", "source_locator": "y"},
    ])
    out = run_forensics(ctx, [d])
    assert out["findings"][0]["status"] == "ABSTAIN"
    assert out["findings"][0]["applicable"] is False
    assert out["findings"][1]["status"] == "PASS"


def test_grim_possible_and_impossible():
    d = GRIMItemMeanDetector()
    ctx = context(discrete_means=[
        {"reported_mean": "6.96", "n": 25, "scale_min": 1, "scale_max": 7, "integer_valued": True, "source_locator": "a"},
        {"reported_mean": "6.98", "n": 25, "scale_min": 1, "scale_max": 7, "integer_valued": True, "source_locator": "b"},
    ])
    out = run_forensics(ctx, [d])
    assert [x["status"] for x in out["findings"]] == ["PASS", "FLAG"]


def test_grim_refuses_noninteger_record():
    d = GRIMItemMeanDetector()
    ctx = context(discrete_means=[
        {"reported_mean": "4.20", "n": 20, "scale_min": 1, "scale_max": 7, "integer_valued": True},
        {"reported_mean": "4.20", "n": 20, "scale_min": 1, "scale_max": 7, "integer_valued": False},
    ])
    out = run_forensics(ctx, [d])
    assert out["findings"][1]["status"] == "ABSTAIN"
    assert out["findings"][1]["applicable"] is False


def test_binary_summary_pass_and_flag():
    d = DebitStyleBinaryDetector()
    # n=10, k=5 -> mean=.50; sample SD ~=.527
    ctx = context(binary_summaries=[
        {"binary": True, "n": 10, "reported_mean": ".50", "reported_sd": ".527", "sample_sd": True, "source_locator": "ok"},
        {"binary": True, "n": 10, "reported_mean": ".50", "reported_sd": ".200", "sample_sd": True, "source_locator": "bad"},
    ])
    out = run_forensics(ctx, [d])
    assert [x["status"] for x in out["findings"]] == ["PASS", "FLAG"]


def test_table_percentage_and_rank_gap():
    d = TableArithmeticDetector()
    ctx = context(table_checks=[
        {"check_type": "percentage", "numerator": 5, "denominator": 20, "reported_percent": "25.0", "source_locator": "pct"},
        {"check_type": "rank_sequence", "observed_ranks": [1, 2, 3, 5], "expected_start": 1, "expected_end": 5, "source_locator": "rank"},
    ])
    out = run_forensics(ctx, [d])
    assert out["findings"][0]["status"] == "PASS"
    assert out["findings"][1]["status"] == "FLAG"
    assert out["findings"][1]["evidence"]["missing_ranks"] == [4]


def test_reference_metadata_requires_provenance():
    d = ReferenceMetadataDetector()
    ctx = context(doi_resolutions=[
        {"reported_doi": "10.1000/example", "exists": True, "metadata_match": True},
        {"reported_doi": "10.1000/example", "exists": True, "metadata_match": True, "resolver": "Crossref", "verified_at": "2026-09-18"},
    ])
    out = run_forensics(ctx, [d])
    assert out["findings"][0]["status"] == "ABSTAIN"
    assert out["findings"][1]["status"] == "PASS"


def test_reference_nonexistent_is_provenance_fact_not_misconduct():
    d = ReferenceMetadataDetector()
    ctx = context(doi_resolutions=[
        {
            "reported_doi": "10.1000/does-not-exist",
            "exists": False,
            "metadata_match": None,
            "resolver": "Crossref",
            "verified_at": "2026-09-18",
            "source_locator": "ref-1",
        }
    ])
    out = run_forensics(ctx, [d])
    f = out["findings"][0]
    assert f["status"] == "FLAG"
    assert f["evidence_class"] == "E2"
    assert f["misconduct_inference"] is False


def test_table_row_completeness_catches_present_rank_with_missing_article_cell():
    d = TableArithmeticDetector()
    ctx = context(table_checks=[
        {
            "check_type": "row_completeness",
            "row_key": "rank",
            "required_fields": ["rank", "article", "citations"],
            "rows": [
                {"rank": 13, "article": "Article thirteen", "citations": "324 (18.0)"},
                {"rank": 14, "article": "", "citations": "314 (6.8)"},
                {"rank": 15, "article": "Article fifteen", "citations": "306 (18.0)"},
            ],
            "source_locator": "Table 1, ranks 13-15",
        }
    ])
    out = run_forensics(ctx, [d])
    f = out["findings"][0]
    assert f["status"] == "FLAG"
    assert f["evidence"]["missing_by_row"] == [
        {"row_key": 14, "missing_fields": ["article"]}
    ]
    assert f["misconduct_inference"] is False


def test_table_row_completeness_passes_complete_rows():
    d = TableArithmeticDetector()
    ctx = context(table_checks=[
        {
            "check_type": "row_completeness",
            "row_key": "rank",
            "required_fields": ["rank", "article", "citations"],
            "rows": [
                {"rank": 13, "article": "Article thirteen", "citations": "324 (18.0)"},
                {"rank": 14, "article": "Article fourteen", "citations": "314 (6.8)"},
            ],
        }
    ])
    out = run_forensics(ctx, [d])
    assert out["findings"][0]["status"] == "PASS"


def test_cross_source_numeric_formatting_is_not_a_false_mismatch():
    d = CrossSourceFieldConsistencyDetector()
    ctx = context(cross_source_records=[{
        "source_locator": "target Table 1",
        "target_source_locator": "target Table 1",
        "comparison_source_locator": "cited paper Results",
        "source_doi": "10.1111/example",
        "source_available_at_target_time": True,
        "provenance_verified": True,
        "fields_to_compare": ["rmsea"],
        "field_types": {"rmsea": "numeric"},
        "target_fields": {"rmsea": "0.080"},
        "source_fields": {"rmsea": "0.08"},
    }])
    out = run_forensics(ctx, [d])
    assert out["findings"][0]["status"] == "PASS"


def test_cross_source_detects_field_mismatches_without_misconduct_inference():
    d = CrossSourceFieldConsistencyDetector()
    ctx = context(cross_source_records=[{
        "source_locator": "archived PDF p.15 Table 1",
        "target_source_locator": "archived PDF p.15 Table 1, Harper & Rhodes (2021)",
        "comparison_source_locator": "Harper & Rhodes (2021), Study 2 CFA results",
        "source_doi": "10.1111/bjso.12452",
        "source_available_at_target_time": True,
        "provenance_verified": True,
        "fields_to_compare": ["n", "rmsea", "cfi", "best_fitting_model"],
        "field_types": {"n":"numeric","rmsea":"numeric","cfi":"numeric","best_fitting_model":"text"},
        "target_fields": {"n":322,"rmsea":"0.080","cfi":"0.77","best_fitting_model":"5 factors"},
        "source_fields": {"n":322,"rmsea":"0.07","cfi":"0.87","best_fitting_model":"3 factors"},
    }])
    out = run_forensics(ctx, [d])
    f = out["findings"][0]
    assert f["status"] == "FLAG"
    assert f["evidence_class"] == "E2"
    assert f["evidence"]["matched_fields"] == ["n"]
    assert [m["field"] for m in f["evidence"]["mismatches"]] == ["rmsea","cfi","best_fitting_model"]
    assert f["misconduct_inference"] is False


def test_cross_source_abstains_without_contemporaneous_source_proof():
    d = CrossSourceFieldConsistencyDetector()
    ctx = context(cross_source_records=[{
        "source_locator":"target table",
        "target_source_locator":"target table",
        "comparison_source_locator":"source results",
        "source_doi":"10.1111/example",
        "source_available_at_target_time":False,
        "provenance_verified":True,
        "fields_to_compare":["n"],
        "target_fields":{"n":10},
        "source_fields":{"n":10},
    }])
    out = run_forensics(ctx, [d])
    assert out["findings"][0]["status"] == "ABSTAIN"
