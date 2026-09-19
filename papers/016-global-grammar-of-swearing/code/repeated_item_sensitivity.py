#!/usr/bin/env python3
"""Balanced-shared-item and filler negative-control sensitivity for ARIS4C016.

Uses the same pure-Python item-fixed-effects FWL diagnostic as
repeated_item_model.py. Raw lexical items are never emitted.
"""

from __future__ import annotations
import csv, hashlib, io, json, math, random, urllib.request

GUID="t8wj9"
VIEW_ONLY="60b964248cc64a8793a9013075132a1c"
SHA256="617306c5d762586e0426081b13f779d64b30937f2d35cfbe24fdb97ded1f7a5a"
DIMS=("tabooness","offensiveness","valence","arousal","concreteness","aoa")
BOOTSTRAPS=500
SEED=16016

def load():
    url=f"https://osf.io/download/{GUID}/?view_only={VIEW_ONLY}"
    with urllib.request.urlopen(url,timeout=120) as response:
        blob=response.read()
    if hashlib.sha256(blob).hexdigest()!=SHA256:
        raise RuntimeError("Study-2 checksum mismatch")
    rows=list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig",errors="replace"))))
    return [r for r in rows if r["lang"].startswith("English")]

def solve(matrix,vector):
    n=len(vector)
    aug=[list(map(float,matrix[i]))+[float(vector[i])] for i in range(n)]
    for col in range(n):
        pivot=max(range(col,n),key=lambda i:abs(aug[i][col]))
        if abs(aug[pivot][col])<1e-12:
            aug[pivot][col]+=1e-8
        aug[col],aug[pivot]=aug[pivot],aug[col]
        d=aug[col][col]
        aug[col]=[x/d for x in aug[col]]
        for i in range(n):
            if i==col: continue
            factor=aug[i][col]
            aug[i]=[aug[i][j]-factor*aug[col][j] for j in range(n+1)]
    return [aug[i][-1] for i in range(n)]

def fit(blocks,communities,dimension):
    obs=[]
    for _,mapping in blocks:
        values=[]
        for community,row in mapping.items():
            try:value=float(row[dimension])
            except (TypeError,ValueError):continue
            if math.isfinite(value):values.append((community,value))
        if len(values)<2:continue
        mean_y=sum(y for _,y in values)/len(values)
        proportions={
            community:sum(1 for c,_ in values if c==community)/len(values)
            for community in communities
        }
        for community,value in values:
            x=[
                (1.0 if community==c else 0.0)-proportions[c]
                for c in communities[1:]
            ]
            obs.append((value-mean_y,x))
    if not obs:
        return 0.0,0
    p=len(communities)-1
    xtx=[[0.0]*p for _ in range(p)]
    xty=[0.0]*p
    rss0=sum(y*y for y,_ in obs)
    for y,x in obs:
        for j in range(p):
            xty[j]+=x[j]*y
            for k in range(p):
                xtx[j][k]+=x[j]*x[k]
    beta=solve(xtx,xty)
    rss1=sum((y-sum(beta[j]*x[j] for j in range(p)))**2 for y,x in obs)
    return ((rss0-rss1)/rss0 if rss0 else 0.0),len(obs)

def make_blocks(rows,kind,all_five=False):
    by_word={}
    for row in rows:
        is_filler=(row.get("category") or "").strip().lower()=="filler"
        if (kind=="filler")!=is_filler:
            continue
        by_word.setdefault(row["word_clean"],{})[row["lang"]]=row
    return [
        (word,mapping) for word,mapping in by_word.items()
        if (len(mapping)==5 if all_five else len(mapping)>=2)
    ]

def summarize(blocks,communities,dimension,seed):
    estimate,nobs=fit(blocks,communities,dimension)
    if not blocks:
        return {"items":0,"observations":0,"partial_r2":None,"bootstrap95":None}
    rng=random.Random(seed)
    boot=[]
    for _ in range(BOOTSTRAPS):
        sample=[blocks[rng.randrange(len(blocks))] for _ in range(len(blocks))]
        boot.append(fit(sample,communities,dimension)[0])
    boot.sort()
    return {
        "items":len(blocks),
        "observations":nobs,
        "partial_r2":round(estimate,4),
        "bootstrap95":[
            round(boot[int(.025*len(boot))],4),
            round(boot[int(.975*len(boot))-1],4),
        ],
    }

def main():
    rows=load()
    communities=sorted({r["lang"] for r in rows})
    output={"project":"ARIS4C016","communities":communities,"results":{}}
    for kind in ("taboo","filler"):
        output["results"][kind]={}
        for label,all5 in (("shared_2plus",False),("shared_all5",True)):
            blocks=make_blocks(rows,kind,all5)
            output["results"][kind][label]={
                d:summarize(blocks,communities,d,SEED+len(blocks)+sum(map(ord,d)))
                for d in DIMS
            }
    output["limitations"]=[
        "Filler shared-item sample is sparse (35 items, 73 observations) and has no item shared across all five English communities.",
        "Community effects may reflect participant composition, rating calibration, procedure, dialect/register, or other site differences; they are not causal culture effects.",
        "Study-2 values are aggregate item ratings rather than participant-level observations."
    ]
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
