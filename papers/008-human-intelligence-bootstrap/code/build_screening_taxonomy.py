"""Build and audit the ARIS4C008 screening pool taxonomy.

The script queries Open Tree of Life TNRS with approximate matching disabled.
It prefers a unique non-synonym self match. Special cases are documented in
data/screening_taxonomy_overrides_v0.csv.

A missing OpenTree match is NOT treated as an invalid biological taxon:
Serracutisoma proximum is a known current combination absent from OpenTree 3.7
and has an explicit manual legacy-OTT crosswalk.
"""
from __future__ import annotations
import csv, json, urllib.request
from pathlib import Path

TNRS="https://api.opentreeoflife.org/v3/tnrs/match_names"

def post(payload):
    req=urllib.request.Request(TNRS,data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=120) as r:
        return json.loads(r.read().decode())

def main():
    base=Path(__file__).resolve().parents[1]
    pool=list(csv.DictReader(open(base/"data"/"screening_pool_expanded_v1.csv",encoding="utf-8-sig")))
    overrides={r["query_name"]:r for r in csv.DictReader(open(base/"data"/"screening_taxonomy_overrides_v0.csv",encoding="utf-8-sig"))}
    names=[r["scientific_name"] for r in pool]
    tn=post({"names":names,"context_name":"Animals","do_approximate_matching":False})
    out=[]
    for q in tn["results"]:
        name=q["name"]; ms=q.get("matches",[])
        self_non_syn=[m for m in ms if not m.get("is_synonym",False) and m["taxon"].get("name")==name]
        if len(self_non_syn)==1:
            m=self_non_syn[0]; t=m["taxon"]; status="clean_self"
        elif name in overrides:
            ov=overrides[name]
            out.append({"query_name":name,"resolved_name":ov["opentree_name"],"ott_id":ov["ott_id"],
                        "rank":ov["opentree_rank"],"resolution_status":ov["resolution_action"],
                        "analysis_rule":ov["analysis_rule"],"n_tnrs_matches":len(ms)})
            continue
        elif len(ms)==1:
            m=ms[0]; t=m["taxon"]; status="single_nonself"
        else:
            raise RuntimeError(f"Unresolved TNRS case: {name} / {len(ms)} matches")
        out.append({"query_name":name,"resolved_name":t.get("name",""),"ott_id":t.get("ott_id",""),
                    "rank":t.get("rank",""),"resolution_status":status,
                    "analysis_rule":"exact_species_terminal" if t.get("rank")=="species" else "review_rank",
                    "n_tnrs_matches":len(ms)})
    fields=["query_name","resolved_name","ott_id","rank","resolution_status","analysis_rule","n_tnrs_matches"]
    with open(base/"data"/"screening_pool_taxonomy_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    print("n",len(out),"taxonomy",tn.get("taxonomy"))

if __name__=="__main__":
    main()
