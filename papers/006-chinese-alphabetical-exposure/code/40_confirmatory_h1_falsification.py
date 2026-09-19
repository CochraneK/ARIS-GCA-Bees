#!/usr/bin/env python3
"""ARIS4C006 — post-lock future-exposure placebo + team-preserving permutation.

Requires valid preregistration lock + explicit unlock. This is a falsification
diagnostic only and cannot redefine the frozen H1 estimand.

Outputs:
1) future LOAO exposure frame (field convention from t+1..t+3, where observable);
2) field-year past/future persistence summary;
3) deterministic within-work permutation distribution for the frozen H1 beta.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,subprocess,sys
from collections import defaultdict
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PROC=ROOT/"process"

def read_csv(path):
    with Path(path).open(encoding="utf-8",newline="") as h:
        return list(csv.DictReader(h))

def write_csv(path,rows):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        path.write_text("",encoding="utf-8"); return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def verify():
    p=subprocess.run([sys.executable,str(ROOT/"code"/"31_verify_prereg_lock.py"),"--require-unlock"],
                     capture_output=True,text=True)
    if p.returncode!=0:
        raise SystemExit("LOCKED/INVALID PREREG STATE:\n"+p.stdout+"\n"+p.stderr)
    return json.loads((PROC/"PREREGISTRATION_LOCK.json").read_text(encoding="utf-8"))

def pearson(a,b):
    if len(a)<2:return None
    x=np.asarray(a,float); y=np.asarray(b,float)
    if np.std(x)==0 or np.std(y)==0:return None
    return float(np.corrcoef(x,y)[0,1])

def demean_by_work(values,groups):
    v=np.asarray(values,float)
    out=np.empty_like(v)
    buckets=defaultdict(list)
    for i,g in enumerate(groups): buckets[g].append(i)
    for inds in buckets.values():
        arr=v[inds]; out[inds]=arr-arr.mean()
    return out

def ols_interaction_beta(y,rank,exp,work):
    ydm=demean_by_work(y,work)
    x1=demean_by_work(rank,work)
    x2=demean_by_work(np.asarray(rank)*np.asarray(exp),work)
    X=np.column_stack([x1,x2])
    b=np.linalg.lstsq(X,ydm,rcond=None)[0]
    return float(b[1])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--loao-frame",required=True)
    ap.add_argument("--convention-contributions",required=True)
    ap.add_argument("--rolling-past",required=True)
    ap.add_argument("--outdir",required=True)
    ap.add_argument("--permutations",type=int,default=1000)
    a=ap.parse_args()

    lock=verify()
    focal=read_csv(a.loao_frame)
    contrib=read_csv(a.convention_contributions)
    rolling=read_csv(a.rolling_past)

    # Future field-window totals: convention works t+1..t+3, only fully observed
    # when t+3 <= max convention year.
    years=[int(r["year"]) for r in contrib]
    max_year=max(years)
    future_totals=defaultdict(lambda:[0.0,0.0])
    future_own=defaultdict(lambda:[0.0,0.0])
    for r in contrib:
        field=int(r["field_id"]); y=int(r["year"])
        num=float(r["num"]); den=float(r["den"])
        authors={x for x in str(r.get("canonical_author_ids") or "").split(";") if x}
        # A convention work in y contributes to focal future window targets y-1,y-2,y-3.
        for target in (y-1,y-2,y-3):
            if target < 2011 or target+3>max_year: continue
            z=future_totals[(field,target)]; z[0]+=num; z[1]+=den
            for aid in authors:
                q=future_own[(aid,field,target)]; q[0]+=num; q[1]+=den

    future_rows=[]
    for r in focal:
        field=int(r["field_id"]); year=int(r["year"]); aid=r["canonical_author_id"]
        if year+3>max_year: continue
        t=future_totals.get((field,year))
        if not t: continue
        own=future_own.get((aid,field,year),(0.0,0.0))
        D=t[1]-own[1]
        if D<50: continue
        q=dict(r)
        q["future_loao_exposure"]=(t[0]-own[0])/D
        q["future_loao_D"]=D
        future_rows.append(q)
    out=Path(a.outdir); out.mkdir(parents=True,exist_ok=True)
    write_csv(out/"future_loao_frame.csv",future_rows)

    # Persistence of regime at field-year level: compare frozen prior exposure
    # against future t+1..t+3 exposure, without author-specific subtraction.
    past={(int(r["field_id"]),int(r["target_year"])):float(r["excess_alpha"])
          for r in rolling if str(r.get("excess_alpha","")).strip() not in {"","None","nan"}}
    pers=[]
    pa=[]; fu=[]
    for key,pv in sorted(past.items()):
        t=future_totals.get(key)
        if not t or t[1]<50: continue
        fv=t[0]/t[1]
        pers.append({"field_id":key[0],"year":key[1],"prior_exposure":pv,
                     "future_exposure":fv,"future_D":t[1]})
        pa.append(pv); fu.append(fv)
    write_csv(out/"field_year_prior_future_exposure.csv",pers)

    # Deterministic within-work rank permutation using the committed lock SHA.
    seed=int(lock["combined_sha256"][:8],16)
    rng=np.random.default_rng(seed)
    y=np.array([float(r["listed_position_norm"]) for r in focal])
    rank=np.array([float(r["rel_alpha_rank"]) for r in focal])
    exp=np.array([float(r["loao_exposure"]) for r in focal])
    work=np.array([r["work_id"] for r in focal],dtype=object)

    observed=ols_interaction_beta(y,rank,exp,work)
    buckets=defaultdict(list)
    for i,g in enumerate(work): buckets[g].append(i)
    perm=[]
    for b in range(a.permutations):
        rp=rank.copy()
        for inds in buckets.values():
            if len(inds)>1:
                rp[inds]=rng.permutation(rp[inds])
        perm.append(ols_interaction_beta(y,rp,exp,work))
    perm=np.asarray(perm)
    extreme=int(np.sum(np.abs(perm)>=abs(observed)))
    pplus=(extreme+1)/(a.permutations+1)
    write_csv(out/"permutation_distribution.csv",
              [{"permutation":i+1,"beta_interaction":float(v)} for i,v in enumerate(perm)])

    manifest={
      "script":"40_confirmatory_h1_falsification.py",
      "prereg_lock_label":lock["lock_label"],
      "prereg_lock_sha256":lock["combined_sha256"],
      "confirmatory_unlock_verified":True,
      "future_placebo_rows":len(future_rows),
      "future_placebo_works":len({r["work_id"] for r in future_rows}),
      "field_year_prior_future_pairs":len(pers),
      "field_year_prior_future_pearson":pearson(pa,fu),
      "permutation_seed_source":"first 8 hex chars of prereg combined SHA256",
      "permutation_seed":seed,
      "permutations":a.permutations,
      "observed_h1_beta_recomputed":observed,
      "permutation_beta_mean":float(np.mean(perm)),
      "permutation_beta_sd":float(np.std(perm,ddof=1)),
      "permutation_beta_min":float(np.min(perm)),
      "permutation_beta_max":float(np.max(perm)),
      "two_sided_extreme_count":extreme,
      "randomization_p_plus1":pplus,
      "note":"Future exposure is a placebo/proxy diagnostic, not a replacement exposure. A strong result can arise if field conventions are persistent; prior-future correlation is reported explicitly."
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
