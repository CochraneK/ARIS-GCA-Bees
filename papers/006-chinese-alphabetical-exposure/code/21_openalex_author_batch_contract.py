#!/usr/bin/env python3
"""ARIS4C006 — OpenAlex author-ID batch canonicalization contract probe.

Outcome-blind engineering probe:
1) randomly sample one eligible China-affiliated paper,
2) collect 2-10 embedded author IDs,
3) try /authors?filter=openalex:A...|A...&per_page=100,
4) verify returned author entities cover the requested resolvable IDs.
"""
from __future__ import annotations
import json, os, urllib.parse, urllib.request
from pathlib import Path

UA="ARIS4C006/0.21 author-batch-contract"
OA="https://api.openalex.org"

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def short(s): return (s or "").rstrip("/").split("/")[-1]

def main():
    params={
        "filter":"authorships.institutions.country_code:CN,type:article|conference-paper,publication_year:2024",
        "select":"id,authorships",
        "sample":1,
        "seed":600621,
        "per_page":1,
    }
    if os.getenv("OPENALEX_API_KEY"): params["api_key"]=os.environ["OPENALEX_API_KEY"]
    work=get(OA+"/works?"+urllib.parse.urlencode(params))["results"][0]
    ids=[]
    for a in work.get("authorships") or []:
        aid=short((a.get("author") or {}).get("id"))
        if aid and aid not in ids: ids.append(aid)
        if len(ids)>=10: break
    if len(ids)<2: raise RuntimeError("probe work did not yield >=2 author IDs")

    filt="|".join(ids)
    p={"filter":"openalex:"+filt,"per_page":100,"select":"id,orcid,display_name"}
    if os.getenv("OPENALEX_API_KEY"): p["api_key"]=os.environ["OPENALEX_API_KEY"]
    url=OA+"/authors?"+urllib.parse.urlencode(p,safe="|:")
    status="unknown";returned=[]
    try:
        d=get(url)
        returned=[short(x.get("id")) for x in d.get("results") or []]
        status="supported"
    except Exception as e:
        status="unsupported"
        err=repr(e)
    else:
        err=""

    # Singleton ground truth, and canonical ids returned from raw ids.
    singleton=[]
    for aid in ids:
        try:
            d=get(OA+"/authors/"+urllib.parse.quote(aid,safe=""))
            singleton.append({"raw":aid,"canonical":short(d.get("id"))})
        except Exception:
            singleton.append({"raw":aid,"canonical":""})
    canonical_requested=sorted({x["canonical"] for x in singleton if x["canonical"]})
    returned_set=sorted(set(returned))
    exact_cover=(status=="supported" and set(canonical_requested).issubset(set(returned_set)))

    manifest={
        "script":"21_openalex_author_batch_contract.py",
        "real_outcome_data_used":False,
        "requested_raw_ids":len(ids),
        "singleton_resolved":sum(bool(x["canonical"]) for x in singleton),
        "batch_filter":"openalex:<pipe-separated IDs>",
        "batch_status":status,
        "batch_returned":len(returned),
        "batch_covers_singleton_canonical_ids":exact_cover,
        "error_if_any":err,
        "decision":"Use batch openalex-ID canonicalization only if batch_status=supported and coverage=true; otherwise use singleton fallback."
    }
    out=Path("data/pilot/openalex_author_batch_contract");out.mkdir(parents=True,exist_ok=True)
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2))
    # Probe itself does not fail merely because undocumented batching is unsupported.
    if status=="supported" and not exact_cover:
        raise RuntimeError("batch endpoint responded but failed canonical coverage contract")

if __name__=="__main__":
    main()
