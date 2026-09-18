#!/usr/bin/env python3
"""ARIS4C006 — all-26-field historical coverage gate.

Outcome-blind. Uses OpenAlex primary_topic fields and frozen primary work types
(article + conference-paper) to select the final global start year.
"""
from __future__ import annotations
import argparse,csv,json,os,re,time,unicodedata,urllib.parse,urllib.request
from pathlib import Path

OA="https://api.openalex.org"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.16 all-field-historical-coverage"

def get(url,retries=4):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=60) as r:return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(.4*(i+1))

def fid(raw):
    m=re.search(r"(\d+)$",str(raw or "").rstrip("/").split("/")[-1])
    return int(m.group(1)) if m else None

def fields():
    d=get(OA+"/fields?per_page=100")
    return sorted((fid(x.get("id")),x.get("display_name") or "") for x in (d or {}).get("results") or [] if fid(x.get("id")) is not None)

def filt(field,year):
    return ",".join([
        "authorships.institutions.country_code:CN",
        f"primary_topic.field.id:{field}",
        "type:article|conference-paper",
        f"from_publication_date:{year}-01-01",
        f"to_publication_date:{year}-12-31",
    ])

def sample(field,year,target):
    want=min(100,max(target*4,target+40));seed=int(f"{year}{field:02d}16")
    p={"filter":filt(field,year),"select":"id,doi,authorships","sample":want,"seed":seed,"per_page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA+"/works?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def cr(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def norm(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",str(s))
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z0-9]","",s)

def positional(w,c):
    oa=w.get("authorships") or [];ca=c.get("author") or []
    if not oa or len(oa)!=len(ca):return (False,False)
    if not all(a.get("family") for a in ca):return (True,False)
    ok=True
    for o,a in zip(oa,ca):
        fam=norm(a.get("family"))
        raw=norm(o.get("raw_author_name") or (o.get("author") or {}).get("display_name") or "")
        if not fam or fam not in raw:
            ok=False;break
    return (True,ok)

def rate(n,d):return n/d if d else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--start",type=int,default=2010)
    ap.add_argument("--end",type=int,default=2025)
    ap.add_argument("--per-field-year",type=int,default=8)
    ap.add_argument("--outdir",default="data/pilot/all_field_historical_coverage")
    a=ap.parse_args()
    fs=fields();rows=[]
    for year in range(a.start,a.end+1):
        for field,name in fs:
            works=sample(field,year,a.per_field_year)
            doi=crn=same=strict=0
            for w in works:
                if not w.get("doi"):continue
                doi+=1;c=cr(w["doi"])
                if not c:continue
                crn+=1;sc,sp=positional(w,c);same+=int(sc);strict+=int(sp)
                time.sleep(.015)
            row={
                "year":year,"field_id":field,"field_name":name,
                "sampled_multi_author":len(works),
                "doi_n":doi,"doi_rate":rate(doi,len(works)),
                "crossref_n":crn,"crossref_rate_given_doi":rate(crn,doi),
                "same_count_n":same,
                "strict_n":strict,
                "strict_rate_given_same_count":rate(strict,same),
            }
            rows.append(row);print(json.dumps(row,ensure_ascii=False))
    yearly=[]
    for year in range(a.start,a.end+1):
        rr=[r for r in rows if r["year"]==year]
        S=sum(r["sampled_multi_author"] for r in rr)
        D=sum(r["doi_n"] for r in rr)
        C=sum(r["crossref_n"] for r in rr)
        SC=sum(r["same_count_n"] for r in rr)
        ST=sum(r["strict_n"] for r in rr)
        yearly.append({
            "year":year,
            "sampled_multi_author":S,
            "doi_rate":rate(D,S),
            "crossref_rate_given_doi":rate(C,D),
            "strict_rate_given_same_count":rate(ST,SC),
            "fields_doi_ge_0_75":sum((r["doi_rate"] or 0)>=.75 for r in rr),
            "fields_sampled_ge_6":sum(r["sampled_multi_author"]>=6 for r in rr),
        })
    eligible=[]
    for start in range(a.start,min(2019,a.end+1)):
        suffix=[y for y in yearly if y["year"]>=start]
        ok=all(
            (y["doi_rate"] or 0)>=.90
            and (y["crossref_rate_given_doi"] or 0)>=.90
            and (y["strict_rate_given_same_count"] or 0)>=.95
            and y["fields_doi_ge_0_75"]>=22
            for y in suffix
        )
        if ok:eligible.append(start)
    proposed=min(eligible) if eligible else None

    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    for fn,data in [("coverage_by_field_year.csv",rows),("coverage_by_year.csv",yearly)]:
        with (out/fn).open("w",encoding="utf-8",newline="") as h:
            w=csv.DictWriter(h,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    manifest={
        "script":"16_all_field_historical_coverage.py",
        "confirmatory_use_allowed":False,
        "field_rule":"OpenAlex primary_topic.field.id",
        "work_types":["article","conference-paper"],
        "fields_found":len(fs),
        "years":[a.start,a.end],
        "per_field_year_requested":a.per_field_year,
        "window_rule_frozen_before_results":"Choose earliest start in 2010-2018 such that every subsequent year through 2025 has aggregate DOI >=0.90, Crossref|DOI >=0.90, strict positional support >=0.95, and at least 22/26 fields with DOI coverage >=0.75.",
        "proposed_global_start":proposed,
        "privacy":"aggregate only",
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":main()
