"""Cross-source enrichment helpers for OpenIntegrity.

These helpers make joins explicit. Exact stable identifiers may merge directly.
Otherwise the caller must provide a conservative MatchDecision that is usable
for high-priority evidence; names are never silently joined.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from typing import Optional

from entity_resolution import MatchDecision
from open_integrity_agent import (
    EntityRecord,
    IntegrityCase,
    SourceRef,
)
from source_adapters import CompaniesHouseImportResult


def _merge_entity(base: EntityRecord, enriched: EntityRecord) -> EntityRecord:
    return EntityRecord(
        entity_id=base.entity_id,
        name=enriched.name or base.name,
        entity_type=enriched.entity_type or base.entity_type,
        incorporated_on=enriched.incorporated_on or base.incorporated_on,
        stable_ids=tuple(dict.fromkeys((*base.stable_ids, *enriched.stable_ids))),
        public_office_from=base.public_office_from or enriched.public_office_from,
        public_office_to=base.public_office_to or enriched.public_office_to,
        source_refs=tuple(dict.fromkeys((*base.source_refs, *enriched.source_refs))),
    )


def attach_companies_house(
    case: IntegrityCase,
    imported: CompaniesHouseImportResult,
    *,
    supplier_id: Optional[str] = None,
    match_decision: Optional[MatchDecision] = None,
) -> IntegrityCase:
    """Attach Companies House profile/PSC data to a procurement case.

    Direct merge is allowed when the supplier ID equals the Companies House
    stable ID. Otherwise an explicit high-quality match decision is required.
    The input case is mutated and returned for pipeline convenience.
    """
    company_id = imported.company.entity_id
    supplier_set = set(case.contract.supplier_ids)

    target = supplier_id or (company_id if company_id in supplier_set else None)
    if target is None or target not in supplier_set:
        raise ValueError("Companies House company is not an identified supplier in this case")

    exact = target == company_id or company_id in set(case.entities.get(target, imported.company).stable_ids)
    if not exact:
        if match_decision is None or not match_decision.usable_for_high_priority:
            raise ValueError("non-exact company join requires a high-quality explicit MatchDecision")

    existing = case.entities.get(target)
    if existing:
        case.entities[target] = _merge_entity(existing, replace(imported.company, entity_id=target))
    else:
        case.entities[target] = replace(imported.company, entity_id=target)

    # If company_id differs from target, rewrite only the company-side endpoint
    # after an explicit verified match. Person IDs remain source-scoped.
    for owner_id, owner in imported.owner_entities.items():
        case.entities[owner_id] = owner
    for rel in imported.relations:
        if rel.right_id == company_id and target != company_id:
            rel = replace(rel, right_id=target)
        case.relations.append(rel)

    case.source_coverage.add("ownership")
    return case


@dataclass(frozen=True)
class PublicOfficeObservation:
    person_id: str
    title: str
    valid_from: Optional[date]
    valid_to: Optional[date]
    source_ref: SourceRef


def attach_public_office(
    case: IntegrityCase,
    observation: PublicOfficeObservation,
    *,
    source_person_id: Optional[str] = None,
    match_decision: Optional[MatchDecision] = None,
) -> IntegrityCase:
    """Attach a public-office interval to an already resolved person entity.

    If source_person_id differs from the canonical person ID, an explicit
    high-quality entity-resolution decision is mandatory.
    """
    target = observation.person_id
    if target not in case.entities:
        raise ValueError("public-office target person is not present in the case")

    if source_person_id and source_person_id != target:
        if match_decision is None or not match_decision.usable_for_high_priority:
            raise ValueError("cross-source person join requires a high-quality MatchDecision")

    person = case.entities[target]
    if person.entity_type != "person":
        raise ValueError("public-office observation must attach to a person entity")

    refs = tuple(dict.fromkeys((*person.source_refs, observation.source_ref)))
    case.entities[target] = replace(
        person,
        public_office_from=observation.valid_from,
        public_office_to=observation.valid_to,
        source_refs=refs,
    )
    case.source_coverage.add("public_office")
    return case
