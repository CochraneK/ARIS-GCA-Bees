"""Immutable-ish source snapshot helpers for OpenIntegrity.

The helpers canonicalize JSON, compute a SHA-256 digest, and preserve the three
time dimensions needed for Track A:
- published_at: when the record became public (when known)
- valid_from/valid_to: when the underlying relationship was true (when known)
- retrieved_at: when OpenIntegrity fetched this copy

A retrieval timestamp is never substituted for an unknown publication date.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import hashlib
import json
from typing import Any, Optional


def canonical_json_bytes(payload: Any) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


@dataclass(frozen=True)
class SourceSnapshot:
    source_name: str
    source_record_id: str
    source_url: str
    retrieved_at: datetime
    published_at: Optional[datetime]
    valid_from: Optional[date]
    valid_to: Optional[date]
    parser_version: str
    sha256: str

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        for key in ("retrieved_at", "published_at"):
            value = out[key]
            out[key] = value.isoformat() if value else None
        for key in ("valid_from", "valid_to"):
            value = out[key]
            out[key] = value.isoformat() if value else None
        return out


def make_snapshot(
    payload: Any,
    *,
    source_name: str,
    source_record_id: str,
    source_url: str,
    parser_version: str,
    retrieved_at: Optional[datetime] = None,
    published_at: Optional[datetime] = None,
    valid_from: Optional[date] = None,
    valid_to: Optional[date] = None,
) -> SourceSnapshot:
    retrieved = retrieved_at or datetime.now(timezone.utc)
    digest = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    return SourceSnapshot(
        source_name=source_name,
        source_record_id=source_record_id,
        source_url=source_url,
        retrieved_at=retrieved,
        published_at=published_at,
        valid_from=valid_from,
        valid_to=valid_to,
        parser_version=parser_version,
        sha256=digest,
    )


def track_a_eligibility(snapshot: SourceSnapshot, cutoff: datetime) -> tuple[bool, str]:
    """Return whether the record is feature-side safe for a Track A cutoff."""
    if snapshot.published_at is None:
        return False, "publication_time_unknown"
    pub = snapshot.published_at
    if pub.tzinfo is None and cutoff.tzinfo is not None:
        pub = pub.replace(tzinfo=timezone.utc)
    if cutoff.tzinfo is None and pub.tzinfo is not None:
        cutoff = cutoff.replace(tzinfo=timezone.utc)
    if pub > cutoff:
        return False, "published_after_cutoff"
    return True, "published_on_or_before_cutoff"
