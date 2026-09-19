#!/usr/bin/env python3
"""ARIS4C006 — outcome-blind longitudinal identity-risk prevalence audit.

Randomly seeds CN-affiliated eligible works from entry years 2014–2020,
identifies high-confidence focal surname authors, canonicalizes OpenAlex author
IDs, reconstructs eligible publication histories, and reports only identity-QA
flag prevalence. No persistence outcome and no surname×exposure effect is
computed.
"""
from __future__ import annotations
import argparse,csv,json,os,re,time,unicodedata,urllib.parse,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

OA="https://api.openalex.org"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.26 identity-risk-prevalence"

def get_json(url,retries=5):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=75) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(min(8,.8*(2**i)))
    return None

def short(s): return (s or "").rstrip("/").split("/")[-1]

def norm_latin(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",str(s))
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z]","",s)

def authorship_is_cn(a):
    return any(i.get("country_code")=="CN" for i in (a.get("institutions") or [])) or "CN" in (a.get("countries") or [])

def load_maps(family_csv,ccnc_json):
    pop={}
    with open(family_csv,encoding="utf-8-sig") as h:
        for r in csv.DictReader(h):
            pop[r["surname"]]=int(float(r["n.1930_2008"]))
    raw=json.load(open(ccnc_json,encoding="utf-8"))
    han_to_py={}
    for han,py in raw.items():
        if han in pop:
            n=norm_latin(py)
            if n:han_to_py[han]=n
    roman=defaultdict(int)
    for han,py in han_to_py.items():roman[py]+=pop[han]
    return pop,han_to_py,roman

def crossref(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get_json(CR+urllib.parse.quote(doi,safe=""))
    time.sleep(.012)
    return (d or {}).get("message") or None

def canonical_author(raw_id):
    d=get_json(OA+"/authors/"+urllib.parse.quote(short(raw_id),safe=""))
    if not d:return None
    return {"id":short(d.get("id")),"orcid":d.get("orcid") or ""}

def seed_works(year,target):
    p={
      "filter":",".join([
        "authorships.institutions.country_code:CN",
        "type:article|conference-paper",
        f"from_publication_date:{year}-01-01",
        f"to_publication_date:{year}-12-31",
      ]),
      "select":"id,doi,authorships",
      "sample":min(100,max(target*3,target+30)),
      "seed":600626000+year,
      "per_page":min(100,max(target*3,target+30)),
    }
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get_json(OA+"/works?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=1][:target]

def focal_candidates(w,han_to_py,roman):
    if not w.get("doi"):return []
    cr=crossref(w["doi"]);oa=w.get("authorships") or [];ca=(cr or {}).get("author") or []
    if not cr or len(oa)!=len(ca):return []
    out=[]
    for o,c in zip(oa,ca):
        if not authorship_is_cn(o):continue
        fam=str(c.get("family") or "").strip()
        raw=o.get("raw_author_name") or (o.get("author") or {}).get("display_name") or ""
        route="";mapped_form=""
        if fam in han_to_py:
            mapped_form=han_to_py[fam]
            if fam not in raw and mapped_form not in norm_latin(raw):continue
            route="direct_han"
        else:
            lat=norm_latin(fam)
            if not lat or lat not in roman or lat not in norm_latin(raw):continue
            mapped_form=lat;route="canonical_romanized"
        rid=short((o.get("author") or {}).get("id"))
        if not rid:continue
        out.append({"raw_id":rid,"route":route,"surname_form":mapped_form,"surname_pop":roman[mapped_form]})
    return out

def author_history(cid,start=2011,end=2025,maxworks=1000):
    cur="*";works=[]
    while cur and len(works)<maxworks:
        p={
          "filter":",".join([f"author.id:{cid}","type:article|conference-paper",f"from_publication_date:{start}-01-01",f"to_publication_date:{end}-12-31"]),
          "select":"id,publication_year,authorships",
          "per_page":100,
          "cursor":cur,
        }
        if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
        d=get_json(OA+"/works?"+urllib.parse.urlencode(p))
        if not d:break
        rr=d.get("results") or []
        if not rr:break
        works.extend(rr[:maxworks-len(works)])
        cur=(d.get("meta") or {}).get("next_cursor")
    return works

def focal_authorship(work,cid):
    for a in work.get("authorships") or []:
        aid=short((a.get("author") or {}).get("id"))
        if not aid:continue
        # Embedded alias may differ; caller resolves only when needed.
        if aid==cid:return a
    return None

def analyze_candidate(seed,corrected_total):
    can=canonical_author(seed["raw_id"])
    if not can or not can["id"]:
        return {"hard_exclusion":"canonicalization_failure"}
    cid=can["id"];works=author_history(cid)
    years=defaultdict(list);raw_ids=set();orcid_values=set()
    if can.get("orcid"):orcid_values.add(str(can["orcid"]).lower())

    # Resolve embedded aliases only for focal authorship matching/provenance.
    alias_cache={}
    for w in works:
        y=w.get("publication_year")
        if not y:continue
        matched=None
        for a in w.get("authorships") or []:
            rid=short((a.get("author") or {}).get("id"))
            if not rid:continue
            if rid==cid:
                matched=a;raw_ids.add(rid);break
            if rid not in alias_cache:
                ca=canonical_author(rid);alias_cache[rid]=(ca or {}).get("id","")
            if alias_cache[rid]==cid:
                matched=a;raw_ids.add(rid);break
        if matched is None:continue
        yrs=years[y];yrs.append(w)
        ao=(matched.get("author") or {}).get("orcid")
        if ao:orcid_values.add(str(ao).lower())

    if len(orcid_values)>1:
        return {"hard_exclusion":"orcid_conflict","canonical_author_id":cid}

    counts={y:len(v) for y,v in years.items()}
    maxworks=max(counts.values(),default=0)
    max_inst=0;max_countries=0
    for y,ww in years.items():
        inst=set();countries=set()
        for w in ww:
            for a in w.get("authorships") or []:
                rid=short((a.get("author") or {}).get("id"))
                if rid not in raw_ids and rid!=cid:continue
                for i in a.get("institutions") or []:
                    if i.get("id"):inst.add(i["id"])
                    if i.get("country_code"):countries.add(i["country_code"])
                for cc in a.get("countries") or []:
                    if cc:countries.add(cc)
        max_inst=max(max_inst,len(inst));max_countries=max(max_countries,len(countries))

    # Entry/cohort diagnostic only; do not compute e+4/e+5 persistence.
    active=sorted(counts)
    entry=min(active) if active else None
    first3=sum(counts.get(y,0) for y in range(entry,entry+3)) if entry is not None else 0

    flags={
      "R1_no_orcid":not bool(orcid_values),
      "R2_extreme_annual_output":maxworks>100,
      "R3_many_institutions":max_inst>12,
      "R4_many_countries":max_countries>4,
      "R5_alias_history":len(raw_ids)>=2,
      "R6_sparse_early_identity":first3<2,
    }
    low_risk=not(flags["R2_extreme_annual_output"] or flags["R3_many_institutions"] or flags["R4_many_countries"])
    return {
      "hard_exclusion":"",
      "canonical_author_id":cid,
      "entry_year_observed":entry,
      "seed_year":seed["seed_year"],
      "surname_route":seed["route"],
      "surname_collision_share":seed["surname_pop"]/corrected_total,
      "max_annual_eligible_works":maxworks,
      "max_annual_institutions":max_inst,
      "max_annual_countries":max_countries,
      "raw_alias_ids_seen":len(raw_ids),
      "eligible_works_first3":first3,
      **flags,
      "low_risk":low_risk,
      "orcid_anchored":not flags["R1_no_orcid"],
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--familyname-csv",required=True)
    ap.add_argument("--ccnc-json",required=True)
    ap.add_argument("--seed-works-per-year",type=int,default=15)
    ap.add_argument("--max-authors",type=int,default=180)
    ap.add_argument("--outdir",default="data/pilot/identity_risk")
    a=ap.parse_args()

    pop,han_to_py,roman=load_maps(a.familyname_csv,a.ccnc_json)
    corrected_total=sum(pop[h] for h in han_to_py)
    seeds=[];seen_can=set()
    for year in range(2014,2021):
        for w in seed_works(year,a.seed_works_per_year):
            for s in focal_candidates(w,han_to_py,roman):
                can=canonical_author(s["raw_id"])
                cid=(can or {}).get("id","")
                if not cid or cid in seen_can:continue
                s["seed_year"]=year;seeds.append(s);seen_can.add(cid)
                if len(seeds)>=a.max_authors:break
            if len(seeds)>=a.max_authors:break
        if len(seeds)>=a.max_authors:break

    rows=[]
    for i,s in enumerate(seeds,1):
        rows.append(analyze_candidate(s,corrected_total))
        if i%20==0:print("authors",i)

    hard=Counter(r.get("hard_exclusion") or "none" for r in rows)
    valid=[r for r in rows if not r.get("hard_exclusion")]
    flag_names=["R1_no_orcid","R2_extreme_annual_output","R3_many_institutions","R4_many_countries","R5_alias_history","R6_sparse_early_identity"]
    flag_counts={k:sum(bool(r.get(k)) for r in valid) for k in flag_names}
    overlap=Counter(sum(bool(r.get(k)) for k in flag_names) for r in valid)
    cohort_years=Counter(r.get("entry_year_observed") for r in valid if r.get("entry_year_observed") is not None)
    route_counts=Counter(r.get("surname_route") for r in valid)
    collision={
      "lt_1pct":sum((r.get("surname_collision_share") or 0)<.01 for r in valid),
      "ge_1pct":sum((r.get("surname_collision_share") or 0)>=.01 for r in valid),
      "ge_5pct":sum((r.get("surname_collision_share") or 0)>=.05 for r in valid),
    }
    manifest={
      "script":"26_identity_risk_prevalence.py",
      "confirmatory_outcomes_unlocked":False,
      "persistence_outcome_computed":False,
      "effect_or_pvalue_computed":False,
      "seed_authors":len(rows),
      "hard_exclusions":dict(hard),
      "hard_qa_pass":len(valid),
      "hard_qa_pass_share":len(valid)/len(rows) if rows else None,
      "flag_counts":flag_counts,
      "flag_shares":{k:(v/len(valid) if valid else None) for k,v in flag_counts.items()},
      "flag_overlap_count":dict(sorted(overlap.items())),
      "low_risk_subset":sum(bool(r.get("low_risk")) for r in valid),
      "orcid_anchored_subset":sum(bool(r.get("orcid_anchored")) for r in valid),
      "surname_route_counts":dict(route_counts),
      "surname_collision_bands":collision,
      "observed_entry_year_counts":{str(k):v for k,v in sorted(cohort_years.items())},
      "identity_rule":"process/IDENTITY_RISK_RULE.md",
      "privacy":"aggregate manifest is the review artifact; row-level IDs are not uploaded",
    }
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
