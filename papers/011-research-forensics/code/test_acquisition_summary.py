from acquisition_summary import summarize_all


def req(doi, status, roles="", issue="x"):
    return {
        "target_doi": doi,
        "stratum": "E",
        "ground_truth_tier": "GT-B",
        "issue_code": issue,
        "track_a_issue_status": status,
        "required_roles": roles,
        "eligible_detector_families": "",
        "rationale": "",
    }


def obj(doi, role, status):
    return {
        "target_doi": doi,
        "object_role": role,
        "status": status,
    }


def test_exact_required_role_is_ready():
    rows, summary = summarize_all(
        [req("10.x/a", "CONTENT_ELIGIBLE", "table")],
        [obj("10.x/a", "table", "SAFE_EXACT")],
    )
    assert rows[0]["issue_readiness"] == "SAFE_EXACT_READY"
    assert summary["safe_exact_issue_ready_count"] == 1


def test_safe_body_does_not_make_missing_image_ready():
    rows, summary = summarize_all(
        [req("10.x/a", "CONTENT_ELIGIBLE", "figure_image")],
        [obj("10.x/a", "body_text", "SAFE_EXACT")],
    )
    assert rows[0]["issue_readiness"] == "BLOCKED_REQUIRED_ROLE"
    assert rows[0]["role_states"] == "figure_image:NO_OBJECT"
    assert summary["targets_with_any_safe_exact_object"] == 1


def test_blocked_required_object_remains_blocked():
    rows, _ = summarize_all(
        [req("10.x/a", "CONTENT_ELIGIBLE", "figure_image")],
        [obj("10.x/a", "figure_image", "BLOCKED")],
    )
    assert rows[0]["issue_readiness"] == "BLOCKED_REQUIRED_ROLE"
    assert rows[0]["role_states"] == "figure_image:BLOCKED"


def test_content_ineligible_not_counted_as_detector_failure():
    rows, summary = summarize_all(
        [req("10.x/a", "CONTENT_INELIGIBLE")],
        [obj("10.x/a", "body_text", "SAFE_EXACT")],
    )
    assert rows[0]["issue_readiness"] == "TRACK_A_INELIGIBLE_CONTENT"
    assert summary["content_eligible_issue_count"] == 0
    assert summary["targets_with_any_safe_exact_object"] == 1


def test_seed_shape_counts_three_eligible_two_ineligible_one_adjudication():
    requirements = [
        req("1", "CONTENT_ELIGIBLE", "figure_image"),
        req("2", "CONTENT_ELIGIBLE", "figure_image"),
        req("3", "CONTENT_ELIGIBLE", "table"),
        req("4", "CONTENT_INELIGIBLE"),
        req("5", "ADJUDICATION_REQUIRED"),
        req("6", "CONTENT_INELIGIBLE"),
    ]
    rows, summary = summarize_all(requirements, [])
    assert len(rows) == 6
    assert summary["content_eligible_issue_count"] == 3
    assert summary["content_ineligible_issue_count"] == 2
    assert summary["adjudication_required_issue_count"] == 1
    assert summary["blocked_required_role_count"] == 3
