"""Tier-1 recoverability stress test for ARIS4C008.

Design diagnostic only -- not a biological power analysis.

Scenarios:
1) Pilot-7 current 29-taxon observed mask.
2) Tier-1 empirical 79-taxon mask.
3) Tier-1 after deep-coding A-F for the 50 new taxa.
4) Tier-1 after deep-coding A-F for all 79 taxa.
5) Tier-1 complete 79 x 10 benchmark.

The simulation uses the same simplified architecture family as the Pilot-7
recoverability diagnostic, so differences among scenarios are interpretable
as design/missingness effects rather than a change of model family.
"""
from __future__ import annotations
import argparse, csv
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

SEED=20260918
MODULES=list("ABCDEFGHIJ")
MODELS=("additive","weakest","threshold","interaction")

OBSERVED_STATES={
    "measured","partial_measured","measured_multi_axis","measured_ecology",
    "measured_network_proxy","measured_multi_source_proxy",
    "measured_social_demography","measured_cultural_context",
    "positive","positive_with_uncertainty","tested_negative","ambiguous"
}

def feature(X,model):
    if model=="additive":
        return X.mean(1)[:,None]
    if model=="weakest":
        return X.min(1)[:,None]
    if model=="threshold":
        return np.c_[(X>=0.6).mean(1),X.min(1)]
    if model=="interaction":
        return np.c_[X.mean(1),X.min(1),(X**2).mean(1)]
    raise ValueError(model)

def outcome(X,true_model,rng):
    if true_model=="additive":
        z=X.mean(1)
    elif true_model=="weakest":
        z=X.min(1)
    elif true_model=="threshold":
        k=(X>=0.6).sum(1)
        z=0.15*X.mean(1)+0.85/(1+np.exp(-(k-6.5)*2))
    else:
        raise ValueError(true_model)
    return z+rng.normal(0,0.07,len(X))

def impute_mean(Z):
    Z=Z.copy()
    for j in range(Z.shape[1]):
        miss=np.isnan(Z[:,j])
        if miss.all():
            Z[:,j]=0.5
        elif miss.any():
            Z[miss,j]=np.nanmean(Z[:,j])
    return Z

def cv_rmse(F,y,folds):
    errs=[]
    idx=np.arange(len(y))
    for te in folds:
        tr=np.setdiff1d(idx,te)
        A=np.c_[np.ones(len(tr)),F[tr]]
        B=np.c_[np.ones(len(te)),F[te]]
        beta=np.linalg.lstsq(A,y[tr],rcond=None)[0]
        pred=B@beta
        errs.append(np.sqrt(np.mean((y[te]-pred)**2)))
    return float(np.mean(errs))

def make_latent(n,rng):
    shared=rng.beta(2,2,(n,1))
    raw=rng.beta(1.5,1.5,(n,len(MODULES)))
    return np.clip(0.25*shared+0.75*raw,0,1)

def evaluate_once(mask,rng):
    n=mask.shape[0]
    X=make_latent(n,rng)
    Z=np.clip(X+rng.normal(0,0.08,X.shape),0,1)
    Z[~mask]=np.nan
    Z=impute_mean(Z)
    folds=np.array_split(rng.permutation(n),4)
    F={m:feature(Z,m) for m in MODELS}
    rows=[]
    for true in ("additive","weakest","threshold"):
        y=outcome(X,true,rng)
        scores={m:cv_rmse(F[m],y,folds) for m in MODELS}
        ordered=sorted(scores.items(),key=lambda kv:kv[1])
        rows.append((true,ordered[0][0],ordered[0][1],ordered[1][1]-ordered[0][1]))
    return rows

def run(mask,reps,seed):
    rng=np.random.default_rng(seed)
    wins=Counter()
    confusion=Counter()
    margins=defaultdict(list)
    for _ in range(reps):
        for true,pred,rmse,margin in evaluate_once(mask,rng):
            confusion[(true,pred)]+=1
            if true==pred:
                wins[true]+=1
            margins[true].append(margin)
    return {
        "recovery":{m:wins[m]/reps for m in ("additive","weakest","threshold")},
        "confusion":confusion,
        "margin":{m:float(np.median(margins[m])) for m in margins},
    }

def read_pilot7(path):
    rows=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    taxa=list(dict.fromkeys(r["scientific_name"] for r in rows))
    by={(r["scientific_name"],r["module_id"]):r for r in rows}
    mask=[]
    for sp in taxa:
        row=[]
        for m in MODULES:
            r=by[(sp,m)]
            observed=(r["evidence_state"] in OBSERVED_STATES or bool((r.get("measurement_coverage") or "").strip()))
            row.append(observed)
        mask.append(row)
    return taxa,np.asarray(mask,dtype=bool)

def read_tier1(path):
    rows=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    taxa=list(dict.fromkeys(r["scientific_name"] for r in rows))
    by={(r["scientific_name"],r["module_id"]):r for r in rows}
    segment={sp:next(r["matrix_segment"] for r in rows if r["scientific_name"]==sp) for sp in taxa}
    mask=np.asarray([[str(by[(sp,m)]["observed_now"]).strip()=="1" for m in MODULES] for sp in taxa],dtype=bool)
    return taxa,segment,mask

def scenarios(base):
    taxa29,m29=read_pilot7(base/"data"/"module_evidence_state_v2.csv")
    taxa79,seg,m79=read_tier1(base/"data"/"module_evidence_state_tier1_v0.csv")

    new50_af=m79.copy()
    for i,sp in enumerate(taxa79):
        if seg[sp]=="tier1_new50":
            new50_af[i,:6]=True

    all79_af=m79.copy()
    all79_af[:,:6]=True

    complete=np.ones_like(m79,dtype=bool)
    return {
      "pilot7_current29":m29,
      "tier1_empirical79":m79,
      "tier1_new50_AF_complete":new50_af,
      "tier1_all79_AF_complete":all79_af,
      "tier1_complete79":complete,
    }

def main():
    base=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser()
    ap.add_argument("--reps",type=int,default=500)
    args=ap.parse_args()

    allsc=scenarios(base)
    summary=[]
    confusion=[]
    for si,(name,mask) in enumerate(allsc.items()):
        res=run(mask,args.reps,SEED+si*10000)
        coverage=mask.mean()
        permod=mask.sum(0)
        for true,rate in res["recovery"].items():
            summary.append({
              "scenario":name,"n_taxa":mask.shape[0],"observed_cells":int(mask.sum()),
              "total_cells":int(mask.size),"coverage":coverage,"true_model":true,
              "recovery_rate":rate,"median_winner_margin_rmse":res["margin"][true],
              **{f"coverage_{m}":int(permod[j]) for j,m in enumerate(MODULES)}
            })
        for (true,pred),n in res["confusion"].items():
            confusion.append({"scenario":name,"true_model":true,"selected_model":pred,"count":n,"reps":args.reps})

    fields=list(summary[0])
    with open(base/"data"/"tier1_recoverability_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(summary)
    fields2=["scenario","true_model","selected_model","count","reps"]
    with open(base/"data"/"tier1_recoverability_confusion_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields2);w.writeheader();w.writerows(confusion)

    print("SCENARIOS")
    for name,mask in allsc.items():
        print(name,"n",mask.shape[0],"coverage",round(float(mask.mean()),4),"per_module",dict(zip(MODULES,mask.sum(0).tolist())))
        rr={r["true_model"]:r["recovery_rate"] for r in summary if r["scenario"]==name}
        print(" recovery",rr)

if __name__=="__main__":
    main()
