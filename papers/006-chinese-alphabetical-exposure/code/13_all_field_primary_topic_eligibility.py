#!/usr/bin/env python3
"""ARIS4C006 — all-field primary-topic eligibility pilot.

Outcome-blind. Enumerates all current OpenAlex fields, measures China-affiliated
primary-field output volume in two lag windows, and uses reproducible random
samples to assess DOI/Crossref/structured-family order coverage.

No surname rank or career outcome is used.
"""
from __future__ import annotations
import argparse,csv,json,math,os,re,time,unicodedata,urllib.parse,urllib.request
from collections import Counter
from pathlib import Path

OA="https://api.openalex.org"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.13 all-field-primary-topic-eligibility"

def get(url,retries=4):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=60) as r:return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(.5*(i+1))

def field_id(raw):
    s=str(raw or "").rstrip("/").split("/")[-1]
    m=re.search(r"(\d+)$",s)
    return int(m.group(1)) if m else None

def fields():
    d=get(OA+"/fields?per_page=100")
    out=[]
    for x in (d or {}).get("results") or []:
        fid=field_id(x.get("id"))
        if fid is not None:out.append((fid,x.get("display_name") or str(fid)))
    return sorted(out)

def base_filter(fid,start,end):
    return ",".join([
        "authorships.institutions.country_code:CN",
        f"primary_topic.field.id:{fid}",
        f"from_publication_date:{start}-01-01",
        f"to_publication_date:{end}-12-31"
    ])

def count_works(fid,start,end):
    p={"filter":base_filter(fid,start,end),"select":"id","per_page":1}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA+"/works?"+urllib.parse.urlencode(p))
    return int(((d or {}).get("meta") or {}).get("count") or 0)

def sample(fid,year,target):
    want=min(100,max(target*3,target+40));seed=int(f"{year}{fid:02d}13")
    p={"filter":base_filter(fid,year,year),"select":"id,doi,authorships","sample":want,"seed":seed,"per_page":want}
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
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z0-9]","",s)

def chance(keys):
    n=len(keys);num=1
    for m in Counter(keys).values():num*=math.factorial(m)
    return num/math.factorial(n)

def measure(w,c):
    oa=w.get("authorships") or [];ca=c.get("author") or []
    if not oa or len(oa)!=len(ca):return None
    keys=[norm(x.get("family")) for x in ca]
    if any(not k for k in keys):return None
    ia=int(all(keys[i]<=keys[i+1] for i in range(len(keys)-1)));pc=chance(keys)
    return (ia-pc,1-pc)

def rate(n,d):return n/d if d else None

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--per-field-year",type=int,default=15);ap.add_argument("--outdir",default="data/pilot/all_field_eligibility");a=ap.parse_args()
    fs=fields();rows=[]
    for fid,fname in fs:
        count_a=count_works(fid,2017,2019);count_b=count_works(fid,2021,2023)
        sampled=doi=crn=valid=0;valid_by_year={2020:0,2024:0};num=den=0.0
        for year in [2020,2024]:
            ww=sample(fid,year,a.per_field_year);sampled+=len(ww)
            for w in ww:
                if not w.get("doi"):continue
                doi+=1;c=cr(w["doi"])
                if not c:continue
                crn+=1;m=measure(w,c)
                if m is not None:
                    valid+=1;valid_by_year[year]+=1;num+=m[0];den+=m[1]
                time.sleep(.02)
        pooled_valid_rate=rate(valid,sampled)
        eligible=(min(count_a,count_b)>=500 and (pooled_valid_rate or 0)>=.50 and valid_by_year[2020]>=8 and valid_by_year[2024]>=8)
        row={"field_id":fid,"field_name":fname,"cn_primaryfield_works_2017_2019":count_a,"cn_primaryfield_works_2021_2023":count_b,"sampled_multi_author_2020_2024":sampled,"doi_n":doi,"doi_rate":rate(doi,sampled),"crossref_n":crn,"crossref_rate_given_doi":rate(crn,doi),"valid_order_n":valid,"valid_order_rate":pooled_valid_rate,"valid_order_2020":valid_by_year[2020],"valid_order_2024":valid_by_year[2024],"pilot_excess_alpha":num/den if den else None,"eligible_primary_field":eligible}
        rows.append(row);print(json.dumps(row,ensure_ascii=False))
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    with (out/"all_field_eligibility.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    manifest={"script":"13_all_field_primary_topic_eligibility.py","confirmatory_use_allowed":False,"openalex_fields_found":len(fs),"field_context_rule":"primary_topic.field.id only","prospective_field_gate":"Include field in primary work-level frame if both 2017-2019 and 2021-2023 China-affiliated primary-field counts >=500, pooled random-sample valid structured-order rate >=0.50, and >=8 valid structured-order works in each 2020 and 2024 sample.","eligible_fields":sum(bool(r["eligible_primary_field"]) for r in rows),"privacy":"aggregate only"}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
