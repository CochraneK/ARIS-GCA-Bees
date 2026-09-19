#!/usr/bin/env python3
"""ARIS4C006 — outcome-blind prelock promotion helper.

Consumes ONLY the frozen execution-gate evaluation. If and only if all
execution gates pass, it updates the two materialization gate records and the
matching preregistration checklist items. It never reads scientific effects.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROC=ROOT/"process"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--evaluation",required=True)
    ap.add_argument("--aggregate-run-id",required=True)
    ap.add_argument("--apply",action="store_true")
    a=ap.parse_args()

    ev=json.loads(Path(a.evaluation).read_text(encoding="utf-8"))
    if ev.get("effect_estimation_performed") is not False:
        raise SystemExit("evaluation does not prove effect estimation remained off")
    if ev.get("all_execution_gates_pass") is not True:
        raise SystemExit("execution gates did not all pass; promotion forbidden")
    for k in ["convention","primary_frame","identity_risk"]:
        if (ev.get(k) or {}).get("status")!="pass":
            raise SystemExit(f"{k} gate is not pass")

    gates_path=PROC/"DESIGN_GATES.json"
    gates=json.loads(gates_path.read_text(encoding="utf-8"))
    if gates.get("confirmatory_outcomes_unlocked") is not False:
        raise SystemExit("design gates unexpectedly unlocked before preregistration")
    gs=gates.setdefault("gates",{})
    gs["final_convention_materialization"]={
        "status":"pass",
        "evidence":{
            "aggregate_workflow_run":int(a.aggregate_run_id),
            "artifact":"aris4c006-final-convention-aggregate-repaired",
            "evaluation_artifact":"aris4c006-execution-gate-evaluation-repaired",
            "rule":"process/EXECUTION_ACCEPTANCE_RULE.md"
        },
        "note":"Outcome-blind 26-field convention/exposure materialization passed every prospectively frozen structural and information-support threshold; no H1/H2/H3 effect was estimated."
    }
    gs["primary_frame_materialization"]={
        "status":"pass",
        "evidence":{
            "aggregate_workflow_run":int(a.aggregate_run_id),
            "artifact":"aris4c006-primary-frame-aggregate-repaired",
            "evaluation_artifact":"aris4c006-execution-gate-evaluation-repaired",
            "rule":"process/EXECUTION_ACCEPTANCE_RULE.md"
        },
        "note":"Outcome-blind 26-field primary focal-work frame passed every prospectively frozen structural/sample-adequacy threshold; no H1/H2/H3 coefficient or p-value was computed."
    }

    prereg_path=PROC/"PREREGISTRATION_DRAFT.md"
    prereg=prereg_path.read_text(encoding="utf-8")
    exact={
        "- [ ] materialize the final primary-field convention/exposure build under article+conference-paper types;":
        "- [x] materialize the final primary-field convention/exposure build under article+conference-paper types;",
        "- [ ] materialize the primary work frame and report sample/cluster counts **without calculating H1/H2 coefficients**;":
        "- [x] materialize the primary work frame and report sample/cluster counts **without calculating H1/H2 coefficients**;",
    }
    for old,new in exact.items():
        if old not in prereg and new not in prereg:
            raise SystemExit(f"expected prereg checklist text not found: {old}")
        prereg=prereg.replace(old,new)

    status_path=PROC/"STATUS.md"
    status=status_path.read_text(encoding="utf-8")
    status=re.sub(
        r"\*\*RESEARCH-DESIGN — .*?\*\*",
        "**RESEARCH-DESIGN — all outcome-blind execution gates passed; preregistration lock ready**",
        status,
        count=1,
    )
    status=status.replace(
        "2. [ ] materialize final 26-field primary convention/exposure build under article+conference-paper types (25/26 field artifacts complete; field 36 running/repairing under unchanged rules);",
        "2. [x] materialize final 26-field primary convention/exposure build under article+conference-paper types (PASS under frozen execution thresholds);"
    )
    status=status.replace(
        "5. [ ] materialize the primary work frame and report only sample/cluster/exclusion counts, **without estimating H1/H2** (25/26 field artifacts complete; field 36 running/repairing under unchanged rules);",
        "5. [x] materialize the primary work frame and report only sample/cluster/exclusion counts, **without estimating H1/H2** (PASS under frozen execution thresholds);"
    )
    status=status.replace(
        "7. [ ] finish preregistration consistency audit, generate lock/hash, then explicitly unlock confirmatory outcomes.",
        "7. [ ] run the now-unblocked preregistration consistency audit, generate lock/hash, then explicitly unlock confirmatory outcomes."
    )

    summary={
        "script":"32_promote_prelock_gates.py",
        "effect_estimation_performed":False,
        "execution_evaluation_passed":True,
        "aggregate_run_id":int(a.aggregate_run_id),
        "files_to_update":[
            "process/DESIGN_GATES.json",
            "process/PREREGISTRATION_DRAFT.md",
            "process/STATUS.md"
        ],
        "applied":bool(a.apply),
    }
    if a.apply:
        gates_path.write_text(json.dumps(gates,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        prereg_path.write_text(prereg,encoding="utf-8")
        status_path.write_text(status,encoding="utf-8")
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
