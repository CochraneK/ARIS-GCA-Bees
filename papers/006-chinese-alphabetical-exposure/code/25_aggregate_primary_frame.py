#!/usr/bin/env python3
"""Aggregate ARIS4C006 outcome-locked primary-frame artifacts.

Structural aggregation only. No H1/H2/H3 coefficient, correlation, p-value,
or predictor-outcome cross-tab is computed.
"""
from __future__ import annotations
import argparse,csv,json
from collections import Counter
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
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("artifact_root")
    ap.add_argument("--outdir",required=True)
    a=ap.parse_args()
    root=Path(a.artifact_root);out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)

    counts=read_csvs(root,"field_year_counts.csv")
    focal=read_csvs(root,"primary_focal_rows.csv")
    works=read_csvs(root,"primary_work_rows.csv")
    manifests=[]
    for p in sorted(root.rglob("manifest.json")):
        try:
            j=json.loads(p.read_text(encoding="utf-8"))
            if j.get("script")=="24_materialize_primary_frame.py":manifests.append(j)
        except Exception:
            pass

    fields=sorted({int(x["field_id"]) for x in counts})
    years=sorted({int(x["year"]) for x in counts})
    expected_fields=list(range(11,37))
    expected_years=list(range(2011,2026))
    status=Counter(x["cell_status"] for x in counts)

    # Aggregate structural exclusion counts from manifests only.
    exclusion_keys=sorted({k for m in manifests for k in (m.get("exclusions") or {})})
    exclusions={k:sum(int((m.get("exclusions") or {}).get(k,0)) for m in manifests) for k in exclusion_keys}

    manifest={
        "script":"25_aggregate_primary_frame.py",
        "confirmatory_effect_estimation_allowed":False,
        "effects_or_pvalues_computed":False,
        "fields_found":fields,
        "all_26_fields_present":fields==expected_fields,
        "years_found":years,
        "all_15_focal_years_present":years==expected_years,
        "field_year_cells":len(counts),
        "expected_field_year_cells":26*15,
        "cell_status_counts":dict(status),
        "works_retained":len(works),
        "focal_rows_retained":len(focal),
        "unique_canonical_authors_retained":len({x["canonical_author_id"] for x in focal if x.get("canonical_author_id")}),
        "field_year_clusters_retained":len({(x["field_id"],x["year"]) for x in works}),
        "surname_route_counts":dict(Counter(x["surname_route"] for x in focal)),
        "team_size_min":min((int(x["team_size"]) for x in works),default=None),
        "team_size_max":max((int(x["team_size"]) for x in works),default=None),
        "focal_rows_per_work_min":min((int(x["focal_rows"]) for x in works),default=None),
        "focal_rows_per_work_max":max((int(x["focal_rows"]) for x in works),default=None),
        "total_exclusions":exclusions,
        "safety_note":"This aggregator does not compute any association between RelAlphaRank/exposure and listed position/first-listed outcomes."
    }

    write_csv(out/"field_year_counts_all_fields.csv",counts)
    # Persist rows for downstream preregistered execution, but do not summarize
    # predictor-outcome relationships here.
    write_csv(out/"primary_work_rows_all_fields.csv",works)
    write_csv(out/"primary_focal_rows_all_fields.csv",focal)
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

    if fields!=expected_fields:
        raise SystemExit("not all 26 fields present")
    if years!=expected_years or len(counts)!=26*15:
        raise SystemExit("unexpected field-year frame coverage")
    if not works or not focal:
        raise SystemExit("empty primary frame")

if __name__=="__main__":
    main()
