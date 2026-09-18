"""Extraction verification utilities for ARIS4C011.

The extractor is not a trusted oracle. These helpers compare extracted
bibliographic claims with source-anchored authoritative fields before detector
inputs are allowed into confirmatory Track A.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Dict, List


def _norm_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def _norm_pages(value: Any) -> str:
    text = str(value or "").strip()
    text = text.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", "", text)


def _norm_field(field: str, value: Any) -> str:
    if field == "pages":
        return _norm_pages(value)
    return _norm_text(value)


@dataclass(frozen=True)
class MetadataMismatch:
    field: str
    expected: Any
    extracted: Any
    source_locator: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def verify_metadata_claims(
    extracted: Dict[str, Any],
    authoritative: Dict[str, Any],
    source_locators: Dict[str, str],
) -> Dict[str, Any]:
    """Compare extracted metadata with independently anchored source values."""
    mismatches: List[MetadataMismatch] = []
    unanchored: List[str] = []

    for field, expected in authoritative.items():
        locator = str(source_locators.get(field) or "").strip()
        if not locator:
            unanchored.append(field)
            continue
        actual = extracted.get(field)
        if _norm_field(field, actual) != _norm_field(field, expected):
            mismatches.append(MetadataMismatch(
                field=field,
                expected=expected,
                extracted=actual,
                source_locator=locator,
            ))

    safe = not mismatches and not unanchored
    return {
        "safe": safe,
        "mismatches": [m.to_dict() for m in mismatches],
        "unanchored_fields": unanchored,
        "reason": (
            "Extracted metadata matches all source-anchored authoritative fields."
            if safe else
            "Extractor output failed source-anchored metadata verification."
        ),
    }
