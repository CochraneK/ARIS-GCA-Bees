#!/usr/bin/env python3
"""Deterministic same-stratum evidence-availability replacement for ARIS4C012.

This is a pre-coding validation-sample amendment. Selection uses only the
frozen retrieval frame, original deterministic hash order, stratum, and
whether record-level evidence can be materialized. It never reads labels.
"""
from __future__ import annotations
import argparse,csv,json
from datetime import datetime,timezone
from pathlib import Path
from materialize_v2_blind_packet import (
    build_response_csv,canonical_jsonl,cap_words,evidence_for,
    fetch_landing_description,sha256_bytes,sha256_file,
)

SEED="ARIS4C012-V2-A2B2-20260919"

def fnv1a(text:str)->int:
    h=0x811c9dc5
    for b in text.encode("utf-8"):
        h ^= b; h=(h*0x01000193)&0xffffffff
    return h

def norm(x):return " ".join((x or "").strip().lower().split())

def read_csv(path):
    with open(path,encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def materialize(row,target_id):
    x=dict(row);x["sample_id"]=target_id
    e=evidence_for(x)
    if e["evidence_state"]!="BIBLIOGRAPHIC_ONLY":return e
    urls=[]
    doi=(x.get("doi") or "").strip()
    if doi:urls.append("https://doi.org/"+doi)
    landing=(x.get("landing_url") or "").strip()
    if landing and landing not in urls:urls.append(landing)
    for url in urls:
        text,key,final=fetch_landing_description(url)
        if not text:continue
        text,truncated,n=cap_words(text)
        e.update({
          "evidence_text":text,"evidence_state":"SOURCE_DESCRIPTION_EXCERPT",
          "evidence_source":"landing_meta:"+key,"evidence_source_url":final or url,
          "landing_url":final or url,"evidence_word_count":n,"evidence_truncated":truncated,
        })
        break
    return e

def esc_csv(path,rows,fields):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--frame",required=True)
    ap.add_argument("--pilot0",required=True)
    ap.add_argument("--sample",required=True)
    ap.add_argument("--packet",required=True)
    ap.add_argument("--prior-freeze",required=True)
    ap.add_argument("--amendment1-freeze",required=True)
    ap.add_argument("--schema",required=True)
    ap.add_argument("--template",required=True)
    ap.add_argument("--out-dir",required=True)
    ap.add_argument("--freeze-dir",required=True)
    a=ap.parse_args()

    out=Path(a.out_dir);freezes=Path(a.freeze_dir)
    final_freeze=freezes/"V2_BLIND_PACKET_AMENDMENT_02_FREEZE.json"
    if final_freeze.exists():
        print(f"Amendment 02 already frozen: {final_freeze}; refusing to overwrite.");return

    prior=json.loads(Path(a.prior_freeze).read_text(encoding="utf-8"))
    amend1=json.loads(Path(a.amendment1_freeze).read_text(encoding="utf-8"))
    if amend1.get("ready_for_independent_coding") is not False:
        raise AssertionError("Amendment 02 should run only after Amendment 01 failed to complete evidence")

    frame=read_csv(a.frame);pilot=read_csv(a.pilot0);sample=read_csv(a.sample);records=read_jsonl(a.packet)
    by_id={r["sample_id"]:r for r in records}
    missing=sorted(r["sample_id"] for r in records if r.get("evidence_state")=="BIBLIOGRAPHIC_ONLY")
    expected={"V215","V216","V219","V224","V225","V227"}
    if set(missing)!=expected:
        raise AssertionError(f"unexpected Amendment-02 target IDs: {missing}")

    sample_by_id={r["sample_id"]:r for r in sample}
    old_ids={norm(r.get("stable_id")) for r in pilot if norm(r.get("stable_id"))}
    old_ids|={norm(r.get("title")) for r in pilot if norm(r.get("title"))}
    fresh=[r for r in frame if norm(r.get("doi")) not in old_ids and norm(r.get("provider_id")) not in old_ids and norm(r.get("title")) not in old_ids]
    for r in fresh:
        key=r.get("dedupe_key") or r.get("doi") or r.get("title")
        r["_score"]=fnv1a(SEED+"|"+key)

    used={r.get("dedupe_key") for r in sample if r.get("dedupe_key")}
    attempts=[];mappings=[]
    for target in missing:
        old=sample_by_id[target];stratum=old["stratum"]
        pool=[r for r in fresh if r["stratum"]==stratum and r.get("dedupe_key") not in used]
        pool.sort(key=lambda r:(r["_score"],int(r.get("selection_rank") or 10**9)))
        accepted=None
        for cand in pool:
            key=cand.get("dedupe_key") or cand.get("doi") or cand.get("title")
            ev=materialize(cand,target)
            ok=ev["evidence_state"]!="BIBLIOGRAPHIC_ONLY"
            attempts.append({
              "target_sample_id":target,"stratum":stratum,"candidate_dedupe_key":key,
              "candidate_doi":cand.get("doi",""),"candidate_title":cand.get("title",""),
              "draw_score":cand["_score"],"evidence_state":ev["evidence_state"],
              "evidence_source":ev.get("evidence_source",""),"accepted":"yes" if ok else "no",
            })
            if ok:
                accepted=(cand,ev,key);break
        if accepted is None:
            continue
        cand,ev,key=accepted;used.add(cand.get("dedupe_key"))
        old_record=by_id[target]
        by_id[target]=ev
        mappings.append({
          "sample_id":target,"stratum":stratum,
          "old_doi":old_record.get("doi",""),"old_title":old_record.get("title",""),
          "new_doi":ev.get("doi",""),"new_title":ev.get("title",""),
          "new_dedupe_key":key,"new_draw_score":cand["_score"],
          "evidence_state":ev["evidence_state"],"evidence_source":ev.get("evidence_source",""),
        })

    final_records=[by_id[k] for k in sorted(by_id)]
    still=[r["sample_id"] for r in final_records if r["evidence_state"]=="BIBLIOGRAPHIC_ONLY"]
    out.mkdir(parents=True,exist_ok=True);freezes.mkdir(parents=True,exist_ok=True)
    attempt_fields=["target_sample_id","stratum","candidate_dedupe_key","candidate_doi","candidate_title","draw_score","evidence_state","evidence_source","accepted"]
    map_fields=["sample_id","stratum","old_doi","old_title","new_doi","new_title","new_dedupe_key","new_draw_score","evidence_state","evidence_source"]
    esc_csv(out/"replacement_attempt_log.csv",attempts,attempt_fields)
    esc_csv(out/"replacement_manifest.csv",mappings,map_fields)

    packet_bytes=canonical_jsonl(final_records);packet_path=out/"common_evidence_packet_amendment_02.jsonl";packet_path.write_bytes(packet_bytes)
    response=build_response_csv(Path(a.template),final_records)
    a2=out/"A2_response_amendment_02.csv";b2=out/"B2_response_amendment_02.csv";a2.write_bytes(response);b2.write_bytes(response)
    packet_sha=sha256_bytes(packet_bytes);schema_sha=sha256_file(Path(a.schema));response_sha=sha256_bytes(response)
    bundle_sha=sha256_bytes((packet_sha+"\n"+schema_sha+"\n"+response_sha+"\n").encode())
    counts={}
    for r in final_records:counts[r["evidence_state"]]=counts.get(r["evidence_state"],0)+1
    now=datetime.now(timezone.utc).isoformat();ready=not still and len(mappings)==len(missing)
    report={
      "classification":"V2_BLIND_EVIDENCE_AMENDMENT_02_DETERMINISTIC_REPLACEMENT",
      "frozen_at":now,"original_missing_ids":missing,"replacement_count":len(mappings),
      "remaining_bibliographic_only_ids":still,"evidence_state_counts":counts,
      "sample_changed":bool(mappings),"replacement_selection":"same-stratum fixed-hash order; first evidence-materializable candidate",
      "labels_or_adjudication_inspected":False,"pre_coding":True,"ready_for_independent_coding":ready,
    }
    (out/"amendment_02_report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    common={
      "classification":"V2_BLIND_PACKET_AMENDMENT_02_FREEZE","frozen_at":now,
      "supersedes_initial_bundle_sha256":prior["bundle_sha256"],
      "supersedes_amendment_01_bundle_sha256":amend1["bundle_sha256"],
      "amendment_scope":"deterministic same-stratum replacement based only on evidence availability before coding",
      "evidence_packet":str(packet_path),"evidence_packet_sha256":packet_sha,"schema_sha256":schema_sha,
      "response_form_sha256":response_sha,"bundle_sha256":bundle_sha,"sample_count":30,
      "replacement_count":len(mappings),"byte_identical_coder_inputs":True,
      "ready_for_independent_coding":ready,
      "replacement_manifest":str(out/"replacement_manifest.csv"),
      "replacement_attempt_log":str(out/"replacement_attempt_log.csv"),
    }
    final_freeze.write_text(json.dumps(common,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for coder,path in (("A2",a2),("B2",b2)):
        d={
          "classification":"V2_INDEPENDENT_CODER_INPUT_AMENDMENT_02_FREEZE","coder":coder,"frozen_at":now,
          "evidence_packet_sha256":packet_sha,"schema_sha256":schema_sha,"response_form":str(path),
          "response_form_sha256":sha256_file(path),"bundle_sha256":bundle_sha,
          "must_remain_blind_to_other_coder":True,"must_remain_blind_to_pilot0_labels_and_adjudication":True,
          "ready_for_independent_coding":ready,
        }
        (freezes/f"{coder}_INPUT_AMENDMENT_02_FREEZE.json").write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
    assert sha256_file(a2)==sha256_file(b2)==response_sha
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if not ready:raise SystemExit("Amendment 02 could not materialize all replacement slots")

if __name__=="__main__":main()
