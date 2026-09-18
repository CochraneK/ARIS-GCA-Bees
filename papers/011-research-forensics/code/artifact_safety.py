"""Time-safe artifact qualification for ARIS4C011 Track A.

Statuses:
    SAFE_EXACT   eligible for primary Track A
    PROXY_ONLY   eligible only for prespecified proxy/sensitivity analyses
    BLOCKED      not eligible for content-only Track A
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
import re
from typing import Any, Dict, List, Optional


EXACT_EQUIVALENCE = {
    "same_published_version",
    "publisher_original_snapshot",
    "archive_snapshot_of_published_version",
    "preserved_original_published_version",
}

PROXY_EQUIVALENCE = {
    "preprint_proxy",
    "accepted_manuscript_proxy",
    "author_manuscript_proxy",
}

_TITLE_STATUS_PATTERNS = [
    re.compile(r"^\s*retracted(?:\s+article)?\s*[:\-]", re.I),
    re.compile(r"^\s*withdrawn(?:\s+article)?\s*[:\-]", re.I),
    re.compile(r"^\s*expression\s+of\s+concern\s*[:\-]", re.I),
    re.compile(r"^\s*(?:author\s+)?correction\s*[:\-]", re.I),
    re.compile(r"^\s*corrigendum\b", re.I),
    re.compile(r"^\s*erratum\b", re.I),
]

_LEADING_BANNER_PATTERNS = [
    re.compile(r"\bthis\s+article\s+(?:has\s+been|was)\s+retracted\b", re.I),
    re.compile(r"\bthis\s+article\s+has\s+been\s+corrected\b", re.I),
    re.compile(r"\ba\s+correction\s+to\s+this\s+(?:paper|article)\b", re.I),
    re.compile(r"\bexpression\s+of\s+concern\b", re.I),
    re.compile(r"\bupdates?\s+(?:are|is)\s+available\b", re.I),
    re.compile(r"\bretraction\s+notice\b", re.I),
]

_FILENAME_LABEL_PATTERNS = [
    re.compile(r"(?:^|[_\-./])(retracted|fraud|misconduct|correction|corrigendum|erratum)(?:[_\-./]|$)", re.I),
]


@dataclass
class ArtifactQualification:
    status: str
    track_a_eligible: bool
    proxy_eligible: bool
    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    return date.fromisoformat(str(value)[:10])


def _matches(patterns: List[re.Pattern], value: str) -> List[str]:
    hits = []
    text = value or ""
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            hits.append(match.group(0))
    return hits


def assess_track_a_artifact(
    *,
    artifact_version_date: Optional[str],
    outcome_date: Optional[str],
    immutable_or_historical_snapshot: bool,
    historical_equivalence: str,
    provenance_source: str,
    title: str = "",
    filename_or_path: str = "",
    leading_text: str = "",
    current_metadata_has_update_relation: bool = False,
) -> ArtifactQualification:
    """Qualify one artifact for primary Track A or proxy-only analysis."""

    reasons: List[str] = []
    warnings: List[str] = []
    evidence: Dict[str, Any] = {
        "artifact_version_date": artifact_version_date,
        "outcome_date": outcome_date,
        "immutable_or_historical_snapshot": bool(immutable_or_historical_snapshot),
        "historical_equivalence": historical_equivalence,
        "provenance_source": provenance_source,
        "current_metadata_has_update_relation": bool(current_metadata_has_update_relation),
    }

    version_date = _parse_date(artifact_version_date)
    event_date = _parse_date(outcome_date)

    if not provenance_source.strip():
        reasons.append("Missing artifact provenance source.")

    if version_date is None:
        reasons.append("Artifact version date is missing.")
    if event_date is None:
        reasons.append("Outcome/update date is missing.")
    if version_date is not None and event_date is not None and version_date >= event_date:
        reasons.append("Artifact version is not demonstrably earlier than the outcome/update.")

    if not immutable_or_historical_snapshot:
        reasons.append("Artifact is a mutable/current representation rather than a verified historical snapshot.")

    title_hits = _matches(_TITLE_STATUS_PATTERNS, title)
    banner_hits = _matches(_LEADING_BANNER_PATTERNS, (leading_text or "")[:6000])
    path_hits = _matches(_FILENAME_LABEL_PATTERNS, filename_or_path)
    evidence["title_status_hits"] = title_hits
    evidence["leading_banner_hits"] = banner_hits
    evidence["path_label_hits"] = path_hits

    if title_hits:
        reasons.append("Title contains a post-publication status marker.")
    if banner_hits:
        reasons.append("Leading document content contains a post-publication status/update marker.")
    if path_hits:
        reasons.append("Filename/path contains a potential outcome label.")

    if current_metadata_has_update_relation:
        warnings.append(
            "Current bibliographic metadata contains an update relation; keep it outside Track A model-visible inputs."
        )

    equivalence = (historical_equivalence or "").strip().lower()
    if equivalence in EXACT_EQUIVALENCE:
        proxy = False
    elif equivalence in PROXY_EQUIVALENCE:
        proxy = True
        warnings.append(
            "Artifact predates the outcome but is a proxy version, not the same published version."
        )
    else:
        proxy = False
        reasons.append("Historical equivalence class is unknown or unsupported.")

    if reasons:
        return ArtifactQualification(
            status="BLOCKED",
            track_a_eligible=False,
            proxy_eligible=False,
            reasons=reasons,
            warnings=warnings,
            evidence=evidence,
        )

    if proxy:
        return ArtifactQualification(
            status="PROXY_ONLY",
            track_a_eligible=False,
            proxy_eligible=True,
            reasons=[],
            warnings=warnings,
            evidence=evidence,
        )

    return ArtifactQualification(
        status="SAFE_EXACT",
        track_a_eligible=True,
        proxy_eligible=False,
        reasons=[],
        warnings=warnings,
        evidence=evidence,
    )
