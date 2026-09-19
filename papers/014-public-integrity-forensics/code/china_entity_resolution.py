"""Conservative cross-source organization resolution for OpenIntegrity China.

Rules:
- exact valid CN-USCC is the only automatic cross-source merge key;
- exact normalized names without a shared stable ID create review-only links;
- same names paired with disjoint stable IDs are explicit conflicts, never merge candidates;
- name similarity, mission, geography, nationality, or institutional type never auto-merge;
- every decision keeps source provenance and corruption_inference=False.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import re
from typing import Iterable, Mapping, Any


_CN_USCC_RE = re.compile(r"^[0-9A-HJ-NPQRTUWXY]{18}$")


def normalize_org_name(value: str) -> str:
    value = (value or "").strip()
    value = value.replace("（", "(").replace("）", ")")
    value = re.sub(r"\s+", "", value)
    return value


def normalize_cn_uscc(value: str) -> str | None:
    """Return a canonical CN-USCC token or None.

    This is deliberately a narrow syntactic gate. It does not claim that the
    identifier is currently valid in an authoritative registry; live-source
    provenance is handled by source adapters.
    """
    raw = str(value or "").strip().upper()
    if raw.startswith("CN-USCC:"):
        raw = raw.split(":", 1)[1].strip()
    if not _CN_USCC_RE.fullmatch(raw):
        return None
    return f"CN-USCC:{raw}"


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
        normalized = normalize_cn_uscc(str(raw))
        if normalized:
            out.add(normalized)
    normalized_id = normalize_cn_uscc(str(node.get("id") or ""))
    if normalized_id:
        out.add(normalized_id)
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
        if a and b and a.isdisjoint(b):
            return ResolutionDecision(
                left_id=left_id,
                right_id=right_id,
                relation="STABLE_ID_CONFLICT",
                basis="exact_normalized_name_with_disjoint_stable_ids",
                confidence="review_required",
                auto_merge=False,
            )
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


def build_resolution_audit(nodes: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Build a deterministic identity-resolution audit artifact.

    The artifact separates:
    - exact stable-ID clusters that are safe to auto-merge;
    - name-only review candidates;
    - same-name/disjoint-ID conflicts;
    - unresolved manifestations.

    No output is an integrity-risk signal.
    """
    rows = [dict(x) for x in nodes]
    node_ids = [str(x.get("id") or "") for x in rows]
    if any(not x for x in node_ids):
        raise ValueError("all nodes must have a non-empty id")
    if len(node_ids) != len(set(node_ids)):
        raise ValueError("node ids must be unique")

    by_uscc: dict[str, list[str]] = {}
    nodes_with_uscc: set[str] = set()
    for node in rows:
        nid = str(node["id"])
        ids = _stable_uscc(node)
        if ids:
            nodes_with_uscc.add(nid)
        for stable_id in sorted(ids):
            by_uscc.setdefault(stable_id, []).append(nid)

    exact_clusters = [
        {
            "stable_id": stable_id,
            "node_ids": sorted(ids),
            "manifestations": len(ids),
            "auto_merge": True,
            "corruption_inference": False,
        }
        for stable_id, ids in sorted(by_uscc.items())
        if len(ids) >= 2
    ]

    decisions = resolve_cross_source(rows)
    auto_merge = [x for x in decisions if x["auto_merge"]]
    review = [x for x in decisions if x["relation"] == "REVIEW_CANDIDATE"]
    conflicts = [x for x in decisions if x["relation"] == "STABLE_ID_CONFLICT"]

    linked_nodes: set[str] = set()
    for decision in decisions:
        linked_nodes.add(decision["left_id"])
        linked_nodes.add(decision["right_id"])

    return {
        "schema_version": 1,
        "nodes": len(rows),
        "nodes_with_valid_cn_uscc": len(nodes_with_uscc),
        "valid_cn_uscc_values": len(by_uscc),
        "exact_stable_id_clusters": exact_clusters,
        "exact_stable_id_cluster_count": len(exact_clusters),
        "auto_merge_decisions": auto_merge,
        "auto_merge_decision_count": len(auto_merge),
        "name_only_review_candidates": review,
        "name_only_review_candidate_count": len(review),
        "stable_id_conflicts": conflicts,
        "stable_id_conflict_count": len(conflicts),
        "unlinked_node_ids": sorted(set(node_ids) - linked_nodes),
        "corruption_inference": False,
        "interpretation": (
            "Identity-resolution audit only. Exact stable-ID equality can support "
            "deterministic organization merging; name-only links require review; "
            "same-name disjoint IDs are conflicts. None is an integrity-risk signal."
        ),
    }
