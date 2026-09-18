"""Adapter from ARIS4C011 Research Forensics findings to ARIS4C015.

The adapter is intentionally conservative:
- 011 findings never add scientific-value points;
- a FLAG is not an allegation of misconduct;
- prospective use requires evidence to be demonstrably available by cutoff;
- duplicated detector signals are grouped by dependency_group when supplied.

The output is routing metadata for human review: CLEAR, CAUTION, QUARANTINE,
or ABSTAIN.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable


STRONG_CLASSES = {"E0", "E1", "E2", "E3"}


@dataclass(frozen=True)
class IntegrityGate:
    state: str
    cutoff_safe: bool
    finding_ids: tuple[str, ...]
    reasons: tuple[str, ...]
    excluded_future_finding_ids: tuple[str, ...] = ()
    unknown_time_finding_ids: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "cutoff_safe": self.cutoff_safe,
            "finding_ids": list(self.finding_ids),
            "reasons": list(self.reasons),
            "excluded_future_finding_ids": list(
                self.excluded_future_finding_ids
            ),
            "unknown_time_finding_ids": list(self.unknown_time_finding_ids),
        }


def _year(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, (date, datetime)):
        return value.year
    text = str(value)
    if len(text) >= 4 and text[:4].isdigit():
        return int(text[:4])
    return None


def _finding_id(finding: dict[str, Any], index: int) -> str:
    return str(finding.get("finding_id") or f"finding-{index}")


def _dependency_group(finding: dict[str, Any], index: int) -> str:
    return str(
        finding.get("dependency_group")
        or finding.get("detector_id")
        or _finding_id(finding, index)
    )


def adapt_011_findings(
    findings: Iterable[dict[str, Any]],
    *,
    cutoff_year: int | None = None,
    require_timestamp_for_prospective: bool = True,
) -> IntegrityGate:
    """Convert 011 finding nodes into 015 routing state.

    Expected 011 fields include:
      finding_id, detector_id, family, applicable, status, evidence_class,
      reproducible, benign_explanations, misconduct_inference.

    For prospective use, callers may additionally provide one of:
      available_year, available_at, timestamp_available.

    Findings demonstrably after cutoff are excluded. If cutoff is supplied and
    timestamp is unknown, the finding is excluded by default rather than
    risking future leakage.
    """
    rows = list(findings)
    if not rows:
        return IntegrityGate(
            state="ABSTAIN",
            cutoff_safe=cutoff_year is None,
            finding_ids=(),
            reasons=("No 011 findings supplied.",),
        )

    eligible: list[tuple[int, dict[str, Any]]] = []
    future_ids: list[str] = []
    unknown_time_ids: list[str] = []

    for index, finding in enumerate(rows):
        fid = _finding_id(finding, index)
        if not bool(finding.get("applicable", False)):
            continue

        if cutoff_year is not None:
            observed_year = _year(
                finding.get("available_year")
                or finding.get("available_at")
                or finding.get("timestamp_available")
            )
            if observed_year is None and require_timestamp_for_prospective:
                unknown_time_ids.append(fid)
                continue
            if observed_year is not None and observed_year > cutoff_year:
                future_ids.append(fid)
                continue

        eligible.append((index, finding))

    if not eligible:
        reason = "No cutoff-safe applicable 011 findings."
        if cutoff_year is None:
            reason = "No applicable 011 findings."
        return IntegrityGate(
            state="ABSTAIN",
            cutoff_safe=not unknown_time_ids,
            finding_ids=(),
            reasons=(reason,),
            excluded_future_finding_ids=tuple(future_ids),
            unknown_time_finding_ids=tuple(unknown_time_ids),
        )

    flags = [
        (index, finding)
        for index, finding in eligible
        if str(finding.get("status", "")).upper() == "FLAG"
    ]
    non_error = [
        (index, finding)
        for index, finding in eligible
        if str(finding.get("status", "")).upper() != "ERROR"
    ]

    if not flags:
        return IntegrityGate(
            state="CLEAR" if non_error else "ABSTAIN",
            cutoff_safe=not unknown_time_ids,
            finding_ids=tuple(
                _finding_id(finding, index) for index, finding in non_error
            ),
            reasons=(
                "Applicable cutoff-safe 011 checks supplied no FLAG findings.",
            ),
            excluded_future_finding_ids=tuple(future_ids),
            unknown_time_finding_ids=tuple(unknown_time_ids),
        )

    strong_groups: set[str] = set()
    flag_ids: list[str] = []
    deterministic_e0 = False

    for index, finding in flags:
        fid = _finding_id(finding, index)
        flag_ids.append(fid)
        evidence_class = str(finding.get("evidence_class", "")).upper()
        if evidence_class in STRONG_CLASSES:
            strong_groups.add(_dependency_group(finding, index))
        if evidence_class == "E0" and str(
            finding.get("reproducible", "")
        ).lower() in {"yes", "true", "1"}:
            deterministic_e0 = True

    if deterministic_e0 or len(strong_groups) >= 2:
        state = "QUARANTINE"
        reasons = (
            "Unresolved cutoff-safe 011 flags warrant human review before "
            "discovery promotion.",
            "Quarantine is a routing decision, not a misconduct judgment.",
        )
    else:
        state = "CAUTION"
        reasons = (
            "At least one cutoff-safe 011 FLAG requires caution.",
            "The finding does not establish misconduct or invalidate the paper.",
        )

    return IntegrityGate(
        state=state,
        cutoff_safe=not unknown_time_ids,
        finding_ids=tuple(flag_ids),
        reasons=reasons,
        excluded_future_finding_ids=tuple(future_ids),
        unknown_time_finding_ids=tuple(unknown_time_ids),
    )
