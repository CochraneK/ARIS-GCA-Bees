#!/usr/bin/env python3
"""ARIS4C006 — post-unlock exact-LOAO model-frame builder for H1/H2.

Refuses to run unless the preregistration lock exists and both canonical
machine-readable gate files explicitly set confirmatory_outcomes_unlocked=true.
It constructs model inputs only and does not estimate effects.
"""
from __future__ import annotations
import argparse,csv,json,subprocess,sys
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROC=ROOT/"process"

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def read_csv(path):
    with Path(path).open(encoding="utf-8",newline="") as h:
        return list(csv.DictReader(h))

def write_csv(path,rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def truth(x):
    return str(x).strip().lower()=="true" if isinstance(x,str) else bool(x)

def guard():
    verifier=ROOT/"code"/"31_verify_prereg_lock.py"
    p=subprocess.run([sys.executable,str(verifier),"--require-unlock"],capture_output=True,text=True)
    if p.returncode!=0:
        raise SystemExit("LOCKED/INVALID PREREG STATE:\n"+p.stdout+"\n"+p.stderr)
    return load_json(PROC/"PREREGISTRATION_LOCK.json")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--focal-rows",required=True)
    ap.add_argument("--rolling-exposure",required=True)
    ap.add_argument("--convention-contributions",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--manifest",required=True)
    a=ap.parse_args()

    lock=guard()
    focal=read_csv(a.focal_rows)
    rolling=read_csv(a.rolling_exposure)
    contrib=read_csv(a.convention_contributions)

    totals={}
    for r in rolling:
        totals[(int(r["field_id"]),int(r["target_year"]))]={
            "N":float(r["N"]),"D":float(r["D"]),
            "N3":float(r["N3"]),"D3":float(r["D3"]),
        }

    # Each work stores de-duplicated canonical author IDs. A convention work from
    # year y contributes to focal target years y+1, y+2, y+3.
    own=defaultdict(lambda:[0.0,0.0,0.0,0.0])
    for r in contrib:
        field=int(r["field_id"]);year=int(r["year"])
        num=float(r["num"]);den=float(r["den"]);team=int(r["team_size"])
        authors={x for x in str(r.get("canonical_author_ids") or "").split(";") if x}
        for target in (year+1,year+2,year+3):
            if not 2011<=target<=2025:continue
            for aid in authors:
                z=own[(aid,field,target)]
                z[0]+=num;z[1]+=den
                if team>=3:
                    z[2]+=num;z[3]+=den

    rows=[];excluded=defaultdict(int)
    for r in focal:
        field=int(r["field_id"]);year=int(r["year"]);aid=r["canonical_author_id"]
        total=totals.get((field,year))
        if not total:
            excluded["missing_field_year_exposure"]+=1;continue
        z=own.get((aid,field,year),(0.0,0.0,0.0,0.0))
        N=total["N"]-z[0];D=total["D"]-z[1]
        if D<50:
            excluded["loao_D_below_50"]+=1;continue
        N3=total["N3"]-z[2];D3=total["D3"]-z[3]
        q=dict(r)
        q["loao_exposure"]=N/D
        q["loao_D"]=D
        q["loao_3plus_exposure"]=(N3/D3) if D3>=50 else ""
        q["loao_3plus_D"]=D3
        q["field_year_cluster"]=f"{field}_{year}"
        rows.append(q)

    write_csv(a.out,rows)
    manifest={
        "script":"29_build_confirmatory_loao_frame.py",
        "prereg_lock_label":lock.get("lock_label"),
        "prereg_lock_sha256":lock.get("combined_sha256"),
        "confirmatory_unlock_verified":True,
        "focal_rows_input":len(focal),
        "focal_rows_retained":len(rows),
        "loao_D_threshold":50,
        "exclusions":dict(excluded),
        "effect_estimation_performed":False,
    }
    Path(a.manifest).parent.mkdir(parents=True,exist_ok=True)
    Path(a.manifest).write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
