#!/usr/bin/env python3
"""Aggregate ARIS4C004 work-review priority from rows to persons.

This reduces reviewer navigation cost. It does not decide whether any work
belongs to a focal person and does not change network release status.
"""
from __future__ import annotations
import argparse,csv,json
from collections import Counter,defaultdict
from pathlib import Path

def read(path):
    with path.open(encoding="utf-8-sig",newline="") as h:
        return list(csv.DictReader(h))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rows",type=Path,required=True)
    p.add_argument("--work-summary",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--summary-json",type=Path,required=True)
    a=p.parse_args()
    rows=read(a.rows)
    ws={r["person_id"]:r for r in read(a.work_summary)}
    by=defaultdict(list)
    for r in rows: by[r["person_id"]].append(r)
    out=[]
    for pid,rr in by.items():
        tiers=Counter(r["review_priority_tier"] for r in rr)
        signals=Counter()
        for r in rr:
            for sig in (r.get("priority_signals") or "").split(";"):
                if sig: signals[sig]+=1
        meta=ws.get(pid,{})
        max_score=max(int(r["review_priority_score"]) for r in rr)
        person_tier="P1" if tiers["P1"] else ("P2" if tiers["P2"] else "P3")
        out.append({
            "person_id":pid,
            "canonical_name":rr[0]["canonical_name"],
            "identity_status":rr[0]["identity_status"],
            "person_review_tier":person_tier,
            "max_row_priority_score":max_score,
            "sample_rows_n":len(rr),
            "P1_rows_n":tiers["P1"],
            "P2_rows_n":tiers["P2"],
            "P3_rows_n":tiers["P3"],
            "plausible_unique_works_n":meta.get("plausible_unique_works_n",""),
            "accepted_author_ids_n":meta.get("accepted_author_ids_n",""),
            "mechanical_min_works_met":meta.get("mechanical_min_works_met",""),
            "top_priority_signals":";".join(k for k,_ in signals.most_common(6)),
            "review_status":"PENDING",
            "machine_verdict":"NONE",
            "auto_release_allowed":"false",
            "auto_exclusion_allowed":"false",
        })
    out.sort(key=lambda r:(
        {"P1":0,"P2":1,"P3":2}[r["person_review_tier"]],
        -int(r["max_row_priority_score"]),
        -int(r["P1_rows_n"]),
        r["canonical_name"],
    ))
    for i,r in enumerate(out,1): r["person_review_rank"]=i
    fields=["person_review_rank"]+[k for k in out[0] if k!="person_review_rank"]
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(out)
    summary={
        "people":len(out),
        "person_tiers":dict(Counter(r["person_review_tier"] for r in out)),
        "P1_sample_rows":sum(int(r["P1_rows_n"]) for r in out if r["person_review_tier"]=="P1"),
        "machine_verdicts":dict(Counter(r["machine_verdict"] for r in out)),
        "auto_release_people":sum(r["auto_release_allowed"]=="true" for r in out),
        "auto_exclusion_people":sum(r["auto_exclusion_allowed"]=="true" for r in out),
        "mental_health_information_used":False,
        "interpretation":"Person-level review ordering only; independent evidence review is still required."
    }
    a.summary_json.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
