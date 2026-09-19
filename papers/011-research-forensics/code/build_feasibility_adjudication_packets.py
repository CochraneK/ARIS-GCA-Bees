#!/usr/bin/env python3
"""Split the blinded feasibility frame into manager-only adjudication packets.

The 80-record feasibility frame is design-affecting and already excluded from
final confirmatory performance reuse. This builder creates:
1) manager-only issue/adjudication packets containing post-publication outcome
   provenance needed to determine issue family and required artifact role;
2) manager-only acquisition packets containing the outcome cutoff needed to
   search for a pre-outcome artifact;
3) a public-safe aggregate summary.

No detector-visible Track-A manifest is produced here.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_FRAME=ROOT/"data"/"results"/"confirmatory_feasibility_frame_v0.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build(frame: dict) -> tuple[list[dict],list[dict],dict]:
    rows=list(frame.get("rows") or [])
    if frame.get("state")!="FEASIBILITY_ONLY_NOT_CONFIRMATORY":
        raise ValueError("Expected a feasibility-only frame")

    manager=[]
    acquisition=[]
    seen=set()

    for row in rows:
        fid=str(row.get("feasibility_id") or "").strip()
        doi=str(row.get("target_doi") or "").strip().lower()
        if not fid or not doi:
            raise ValueError("Every row requires feasibility_id and target_doi")
        if fid in seen:
            raise ValueError(f"Duplicate feasibility_id: {fid}")
        seen.add(fid)

        manager.append({
            "feasibility_id":fid,
            "target_doi":doi,
            "notice_or_source_doi":str(row.get("notice_or_source_doi") or "").strip().lower(),
            "update_type":str(row.get("update_type") or "").strip().lower(),
            "outcome_date":str(row.get("outcome_date") or "").strip(),
            "assertion_source":str(row.get("assertion_source") or "").strip(),
            "relation_label":str(row.get("relation_label") or "").strip(),
            "source_work_title":str(row.get("source_work_title") or "").strip(),
            "target_title_current":str(row.get("target_title_current") or "").strip(),
            "target_title_has_status_marker":bool(row.get("target_title_has_status_marker")),
            "issue_family":"UNADJUDICATED",
            "issue_description":"UNADJUDICATED",
            "ground_truth_tier":"UNADJUDICATED",
            "required_artifact_role":"UNADJUDICATED",
            "content_detectability":"UNADJUDICATED",
            "adjudication_evidence_url":"",
            "adjudication_notes":"",
            "detector_visible":False,
            "manager_only":True,
        })

        acquisition.append({
            "feasibility_id":fid,
            "target_doi":doi,
            "target_published":str(row.get("target_published") or "").strip(),
            "pre_outcome_cutoff_exclusive":str(row.get("outcome_date") or "").strip(),
            "target_title_current":str(row.get("target_title_current") or "").strip(),
            "target_title_has_status_marker":bool(row.get("target_title_has_status_marker")),
            "crossref_has_fulltext_link":bool(row.get("crossref_has_fulltext_link")),
            "required_artifact_role":"UNADJUDICATED",
            "artifact_state":"UNASSESSED",
            "artifact_url":"",
            "artifact_capture_date":"",
            "artifact_sha256":"",
            "identity_verified":False,
            "historical_equivalence_verified":False,
            "detector_visible":False,
            "manager_only":True,
        })

    summary={
        "analysis":"ARIS4C011 feasibility manager-packet build",
        "state":"MANAGER_ONLY_PRE_ADJUDICATION",
        "input_state":frame.get("state"),
        "records":len(rows),
        "update_type_counts":{},
        "current_title_status_markers":sum(
            bool(r.get("target_title_has_status_marker")) for r in rows
        ),
        "crossref_fulltext_link_available":sum(
            bool(r.get("crossref_has_fulltext_link")) for r in rows
        ),
        "issue_family_adjudicated":0,
        "required_artifact_role_adjudicated":0,
        "artifact_state_assessed":0,
        "detector_visible_records":0,
        "claim_boundary":(
            "These packets are manager/acquisition surfaces only. Outcome/update "
            "metadata must never be passed to Track A detectors. UNADJUDICATED "
            "or UNASSESSED values are not negatives and must not be imputed."
        ),
    }
    for r in rows:
        k=str(r.get("update_type") or "unknown")
        summary["update_type_counts"][k]=summary["update_type_counts"].get(k,0)+1

    return manager,acquisition,summary


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("No rows to write")
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--frame",type=Path,default=DEFAULT_FRAME)
    p.add_argument("--manager-output",type=Path,required=True)
    p.add_argument("--acquisition-output",type=Path,required=True)
    p.add_argument("--summary-output",type=Path,required=True)
    a=p.parse_args()

    raw=a.frame.read_text(encoding="utf-8")
    frame=json.loads(raw)
    manager,acquisition,summary=build(frame)
    summary["input_sha256"]=sha256_text(raw)

    write_csv(a.manager_output,manager)
    write_csv(a.acquisition_output,acquisition)
    a.summary_output.parent.mkdir(parents=True,exist_ok=True)
    a.summary_output.write_text(
        json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
