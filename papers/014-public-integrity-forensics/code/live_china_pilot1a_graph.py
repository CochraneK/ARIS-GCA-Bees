"""China Pilot 1A: bounded live multi-notice procurement graph.

Purpose: test graph union and conservative organization joinability, not risk.
Stable CN-USCC nodes can collapse deterministically. Name-only matches remain
REVIEW_CANDIDATE and are never auto-merged. Output is aggregate-only.
"""
from __future__ import annotations

from collections import Counter,defaultdict
from datetime import datetime
import json
from pathlib import Path

from china_ccgp import discover_live,fetch_text
from china_ccgp_detail import parse_ccgp_award_detail
from china_entity_resolution import resolve_cross_source
from china_procurement_graph import ccgp_notice_graph

FIXED_USCC_URL=(
    "https://www.ccgp.gov.cn/cggg/dfgg/zbgg/202609/"
    "t20260914_27325491.htm"
)

def main():
    retrieved=datetime.now().astimezone().isoformat()
    discovery=discover_live(per_page_limit=8)
    urls=[]
    for result in discovery:
        for lead in result.leads:
            if lead.url not in urls:
                urls.append(lead.url)
    urls=urls[:12]
    if FIXED_USCC_URL not in urls:
        urls.append(FIXED_USCC_URL)

    graphs=[]
    failures=[]
    for url in urls:
        try:
            html=fetch_text(url)
            notice=parse_ccgp_award_detail(
                html,source_url=url,retrieved_at=retrieved
            )
            graphs.append(ccgp_notice_graph(notice))
        except Exception as exc:
            failures.append({
                "source_url":url,
                "error_class":type(exc).__name__,
            })

    all_nodes=[]
    all_edges=[]
    for g in graphs:
        all_nodes.extend(g["nodes"])
        all_edges.extend(g["edges"])

    # Preserve manifestations for review-candidate discovery, then union exact
    # graph IDs. Same CN-USCC node ID is already deterministic across notices.
    decisions=resolve_cross_source(all_nodes)
    unique_nodes={}
    node_manifestations=Counter()
    for n in all_nodes:
        unique_nodes.setdefault(n["id"],n)
        node_manifestations[n["id"]]+=1

    stable_supplier_ids=[
        nid for nid,n in unique_nodes.items()
        if n.get("type")=="supplier" and str(nid).startswith("cn-uscc:")
    ]
    local_supplier_ids=[
        nid for nid,n in unique_nodes.items()
        if n.get("type")=="supplier" and not str(nid).startswith("cn-uscc:")
    ]
    repeated_stable=[
        nid for nid in stable_supplier_ids if node_manifestations[nid]>1
    ]

    resolution_counts=Counter(x["relation"] for x in decisions)
    payload={
        "pilot":"CHINA_PILOT_1A_PROCUREMENT_GRAPH_JOINABILITY",
        "retrieved_at":retrieved,
        "requested_notice_urls":len(urls),
        "graphs_built":len(graphs),
        "fetch_or_parse_failures":len(failures),
        "graph":{
            "raw_node_manifestations":len(all_nodes),
            "unique_node_ids":len(unique_nodes),
            "edges":len(all_edges),
            "projects":sum(n.get("type")=="procurement_project" for n in unique_nodes.values()),
            "suppliers_with_stable_uscc":len(stable_supplier_ids),
            "suppliers_name_only_source_local":len(local_supplier_ids),
            "stable_supplier_ids_reused_across_notices":len(repeated_stable),
            "final_award_edges":sum(e.get("type")=="AWARDED_TO" for e in all_edges),
            "ranked_candidate_edges":sum(e.get("type")=="HAS_RANKED_CANDIDATE" for e in all_edges),
        },
        "cross_manifestation_resolution":{
            "same_org_exact_stable_id_decisions":resolution_counts["SAME_ORG"],
            "name_only_review_candidate_decisions":resolution_counts["REVIEW_CANDIDATE"],
            "automatic_name_only_merges":0,
        },
        "coverage_failures":[x["error_class"] for x in failures],
        "corruption_inference":False,
        "risk_score_computed":False,
        "named_risk_findings_emitted":False,
        "interpretation":(
            "Engineering/joinability pilot only. Stable-ID reuse and name-only "
            "review candidates are identity-resolution facts, not integrity signals."
        ),
    }
    Path("china_pilot1a_graph_summary.json").write_text(
        json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )
    print(json.dumps(payload,ensure_ascii=False,indent=2))
    if not graphs:
        raise SystemExit("No CCGP graph could be built")
    if len(stable_supplier_ids)<1:
        raise SystemExit("Known USCC regression page did not yield stable supplier nodes")

if __name__=="__main__":
    main()
