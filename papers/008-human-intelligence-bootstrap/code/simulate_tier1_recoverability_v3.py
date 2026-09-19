"""Architecture-balanced recoverability diagnostic for ARIS4C008 · Pilot 9 update.

Why v3
------
The legacy diagnostic allowed a 3-feature interaction model to compete against
1-2 feature architectures, and the threshold feature set itself included the
minimum. Under complete data, the flexible interaction model frequently won
when weakest-link or threshold was true. That mixes sampling identifiability
with model-class overlap.

This v2 diagnostic asks a narrower design question: can the panel distinguish
three static architecture signatures when all have equal fitted complexity?

- additive: mean of the ten latent modules
- weakest-link: minimum module value
- threshold: fixed nonlinear transition signature based on the number of
  modules above 0.6, with a small mean-performance contribution

Each candidate is fitted as y = intercept + slope * signature.
Feedback/dynamic interaction is deliberately not a fourth static catch-all;
it requires a separately specified temporal/network model.

This is a design diagnostic, not a biological power calculation.\n\nPilot-9 v3 uses common random numbers across fixed-mask scenarios so differences between 79-taxon masks are attributable to missingness/design rather than scenario-specific Monte Carlo draws.
"""
from __future__ import annotations
import argparse,csv,math,random,statistics
from collections import Counter,defaultdict
from pathlib import Path

SEED=20260918
MODULES=list("ABCDEFGHIJ")
MODELS=("additive","weakest","threshold")
OBSERVED_STATES={
 "measured","partial_measured","measured_multi_axis","measured_ecology",
 "measured_network_proxy","measured_multi_source_proxy","measured_social_demography",
 "measured_cultural_context","positive","positive_with_uncertainty",
 "tested_negative","ambiguous"
}

def sigmoid(x):
    if x>=0:
        z=math.exp(-x);return 1/(1+z)
    z=math.exp(x);return z/(1+z)

def signature(row,model):
    mean=sum(row)/len(row)
    if model=="additive": return mean
    if model=="weakest": return min(row)
    if model=="threshold":
        k=sum(x>=0.6 for x in row)
        return 0.15*mean+0.85*sigmoid((k-6.5)*2)
    raise ValueError(model)

def outcome(X,true,rng):
    return [signature(row,true)+rng.gauss(0,0.07) for row in X]

def fit_line(x,y):
    mx=sum(x)/len(x);my=sum(y)/len(y)
    den=sum((v-mx)**2 for v in x)
    b=sum((a-mx)*(yy-my) for a,yy in zip(x,y))/den if den>1e-12 else 0.0
    return my-b*mx,b

def cv_rmse(sig,y,folds):
    n=len(y); allidx=set(range(n)); errs=[]
    for te in folds:
        teset=set(te);tr=sorted(allidx-teset)
        a,b=fit_line([sig[i] for i in tr],[y[i] for i in tr])
        pred=[a+b*sig[i] for i in te]
        errs.append(math.sqrt(sum((y[i]-p)**2 for i,p in zip(te,pred))/len(te)))
    return sum(errs)/len(errs)

def make_latent(n,rng):
    ans=[]
    for _ in range(n):
        shared=rng.betavariate(2,2)
        ans.append([max(0,min(1,0.25*shared+0.75*rng.betavariate(1.5,1.5))) for _ in MODULES])
    return ans

def noisy_imputed(X,mask,rng):
    Z=[]
    for row,mrow in zip(X,mask):
        Z.append([max(0,min(1,x+rng.gauss(0,0.08))) if obs else None for x,obs in zip(row,mrow)])
    means=[]
    for j in range(len(MODULES)):
        xs=[row[j] for row in Z if row[j] is not None]
        means.append(sum(xs)/len(xs) if xs else 0.5)
    return [[means[j] if x is None else x for j,x in enumerate(row)] for row in Z]

def folds(n,rng,k=4):
    idx=list(range(n));rng.shuffle(idx)
    return [idx[i::k] for i in range(k)]

def evaluate(X,mask,rng):
    Z=noisy_imputed(X,mask,rng); ff=folds(len(X),rng)
    S={m:[signature(row,m) for row in Z] for m in MODELS}
    ans=[]
    for true in MODELS:
        y=outcome(X,true,rng)
        score={m:cv_rmse(S[m],y,ff) for m in MODELS}
        ordered=sorted(score.items(),key=lambda kv:kv[1])
        ans.append((true,ordered[0][0],ordered[1][1]-ordered[0][1]))
    return ans

def run_mask(mask,reps,seed):
    rng=random.Random(seed);wins=Counter();conf=Counter();marg=defaultdict(list)
    for _ in range(reps):
        X=make_latent(len(mask),rng)
        for true,pred,margin in evaluate(X,mask,rng):
            conf[(true,pred)]+=1
            if true==pred:wins[true]+=1
            marg[true].append(margin)
    return {m:wins[m]/reps for m in MODELS},{k:statistics.median(v) for k,v in marg.items()},conf

def read_pilot7(path):
    rr=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    taxa=list(dict.fromkeys(r["scientific_name"] for r in rr));by={(r["scientific_name"],r["module_id"]):r for r in rr}
    return taxa,[[by[(sp,m)]["evidence_state"] in OBSERVED_STATES or bool((by[(sp,m)].get("measurement_coverage") or "").strip()) for m in MODULES] for sp in taxa]

def read_tier1(path):
    rr=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    taxa=list(dict.fromkeys(r["scientific_name"] for r in rr));by={(r["scientific_name"],r["module_id"]):r for r in rr}
    seg={sp:next(r["matrix_segment"] for r in rr if r["scientific_name"]==sp) for sp in taxa}
    return taxa,seg,[[str(by[(sp,m)]["observed_now"]).strip()=="1" for m in MODULES] for sp in taxa]

def cp(m):return [list(r) for r in m]
def fill_cols(mask,cols):
    x=cp(mask)
    for row in x:
        for j in cols:row[j]=True
    return x

def scenarios(base):
    _,m29=read_pilot7(base/"data"/"module_evidence_state_v2.csv")
    taxa,seg,m79=read_tier1(base/"data"/"module_evidence_state_tier1_v0.csv")
    taxa9,seg9,m79_pilot9=read_tier1(base/"data"/"module_evidence_state_tier1_v1.csv")
    assert taxa9==taxa, "Pilot-9 matrix must preserve Tier-1 taxon order"
    new50=cp(m79)
    for i,sp in enumerate(taxa):
        if seg[sp]=="tier1_new50":
            for j in range(6):new50[i][j]=True
    af=fill_cols(m79,range(6))
    sc={
      "pilot7_current29":m29,
      "tier1_empirical79":m79,
      "tier1_pilot9_partial_deep79":m79_pilot9,
      "tier1_new50_AF_complete":new50,
      "tier1_all79_AF_complete":af,
      "tier1_AF_plus_G":fill_cols(af,[6]),
      "tier1_AF_plus_H":fill_cols(af,[7]),
      "tier1_AF_plus_I":fill_cols(af,[8]),
      "tier1_AF_plus_J":fill_cols(af,[9]),
      "tier1_AF_GHI_Jempirical":fill_cols(af,[6,7,8]),
      "tier1_AF_GHJ_Iempirical":fill_cols(af,[6,7,9]),
      "tier1_AF_GIJ_Hempirical":fill_cols(af,[6,8,9]),
      "tier1_AF_HIJ_Gempirical":fill_cols(af,[7,8,9]),
      "tier1_complete79":[[True]*10 for _ in m79],
    }
    return sc

def standardized_signature(pool):
    raw=[[signature(r,m) for m in MODELS] for r in pool]
    means=[];sds=[]
    for j in range(len(MODELS)):
        xs=[r[j] for r in raw];mu=sum(xs)/len(xs)
        sd=(sum((x-mu)**2 for x in xs)/(len(xs)-1))**0.5
        means.append(mu);sds.append(sd or 1.0)
    return [[(r[j]-means[j])/sds[j] for j in range(len(MODELS))] for r in raw]

def oracle_select(pool,n):
    S=standardized_signature(pool)
    centroid=[sum(r[j] for r in S)/len(S) for j in range(len(MODELS))]
    def d2(a,b):return sum((x-y)**2 for x,y in zip(a,b))
    chosen=[max(range(len(S)),key=lambda i:d2(S[i],centroid))]
    mind=[d2(s,S[chosen[0]]) for s in S]
    while len(chosen)<n:
        j=max((i for i in range(len(S)) if i not in set(chosen)),key=lambda i:mind[i])
        chosen.append(j)
        for i,s in enumerate(S):mind[i]=min(mind[i],d2(s,S[j]))
    return [pool[i] for i in chosen]

def run_oracle(n,reps,seed):
    rng=random.Random(seed);wins=Counter();conf=Counter();marg=defaultdict(list)
    mask=[[True]*10 for _ in range(n)]
    for _ in range(reps):
        pool=make_latent(1000,rng);X=oracle_select(pool,n)
        for true,pred,margin in evaluate(X,mask,rng):
            conf[(true,pred)]+=1
            if true==pred:wins[true]+=1
            marg[true].append(margin)
    return {m:wins[m]/reps for m in MODELS},{m:statistics.median(marg[m]) for m in MODELS},conf

def main():
    base=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser();ap.add_argument("--reps",type=int,default=500);ap.add_argument("--oracle-reps",type=int,default=200);args=ap.parse_args()
    summary=[];confrows=[]
    for name,mask in scenarios(base).items():
        rec,margin,conf=run_mask(mask,args.reps,SEED+si*10000)
        per=[sum(row[j] for row in mask) for j in range(10)];obs=sum(per);total=len(mask)*10
        for true in MODELS:
            row={"scenario":name,"sampling":"fixed_mask_random_latent","n_taxa":len(mask),"observed_cells":obs,"total_cells":total,"coverage":obs/total,"true_model":true,"recovery_rate":rec[true],"median_winner_margin_rmse":margin[true]}
            row.update({f"coverage_{m}":per[j] for j,m in enumerate(MODULES)});summary.append(row)
        for (true,pred),n in conf.items():confrows.append({"scenario":name,"sampling":"fixed_mask_random_latent","true_model":true,"selected_model":pred,"count":n,"reps":args.reps})
        print(name,round(obs/total,4),rec)
    rec,margin,conf=run_oracle(79,args.oracle_reps,SEED+999999)
    for true in MODELS:
        row={"scenario":"tier1_complete79_oracle_geometry","sampling":"latent_signature_oracle_upper_bound","n_taxa":79,"observed_cells":790,"total_cells":790,"coverage":1.0,"true_model":true,"recovery_rate":rec[true],"median_winner_margin_rmse":margin[true]}
        row.update({f"coverage_{m}":79 for m in MODULES});summary.append(row)
    for (true,pred),n in conf.items():confrows.append({"scenario":"tier1_complete79_oracle_geometry","sampling":"latent_signature_oracle_upper_bound","true_model":true,"selected_model":pred,"count":n,"reps":args.oracle_reps})
    print("tier1_complete79_oracle_geometry",rec)

    fields=list(summary[0])
    with open(base/"data"/"tier1_recoverability_v3.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(summary)
    cf=["scenario","sampling","true_model","selected_model","count","reps"]
    with open(base/"data"/"tier1_recoverability_confusion_v3.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cf);w.writeheader();w.writerows(confrows)

if __name__=="__main__":
    main()
