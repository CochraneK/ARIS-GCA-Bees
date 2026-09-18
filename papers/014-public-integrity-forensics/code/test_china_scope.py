from china_scope import (
    CHINA_PRIORITY_INSTITUTION_TYPES,
    ChinaSourceTier,
    InstitutionType,
    china_high_priority_allowed,
    source_policy,
)


def test_china_scope_includes_non_government_priority_institutions():
    assert InstitutionType.HOSPITAL in CHINA_PRIORITY_INSTITUTION_TYPES
    assert InstitutionType.SOE in CHINA_PRIORITY_INSTITUTION_TYPES
    assert InstitutionType.RESEARCH_INSTITUTE in CHINA_PRIORITY_INSTITUTION_TYPES
    assert InstitutionType.UNIVERSITY in CHINA_PRIORITY_INSTITUTION_TYPES
    assert InstitutionType.NGO_OR_SOCIAL_ORGANIZATION in CHINA_PRIORITY_INSTITUTION_TYPES


def test_public_social_web_is_lead_only():
    policy = source_policy(ChinaSourceTier.CN_F_PUBLIC_WEB_LEAD)
    assert policy.lead_only is True
    assert policy.max_evidence_class == "E5"
    assert china_high_priority_allowed(
        source_tier=ChinaSourceTier.CN_F_PUBLIC_WEB_LEAD,
        identity_resolved=True,
        temporally_valid=True,
        independent_corroboration=True,
    ) is False


def test_official_source_still_needs_identity_time_and_independent_support():
    assert china_high_priority_allowed(
        source_tier=ChinaSourceTier.CN_A_OFFICIAL_STRUCTURED,
        identity_resolved=True,
        temporally_valid=True,
        independent_corroboration=True,
    ) is True
    assert china_high_priority_allowed(
        source_tier=ChinaSourceTier.CN_A_OFFICIAL_STRUCTURED,
        identity_resolved=False,
        temporally_valid=True,
        independent_corroboration=True,
    ) is False
    assert china_high_priority_allowed(
        source_tier=ChinaSourceTier.CN_C_OFFICIAL_OUTCOME,
        identity_resolved=True,
        temporally_valid=True,
        independent_corroboration=False,
    ) is False
