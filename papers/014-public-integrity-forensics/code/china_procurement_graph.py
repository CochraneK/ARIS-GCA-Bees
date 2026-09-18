"""Procurement graph projection for normalized CCGP notices.

This graph is source-local by design. Buyer/supplier names do not become global
entities merely because the same string appears elsewhere. Cross-source merging
must pass the normal OpenIntegrity identity-resolution layer.

Final awards and ranked candidates use different edge types.
"""

from __future__ import annotations

from hashlib import sha256
from typing import Any

from china_ccgp_detail import CCGPAwardNotice


def _local_id(source_url: str, role: str, name: str) -> str:
    digest = sha256(f"{source_url}|{role}|{name}".encode("utf-8")).hexdigest()[:20]
    return f"cn-ccgp-local:{role}:{digest}"


def ccgp_notice_graph(notice: CCGPAwardNotice) -> dict[str, Any]:
    project_key = notice.project_id or notice.html_sha256[:20]
    project_id = f"cn-ccgp-project:{project_key}"

    nodes: list[dict[str, Any]] = [
        {
            "id": project_id,
            "type": "procurement_project",
            "project_id": notice.project_id,
            "project_name": notice.project_name,
            "published_at": notice.published_at,
            "source_url": notice.source_url,
            "source_sha256": notice.html_sha256,
        }
    ]
    edges: list[dict[str, Any]] = []
    node_ids = {project_id}

    def add_node(payload: dict[str, Any]) -> None:
        if payload["id"] not in node_ids:
            nodes.append(payload)
            node_ids.add(payload["id"])

    if notice.buyer_name:
        buyer_id = _local_id(notice.source_url, "buyer", notice.buyer_name)
        add_node(
            {
                "id": buyer_id,
                "type": notice.buyer_institution_type,
                "name": notice.buyer_name,
                "identity_scope": "source_local_name",
                "stable_ids": [],
            }
        )
        edges.append(
            {
                "source": buyer_id,
                "target": project_id,
                "type": "BUYER_OF",
                "source_url": notice.source_url,
            }
        )

    if notice.procurement_agency_name:
        agency_id = _local_id(
            notice.source_url,
            "procurement_agency",
            notice.procurement_agency_name,
        )
        add_node(
            {
                "id": agency_id,
                "type": "procurement_agency",
                "name": notice.procurement_agency_name,
                "identity_scope": "source_local_name",
                "stable_ids": [],
            }
        )
        edges.append(
            {
                "source": agency_id,
                "target": project_id,
                "type": "PROCUREMENT_AGENT_FOR",
                "source_url": notice.source_url,
            }
        )

    for lot in notice.lots:
        if lot.supplier_uscc:
            supplier_id = f"cn-uscc:{lot.supplier_uscc}"
            identity_scope = "stable_id"
            stable_ids = [f"CN-USCC:{lot.supplier_uscc}"]
        else:
            supplier_id = _local_id(
                notice.source_url,
                f"supplier:{lot.lot_index}",
                lot.supplier_name,
            )
            identity_scope = "source_local_name"
            stable_ids = []

        add_node(
            {
                "id": supplier_id,
                "type": "supplier",
                "name": lot.supplier_name,
                "identity_scope": identity_scope,
                "stable_ids": stable_ids,
            }
        )

        edge: dict[str, Any] = {
            "source": project_id,
            "target": supplier_id,
            "source_url": notice.source_url,
            "lot_index": lot.lot_index,
            "package_name": lot.package_name,
            "award_value_yuan": lot.award_value_yuan,
            "award_value_raw": lot.award_value_raw,
            "pricing_basis": lot.pricing_basis,
        }
        if lot.result_status == "candidate":
            edge["type"] = "HAS_RANKED_CANDIDATE"
            edge["candidate_rank"] = lot.candidate_rank
        else:
            edge["type"] = "AWARDED_TO"
        edges.append(edge)

    return {
        "subject_id": project_id,
        "nodes": nodes,
        "edges": edges,
        "source_coverage": ["procurement_award_detail"],
        "identity_resolution_required": True,
        "corruption_inference": False,
    }


def graph_summary(graph: dict[str, Any]) -> dict[str, Any]:
    edges = graph.get("edges", [])
    return {
        "nodes": len(graph.get("nodes", [])),
        "edges": len(edges),
        "final_award_edges": sum(x.get("type") == "AWARDED_TO" for x in edges),
        "candidate_edges": sum(
            x.get("type") == "HAS_RANKED_CANDIDATE" for x in edges
        ),
        "identity_resolution_required": bool(
            graph.get("identity_resolution_required")
        ),
        "corruption_inference": False,
    }
