"""Observed-missingness recoverability diagnostic for ARIS4C008.

This is a design diagnostic, not a biological power analysis.

It reads the actual 29 x 10 measurement/evidence mask from
data/module_evidence_state_v2.csv, then asks how often simple candidate
architectures are recovered from simulated latent module profiles.

The model-discriminating selection benchmark is an ORACLE UPPER BOUND because
it selects taxa using their simulated latent configurations. In practice such
selection would require provisional low-cost screening variables.
"""
from __future__ import annotations
import argparse, csv, math
from pathlib import Path
import numpy as np
import pandas as pd

MODULES=list("ABCDEFGHIJ")
CANDIDATES=("additive","weakest","threshold","interaction")

OBSERVED_STATES={
    "measured","partial_measured","measured_multi_axis","measured_ecology",
    "measured_network_proxy","measured_multi_source_proxy",
    "measured_social_demography","measured_cultural_context",
    "positive","positive_with_uncertainty","tested_negative","ambiguous"
}

def is_observed(row):
    return row["evidence_state"] in OBSERVED_STATES or bool(row.get("measurement_coverage","").strip())

def read_mask(path):
    rows=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    taxa=list(dict.fromkeys(r["scientific_name"] for r in rows))
    by={(r["scientific_name"],r["module_id"]):r for r in rows}
    mask=np.array([[is_observed(by[(sp,m)]) for m in MODULES] for sp in taxa],dtype=bool)
    return taxa,mask

def feat(X,model):
    if model=="additive": return X.mean(1)[:,None]
    if model=="weakest": return X.min(1)[:,None]
    if model=="threshold": return np.c_[(X>=0.6).mean(1),X.min(1)]
    if model=="interaction": return np.c_[X.mean(1),X.min(1),(X**2).mean(1)]
    raise ValueError(model)

def gen_y(X,true,rng):
    if true=="additive": z=X.mean(1)
    elif true=="weakest": z=X.min(1)
    elif true=="threshold":
        k=(X>=0.6).sum(1)
        z=.15*X.mean(1)+.85/(1+np.exp(-(k-6.5)*2))
    else: raise ValueError(true)
    return z+rng.normal(0,.07,len(X))

def impute(Z):
    Z=Z.copy()
    for j in range(Z.shape[1]):
        miss=np.isnan(Z[:,j])
        if miss.all(): Z[:,j]=.5
        elif miss.any(): Z[miss,j]=np.nanmean(Z[:,j])
    return Z

def cv_rmse(F,y,folds):
    errs=[]
    idx=np.arange(len(y))
    for te in folds:
        tr=np.setdiff1d(idx,te)
        A=np.c_[np.ones(len(tr)),F[tr]]
        B=np.c_[np.ones(len(te)),F[te]]
        beta=np.linalg.lstsq(A,y[tr],rcond=None)[0]
        errs.append(np.sqrt(np.mean((y[te]-B@beta)**2)))
    return float(np.mean(errs))

def farthest(S,n):
    Z=(S-S.mean(0))/(S.std(0)+1e-9)
    c=Z.mean(0); chosen=[int(np.argmax(((Z-c)**2).sum(1)))]
    d=((Z-Z[chosen[0]])**2).sum(1)
    for _ in range(1,n):
        j=int(np.argmax(d));chosen.append(j)
        d=np.minimum(d,((Z-Z[j])**2).sum(1))
    return np.asarray(chosen)

def choose(pool,n,sampling,rng):
    if sampling=="random": return rng.choice(len(pool),n,replace=False)
    sig=np.c_[pool.mean(1),pool.min(1),(pool>=.6).mean(1),pool.std(1)]
    return farthest(sig,n)

def evaluate(X,Z,reps_rng):
    folds=np.array_split(reps_rng.permutation(len(X)),4)
    Fs={m:feat(Z,m) for m in CANDIDATES}
    out={}
    for true in ("additive","weakest","threshold"):
        y=gen_y(X,true,reps_rng)
        scores={m:cv_rmse(Fs[m],y,folds) for m in CANDIDATES}
        out[true]=min(scores,key=scores.get)==true
    return out

def run_current(mask,reps=500,seed=20260922):
    rng=np.random.default_rng(seed); wins={m:0 for m in ("additive","weakest","threshold")}
    n=mask.shape[0]
    for _ in range(reps):
        latent=rng.beta(2,2,(n,1)); raw=rng.beta(1.5,1.5,(n,len(MODULES)))
        X=np.clip(.25*latent+.75*raw,0,1)
        Z=np.clip(X+rng.normal(0,.08,X.shape),0,1); Z[~mask]=np.nan; Z=impute(Z)
        r=evaluate(X,Z,rng)
        for k,v in r.items(): wins[k]+=v
    return {k:v/reps for k,v in wins.items()}

def run_complete(ns=(29,40,60,80),reps=200,seed=20260921):
    rng=np.random.default_rng(seed); rows=[]
    for n in ns:
        for sampling in ("random","model_discriminating_oracle"):
            wins={m:0 for m in ("additive","weakest","threshold")}
            for _ in range(reps):
                N=1000
                latent=rng.beta(2,2,(N,1));raw=rng.beta(1.5,1.5,(N,len(MODULES)))
                pool=np.clip(.25*latent+.75*raw,0,1)
                sel=choose(pool,n,"random" if sampling=="random" else "oracle",rng)
                X=pool[sel];Z=np.clip(X+rng.normal(0,.08,X.shape),0,1)
                r=evaluate(X,Z,rng)
                for k,v in r.items():wins[k]+=v
            for k,v in wins.items():rows.append((n,sampling,k,v/reps))
    return rows

def main():
    base=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser()
    ap.add_argument("--current-reps",type=int,default=500)
    ap.add_argument("--design-reps",type=int,default=200)
    args=ap.parse_args()
    taxa,mask=read_mask(base/"data"/"module_evidence_state_v2.csv")
    print("taxa",len(taxa),"coverage_by_module",mask.sum(0).tolist(),"overall",mask.mean())
    print("current",run_current(mask,args.current_reps))
    for row in run_complete(reps=args.design_reps):print("complete",row)

if __name__=="__main__":
    main()
