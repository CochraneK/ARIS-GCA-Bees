"""Evidence Graph construction for OpenIntegrity.

The graph is intentionally descriptive. It records entities, relationships,
sources, and detector findings. It never stores a guilt/corruption edge.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from open_integrity_agent import Finding, IntegrityCase


def build_evidence_graph(
    case: IntegrityCase,
    findings: Iterable[Finding | Mapping[str, Any]] = (),
) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    node_index: dict[str, dict[str, Any]] = {}

    def add_node(node_id: str, node_type: str, **attrs: Any) -> None:
        if not node_id:
            return
        existing = node_index.get(node_id)
        if existing is None:
            node = {"id": node_id, "type": node_type, **attrs}
            node_index[node_id] = node
            nodes.append(node)
            return
        # Enrich a placeholder or earlier sparse node without silently
        # replacing non-empty provenance already recorded.
        if existing.get("type") in {"unresolved_entity", "supplier"} and node_type not in {
            "unresolved_entity",
            "supplier",
        }:
            existing["type"] = node_type
        for key, value in attrs.items():
            if value not in (None, "", [], ()) and existing.get(key) in (None, "", [], ()):
                existing[key] = value

    c = case.contract
    if case.subject_id != c.contract_id:
        add_node(case.subject_id, "case_subject")
        edges.append({
            "source": case.subject_id,
            "target": c.contract_id,
            "type": "CONTAINS",
        })

    add_node(
        c.contract_id,
        "contract",
        authority_id=c.authority_id,
        award_date=c.award_date.isoformat() if c.award_date else None,
        award_value=c.award_value,
        procurement_method=c.procurement_method,
        jurisdiction=c.jurisdiction,
    )
    add_node(c.authority_id, "authority")
    edges.append({
        "source": c.authority_id,
        "target": c.contract_id,
        "type": "ISSUED_OR_AWARDED",
    })

    for supplier_id in c.supplier_ids:
        entity = case.entities.get(supplier_id)
        add_node(
            supplier_id,
            entity.entity_type if entity else "supplier",
            name=entity.name if entity else None,
            stable_ids=list(entity.stable_ids) if entity else [],
        )
        edges.append({
            "source": c.contract_id,
            "target": supplier_id,
            "type": "AWARDED_TO",
        })

    for entity_id, entity in case.entities.items():
        add_node(
            entity_id,
            entity.entity_type,
            name=entity.name,
            stable_ids=list(entity.stable_ids),
            incorporated_on=(
                entity.incorporated_on.isoformat()
                if entity.incorporated_on else None
            ),
            public_office_from=(
                entity.public_office_from.isoformat()
                if entity.public_office_from else None
            ),
            public_office_to=(
                entity.public_office_to.isoformat()
                if entity.public_office_to else None
            ),
        )

    for i, rel in enumerate(case.relations):
        add_node(rel.left_id, "unresolved_entity")
        add_node(rel.right_id, "unresolved_entity")
        edges.append({
            "id": f"relation:{i}",
            "source": rel.left_id,
            "target": rel.right_id,
            "type": rel.relation,
            "valid_from": rel.valid_from.isoformat() if rel.valid_from else None,
            "valid_to": rel.valid_to.isoformat() if rel.valid_to else None,
            "identity_strength": rel.identity_strength,
            "source_record_id": rel.source_ref.record_id,
            "source_name": rel.source_ref.source_name,
        })

    for i, deb in enumerate(case.debarments):
        node_id = f"debarment:{deb.source_ref.source_name}:{deb.source_ref.record_id}"
        add_node(
            node_id,
            "debarment",
            imposed_from=deb.imposed_from.isoformat(),
            imposed_to=deb.imposed_to.isoformat() if deb.imposed_to else None,
            source_name=deb.source_ref.source_name,
            source_record_id=deb.source_ref.record_id,
        )
        add_node(deb.entity_id, "unresolved_entity")
        edges.append({
            "id": f"debarment-edge:{i}",
            "source": deb.entity_id,
            "target": node_id,
            "type": "SANCTIONED_OR_DEBARRED",
        })

    for finding in findings:
        if isinstance(finding, Finding):
            payload = finding.to_dict()
        else:
            payload = dict(finding)
        fid = str(payload.get("finding_id") or "")
        if not fid:
            continue
        add_node(
            fid,
            "detector_finding",
            detector_id=payload.get("detector_id"),
            family=payload.get("family"),
            status=payload.get("status"),
            evidence_class=payload.get("evidence_class"),
            claim=payload.get("claim"),
            dependency_group=payload.get("dependency_group"),
            corruption_inference=False,
        )
        edges.append({
            "source": fid,
            "target": case.subject_id,
            "type": "ABOUT",
        })

    return {
        "subject_id": case.subject_id,
        "nodes": nodes,
        "edges": edges,
        "corruption_inference": False,
    }
