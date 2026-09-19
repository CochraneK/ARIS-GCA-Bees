#!/usr/bin/env python3
"""ARIS4C006 — deterministic prelock execution-gate evaluator.

Consumes only aggregate outcome-blind manifests:
  A) final convention/exposure build
  B) primary focal-work frame
  C) longitudinal identity-risk prevalence audit

Applies thresholds frozen in process/EXECUTION_ACCEPTANCE_RULE.md.
Does not read or estimate H1/H2/H3 coefficients or predictor-outcome relations.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

EXPECTED_FIELDS=list(range(11,37))
EXPECTED_YEARS=list(range(2011,2026))

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def truth(x):
    return str(x).strip().lower()=="true" if isinstance(x,str) else bool(x)

def read_csv(path):
    with Path(path).open(encoding="utf-8",newline="") as h:
        return list(csv.DictReader(h))

def convention_gate(m,rolling_rows):
    errors=[]
    if m.get("confirmatory_use_allowed") not in {False,None}:
        errors.append("convention artifact unexpectedly marked confirmatory-use allowed")
    if m.get("outcomes_opened") is not False:
        errors.append("convention artifact does not prove outcomes remained locked")
    if m.get("fields_found")!=EXPECTED_FIELDS:
        errors.append("not all 26 fields present")
    if m.get("annual_cells")!=26*17:
        errors.append("annual cell count != 442")
    if m.get("rolling_cells")!=26*15:
        errors.append("rolling cell count != 390")

    rp=int(m.get("rolling_primary_supported") or 0)
    r3=int(m.get("rolling_3plus_supported") or 0)
    primary_share=rp/(26*15)
    robust_share=r3/(26*15)
    if primary_share < .95:
        errors.append(f"primary rolling support {primary_share:.4f} < 0.95")
    if robust_share < .80:
        errors.append(f"3+ rolling support {robust_share:.4f} < 0.80")

    pf={str(fid):0 for fid in EXPECTED_FIELDS}
    p3={str(fid):0 for fid in EXPECTED_FIELDS}
    for r in rolling_rows:
        fid=str(int(r["field_id"]))
        if truth(r.get("primary_full_field_supported")):pf[fid]=pf.get(fid,0)+1
        if truth(r.get("robustness_3plus_supported")):p3[fid]=p3.get(fid,0)+1
    bad={k:v for k,v in pf.items() if int(v)<10}
    if bad:errors.append(f"fields with <10 primary supported years: {bad}")
    bad3={k:v for k,v in p3.items() if int(v)<8}
    if bad3:errors.append(f"fields with <8 3+ supported years: {bad3}")

    return {
        "status":"pass" if not errors else "fail",
        "errors":errors,
        "primary_supported_share":primary_share,
        "robustness_3plus_supported_share":robust_share,
        "primary_supported_years_by_field":pf,
        "robustness_3plus_supported_years_by_field":p3,
    }

def primary_frame_gate(m,count_rows):
    errors=[]
    if m.get("confirmatory_effect_estimation_allowed") not in {False,None}:
        errors.append("primary-frame artifact unexpectedly allows confirmatory estimation")
    if m.get("effects_or_pvalues_computed") is not False:
        errors.append("primary-frame artifact does not prove effects/p-values remained uncomputed")
    if m.get("fields_found")!=EXPECTED_FIELDS:
        errors.append("not all 26 fields present")
    if m.get("years_found")!=EXPECTED_YEARS:
        errors.append("not all 15 focal years present")
    if m.get("field_year_cells")!=390:
        errors.append("field-year cells != 390")

    status=m.get("cell_status_counts") or {}
    retained_ge20=int(status.get("target_met",0))+int(status.get("retain_below_target",0))
    retained_share=retained_ge20/390
    if retained_share < .90:
        errors.append(f"retained >=20-work cells share {retained_share:.4f} < 0.90")

    per_field={str(fid):0 for fid in EXPECTED_FIELDS}
    for r in count_rows:
        fid=str(int(r["field_id"]))
        if r.get("cell_status") in {"target_met","retain_below_target"}:
            per_field[fid]=per_field.get(fid,0)+1
    bad={k:v for k,v in per_field.items() if int(v)<10}
    if bad:errors.append(f"fields with <10 retained years: {bad}")

    if int(m.get("works_retained") or 0)<10000:
        errors.append("works_retained < 10000")
    if int(m.get("focal_rows_retained") or 0)<20000:
        errors.append("focal_rows_retained < 20000")
    if int(m.get("unique_canonical_authors_retained") or 0)<10000:
        errors.append("unique canonical authors < 10000")
    if int(m.get("field_year_clusters_retained") or 0)<350:
        errors.append("field-year clusters < 350")

    return {
        "status":"pass" if not errors else "fail",
        "errors":errors,
        "retained_cell_share":retained_share,
        "retained_years_by_field":per_field,
    }

def identity_gate(m):
    errors=[]
    if m.get("confirmatory_outcomes_unlocked") is not False:
        errors.append("identity artifact does not prove confirmatory outcomes remained locked")
    if m.get("persistence_outcome_computed") is not False:
        errors.append("identity audit computed persistence outcome")
    if m.get("effect_or_pvalue_computed") is not False:
        errors.append("identity audit computed effect/p-value")

    n=int(m.get("seed_authors") or 0)
    valid=int(m.get("hard_qa_pass") or 0)
    hard_pass_share=(valid/n) if n else 0.0
    if n<100:errors.append("audited unique candidates < 100")
    if hard_pass_share<.95:errors.append(f"hard QA classifiable/pass share {hard_pass_share:.4f} < 0.95")
    if not isinstance(m.get("flag_counts"),dict):errors.append("R1-R6 flag counts missing")
    if int(m.get("low_risk_subset") or 0)<=0:errors.append("low-risk subset empty")
    if int(m.get("orcid_anchored_subset") or 0)<=0:errors.append("ORCID-anchored subset empty")

    # Hard integrity failure rate is the complement of hard_qa_pass_share.
    hard_failure_rate=1-hard_pass_share
    if hard_failure_rate>.05:
        errors.append(f"hard identity-integrity failures {hard_failure_rate:.4f} > 0.05")

    return {
        "status":"pass" if not errors else "fail",
        "errors":errors,
        "hard_qa_pass_share":hard_pass_share,
        "hard_failure_rate":hard_failure_rate,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--convention-manifest",required=True)
    ap.add_argument("--primary-frame-manifest",required=True)
    ap.add_argument("--identity-manifest",required=True)
    ap.add_argument("--convention-rolling-csv",required=True)
    ap.add_argument("--primary-frame-counts-csv",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    cm=load(a.convention_manifest)
    pm=load(a.primary_frame_manifest)
    im=load(a.identity_manifest)
    rolling_rows=read_csv(a.convention_rolling_csv)
    count_rows=read_csv(a.primary_frame_counts_csv)

    result={
        "script":"28_evaluate_execution_gates.py",
        "effect_estimation_performed":False,
        "acceptance_rule":"process/EXECUTION_ACCEPTANCE_RULE.md",
        "convention":convention_gate(cm,rolling_rows),
        "primary_frame":primary_frame_gate(pm,count_rows),
        "identity_risk":identity_gate(im),
    }
    result["all_execution_gates_pass"]=all(
        result[k]["status"]=="pass" for k in ["convention","primary_frame","identity_risk"]
    )

    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if not result["all_execution_gates_pass"]:
        raise SystemExit(1)

if __name__=="__main__":
    main()
