"""Conservative, auditable entity resolution for OpenIntegrity.

This is intentionally a rule-based baseline. It exposes *why* a match is made,
keeps contradictory attributes visible, and refuses to promote name-only
similarity to a usable identity link.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
import unicodedata
from typing import Optional


def _norm_text(value: Optional[str]) -> str:
    if not value:
        return ""
    text = unicodedata.normalize("NFKD", value)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    return re.sub(r"\s+", " ", text)


@dataclass(frozen=True)
class IdentityProfile:
    label: str
    stable_ids: tuple[str, ...] = ()
    registration_number: Optional[str] = None
    birth_year: Optional[int] = None
    birth_month: Optional[int] = None
    address: Optional[str] = None
    jurisdiction: Optional[str] = None


@dataclass
class MatchDecision:
    status: str  # MATCH | POSSIBLE | ABSTAIN | CONFLICT
    score: float
    strength: str  # stable_id | official_cross_id | multi_attribute | name_only | conflict
    reasons: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    human_check_required: bool = True

    @property
    def usable_for_high_priority(self) -> bool:
        return self.status == "MATCH" and self.strength in {
            "stable_id",
            "official_cross_id",
            "multi_attribute",
        } and self.score >= 0.85


def resolve_identity(left: IdentityProfile, right: IdentityProfile) -> MatchDecision:
    left_ids = {x.strip() for x in left.stable_ids if x and x.strip()}
    right_ids = {x.strip() for x in right.stable_ids if x and x.strip()}
    shared_ids = left_ids & right_ids
    if shared_ids:
        return MatchDecision(
            status="MATCH",
            score=1.0,
            strength="stable_id",
            reasons=[f"shared stable identifier: {sorted(shared_ids)[0]}"],
            human_check_required=False,
        )

    conflicts: list[str] = []
    if (
        left.registration_number
        and right.registration_number
        and left.registration_number != right.registration_number
    ):
        conflicts.append("registration_number_conflict")
    if (
        left.birth_year
        and right.birth_year
        and left.birth_year != right.birth_year
    ):
        conflicts.append("birth_year_conflict")
    if (
        left.birth_month
        and right.birth_month
        and left.birth_month != right.birth_month
    ):
        conflicts.append("birth_month_conflict")

    if conflicts:
        return MatchDecision(
            status="CONFLICT",
            score=0.0,
            strength="conflict",
            conflicts=conflicts,
            reasons=["one or more strong attributes contradict"],
            human_check_required=True,
        )

    name_same = _norm_text(left.label) == _norm_text(right.label) and bool(_norm_text(left.label))
    reg_same = bool(
        left.registration_number
        and right.registration_number
        and left.registration_number == right.registration_number
    )
    address_same = bool(
        _norm_text(left.address)
        and _norm_text(left.address) == _norm_text(right.address)
    )
    jurisdiction_same = bool(
        left.jurisdiction
        and right.jurisdiction
        and _norm_text(left.jurisdiction) == _norm_text(right.jurisdiction)
    )
    birth_same = bool(
        left.birth_year
        and right.birth_year
        and left.birth_year == right.birth_year
        and (
            left.birth_month is None
            or right.birth_month is None
            or left.birth_month == right.birth_month
        )
    )

    if reg_same:
        return MatchDecision(
            status="MATCH",
            score=0.98,
            strength="official_cross_id",
            reasons=["same registration number"],
            human_check_required=False,
        )

    evidence = []
    if name_same:
        evidence.append("normalized_name")
    if address_same:
        evidence.append("address")
    if jurisdiction_same:
        evidence.append("jurisdiction")
    if birth_same:
        evidence.append("partial_birth_date")

    # Natural-person matching is deliberately conservative. Name plus at least
    # two independent contextual attributes is required for an automatic link.
    corroborators = len([x for x in (address_same, jurisdiction_same, birth_same) if x])
    if name_same and corroborators >= 2:
        return MatchDecision(
            status="MATCH",
            score=0.90,
            strength="multi_attribute",
            reasons=evidence,
            human_check_required=True,
        )
    if name_same and corroborators == 1:
        return MatchDecision(
            status="POSSIBLE",
            score=0.70,
            strength="multi_attribute",
            reasons=evidence,
            human_check_required=True,
        )
    if name_same:
        return MatchDecision(
            status="ABSTAIN",
            score=0.40,
            strength="name_only",
            reasons=["name-only similarity is insufficient"],
            human_check_required=True,
        )

    return MatchDecision(
        status="ABSTAIN",
        score=0.0,
        strength="name_only",
        reasons=["no sufficient identity evidence"],
        human_check_required=True,
    )
