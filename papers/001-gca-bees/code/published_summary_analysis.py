"""Reproduce the published-summary synthesis in ARIS4C001.

Inputs are numerical values reported in Finke et al. (2023) and
Peñaherrera-Aguirre et al. (2024). This is not a raw-data reanalysis.
"""
import json, math
from pathlib import Path

CORRELATIONS={
"visual":{"AL_RL":{"r":0.53,"n":27},"AL_NP":{"r":0.42,"n":33},"RL_NP":{"r":0.25,"n":27}},
"olfactory":{"AL_RL":{"r":0.60,"n":20},"AL_NP":{"r":0.46,"n":22},"RL_NP":{"r":0.19,"n":20}}}
LOADINGS={"visual":{"AL":0.944,"RL":0.562,"NP":0.445,"variance":0.468},
"olfactory":{"AL":0.997,"RL":0.601,"NP":0.461,"variance":0.523}}

def fisher_pool(pair):
    values=[CORRELATIONS[m][pair] for m in ("visual","olfactory")]
    weights=[v["n"]-3 for v in values]
    zs=[math.atanh(v["r"]) for v in values]
    z=sum(w*x for w,x in zip(weights,zs))/sum(weights); se=math.sqrt(1/sum(weights))
    return {"r":math.tanh(z),"ci95_low":math.tanh(z-1.96*se),"ci95_high":math.tanh(z+1.96*se),"fisher_weight":sum(weights)}

def congruence():
    v=[LOADINGS["visual"][x] for x in ("AL","RL","NP")]; o=[LOADINGS["olfactory"][x] for x in ("AL","RL","NP")]
    dot=sum(a*b for a,b in zip(v,o))
    return dot/math.sqrt(sum(x*x for x in v)*sum(x*x for x in o))

def implied(m):
    l=LOADINGS[m]
    return {"AL_RL":l["AL"]*l["RL"],"AL_NP":l["AL"]*l["NP"],"RL_NP":l["RL"]*l["NP"]}

def rmse(m):
    pred=implied(m)
    res=[CORRELATIONS[m][p]["r"]-pred[p] for p in ("AL_RL","AL_NP","RL_NP")]
    return math.sqrt(sum(x*x for x in res)/len(res))

def main():
    out={"provenance":{"correlations":"Finke et al. 2023","factor_loadings":"Peñaherrera-Aguirre et al. 2024 Table 1","scope":"published-summary synthesis; not raw-data reanalysis"},
    "inputs":{"correlations":CORRELATIONS,"factor_loadings":LOADINGS},
    "descriptive_pooled_correlations":{p:fisher_pool(p) for p in ("AL_RL","AL_NP","RL_NP")},
    "tucker_congruence_visual_vs_olfactory":congruence(),
    "one_factor_implied_correlations":{m:implied(m) for m in ("visual","olfactory")},
    "offdiagonal_rmse":{m:rmse(m) for m in ("visual","olfactory")}}
    path=Path(__file__).resolve().parents[1]/"data"/"published_summary_synthesis.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__": main()
