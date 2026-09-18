#!/usr/bin/env python3
"""ARIS4C006 — annual coverage-only sweep, 2010–2025.

Outcome-blind measurement audit used to freeze the confirmatory time window.
Randomly samples China-affiliated multi-author works within each field/year and
reports DOI, Crossref, structured-family, and positional-reconciliation coverage.
No surname-effect or career outcome is computed.
"""
from __future__ import annotations
import argparse,csv,json,os,re,time,unicodedata,urllib.parse,urllib.request
from pathlib import Path

OA="https://api.openalex.org/works"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.11 annual-coverage-sweep"
FIELDS={20:"Economics",26:"Mathematics",14:"Business",32:"Psychology",27:"Medicine",22:"Engineering"}

def get(url,retries=4):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=60) as r:return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(.5*(i+1))

def sample(fid,year,target):
    want=min(100,max(target*3,target+40));seed=int(f"{year}{fid:02d}11")
    p={"filter":",".join(["authorships.institutions.country_code:CN",f"topics.field.id:{fid}",f"from_publication_date:{year}-01-01",f"to_publication_date:{year}-12-31"]),"select":"id,doi,authorships","sample":want,"seed":seed,"per_page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA+"?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def cr(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def norm(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]","",s.casefold())

def positional_support(w,c):
    oa=w.get("authorships") or [];ca=c.get("author") or []
    if not oa or len(oa)!=len(ca):return (False,False,False)
    allfam=all(a.get("family") for a in ca)
    if not allfam:return (True,False,False)
    supported=True
    for o,a in zip(oa,ca):
        fam=norm(a.get("family"))
        raw=norm(o.get("raw_author_name") or (o.get("author") or {}).get("display_name") or "")
        if not fam or fam not in raw:
            supported=False;break
    return (True,True,supported)

def rate(n,d): return n/d if d else None

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--start",type=int,default=2010);ap.add_argument("--end",type=int,default=2025);ap.add_argument("--per-cell",type=int,default=20);ap.add_argument("--outdir",default="data/pilot/annual_coverage");a=ap.parse_args()
    rows=[]
    for year in range(a.start,a.end+1):
        for fid,fname in FIELDS.items():
            works=sample(fid,year,a.per_cell)
            doi_n=cr_n=same=allfam=strict=0
            for w in works:
                if not w.get("doi"):continue
                doi_n+=1;c=cr(w["doi"])
                if not c:continue
                cr_n+=1
                sc,af,sp=positional_support(w,c)
                same+=int(sc);allfam+=int(af);strict+=int(sp)
                time.sleep(.025)
            row={"year":year,"field_id":fid,"field_name":fname,"sampled_multi_author":len(works),"doi_n":doi_n,"doi_rate":rate(doi_n,len(works)),"crossref_n":cr_n,"crossref_rate_given_doi":rate(cr_n,doi_n),"same_author_count_n":same,"same_author_count_rate":rate(same,cr_n),"all_family_n":allfam,"strict_position_supported_n":strict,"strict_position_supported_rate_given_same_count":rate(strict,same)}
            rows.append(row);print(json.dumps(row,ensure_ascii=False))
    yearly=[]
    for year in range(a.start,a.end+1):
        rr=[x for x in rows if x["year"]==year]
        S=sum(x["sampled_multi_author"] for x in rr);D=sum(x["doi_n"] for x in rr);C=sum(x["crossref_n"] for x in rr);SC=sum(x["same_author_count_n"] for x in rr);SP=sum(x["strict_position_supported_n"] for x in rr)
        yearly.append({"year":year,"sampled_multi_author":S,"doi_n":D,"doi_rate":rate(D,S),"crossref_n":C,"crossref_rate_given_doi":rate(C,D),"same_author_count_n":SC,"strict_position_supported_n":SP,"strict_position_supported_rate_given_same_count":rate(SP,SC),"fields_doi_ge_0_80":sum((x["doi_rate"] or 0)>=.80 for x in rr),"fields_strict_ge_0_90":sum((x["strict_position_supported_rate_given_same_count"] or 0)>=.90 for x in rr)})
    eligible=[]
    for start in range(a.start,min(2019,a.end+1)):
        suffix=[y for y in yearly if y["year"]>=start]
        ok=all((y["doi_rate"] or 0)>=.90 and (y["crossref_rate_given_doi"] or 0)>=.90 and (y["strict_position_supported_rate_given_same_count"] or 0)>=.95 and y["fields_doi_ge_0_80"]>=5 for y in suffix)
        if ok:eligible.append(start)
    proposed=min(eligible) if eligible else None
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    def write(name,data):
        with (out/name).open("w",encoding="utf-8",newline="") as h:
            w=csv.DictWriter(h,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    write("coverage_by_field_year.csv",rows);write("coverage_by_year.csv",yearly)
    manifest={"script":"11_annual_coverage_sweep.py","confirmatory_use_allowed":False,"years":[a.start,a.end],"per_field_year_requested":a.per_cell,"window_rule_frozen_before_results":"Choose earliest start in 2010–2018 such that every subsequent year through 2025 has aggregate DOI >=0.90, Crossref|DOI >=0.90, strict positional support >=0.95, and >=5/6 fields DOI >=0.80.","proposed_start_if_rule_passes":proposed,"privacy":"aggregate only"}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
