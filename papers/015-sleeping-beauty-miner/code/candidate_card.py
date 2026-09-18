"""Candidate Evidence Card construction for ARIS4C015."""

from __future__ import annotations

from typing import Any, Iterable

from integrity_adapter import IntegrityGate


DISCLAIMER = (
    "This is a discovery-priority estimate, not a validity or breakthrough judgment."
)


def evidence_item(
    *,
    name: str,
    applicable: bool,
    cutoff_safe: bool,
    status: str,
    value: Any = None,
    provenance: Iterable[str] = (),
    uncertainty: Any = None,
    notes: str | None = None,
) -> dict[str, Any]:
    allowed = {"SUPPORTIVE", "CONTRADICTORY", "NEUTRAL", "ABSTAIN", "QUARANTINED"}
    if status not in allowed:
        raise ValueError(f"Unknown evidence status: {status}")
    if not applicable and status not in {"ABSTAIN", "QUARANTINED"}:
        raise ValueError("Inapplicable evidence must abstain or be quarantined")
    return {
        "name": name,
        "applicable": bool(applicable),
        "cutoff_safe": bool(cutoff_safe),
        "status": status,
        "value": value,
        "uncertainty": uncertainty,
        "provenance": list(provenance),
        "notes": notes,
    }


def build_candidate_card(
    *,
    paper_id: str,
    mode: str,
    analysis_cutoff: str | int,
    state: str,
    evidence_families: Iterable[dict[str, Any]],
    integrity_gate: IntegrityGate,
    provenance: Iterable[str],
    identifiers: dict[str, str | None] | None = None,
    citation_trajectory: dict[str, Any] | None = None,
    retrospective_metrics: dict[str, Any] | None = None,
    prince_candidates: Iterable[Any] = (),
    rank: int | None = None,
    score: float | None = None,
    score_semantics: str | None = None,
    explanation: str | None = None,
    model_version: str | None = None,
) -> dict[str, Any]:
    if mode not in {"RETROSPECTIVE", "PROSPECTIVE", "DISCOVERY_SCAN"}:
        raise ValueError("Unsupported mode")
    allowed_states = {
        "CONFIRMED_DELAYED_RECOGNITION",
        "AWAKENING_NOW",
        "DORMANT_CANDIDATE",
        "INTEGRITY_QUARANTINED",
        "INSUFFICIENT_DATA",
    }
    if state not in allowed_states:
        raise ValueError("Unsupported candidate state")

    evidence = list(evidence_families)
    missing = [
        item["name"]
        for item in evidence
        if item.get("status") == "ABSTAIN"
    ]
    contradictory = [
        item
        for item in evidence
        if item.get("status") == "CONTRADICTORY"
    ]

    if integrity_gate.state == "QUARANTINE":
        state = "INTEGRITY_QUARANTINED"

    return {
        "paper_id": paper_id,
        "identifiers": identifiers or {},
        "mode": mode,
        "analysis_cutoff": analysis_cutoff,
        "state": state,
        "rank": rank,
        "score": score,
        "score_semantics": score_semantics,
        "citation_trajectory": citation_trajectory or {},
        "retrospective_metrics": retrospective_metrics or {},
        "evidence_families": evidence,
        "prince_candidates": list(prince_candidates),
        "integrity_gate": integrity_gate.as_dict(),
        "missing_evidence": missing,
        "contradictory_evidence": contradictory,
        "explanation": explanation,
        "model_version": model_version,
        "provenance": list(provenance),
        "disclaimer": DISCLAIMER,
    }
