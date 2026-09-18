"""No-key Companies House URI adapter for basic company details.

Official Companies House URI service:
http://data.companieshouse.gov.uk/doc/company/{companynumber}

The JSON representation can be flat or RDF/JSON-like with namespaced predicate
keys and values wrapped in lists/dicts. This adapter therefore extracts only a
small allow-list of basic company fields recursively.

Registered-office addresses and other unrelated fields are deliberately ignored.
"""

from __future__ import annotations

from datetime import date, datetime
import re
from typing import Any, Iterable, Optional

from open_integrity_agent import EntityRecord, SourceRef


_FIELD_ALIASES = {
    "company_number": {"companynumber", "company_number"},
    "company_name": {"companyname", "company_name"},
    "incorporation_date": {
        "incorporationdate",
        "incorporation_date",
        "registrationdate",
        "registration_date",
    },
    "company_status": {"companystatus", "company_status"},
    "company_category": {"companycategory", "company_category"},
    "country_of_origin": {"countryoforigin", "country_of_origin"},
}


def _local_key(key: Any) -> str:
    raw = str(key)
    # RDF predicate URIs commonly end with /CompanyNumber or #CompanyNumber.
    tail = re.split(r"[/#:]", raw)[-1]
    return re.sub(r"[^a-z0-9_]+", "", tail.lower())


def _unbox(value: Any) -> Any:
    """Unbox common RDF/JSON and JSON-LD literal shapes without guessing."""
    if isinstance(value, list):
        for item in value:
            unboxed = _unbox(item)
            if unboxed not in (None, ""):
                return unboxed
        return None
    if isinstance(value, dict):
        for key in ("@value", "value", "literal"):
            if key in value:
                return _unbox(value[key])
        # Do not blindly return arbitrary nested dict content.
        return None
    return value


def _find_field(data: Any, aliases: Iterable[str]) -> Any:
    wanted = set(aliases)
    if isinstance(data, dict):
        # Prefer an exact/local predicate match before descending.
        for key, value in data.items():
            if _local_key(key) in wanted:
                unboxed = _unbox(value)
                if unboxed not in (None, ""):
                    return unboxed
        for value in data.values():
            found = _find_field(value, wanted)
            if found not in (None, ""):
                return found
    elif isinstance(data, list):
        for item in data:
            found = _find_field(item, wanted)
            if found not in (None, ""):
                return found
    return None


def _find_company_number_from_resource(data: Any) -> Optional[str]:
    """Fallback to a company identifier embedded in an RDF resource URI."""
    pattern = re.compile(r"/(?:id/)?company/([A-Za-z0-9]+)(?:[/.#?]|$)")
    if isinstance(data, dict):
        for key, value in data.items():
            match = pattern.search(str(key))
            if match:
                return match.group(1)
            found = _find_company_number_from_resource(value)
            if found:
                return found
    elif isinstance(data, list):
        for item in data:
            found = _find_company_number_from_resource(item)
            if found:
                return found
    elif isinstance(data, str):
        match = pattern.search(data)
        if match:
            return match.group(1)
    return None


def _uri_date(value: Any) -> Optional[date]:
    value = _unbox(value)
    if value in (None, ""):
        return None
    raw = str(value).strip()
    # The service has historically exposed DD/MM/YYYY; tolerate ISO as well.
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw[:10], fmt).date()
        except ValueError:
            pass
    return None


def _basic_value(data: Any, field: str) -> Any:
    return _find_field(data, _FIELD_ALIASES[field])


def normalize_companies_house_uri(
    data: Any,
    *,
    source_url: str,
    retrieved_at: Optional[date] = None,
) -> tuple[EntityRecord, dict[str, Any]]:
    number_value = _basic_value(data, "company_number")
    if not number_value:
        number_value = _find_company_number_from_resource(data)
    number = str(number_value or "").strip().upper()
    if not number:
        raise ValueError("Companies House URI record lacks a recoverable CompanyNumber")

    name = str(_basic_value(data, "company_name") or number).strip()
    incorporated = _uri_date(_basic_value(data, "incorporation_date"))

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
        "company_status": _basic_value(data, "company_status"),
        "company_category": _basic_value(data, "company_category"),
        "country_of_origin": _basic_value(data, "country_of_origin"),
        "incorporation_date": incorporated.isoformat() if incorporated else None,
        "source_url": source_url,
    }
    return entity, metadata


def sanitized_shape(data: Any) -> dict[str, Any]:
    """Return structural diagnostics only; never field values or addresses."""
    if isinstance(data, dict):
        return {
            "top_level_type": "object",
            "top_level_key_local_names": sorted({_local_key(k) for k in data.keys()})[:50],
            "top_level_key_count": len(data),
        }
    if isinstance(data, list):
        return {
            "top_level_type": "array",
            "length": len(data),
            "first_item_type": type(data[0]).__name__ if data else None,
        }
    return {"top_level_type": type(data).__name__}
