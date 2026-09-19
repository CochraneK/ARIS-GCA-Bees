#!/usr/bin/env python3
"""Draw the frozen fresh ARIS4C012 v2 validation sample deterministically."""
from __future__ import annotations
import argparse,csv
from pathlib import Path

SEED="ARIS4C012-V2-A2B2-20260919"
PER_STRATUM=5

def norm(x):
    return " ".join((x or "").strip().lower().split())

def fnv1a(text):
    h=0x811c9dc5
    for b in text.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xffffffff
    return h

def read(path):
    with open(path,encoding="utf-8",newline="") as f: return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--frame",required=True)
    ap.add_argument("--pilot0",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    frame=read(a.frame); old=read(a.pilot0)
    used={norm(r.get("stable_id")) for r in old if norm(r.get("stable_id"))}
    used|={norm(r.get("title")) for r in old if norm(r.get("title"))}
    fresh=[r for r in frame if norm(r.get("doi")) not in used and norm(r.get("provider_id")) not in used and norm(r.get("title")) not in used]
    strata=sorted({r["stratum"] for r in fresh})
    out=[]
    for s in strata:
        pool=[]
        for r in fresh:
            if r["stratum"]!=s: continue
            key=r.get("dedupe_key") or r.get("doi") or r.get("title")
            rr=dict(r); rr["draw_score"]=str(fnv1a(SEED+"|"+key)); pool.append(rr)
        pool.sort(key=lambda r:(int(r["draw_score"]),int(r["selection_rank"])))
        out.extend(pool[:PER_STRATUM])
    out.sort(key=lambda r:(r["stratum"],int(r["draw_score"])))
    for i,r in enumerate(out,1): r["sample_id"]=f"V2{i:02d}"
    fields=["sample_id","stratum","query_index","query","provider","provider_id","doi","title","year","type","venue_or_topic","cited_by_count","landing_url","dedupe_key","draw_score"]
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    with open(a.output,"w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows({k:r.get(k,"") for k in fields} for r in out)
    assert len(out)==30
    assert all(sum(1 for r in out if r["stratum"]==s)==5 for s in strata)
if __name__=="__main__": main()
