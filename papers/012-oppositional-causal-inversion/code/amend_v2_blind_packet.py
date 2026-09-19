#!/usr/bin/env python3
"""ARIS4C012 pre-coding evidence-availability Amendment 01.

Preserves the first frozen blind packet and enriches only records that were
BIBLIOGRAPHIC_ONLY, using record DOI/landing-page public metadata. No labels,
Pilot-0 material, disagreement diagnoses, or sample-selection strata are read.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from materialize_v2_blind_packet import (
    build_response_csv,canonical_jsonl,cap_words,fetch_landing_description,
    sha256_bytes,sha256_file,
)

def read_jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--packet",required=True)
    ap.add_argument("--prior-freeze",required=True)
    ap.add_argument("--schema",required=True)
    ap.add_argument("--template",required=True)
    ap.add_argument("--out-dir",required=True)
    ap.add_argument("--freeze-dir",required=True)
    a=ap.parse_args()
    packet=Path(a.packet);prior_path=Path(a.prior_freeze);schema=Path(a.schema);template=Path(a.template)
    out=Path(a.out_dir);freezes=Path(a.freeze_dir)
    common_path=freezes/"V2_BLIND_PACKET_AMENDMENT_01_FREEZE.json"
    if common_path.exists():
        print(f"Amendment already frozen: {common_path}; refusing to overwrite.")
        return
    prior=json.loads(prior_path.read_text(encoding="utf-8"))
    if prior.get("classification")!="V2_BLIND_PACKET_FREEZE":
        raise AssertionError("prior freeze classification mismatch")
    if sha256_file(packet)!=prior["evidence_packet_sha256"]:
        raise AssertionError("prior evidence packet hash mismatch")
    records=read_jsonl(packet)
    if len(records)!=30:raise AssertionError("prior packet must contain 30 rows")

    recovered=[];attempted=[]
    for r in records:
        if r.get("evidence_state")!="BIBLIOGRAPHIC_ONLY":continue
        urls=[]
        doi=(r.get("doi") or "").strip()
        if doi:urls.append("https://doi.org/"+doi)
        landing=(r.get("landing_url") or "").strip()
        if landing and landing not in urls:urls.append(landing)
        attempted.append(r["sample_id"])
        for url in urls:
            text,key,final=fetch_landing_description(url)
            if not text:continue
            text,truncated,n=cap_words(text)
            r["evidence_text"]=text
            r["evidence_state"]="SOURCE_DESCRIPTION_EXCERPT"
            r["evidence_source"]="landing_meta:"+key
            r["evidence_source_url"]=final or url
            r["landing_url"]=final or landing or url
            r["evidence_word_count"]=n
            r["evidence_truncated"]=truncated
            recovered.append(r["sample_id"])
            break

    out.mkdir(parents=True,exist_ok=True);freezes.mkdir(parents=True,exist_ok=True)
    packet_bytes=canonical_jsonl(records)
    packet_out=out/"common_evidence_packet_amendment_01.jsonl";packet_out.write_bytes(packet_bytes)
    response=build_response_csv(template,records)
    a2=out/"A2_response_amendment_01.csv";b2=out/"B2_response_amendment_01.csv"
    a2.write_bytes(response);b2.write_bytes(response)
    packet_sha=sha256_bytes(packet_bytes);schema_sha=sha256_file(schema);response_sha=sha256_bytes(response)
    bundle_sha=sha256_bytes((packet_sha+"\n"+schema_sha+"\n"+response_sha+"\n").encode())
    counts={}
    for r in records:counts[r["evidence_state"]]=counts.get(r["evidence_state"],0)+1
    missing=[r["sample_id"] for r in records if r["evidence_state"]=="BIBLIOGRAPHIC_ONLY"]
    now=datetime.now(timezone.utc).isoformat()
    report={
      "classification":"V2_BLIND_EVIDENCE_AMENDMENT_01",
      "frozen_at":now,
      "prior_bundle_sha256":prior["bundle_sha256"],
      "attempted_ids":attempted,
      "recovered_ids":recovered,
      "remaining_bibliographic_only_ids":missing,
      "evidence_state_counts":counts,
      "sample_changed":False,
      "labels_or_adjudication_inspected":False,
      "ready_for_independent_coding":not missing,
      "next_if_not_ready":"Apply a separately frozen, outcome-blind deterministic same-stratum evidence-availability replacement rule; do not start A2/B2.",
    }
    report_path=out/"amendment_01_report.json";report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    common={
      "classification":"V2_BLIND_PACKET_AMENDMENT_01_FREEZE",
      "frozen_at":now,
      "supersedes_bundle_sha256":prior["bundle_sha256"],
      "amendment_scope":"evidence availability only; sample and schema unchanged; no labels inspected",
      "evidence_packet":str(packet_out),"evidence_packet_sha256":packet_sha,
      "schema_sha256":schema_sha,"response_form_sha256":response_sha,"bundle_sha256":bundle_sha,
      "sample_count":30,"byte_identical_coder_inputs":True,
      "report":str(report_path),"ready_for_independent_coding":not missing,
    }
    common_path.write_text(json.dumps(common,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for coder,path in (("A2",a2),("B2",b2)):
        d={
          "classification":"V2_INDEPENDENT_CODER_INPUT_AMENDMENT_01_FREEZE","coder":coder,"frozen_at":now,
          "supersedes_bundle_sha256":prior["bundle_sha256"],"evidence_packet_sha256":packet_sha,
          "schema_sha256":schema_sha,"response_form":str(path),"response_form_sha256":sha256_file(path),
          "bundle_sha256":bundle_sha,"must_remain_blind_to_other_coder":True,
          "must_remain_blind_to_pilot0_labels_and_adjudication":True,
          "ready_for_independent_coding":not missing,
        }
        (freezes/f"{coder}_INPUT_AMENDMENT_01_FREEZE.json").write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
    assert sha256_file(a2)==sha256_file(b2)==response_sha
    print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=="__main__":main()
