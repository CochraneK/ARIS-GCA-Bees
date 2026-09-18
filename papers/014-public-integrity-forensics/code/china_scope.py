"""China-first scope and source policy for OpenIntegrity.

This module contains no scraping logic. It gives the agent a stable institution
ontology and evidence-source policy so China web-mining adapters do not silently
collapse hospitals, SOEs, institutes, NGOs and government bodies into one type.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class InstitutionType(str, Enum):
    GOVERNMENT = "government"
    PUBLIC_INSTITUTION = "public_institution"
    HOSPITAL = "hospital"
    SOE = "soe"
    RESEARCH_INSTITUTE = "research_institute"
    UNIVERSITY = "university"
    NGO_OR_SOCIAL_ORGANIZATION = "ngo_or_social_organization"
    STATE_OWNED_FINANCIAL_INSTITUTION = "state_owned_financial_institution"
    PROCUREMENT_AGENCY = "procurement_agency"
    PRIVATE_SUPPLIER = "private_supplier"
    OTHER = "other"


class ChinaSourceTier(str, Enum):
    CN_A_OFFICIAL_STRUCTURED = "CN-A"
    CN_B_OFFICIAL_WEB = "CN-B"
    CN_C_OFFICIAL_OUTCOME = "CN-C"
    CN_D_REPUTABLE_JOURNALISM = "CN-D"
    CN_E_LICENSED_COMMERCIAL = "CN-E"
    CN_F_PUBLIC_WEB_LEAD = "CN-F"


@dataclass(frozen=True)
class ChinaSourcePolicy:
    tier: ChinaSourceTier
    default_role: str
    max_evidence_class: str
    can_support_negative_pass: bool
    lead_only: bool
    notes: str


SOURCE_POLICIES = {
    ChinaSourceTier.CN_A_OFFICIAL_STRUCTURED: ChinaSourcePolicy(
        ChinaSourceTier.CN_A_OFFICIAL_STRUCTURED,
        "primary_record",
        "E3",
        True,
        False,
        "Structured official records can support strong factual/provenance findings after identity and temporal validation.",
    ),
    ChinaSourceTier.CN_B_OFFICIAL_WEB: ChinaSourcePolicy(
        ChinaSourceTier.CN_B_OFFICIAL_WEB,
        "primary_record",
        "E2",
        False,
        False,
        "Official webpages/PDFs can establish published facts but absence from one webpage is rarely complete negative coverage.",
    ),
    ChinaSourceTier.CN_C_OFFICIAL_OUTCOME: ChinaSourcePolicy(
        ChinaSourceTier.CN_C_OFFICIAL_OUTCOME,
        "outcome_or_official_finding",
        "E2",
        False,
        False,
        "Keep investigation, sanction, audit finding, penalty and judgment as distinct outcome classes.",
    ),
    ChinaSourceTier.CN_D_REPUTABLE_JOURNALISM: ChinaSourcePolicy(
        ChinaSourceTier.CN_D_REPUTABLE_JOURNALISM,
        "discovery_or_corroboration",
        "E1",
        False,
        False,
        "Journalism can corroborate chronology or locate records; allegations are not official adjudications.",
    ),
    ChinaSourceTier.CN_E_LICENSED_COMMERCIAL: ChinaSourcePolicy(
        ChinaSourceTier.CN_E_LICENSED_COMMERCIAL,
        "optional_enrichment",
        "E2",
        False,
        False,
        "Use only under licence/terms and retain original provenance where supplied.",
    ),
    ChinaSourceTier.CN_F_PUBLIC_WEB_LEAD: ChinaSourcePolicy(
        ChinaSourceTier.CN_F_PUBLIC_WEB_LEAD,
        "lead_generation",
        "E5",
        False,
        True,
        "Social/public-web content cannot by itself create a consequential or high-priority integrity conclusion.",
    ),
}


CHINA_PRIORITY_INSTITUTION_TYPES = {
    InstitutionType.GOVERNMENT,
    InstitutionType.PUBLIC_INSTITUTION,
    InstitutionType.HOSPITAL,
    InstitutionType.SOE,
    InstitutionType.RESEARCH_INSTITUTE,
    InstitutionType.UNIVERSITY,
    InstitutionType.NGO_OR_SOCIAL_ORGANIZATION,
    InstitutionType.STATE_OWNED_FINANCIAL_INSTITUTION,
}


def source_policy(tier: ChinaSourceTier) -> ChinaSourcePolicy:
    return SOURCE_POLICIES[tier]


def china_high_priority_allowed(
    *,
    source_tier: ChinaSourceTier,
    identity_resolved: bool,
    temporally_valid: bool,
    independent_corroboration: bool,
) -> bool:
    """Conservative source-layer gate, not a corruption classifier."""
    policy = source_policy(source_tier)
    if policy.lead_only:
        return False
    if not identity_resolved or not temporally_valid:
        return False
    return independent_corroboration and policy.max_evidence_class in {"E2", "E3"}
