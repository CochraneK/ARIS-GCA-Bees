#!/usr/bin/env python3
"""ARIS4C006 — targeted source-context exposure pilot.

Identify high-volume sources independently using OpenAlex group_by counts,
then estimate lagged excess alphabetical authorship from reproducible random
samples inside those source × field × lag-window contexts.

Measurement only; no focal surname rank or career outcome is used.
"""
from __future__ import annotations
import argparse, csv, json, math, os, re, time, unicodedata, urllib.parse, urllib.request, zlib
from collections import Counter
from pathlib import Path

OA="https://api.openalex.org/works"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.8 source-context-pilot"
FIELDS={20:"Economics",26:"Mathematics",14:"Business",32:"Psychology",27:"Medicine",22:"Engineering"}

def get(url,retries=4):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(.5*(i+1))

def sortkey(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z0-9]","",s)

def short_id(s):
    return (s or "").rstrip("/").split("/")[-1]

def base_filter(fid,start,end):
    return ",".join([
        "authorships.institutions.country_code:CN",
        f"topics.field.id:{fid}",
        f"from_publication_date:{start}-01-01",
        f"to_publication_date:{end}-12-31",
    ])

def group_sources(fid,start,end,max_groups=2000):
    cursor="*";groups=[]
    while cursor and len(groups)<max_groups:
        p={"filter":base_filter(fid,start,end),"group_by":"primary_location.source.id","per_page":200,"cursor":cursor}
        if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
        d=get(OA+"?"+urllib.parse.urlencode(p))
        if not d:break
        for g in d.get("group_by") or []:
            key=g.get("key")
            if key and key not in {"unknown","-111"}:
                groups.append({"source_id":short_id(key),"source_name":g.get("key_display_name") or "","count":int(g.get("count") or 0)})
        cursor=(d.get("meta") or {}).get("next_cursor")
        if not cursor:break
    return sorted(groups,key=lambda x:(-x["count"],x["source_id"]))

def sample_source(fid,start,end,source_id,target):
    want=min(100,max(target*2,target+30))
    seed=zlib.crc32(f"{fid}|{start}|{end}|{source_id}|83".encode()) & 0x7fffffff
    p={"filter":base_filter(fid,start,end)+f",primary_location.source.id:{source_id}","select":"id,doi,authorships,primary_location","sample":want,"seed":seed,"per_page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA+"?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def cr_record(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def chance(keys):
    n=len(keys);num=1
    for m in Counter(keys).values():num*=math.factorial(m)
    return num/math.factorial(n)

def measure(w,cr):
    oa=w.get("authorships") or [];ca=cr.get("author") or []
    if not oa or len(oa)!=len(ca):return None
    keys=[sortkey(a.get("family")) for a in ca]
    if any(not k for k in keys):return None
    ia=int(all(keys[i]<=keys[i+1] for i in range(len(keys)-1)))
    pc=chance(keys)
    return {"team":len(keys),"num":ia-pc,"den":1-pc}

def excess(rows):
    d=sum(x["den"] for x in rows)
    return sum(x["num"] for x in rows)/d if d else None

def q(vals,p):
    if not vals:return None
    s=sorted(vals);x=(len(s)-1)*p;lo=int(x);hi=min(lo+1,len(s)-1);f=x-lo
    return s[lo]*(1-f)+s[hi]*f

def pearson(a,b):
    if len(a)<2:return None
    ma=sum(a)/len(a);mb=sum(b)/len(b)
    num=sum((x-ma)*(y-mb) for x,y in zip(a,b))
    da=sum((x-ma)**2 for x in a);db=sum((y-mb)**2 for y in b)
    return num/(da*db)**.5 if da and db else None

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--target-years",default="2020,2024")
    ap.add_argument("--top-sources",type=int,default=2)
    ap.add_argument("--per-source",type=int,default=40)
    ap.add_argument("--min-window-output",type=int,default=20)
    ap.add_argument("--outdir",default="data/pilot/source_context")
    a=ap.parse_args()
    target_years=[int(x) for x in a.target_years.split(",")]
    rows=[]
    for target in target_years:
        start,end=target-3,target-1
        for fid,fname in FIELDS.items():
            candidates=[g for g in group_sources(fid,start,end) if g["count"]>=a.min_window_output][:a.top_sources]
            for g in candidates:
                works=sample_source(fid,start,end,g["source_id"],a.per_source)
                valid=[];doi_n=cr_n=0
                for w in works:
                    if w.get("doi"):
                        doi_n+=1
                        cr=cr_record(w["doi"])
                        if cr:
                            cr_n+=1
                            m=measure(w,cr)
                            if m:valid.append(m)
                    time.sleep(.035)
                v3=[x for x in valid if x["team"]>=3]
                row={"field_id":fid,"field_name":fname,"target_year":target,"lag_start":start,"lag_end":end,"source_id":g["source_id"],"source_name":g["source_name"],"source_window_output_count":g["count"],"sampled_multi_author_works":len(works),"doi_works":doi_n,"crossref_found":cr_n,"valid_order_works":len(valid),"valid_3plus_works":len(v3),"excess_alpha":excess(valid),"excess_alpha_3plus":excess(v3)}
                rows.append(row);print(json.dumps(row,ensure_ascii=False))
    out=Path(a.outdir);write_csv(out/"source_context_exposure.csv",rows)
    valid_scores=[r["excess_alpha"] for r in rows if r["excess_alpha"] is not None and r["valid_order_works"]>=20]
    valid3=[r["excess_alpha_3plus"] for r in rows if r["excess_alpha_3plus"] is not None and r["valid_3plus_works"]>=15]
    # Adjacent-window reliability where the same source is top-volume in both target windows.
    keyed={(r["field_id"],r["source_id"],r["target_year"]):r for r in rows}
    pairs=[]
    if len(target_years)>=2:
        y0,y1=target_years[0],target_years[-1]
        for fid in FIELDS:
            sources={r["source_id"] for r in rows if r["field_id"]==fid}
            for sid in sources:
                a0=keyed.get((fid,sid,y0));a1=keyed.get((fid,sid,y1))
                if a0 and a1 and a0["excess_alpha"] is not None and a1["excess_alpha"] is not None:
                    pairs.append((a0["excess_alpha"],a1["excess_alpha"]))
    manifest={"script":"08_source_context_pilot.py","confirmatory_use_allowed":False,"selection_rule":"Top sources selected by OpenAlex lag-window publication count only, before convention score is calculated","target_years":target_years,"lag_years":3,"top_sources_per_field":a.top_sources,"per_source_requested":a.per_source,"source_contexts":len(rows),"source_contexts_with_20plus_valid":sum(r["valid_order_works"]>=20 for r in rows),"source_contexts_with_15plus_valid_3plus":sum(r["valid_3plus_works"]>=15 for r in rows),"excess_q10":q(valid_scores,.1),"excess_median":q(valid_scores,.5),"excess_q90":q(valid_scores,.9),"excess_3plus_q10":q(valid3,.1),"excess_3plus_median":q(valid3,.5),"excess_3plus_q90":q(valid3,.9),"same_source_cross_window_pairs":len(pairs),"same_source_cross_window_pearson":pearson([x for x,_ in pairs],[y for _,y in pairs]),"privacy":"context aggregates only; no personal identifiers persisted"}
    out.mkdir(parents=True,exist_ok=True);(out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
