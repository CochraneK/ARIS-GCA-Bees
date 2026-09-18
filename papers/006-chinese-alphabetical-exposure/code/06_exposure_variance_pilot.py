#!/usr/bin/env python3
"""ARIS4C006 — exposure-variance pilot.

Measurement-only pilot for excess alphabetical authorship using Crossref
structured family names joined to reproducibly sampled OpenAlex works.
No focal surname rank or career outcome is used.
"""
from __future__ import annotations
import argparse, csv, json, math, os, re, time, unicodedata, urllib.parse, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

OA="https://api.openalex.org/works"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.6 exposure-variance-pilot"
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
    # Convention pilot requires a Latin-script family key.
    return re.sub(r"[^a-z0-9]","",s)

def oa_sample(fid,year,target):
    # Oversample to survive DOI / CR / structured-family exclusions.
    want=min(100,max(target*2,target+30))
    seed=int(f"{year}{fid:02d}61")
    p={"filter":",".join(["authorships.institutions.country_code:CN",f"topics.field.id:{fid}",f"from_publication_date:{year}-01-01",f"to_publication_date:{year}-12-31"]),"select":"id,doi,authorships,primary_location","sample":want,"seed":seed,"per-page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    if os.getenv("OPENALEX_MAILTO"):p["mailto"]=os.environ["OPENALEX_MAILTO"]
    d=get(OA+"?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def cr_record(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def chance_prob(keys):
    n=len(keys);counts=Counter(keys);num=1
    for m in counts.values():num*=math.factorial(m)
    return num/math.factorial(n)

def work_measure(w,cr):
    oa=w.get("authorships") or [];ca=cr.get("author") or []
    if not oa or len(oa)!=len(ca):return None
    keys=[sortkey(a.get("family")) for a in ca]
    if any(not k for k in keys):return None
    alpha=int(all(keys[i]<=keys[i+1] for i in range(len(keys)-1)))
    pc=chance_prob(keys)
    src=((w.get("primary_location") or {}).get("source") or {})
    return {"source_id":src.get("id") or "NO_SOURCE","source_name":src.get("display_name") or "","team_size":len(keys),"i_alpha":alpha,"p_chance":pc,"num":alpha-pc,"den":1-pc}

def excess(rows):
    den=sum(r["den"] for r in rows)
    return sum(r["num"] for r in rows)/den if den else None

def q(v,p):
    if not v:return None
    s=sorted(v);x=(len(s)-1)*p;lo=int(x);hi=min(lo+1,len(s)-1);f=x-lo
    return s[lo]*(1-f)+s[hi]*f

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--years",default="2020,2024");ap.add_argument("--per-cell",type=int,default=60);ap.add_argument("--min-source-n",type=int,default=4);ap.add_argument("--outdir",default="data/pilot/exposure_variance");a=ap.parse_args()
    years=[int(x) for x in a.years.split(",")];cell_rows=[];source_rows=[];all_valid=[]
    for year in years:
        for fid,fname in FIELDS.items():
            sampled=oa_sample(fid,year,a.per_cell);valid=[];doi_n=cr_n=0
            for w in sampled:
                if w.get("doi"):
                    doi_n+=1;cr=cr_record(w["doi"])
                    if cr:
                        cr_n+=1;m=work_measure(w,cr)
                        if m:valid.append(m)
                time.sleep(.035)
            all_valid.extend(({**r,"field_id":fid,"field_name":fname,"year":year} for r in valid))
            v3=[r for r in valid if r["team_size"]>=3]
            bysrc=defaultdict(list)
            for r in valid:bysrc[r["source_id"]].append(r)
            eligible_sources=[]
            for sid,rr in bysrc.items():
                if len(rr)>=a.min_source_n:
                    e=excess(rr);eligible_sources.append(e)
                    source_rows.append({"field_id":fid,"field_name":fname,"year":year,"source_id":sid,"n":len(rr),"excess_alpha":e,"n_3plus":sum(x["team_size"]>=3 for x in rr),"excess_alpha_3plus":excess([x for x in rr if x["team_size"]>=3])})
            cell_rows.append({"field_id":fid,"field_name":fname,"year":year,"sampled_multi_author_works":len(sampled),"doi_works":doi_n,"crossref_found":cr_n,"valid_order_works":len(valid),"valid_3plus_works":len(v3),"excess_alpha":excess(valid),"excess_alpha_3plus":excess(v3),"eligible_source_contexts":len(eligible_sources),"source_excess_q10":q(eligible_sources,.1),"source_excess_median":q(eligible_sources,.5),"source_excess_q90":q(eligible_sources,.9)})
            print(json.dumps(cell_rows[-1],ensure_ascii=False))
    cell_vals=[r["excess_alpha"] for r in cell_rows if r["excess_alpha"] is not None]
    source_vals=[r["excess_alpha"] for r in source_rows if r["excess_alpha"] is not None]
    manifest={"script":"06_exposure_variance_pilot.py","confirmatory_use_allowed":False,"sampling":"OpenAlex sample+seed, Crossref structured family names","years":years,"per_cell_requested":a.per_cell,"min_source_n":a.min_source_n,"field_year_cells":len(cell_rows),"valid_order_works_total":sum(r["valid_order_works"] for r in cell_rows),"eligible_source_contexts_total":len(source_rows),"field_year_excess_range":[min(cell_vals),max(cell_vals)] if cell_vals else None,"field_year_excess_sd":(sum((x-sum(cell_vals)/len(cell_vals))**2 for x in cell_vals)/len(cell_vals))**.5 if cell_vals else None,"source_excess_q10":q(source_vals,.1),"source_excess_median":q(source_vals,.5),"source_excess_q90":q(source_vals,.9),"privacy":"aggregate context summaries only; no personal identifiers persisted"}
    out=Path(a.outdir);write_csv(out/"field_year_exposure.csv",cell_rows);write_csv(out/"source_field_year_exposure.csv",source_rows);(out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
