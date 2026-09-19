#!/usr/bin/env python3
"""Summarize held-out Universal Clock 2/3 predictions for ARIS4C007 Pilot 3C.

The molecular linear predictors (eta2, eta3) are kept separate from the
life-history inverse transformations used to express them as chronological or
human-equivalent ages.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))


def q(xs:list[float],p:float)->float:
    ys=sorted(xs)
    if len(ys)==1:return ys[0]
    pos=(len(ys)-1)*p
    lo=int(math.floor(pos));hi=int(math.ceil(pos))
    if lo==hi:return ys[lo]
    return ys[lo]*(hi-pos)+ys[hi]*(pos-lo)


def pearson(x:list[float],y:list[float])->float:
    mx=statistics.fmean(x);my=statistics.fmean(y)
    num=sum((a-mx)*(b-my) for a,b in zip(x,y))
    den=math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
    return num/den if den else float("nan")


def c2_rel_from_eta(eta:float)->float:
    return math.exp(-math.exp(-eta))


def c2_eta_true(age:float,g:float,highmax:float)->float:
    r=(age+g)/(highmax+g)
    if not 0<r<1:
        return float("nan")
    return -math.log(-math.log(r))


def c2_age_from_eta(eta:float,g:float,highmax:float)->float:
    return c2_rel_from_eta(eta)*(highmax+g)-g


def c3_m(g:float,maturity:float)->float:
    return 5.0*(g/maturity)**0.38


def c3_eta_true(age:float,g:float,maturity:float)->float:
    x=(age+g)/(maturity+g)
    m=c3_m(g,maturity)
    z=x/m
    if z<=0:return float("nan")
    return math.log(z) if z<1 else z-1


def c3_age_from_eta(eta:float,g:float,maturity:float)->float:
    m=c3_m(g,maturity)
    reladult=m*math.exp(eta) if eta<0 else m*(eta+1)
    return reladult*(maturity+g)-g


def metric(rows:list[dict[str,float]],pred_key:str)->dict[str,float]:
    valid=[r for r in rows if math.isfinite(r[pred_key]) and math.isfinite(r["age"])]
    err=[abs(r[pred_key]-r["age"]) for r in valid]
    return {
        "n":len(valid),
        "median_abs_error_y":statistics.median(err),
        "mean_abs_error_y":statistics.fmean(err),
        "p90_abs_error_y":q(err,0.9),
        "cor_predicted_vs_chronological":pearson([r[pred_key] for r in valid],[r["age"] for r in valid]),
    }


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--predictions",type=Path,required=True)
    ap.add_argument("--traits",type=Path,required=True)
    ap.add_argument("--out-csv",type=Path,required=True)
    ap.add_argument("--out-json",type=Path,required=True)
    args=ap.parse_args()

    preds=read_csv(args.predictions)
    traits={r["species"]:r for r in read_csv(args.traits)}
    human=traits["Homo sapiens"]

    hg_e=float(human["clockera_gestation_y"]); hm_e=float(human["clockera_maturity_y"]); hH_e=float(human["clockera_highmax_y"])
    hg_c=float(human["current_gestation_y"]); hm_c=float(human["current_maturity_y"]); hH_c=float(human["current_highmax_y"])

    enriched=[]
    for r in preds:
        sp=r["species"];t=traits[sp]
        age=float(r["chronological_age_y"]);e2=float(r["clock2_eta"]);e3=float(r["clock3_eta"])
        ge=float(t["clockera_gestation_y"]);me=float(t["clockera_maturity_y"]);He=float(t["clockera_highmax_y"])
        gc=float(t["current_gestation_y"]);mc=float(t["current_maturity_y"]);Hc=float(t["current_highmax_y"])

        true2e=c2_eta_true(age,ge,He)
        true3e=c3_eta_true(age,ge,me)
        pred2e=c2_age_from_eta(e2,ge,He)
        pred3e=c3_age_from_eta(e3,ge,me)
        pred2c=c2_age_from_eta(e2,gc,Hc)
        pred3c=c3_age_from_eta(e3,gc,mc)

        # Human-equivalent ages implied by the same predicted molecular coordinate.
        human2e=c2_age_from_eta(e2,hg_e,hH_e)
        human3e=c3_age_from_eta(e3,hg_e,hm_e)
        human2c=c2_age_from_eta(e2,hg_c,hH_c)
        human3c=c3_age_from_eta(e3,hg_c,hm_c)

        # Deterministic target-equivalent human ages using chronological age only.
        human2_truth=c2_age_from_eta(true2e,hg_e,hH_e) if math.isfinite(true2e) else float("nan")
        human3_truth=c3_age_from_eta(true3e,hg_e,hm_e) if math.isfinite(true3e) else float("nan")

        x=dict(r)
        x.update({
            "clock2_eta_true_clockera":true2e,
            "clock2_eta_residual":e2-true2e if math.isfinite(true2e) else float("nan"),
            "clock3_eta_true_clockera":true3e,
            "clock3_eta_residual":e3-true3e if math.isfinite(true3e) else float("nan"),
            "clock2_age_clockera_y":pred2e,
            "clock3_age_clockera_y":pred3e,
            "clock2_age_currenttraits_y":pred2c,
            "clock3_age_currenttraits_y":pred3c,
            "clock2_trait_sensitivity_y":pred2c-pred2e,
            "clock3_trait_sensitivity_y":pred3c-pred3e,
            "clock2_molecular_human_equiv_clockera_y":human2e,
            "clock3_molecular_human_equiv_clockera_y":human3e,
            "clock2_molecular_human_equiv_currenttraits_y":human2c,
            "clock3_molecular_human_equiv_currenttraits_y":human3c,
            "clock2_deterministic_human_equiv_clockera_y":human2_truth,
            "clock3_deterministic_human_equiv_clockera_y":human3_truth,
            "clock2_molecular_shift_from_target_human_y":human2e-human2_truth if math.isfinite(human2_truth) else float("nan"),
            "clock3_molecular_shift_from_target_human_y":human3e-human3_truth if math.isfinite(human3_truth) else float("nan"),
            "molecular_human_equiv_clock3_minus_clock2_y":human3e-human2e,
        })
        enriched.append(x)

    args.out_csv.parent.mkdir(parents=True,exist_ok=True)
    with args.out_csv.open("w",encoding="utf-8",newline="") as f:
        fields=list(enriched[0])
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader();w.writerows(enriched)

    numeric=[]
    for r in enriched:
        numeric.append({
            **r,
            "age":float(r["chronological_age_y"]),
            "clock2_age_clockera_y":float(r["clock2_age_clockera_y"]),
            "clock3_age_clockera_y":float(r["clock3_age_clockera_y"]),
        })

    by=defaultdict(list)
    for r in numeric:by[r["species"]].append(r)

    summary={
        "n_samples":len(numeric),
        "n_species":len(by),
        "clock2_chronological_performance_clockera_traits":metric(numeric,"clock2_age_clockera_y"),
        "clock3_chronological_performance_clockera_traits":metric(numeric,"clock3_age_clockera_y"),
        "species":{
            sp:{
                "n":len(g),
                "clock2":metric(g,"clock2_age_clockera_y"),
                "clock3":metric(g,"clock3_age_clockera_y"),
            } for sp,g in sorted(by.items())
        },
        "target_space":{
            "clock2_median_abs_eta_residual":statistics.median(abs(float(r["clock2_eta_residual"])) for r in enriched if math.isfinite(float(r["clock2_eta_residual"]))),
            "clock3_median_abs_eta_residual":statistics.median(abs(float(r["clock3_eta_residual"])) for r in enriched if math.isfinite(float(r["clock3_eta_residual"]))),
        },
        "trait_version_sensitivity":{
            "clock2_median_abs_age_change_y":statistics.median(abs(float(r["clock2_trait_sensitivity_y"])) for r in enriched),
            "clock2_max_abs_age_change_y":max(abs(float(r["clock2_trait_sensitivity_y"])) for r in enriched),
            "clock3_median_abs_age_change_y":statistics.median(abs(float(r["clock3_trait_sensitivity_y"])) for r in enriched),
            "clock3_max_abs_age_change_y":max(abs(float(r["clock3_trait_sensitivity_y"])) for r in enriched),
        },
        "molecular_equivalence":{
            "median_abs_clock3_minus_clock2_human_equiv_y":statistics.median(abs(float(r["molecular_human_equiv_clock3_minus_clock2_y"])) for r in enriched),
            "clock2_median_abs_molecular_shift_from_own_target_human_y":statistics.median(abs(float(r["clock2_molecular_shift_from_target_human_y"])) for r in enriched if math.isfinite(float(r["clock2_molecular_shift_from_target_human_y"]))),
            "clock3_median_abs_molecular_shift_from_own_target_human_y":statistics.median(abs(float(r["clock3_molecular_shift_from_target_human_y"])) for r in enriched if math.isfinite(float(r["clock3_molecular_shift_from_target_human_y"]))),
        },
        "interpretation_guardrail":"Clock2 and Clock3 targets encode A1/A3-like life-history assumptions. Held-out sample prediction tests molecular generalization, not independence of the target construct itself.",
    }
    args.out_json.write_text(json.dumps(summary,indent=2,allow_nan=True)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2,allow_nan=True))


if __name__=="__main__":
    main()
