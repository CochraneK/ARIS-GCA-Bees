"""ARIS4C011 Pilot 0.

Minimal, dependency-free prototype for:
1) a detector output contract;
2) a conservative GRIM-style item-mean feasibility check;
3) sample-size consistency checks;
4) transparent review-priority aggregation.

This is a DESIGN/PILOT utility, not a fraud detector.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, Iterable, List, Optional
import json


@dataclass
class Finding:
    detector_id: str
    detector_version: str
    family: str
    applicable: bool
    applicability_reason: str
    status: str  # FLAG | PASS | ABSTAIN | ERROR
    evidence_class: str  # E0..E5
    claim: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    confidence: Optional[float] = None
    benign_explanations: List[str] = field(default_factory=list)
    dependency_group: Optional[str] = None
    misconduct_inference: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _decimal_places(text: str) -> int:
    text = text.strip().lower()
    if "e" in text:
        return max(0, -Decimal(text).as_tuple().exponent)
    return len(text.split(".", 1)[1]) if "." in text else 0


def grim_item_mean(
    reported_mean: str,
    n: int,
    scale_min: int,
    scale_max: int,
) -> Finding:
    """Conservative GRIM-style feasibility test for ONE integer-valued item.

    This implementation intentionally does not attempt the full family of
    GRIM variants. It checks whether any legal integer total for n observations
    rounds HALF_UP to the reported mean at the reported decimal precision.
    """
    if n <= 0 or scale_min > scale_max:
        return Finding(
            detector_id="grim_item_mean",
            detector_version="pilot0",
            family="numerical_forensics",
            applicable=False,
            applicability_reason="Invalid N or scale bounds.",
            status="ERROR",
            evidence_class="E1",
            claim="Input invalid.",
        )

    try:
        target = Decimal(reported_mean)
    except Exception:
        return Finding(
            detector_id="grim_item_mean",
            detector_version="pilot0",
            family="numerical_forensics",
            applicable=False,
            applicability_reason="Reported mean could not be parsed exactly.",
            status="ERROR",
            evidence_class="E1",
            claim="Mean parse failed.",
        )

    dp = _decimal_places(reported_mean)
    quantum = Decimal(1).scaleb(-dp)

    possible = []
    lo = n * scale_min
    hi = n * scale_max
    dn = Decimal(n)

    for total in range(lo, hi + 1):
        exact = Decimal(total) / dn
        if exact.quantize(quantum, rounding=ROUND_HALF_UP) == target:
            possible.append(str(exact))

    ok = bool(possible)
    return Finding(
        detector_id="grim_item_mean",
        detector_version="pilot0",
        family="numerical_forensics",
        applicable=True,
        applicability_reason=(
            "Integer-valued single-item outcome with known N and scale bounds."
        ),
        status="PASS" if ok else "FLAG",
        evidence_class="E1",
        claim=(
            "Reported mean is compatible with at least one legal integer total."
            if ok
            else "No legal integer total rounds to the reported mean under the pilot rounding rule."
        ),
        evidence={
            "reported_mean": reported_mean,
            "n": n,
            "scale_min": scale_min,
            "scale_max": scale_max,
            "decimal_places": dp,
            "compatible_exact_means_preview": possible[:10],
            "compatible_count": len(possible),
        },
        benign_explanations=(
            []
            if ok
            else [
                "Different denominator than reported.",
                "Composite/non-integer scoring.",
                "Different rounding convention.",
                "Transcription or table error.",
            ]
        ),
        dependency_group="reported_mean_n",
        misconduct_inference=False,
    )


def sample_size_consistency(values: Dict[str, int]) -> Finding:
    cleaned = {k: int(v) for k, v in values.items() if v is not None}
    unique = sorted(set(cleaned.values()))
    if len(cleaned) < 2:
        return Finding(
            detector_id="sample_size_consistency",
            detector_version="pilot0",
            family="table_consistency",
            applicable=False,
            applicability_reason="At least two independently extracted N values are required.",
            status="ABSTAIN",
            evidence_class="E1",
            claim="Insufficient independent N reports.",
            evidence={"values": cleaned},
        )

    ok = len(unique) == 1
    return Finding(
        detector_id="sample_size_consistency",
        detector_version="pilot0",
        family="table_consistency",
        applicable=True,
        applicability_reason="Multiple N values were extracted from comparable study scopes.",
        status="PASS" if ok else "FLAG",
        evidence_class="E1",
        claim="Reported sample sizes agree." if ok else "Reported sample sizes disagree.",
        evidence={"values": cleaned, "unique_values": unique},
        benign_explanations=(
            []
            if ok
            else [
                "Different analysis populations.",
                "Missing-data exclusions.",
                "Subgroup rather than full-sample denominator.",
                "Reporting/transcription error.",
            ]
        ),
        dependency_group="sample_size",
        misconduct_inference=False,
    )


def review_priority(findings: Iterable[Finding]) -> Dict[str, Any]:
    flags = [f for f in findings if f.status == "FLAG" and f.applicable]
    strong = [f for f in flags if f.evidence_class in {"E1", "E2", "E3"}]
    weak = [f for f in flags if f.evidence_class in {"E4", "E5"}]

    independent_strong_families = sorted({f.family for f in strong})
    all_flag_families = sorted({f.family for f in flags})

    if len(independent_strong_families) >= 2:
        priority = "HIGH"
    elif len(independent_strong_families) == 1:
        priority = "MODERATE"
    elif len(all_flag_families) >= 2:
        priority = "MODERATE"
    elif weak:
        priority = "LOW"
    else:
        priority = "NONE"

    return {
        "review_priority": priority,
        "flag_count": len(flags),
        "flag_families": all_flag_families,
        "strong_independent_families": independent_strong_families,
        "interpretation": "Triage priority only; not a misconduct probability.",
    }


def demo() -> Dict[str, Any]:
    findings = [
        grim_item_mean("6.98", n=25, scale_min=1, scale_max=7),
        sample_size_consistency({"methods": 42, "table_1": 37}),
    ]
    return {
        "findings": [f.to_dict() for f in findings],
        "summary": review_priority(findings),
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, ensure_ascii=False))
