from artifact_safety import (
    ArtifactObject,
    qualify_issue_artifact_set,
)


def test_text_can_be_safe_while_image_is_blocked():
    objects = [
        ArtifactObject("html-2022", "body_text", "SAFE_EXACT"),
        ArtifactObject("html-2022-caption", "figure_caption", "SAFE_EXACT"),
        ArtifactObject("fig1-unarchived", "figure_image", "BLOCKED"),
    ]
    text_q = qualify_issue_artifact_set(objects, ["body_text"])
    image_q = qualify_issue_artifact_set(objects, ["figure_image"])

    assert text_q.status == "SAFE_EXACT"
    assert text_q.track_a_eligible is True
    assert image_q.status == "BLOCKED"
    assert image_q.track_a_eligible is False


def test_multirole_issue_requires_every_role():
    objects = [
        ArtifactObject("html", "body_text", "SAFE_EXACT"),
        ArtifactObject("table", "table", "SAFE_EXACT"),
    ]
    q = qualify_issue_artifact_set(objects, ["body_text", "table"])
    assert q.status == "SAFE_EXACT"
    assert set(q.exact_roles) == {"body_text", "table"}


def test_proxy_role_downgrades_entire_issue_to_proxy():
    objects = [
        ArtifactObject("published-html", "body_text", "SAFE_EXACT"),
        ArtifactObject("preprint-table", "table", "PROXY_ONLY"),
    ]
    q = qualify_issue_artifact_set(objects, ["body_text", "table"])
    assert q.status == "PROXY_ONLY"
    assert q.track_a_eligible is False
    assert q.proxy_eligible is True
    assert q.proxy_roles == ["table"]


def test_missing_role_blocks_issue():
    objects = [ArtifactObject("html", "body_text", "SAFE_EXACT")]
    q = qualify_issue_artifact_set(objects, ["body_text", "figure_image"])
    assert q.status == "BLOCKED"
    assert q.missing_or_blocked_roles == ["figure_image"]


def test_no_roles_declared_fails_closed():
    q = qualify_issue_artifact_set([], [])
    assert q.status == "BLOCKED"
    assert q.track_a_eligible is False
