"""Metadata leakage guards for ARIS4C011 Track A.

Current bibliographic metadata can itself encode a later integrity outcome
(e.g. titles prefixed with "RETRACTED:"). Track A must not expose such fields
to a model intended to simulate pre-outcome/content-only screening.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Tuple


_STATUS_PREFIX = re.compile(
    r"""^\s*(?:
        retracted(?:\s+article)? |
        withdrawn(?:\s+article)? |
        retraction(?:\s+notice)? |
        expression\s+of\s+concern
    )\s*[:\-]\s*""",
    flags=re.IGNORECASE | re.VERBOSE,
)


def first_text(value: Any) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value or "")


def sanitize_title(raw: str) -> Tuple[str, bool]:
    """Strip explicit post-publication status prefixes, preserving a leakage flag."""
    text = (raw or "").strip()
    cleaned = _STATUS_PREFIX.sub("", text, count=1).strip()
    return cleaned, cleaned != text


def date_year(value: Any) -> str:
    try:
        parts = (value or {}).get("date-parts") or []
        return str(parts[0][0]) if parts and parts[0] else ""
    except (TypeError, IndexError, KeyError):
        return ""


def extract_target_metadata(payload: Dict[str, Any], expected_doi: str = "") -> Dict[str, str]:
    msg = (payload or {}).get("message") or {}
    doi = str(msg.get("DOI") or "").strip().lower()
    expected = (expected_doi or "").strip().lower()
    if expected and doi != expected:
        raise ValueError(f"Crossref target DOI mismatch: expected {expected}, got {doi}")

    raw_title = first_text(msg.get("title"))
    safe_title, marker = sanitize_title(raw_title)

    year = (
        date_year(msg.get("published"))
        or date_year(msg.get("issued"))
        or date_year(msg.get("published-online"))
        or date_year(msg.get("published-print"))
    )
    updated_by = msg.get("updated-by") or []

    return {
        "target_doi": doi,
        "target_title_raw_current": raw_title,
        "target_title_safe": safe_title,
        "title_status_marker": "1" if marker else "0",
        "target_year": year,
        "target_journal": first_text(msg.get("container-title")),
        "article_type": str(msg.get("type") or ""),
        "publisher": str(msg.get("publisher") or ""),
        "current_metadata_contains_update_relations": "1" if updated_by else "0",
        "track_a_title_requires_historical_validation": "1" if marker else "0",
    }
