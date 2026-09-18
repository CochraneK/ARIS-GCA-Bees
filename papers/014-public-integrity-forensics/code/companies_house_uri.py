"""No-key Companies House URI adapter for basic company details.

Official Companies House URI service:
http://data.companieshouse.gov.uk/doc/company/{companynumber}

The service supports JSON via content negotiation / .json and exposes basic
company data including company number, status, category and incorporation date.
This adapter deliberately ignores registered-office address by default because
Pilot 1A/B only needs stable company identity and incorporation timing.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from open_integrity_agent import EntityRecord, SourceRef


def _uri_date(value: Any) -> Optional[date]:
    if not value:
        return None
    raw = str(value).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            pass
    return None


def normalize_companies_house_uri(
    data: dict[str, Any],
    *,
    source_url: str,
    retrieved_at: Optional[date] = None,
) -> tuple[EntityRecord, dict[str, Any]]:
    number = str(
        data.get("CompanyNumber")
        or data.get("companyNumber")
        or data.get("company_number")
        or ""
    ).strip().upper()
    if not number:
        raise ValueError("Companies House URI record lacks CompanyNumber")

    name = str(
        data.get("CompanyName")
        or data.get("companyName")
        or data.get("company_name")
        or number
    ).strip()
    incorporated = _uri_date(
        data.get("IncorporationDate")
        or data.get("incorporationDate")
        or data.get("incorporation_date")
        or data.get("RegistrationDate")
        or data.get("registrationDate")
    )

    entity_id = f"GB-COH:{number}"
    src = SourceRef(
        source_name="Companies House URI",
        record_id=number,
        url=source_url,
        retrieved_at=retrieved_at,
    )
    entity = EntityRecord(
        entity_id=entity_id,
        name=name,
        entity_type="legal_entity",
        incorporated_on=incorporated,
        stable_ids=(entity_id,),
        source_refs=(src,),
    )
    metadata = {
        "company_number": number,
        "company_status": data.get("CompanyStatus") or data.get("companyStatus"),
        "company_category": data.get("CompanyCategory") or data.get("companyCategory"),
        "country_of_origin": data.get("CountryOfOrigin") or data.get("countryOfOrigin"),
        "incorporation_date": incorporated.isoformat() if incorporated else None,
        "source_url": source_url,
    }
    return entity, metadata
