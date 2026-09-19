#!/usr/bin/env python3
"""Validate ARIS4C011 manager-side confirmatory adjudication coding."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def split_values(v):
    return [x.strip() for x in (v or "").split(";") if x.strip()]

def validate(rows,protocol,require_complete=False):
    errors=[]; counts={}
    issue_vocab=set(protocol["issue_family_vocab"])
    gt_vocab=set(protocol["ground_truth_tiers"])
    role_vocab=set(protocol["artifact_role_vocab"])
    detect_vocab=set(protocol["content_detectability"])
    state_vocab=set(protocol["first_pass_states"])
    ids=set()
    forbidden={
        "detector_output","review_priority","artifact_state","confirmatory_eligible",
        "finding_count","flag_count","anomaly_score","model_score",
    }
    if rows and (set(rows[0]) & forbidden):
        errors.append("forbidden_columns:"+",".join(sorted(set(rows[0])&forbidden)))
    for i,row in enumerate(rows,2):
        fid=(row.get("feasibility_id") or "").strip()
        if not fid: errors.append(f"missing_feasibility_id:row_{i}")
        elif fid in ids: errors.append(f"duplicate_feasibility_id:{fid}")
        ids.add(fid)
        state=(row.get("adjudication_state") or "").strip()
        counts[state]=counts.get(state,0)+1
        if state not in state_vocab:
            errors.append(f"invalid_state:{fid}:{state}")
            continue
        if state=="UNASSESSED":
            if require_complete:
                errors.append(f"unassessed_when_complete_required:{fid}")
            continue
        if state=="NEEDS_SOURCE":
            continue
        if state=="EXCLUDE_DUPLICATE_EVENT":
            continue

        issues=split_values(row.get("issue_family_codes"))
        roles=split_values(row.get("required_artifact_roles"))
        gt=(row.get("ground_truth_tier") or "").strip()
        detect=(row.get("content_detectability") or "").strip()
        if not issues: errors.append(f"missing_issue_family:{fid}")
        if any(x not in issue_vocab for x in issues):
            errors.append(f"invalid_issue_family:{fid}")
        if gt not in gt_vocab: errors.append(f"invalid_ground_truth_tier:{fid}:{gt}")
        if detect not in detect_vocab: errors.append(f"invalid_content_detectability:{fid}:{detect}")
        if not roles: errors.append(f"missing_required_artifact_role:{fid}")
        if any(x not in role_vocab for x in roles):
            errors.append(f"invalid_artifact_role:{fid}")

        if detect=="PROCESS_ONLY":
            if set(roles)!={"none_content_detectable"}:
                errors.append(f"process_only_role_mismatch:{fid}")
        elif detect in {"CONTENT_ASSESSABLE","MIXED"}:
            if "none_content_detectable" in roles or not roles:
                errors.append(f"content_role_mismatch:{fid}")

    return {
        "analysis":"ARIS4C011 confirmatory adjudication validation",
        "row_count":len(rows),
        "state_counts":counts,
        "require_complete":require_complete,
        "error_count":len(errors),
        "errors":errors,
        "structure_valid":not errors,
        "adjudication_complete":bool(rows) and not errors and counts.get("UNASSESSED",0)==0 and counts.get("NEEDS_SOURCE",0)==0,
        "confirmatory_eligibility_inferred":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--packet",type=Path,required=True)
    p.add_argument("--protocol",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--require-complete",action="store_true")
    a=p.parse_args()
    with a.packet.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    protocol=json.loads(a.protocol.read_text(encoding="utf-8"))
    out=validate(rows,protocol,a.require_complete)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "rows":out["row_count"],"state_counts":out["state_counts"],
        "errors":out["error_count"],"complete":out["adjudication_complete"]
    },indent=2))
    if out["error_count"]: raise SystemExit(1)

if __name__=="__main__": main()
