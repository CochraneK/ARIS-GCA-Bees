#!/usr/bin/env python3
"""ARIS4C006 — canonical author-ID reconciliation pilot.

Reproduce the outcome-blind ORCID identity sample and classify raw
authorship-ID/ORCID-ID mismatches as:
  * resolved by canonicalizing the embedded OpenAlex author ID,
  * unresolved true conflict,
  * lookup failure.

Aggregate only; no identifiers are persisted.
"""
from __future__ import annotations
import argparse, csv, json, os, re, time, unicodedata, urllib.parse, urllib.request
from collections import defaultdict
from pathlib import Path

OA_WORKS="https://api.openalex.org/works"
OA_AUTHORS="https://api.openalex.org/authors/"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.7.1 author-id-canonicalization"
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
    return re.sub(r"[^0-9x-]","",s)

def short(s): return (s or "").rstrip("/").split("/")[-1]

def is_cn(a):
    return any(i.get("country_code")=="CN" for i in (a.get("institutions") or [])) or "CN" in (a.get("countries") or [])

def oa_sample(fid,year,target):
    want=min(100,max(target*2,target+30));seed=int(f"{year}{fid:02d}73")
    p={"filter":",".join(["authorships.institutions.country_code:CN",f"topics.field.id:{fid}",f"from_publication_date:{year}-01-01",f"to_publication_date:{year}-12-31"]),"select":"id,doi,authorships","sample":want,"seed":seed,"per_page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA_WORKS+"?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def crossref(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def band(family):
    k=norm(family)
    if not k:return "unknown"
    r=ord(k[0])-96 if "a"<=k[0]<="z" else -1
    return "early_A-I" if 1<=r<=9 else ("middle_J-R" if 10<=r<=18 else ("late_S-Z" if 19<=r<=26 else "unknown"))

def resolve_orcid(oid,cache):
    if oid not in cache:
        d=get(OA_AUTHORS+"orcid:"+urllib.parse.quote(oid,safe="-"))
        cache[oid]=short((d or {}).get("id"))
        time.sleep(.02)
    return cache[oid]

def canonicalize_author(aid,cache):
    if aid not in cache:
        d=get(OA_AUTHORS+urllib.parse.quote(aid,safe=""))
        cache[aid]={"id":short((d or {}).get("id")),"orcid":norm_orcid((d or {}).get("orcid"))} if d else {"id":"","orcid":""}
        time.sleep(.02)
    return cache[aid]

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--years",default="2020,2024");ap.add_argument("--per-cell",type=int,default=25);ap.add_argument("--outdir",default="data/pilot/identity_canonical");a=ap.parse_args()
    years=[int(x) for x in a.years.split(",")];ocache={};acache={};rows=[]
    totals=defaultdict(int)
    for year in years:
        for fid,fname in FIELDS.items():
            buckets=defaultdict(lambda:defaultdict(int))
            for w in oa_sample(fid,year,a.per_cell):
                cr=crossref(w.get("doi"));oa=w.get("authorships") or [];ca=(cr or {}).get("author") or []
                positional=bool(cr) and len(oa)==len(ca) and len(oa)>0
                for pos,o in enumerate(oa):
                    if not is_cn(o):continue
                    au=o.get("author") or {};aid=short(au.get("id"));oid=norm_orcid(au.get("orcid"))
                    if not (aid and oid):continue
                    b=band(ca[pos].get("family") if positional else "")
                    rid=resolve_orcid(oid,ocache)
                    if not rid:continue
                    buckets[b]["resolved"]+=1;totals["resolved"]+=1
                    if rid==aid:
                        buckets[b]["raw_match"]+=1;totals["raw_match"]+=1
                        continue
                    buckets[b]["raw_mismatch"]+=1;totals["raw_mismatch"]+=1
                    can=canonicalize_author(aid,acache)
                    if can["id"]==rid or (can["orcid"] and can["orcid"]==oid):
                        buckets[b]["fixed_by_canonicalization"]+=1;totals["fixed_by_canonicalization"]+=1
                    elif not can["id"]:
                        buckets[b]["embedded_id_lookup_failure"]+=1;totals["embedded_id_lookup_failure"]+=1
                    else:
                        buckets[b]["unresolved_conflict"]+=1;totals["unresolved_conflict"]+=1
                time.sleep(.02)
            for b,d in buckets.items():
                res=d["resolved"];rawmis=d["raw_mismatch"]
                rows.append({"field_id":fid,"field_name":fname,"year":year,"initial_band":b,"resolved":res,"raw_match":d["raw_match"],"raw_mismatch":rawmis,"raw_mismatch_rate":rawmis/res if res else None,"fixed_by_canonicalization":d["fixed_by_canonicalization"],"unresolved_conflict":d["unresolved_conflict"],"embedded_id_lookup_failure":d["embedded_id_lookup_failure"],"residual_conflict_rate":d["unresolved_conflict"]/res if res else None})
                print(json.dumps(rows[-1],ensure_ascii=False))
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    with (out/"identity_canonicalization_by_band.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    res=totals["resolved"]
    manifest={"script":"09_identity_canonicalization_pilot.py","confirmatory_use_allowed":False,"sampling":"same reproducible OpenAlex sample+seed as Pilot 7","resolved_checks":res,"raw_mismatches":totals["raw_mismatch"],"raw_mismatch_rate":totals["raw_mismatch"]/res if res else None,"fixed_by_canonicalization":totals["fixed_by_canonicalization"],"unresolved_conflicts":totals["unresolved_conflict"],"lookup_failures":totals["embedded_id_lookup_failure"],"residual_conflict_rate":totals["unresolved_conflict"]/res if res else None,"rule_candidate":"Canonicalize embedded OpenAlex author IDs through /authors/{id} before longitudinal joins; then validate against ORCID where available.","privacy":"aggregate only"}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
