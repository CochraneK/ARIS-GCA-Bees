"""Exact-stable-ID cross-source enrichment for OpenIntegrity China.

This module enriches organization identities with factual public-source
attributes. It is deliberately NOT a corruption-risk scorer.

Safety / identity rules:
- only exact valid CN-USCC equality can auto-attach a second-source record;
- exact-name-only matches are emitted as REVIEW_CANDIDATE and never enriched;
- same-name records with disjoint stable IDs are STABLE_ID_CONFLICT;
- inaccessible / interactive-only sources remain explicit COVERAGE_GAP;
- each attached attribute retains source provenance;
- no output may set corruption_inference=True.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable, Mapping

from china_entity_resolution import normalize_cn_uscc, normalize_org_name


ALLOWED_ENRICHMENT_FIELDS = {
    "registered_name",
    "organization_type",
    "registration_status",
    "registration_date",
    "registered_authority",
    "public_registry_url",
}


@dataclass(frozen=True)
class SourceObservation:
    source_id: str
    source_record_id: str
    name: str
    stable_ids: tuple[str, ...]
    attributes: Mapping[str, Any]
    source_url: str
    retrieved_at: str
    source_access_state: str = "AVAILABLE"

    def to_dict(self) -> dict[str, Any]:
        out=asdict(self)
        out["stable_ids"]=list(self.stable_ids)
        out["attributes"]=dict(self.attributes)
        return out


def _usccs(record: Mapping[str, Any]) -> set[str]:
    values=list(record.get("stable_ids") or [])
    values.append(str(record.get("id") or ""))
    out=set()
    for raw in values:
        val=normalize_cn_uscc(str(raw))
        if val:
            out.add(val)
    return out


def _safe_attributes(attributes: Mapping[str, Any]) -> dict[str, Any]:
    return {
        k: attributes[k]
        for k in sorted(attributes)
        if k in ALLOWED_ENRICHMENT_FIELDS
    }


def enrich_one(
    graph_node: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> dict[str, Any]:
    """Return one auditable enrichment decision."""
    node_id=str(graph_node.get("id") or "")
    source_id=str(observation.get("source_id") or "")
    source_record_id=str(observation.get("source_record_id") or "")
    access_state=str(observation.get("source_access_state") or "AVAILABLE")

    base={
        "node_id":node_id,
        "source_id":source_id,
        "source_record_id":source_record_id,
        "source_url":str(observation.get("source_url") or ""),
        "retrieved_at":str(observation.get("retrieved_at") or ""),
        "corruption_inference":False,
    }

    if access_state != "AVAILABLE":
        return {
            **base,
            "status":"COVERAGE_GAP",
            "basis":f"source_access_state:{access_state}",
            "auto_attach":False,
            "attached_attributes":{},
        }

    node_ids=_usccs(graph_node)
    source_ids=_usccs(observation)
    shared=sorted(node_ids & source_ids)
    if shared:
        return {
            **base,
            "status":"ENRICHED_EXACT_STABLE_ID",
            "basis":f"exact_stable_id:{shared[0]}",
            "auto_attach":True,
            "attached_attributes":_safe_attributes(
                observation.get("attributes") or {}
            ),
        }

    left_name=normalize_org_name(str(graph_node.get("name") or ""))
    right_name=normalize_org_name(str(observation.get("name") or ""))
    if left_name and right_name and left_name == right_name:
        if node_ids and source_ids and node_ids.isdisjoint(source_ids):
            status="STABLE_ID_CONFLICT"
            basis="exact_normalized_name_with_disjoint_stable_ids"
        else:
            status="REVIEW_CANDIDATE"
            basis="exact_normalized_name_without_shared_stable_id"
        return {
            **base,
            "status":status,
            "basis":basis,
            "auto_attach":False,
            "attached_attributes":{},
        }

    return {
        **base,
        "status":"NO_MATCH",
        "basis":"no_exact_stable_id_or_exact_name_match",
        "auto_attach":False,
        "attached_attributes":{},
    }


def enrich_nodes(
    graph_nodes: Iterable[Mapping[str, Any]],
    observations: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Apply second-source observations without name-based auto-merging."""
    nodes=[dict(x) for x in graph_nodes]
    obs=[dict(x) for x in observations]
    decisions=[]

    for record in obs:
        access=str(record.get("source_access_state") or "AVAILABLE")
        if access != "AVAILABLE":
            # A source-level inaccessible observation is retained once rather
            # than spuriously compared to every graph node.
            decisions.append({
                "node_id":"",
                "source_id":str(record.get("source_id") or ""),
                "source_record_id":str(record.get("source_record_id") or ""),
                "source_url":str(record.get("source_url") or ""),
                "retrieved_at":str(record.get("retrieved_at") or ""),
                "status":"COVERAGE_GAP",
                "basis":f"source_access_state:{access}",
                "auto_attach":False,
                "attached_attributes":{},
                "corruption_inference":False,
            })
            continue

        candidates=[]
        record_ids=_usccs(record)
        record_name=normalize_org_name(str(record.get("name") or ""))

        for node in nodes:
            node_ids=_usccs(node)
            node_name=normalize_org_name(str(node.get("name") or ""))
            if record_ids & node_ids or (record_name and record_name == node_name):
                candidates.append(enrich_one(node,record))

        if not candidates:
            decisions.append({
                "node_id":"",
                "source_id":str(record.get("source_id") or ""),
                "source_record_id":str(record.get("source_record_id") or ""),
                "source_url":str(record.get("source_url") or ""),
                "retrieved_at":str(record.get("retrieved_at") or ""),
                "status":"UNLINKED_SOURCE_RECORD",
                "basis":"no_graph_identity_candidate",
                "auto_attach":False,
                "attached_attributes":{},
                "corruption_inference":False,
            })
        else:
            decisions.extend(candidates)

    counts={}
    for d in decisions:
        counts[d["status"]]=counts.get(d["status"],0)+1

    return {
        "schema_version":1,
        "graph_nodes":len(nodes),
        "source_observations":len(obs),
        "decision_count":len(decisions),
        "status_counts":counts,
        "decisions":decisions,
        "auto_attached_count":sum(bool(x["auto_attach"]) for x in decisions),
        "review_required_count":sum(
            x["status"] in {"REVIEW_CANDIDATE","STABLE_ID_CONFLICT"}
            for x in decisions
        ),
        "coverage_gap_count":sum(
            x["status"]=="COVERAGE_GAP" for x in decisions
        ),
        "corruption_inference":False,
        "interpretation":(
            "Cross-source identity/enrichment audit only. Exact CN-USCC equality "
            "permits factual attribute attachment; name-only matches require "
            "review; inaccessible sources remain coverage gaps. No integrity "
            "or corruption inference is produced."
        ),
    }
