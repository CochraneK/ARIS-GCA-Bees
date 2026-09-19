"""Reference orchestrator for the ARIS4C011 Research Forensics skill.

Dependency-free by design. Real detector adapters can wrap external libraries,
APIs, or local models while preserving the same applicability and finding
semantics.

This module never computes a fraud probability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Protocol, Sequence
import hashlib


STRONG_CLASSES = {"E1", "E2", "E3"}
WEAK_CLASSES = {"E4", "E5"}
VALID_STATUSES = {"FLAG", "PASS", "ABSTAIN", "ERROR"}

# Structured inputs that can alter deterministic detector outputs. In Track A,
# every supplied record must be anchored to a source locator and explicitly
# verified against the time-safe artifact before execution.
STRUCTURED_INPUT_KEYS = {
    "nhst_tests",
    "discrete_means",
    "binary_summaries",
    "table_checks",
    "doi_resolutions",
    "cross_source_records",
    "categorical_aggregate_checks",
}


@dataclass(frozen=True)
class Applicability:
    applicable: bool
    reason: str


@dataclass
class Finding:
    detector_id: str
    detector_version: str
    family: str
    applicable: bool
    applicability_reason: str
    status: str
    evidence_class: str
    claim: str
    source_locator: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)
    reproducible: str = "unknown"
    confidence: Optional[float] = None
    calibration_reference: Optional[str] = None
    benign_explanations: List[str] = field(default_factory=list)
    dependency_group: Optional[str] = None
    next_action: Optional[str] = None
    misconduct_inference: bool = False
    finding_id: str = ""

    def finalize(self) -> "Finding":
        if self.status not in VALID_STATUSES:
            raise ValueError(f"Invalid finding status: {self.status}")
        if self.evidence_class not in {"E0", "E1", "E2", "E3", "E4", "E5"}:
            raise ValueError(f"Invalid evidence class: {self.evidence_class}")
        if self.misconduct_inference:
            raise ValueError("Detector-level misconduct inference is prohibited.")
        if not self.finding_id:
            raw = "|".join([
                self.detector_id,
                self.detector_version,
                self.family,
                self.status,
                self.source_locator,
                self.claim,
            ]).encode("utf-8")
            self.finding_id = "f_" + hashlib.sha256(raw).hexdigest()[:16]
        return self

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self.finalize())


@dataclass
class ForensicContext:
    artifact_id: str
    mode: str = "ad_hoc"
    artifact_safety: Dict[str, Any] = field(default_factory=dict)
    content: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class Detector(Protocol):
    detector_id: str
    detector_version: str
    family: str

    def applicability(self, context: ForensicContext) -> Applicability:
        ...

    def run(self, context: ForensicContext) -> Sequence[Finding]:
        ...


def _abstain(detector: Detector, reason: str) -> Finding:
    return Finding(
        detector_id=detector.detector_id,
        detector_version=detector.detector_version,
        family=detector.family,
        applicable=False,
        applicability_reason=reason,
        status="ABSTAIN",
        evidence_class="E0",
        claim="Detector not applicable to the available artifact.",
        reproducible="yes",
        misconduct_inference=False,
    ).finalize()


def _error(detector: Detector, reason: str) -> Finding:
    return Finding(
        detector_id=detector.detector_id,
        detector_version=detector.detector_version,
        family=detector.family,
        applicable=True,
        applicability_reason="Detector passed applicability but execution failed.",
        status="ERROR",
        evidence_class="E0",
        claim=reason,
        reproducible="unknown",
        misconduct_inference=False,
    ).finalize()


def structured_extraction_preflight(content: Dict[str, Any]) -> Dict[str, Any]:
    """Fail closed on unverified structured detector inputs.

    Extraction is a separate source of error from the detector. Track A may
    only consume records that retain a source locator and have been explicitly
    checked against the qualified artifact.
    """
    supplied = 0
    failures: List[Dict[str, Any]] = []

    for key in sorted(STRUCTURED_INPUT_KEYS):
        records = content.get(key) or []
        if not isinstance(records, list):
            failures.append({
                "input_key": key,
                "record_index": None,
                "reason": "Structured detector input must be a list.",
            })
            continue

        for index, record in enumerate(records):
            supplied += 1
            if not isinstance(record, dict):
                failures.append({
                    "input_key": key,
                    "record_index": index,
                    "reason": "Structured detector record must be an object.",
                })
                continue
            if not str(record.get("source_locator") or "").strip():
                failures.append({
                    "input_key": key,
                    "record_index": index,
                    "reason": "Missing source_locator.",
                })
            if record.get("provenance_verified") is not True:
                failures.append({
                    "input_key": key,
                    "record_index": index,
                    "reason": "provenance_verified is not true.",
                })

    return {
        "safe": not failures,
        "structured_record_count": supplied,
        "failures": failures,
        "reason": (
            "All structured records are source-anchored and verified."
            if not failures else
            "One or more structured records failed extraction provenance checks."
        ),
    }


def artifact_preflight(context: ForensicContext) -> Dict[str, Any]:
    if context.mode not in {"track_a", "track_b", "ad_hoc"}:
        return {"eligible": False, "reason": f"Unknown mode: {context.mode}"}

    safety = dict(context.artifact_safety or {})

    if context.mode == "track_a":
        time_safe = safety.get("time_safe")
        document_safe = safety.get("document_safe")
        title_safe = safety.get("title_safe")
        if time_safe is not True:
            return {
                **safety,
                "eligible": False,
                "reason": "Track A requires an explicitly time-safe artifact.",
            }
        if document_safe is not True:
            return {
                **safety,
                "eligible": False,
                "reason": "Track A requires a document with no post-outcome banner/status leakage.",
            }
        if title_safe is not True:
            return {
                **safety,
                "eligible": False,
                "reason": "Track A requires a historically validated status-free title.",
            }

        extraction = structured_extraction_preflight(context.content)
        safety["extraction"] = extraction
        if extraction["safe"] is not True:
            return {
                **safety,
                "eligible": False,
                "reason": "Track A requires source-verified structured extraction records.",
            }

    return {
        **safety,
        "eligible": True,
        "reason": "Artifact passed the requested mode's preflight.",
    }


def run_detectors(
    context: ForensicContext,
    detectors: Iterable[Detector],
) -> List[Finding]:
    findings: List[Finding] = []

    for detector in detectors:
        try:
            decision = detector.applicability(context)
        except Exception as exc:
            findings.append(_error(detector, f"Applicability check failed: {exc}"))
            continue

        if not decision.applicable:
            findings.append(_abstain(detector, decision.reason))
            continue

        try:
            produced = list(detector.run(context))
            if not produced:
                findings.append(_error(detector, "Applicable detector returned no finding records."))
                continue

            for finding in produced:
                # Preserve record-level ABSTAIN semantics inside a detector that
                # is applicable to other records in the same artifact.
                if finding.status == "ABSTAIN":
                    finding.applicable = False
                elif finding.status in {"FLAG", "PASS"}:
                    finding.applicable = True
                if not finding.applicability_reason:
                    finding.applicability_reason = decision.reason
                findings.append(finding.finalize())
        except Exception as exc:
            findings.append(_error(detector, f"Detector execution failed: {exc}"))

    return findings


def _independent_strong_groups(findings: Sequence[Finding]) -> set:
    groups = set()
    for finding in findings:
        if (
            finding.status == "FLAG"
            and finding.applicable
            and finding.evidence_class in STRONG_CLASSES
        ):
            group = finding.dependency_group or (
                f"family:{finding.family}:{finding.finding_id}"
            )
            groups.add((finding.family, group))
    return groups


def _independent_model_groups(findings: Sequence[Finding]) -> set:
    groups = set()
    for finding in findings:
        if (
            finding.status == "FLAG"
            and finding.applicable
            and finding.evidence_class == "E4"
        ):
            group = finding.dependency_group or (
                f"family:{finding.family}:{finding.finding_id}"
            )
            groups.add((finding.family, group))
    return groups


def review_priority(findings: Sequence[Finding]) -> str:
    strong = _independent_strong_groups(findings)
    strong_families = {family for family, _ in strong}
    model = _independent_model_groups(findings)
    model_families = {family for family, _ in model}
    weak_flags = [
        finding for finding in findings
        if finding.status == "FLAG" and finding.evidence_class == "E5"
    ]

    if len(strong_families) >= 2:
        return "HIGH"
    if len(strong_families) == 1:
        return "MODERATE"
    if len(model_families) >= 2:
        return "MODERATE"
    if model_families or weak_flags:
        return "LOW"
    return "NONE"


def coverage(findings: Sequence[Finding], registered_families: Sequence[str]) -> Dict[str, List[str]]:
    registered = sorted(set(registered_families))
    applicable = sorted({
        f.family for f in findings
        if f.applicable and f.status in {"FLAG", "PASS"}
    })
    executed = sorted({
        f.family for f in findings
        if f.status in {"FLAG", "PASS"}
    })
    abstained = sorted({f.family for f in findings if f.status == "ABSTAIN"})
    errored = sorted({f.family for f in findings if f.status == "ERROR"})

    return {
        "registered_families": registered,
        "applicable_families": applicable,
        "executed_families": executed,
        "abstained_families": abstained,
        "errored_families": errored,
    }


def evidence_graph(findings: Sequence[Finding]) -> Dict[str, Any]:
    nodes = [f.to_dict() for f in findings]
    edges: List[Dict[str, str]] = []

    by_dependency: Dict[str, List[Finding]] = {}
    for finding in findings:
        if finding.dependency_group:
            by_dependency.setdefault(finding.dependency_group, []).append(finding)

    for group, members in by_dependency.items():
        if len(members) < 2:
            continue
        anchor = members[0].finding_id
        for other in members[1:]:
            edges.append({
                "source": other.finding_id,
                "target": anchor,
                "relation": "same_source_as",
                "dependency_group": group,
            })

    return {"nodes": nodes, "edges": edges}


def run_forensics(
    context: ForensicContext,
    detectors: Sequence[Detector],
    limitations: Optional[List[str]] = None,
) -> Dict[str, Any]:
    safety = artifact_preflight(context)
    registered_families = [detector.family for detector in detectors]

    if not safety["eligible"]:
        return {
            "report_version": "0.1.0",
            "artifact_id": context.artifact_id,
            "mode": context.mode,
            "artifact_safety": safety,
            "findings": [],
            "coverage": {
                "registered_families": sorted(set(registered_families)),
                "applicable_families": [],
                "executed_families": [],
                "abstained_families": sorted(set(registered_families)),
                "errored_families": [],
            },
            "evidence_graph": {"nodes": [], "edges": []},
            "review_priority": "BLOCKED",
            "interpretation": (
                "Requested mode failed artifact/provenance preflight. "
                "No misconduct inference was made."
            ),
            "limitations": list(limitations or []),
        }

    findings = run_detectors(context, detectors)
    priority = review_priority(findings)
    return {
        "report_version": "0.1.0",
        "artifact_id": context.artifact_id,
        "mode": context.mode,
        "artifact_safety": safety,
        "findings": [finding.to_dict() for finding in findings],
        "coverage": coverage(findings, registered_families),
        "evidence_graph": evidence_graph(findings),
        "review_priority": priority,
        "interpretation": (
            "Review priority is triage only; it is not a probability of fraud "
            "or a finding of misconduct."
        ),
        "limitations": list(limitations or []),
    }
