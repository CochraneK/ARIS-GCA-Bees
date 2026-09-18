#!/usr/bin/env python3
"""ARIS4C006 — surname-specific Romanization audit using CCNC.

Combines:
  * ChineseNames familyname population weights
  * CCNC Romanized Chinese Last Names Dictionary

Outputs:
  * Han-surname -> surname-specific canonical Hanyu-Pinyin map
  * aggregated Romanized-form population weights
  * ChineseNames-initial vs CCNC-pronunciation-initial discrepancies
  * outcome-blind 2024 all-field exact-mapping coverage

No focal surname-effect or career outcome is computed.
"""
from __future__ import annotations
import argparse,csv,json,os,re,time,unicodedata,urllib.parse,urllib.request
from collections import defaultdict
from pathlib import Path

OA="https://api.openalex.org"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.15 ccnc-surname-romanization-audit"

def get(url,retries=4):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(.5*(i+1))

def norm_latin(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",str(s))
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z]","",s)

def load_cn(path):
    rows=[]
    with open(path,encoding="utf-8-sig") as h:
        for r in csv.DictReader(h):
            r["population_n"]=int(float(r["n.1930_2008"]))
            r["ppm"]=float(r["ppm.1930_2008"])
            r["compound_i"]=int(r["compound"])
            rows.append(r)
    return rows

def load_ccnc(path):
    raw=json.load(open(path,encoding="utf-8"))
    return {k:norm_latin(v) for k,v in raw.items() if norm_latin(v)}

def field_id(raw):
    m=re.search(r"(\d+)$",str(raw or "").rstrip("/").split("/")[-1])
    return int(m.group(1)) if m else None

def fields():
    d=get(OA+"/fields?per_page=100")
    return sorted((field_id(x.get("id")),x.get("display_name") or "") for x in (d or {}).get("results") or [] if field_id(x.get("id")) is not None)

def sample_field(fid,year,target):
    want=min(100,max(target*3,target+30));seed=int(f"{year}{fid:02d}15")
    filt=",".join([
        "authorships.institutions.country_code:CN",
        f"primary_topic.field.id:{fid}",
        "type:article|conference-paper",
        f"from_publication_date:{year}-01-01",
        f"to_publication_date:{year}-12-31",
    ])
    p={"filter":filt,"select":"id,doi,authorships","sample":want,"seed":seed,"per_page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA+"/works?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def cr(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def is_cn(a):
    return any(i.get("country_code")=="CN" for i in (a.get("institutions") or [])) or "CN" in (a.get("countries") or [])

def write_csv(path,rows,fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields or list(rows[0].keys()));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("familyname_csv")
    ap.add_argument("ccnc_json")
    ap.add_argument("--year",type=int,default=2024)
    ap.add_argument("--per-field",type=int,default=10)
    ap.add_argument("--outdir",default="data/pilot/ccnc_romanization")
    a=ap.parse_args()

    cn=load_cn(a.familyname_csv)
    ccnc=load_ccnc(a.ccnc_json)

    mapped=[];missing=[];mismatch=[]
    for r in cn:
        han=r["surname"]
        py=ccnc.get(han,"")
        if not py:
            missing.append({
                "surname":han,
                "compound":r["compound_i"],
                "population_n":r["population_n"],
                "chinesenames_initial":r["initial"],
                "reason":"surname_not_in_ccnc_dictionary",
            })
            continue
        rec={
            "surname":han,
            "compound":r["compound_i"],
            "romanized":py,
            "ccnc_initial":py[0],
            "chinesenames_initial":(r["initial"] or "").lower(),
            "population_n":r["population_n"],
            "ppm":r["ppm"],
        }
        mapped.append(rec)
        if rec["ccnc_initial"]!=rec["chinesenames_initial"]:
            mismatch.append(rec.copy())

    grouped=defaultdict(list)
    for r in mapped:grouped[r["romanized"]].append(r)
    agg=[]
    for form,rr in grouped.items():
        agg.append({
            "romanized":form,
            "initial":form[0],
            "population_n":sum(x["population_n"] for x in rr),
            "population_ppm":sum(x["ppm"] for x in rr),
            "han_surname_count":len(rr),
            "compound_member_count":sum(x["compound"] for x in rr),
            "members":";".join(x["surname"] for x in rr),
        })
    romanized_forms={x["romanized"] for x in agg}

    field_rows=[];total_cn=total_map=0
    for fid,fname in fields():
        cn_rows=mapped_rows=aligned_works=0
        for w in sample_field(fid,a.year,a.per_field):
            c=cr(w.get("doi"));oa=w.get("authorships") or [];ca=(c or {}).get("author") or []
            if not c or len(oa)!=len(ca):continue
            aligned_works+=1
            for o,cc in zip(oa,ca):
                if not is_cn(o):continue
                fam=norm_latin(cc.get("family"))
                if not fam:continue
                cn_rows+=1
                if fam in romanized_forms:mapped_rows+=1
            time.sleep(.02)
        total_cn+=cn_rows;total_map+=mapped_rows
        field_rows.append({
            "field_id":fid,"field_name":fname,"aligned_works":aligned_works,
            "cn_structured_family_rows":cn_rows,
            "ccnc_exact_mapped_rows":mapped_rows,
            "mapping_rate":mapped_rows/cn_rows if cn_rows else None,
        })
        print(json.dumps(field_rows[-1],ensure_ascii=False))

    total_pop=sum(r["population_n"] for r in cn)
    mapped_pop=sum(r["population_n"] for r in mapped)
    mismatch_pop=sum(r["population_n"] for r in mismatch)

    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    write_csv(out/"han_to_ccnc_pinyin.csv",mapped)
    write_csv(out/"romanized_population_map.csv",sorted(agg,key=lambda x:(-x["population_n"],x["romanized"])))
    write_csv(out/"missing_chinesenames_surnames.csv",missing)
    write_csv(out/"initial_discrepancies.csv",sorted(mismatch,key=lambda x:-x["population_n"]))
    write_csv(out/"field_mapping_coverage.csv",field_rows)

    manifest={
        "script":"15_ccnc_surname_romanization_audit.py",
        "confirmatory_use_allowed":False,
        "chinesenames_rows":len(cn),
        "ccnc_dictionary_rows":len(ccnc),
        "direct_han_intersection_rows":len(mapped),
        "direct_han_intersection_rate":len(mapped)/len(cn),
        "mapped_population_coverage":mapped_pop/total_pop if total_pop else None,
        "missing_chinesenames_rows":len(missing),
        "ccnc_vs_chinesenames_initial_discrepancies":len(mismatch),
        "discrepancy_population_share":mismatch_pop/total_pop if total_pop else None,
        "aggregated_romanized_forms":len(agg),
        "sample_year":a.year,
        "cn_structured_family_rows_sample":total_cn,
        "ccnc_exact_mapped_rows_sample":total_map,
        "ccnc_exact_mapping_coverage_sample":total_map/total_cn if total_cn else None,
        "primary_candidate_rule":"ChineseNames supplies population weights; CCNC supplies surname-specific Hanyu-Pinyin form. Exact normalized Crossref family == frozen CCNC form is eligible. Missing/legacy/regional variants are excluded from primary unless separately reviewed and frozen.",
        "ambiguity_rule":"If multiple Han surnames share one Romanized form, aggregate population weight to the observed Romanized form; do not impute a specific Han surname.",
        "privacy":"public surname-dictionary derivatives and aggregate bibliographic coverage only",
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":main()
