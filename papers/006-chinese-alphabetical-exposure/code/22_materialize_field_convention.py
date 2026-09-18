#!/usr/bin/env python3
"""ARIS4C006 — final outcome-blind field convention materialization.

Per one OpenAlex primary-topic field:
- reproducibly sample annual CN-affiliated article/conference-paper works,
- reconstruct full structured bylines through Crossref,
- chance-correct alphabetical ordering,
- canonicalize embedded OpenAlex author IDs,
- store annual and rolling field convention evidence plus work contributions.

NO focal surname/outcome coefficients are computed.
"""
from __future__ import annotations
import argparse,csv,json,math,os,re,time,unicodedata,urllib.parse,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

OA="https://api.openalex.org"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.22 final-convention-materialization"

def get_json(url,retries=5):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=75) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(min(8.0,.8*(2**i)))
    return None

def short(s):
    return (s or "").rstrip("/").split("/")[-1]

def norm_family(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",str(s))
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z0-9]","",s)

def chance(keys):
    n=len(keys)
    num=1
    for m in Counter(keys).values():
        num*=math.factorial(m)
    return num/math.factorial(n)

def field_name(fid):
    d=get_json(f"{OA}/fields/{fid}")
    return (d or {}).get("display_name") or str(fid)

def sample_block(fid,year,block):
    seed=600622000 + fid*100000 + year*10 + block
    filt=",".join([
        "authorships.institutions.country_code:CN",
        f"primary_topic.field.id:{fid}",
        "type:article|conference-paper",
        f"from_publication_date:{year}-01-01",
        f"to_publication_date:{year}-12-31",
    ])
    p={
        "filter":filt,
        "select":"id,doi,authorships",
        "sample":100,
        "seed":seed,
        "per_page":100,
    }
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    return (get_json(OA+"/works?"+urllib.parse.urlencode(p)) or {}).get("results") or []

def crossref(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get_json(CR+urllib.parse.quote(doi,safe=""))
    time.sleep(.015)
    return (d or {}).get("message") or None

def canonicalize_ids(raw_ids):
    """Map raw embedded OpenAlex author IDs to current canonical IDs.

    Fast path: batch openalex filter. Any raw ID not returned literally is
    singleton-resolved because it may be an obsolete merged alias.
    """
    ids=sorted({short(x) for x in raw_ids if short(x)})
    mapping={}
    for k in range(0,len(ids),100):
        chunk=ids[k:k+100]
        p={
            "filter":"openalex:"+"|".join(chunk),
            "per_page":100,
            "select":"id",
        }
        if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
        url=OA+"/authors?"+urllib.parse.urlencode(p,safe="|:")
        d=get_json(url)
        returned={short(x.get("id")) for x in (d or {}).get("results") or [] if x.get("id")}
        for aid in chunk:
            if aid in returned:
                mapping[aid]=aid
        missing=[aid for aid in chunk if aid not in mapping]
        for aid in missing:
            one=get_json(OA+"/authors/"+urllib.parse.quote(aid,safe=""))
            cid=short((one or {}).get("id"))
            if cid:mapping[aid]=cid
            time.sleep(.005)
    return mapping

def reconstruct_candidates(works,seen,excl):
    """Return structured-order candidates before canonical author resolution."""
    out=[]
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
        keys=[norm_family(x.get("family")) for x in ca]
        if any(not x for x in keys):
            excl["missing_structured_family"]+=1;continue
        compatible=True
        for oa_row,fam in zip(auth,keys):
            raw_name=norm_family(
                oa_row.get("raw_author_name")
                or (oa_row.get("author") or {}).get("display_name")
                or ""
            )
            if not raw_name or fam not in raw_name:
                compatible=False
                break
        if not compatible:
            excl["position_name_incompatibility"]+=1;continue
        rawids=[short((x.get("author") or {}).get("id")) for x in auth]
        if any(not x for x in rawids):
            excl["missing_openalex_author_id"]+=1;continue
        pc=chance(keys)
        ia=int(all(keys[i]<=keys[i+1] for i in range(len(keys)-1)))
        out.append({
            "work_id":wid,
            "team_size":len(keys),
            "i_alpha":ia,
            "p_chance":pc,
            "num":ia-pc,
            "den":1-pc,
            "raw_author_ids":rawids,
        })
    return out

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--field-id",type=int,required=True)
    ap.add_argument("--start-year",type=int,default=2008)
    ap.add_argument("--end-year",type=int,default=2024)
    ap.add_argument("--annual-D",type=float,default=35.0)
    ap.add_argument("--annual-D3",type=float,default=20.0)
    ap.add_argument("--max-blocks",type=int,default=4)
    ap.add_argument("--outdir",required=True)
    a=ap.parse_args()

    fname=field_name(a.field_id)
    annual=[];workrows=[];all_excl=Counter()

    for year in range(a.start_year,a.end_year+1):
        seen=set();accepted=[];excl=Counter()
        sampled_total=0
        for block in range(1,a.max_blocks+1):
            works=sample_block(a.field_id,year,block)
            sampled_total+=len(works)
            cand=reconstruct_candidates(works,seen,excl)
            raw=[rid for x in cand for rid in x["raw_author_ids"]]
            mp=canonicalize_ids(raw)
            for x in cand:
                canonical=[mp.get(rid,"") for rid in x["raw_author_ids"]]
                if any(not z for z in canonical):
                    excl["canonical_author_resolution_failure"]+=1
                    continue
                x["canonical_author_ids"]=sorted(set(canonical))
                accepted.append(x)

            D=sum(x["den"] for x in accepted)
            D3=sum(x["den"] for x in accepted if x["team_size"]>=3)
            if D>=a.annual_D and D3>=a.annual_D3:
                break

        N=sum(x["num"] for x in accepted)
        D=sum(x["den"] for x in accepted)
        N3=sum(x["num"] for x in accepted if x["team_size"]>=3)
        D3=sum(x["den"] for x in accepted if x["team_size"]>=3)

        annual.append({
            "field_id":a.field_id,
            "field_name":fname,
            "year":year,
            "blocks_used":block,
            "sampled_raw_works":sampled_total,
            "unique_sampled_works":len(seen),
            "valid_convention_works":len(accepted),
            "valid_3plus_works":sum(x["team_size"]>=3 for x in accepted),
            "N":N,"D":D,
            "excess_alpha":N/D if D else None,
            "N3":N3,"D3":D3,
            "excess_alpha_3plus":N3/D3 if D3 else None,
            "annual_target_met":D>=a.annual_D and D3>=a.annual_D3,
        })
        for x in accepted:
            workrows.append({
                "field_id":a.field_id,
                "field_name":fname,
                "year":year,
                "work_id":x["work_id"],
                "team_size":x["team_size"],
                "i_alpha":x["i_alpha"],
                "p_chance":x["p_chance"],
                "num":x["num"],
                "den":x["den"],
                "canonical_author_ids":";".join(x["canonical_author_ids"]),
            })
        all_excl.update(excl)
        print(json.dumps(annual[-1],ensure_ascii=False))

    byyear={x["year"]:x for x in annual}
    rolling=[]
    for target in range(2011,2026):
        ys=[target-3,target-2,target-1]
        rr=[byyear.get(y) for y in ys]
        if any(x is None for x in rr):continue
        N=sum(x["N"] for x in rr);D=sum(x["D"] for x in rr)
        N3=sum(x["N3"] for x in rr);D3=sum(x["D3"] for x in rr)
        rolling.append({
            "field_id":a.field_id,
            "field_name":fname,
            "target_year":target,
            "lag_start":target-3,
            "lag_end":target-1,
            "N":N,"D":D,
            "excess_alpha":N/D if D else None,
            "primary_full_field_supported":D>=50,
            "N3":N3,"D3":D3,
            "excess_alpha_3plus":N3/D3 if D3 else None,
            "robustness_3plus_supported":D3>=50,
        })

    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    write_csv(out/"annual_convention.csv",annual)
    write_csv(out/"rolling_exposure.csv",rolling)
    write_csv(out/"convention_work_contributions.csv",workrows)

    manifest={
        "script":"22_materialize_field_convention.py",
        "confirmatory_use_allowed":False,
        "field_id":a.field_id,
        "field_name":fname,
        "source_years":[a.start_year,a.end_year],
        "focal_years":[2011,2025],
        "annual_information_targets":{"D":a.annual_D,"D3":a.annual_D3},
        "max_blocks_per_field_year":a.max_blocks,
        "annual_cells":len(annual),
        "annual_cells_target_met":sum(bool(x["annual_target_met"]) for x in annual),
        "rolling_cells":len(rolling),
        "rolling_primary_supported":sum(bool(x["primary_full_field_supported"]) for x in rolling),
        "rolling_3plus_supported":sum(bool(x["robustness_3plus_supported"]) for x in rolling),
        "valid_convention_works":len(workrows),
        "unique_canonical_authors_in_convention_sample":len({a for w in workrows for a in w["canonical_author_ids"].split(";") if a}),
        "exclusions":dict(all_excl),
        "field_assignment":"primary_topic.field.id",
        "work_types":["article","conference-paper"],
        "china_filter":"at least one CN-affiliated authorship",
        "authorship_cap_rule":"exclude len(authorships)>=100",
        "outcomes_opened":False,
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
