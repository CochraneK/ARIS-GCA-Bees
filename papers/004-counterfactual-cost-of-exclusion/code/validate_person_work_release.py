#!/usr/bin/env python3
"""Validate person-level network100 work-release decisions."""

from __future__ import annotations
import argparse,csv,sys
from pathlib import Path
from collections import Counter

VERIFIED={"VERIFIED_SINGLE","VERIFIED_CLUSTER"}
ALLOWED={"RELEASE_SAMPLE_PASS","HOLD_INSUFFICIENT_CLEAN_WORKS","ESCALATE_TARGETED_WORK_REVIEW"}

def truthy(v): return (v or "").strip().lower() in {"1","true","yes","y"}
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as h: return list(csv.DictReader(h))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--decisions",type=Path,required=True)
    p.add_argument("--identities",type=Path,required=True)
    p.add_argument("--work-summary",type=Path,required=True)
    p.add_argument("--audit-sample",type=Path,required=True)
    p.add_argument("--prior-work-decisions",type=Path,required=True)
    a=p.parse_args()

    ids={r["person_id"]:r for r in read(a.identities)}
    ws={r["person_id"]:r for r in read(a.work_summary)}
    sample=read(a.audit_sample)
    prior=read(a.prior_work_decisions)
    decisions=read(a.decisions)
    errors=[]

    held={pid for pid,r in ids.items() if r.get("identity_status") in VERIFIED and not truthy(r.get("network_observable"))}
    released_by_table={r["person_id"] for r in decisions if r.get("person_work_decision")=="RELEASE_SAMPLE_PASS"}
    expected=held | released_by_table
    seen=[r["person_id"] for r in decisions]
    if len(seen)!=len(set(seen)): errors.append("duplicate person_id in person work decisions")
    if set(seen)!=expected:
        errors.append(f"decision coverage mismatch: expected={len(expected)}, observed={len(set(seen))}, missing={sorted(expected-set(seen))}, extra={sorted(set(seen)-expected)}")

    sample_by={}
    for r in sample: sample_by.setdefault(r["person_id"],[]).append(r)
    prior_keep=Counter()
    for r in prior:
        if r.get("work_decision") in {"KEEP_ORIGINAL","KEEP_POSTHUMOUS_ORIGINAL"} and truthy(r.get("include_in_network")):
            prior_keep[r["person_id"]]+=1

    for r in decisions:
        pid=r["person_id"]; dec=r.get("person_work_decision","")
        if dec not in ALLOWED:
            errors.append(f"{pid}: invalid decision {dec!r}"); continue
        meta=ws.get(pid,{})
        plausible=int(meta.get("plausible_unique_works_n") or 0)
        approved=truthy(r.get("network_release_approved"))
        if approved != (dec=="RELEASE_SAMPLE_PASS"):
            errors.append(f"{pid}: network_release_approved inconsistent with decision")
        identity_observable=truthy((ids.get(pid) or {}).get("network_observable"))
        if identity_observable != approved:
            errors.append(f"{pid}: canonical identity network_observable={identity_observable} disagrees with approved={approved}")
        if not truthy(r.get("mh_blinded_at_work_lock")):
            errors.append(f"{pid}: MH-blind lock required")
        if not (r.get("reviewer") or "").strip() or not (r.get("decision_evidence") or "").strip():
            errors.append(f"{pid}: reviewer/evidence required")

        if dec=="RELEASE_SAMPLE_PASS":
            rows=sample_by.get(pid,[])
            if plausible<5: errors.append(f"{pid}: release requires >=5 plausible works, got {plausible}")
            if not rows: errors.append(f"{pid}: release requires deterministic audit sample")
            bad=[x for x in rows if not truthy(x.get("work_belongs_to_focal_person"))]
            unreviewed=[x for x in rows if not (x.get("reviewer") or "").strip() or not truthy(x.get("mh_blinded_at_work_audit"))]
            if bad: errors.append(f"{pid}: {len(bad)} sampled rows not affirmed as focal-person works")
            if unreviewed: errors.append(f"{pid}: {len(unreviewed)} sampled rows lack blinded review")
        elif dec=="HOLD_INSUFFICIENT_CLEAN_WORKS":
            if not (plausible<5 or prior_keep[pid]<5 and prior_keep[pid]>0):
                errors.append(f"{pid}: insufficient-work hold not supported (plausible={plausible}, prior_keep={prior_keep[pid]})")

    if errors:
        print(f"FAIL: {len(errors)} person-work decision invariant error(s)",file=sys.stderr)
        for e in errors: print("- "+e,file=sys.stderr)
        return 1
    print(f"PASS: {len(decisions)} held verified people covered; releases={sum(r['person_work_decision']=='RELEASE_SAMPLE_PASS' for r in decisions)}")
    return 0

if __name__=="__main__": raise SystemExit(main())
