"""Conservative cross-source organization resolution for OpenIntegrity China.

Rules:
- exact CN-USCC is the only automatic cross-source merge key;
- exact normalized names without a stable ID create REVIEW_CANDIDATE links only;
- name similarity, mission, geography, nationality, or institutional type never auto-merge;
- every decision keeps source provenance and corruption_inference=False.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import re
from typing import Iterable, Mapping, Any


def normalize_org_name(value: str) -> str:
    value = (value or "").strip()
    value = value.replace("（", "(").replace("）", ")")
    value = re.sub(r"\s+", "", value)
    return value


@dataclass(frozen=True)
class ResolutionDecision:
    left_id: str
    right_id: str
    relation: str
    basis: str
    confidence: str
    auto_merge: bool
    corruption_inference: bool = False

    def as_json(self) -> dict[str, Any]:
        return asdict(self)


def _stable_uscc(node: Mapping[str, Any]) -> set[str]:
    out: set[str] = set()
    for raw in node.get("stable_ids", []) or []:
        raw = str(raw).strip().upper()
        if raw.startswith("CN-USCC:") and len(raw.split(":", 1)[1]) == 18:
            out.add(raw)
    node_id = str(node.get("id") or "").strip().upper()
    if node_id.startswith("CN-USCC:") and len(node_id.split(":", 1)[1]) == 18:
        out.add(node_id)
    return out


def resolve_pair(left: Mapping[str, Any], right: Mapping[str, Any]) -> ResolutionDecision | None:
    left_id = str(left.get("id") or "")
    right_id = str(right.get("id") or "")
    if not left_id or not right_id or left_id == right_id:
        return None

    a = _stable_uscc(left)
    b = _stable_uscc(right)
    shared = sorted(a & b)
    if shared:
        return ResolutionDecision(
            left_id=left_id,
            right_id=right_id,
            relation="SAME_ORG",
            basis=f"exact_stable_id:{shared[0]}",
            confidence="deterministic",
            auto_merge=True,
        )

    ln = normalize_org_name(str(left.get("name") or ""))
    rn = normalize_org_name(str(right.get("name") or ""))
    if ln and rn and ln == rn:
        return ResolutionDecision(
            left_id=left_id,
            right_id=right_id,
            relation="REVIEW_CANDIDATE",
            basis="exact_normalized_name_without_shared_stable_id",
            confidence="review_required",
            auto_merge=False,
        )
    return None


def resolve_cross_source(nodes: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = list(nodes)
    out: list[dict[str, Any]] = []
    for i, left in enumerate(rows):
        for right in rows[i + 1 :]:
            decision = resolve_pair(left, right)
            if decision is not None:
                out.append(decision.as_json())
    return out
