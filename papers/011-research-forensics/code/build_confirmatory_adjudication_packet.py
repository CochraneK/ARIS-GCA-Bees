#!/usr/bin/env python3
"""Build a manager-only adjudication packet from the frozen feasibility frame.

The packet projects only label-side provenance needed to adjudicate issue
family, ground-truth tier, and required historical artifact role. It contains
no detector output, anomaly score, review priority, or artifact qualification
result. Blank adjudication fields must be filled before artifact acquisition.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

SOURCE_FIELDS=[
    "feasibility_id","calendar_stratum","target_doi","notice_or_source_doi",
    "update_type","outcome_date","assertion_source","relation_label",
    "source_work_title","source_work_date","target_title_current",
    "target_title_has_status_marker","target_published","target_year",
    "target_journal","target_type",
]
ADJUDICATION_FIELDS=[
    "issue_family_codes","ground_truth_tier","required_artifact_roles",
    "content_detectability","adjudication_state","adjudication_notes",
]
FIELDS=SOURCE_FIELDS+ADJUDICATION_FIELDS

ISSUE_FAMILY_VOCAB=[
    "statistical_reporting",
    "table_numerical_reporting",
    "data_fabrication_falsification",
    "image_integrity",
    "plagiarism_text_duplication",
    "paper_mill",
    "authorship_peer_review",
    "citation_reference",
    "registration_ethics_provenance",
    "methods_results_coherence",
    "other_unclear",
]
GROUND_TRUTH_TIERS=["GT-A","GT-B","GT-C","GT-D","GT-E"]
ARTIFACT_ROLE_VOCAB=[
    "body_text","table","figure_image","references","raw_data","supplement",
    "registration_protocol","metadata_timeline","cross_source_reference",
    "none_content_detectable","other",
]
CONTENT_DETECTABILITY_VOCAB=[
    "CONTENT_ASSESSABLE","PROCESS_ONLY","MIXED","UNCLEAR",
]
FORBIDDEN_SOURCE_FIELDS=[
    "detector_output","review_priority","artifact_state","confirmatory_eligible",
    "finding_count","flag_count","anomaly_score","model_score",
]

def sha256(path:Path)->str:
    h=hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def build(frame:dict)->tuple[list[dict],dict]:
    if frame.get("state")!="FEASIBILITY_ONLY_NOT_CONFIRMATORY":
        raise ValueError("input is not the frozen feasibility-only frame")
    rows=frame.get("rows") or []
    out=[]
    for source in rows:
        if source.get("detector_output_visible") is not False:
            raise ValueError("feasibility row does not preserve detector blinding")
        projected={k:source.get(k,"") for k in SOURCE_FIELDS}
        projected.update({
            "issue_family_codes":"",
            "ground_truth_tier":"",
            "required_artifact_roles":"",
            "content_detectability":"",
            "adjudication_state":"UNASSESSED",
            "adjudication_notes":"",
        })
        out.append(projected)
    ids=[str(x["feasibility_id"]) for x in out]
    if len(ids)!=len(set(ids)):
        raise ValueError("duplicate feasibility_id")
    return out,{
        "schema_version":"0.1.0",
        "state":"MANAGER_ONLY_UNADJUDICATED",
        "row_count":len(out),
        "packet_visibility":"LABEL_SIDE_MANAGER_ONLY_NEVER_TRACK_A_INPUT",
        "source_frame_state":frame["state"],
        "source_frame_candidate_count":frame["candidate_count"],
        "selection_used_detector_output":False,
        "adjudication_fields":ADJUDICATION_FIELDS,
        "issue_family_vocab":ISSUE_FAMILY_VOCAB,
        "ground_truth_tier_vocab":GROUND_TRUTH_TIERS,
        "artifact_role_vocab":ARTIFACT_ROLE_VOCAB,
        "content_detectability_vocab":CONTENT_DETECTABILITY_VOCAB,
        "multi_value_separator":";",
        "forbidden_input_fields":FORBIDDEN_SOURCE_FIELDS,
        "instructions":[
            "Adjudicate from notice/source evidence, never detector output.",
            "issue_family_codes and required_artifact_roles may contain semicolon-separated controlled values.",
            "Use none_content_detectable when the official issue is process-only and no manuscript artifact can directly represent the labelled issue.",
            "Do not run detector scoring on this packet or expose adjudicated label-side fields to Track A.",
        ],
    }

def write_csv(path:Path,rows:list[dict])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--csv-output",type=Path,required=True)
    p.add_argument("--manifest-output",type=Path,required=True)
    a=p.parse_args()
    frame=json.loads(a.input.read_text(encoding="utf-8"))
    rows,manifest=build(frame)
    write_csv(a.csv_output,rows)
    manifest["source_frame_file"]=str(a.input.relative_to(ROOT)) if a.input.is_relative_to(ROOT) else a.input.name
    manifest["source_frame_sha256"]=sha256(a.input)
    manifest["packet_csv_sha256"]=sha256(a.csv_output)
    a.manifest_output.parent.mkdir(parents=True,exist_ok=True)
    a.manifest_output.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "state":manifest["state"],
        "row_count":manifest["row_count"],
        "packet_csv_sha256":manifest["packet_csv_sha256"],
        "selection_used_detector_output":False,
    },indent=2))

if __name__=="__main__":
    main()
