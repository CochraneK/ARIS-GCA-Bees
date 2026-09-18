"""OpenIntegrity core for ARIS4C014.

The module is intentionally network-free. Source adapters normalize records elsewhere;
this core enforces applicability, temporal checks, evidence semantics, dependency
groups, and non-accusatory outputs.

A FLAG means "review this reproducible condition", never "corruption occurred".
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from enum import Enum
from typing import Any, Iterable, Optional
from uuid import uuid4


class Status(str, Enum):
    FLAG = "FLAG"
    PASS = "PASS"
    ABSTAIN = "ABSTAIN"
    ERROR = "ERROR"


class EvidenceClass(str, Enum):
    E0 = "E0"  # direct metadata / process observation
    E1 = "E1"  # deterministic incompatibility or configured rule anomaly
    E2 = "E2"  # externally verifiable official/public-record fact
    E3 = "E3"  # high-specificity cross-source forensic match
    E4 = "E4"  # model/statistical anomaly
    E5 = "E5"  # weak/context-dependent heuristic


@dataclass(frozen=True)
class SourceRef:
    source_name: str
    record_id: str
    url: str = ""
    published_at: Optional[date] = None
    retrieved_at: Optional[date] = None


@dataclass(frozen=True)
class EntityRecord:
    entity_id: str
    name: str
    entity_type: str = "legal_entity"
    incorporated_on: Optional[date] = None
    stable_ids: tuple[str, ...] = ()
    public_office_from: Optional[date] = None
    public_office_to: Optional[date] = None
    source_refs: tuple[SourceRef, ...] = ()


@dataclass(frozen=True)
class ContractRecord:
    contract_id: str
    authority_id: str
    supplier_ids: tuple[str, ...]
    award_date: Optional[date] = None
    publication_date: Optional[date] = None
    award_value: Optional[float] = None
    legal_threshold: Optional[float] = None
    bid_count: Optional[int] = None
    procurement_method: Optional[str] = None
    jurisdiction: Optional[str] = None
    source_refs: tuple[SourceRef, ...] = ()


@dataclass(frozen=True)
class RelationRecord:
    left_id: str
    relation: str
    right_id: str
    source_ref: SourceRef
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    identity_strength: str = "stable_id"
    # stable_id | official_cross_id | multi_attribute | name_only


@dataclass(frozen=True)
class DebarmentRecord:
    entity_id: str
    imposed_from: date
    imposed_to: Optional[date]
    source_ref: SourceRef

    def in_force(self, when: date) -> bool:
        if when < self.imposed_from:
            return False
        return self.imposed_to is None or when <= self.imposed_to


@dataclass
class IntegrityCase:
    subject_id: str
    contract: ContractRecord
    entities: dict[str, EntityRecord] = field(default_factory=dict)
    relations: list[RelationRecord] = field(default_factory=list)
    debarments: list[DebarmentRecord] = field(default_factory=list)
    source_coverage: set[str] = field(default_factory=set)
    # Examples: procurement_award, procurement_competition, ownership,
    # public_office, debarment. Absence of a source family is not negative evidence.


@dataclass
class Finding:
    subject_id: str
    detector_id: str
    detector_version: str
    family: str
    applicable: bool
    applicability_reason: str
    status: Status
    evidence_class: EvidenceClass
    claim: str
    evidence: dict[str, Any] = field(default_factory=dict)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    dependency_group: str = ""
    observed_at: Optional[str] = None
    reproducible: str = "yes"
    confidence: Optional[float] = None
    calibration_reference: Optional[str] = None
    benign_explanations: list[str] = field(default_factory=list)
    corruption_inference: bool = False
    finding_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        # Hard invariant inherited from ARIS4C011.
        self.corruption_inference = False

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["status"] = self.status.value
        out["evidence_class"] = self.evidence_class.value
        return out


def _source_dicts(refs: Iterable[SourceRef]) -> list[dict[str, Any]]:
    return [
        {
            "source_name": r.source_name,
            "record_id": r.record_id,
            "url": r.url,
            "published_at": r.published_at.isoformat() if r.published_at else None,
            "retrieved_at": r.retrieved_at.isoformat() if r.retrieved_at else None,
        }
        for r in refs
    ]


def _active_on(start: Optional[date], end: Optional[date], when: date) -> bool:
    if start and when < start:
        return False
    if end and when > end:
        return False
    return True


class Detector:
    detector_id = "base"
    detector_version = "0.1.0"
    family = "base"

    def run(self, case: IntegrityCase) -> Finding:
        raise NotImplementedError

    def _finding(
        self,
        case: IntegrityCase,
        *,
        applicable: bool,
        reason: str,
        status: Status,
        evidence_class: EvidenceClass,
        claim: str,
        evidence: Optional[dict[str, Any]] = None,
        sources: Iterable[SourceRef] = (),
        dependency_group: str,
        benign: Optional[list[str]] = None,
    ) -> Finding:
        return Finding(
            subject_id=case.subject_id,
            detector_id=self.detector_id,
            detector_version=self.detector_version,
            family=self.family,
            applicable=applicable,
            applicability_reason=reason,
            status=status,
            evidence_class=evidence_class,
            claim=claim,
            evidence=evidence or {},
            source_refs=_source_dicts(sources),
            dependency_group=dependency_group,
            benign_explanations=benign or [],
        )


class SingleBidderDetector(Detector):
    detector_id = "single_bidder"
    family = "procurement_process"

    def run(self, case: IntegrityCase) -> Finding:
        c = case.contract
        if c.bid_count is None:
            return self._finding(
                case,
                applicable=False,
                reason="bid_count is not available",
                status=Status.ABSTAIN,
                evidence_class=EvidenceClass.E0,
                claim="Bidder-count check could not be applied.",
                sources=c.source_refs,
                dependency_group=f"bid_count:{c.contract_id}",
            )
        flagged = c.bid_count == 1
        return self._finding(
            case,
            applicable=True,
            reason="bid_count is available",
            status=Status.FLAG if flagged else Status.PASS,
            evidence_class=EvidenceClass.E0,
            claim=(
                "The public record reports one bidder."
                if flagged
                else "The public record does not report a single-bidder procedure."
            ),
            evidence={"bid_count": c.bid_count},
            sources=c.source_refs,
            dependency_group=f"bid_count:{c.contract_id}",
            benign=[
                "The market may have only one qualified supplier.",
                "Emergency or specialized procurement may legitimately limit competition.",
            ] if flagged else [],
        )


class NearThresholdDetector(Detector):
    detector_id = "near_threshold"
    family = "value_threshold"

    def __init__(self, margin_fraction: float = 0.02) -> None:
        if not 0 < margin_fraction < 1:
            raise ValueError("margin_fraction must be between 0 and 1")
        self.margin_fraction = margin_fraction

    def run(self, case: IntegrityCase) -> Finding:
        c = case.contract
        if c.award_value is None or c.legal_threshold is None:
            return self._finding(
                case,
                applicable=False,
                reason="award_value and configured legal_threshold are both required",
                status=Status.ABSTAIN,
                evidence_class=EvidenceClass.E0,
                claim="Near-threshold check could not be applied.",
                sources=c.source_refs,
                dependency_group=f"threshold:{c.contract_id}",
            )
        if c.legal_threshold <= 0:
            return self._finding(
                case,
                applicable=False,
                reason="legal_threshold must be positive",
                status=Status.ERROR,
                evidence_class=EvidenceClass.E0,
                claim="Near-threshold configuration is invalid.",
                sources=c.source_refs,
                dependency_group=f"threshold:{c.contract_id}",
            )
        lower = c.legal_threshold * (1 - self.margin_fraction)
        flagged = lower <= c.award_value < c.legal_threshold
        return self._finding(
            case,
            applicable=True,
            reason="award value and jurisdiction-specific threshold are configured",
            status=Status.FLAG if flagged else Status.PASS,
            evidence_class=EvidenceClass.E0,
            claim=(
                "Award value falls just below the configured threshold."
                if flagged
                else "Award value is not within the configured near-threshold band."
            ),
            evidence={
                "award_value": c.award_value,
                "legal_threshold": c.legal_threshold,
                "margin_fraction": self.margin_fraction,
                "lower_bound": lower,
            },
            sources=c.source_refs,
            dependency_group=f"threshold:{c.contract_id}",
            benign=[
                "Legitimate pricing can naturally fall near a threshold.",
                "The configured threshold may not govern this procurement type.",
            ] if flagged else [],
        )


class NewlyIncorporatedSupplierDetector(Detector):
    detector_id = "new_supplier_before_award"
    family = "temporal_forensics"

    def __init__(self, days: int = 90) -> None:
        self.days = days

    def run(self, case: IntegrityCase) -> Finding:
        c = case.contract
        if c.award_date is None:
            return self._finding(
                case,
                applicable=False,
                reason="award_date is missing",
                status=Status.ABSTAIN,
                evidence_class=EvidenceClass.E0,
                claim="Supplier-age check could not be applied.",
                dependency_group=f"supplier_age:{c.contract_id}",
            )

        suppliers = [case.entities.get(x) for x in c.supplier_ids]
        suppliers = [x for x in suppliers if x is not None]
        dated = [x for x in suppliers if x.incorporated_on is not None]
        if not dated:
            return self._finding(
                case,
                applicable=False,
                reason="no supplier incorporation date is available",
                status=Status.ABSTAIN,
                evidence_class=EvidenceClass.E0,
                claim="Supplier-age check could not be applied.",
                sources=c.source_refs,
                dependency_group=f"supplier_age:{c.contract_id}",
            )

        hits: list[dict[str, Any]] = []
        for entity in dated:
            age = (c.award_date - entity.incorporated_on).days
            if 0 <= age <= self.days:
                hits.append(
                    {
                        "entity_id": entity.entity_id,
                        "incorporated_on": entity.incorporated_on.isoformat(),
                        "days_before_award": age,
                    }
                )

        refs = list(c.source_refs)
        for entity in dated:
            refs.extend(entity.source_refs)

        return self._finding(
            case,
            applicable=True,
            reason="award date and at least one supplier incorporation date are available",
            status=Status.FLAG if hits else Status.PASS,
            evidence_class=EvidenceClass.E0,
            claim=(
                f"{len(hits)} supplier(s) were incorporated within {self.days} days before award."
                if hits
                else f"No supplier was incorporated within {self.days} days before award."
            ),
            evidence={"matches": hits, "window_days": self.days},
            sources=refs,
            dependency_group=f"supplier_age:{c.contract_id}",
            benign=[
                "A new company can legitimately win a contract.",
                "A reorganization or special-purpose vehicle may explain recent incorporation.",
            ] if hits else [],
        )


class InForceDebarmentDetector(Detector):
    detector_id = "in_force_debarment"
    family = "sanctions_debarment"

    def run(self, case: IntegrityCase) -> Finding:
        c = case.contract
        if c.award_date is None:
            return self._finding(
                case,
                applicable=False,
                reason="award_date is missing",
                status=Status.ABSTAIN,
                evidence_class=EvidenceClass.E2,
                claim="Debarment timing check could not be applied.",
                dependency_group=f"debarment:{c.contract_id}",
            )

        relevant = [d for d in case.debarments if d.entity_id in set(c.supplier_ids)]
        coverage_present = "debarment" in case.source_coverage or bool(case.debarments)
        if not relevant and not coverage_present:
            return self._finding(
                case,
                applicable=False,
                reason="no debarment source coverage was supplied",
                status=Status.ABSTAIN,
                evidence_class=EvidenceClass.E2,
                claim="Debarment check was not performed because source coverage is absent.",
                sources=c.source_refs,
                dependency_group=f"debarment:{c.contract_id}",
            )
        if not relevant:
            return self._finding(
                case,
                applicable=True,
                reason="debarment source coverage is present and no supplier match was found",
                status=Status.PASS,
                evidence_class=EvidenceClass.E2,
                claim="No covered debarment record matched a supplier stable identity.",
                sources=c.source_refs,
                dependency_group=f"debarment:{c.contract_id}",
            )

        active = [d for d in relevant if d.in_force(c.award_date)]
        return self._finding(
            case,
            applicable=True,
            reason="supplier identity and award date are available",
            status=Status.FLAG if active else Status.PASS,
            evidence_class=EvidenceClass.E2,
            claim=(
                "A matched supplier had a supplied debarment record in force on the award date."
                if active
                else "Supplied debarment records were not in force on the award date."
            ),
            evidence={
                "award_date": c.award_date.isoformat(),
                "active_records": [
                    {
                        "entity_id": d.entity_id,
                        "imposed_from": d.imposed_from.isoformat(),
                        "imposed_to": d.imposed_to.isoformat() if d.imposed_to else None,
                    }
                    for d in active
                ],
            },
            sources=[d.source_ref for d in relevant],
            dependency_group=f"debarment:{c.contract_id}",
            benign=[
                "The legal scope of a debarment may not apply to every awarding authority.",
                "The source record should be checked for affiliates, successors, and jurisdictional scope.",
            ] if active else [],
        )


class PublicOfficeOwnershipLinkDetector(Detector):
    detector_id = "public_office_ownership_link"
    family = "conflict_of_interest"

    OWNER_RELATIONS = {"OWNS", "CONTROLS", "BENEFICIAL_OWNER_OF"}

    def run(self, case: IntegrityCase) -> Finding:
        c = case.contract
        if c.award_date is None:
            return self._finding(
                case,
                applicable=False,
                reason="award_date is required for temporal overlap",
                status=Status.ABSTAIN,
                evidence_class=EvidenceClass.E2,
                claim="Public-office ownership-link check could not be applied.",
                dependency_group=f"office_owner:{c.contract_id}",
            )

        supplier_set = set(c.supplier_ids)
        candidates: list[RelationRecord] = []
        weak_identity = False

        for rel in case.relations:
            if rel.relation not in self.OWNER_RELATIONS or rel.right_id not in supplier_set:
                continue
            person = case.entities.get(rel.left_id)
            if person is None or person.entity_type != "person":
                continue
            if not _active_on(rel.valid_from, rel.valid_to, c.award_date):
                continue
            if not _active_on(person.public_office_from, person.public_office_to, c.award_date):
                continue
            if rel.identity_strength == "name_only":
                weak_identity = True
                continue
            candidates.append(rel)

        if not candidates and weak_identity:
            return self._finding(
                case,
                applicable=False,
                reason="only name-only identity matches connect an office-holder to a supplier",
                status=Status.ABSTAIN,
                evidence_class=EvidenceClass.E5,
                claim="A possible name-only ownership/office link requires identity verification.",
                dependency_group=f"office_owner:{c.contract_id}",
                benign=["Different people can share the same or similar names."],
            )

        if not candidates:
            covered = {"ownership", "public_office"}.issubset(case.source_coverage)
            if not covered:
                return self._finding(
                    case,
                    applicable=False,
                    reason="ownership and public-office source coverage are both required",
                    status=Status.ABSTAIN,
                    evidence_class=EvidenceClass.E2,
                    claim="Public-office ownership-link check could not establish a negative result because source coverage is incomplete.",
                    dependency_group=f"office_owner:{c.contract_id}",
                )
            return self._finding(
                case,
                applicable=True,
                reason="ownership and public-office source coverage are present and relevant relationships were checked",
                status=Status.PASS,
                evidence_class=EvidenceClass.E2,
                claim="No identity-resolved public-office ownership link was found in covered relations.",
                dependency_group=f"office_owner:{c.contract_id}",
            )

        return self._finding(
            case,
            applicable=True,
            reason="identity-resolved ownership/control and public-office intervals overlap the award date",
            status=Status.FLAG,
            evidence_class=EvidenceClass.E2,
            claim="A public record relationship links an office-holder to a supplier during the award period.",
            evidence={
                "links": [
                    {
                        "person_id": r.left_id,
                        "relation": r.relation,
                        "supplier_id": r.right_id,
                        "identity_strength": r.identity_strength,
                    }
                    for r in candidates
                ]
            },
            sources=[r.source_ref for r in candidates],
            dependency_group=f"office_owner:{c.contract_id}",
            benign=[
                "The relationship may be lawful, disclosed, recused, or irrelevant to the decision.",
                "The office-holder may have had no role in the procurement.",
            ],
        )


DEFAULT_DETECTORS: tuple[Detector, ...] = (
    SingleBidderDetector(),
    NearThresholdDetector(),
    NewlyIncorporatedSupplierDetector(),
    InForceDebarmentDetector(),
    PublicOfficeOwnershipLinkDetector(),
)


def review_priority(findings: Iterable[Finding]) -> str:
    """Return review priority, never a corruption probability."""
    flags = [f for f in findings if f.status == Status.FLAG]
    if not flags:
        if any(f.status in {Status.ABSTAIN, Status.ERROR} for f in findings):
            return "ABSTAIN_OR_INCOMPLETE"
        return "NO_FLAG"

    non_e5 = [f for f in flags if f.evidence_class != EvidenceClass.E5]
    if not non_e5:
        return "VERY_LOW"

    independent_groups = {f.dependency_group for f in non_e5}
    families = {f.family for f in non_e5}
    strong = [f for f in non_e5 if f.evidence_class in {EvidenceClass.E2, EvidenceClass.E3}]

    if len(independent_groups) >= 2 and len(families) >= 2 and strong:
        return "HIGH"
    if strong or len(independent_groups) >= 2:
        return "MODERATE"
    return "LOW"


class OpenIntegrityAgent:
    def __init__(self, detectors: Iterable[Detector] = DEFAULT_DETECTORS) -> None:
        self.detectors = tuple(detectors)

    def run(self, case: IntegrityCase) -> dict[str, Any]:
        findings: list[Finding] = []
        for detector in self.detectors:
            try:
                findings.append(detector.run(case))
            except Exception as exc:  # defensive boundary: one module must not kill the run
                findings.append(
                    Finding(
                        subject_id=case.subject_id,
                        detector_id=getattr(detector, "detector_id", detector.__class__.__name__),
                        detector_version=getattr(detector, "detector_version", "unknown"),
                        family=getattr(detector, "family", "unknown"),
                        applicable=True,
                        applicability_reason="detector raised an exception",
                        status=Status.ERROR,
                        evidence_class=EvidenceClass.E0,
                        claim="Detector execution failed.",
                        evidence={"error_type": type(exc).__name__, "error": str(exc)},
                        dependency_group=f"error:{getattr(detector, 'detector_id', 'unknown')}",
                        reproducible="unknown",
                    )
                )

        return {
            "subject_id": case.subject_id,
            "review_priority": review_priority(findings),
            "corruption_inference": False,
            "findings": [f.to_dict() for f in findings],
        }
