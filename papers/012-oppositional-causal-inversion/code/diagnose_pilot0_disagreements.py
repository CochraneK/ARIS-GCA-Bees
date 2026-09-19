#!/usr/bin/env python3
"""Classify ARIS4C012 Pilot-0B disagreement cells without changing raw v1 reliability.

This is a diagnostic instrument. It does not fill adjudicated_value and must not
be used to post-hoc recode Pilot 0B as a successful reliability result.
"""
from __future__ import annotations
import argparse,csv,json,re
from collections import Counter,defaultdict
from pathlib import Path

BINARY_FIELDS={"opposition_valid","oci_candidate","actor_switch","level_switch","time_switch","construct_switch","environment_switch","feedback","nonlinearity","selection_filtering","power_asymmetry"}

def norm(x:str)->str:
    return re.sub(r"\\s+"," ",re.sub(r"[_;/\\-]+"," ",(x or "").strip().lower())).strip()

def classify(row):
    a,b=norm(row["coder_a"]),norm(row["coder_b"])
    field=row["field"]
    if a==b:
        return "lexical_token_vocabulary_mismatch","separator/case normalization makes labels identical","no"
    if field=="evidence_mode":
        if (("meta analysis" in a and b=="meta analysis") or ("systematic review" in a and b=="review") or (a=="protocol" and b=="review")):
            return "lexical_token_vocabulary_mismatch","evidence-mode labels use different granularity/tokens","no"
        return "source_metadata_disagreement","evidence-mode classification differs beyond token formatting","yes"
    if field=="evidence_tier":
        return "source_metadata_disagreement","evidence-tier systems/granularity differ and require source-level crosswalk","yes"
    if field=="primary_mechanism":
        if b=="none":
            return "genuine_conceptual_disagreement","Coder A assigns a mechanism while Coder B assigns none","yes"
        return "schema_category_overlap","free-text/index/mechanism label is being forced against a different controlled mechanism family","yes"
    if field in BINARY_FIELDS:
        return "genuine_conceptual_disagreement","construct/index-switch judgment differs","yes"
    if field=="causal_claim_strength":
        def coarse(x):
            if re.search(r"high|strong",x): return "strong"
            if "moderate" in x: return "moderate"
            if "weak" in x: return "weak"
            if re.search(r"none|not yet evidential",x): return "none"
            return ""
        if coarse(a) and coarse(a)==b:
            return "lexical_token_vocabulary_mismatch","free-text causal-strength wording collapses to Coder B ordinal token","no"
        return "genuine_conceptual_disagreement","causal-strength judgment differs after coarse ordinal crosswalk","yes"
    if field=="result_support":
        def coarse(x):
            if x in {"support","conditional support","mechanism support","support for neighboring theory"}: return "yes"
            if "counterevidence" in x or x=="no": return "no"
            if "mixed" in x or "conditional" in x: return "partial"
            if "not tested" in x: return "not tested"
            return ""
        if coarse(a) and coarse(a)==b:
            return "lexical_token_vocabulary_mismatch","free-text result label maps directly to Coder B coarse token","no"
        return "genuine_conceptual_disagreement","result-direction judgment differs after coarse crosswalk","yes"
    return "genuine_conceptual_disagreement","non-equivalent labels require adjudication","yes"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--summary",required=True)
    a=ap.parse_args()
    with open(a.input,encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
    for r in rows:
        t,why,review=classify(r)
        r["diagnosis_type"]=t; r["diagnosis_rationale"]=why; r["source_review_required"]=review
    fields=list(rows[0].keys())
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    with open(a.output,"w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    counts=Counter(r["diagnosis_type"] for r in rows)
    by=defaultdict(Counter)
    for r in rows: by[r["field"]][r["diagnosis_type"]]+=1
    summary={"classification":"PILOT0B_DISAGREEMENT_DIAGNOSIS","raw_input":a.input,"disagreement_cells":len(rows),"diagnosis_counts":dict(counts),"by_field":{k:dict(v) for k,v in by.items()},"adjudication_status":"DIAGNOSTIC_ONLY_NOT_RECODED","raw_v1_reliability_immutable":True}
    Path(a.summary).write_text(json.dumps(summary,indent=2)+"\\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
