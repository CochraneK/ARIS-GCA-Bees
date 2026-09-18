from datetime import datetime, timezone

from china_scope import ChinaSourceTier, InstitutionType
from china_web_leads import (
    ChinaWebLead,
    lead_can_enter_strong_review,
    safe_public_summary,
    track_a_web_eligible,
)


def lead(tier=ChinaSourceTier.CN_F_PUBLIC_WEB_LEAD, published=True):
    return ChinaWebLead(
        lead_id="lead-1",
        url="https://example.org/public-page",
        source_tier=tier,
        institution_type=InstitutionType.HOSPITAL,
        title="Public page",
        claim="A public page states a procurement relationship.",
        retrieved_at=datetime(2026, 9, 18, tzinfo=timezone.utc),
        published_at=(
            datetime(2026, 1, 1, tzinfo=timezone.utc) if published else None
        ),
        source_name="example",
    )


def test_social_web_lead_never_becomes_strong_by_itself():
    x = lead()
    assert lead_can_enter_strong_review(
        x,
        identity_resolved=True,
        time_validated=True,
        corroborated_independently=True,
    ) is False
    assert safe_public_summary(x)["corruption_inference"] is False


def test_official_structured_still_requires_independent_corroboration():
    x = lead(ChinaSourceTier.CN_A_OFFICIAL_STRUCTURED)
    assert lead_can_enter_strong_review(
        x,
        identity_resolved=True,
        time_validated=True,
        corroborated_independently=False,
    ) is False
    assert lead_can_enter_strong_review(
        x,
        identity_resolved=True,
        time_validated=True,
        corroborated_independently=True,
    ) is True


def test_track_a_unknown_publication_time_blocks_web_lead():
    ok, reason = track_a_web_eligible(
        lead(published=False),
        datetime(2026, 1, 31, tzinfo=timezone.utc),
    )
    assert ok is False
    assert reason == "publication_time_unknown"
