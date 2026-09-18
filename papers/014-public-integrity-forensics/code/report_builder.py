"""Standard OpenIntegrity report builder.

Converts one IntegrityCase plus detector findings into the portable report shape
defined by the Agent Skill JSON schemas.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Optional

from evidence_graph import build_evidence_graph
from open_integrity_agent import IntegrityCase, OpenIntegrityAgent


ALL_SOURCE_FAMILIES = {
    "procurement_award",
    "procurement_competition",
    "ownership",
    "public_office",
    "debarment",
    "sanctions",
    "declarations_interests",
    "donations_lobbying",
    "property_land",
    "audit_enforcement",
    "documents",
    "network_enrichment",
}


def build_report(
    case: IntegrityCase,
    *,
    mode: str = "ad_hoc",
    cutoff: Optional[date] = None,
    agent: Optional[OpenIntegrityAgent] = None,
) -> dict[str, Any]:
    if mode not in {"track_a", "track_b", "ad_hoc"}:
        raise ValueError("mode must be track_a, track_b, or ad_hoc")

    engine = agent or OpenIntegrityAgent()
    raw = engine.run(case)

    covered = sorted(case.source_coverage)
    missing = sorted(ALL_SOURCE_FAMILIES - set(case.source_coverage))

    time_eligible = True
    time_reason = "not_track_a"
    if mode == "track_a":
        if cutoff is None:
            time_eligible = False
            time_reason = "track_a_requires_cutoff"
        else:
            # Case-level conservative gate: every direct contract source with a
            # known publication date must be <= cutoff; an unknown publication
            # time is not silently replaced with retrieval time.
            dates = [x.published_at for x in case.contract.source_refs]
            if not dates or any(x is None for x in dates):
                time_eligible = False
                time_reason = "source_publication_time_incomplete"
            elif any(x > cutoff for x in dates if x is not None):
                time_eligible = False
                time_reason = "source_published_after_cutoff"
            else:
                time_reason = "contract_sources_public_by_cutoff"

    priority = raw["review_priority"]
    if mode == "track_a" and not time_eligible:
        priority = "BLOCKED"

    limitations = []
    if missing:
        limitations.append(
            "Not all source families were covered; missing families are not negative evidence."
        )
    if mode == "track_a" and not time_eligible:
        limitations.append(
            "Track A temporal eligibility failed; no historical-performance inference should be drawn."
        )
    if any(f["status"] == "ABSTAIN" for f in raw["findings"]):
        limitations.append(
            "At least one detector abstained because required data or assumptions were unavailable."
        )

    return {
        "report_version": "0.1.0",
        "subject_id": case.subject_id,
        "mode": mode,
        "time_safety": {
            "eligible": time_eligible,
            "reason": time_reason,
            "cutoff": cutoff.isoformat() if cutoff else None,
        },
        "source_coverage": {
            "covered": covered,
            "missing": missing,
        },
        "findings": raw["findings"],
        "evidence_graph": build_evidence_graph(case, raw["findings"]),
        "review_priority": priority,
        "corruption_inference": False,
        "interpretation": (
            "This report prioritizes public-record conditions for human review. "
            "It does not determine corruption, intent, criminal liability, or political worthiness."
        ),
        "limitations": limitations,
    }
