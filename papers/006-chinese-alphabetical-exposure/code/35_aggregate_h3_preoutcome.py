#!/usr/bin/env python3
"""Aggregate ARIS4C006 outcome-blind H3 cohort shards and apply frozen gates."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def read_rows(root,name):
    out=[]
    for p in sorted(Path(root).rglob(name)):
        with p.open(encoding="utf-8",newline="") as h:out.extend(list(csv.DictReader(h)))
    return out

def write_csv(path,rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("artifact_root")
    ap.add_argument("--outdir",required=True)
    a=ap.parse_args()
    root=Path(a.artifact_root);out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    rows=read_rows(root,"h3_preoutcome_cohort.csv")
    mans=[]
    for p in sorted(root.rglob("manifest.json")):
        try:
            j=json.loads(p.read_text(encoding="utf-8"))
            if j.get("script")=="34_build_h3_preoutcome_cohort.py":mans.append(j)
        except Exception:pass

    by={}
    for r in rows:
        aid=r["canonical_author_id"]
        if aid in by:raise SystemExit(f"duplicate canonical author across shards: {aid}")
        by[aid]=r
    rows=list(by.values())
    validated=[r for r in rows if int(r["validated_entry"])==1]
    final=[r for r in rows if int(r["final_h3_eligible_preoutcome"])==1]
    years=sorted({int(r["entry_year"]) for r in validated})
    fields=sorted({int(r["entry_primary_field"]) for r in validated})
    orcid=sum(int(r["orcid_anchored"]) for r in final)
    low=sum(int(r["low_identity_risk"]) for r in final)

    checks={
      "validated_entry_authors_ge_1000":len(validated)>=1000,
      "final_h3_authors_ge_750":len(final)>=750,
      "all_7_entry_years":years==list(range(2014,2021)),
      "entry_fields_ge_20":len(fields)>=20,
      "orcid_anchored_final_ge_100":orcid>=100,
      "low_identity_risk_final_ge_500":low>=500,
    }
    passed=all(checks.values())
    write_csv(out/"h3_preoutcome_cohort_all.csv",rows)
    manifest={
      "script":"35_aggregate_h3_preoutcome.py",
      "confirmatory_outcomes_unlocked":False,
      "persistence_outcome_computed":False,
      "effect_or_pvalue_computed":False,
      "shard_manifests":len(mans),
      "unique_candidate_authors":len(rows),
      "validated_entry_authors":len(validated),
      "final_h3_eligible_preoutcome":len(final),
      "entry_years":years,
      "entry_fields":fields,
      "orcid_anchored_final":orcid,
      "low_identity_risk_final":low,
      "frozen_structural_checks":checks,
      "h3_structural_gate_pass":passed,
      "decision":"retain H3 in confirmatory secondary family" if passed else "remove H3 from confirmatory family; do not relax sampling or adequacy rules",
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))
    if not passed:raise SystemExit(2)

if __name__=="__main__":
    main()
