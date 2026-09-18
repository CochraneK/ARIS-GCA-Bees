#!/usr/bin/env python3
"""ARIS4C006 — outcome-locked primary focal-frame materializer.

Per one primary-topic field, 2011–2025:
- reproducibly sample works under the frozen frame rule,
- strict OpenAlex/Crossref byline reconciliation,
- identify CN-affiliated ChineseNames×CCNC focal surname rows,
- compute whole-team relative alphabetical rank and listed position,
- canonicalize focal OpenAlex author IDs,
- persist rows + structural counts only.

NO H1/H2/H3 model or predictor-outcome summary is computed.
"""
from __future__ import annotations
import argparse,csv,json,os,re,time,unicodedata,urllib.parse,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

OA="https://api.openalex.org"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.24 primary-frame-materializer"

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

def short(s):return (s or "").rstrip("/").split("/")[-1]

def norm_latin(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",str(s))
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z]","",s)

def is_han_string(s):
    if not s:return False
    chars=[c for c in str(s) if not c.isspace()]
    return bool(chars) and all("\u3400"<=c<="\u9fff" for c in chars)

def authorship_is_cn(a):
    return any(i.get("country_code")=="CN" for i in (a.get("institutions") or [])) or "CN" in (a.get("countries") or [])

def load_maps(family_csv,ccnc_json):
    pop={}
    compound={}
    with open(family_csv,encoding="utf-8-sig") as h:
        for r in csv.DictReader(h):
            pop[r["surname"]]=int(float(r["n.1930_2008"]))
            compound[r["surname"]]=int(r["compound"])
    raw=json.load(open(ccnc_json,encoding="utf-8"))
    han_to_py={}
    for han,py in raw.items():
        if han in pop:
            n=norm_latin(py)
            if n:han_to_py[han]=n
    roman=defaultdict(lambda:{"population_n":0,"han_count":0})
    for han,py in han_to_py.items():
        roman[py]["population_n"]+=pop[han]
        roman[py]["han_count"]+=1
    return pop,han_to_py,roman

def field_name(fid):
    return (get_json(f"{OA}/fields/{fid}") or {}).get("display_name") or str(fid)

def sample_block(fid,year,block):
    seed=600624000 + fid*100000 + year*10 + block
    filt=",".join([
        "authorships.institutions.country_code:CN",
        f"primary_topic.field.id:{fid}",
        "type:article|conference-paper",
        f"from_publication_date:{year}-01-01",
        f"to_publication_date:{year}-12-31",
    ])
    p={"filter":filt,"select":"id,doi,authorships","sample":100,"seed":seed,"per_page":100}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    return (get_json(OA+"/works?"+urllib.parse.urlencode(p)) or {}).get("results") or []

def crossref(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get_json(CR+urllib.parse.quote(doi,safe=""))
    time.sleep(.012)
    return (d or {}).get("message") or None

def canonicalize_ids(raw_ids):
    ids=sorted({short(x) for x in raw_ids if short(x)})
    mapping={}
    for k in range(0,len(ids),100):
        chunk=ids[k:k+100]
        p={"filter":"openalex:"+"|".join(chunk),"per_page":100,"select":"id"}
        if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
        d=get_json(OA+"/authors?"+urllib.parse.urlencode(p,safe="|:"))
        returned={short(x.get("id")) for x in (d or {}).get("results") or [] if x.get("id")}
        for aid in chunk:
            if aid in returned:mapping[aid]=aid
        for aid in (x for x in chunk if x not in mapping):
            one=get_json(OA+"/authors/"+urllib.parse.quote(aid,safe=""))
            cid=short((one or {}).get("id"))
            if cid:mapping[aid]=cid
            time.sleep(.004)
    return mapping

def order_and_focal(family,raw_name,han_to_py,roman):
    """Return (order_key, focal_map_or_none, compatible)."""
    fam=str(family or "").strip()
    if not fam:return "",None,False
    raw=str(raw_name or "")
    if fam in han_to_py:
        key=han_to_py[fam]
        compatible=(fam in raw) or (key and key in norm_latin(raw))
        focal={"route":"direct_han","order_key":key,"population_n":None,"han":fam}
        return key,focal,compatible
    lat=norm_latin(fam)
    if not lat:return "",None,False
    compatible=lat in norm_latin(raw)
    focal=None
    if lat in roman:
        focal={"route":"canonical_romanized","order_key":lat,"population_n":roman[lat]["population_n"],"han":""}
    return lat,focal,compatible

def midranks(keys):
    by=defaultdict(list)
    for i,k in enumerate(sorted(keys)):
        by[k].append(i)
    denom=len(keys)-1
    return {k:(sum(v)/len(v))/denom for k,v in by.items()}

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--field-id",type=int,required=True)
    ap.add_argument("--familyname-csv",required=True)
    ap.add_argument("--ccnc-json",required=True)
    ap.add_argument("--target-works",type=int,default=40)
    ap.add_argument("--min-cell-works",type=int,default=20)
    ap.add_argument("--max-blocks",type=int,default=5)
    ap.add_argument("--outdir",required=True)
    a=ap.parse_args()

    pop,han_to_py,roman=load_maps(a.familyname_csv,a.ccnc_json)
    fname=field_name(a.field_id)
    summaries=[];focal_rows=[];work_rows=[];all_excl=Counter()

    for year in range(2011,2026):
        seen=set();accepted=[];excl=Counter();raw_sampled=0
        for block in range(1,a.max_blocks+1):
            works=sample_block(a.field_id,year,block);raw_sampled+=len(works)
            candidates=[]
            focal_raw_ids=[]
            for w in works:
                wid=short(w.get("id"))
                if not wid or wid in seen:
                    excl["duplicate_or_missing_work_id"]+=1;continue
                seen.add(wid)
                auth=w.get("authorships") or []
                if len(auth)<2:
                    excl["single_author"]+=1;continue
                if len(auth)>=100:
                    excl["authorship_cap_or_100plus"]+=1;continue
                if not w.get("doi"):
                    excl["no_doi"]+=1;continue
                cr=crossref(w["doi"])
                if not cr:
                    excl["crossref_missing"]+=1;continue
                ca=cr.get("author") or []
                if len(ca)!=len(auth):
                    excl["author_count_mismatch"]+=1;continue

                keys=[];focals=[];bad=False
                for idx,(oa_row,cr_row) in enumerate(zip(auth,ca)):
                    raw_name=oa_row.get("raw_author_name") or (oa_row.get("author") or {}).get("display_name") or ""
                    key,focal,compat=order_and_focal(cr_row.get("family"),raw_name,han_to_py,roman)
                    if not key:
                        excl["unreconstructable_family_order_key"]+=1;bad=True;break
                    if not compat:
                        excl["position_name_incompatibility"]+=1;bad=True;break
                    keys.append(key)
                    if authorship_is_cn(oa_row) and focal is not None:
                        rid=short((oa_row.get("author") or {}).get("id"))
                        if not rid:
                            excl["focal_missing_openalex_author_id"]+=1;bad=True;break
                        focal2=dict(focal)
                        focal2.update({"index":idx,"raw_author_id":rid})
                        if focal2["route"]=="direct_han":
                            focal2["population_n"]=pop[focal2["han"]]
                        focals.append(focal2)
                if bad:continue
                if len(focals)<2:
                    excl["fewer_than_2_focal_rows"]+=1;continue
                ranks=midranks(keys)
                for z in focals:z["rel_alpha_rank"]=ranks[z["order_key"]]
                if len({round(z["rel_alpha_rank"],12) for z in focals})<2:
                    excl["no_focal_within_work_rank_variation"]+=1;continue
                focal_raw_ids.extend(z["raw_author_id"] for z in focals)
                candidates.append({"work_id":wid,"team_size":len(auth),"keys":keys,"focals":focals})

            mp=canonicalize_ids(focal_raw_ids)
            for w in candidates:
                ok=True;canon=[]
                for z in w["focals"]:
                    cid=mp.get(z["raw_author_id"],"")
                    if not cid:
                        ok=False;break
                    z["canonical_author_id"]=cid;canon.append(cid)
                if not ok:
                    excl["focal_canonicalization_failure"]+=1;continue
                if len(set(canon))<len(canon):
                    excl["duplicate_canonical_focal_author_within_work"]+=1;continue
                accepted.append(w)
                if len(accepted)>=a.target_works:break

            if len(accepted)>=a.target_works:break

        accepted=accepted[:a.target_works]
        status="target_met" if len(accepted)>=a.target_works else ("retain_below_target" if len(accepted)>=a.min_cell_works else "exclude_below_minimum")
        kept=accepted if status!="exclude_below_minimum" else []
        for w in kept:
            work_rows.append({
                "field_id":a.field_id,"field_name":fname,"year":year,
                "work_id":w["work_id"],"team_size":w["team_size"],
                "focal_rows":len(w["focals"]),"cell_status":status,
            })
            for z in w["focals"]:
                rank=ord(z["order_key"][0])-96
                focal_rows.append({
                    "field_id":a.field_id,"field_name":fname,"year":year,
                    "work_id":w["work_id"],"team_size":w["team_size"],
                    "canonical_author_id":z["canonical_author_id"],
                    "surname_route":z["route"],
                    "surname_initial_rank":rank,
                    "surname_initial_rank_norm":(rank-1)/25,
                    "surname_population_n":z["population_n"],
                    "rel_alpha_rank":z["rel_alpha_rank"],
                    "listed_position_norm":z["index"]/(w["team_size"]-1),
                    "first_listed":int(z["index"]==0),
                    "cell_status":status,
                })

        summaries.append({
            "field_id":a.field_id,"field_name":fname,"year":year,
            "blocks_used":block,"raw_sampled_works":raw_sampled,"unique_sampled_works":len(seen),
            "informative_eligible_works_found":len(accepted),
            "works_retained":len(kept),
            "focal_rows_retained":sum(len(w["focals"]) for w in kept),
            "unique_focal_authors_retained":len({z["canonical_author_id"] for w in kept for z in w["focals"]}),
            "cell_status":status,
        })
        all_excl.update(excl)
        print(json.dumps(summaries[-1],ensure_ascii=False))

    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    write_csv(out/"field_year_counts.csv",summaries)
    write_csv(out/"primary_focal_rows.csv",focal_rows)
    write_csv(out/"primary_work_rows.csv",work_rows)
    manifest={
        "script":"24_materialize_primary_frame.py",
        "confirmatory_effect_estimation_allowed":False,
        "field_id":a.field_id,"field_name":fname,
        "focal_years":[2011,2025],
        "target_works_per_field_year":a.target_works,
        "minimum_works_per_field_year":a.min_cell_works,
        "max_blocks":a.max_blocks,
        "field_year_cells":len(summaries),
        "cells_target_met":sum(x["cell_status"]=="target_met" for x in summaries),
        "cells_retained_below_target":sum(x["cell_status"]=="retain_below_target" for x in summaries),
        "cells_excluded_below_minimum":sum(x["cell_status"]=="exclude_below_minimum" for x in summaries),
        "works_retained":len(work_rows),
        "focal_rows_retained":len(focal_rows),
        "unique_focal_authors_retained":len({x["canonical_author_id"] for x in focal_rows}),
        "exclusions":dict(all_excl),
        "surname_map":"aris4c006-surname-map-v2-ccnc",
        "effects_or_pvalues_computed":False,
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
