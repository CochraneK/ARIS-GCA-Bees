from orchestrator import (
    Applicability,
    Finding,
    ForensicContext,
    review_priority,
    run_forensics,
)


class FixedDetector:
    def __init__(self, detector_id, family, finding=None, applicable=True):
        self.detector_id = detector_id
        self.detector_version = "test"
        self.family = family
        self._finding = finding
        self._applicable = applicable

    def applicability(self, context):
        return Applicability(self._applicable, "test applicability")

    def run(self, context):
        return [self._finding]


def flag(detector_id, family, evidence_class, dependency):
    return Finding(
        detector_id=detector_id,
        detector_version="test",
        family=family,
        applicable=True,
        applicability_reason="",
        status="FLAG",
        evidence_class=evidence_class,
        claim="test flag",
        source_locator="Table 1",
        evidence={"x": 1},
        reproducible="yes",
        benign_explanations=["reporting error"],
        dependency_group=dependency,
        misconduct_inference=False,
    )


def test_track_a_fails_closed_without_time_safe_artifact():
    ctx = ForensicContext(
        artifact_id="x",
        mode="track_a",
        artifact_safety={"time_safe": False, "document_safe": True, "title_safe": True},
    )
    out = run_forensics(ctx, [])
    assert out["review_priority"] == "BLOCKED"
    assert out["artifact_safety"]["eligible"] is False


def test_track_b_does_not_require_historical_artifact():
    ctx = ForensicContext(artifact_id="x", mode="track_b")
    out = run_forensics(ctx, [])
    assert out["review_priority"] == "NONE"
    assert out["artifact_safety"]["eligible"] is True


def test_non_applicable_detector_abstains_not_passes():
    d = FixedDetector("d", "citation_forensics", applicable=False)
    ctx = ForensicContext(artifact_id="x", mode="ad_hoc")
    out = run_forensics(ctx, [d])
    assert out["findings"][0]["status"] == "ABSTAIN"
    assert "citation_forensics" in out["coverage"]["abstained_families"]


def test_two_independent_strong_families_raise_high():
    a = flag("a", "statistical_inference", "E1", "p-value")
    b = flag("b", "image_forensics", "E3", "figure-pair")
    assert review_priority([a.finalize(), b.finalize()]) == "HIGH"


def test_same_family_does_not_fake_independent_corroboration():
    a = flag("a", "statistical_inference", "E1", "p-value-1")
    b = flag("b", "statistical_inference", "E1", "p-value-2")
    assert review_priority([a.finalize(), b.finalize()]) == "MODERATE"


def test_e5_alone_never_high():
    a = flag("ai", "genai_provenance", "E5", "style")
    assert review_priority([a.finalize()]) == "LOW"


def test_detector_cannot_emit_misconduct_inference():
    bad = flag("bad", "text_papermill", "E4", "text")
    bad.misconduct_inference = True
    d = FixedDetector("bad", "text_papermill", finding=bad)
    ctx = ForensicContext(artifact_id="x")
    out = run_forensics(ctx, [d])
    assert out["findings"][0]["status"] == "ERROR"
