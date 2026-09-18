#!/usr/bin/env python3
"""Aggregate ARIS4C006 per-field convention artifacts.

Outcome-blind: concatenates measurement outputs and checks structural coverage.
"""
from __future__ import annotations
import argparse,csv,json,statistics
from pathlib import Path

def read_csvs(root,name):
    rows=[]
    for p in sorted(root.rglob(name)):
        with p.open(encoding="utf-8",newline="") as h:
            rows.extend(list(csv.DictReader(h)))
    return rows

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def f(x):
    try:return float(x)
    except:return None

def truth(x):
    return str(x).lower()=="true"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("artifact_root")
    ap.add_argument("--outdir",required=True)
    a=ap.parse_args()
    root=Path(a.artifact_root);out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)

    annual=read_csvs(root,"annual_convention.csv")
    rolling=read_csvs(root,"rolling_exposure.csv")
    works=read_csvs(root,"convention_work_contributions.csv")
    manifests=[]
    for p in sorted(root.rglob("manifest.json")):
        try:
            j=json.loads(p.read_text(encoding="utf-8"))
            if j.get("script")=="22_materialize_field_convention.py":manifests.append(j)
        except Exception:pass

    write_csv(out/"annual_convention_all_fields.csv",annual)
    write_csv(out/"rolling_exposure_all_fields.csv",rolling)
    write_csv(out/"convention_work_contributions_all_fields.csv",works)

    fields=sorted({int(x["field_id"]) for x in annual})
    years=sorted({int(x["year"]) for x in annual})
    targets=sorted({int(x["target_year"]) for x in rolling})
    D=[f(x["D"]) for x in rolling if f(x["D"]) is not None]
    D3=[f(x["D3"]) for x in rolling if f(x["D3"]) is not None]
    unsupported=[x for x in rolling if not truth(x["primary_full_field_supported"])]
    unsupported3=[x for x in rolling if not truth(x["robustness_3plus_supported"])]
    below_annual=[x for x in annual if not truth(x["annual_target_met"])]

    write_csv(out/"unsupported_primary_contexts.csv",unsupported)
    write_csv(out/"unsupported_3plus_contexts.csv",unsupported3)
    write_csv(out/"below_annual_target.csv",below_annual)

    expected_fields=list(range(11,37))
    manifest={
        "script":"23_aggregate_final_convention.py",
        "confirmatory_use_allowed":False,
        "expected_fields":expected_fields,
        "fields_found":fields,
        "all_26_fields_present":fields==expected_fields,
        "annual_years_found":years,
        "focal_target_years_found":targets,
        "annual_cells":len(annual),
        "expected_annual_cells":26*17,
        "annual_cells_target_met":sum(truth(x["annual_target_met"]) for x in annual),
        "rolling_cells":len(rolling),
        "expected_rolling_cells":26*15,
        "rolling_primary_supported":sum(truth(x["primary_full_field_supported"]) for x in rolling),
        "rolling_primary_unsupported":len(unsupported),
        "rolling_3plus_supported":sum(truth(x["robustness_3plus_supported"]) for x in rolling),
        "rolling_3plus_unsupported":len(unsupported3),
        "rolling_D_min":min(D) if D else None,
        "rolling_D_median":statistics.median(D) if D else None,
        "rolling_D3_min":min(D3) if D3 else None,
        "rolling_D3_median":statistics.median(D3) if D3 else None,
        "valid_convention_work_rows":len(works),
        "per_field_manifests":len(manifests),
        "total_exclusions":{
            k:sum(int((m.get("exclusions") or {}).get(k,0)) for m in manifests)
            for k in sorted({k for m in manifests for k in (m.get("exclusions") or {})})
        },
        "outcomes_opened":False,
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

    if fields != expected_fields:
        raise SystemExit("Not all 26 expected fields are present")
    if len(annual) != 26*17 or len(rolling) != 26*15:
        raise SystemExit("Unexpected convention cell counts")

if __name__=="__main__":
    main()
