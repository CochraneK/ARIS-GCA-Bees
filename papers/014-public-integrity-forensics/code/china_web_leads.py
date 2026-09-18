"""China web-lead contract for OpenIntegrity.

A web lead is a discoverable public item, not a misconduct finding. The contract
keeps source tier, institution type, chronology and corroboration separate so
Chinese web pages, PDFs, news, social posts and official records cannot collapse
into one undifferentiated evidence pool.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from china_scope import ChinaSourceTier, InstitutionType, source_policy


@dataclass(frozen=True)
class ChinaWebLead:
    lead_id: str
    url: str
    source_tier: ChinaSourceTier
    institution_type: InstitutionType
    title: str
    claim: str
    retrieved_at: datetime
    published_at: Optional[datetime] = None
    source_name: Optional[str] = None
    stable_ids: tuple[str, ...] = ()
    entity_names: tuple[str, ...] = ()
    document_hash: Optional[str] = None
    source_record_id: Optional[str] = None
    attribution: Optional[str] = None
    corroborating_source_ids: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    corruption_inference: bool = field(default=False, init=False)

    @property
    def lead_only(self) -> bool:
        return source_policy(self.source_tier).lead_only

    @property
    def max_evidence_class(self) -> str:
        return source_policy(self.source_tier).max_evidence_class


def lead_can_enter_strong_review(
    lead: ChinaWebLead,
    *,
    identity_resolved: bool,
    time_validated: bool,
    corroborated_independently: bool,
) -> bool:
    policy = source_policy(lead.source_tier)
    if policy.lead_only:
        return False
    if not identity_resolved or not time_validated:
        return False
    if policy.max_evidence_class not in {"E2", "E3"}:
        return False
    return corroborated_independently


def track_a_web_eligible(lead: ChinaWebLead, cutoff: datetime) -> tuple[bool, str]:
    if lead.published_at is None:
        return False, "publication_time_unknown"
    if lead.published_at > cutoff:
        return False, "published_after_cutoff"
    return True, "published_on_or_before_cutoff"


def safe_public_summary(lead: ChinaWebLead) -> dict:
    """Return a public-facing lead description without implying wrongdoing."""
    return {
        "lead_id": lead.lead_id,
        "url": lead.url,
        "source_tier": lead.source_tier.value,
        "institution_type": lead.institution_type.value,
        "title": lead.title,
        "claim": lead.claim,
        "published_at": lead.published_at.isoformat() if lead.published_at else None,
        "source_name": lead.source_name,
        "stable_ids": list(lead.stable_ids),
        "corroboration_count": len(lead.corroborating_source_ids),
        "lead_only": lead.lead_only,
        "max_evidence_class": lead.max_evidence_class,
        "corruption_inference": False,
    }
