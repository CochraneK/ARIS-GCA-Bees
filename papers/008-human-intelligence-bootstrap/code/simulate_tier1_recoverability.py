"""Tier-1 recoverability stress test for ARIS4C008.

Zero third-party dependencies: Python standard library only.

Design diagnostic only -- not a biological power analysis.

Scenarios:
1) Pilot-7 current 29-taxon observed mask.
2) Tier-1 empirical 79-taxon mask.
3) Tier-1 after deep-coding A-F for the 50 new taxa.
4) Tier-1 after deep-coding A-F for all 79 taxa.
5) Tier-1 complete 79 x 10 benchmark.
"""
from __future__ import annotations
import argparse, csv, math, random, statistics
from collections import Counter, defaultdict
from pathlib import Path

SEED=20260918
MODULES=list("ABCDEFGHIJ")
MODELS=("additive","weakest","threshold","interaction")
OBSERVED_STATES={
 "measured","partial_measured","measured_multi_axis","measured_ecology",
 "measured_network_proxy","measured_multi_source_proxy","measured_social_demography",
 "measured_cultural_context","positive","positive_with_uncertainty",
 "tested_negative","ambiguous"
}

def model_features(row,model):
    mean=sum(row)/len(row); mn=min(row)
    if model=="additive": return [mean]
    if model=="weakest": return [mn]
    if model=="threshold": return [sum(x>=0.6 for x in row)/len(row),mn]
    if model=="interaction": return [mean,mn,sum(x*x for x in row)/len(row)]
    raise ValueError(model)

def outcome(X,true_model,rng):
    y=[]
    for row in X:
        mean=sum(row)/len(row); mn=min(row)
        if true_model=="additive": z=mean
        elif true_model=="weakest": z=mn
        elif true_model=="threshold":
            k=sum(x>=0.6 for x in row)
            z=0.15*mean+0.85/(1+math.exp(-(k-6.5)*2))
        else: raise ValueError(true_model)
        y.append(z+rng.gauss(0,0.07))
    return y

def solve(A,b):
    n=len(b)
    M=[list(A[i])+[b[i]] for i in range(n)]
    for i in range(n):
        p=max(range(i,n),key=lambda r:abs(M[r][i]))
        M[i],M[p]=M[p],M[i]
        if abs(M[i][i])<1e-10: M[i][i]+=1e-8
        q=M[i][i]
        for j in range(i,n+1): M[i][j]/=q
        for r in range(n):
            if r==i: continue
            q=M[r][i]
            for j in range(i,n+1): M[r][j]-=q*M[i][j]
    return [M[i][n] for i in range(n)]

def ols_fit(F,y):
    X=[[1.0]+list(r) for r in F]
    p=len(X[0])
    xtx=[[0.0]*p for _ in range(p)]
    xty=[0.0]*p
    for row,yy in zip(X,y):
        for i in range(p):
            xty[i]+=row[i]*yy
            for j in range(p): xtx[i][j]+=row[i]*row[j]
    for i in range(p): xtx[i][i]+=1e-9
    return solve(xtx,xty)

def predict(F,beta):
    return [beta[0]+sum(b*x for b,x in zip(beta[1:],r)) for r in F]

def cv_rmse(F,y,folds):
    n=len(y); allidx=set(range(n)); errs=[]
    for te in folds:
        teset=set(te); tr=sorted(allidx-teset)
        beta=ols_fit([F[i] for i in tr],[y[i] for i in tr])
        pred=predict([F[i] for i in te],beta)
        errs.append(math.sqrt(sum((y[i]-p)**2 for i,p in zip(te,pred))/len(te)))
    return sum(errs)/len(errs)

def make_latent(n,rng):
    X=[]
    for _ in range(n):
        shared=rng.betavariate(2,2)
        row=[]
        for _ in MODULES:
            raw=rng.betavariate(1.5,1.5)
            row.append(max(0,min(1,0.25*shared+0.75*raw)))
        X.append(row)
    return X

def noisy_observed(X,mask,rng):
    Z=[]
    for row,mrow in zip(X,mask):
        Z.append([max(0,min(1,x+rng.gauss(0,0.08))) if obs else None for x,obs in zip(row,mrow)])
    means=[]
    for j in range(len(MODULES)):
        xs=[row[j] for row in Z if row[j] is not None]
        means.append(sum(xs)/len(xs) if xs else 0.5)
    return [[means[j] if x is None else x for j,x in enumerate(row)] for row in Z]

def make_folds(n,rng,k=4):
    idx=list(range(n)); rng.shuffle(idx)
    return [idx[i::k] for i in range(k)]

def evaluate_once(mask,rng):
    n=len(mask)
    X=make_latent(n,rng); Z=noisy_observed(X,mask,rng)
    folds=make_folds(n,rng)
    Fs={m:[model_features(row,m) for row in Z] for m in MODELS}
    ans=[]
    for true in ("additive","weakest","threshold"):
        y=outcome(X,true,rng)
        scores={m:cv_rmse(Fs[m],y,folds) for m in MODELS}
        ordered=sorted(scores.items(),key=lambda kv:kv[1])
        ans.append((true,ordered[0][0],ordered[1][1]-ordered[0][1]))
    return ans

def run(mask,reps,seed):
    rng=random.Random(seed); wins=Counter(); confusion=Counter(); margins=defaultdict(list)
    for _ in range(reps):
        for true,pred,margin in evaluate_once(mask,rng):
            confusion[(true,pred)]+=1
            if true==pred:wins[true]+=1
            margins[true].append(margin)
    return {
      "recovery":{m:wins[m]/reps for m in ("additive","weakest","threshold")},
      "confusion":confusion,
      "margin":{m:statistics.median(margins[m]) for m in margins}
    }

def read_pilot7(path):
    rows=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    taxa=list(dict.fromkeys(r["scientific_name"] for r in rows))
    by={(r["scientific_name"],r["module_id"]):r for r in rows}
    mask=[]
    for sp in taxa:
        rr=[]
        for m in MODULES:
            r=by[(sp,m)]
            rr.append(r["evidence_state"] in OBSERVED_STATES or bool((r.get("measurement_coverage") or "").strip()))
        mask.append(rr)
    return taxa,mask

def read_tier1(path):
    rows=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    taxa=list(dict.fromkeys(r["scientific_name"] for r in rows))
    by={(r["scientific_name"],r["module_id"]):r for r in rows}
    segment={sp:next(r["matrix_segment"] for r in rows if r["scientific_name"]==sp) for sp in taxa}
    mask=[[str(by[(sp,m)]["observed_now"]).strip()=="1" for m in MODULES] for sp in taxa]
    return taxa,segment,mask

def clone(mask): return [list(r) for r in mask]

def scenarios(base):
    _,m29=read_pilot7(base/"data"/"module_evidence_state_v2.csv")
    taxa79,seg,m79=read_tier1(base/"data"/"module_evidence_state_tier1_v0.csv")

    new50=clone(m79)
    for i,sp in enumerate(taxa79):
        if seg[sp]=="tier1_new50":
            for j in range(6):new50[i][j]=True

    allaf=clone(m79)
    for row in allaf:
        for j in range(6):row[j]=True

    complete=[[True]*len(MODULES) for _ in m79]
    return {
      "pilot7_current29":m29,
      "tier1_empirical79":m79,
      "tier1_new50_AF_complete":new50,
      "tier1_all79_AF_complete":allaf,
      "tier1_complete79":complete,
    }

def main():
    base=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser();ap.add_argument("--reps",type=int,default=500);args=ap.parse_args()
    allsc=scenarios(base);summary=[];confusion=[]
    for si,(name,mask) in enumerate(allsc.items()):
        res=run(mask,args.reps,SEED+si*10000)
        n=len(mask); total=n*len(MODULES); observed=sum(sum(r) for r in mask)
        permod=[sum(row[j] for row in mask) for j in range(len(MODULES))]
        for true,rate in res["recovery"].items():
            row={"scenario":name,"n_taxa":n,"observed_cells":observed,"total_cells":total,
                 "coverage":observed/total,"true_model":true,"recovery_rate":rate,
                 "median_winner_margin_rmse":res["margin"][true]}
            row.update({f"coverage_{m}":permod[j] for j,m in enumerate(MODULES)})
            summary.append(row)
        for (true,pred),count in res["confusion"].items():
            confusion.append({"scenario":name,"true_model":true,"selected_model":pred,"count":count,"reps":args.reps})
    fields=list(summary[0])
    with open(base/"data"/"tier1_recoverability_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(summary)
    fields2=["scenario","true_model","selected_model","count","reps"]
    with open(base/"data"/"tier1_recoverability_confusion_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields2);w.writeheader();w.writerows(confusion)
    print("SCENARIOS")
    for name,mask in allsc.items():
        observed=sum(sum(r) for r in mask);total=len(mask)*len(MODULES)
        permod=[sum(row[j] for row in mask) for j in range(len(MODULES))]
        rr={r["true_model"]:r["recovery_rate"] for r in summary if r["scenario"]==name}
        print(name,"n",len(mask),"coverage",round(observed/total,4),"per_module",dict(zip(MODULES,permod)))
        print(" recovery",rr)

if __name__=="__main__":
    main()
