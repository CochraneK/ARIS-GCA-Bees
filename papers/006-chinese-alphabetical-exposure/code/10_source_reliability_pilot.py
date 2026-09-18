#!/usr/bin/env python3
"""ARIS4C006 — split-half reliability for source-context alphabetization.

Outcome-blind measurement pilot. Source contexts are selected by publication
volume only; convention works are sampled reproducibly and deterministically
split by OpenAlex work-ID hash before excess-alphabetization is estimated.
"""
from __future__ import annotations
import argparse, csv, json, math, os, re, time, unicodedata, urllib.parse, urllib.request, zlib
from collections import Counter
from pathlib import Path

OA="https://api.openalex.org/works"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.10 source-reliability-pilot"
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

def short_id(s): return (s or "").rstrip("/").split("/")[-1]

def sortkey(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z0-9]","",s)

def filt(fid,start,end):
    return ",".join(["authorships.institutions.country_code:CN",f"topics.field.id:{fid}",f"from_publication_date:{start}-01-01",f"to_publication_date:{end}-12-31"])

def group_sources(fid,start,end,max_groups=2000):
    cursor="*";out=[]
    while cursor and len(out)<max_groups:
        p={"filter":filt(fid,start,end),"group_by":"primary_location.source.id","per_page":200,"cursor":cursor}
        if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
        d=get(OA+"?"+urllib.parse.urlencode(p))
        if not d:break
        for g in d.get("group_by") or []:
            key=g.get("key")
            if key and key not in {"unknown","-111"}:
                out.append({"source_id":short_id(key),"source_name":g.get("key_display_name") or "","count":int(g.get("count") or 0)})
        cursor=(d.get("meta") or {}).get("next_cursor")
        if not cursor:break
    return sorted(out,key=lambda x:(-x["count"],x["source_id"]))

def sample(fid,start,end,sid,target):
    want=min(100,max(target*2,target+30));seed=zlib.crc32(f"{fid}|{start}|{end}|{sid}|83".encode())&0x7fffffff
    p={"filter":filt(fid,start,end)+f",primary_location.source.id:{sid}","select":"id,doi,authorships","sample":want,"seed":seed,"per_page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA+"?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def cr(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def chance(keys):
    n=len(keys);num=1
    for m in Counter(keys).values():num*=math.factorial(m)
    return num/math.factorial(n)

def measure(w,c):
    oa=w.get("authorships") or [];ca=c.get("author") or []
    if not oa or len(oa)!=len(ca):return None
    keys=[sortkey(x.get("family")) for x in ca]
    if any(not k for k in keys):return None
    ia=int(all(keys[i]<=keys[i+1] for i in range(len(keys)-1)));pc=chance(keys)
    return {"work_id":w.get("id") or "","team":len(keys),"num":ia-pc,"den":1-pc}

def ex(rows):
    d=sum(x["den"] for x in rows)
    return sum(x["num"] for x in rows)/d if d else None

def pearson(a,b):
    if len(a)<2:return None
    ma=sum(a)/len(a);mb=sum(b)/len(b)
    num=sum((x-ma)*(y-mb) for x,y in zip(a,b))
    da=sum((x-ma)**2 for x in a);db=sum((y-mb)**2 for y in b)
    return num/(da*db)**.5 if da and db else None

def rank(v):
    order=sorted(range(len(v)),key=lambda i:v[i]);r=[0.0]*len(v);i=0
    while i<len(order):
        j=i
        while j+1<len(order) and v[order[j+1]]==v[order[i]]:j+=1
        avg=(i+j+2)/2
        for k in range(i,j+1):r[order[k]]=avg
        i=j+1
    return r

def spearman(a,b): return pearson(rank(a),rank(b)) if len(a)>=2 else None

def median(v):
    if not v:return None
    s=sorted(v);n=len(s);return s[n//2] if n%2 else (s[n//2-1]+s[n//2])/2

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--target-years",default="2020,2024");ap.add_argument("--top-sources",type=int,default=2);ap.add_argument("--per-source",type=int,default=40);ap.add_argument("--min-window-output",type=int,default=20);ap.add_argument("--min-half",type=int,default=12);ap.add_argument("--outdir",default="data/pilot/source_reliability");a=ap.parse_args()
    rows=[]
    for target in [int(x) for x in a.target_years.split(",")]:
        start,end=target-3,target-1
        for fid,fname in FIELDS.items():
            sources=[g for g in group_sources(fid,start,end) if g["count"]>=a.min_window_output][:a.top_sources]
            for g in sources:
                valid=[]
                for w in sample(fid,start,end,g["source_id"],a.per_source):
                    c=cr(w.get("doi"))
                    if c:
                        m=measure(w,c)
                        if m:valid.append(m)
                    time.sleep(.035)
                ha=[x for x in valid if (zlib.crc32(x["work_id"].encode())&1)==0]
                hb=[x for x in valid if (zlib.crc32(x["work_id"].encode())&1)==1]
                a3=[x for x in ha if x["team"]>=3];b3=[x for x in hb if x["team"]>=3]
                row={"field_id":fid,"field_name":fname,"target_year":target,"source_id":g["source_id"],"source_name":g["source_name"],"valid_n":len(valid),"half_a_n":len(ha),"half_b_n":len(hb),"half_a_excess":ex(ha),"half_b_excess":ex(hb),"half_abs_diff":abs(ex(ha)-ex(hb)) if ex(ha) is not None and ex(hb) is not None else None,"half_a_3plus_n":len(a3),"half_b_3plus_n":len(b3),"half_a_3plus_excess":ex(a3),"half_b_3plus_excess":ex(b3)}
                rows.append(row);print(json.dumps(row,ensure_ascii=False))
    eligible=[r for r in rows if r["half_a_n"]>=a.min_half and r["half_b_n"]>=a.min_half and r["half_a_excess"] is not None and r["half_b_excess"] is not None]
    aa=[r["half_a_excess"] for r in eligible];bb=[r["half_b_excess"] for r in eligible]
    eligible3=[r for r in rows if r["half_a_3plus_n"]>=7 and r["half_b_3plus_n"]>=7 and r["half_a_3plus_excess"] is not None and r["half_b_3plus_excess"] is not None]
    a3=[r["half_a_3plus_excess"] for r in eligible3];b3=[r["half_b_3plus_excess"] for r in eligible3]
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    with (out/"source_split_half.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    manifest={"script":"10_source_reliability_pilot.py","confirmatory_use_allowed":False,"split_rule":"CRC32 parity of OpenAlex work ID, fixed before scores","contexts_total":len(rows),"contexts_eligible_all":len(eligible),"split_half_pearson":pearson(aa,bb),"split_half_spearman":spearman(aa,bb),"median_half_abs_difference":median([r["half_abs_diff"] for r in eligible]),"contexts_eligible_3plus":len(eligible3),"split_half_3plus_pearson":pearson(a3,b3),"split_half_3plus_spearman":spearman(a3,b3),"privacy":"context aggregates only"}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
