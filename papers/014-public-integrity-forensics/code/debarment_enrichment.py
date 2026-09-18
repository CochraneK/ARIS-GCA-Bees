"""External debarment/sanctions enrichment primitives for OpenIntegrity.

This module separates source normalization from identity linkage. A row from an
official debarment list is first represented as an external entity with a dated
ineligibility interval. It can only be attached to a procurement supplier after
an exact stable-id match or an explicit high-quality MatchDecision.

Name similarity alone is never enough.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from entity_resolution import IdentityProfile, MatchDecision
from open_integrity_agent import DebarmentRecord, IntegrityCase, SourceRef


@dataclass(frozen=True)
class ExternalDebarment:
    external_id: str
    name: str
    country: Optional[str]
    address: Optional[str]
    imposed_from: date
    imposed_to: Optional[date]
    source_ref: SourceRef
    grounds: Optional[str] = None
    stable_ids: tuple[str, ...] = ()

    def identity_profile(self) -> IdentityProfile:
        return IdentityProfile(
            label=self.name,
            stable_ids=self.stable_ids,
            address=self.address,
            jurisdiction=self.country,
        )


def normalize_external_debarment(
    row: dict,
    *,
    source_name: str,
    source_url: str,
    record_id_field: str = "record_id",
    name_field: str = "name",
    country_field: str = "country",
    address_field: str = "address",
    from_field: str = "imposed_from",
    to_field: str = "imposed_to",
    grounds_field: str = "grounds",
) -> ExternalDebarment:
    """Normalize an already retrieved official/approved debarment row.

    Dates must be ISO YYYY-MM-DD. Ambiguous human-readable date parsing belongs
    in a source-specific adapter so it can be audited independently.
    """
    record_id = str(row.get(record_id_field) or "").strip()
    name = str(row.get(name_field) or "").strip()
    start = str(row.get(from_field) or "").strip()
    end = str(row.get(to_field) or "").strip()

    if not record_id:
        raise ValueError("debarment row requires a source record ID")
    if not name:
        raise ValueError("debarment row requires an entity name")
    if not start:
        raise ValueError("debarment row requires imposed_from")

    imposed_from = date.fromisoformat(start)
    imposed_to = date.fromisoformat(end) if end else None
    if imposed_to is not None and imposed_to < imposed_from:
        raise ValueError("imposed_to precedes imposed_from")

    source_ref = SourceRef(
        source_name=source_name,
        record_id=record_id,
        url=source_url,
    )
    stable_ids = tuple(
        str(x).strip()
        for x in (row.get("stable_ids") or [])
        if str(x).strip()
    )
    return ExternalDebarment(
        external_id=f"{source_name}:{record_id}",
        name=name,
        country=(str(row.get(country_field)).strip() if row.get(country_field) else None),
        address=(str(row.get(address_field)).strip() if row.get(address_field) else None),
        imposed_from=imposed_from,
        imposed_to=imposed_to,
        source_ref=source_ref,
        grounds=(str(row.get(grounds_field)).strip() if row.get(grounds_field) else None),
        stable_ids=stable_ids,
    )


def attach_debarment_to_supplier(
    case: IntegrityCase,
    external: ExternalDebarment,
    *,
    supplier_id: str,
    match_decision: Optional[MatchDecision] = None,
    source_scan_complete: bool = False,
) -> IntegrityCase:
    """Attach a dated debarment to one supplier after explicit identity proof."""
    if supplier_id not in set(case.contract.supplier_ids):
        raise ValueError("target entity is not a supplier in this procurement case")

    supplier = case.entities.get(supplier_id)
    supplier_stable = set(supplier.stable_ids if supplier else ())
    external_stable = set(external.stable_ids)
    exact = bool(supplier_stable & external_stable) or supplier_id in external_stable

    if not exact:
        if match_decision is None or not match_decision.usable_for_high_priority:
            raise ValueError(
                "non-exact debarment join requires a high-quality explicit MatchDecision"
            )

    case.debarments.append(
        DebarmentRecord(
            entity_id=supplier_id,
            imposed_from=external.imposed_from,
            imposed_to=external.imposed_to,
            source_ref=external.source_ref,
        )
    )
    if source_scan_complete:
        case.source_coverage.add("debarment")
    return case


def mark_debarment_scan_complete(case: IntegrityCase) -> IntegrityCase:
    """Mark negative coverage only after the caller completed the defined scan."""
    case.source_coverage.add("debarment")
    return case
