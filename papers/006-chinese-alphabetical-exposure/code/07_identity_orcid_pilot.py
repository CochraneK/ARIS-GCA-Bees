#!/usr/bin/env python3
"""ARIS4C006 — ORCID/OpenAlex person-identity pilot.

Randomly sample China-affiliated authorships, obtain high-confidence structured
family names from Crossref when possible, and check whether an authorship's
OpenAlex author ID equals the OpenAlex author resolved directly from its ORCID.

Aggregate outputs only; no personal identifiers are persisted.
"""
from __future__ import annotations
import argparse, csv, json, os, re, time, unicodedata, urllib.parse, urllib.request
from collections import defaultdict
from pathlib import Path

OA_WORKS="https://api.openalex.org/works"
OA_AUTHORS="https://api.openalex.org/authors/"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.7 ORCID identity pilot"
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

def norm(s):
    s=unicodedata.normalize("NFKD",s or "")
    s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z]","",s.lower())

def norm_orcid(s):
    if not s:return ""
    s=s.lower().replace("https://orcid.org/","").replace("http://orcid.org/","")
    s=re.sub(r"[^0-9x-]","",s)
    return s

def short_oa(s):
    return (s or "").rstrip("/").split("/")[-1]

def is_cn(a):
    return any(i.get("country_code")=="CN" for i in (a.get("institutions") or [])) or "CN" in (a.get("countries") or [])

def oa_sample(fid,year,target):
    want=min(100,max(target*2,target+30));seed=int(f"{year}{fid:02d}73")
    p={"filter":",".join(["authorships.institutions.country_code:CN",f"topics.field.id:{fid}",f"from_publication_date:{year}-01-01",f"to_publication_date:{year}-12-31"]),"select":"id,doi,authorships","sample":want,"seed":seed,"per-page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA_WORKS+"?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def cr_record(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def band(family):
    k=norm(family)
    if not k or not ("a"<=k[0]<="z"):return "unknown"
    r=ord(k[0])-96
    return "early_A-I" if r<=9 else ("middle_J-R" if r<=18 else "late_S-Z")

def resolve_orcid(oid,cache):
    if oid in cache:return cache[oid]
    d=get(OA_AUTHORS+"orcid:"+urllib.parse.quote(oid,safe="-"))
    cache[oid]=short_oa((d or {}).get("id")) if d else ""
    time.sleep(.03)
    return cache[oid]

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--years",default="2020,2024");ap.add_argument("--per-cell",type=int,default=25);ap.add_argument("--outdir",default="data/pilot/identity_orcid");a=ap.parse_args()
    years=[int(x) for x in a.years.split(",")];cache={};rows=[];author_orcids=defaultdict(set)
    for year in years:
        for fid,fname in FIELDS.items():
            works=oa_sample(fid,year,a.per_cell)
            counts=defaultdict(lambda:{"eligible":0,"resolved":0,"match":0,"mismatch":0})
            for w in works:
                cr=cr_record(w.get("doi"))
                oa=w.get("authorships") or [];ca=(cr or {}).get("author") or []
                positional=(bool(cr) and len(oa)==len(ca) and len(oa)>0)
                for pos,o in enumerate(oa):
                    if not is_cn(o):continue
                    auth=o.get("author") or {};aid=short_oa(auth.get("id"));oid=norm_orcid(auth.get("orcid"))
                    if oid and aid:author_orcids[aid].add(oid)
                    if not (oid and aid):continue
                    fam=ca[pos].get("family") if positional else ""
                    b=band(fam)
                    counts[b]["eligible"]+=1
                    rid=resolve_orcid(oid,cache)
                    if rid:
                        counts[b]["resolved"]+=1
                        if rid==aid:counts[b]["match"]+=1
                        else:counts[b]["mismatch"]+=1
                time.sleep(.03)
            for b,d in counts.items():
                rows.append({"field_id":fid,"field_name":fname,"year":year,"initial_band":b,**d,"mismatch_rate_given_resolved":(d["mismatch"]/d["resolved"] if d["resolved"] else None)})
                print(json.dumps(rows[-1],ensure_ascii=False))
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    if rows:
        with (out/"identity_orcid_by_field_year_band.csv").open("w",encoding="utf-8",newline="") as h:
            w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    else:(out/"identity_orcid_by_field_year_band.csv").write_text("",encoding="utf-8")
    total_res=sum(r["resolved"] for r in rows);total_mis=sum(r["mismatch"] for r in rows)
    manifest={"script":"07_identity_orcid_pilot.py","confirmatory_use_allowed":False,"sampling":"OpenAlex sample+seed","years":years,"per_cell_requested":a.per_cell,"unique_orcids_resolved_or_attempted":len(cache),"resolved_authorship_checks":total_res,"orcid_author_id_mismatches":total_mis,"mismatch_rate":(total_mis/total_res if total_res else None),"openalex_author_ids_seen_with_multiple_orcids_lower_bound":sum(len(v)>1 for v in author_orcids.values()),"privacy":"aggregate only; no names, ORCIDs, author IDs, or DOIs persisted"}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
