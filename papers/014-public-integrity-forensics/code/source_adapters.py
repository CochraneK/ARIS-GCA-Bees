"""Deterministic source adapters for OpenIntegrity.

Adapters convert public records into the small canonical objects used by the
network-free core. They do not decide whether a record is suspicious.

Supported in this module:
- OCDS 1.1.x release objects
- UK Companies House company profile + PSC response fragments

Network retrieval is deliberately outside this file so fixtures can be tested
without credentials or internet access.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime
from typing import Any, Iterable, Optional

from open_integrity_agent import (
    ContractRecord,
    EntityRecord,
    IntegrityCase,
    RelationRecord,
    SourceRef,
)


def _date(value: Any) -> Optional[date]:
    if not value or not isinstance(value, str):
        return None
    raw = value.strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(raw[:10])
        except ValueError:
            return None


def _amount(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", "").strip())
        except ValueError:
            return None
    return None


def _stable_party_id(party: dict[str, Any]) -> str:
    ident = party.get("identifier") or {}
    scheme = ident.get("scheme")
    value = ident.get("id")
    if scheme and value:
        return f"{scheme}:{value}"
    # OCDS party.id is only local to the release/process, but preserving it is
    # still preferable to a name-generated identifier.
    return str(party.get("id") or "").strip()


def _party_record(
    party: dict[str, Any],
    *,
    source_ref: SourceRef,
    prefix: str,
) -> Optional[EntityRecord]:
    local_id = str(party.get("id") or "").strip()
    stable = _stable_party_id(party)
    if not local_id and not stable:
        return None
    identifier = party.get("identifier") or {}
    legal_name = identifier.get("legalName")
    name = str(legal_name or party.get("name") or local_id or stable)
    entity_id = stable or f"{prefix}:{local_id}"
    stable_ids: tuple[str, ...] = (stable,) if ":" in stable else ()
    return EntityRecord(
        entity_id=entity_id,
        name=name,
        entity_type="legal_entity",
        stable_ids=stable_ids,
        source_refs=(source_ref,),
    )


@dataclass
class OCDSImportResult:
    cases: list[IntegrityCase] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ocid: str = ""
    release_id: str = ""


def normalize_ocds_release(
    release: dict[str, Any],
    *,
    source_name: str = "OCDS",
    source_url: str = "",
    jurisdiction: Optional[str] = None,
    retrieved_at: Optional[date] = None,
) -> OCDSImportResult:
    """Normalize an OCDS 1.1.x release into one IntegrityCase per award.

    Award IDs are scoped by the OCID. Suppliers are resolved through party.id,
    then replaced with organization identifiers when available.

    The adapter intentionally does not invent legal thresholds or infer bidder
    counts from document counts.
    """
    ocid = str(release.get("ocid") or "").strip()
    release_id = str(release.get("id") or "").strip()
    warnings: list[str] = []
    if not ocid:
        warnings.append("missing_ocid")
    if not release_id:
        warnings.append("missing_release_id")

    published_at = _date(release.get("date"))
    src = SourceRef(
        source_name=source_name,
        record_id=release_id or ocid or "unknown",
        url=source_url,
        published_at=published_at,
        retrieved_at=retrieved_at,
    )

    parties = release.get("parties") or []
    party_by_local: dict[str, EntityRecord] = {}
    entities: dict[str, EntityRecord] = {}
    for raw in parties:
        if not isinstance(raw, dict):
            continue
        ent = _party_record(raw, source_ref=src, prefix=ocid or release_id or "ocds")
        if ent is None:
            continue
        local = str(raw.get("id") or "").strip()
        if local:
            party_by_local[local] = ent
        entities[ent.entity_id] = ent

    tender = release.get("tender") or {}
    buyer = release.get("buyer") or {}
    procuring = tender.get("procuringEntity") or {}
    authority_local = str(buyer.get("id") or procuring.get("id") or "").strip()
    authority_ent = party_by_local.get(authority_local)
    authority_id = (
        authority_ent.entity_id
        if authority_ent
        else authority_local or f"unknown-authority:{ocid or release_id or 'record'}"
    )

    bid_count = tender.get("numberOfTenderers")
    if isinstance(bid_count, bool) or not isinstance(bid_count, int):
        bid_count = None

    method = tender.get("procurementMethod")
    if method is not None:
        method = str(method)

    awards = release.get("awards") or []
    cases: list[IntegrityCase] = []
    for raw_award in awards:
        if not isinstance(raw_award, dict):
            continue
        award_id = str(raw_award.get("id") or "").strip()
        if not award_id:
            warnings.append("award_without_id")
            continue

        supplier_ids: list[str] = []
        for ref in raw_award.get("suppliers") or []:
            if not isinstance(ref, dict):
                continue
            local = str(ref.get("id") or "").strip()
            ent = party_by_local.get(local)
            supplier_id = ent.entity_id if ent else local
            if supplier_id:
                supplier_ids.append(supplier_id)

        if not supplier_ids:
            warnings.append(f"award_without_supplier:{award_id}")

        value = raw_award.get("value") or {}
        award_value = _amount(value.get("amount"))
        award_date = _date(raw_award.get("date"))

        contract_id = f"{ocid}:{award_id}" if ocid else award_id
        contract = ContractRecord(
            contract_id=contract_id,
            authority_id=authority_id,
            supplier_ids=tuple(dict.fromkeys(supplier_ids)),
            award_date=award_date,
            publication_date=published_at,
            award_value=award_value,
            legal_threshold=None,
            bid_count=bid_count,
            procurement_method=method,
            jurisdiction=jurisdiction,
            source_refs=(src,),
        )
        cases.append(
            IntegrityCase(
                subject_id=contract_id,
                contract=contract,
                entities=dict(entities),
                source_coverage={
                    "procurement_award",
                    *(["procurement_competition"] if "numberOfTenderers" in tender else []),
                },
            )
        )

    return OCDSImportResult(
        cases=cases,
        warnings=warnings,
        ocid=ocid,
        release_id=release_id,
    )


@dataclass
class CompaniesHouseImportResult:
    company: EntityRecord
    owner_entities: dict[str, EntityRecord]
    relations: list[RelationRecord]
    warnings: list[str] = field(default_factory=list)


def _psc_record_id(item: dict[str, Any], index: int) -> str:
    links = item.get("links") or {}
    self_link = str(links.get("self") or "").rstrip("/")
    if self_link:
        return self_link.rsplit("/", 1)[-1]
    return f"row-{index}"


def normalize_companies_house(
    company_profile: dict[str, Any],
    psc_items: Iterable[dict[str, Any]],
    *,
    retrieved_at: Optional[date] = None,
    base_url: str = "https://api.company-information.service.gov.uk",
) -> CompaniesHouseImportResult:
    """Normalize a Companies House company profile and PSC records.

    Natural-person PSC IDs are intentionally scoped to the company record.
    They are *not* treated as a universal person identifier. Cross-company or
    PEP matching must go through the separate entity-resolution layer.
    """
    number = str(company_profile.get("company_number") or "").strip()
    if not number:
        raise ValueError("company_profile.company_number is required")
    company_id = f"GB-COH:{number}"
    company_src = SourceRef(
        "Companies House",
        number,
        url=f"{base_url}/company/{number}",
        retrieved_at=retrieved_at,
    )
    company = EntityRecord(
        entity_id=company_id,
        name=str(company_profile.get("company_name") or number),
        entity_type="legal_entity",
        incorporated_on=_date(company_profile.get("date_of_creation")),
        stable_ids=(company_id,),
        source_refs=(company_src,),
    )

    owners: dict[str, EntityRecord] = {}
    relations: list[RelationRecord] = []
    warnings: list[str] = []

    for i, item in enumerate(psc_items):
        if not isinstance(item, dict):
            continue
        rec_id = _psc_record_id(item, i)
        kind = str(item.get("kind") or "unknown")
        name = str(item.get("name") or "").strip()
        if not name:
            warnings.append(f"psc_without_name:{rec_id}")
            name = rec_id

        src = SourceRef(
            "Companies House PSC",
            f"{number}:{rec_id}",
            url=f"{base_url}/company/{number}/persons-with-significant-control",
            retrieved_at=retrieved_at,
        )

        identification = item.get("identification") or {}
        registration_number = identification.get("registration_number")
        country = identification.get("country_registered")
        legal_authority = identification.get("legal_authority")

        is_legal = "legal-person" in kind or "corporate-entity" in kind
        if is_legal and registration_number:
            qualifier = str(country or legal_authority or "PSC").strip()
            owner_id = f"{qualifier}:{registration_number}"
            strength = "official_cross_id"
            stable_ids = (owner_id,)
            entity_type = "legal_entity"
        else:
            # The PSC endpoint proves a relationship to this company, but the
            # local record token does not prove that two same-named PSC records
            # in different companies are the same natural person.
            owner_id = f"GB-PSC:{number}:{rec_id}"
            strength = "multi_attribute"
            stable_ids = ()
            entity_type = "person"

        owner = EntityRecord(
            entity_id=owner_id,
            name=name,
            entity_type=entity_type,
            stable_ids=stable_ids,
            source_refs=(src,),
        )
        owners[owner_id] = owner
        relations.append(
            RelationRecord(
                left_id=owner_id,
                relation="BENEFICIAL_OWNER_OF",
                right_id=company_id,
                source_ref=src,
                valid_from=_date(item.get("notified_on")),
                valid_to=_date(item.get("ceased_on")),
                identity_strength=strength,
            )
        )

    return CompaniesHouseImportResult(
        company=company,
        owner_entities=owners,
        relations=relations,
        warnings=warnings,
    )


@dataclass
class USASpendingImportResult:
    case: IntegrityCase
    warnings: list[str] = field(default_factory=list)


def normalize_usaspending_award(
    row: dict[str, Any],
    *,
    retrieved_at: Optional[date] = None,
    source_url: str = "https://api.usaspending.gov/api/v2/search/spending_by_award/",
) -> USASpendingImportResult:
    """Normalize one USAspending spending_by_award result.

    This adapter intentionally leaves bid_count and legal_threshold unset:
    USAspending award search is an award/spending source, not a complete
    tender-competition record.
    """
    warnings: list[str] = []

    award_id = str(
        row.get("Award ID")
        or row.get("generated_internal_id")
        or row.get("internal_id")
        or ""
    ).strip()
    if not award_id:
        raise ValueError("USAspending row requires an award identifier")

    recipient_name = str(row.get("Recipient Name") or "").strip()
    recipient_uei = str(row.get("Recipient UEI") or "").strip()
    recipient_id = str(row.get("recipient_id") or "").strip()

    if recipient_uei:
        supplier_id = f"US-UEI:{recipient_uei}"
        stable_ids = (supplier_id,)
    elif recipient_id:
        supplier_id = f"USAspending-recipient:{recipient_id}"
        stable_ids = ()
        warnings.append("recipient_uei_missing")
    else:
        supplier_id = f"USAspending-recipient-name:{recipient_name or 'unknown'}"
        stable_ids = ()
        warnings.append("stable_recipient_identifier_missing")

    agency_code = str(row.get("Awarding Agency Code") or "").strip()
    agency_name = str(row.get("Awarding Agency") or "").strip()
    if agency_code:
        authority_id = f"US-FED-AGENCY:{agency_code}"
    elif agency_name:
        authority_id = f"USAspending-agency-name:{agency_name}"
        warnings.append("awarding_agency_code_missing")
    else:
        authority_id = "USAspending-agency:unknown"
        warnings.append("awarding_agency_missing")

    published = _date(row.get("Last Modified Date"))
    award_date = _date(row.get("Base Obligation Date") or row.get("Start Date"))
    amount = _amount(row.get("Award Amount"))

    src = SourceRef(
        source_name="USAspending",
        record_id=award_id,
        url=source_url,
        published_at=published,
        retrieved_at=retrieved_at,
    )

    supplier = EntityRecord(
        entity_id=supplier_id,
        name=recipient_name or supplier_id,
        entity_type="legal_entity",
        stable_ids=stable_ids,
        source_refs=(src,),
    )
    authority = EntityRecord(
        entity_id=authority_id,
        name=agency_name or authority_id,
        entity_type="public_authority",
        stable_ids=(authority_id,) if agency_code else (),
        source_refs=(src,),
    )

    contract = ContractRecord(
        contract_id=f"USAspending:{award_id}",
        authority_id=authority_id,
        supplier_ids=(supplier_id,),
        award_date=award_date,
        publication_date=published,
        award_value=amount,
        legal_threshold=None,
        bid_count=None,
        procurement_method=str(row.get("Contract Award Type") or "") or None,
        jurisdiction="US-federal",
        source_refs=(src,),
    )
    case = IntegrityCase(
        subject_id=contract.contract_id,
        contract=contract,
        entities={
            supplier.entity_id: supplier,
            authority.entity_id: authority,
        },
        source_coverage={"procurement_award"},
    )
    return USASpendingImportResult(case=case, warnings=warnings)



@dataclass
class OCDSRecordImportResult:
    cases: list[IntegrityCase] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    record_count: int = 0
    release_count: int = 0


def _release_datetime(release: dict[str, Any]) -> datetime:
    raw = release.get("date")
    if isinstance(raw, str) and raw.strip():
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            pass
    return datetime.min


def normalize_ocds_record_package(
    package: dict[str, Any],
    *,
    source_name: str = "OCDS record package",
    source_url: str = "",
    jurisdiction: Optional[str] = None,
    retrieved_at: Optional[date] = None,
) -> OCDSRecordImportResult:
    """Normalize an OCDS record package into de-duplicated award cases.

    A record package can contain multiple lifecycle releases for one OCID.
    This function preserves the latest observed award representation while
    carrying forward competition fields such as tender.numberOfTenderers from
    earlier releases *within the same OCID*.

    It does not carry fields across OCIDs and does not infer missing values.
    """
    records = package.get("records") or []
    all_cases: list[IntegrityCase] = []
    warnings: list[str] = []
    total_releases = 0

    for record in records:
        if not isinstance(record, dict):
            continue
        releases = [r for r in (record.get("releases") or []) if isinstance(r, dict)]
        total_releases += len(releases)
        releases.sort(key=_release_datetime)

        latest_bid_count: Optional[int] = None
        latest_method: Optional[str] = None
        seen_bid_counts: list[int] = []
        merged_entities: dict[str, EntityRecord] = {}
        latest_cases: dict[str, tuple[datetime, IntegrityCase]] = {}

        for release in releases:
            tender = release.get("tender") or {}
            raw_count = tender.get("numberOfTenderers")
            if isinstance(raw_count, int) and not isinstance(raw_count, bool):
                latest_bid_count = raw_count
                seen_bid_counts.append(raw_count)

            raw_method = tender.get("procurementMethod")
            if raw_method is not None:
                latest_method = str(raw_method)

            imported = normalize_ocds_release(
                release,
                source_name=source_name,
                source_url=source_url,
                jurisdiction=jurisdiction,
                retrieved_at=retrieved_at,
            )
            warnings.extend(imported.warnings)
            release_time = _release_datetime(release)

            for case in imported.cases:
                merged_entities.update(case.entities)
                previous = latest_cases.get(case.contract.contract_id)
                if previous is None or release_time >= previous[0]:
                    latest_cases[case.contract.contract_id] = (release_time, case)

        if len(set(seen_bid_counts)) > 1:
            record_ocid = str(record.get("ocid") or (releases[-1].get("ocid") if releases else "unknown"))
            warnings.append(
                f"number_of_tenderers_changed:{record_ocid}:{','.join(map(str, seen_bid_counts))}"
            )

        for _, case in latest_cases.values():
            contract = case.contract
            coverage = set(case.source_coverage)
            if latest_bid_count is not None:
                coverage.add("procurement_competition")
            contract = replace(
                contract,
                bid_count=(
                    contract.bid_count
                    if contract.bid_count is not None
                    else latest_bid_count
                ),
                procurement_method=(
                    contract.procurement_method
                    if contract.procurement_method
                    else latest_method
                ),
            )
            entities = dict(merged_entities)
            entities.update(case.entities)
            all_cases.append(
                IntegrityCase(
                    subject_id=case.subject_id,
                    contract=contract,
                    entities=entities,
                    relations=list(case.relations),
                    debarments=list(case.debarments),
                    source_coverage=coverage,
                )
            )

    return OCDSRecordImportResult(
        cases=all_cases,
        warnings=warnings,
        record_count=sum(1 for r in records if isinstance(r, dict)),
        release_count=total_releases,
    )
