#!/usr/bin/env python3
"""Verify ARIS4C006 preregistration lock integrity and optional unlock.

Never estimates scientific effects.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROC=ROOT/"process"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--require-unlock",action="store_true")
    a=ap.parse_args()

    lock_path=PROC/"PREREGISTRATION_LOCK.json"
    if not lock_path.exists():
        raise SystemExit("preregistration lock missing")
    lock=load(lock_path)
    errors=[]

    for name,expected in (lock.get("file_sha256") or {}).items():
        p=PROC/name
        if not p.exists():
            errors.append(f"locked file missing: {name}")
            continue
        got=sha(p)
        if got!=expected:
            errors.append(f"locked file hash mismatch: {name}")

    spec=load(PROC/"ANALYSIS_SPEC.json")
    gates=load(PROC/"DESIGN_GATES.json")
    if spec.get("confirmatory_outcomes_unlocked") is not False:
        errors.append("locked ANALYSIS_SPEC unlock flag changed")
    if gates.get("confirmatory_outcomes_unlocked") is not False:
        errors.append("locked DESIGN_GATES unlock flag changed")

    unlock_path=PROC/"CONFIRMATORY_UNLOCK.json"
    unlock_present=unlock_path.exists()
    unlock_valid=False
    if unlock_present:
        u=load(unlock_path)
        unlock_valid=(
            u.get("schema_version")==1
            and u.get("paper_id")=="006"
            and u.get("unlocked") is True
            and u.get("prereg_lock_label")==lock.get("lock_label")
            and u.get("prereg_lock_sha256")==lock.get("combined_sha256")
        )
        if not unlock_valid:
            errors.append("CONFIRMATORY_UNLOCK.json does not match preregistration lock")

    paper=load(ROOT/"paper.json")
    status=paper.get("status")
    if a.require_unlock:
        if not unlock_present:
            errors.append("confirmatory unlock record missing")
        elif not unlock_valid:
            errors.append("confirmatory unlock invalid")
        if status not in {"analysis","manuscript"}:
            errors.append(f"paper status not analysis/manuscript: {status}")

    result={
        "script":"31_verify_prereg_lock.py",
        "require_unlock":a.require_unlock,
        "lock_label":lock.get("lock_label"),
        "combined_sha256":lock.get("combined_sha256"),
        "locked_files_checked":len(lock.get("file_sha256") or {}),
        "unlock_present":unlock_present,
        "unlock_valid":unlock_valid,
        "paper_status":status,
        "errors":errors,
        "valid":not errors,
        "effect_estimation_performed":False,
    }
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if errors:
        raise SystemExit(1)

if __name__=="__main__":
    main()
