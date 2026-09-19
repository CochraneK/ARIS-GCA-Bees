#!/usr/bin/env python3
"""ARIS4C006 preregistration consistency audit and deterministic lock generator.

This script never estimates scientific effects. It verifies that canonical
pre-outcome design documents agree and only emits a preregistration lock when
all required execution gates are recorded as PASS in DESIGN_GATES.json.
"""
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROC=ROOT/"process"

LOCK_FILES=[
    "PREREGISTRATION_DRAFT.md",
    "ANALYSIS_SPEC.json",
    "DESIGN_GATES.json",
    "COHORT_DEFINITION.json",
    "COHORT_PROTOCOL.md",
    "POPULATION_FRAME.md",
    "SURNAME_ROMANIZATION_RULE.md",
    "SURNAME_PARSING_PROTOCOL.md",
    "EXPOSURE_ESTIMATOR.md",
    "LOAO_EXPOSURE_RULE.md",
    "WORK_TYPE_RULE.md",
    "INFERENCE_RULE.md",
    "IDENTITY_RISK_RULE.md",
    "PRIMARY_FRAME_SAMPLING_RULE.md",
    "EXECUTION_ACCEPTANCE_RULE.md",
]

REQUIRED_PASS_GATES=[
    "chinese_surname_population_baseline",
    "crossref_structured_surname_route",
    "randomized_measurement_gate",
    "source_context_reliability",
    "person_identity_resolution",
    "cohort_definition",
    "all_field_scope",
    "within_author_exposure_variation",
    "surname_romanization",
    "global_time_window",
    "loao_implementation",
    "synthetic_model_smoke",
    "final_convention_materialization",
    "primary_frame_materialization",
    "longitudinal_identity_risk_qa",
]

def load_json(name):
    return json.loads((PROC/name).read_text(encoding="utf-8"))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fail_if(cond,msg,errors):
    if cond:errors.append(msg)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--lock",action="store_true")
    a=ap.parse_args()

    errors=[]
    prereg=(PROC/"PREREGISTRATION_DRAFT.md").read_text(encoding="utf-8")
    spec=load_json("ANALYSIS_SPEC.json")
    gates=load_json("DESIGN_GATES.json")
    cohort=load_json("COHORT_DEFINITION.json")
    paper=json.loads((ROOT/"paper.json").read_text(encoding="utf-8"))

    for name in LOCK_FILES:
        fail_if(not (PROC/name).exists(),f"missing lock file: {name}",errors)

    fail_if(paper.get("status") not in {"research-design","preregistered"},
            f"unexpected paper status: {paper.get('status')}",errors)
    fail_if(bool(spec.get("confirmatory_outcomes_unlocked")),
            "ANALYSIS_SPEC already has confirmatory outcomes unlocked",errors)
    fail_if(bool(gates.get("confirmatory_outcomes_unlocked")),
            "DESIGN_GATES already has confirmatory outcomes unlocked",errors)

    # Cross-document frozen constants.
    tw=spec["primary_frame"]["time_window"]
    fail_if((tw.get("start"),tw.get("end"))!=(2011,2025),"analysis time window mismatch",errors)
    fail_if(cohort["primary_work_window"]["start"]!=2011 or cohort["primary_work_window"]["end"]!=2025,
            "cohort primary work window mismatch",errors)
    fail_if(cohort["longitudinal_entry_window"]!={"start":2014,"end":2020},
            "longitudinal entry window mismatch",errors)
    fail_if(cohort["clean_lookback_years"]!=3 or cohort["followup_years"]!=5,
            "cohort lookback/followup mismatch",errors)
    fail_if(spec["primary_frame"]["work_types"]!=["article","conference-paper"],
            "primary work types mismatch",errors)
    fail_if(spec["primary_exposure"]["context"]!="OpenAlex primary_topic field",
            "primary field context mismatch",errors)
    fail_if(spec["primary_exposure"]["lag_window_years"]!=3,
            "lag window mismatch",errors)
    fail_if(spec["surname_measurement"].get("canonical_map")!="aris4c006-surname-map-v2-ccnc",
            "surname map version mismatch",errors)
    fail_if(spec["primary_model"]["primary_estimand"]!="beta2",
            "primary estimand mismatch",errors)
    fail_if(spec["primary_model"]["inference"]["cluster"]!=[
        "canonical_author_id","work_id","primary_field_x_year"],
        "cluster rule mismatch",errors)

    # No unresolved design placeholders in prereg text.
    for pat,label in [
        (r"\bTBF\b","TBF marker"),
        (r"\[ \]","unchecked prereg checkbox"),
        (r"candidate primary","candidate-primary wording"),
    ]:
        if re.search(pat,prereg,flags=re.I):
            errors.append(f"prereg contains unresolved {label}")

    # All execution gates required for lock must exist and be pass-like.
    gate_status={}
    for key in REQUIRED_PASS_GATES:
        g=(gates.get("gates") or {}).get(key)
        if not g:
            errors.append(f"missing required gate: {key}")
            continue
        status=str(g.get("status",""))
        gate_status[key]=status
        if not (status=="pass" or status.startswith("pass-") or status.startswith("pass_")
                or status in {"pass-with-canonicalization-and-sensitivity","frozen-preoutcome",
                              "primary-granularity-and-within-author-variation-passed"}):
            errors.append(f"gate not passed: {key}={status}")

    audit={
        "script":"27_prereg_lock.py",
        "effect_estimation_performed":False,
        "lock_requested":bool(a.lock),
        "errors":errors,
        "required_gate_status":gate_status,
        "lock_files":LOCK_FILES,
    }

    if not errors and a.lock:
        file_hashes={name:sha(PROC/name) for name in LOCK_FILES}
        canonical="\n".join(f"{k}\t{file_hashes[k]}" for k in sorted(file_hashes))
        combined=hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        lock={
            "schema_version":1,
            "paper_id":"006",
            "lock_label":"ARIS4C006-prereg-v1",
            "combined_sha256":combined,
            "file_sha256":file_hashes,
            "confirmatory_outcomes_unlocked_at_lock_creation":False,
            "effect_estimation_performed":False,
            "note":"This hash freezes the canonical pre-outcome design. Unlock is a separate explicit repository change after lock creation.",
        }
        (PROC/"PREREGISTRATION_LOCK.json").write_text(
            json.dumps(lock,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        audit["lock_created"]=True
        audit["combined_sha256"]=combined
    else:
        audit["lock_created"]=False

    out=ROOT/"data"/"qa"/"prereg_audit"
    out.mkdir(parents=True,exist_ok=True)
    (out/"manifest.json").write_text(json.dumps(audit,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(audit,indent=2,ensure_ascii=False))
    if errors:raise SystemExit(1)

if __name__=="__main__":
    main()
