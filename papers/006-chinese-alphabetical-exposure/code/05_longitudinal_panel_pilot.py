#!/usr/bin/env python3
"""ARIS4C006 longitudinal panel feasibility pilot.

Seed high-confidence China-affiliated authors from recent DOI/Crossref-aligned
works, then inspect prior OpenAlex work histories. Aggregate outputs only.
No substantive surname-effect model is estimated.
"""
from __future__ import annotations
import argparse, json, os, re, time, unicodedata, urllib.parse, urllib.request
from pathlib import Path

OA_WORKS="https://api.openalex.org/works"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.5 longitudinal-panel-feasibility"
FIELDS={20:"Economics",26:"Mathematics",14:"Business",32:"Psychology",27:"Medicine",22:"Engineering"}
TOKEN_RE=re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ'’-]+")

def get(url,retries=4):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(.5*(i+1))

def norm(s):
    s=unicodedata.normalize("NFKD",s or "")
    s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub("[^a-z]","",s.lower())

def toks(s): return [norm(x) for x in TOKEN_RE.findall(s or "") if norm(x)]

def is_cn(a):
    return any(i.get("country_code")=="CN" for i in (a.get("institutions") or [])) or "CN" in (a.get("countries") or [])

def oa_params(extra):
    if os.getenv("OPENALEX_API_KEY"):extra["api_key"]=os.environ["OPENALEX_API_KEY"]
    if os.getenv("OPENALEX_MAILTO"):extra["mailto"]=os.environ["OPENALEX_MAILTO"]
    return extra

def seed_works(fid,year,target):
    sample_n=min(100,max(target*3,target+30));seed=int(f"{year}{fid:02d}7")
    p=oa_params({"filter":",".join(["authorships.institutions.country_code:CN",f"topics.field.id:{fid}",f"from_publication_date:{year}-01-01",f"to_publication_date:{year}-12-31"]),"select":"id,doi,authorships","sample":sample_n,"seed":seed,"per-page":sample_n})
    d=get(OA_WORKS+"?"+urllib.parse.urlencode(p))
    if not d:return
    n=0
    for w in d.get("results") or []:
        if w.get("doi") and len(w.get("authorships") or [])>=2:
            yield w;n+=1
            if n>=target:break

def crossref(doi_url):
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def valid_cn_authors(w,cr):
    oa=w.get("authorships") or [];ca=cr.get("author") or []
    if len(oa)!=len(ca) or not oa:return []
    out=[]
    for o,c in zip(oa,ca):
        if not is_cn(o):continue
        fam=norm(c.get("family"))
        raw=o.get("raw_author_name") or (o.get("author") or {}).get("display_name") or ""
        if fam and fam in toks(raw):
            aid=(o.get("author") or {}).get("id")
            if aid:out.append((aid,bool((o.get("author") or {}).get("orcid"))))
    return out

def author_history(aid,start,end,maxworks):
    cur="*";rows=[]
    while len(rows)<maxworks:
        p=oa_params({"filter":",".join([f"author.id:{aid}",f"from_publication_date:{start}-01-01",f"to_publication_date:{end}-12-31"]),"select":"id,publication_year,primary_location,topics,authorships","per-page":100,"cursor":cur})
        d=get(OA_WORKS+"?"+urllib.parse.urlencode(p))
        if not d:break
        rr=d.get("results") or []
        if not rr:break
        rows.extend(rr[:maxworks-len(rows)])
        cur=(d.get("meta") or {}).get("next_cursor")
        if not cur:break
    years=set();sources=set();fields=set();cn_years=set();multi=0
    for w in rows:
        y=w.get("publication_year")
        if y:years.add(y)
        src=((w.get("primary_location") or {}).get("source") or {}).get("id")
        if src:sources.add(src)
        tops=w.get("topics") or []
        if tops:
            fld=((tops[0].get("field") or {}).get("id"))
            if fld:fields.add(fld)
        auths=w.get("authorships") or []
        if len(auths)>=2:multi+=1
        for aa in auths:
            if ((aa.get("author") or {}).get("id")==aid) and is_cn(aa) and y:cn_years.add(y)
    return {"works":len(rows),"years":len(years),"sources":len(sources),"fields":len(fields),"cn_years":len(cn_years),"multi_works":multi}

def quantile(v,q):
    if not v:return None
    s=sorted(v);i=(len(s)-1)*q;lo=int(i);hi=min(lo+1,len(s)-1);f=i-lo
    return s[lo]*(1-f)+s[hi]*f

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--seed-year",type=int,default=2024);ap.add_argument("--seed-per-field",type=int,default=20);ap.add_argument("--max-authors",type=int,default=120);ap.add_argument("--start",type=int,default=2015);ap.add_argument("--end",type=int,default=2024);ap.add_argument("--max-works",type=int,default=300);ap.add_argument("--outdir",default="data/pilot/longitudinal");a=ap.parse_args()
    seeds={};crossref_ok=0
    for fid in FIELDS:
        for w in seed_works(fid,a.seed_year,a.seed_per_field):
            cr=crossref(w["doi"])
            if not cr:continue
            crossref_ok+=1
            for aid,orc in valid_cn_authors(w,cr):
                seeds.setdefault(aid,orc)
                if len(seeds)>=a.max_authors:break
            if len(seeds)>=a.max_authors:break
        if len(seeds)>=a.max_authors:break
    hist=[]
    for k,(aid,orc) in enumerate(list(seeds.items())[:a.max_authors],1):
        h=author_history(aid,a.start,a.end,a.max_works);h["orcid_seed"]=orc;hist.append(h)
        if k%20==0:print("authors",k)
    count=lambda pred:sum(bool(pred(x)) for x in hist)
    summary={"script":"05_longitudinal_panel_pilot.py","sampling":"OpenAlex reproducible random sample+seed for recent seed works","confirmatory_use_allowed":False,"seed_year":a.seed_year,"history_window":[a.start,a.end],"seed_authors":len(hist),"seed_authors_with_orcid":sum(x["orcid_seed"] for x in hist),"crossref_seed_records_found":crossref_ok,"authors_2plus_active_years":count(lambda x:x["years"]>=2),"authors_5plus_active_years":count(lambda x:x["years"]>=5),"authors_10plus_multiworks":count(lambda x:x["multi_works"]>=10),"authors_2plus_sources":count(lambda x:x["sources"]>=2),"authors_3plus_sources":count(lambda x:x["sources"]>=3),"authors_2plus_fields":count(lambda x:x["fields"]>=2),"authors_cn_affiliation_3plus_years":count(lambda x:x["cn_years"]>=3),"median_works":quantile([x["works"] for x in hist],.5),"median_active_years":quantile([x["years"] for x in hist],.5),"median_sources":quantile([x["sources"] for x in hist],.5),"median_fields":quantile([x["fields"] for x in hist],.5),"p25_active_years":quantile([x["years"] for x in hist],.25),"p75_active_years":quantile([x["years"] for x in hist],.75),"privacy":"aggregate only; no names, author IDs, ORCIDs or work IDs persisted"}
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True);(out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
