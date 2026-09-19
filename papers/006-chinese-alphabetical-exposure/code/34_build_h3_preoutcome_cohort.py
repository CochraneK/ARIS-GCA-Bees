#!/usr/bin/env python3
"""ARIS4C006 — outcome-blind H3 cohort materializer.

Requires a valid committed preregistration lock, but NOT confirmatory unlock.
It constructs the frozen nested entry cohort, early LOAO exposure, and identity
risk flags. It explicitly does NOT compute, store, or report Persistence5.

Designed for deterministic author shards; shard outputs can be concatenated
because candidate assignment is by canonical-author hash.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,os,time,urllib.parse,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROC=ROOT/"process"
OA="https://api.openalex.org"
UA="ARIS4C006/0.34 H3-preoutcome-cohort"

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
def truth(x):return str(x).strip().lower()=="true" if isinstance(x,str) else bool(x)

def read_csv(path):
    with Path(path).open(encoding="utf-8",newline="") as h:
        return list(csv.DictReader(h))

def write_csv(path,rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def verify_lock():
    import subprocess,sys
    p=subprocess.run(
        [sys.executable,str(ROOT/"code"/"31_verify_prereg_lock.py")],
        capture_output=True,text=True
    )
    if p.returncode!=0:
        raise SystemExit("INVALID/MISSING PREREG LOCK:\n"+p.stdout+"\n"+p.stderr)
    return json.loads((PROC/"PREREGISTRATION_LOCK.json").read_text(encoding="utf-8"))

def canonicalize_ids(raw_ids):
    ids=sorted({short(x) for x in raw_ids if short(x)})
    mapping={}
    for k in range(0,len(ids),100):
        chunk=ids[k:k+100]
        p={"filter":"openalex:"+"|".join(chunk),"per_page":100,"select":"id,orcid"}
        if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
        d=get_json(OA+"/authors?"+urllib.parse.urlencode(p,safe="|:"))
        for x in (d or {}).get("results") or []:
            cid=short(x.get("id"))
            if cid:mapping[cid]=(cid,x.get("orcid") or "")
        returned=set(mapping)
        for aid in [x for x in chunk if x not in returned]:
            one=get_json(OA+"/authors/"+urllib.parse.quote(aid,safe=""))
            cid=short((one or {}).get("id"))
            if cid:mapping[aid]=(cid,(one or {}).get("orcid") or "")
            time.sleep(.005)
    return mapping

def author_record(aid):
    d=get_json(OA+"/authors/"+urllib.parse.quote(aid,safe=""))
    return d or {}

def field_id(work):
    raw=((work.get("primary_topic") or {}).get("field") or {}).get("id")
    try:return int(short(raw))
    except:return None

def focal_authorship(work,target_aid,cache):
    auth=work.get("authorships") or []
    raws=[short((a.get("author") or {}).get("id")) for a in auth]
    missing=[r for r in raws if r and r not in cache]
    if missing:
        cache.update(canonicalize_ids(missing))
    hits=[]
    for a,rid in zip(auth,raws):
        if not rid:continue
        cid=(cache.get(rid) or ("",""))[0]
        if cid==target_aid:hits.append((a,rid))
    if len(hits)!=1:return None,("duplicate_canonical_authorship" if len(hits)>1 else "focal_authorship_not_found")
    return hits[0],None

def fetch_batch_histories(author_ids,start=2011,end=2025):
    """Fetch eligible works matching any author in a small canonical-ID batch."""
    filt=",".join([
        "author.id:"+"|".join(author_ids),
        "type:article|conference-paper",
        f"from_publication_date:{start}-01-01",
        f"to_publication_date:{end}-12-31",
    ])
    cur="*";out=[]
    while cur:
        p={
            "filter":filt,
            "select":"id,publication_year,publication_date,primary_topic,authorships,type",
            "per_page":100,
            "cursor":cur,
        }
        if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
        d=get_json(OA+"/works?"+urllib.parse.urlencode(p,safe="|:"))
        if not d:break
        rr=d.get("results") or []
        if not rr:break
        out.extend(rr)
        cur=(d.get("meta") or {}).get("next_cursor")
        if not cur:break
    return out

def is_cn_authorship(a):
    return any(i.get("country_code")=="CN" for i in (a.get("institutions") or [])) or "CN" in (a.get("countries") or [])

def institution_country_sets(a):
    inst={short(i.get("id")) for i in (a.get("institutions") or []) if i.get("id")}
    countries={i.get("country_code") for i in (a.get("institutions") or []) if i.get("country_code")}
    countries.update(x for x in (a.get("countries") or []) if x)
    return inst,countries

def shard(aid,index,count):
    return int(hashlib.sha256(aid.encode()).hexdigest()[:16],16)%count==index

def build_exposure_maps(rolling,contrib):
    totals={}
    for r in rolling:
        totals[(int(r["field_id"]),int(r["target_year"]))]={
            "N":float(r["N"]),"D":float(r["D"])
        }
    own=defaultdict(lambda:[0.0,0.0])
    for r in contrib:
        field=int(r["field_id"]);year=int(r["year"])
        num=float(r["num"]);den=float(r["den"])
        authors={x for x in str(r.get("canonical_author_ids") or "").split(";") if x}
        for target in (year+1,year+2,year+3):
            if 2011<=target<=2025:
                for aid in authors:
                    z=own[(aid,field,target)];z[0]+=num;z[1]+=den
    return totals,own

def loao(aid,field,year,totals,own):
    t=totals.get((field,year))
    if not t:return None
    z=own.get((aid,field,year),(0.0,0.0))
    D=t["D"]-z[1]
    if D<50:return None
    return (t["N"]-z[0])/D

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--primary-focal-rows",required=True)
    ap.add_argument("--rolling-exposure",required=True)
    ap.add_argument("--convention-contributions",required=True)
    ap.add_argument("--shard-index",type=int,default=0)
    ap.add_argument("--shard-count",type=int,default=1)
    ap.add_argument("--author-batch-size",type=int,default=20)
    ap.add_argument("--out",required=True)
    ap.add_argument("--manifest",required=True)
    a=ap.parse_args()

    if not 0<=a.shard_index<a.shard_count:raise SystemExit("bad shard")
    lock=verify_lock()
    focal=read_csv(a.primary_focal_rows)
    rolling=read_csv(a.rolling_exposure)
    contrib=read_csv(a.convention_contributions)
    totals,own=build_exposure_maps(rolling,contrib)

    # Candidate authors are unique focal authors sampled in 2014-2020.
    seeds=defaultdict(list)
    for r in focal:
        y=int(r["year"])
        if 2014<=y<=2020:
            seeds[r["canonical_author_id"]].append(r)

    ids=sorted(aid for aid in seeds if shard(aid,a.shard_index,a.shard_count))
    outrows=[];excl=Counter()
    alias_cache={}
    processed=0

    for k in range(0,len(ids),a.author_batch_size):
        batch=ids[k:k+a.author_batch_size]
        works=fetch_batch_histories(batch,2011,2025)
        # Canonicalize work-embedded IDs and assign each work to target candidates.
        byauthor=defaultdict(list)
        raw_ids=[short((au.get("author") or {}).get("id"))
                 for w in works for au in (w.get("authorships") or [])
                 if (au.get("author") or {}).get("id")]
        missing=[x for x in set(raw_ids) if x not in alias_cache]
        if missing:alias_cache.update(canonicalize_ids(missing))
        for w in works:
            seen_targets=set()
            for au in w.get("authorships") or []:
                rid=short((au.get("author") or {}).get("id"))
                cid=(alias_cache.get(rid) or ("",""))[0]
                if cid in batch:
                    if cid in seen_targets:
                        # Preserve duplicate; hard fail is handled per author.
                        byauthor[cid].append((w,None,"duplicate_canonical_authorship"))
                    else:
                        byauthor[cid].append((w,au,None));seen_targets.add(cid)

        for aid in batch:
            processed+=1
            seedrows=seeds[aid]
            seed_years=sorted({int(r["year"]) for r in seedrows})
            earliest_seed=seed_years[0]
            h=byauthor.get(aid,[])
            hard=[]
            if not h:
                excl["no_eligible_history_returned"]+=1;continue
            if any(err for _,_,err in h):
                hard.append("duplicate_canonical_authorship")

            # Canonical entity / ORCID provenance.
            ar=author_record(aid)
            resolved=short(ar.get("id"))
            if not resolved or resolved!=aid:
                hard.append("canonical_author_resolution_failure")
            orcid=ar.get("orcid") or ""
            embedded_ids={short((au.get("author") or {}).get("id"))
                          for _,au,err in h if au and (au.get("author") or {}).get("id")}
            embedded_orcids={(au.get("author") or {}).get("orcid") or ""
                             for _,au,err in h if au}
            embedded_orcids.discard("")
            if orcid and any(x!=orcid for x in embedded_orcids):
                hard.append("orcid_conflict")

            clean=[(w,au) for w,au,err in h if au is not None]
            years=[int(w.get("publication_year") or 0) for w,_ in clean if w.get("publication_year")]
            if not years:
                excl["no_dated_eligible_history"]+=1;continue
            e=min(years)
            if not (2014<=e<=2020):
                excl["entry_year_outside_2014_2020"]+=1;continue
            if e!=earliest_seed:
                excl["sampled_after_validated_entry_year"]+=1;continue

            # Stable surname rank from entry-year primary-frame seed rows.
            entry_seed=[r for r in seedrows if int(r["year"])==e]
            ranks={r["surname_initial_rank_norm"] for r in entry_seed}
            if len(ranks)!=1:
                hard.append("inconsistent_entry_surname_rank")
                rank_norm=""
            else:rank_norm=float(next(iter(ranks)))

            entry_works=[(w,au) for w,au in clean if int(w.get("publication_year") or 0)==e]
            if not any(is_cn_authorship(au) for _,au in entry_works):
                excl["no_CN_affiliated_entry_work"]+=1;continue

            # Earliest entry field: exact publication date, then numeric field ID.
            dated=[]
            for w,au in entry_works:
                fid=field_id(w)
                if fid is None:continue
                date=w.get("publication_date") or f"{e}-12-31"
                dated.append((date,fid,short(w.get("id"))))
            if not dated:
                excl["missing_entry_primary_field"]+=1;continue
            dated.sort(key=lambda z:(z[0],z[1],z[2]))
            entry_field=dated[0][1]
            entry_work_count=len(entry_works)

            # Early CN-affiliated exposure e..e+2.
            exps=[]
            first3_works=0
            annual_counts=Counter()
            annual_inst=defaultdict(set);annual_countries=defaultdict(set)
            aliases=set()
            for w,au in clean:
                y=int(w.get("publication_year") or 0)
                annual_counts[y]+=1
                inst,ctr=institution_country_sets(au)
                annual_inst[y].update(inst);annual_countries[y].update(ctr)
                rid=short((au.get("author") or {}).get("id"))
                if rid:aliases.add(rid)
                if e<=y<=e+2:
                    first3_works+=1
                    if is_cn_authorship(au):
                        fid=field_id(w)
                        if fid is not None:
                            z=loao(aid,fid,y,totals,own)
                            if z is not None:exps.append(z)

            R1=not bool(orcid)
            R2=max(annual_counts.values(),default=0)>100
            R3=max((len(x) for x in annual_inst.values()),default=0)>12
            R4=max((len(x) for x in annual_countries.values()),default=0)>4
            R5=len(aliases)>=2
            R6=first3_works<2
            hard=sorted(set(hard))
            if hard:
                excl["hard_identity_or_integrity_exclusion"]+=1;continue

            validated_entry=True
            if len(exps)<2:
                excl["fewer_than_2_CN_early_exposure_works"]+=1
                final_h3=False
                mean_early=""
            else:
                final_h3=True
                mean_early=sum(exps)/len(exps)

            outrows.append({
                "canonical_author_id":aid,
                "entry_year":e,
                "entry_primary_field":entry_field,
                "entry_field_year_cluster":f"{entry_field}_{e}",
                "entry_work_count":entry_work_count,
                "surname_initial_rank_norm":rank_norm,
                "mean_early_exposure":mean_early,
                "early_exposure_defined_CN_works":len(exps),
                "validated_entry":int(validated_entry),
                "final_h3_eligible_preoutcome":int(final_h3),
                "orcid_anchored":int(not R1),
                "R1_no_orcid":int(R1),
                "R2_extreme_annual_output":int(R2),
                "R3_high_institution_spread":int(R3),
                "R4_high_country_spread":int(R4),
                "R5_alias_history":int(R5),
                "R6_sparse_early_identity":int(R6),
                "low_identity_risk":int(not(R2 or R3 or R4)),
            })

    write_csv(a.out,outrows)
    validated=sum(int(r["validated_entry"]) for r in outrows)
    final=sum(int(r["final_h3_eligible_preoutcome"]) for r in outrows)
    manifest={
        "script":"34_build_h3_preoutcome_cohort.py",
        "prereg_lock_label":lock.get("lock_label"),
        "prereg_lock_sha256":lock.get("combined_sha256"),
        "confirmatory_unlock_required":False,
        "confirmatory_outcomes_unlocked":False,
        "persistence_outcome_computed":False,
        "effect_or_pvalue_computed":False,
        "shard_index":a.shard_index,
        "shard_count":a.shard_count,
        "candidate_seed_authors":len(ids),
        "processed_candidate_authors":processed,
        "validated_entry_authors":validated,
        "final_h3_eligible_preoutcome":final,
        "entry_years":sorted({int(r["entry_year"]) for r in outrows if int(r["validated_entry"])}),
        "entry_fields":sorted({int(r["entry_primary_field"]) for r in outrows if int(r["validated_entry"])}),
        "orcid_anchored_final":sum(int(r["orcid_anchored"]) and int(r["final_h3_eligible_preoutcome"]) for r in outrows),
        "low_identity_risk_final":sum(int(r["low_identity_risk"]) and int(r["final_h3_eligible_preoutcome"]) for r in outrows),
        "exclusions":dict(excl),
        "note":"No e+4/e+5 persistence variable is computed or stored."
    }
    Path(a.manifest).parent.mkdir(parents=True,exist_ok=True)
    Path(a.manifest).write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
