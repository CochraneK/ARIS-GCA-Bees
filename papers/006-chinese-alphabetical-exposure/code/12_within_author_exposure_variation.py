#!/usr/bin/env python3
"""ARIS4C006 — within-author exposure-variation feasibility pilot.

Outcome-blind. Estimates field × prior-3-year excess alphabetization from
independent random work samples, then assigns those field-level exposures to a
random seed of China-affiliated authors' publication histories to measure
within-author variation. No surname rank or career outcome is used.
"""
from __future__ import annotations
import argparse,csv,json,math,os,re,statistics,time,unicodedata,urllib.parse,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

OA_WORKS="https://api.openalex.org/works"
OA_AUTHORS="https://api.openalex.org/authors/"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.12 within-author-exposure-variation"
FIELDS={20:"Economics",26:"Mathematics",14:"Business",32:"Psychology",27:"Medicine",22:"Engineering"}

def get(url,retries=4):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=60) as r:return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(.5*(i+1))

def norm(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z0-9]","",s)

def chance(keys):
    n=len(keys);num=1
    for m in Counter(keys).values():num*=math.factorial(m)
    return num/math.factorial(n)

def excess(rows):
    den=sum(x[1] for x in rows)
    return sum(x[0] for x in rows)/den if den else None

def cr(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def sample_field_window(fid,start,end,target,seed):
    want=min(100,max(target*3,target+40))
    p={"filter":",".join(["authorships.institutions.country_code:CN",f"primary_topic.field.id:{fid}",f"from_publication_date:{start}-01-01",f"to_publication_date:{end}-12-31"]),"select":"id,doi,authorships","sample":want,"seed":seed,"per_page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA_WORKS+"?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def estimate_field_exposure(fid,target_year,n):
    start,end=target_year-3,target_year-1
    works=sample_field_window(fid,start,end,n,int(f"{target_year}{fid:02d}12"))
    vals=[]
    for w in works:
        c=cr(w.get("doi"))
        if not c:continue
        oa=w.get("authorships") or [];ca=c.get("author") or []
        if not oa or len(oa)!=len(ca):continue
        keys=[norm(x.get("family")) for x in ca]
        if any(not k for k in keys):continue
        ia=int(all(keys[i]<=keys[i+1] for i in range(len(keys)-1)));pc=chance(keys)
        vals.append((ia-pc,1-pc))
        time.sleep(.02)
    return excess(vals),len(vals)

def is_cn(a):
    return any(i.get("country_code")=="CN" for i in (a.get("institutions") or [])) or "CN" in (a.get("countries") or [])

def short(s):return (s or "").rstrip("/").split("/")[-1]

def canonical_author(aid,cache):
    if aid not in cache:
        d=get(OA_AUTHORS+urllib.parse.quote(short(aid),safe=""))
        cache[aid]=short((d or {}).get("id")) if d else ""
        time.sleep(.02)
    return cache[aid]

def seed_authors(year,target):
    p={"filter":",".join(["authorships.institutions.country_code:CN",f"from_publication_date:{year}-01-01",f"to_publication_date:{year}-12-31"]),"select":"id,authorships","sample":100,"seed":year*100+12,"per_page":100}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA_WORKS+"?"+urllib.parse.urlencode(p));out=[];seen=set();cache={}
    for w in (d or {}).get("results") or []:
        for a in w.get("authorships") or []:
            if not is_cn(a):continue
            aid=(a.get("author") or {}).get("id")
            if not aid:continue
            cid=canonical_author(aid,cache)
            if cid and cid not in seen:
                seen.add(cid);out.append(cid)
                if len(out)>=target:return out
    return out

def author_works(aid,start,end,maxworks=300):
    cur="*";out=[]
    while cur and len(out)<maxworks:
        p={"filter":",".join([f"author.id:{aid}",f"from_publication_date:{start}-01-01",f"to_publication_date:{end}-12-31"]),"select":"id,publication_year,primary_topic,authorships","per_page":100,"cursor":cur}
        if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
        d=get(OA_WORKS+"?"+urllib.parse.urlencode(p))
        if not d:break
        rr=d.get("results") or []
        if not rr:break
        out.extend(rr[:maxworks-len(out)])
        cur=(d.get("meta") or {}).get("next_cursor")
    return out

def primary_field(w):
    fld=(w.get("primary_topic") or {}).get("field") or {}
    raw=fld.get("id")
    if raw is None:return None
    try:return int(str(raw).rstrip("/").split("/")[-1])
    except:return None

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--start",type=int,default=2018);ap.add_argument("--end",type=int,default=2024);ap.add_argument("--per-field-window",type=int,default=30);ap.add_argument("--authors",type=int,default=100);ap.add_argument("--outdir",default="data/pilot/exposure_switch");a=ap.parse_args()
    exposure={};erows=[]
    for year in range(a.start,a.end+1):
        for fid,fname in FIELDS.items():
            e,n=estimate_field_exposure(fid,year,a.per_field_window);exposure[(year,fid)]=e
            erows.append({"target_year":year,"field_id":fid,"field_name":fname,"prior3_excess_alpha":e,"valid_convention_works":n})
            print("EXPOSURE",json.dumps(erows[-1],ensure_ascii=False))
    seeds=seed_authors(a.end,a.authors);stats=[]
    for k,aid in enumerate(seeds,1):
        byyear=defaultdict(list)
        for w in author_works(aid,a.start,a.end):
            y=w.get("publication_year");fid=primary_field(w)
            if y in range(a.start,a.end+1) and fid in FIELDS and exposure.get((y,fid)) is not None:
                byyear[y].append(exposure[(y,fid)])
        annual=[sum(v)/len(v) for y,v in sorted(byyear.items()) if v]
        if annual:
            rng=max(annual)-min(annual)
            sd=statistics.pstdev(annual) if len(annual)>1 else 0.0
        else:rng=sd=0.0
        stats.append({"years":len(annual),"range":rng,"sd":sd})
        if k%20==0:print("AUTHORS",k)
    elig=[x for x in stats if x["years"]>=3]
    def med(vals):
        return statistics.median(vals) if vals else None
    manifest={"script":"12_within_author_exposure_variation.py","confirmatory_use_allowed":False,"exposure_level":"primary_topic field × prior-3-year window","seed_authors":len(stats),"authors_with_3plus_defined_exposure_years":len(elig),"share_3plus_defined_years":len(elig)/len(stats) if stats else None,"median_within_author_range_3plus":med([x["range"] for x in elig]),"median_within_author_sd_3plus":med([x["sd"] for x in elig]),"share_range_ge_0_05_3plus":sum(x["range"]>=.05 for x in elig)/len(elig) if elig else None,"share_range_ge_0_10_3plus":sum(x["range"]>=.10 for x in elig)/len(elig) if elig else None,"prospective_gate":"Retain a within-author longitudinal exposure design only if >=50 authors have >=3 exposure-defined years and >=50% of that subset has within-author exposure range >=0.05. Otherwise longitudinal within-author exposure is secondary/exploratory.","privacy":"aggregate only; no author IDs or names persisted"}
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    with (out/"field_window_exposure.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(erows[0]));w.writeheader();w.writerows(erows)
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
