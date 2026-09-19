#!/usr/bin/env python3
"""Merge timeout-safe ARIS4C006 field-36 chunk outputs.

This is engineering-only fallback logic. It does not change frozen sampling
seeds, eligibility rules, thresholds, or scientific variables.

Convention chunks intentionally overlap source years so each target-year
rolling window can be computed within one chunk. Duplicate annual/work rows
from overlaps must be byte-equivalent in scientific fields or the merge fails.

Primary-frame chunks are non-overlapping focal-year ranges.
"""
from __future__ import annotations
import argparse,csv,json,math
from collections import Counter
from pathlib import Path

def read_rows(root,name):
    out=[]
    for p in sorted(Path(root).rglob(name)):
        with p.open(encoding="utf-8",newline="") as h:
            out.extend(list(csv.DictReader(h)))
    return out

def write_rows(path,rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def load_manifests(root,script):
    out=[]
    for p in sorted(Path(root).rglob("manifest.json")):
        try:
            j=json.loads(p.read_text(encoding="utf-8"))
            if j.get("script")==script:out.append(j)
        except Exception:pass
    return out

def normrow(r,ignore=()):
    return {k:str(v) for k,v in r.items() if k not in set(ignore)}

def dedupe_exact(rows,key,ignore=()):
    seen={};dups=0
    for r in rows:
        k=tuple(r[x] for x in key)
        if k in seen:
            if normrow(seen[k],ignore)!=normrow(r,ignore):
                raise SystemExit(f"non-identical duplicate for key={k}")
            dups+=1
        else:seen[k]=r
    return list(seen.values()),dups

def truth(x):return str(x).strip().lower()=="true"

def merge_convention(root,outdir):
    annual=read_rows(root,"annual_convention.csv")
    rolling=read_rows(root,"rolling_exposure.csv")
    works=read_rows(root,"convention_work_contributions.csv")
    mans=load_manifests(root,"22_materialize_field_convention.py")
    if not mans:raise SystemExit("no convention chunk manifests")

    annual,dup_a=dedupe_exact(annual,["field_id","year"])
    rolling,dup_r=dedupe_exact(rolling,["field_id","target_year"])
    works,dup_w=dedupe_exact(works,["field_id","year","work_id"])

    annual=sorted(annual,key=lambda r:int(r["year"]))
    rolling=sorted(rolling,key=lambda r:int(r["target_year"]))
    works=sorted(works,key=lambda r:(int(r["year"]),r["work_id"]))

    if {int(r["field_id"]) for r in annual}!={36}:raise SystemExit("convention merge field !=36")
    if [int(r["year"]) for r in annual]!=list(range(2008,2025)):
        raise SystemExit("field36 convention annual years incomplete")
    if [int(r["target_year"]) for r in rolling]!=list(range(2011,2026)):
        raise SystemExit("field36 rolling years incomplete")

    D=[float(r["D"]) for r in rolling]
    D3=[float(r["D3"]) for r in rolling]
    fname=annual[0]["field_name"]
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    write_rows(out/"annual_convention.csv",annual)
    write_rows(out/"rolling_exposure.csv",rolling)
    write_rows(out/"convention_work_contributions.csv",works)
    manifest={
      "script":"22_materialize_field_convention.py",
      "confirmatory_use_allowed":False,
      "field_id":36,
      "field_name":fname,
      "source_years":[2008,2024],
      "focal_years":[2011,2025],
      "annual_information_targets":{"D":35.0,"D3":20.0},
      "max_blocks_per_field_year":4,
      "annual_cells":len(annual),
      "annual_cells_target_met":sum(truth(r["annual_target_met"]) for r in annual),
      "rolling_cells":len(rolling),
      "rolling_primary_supported":sum(truth(r["primary_full_field_supported"]) for r in rolling),
      "rolling_3plus_supported":sum(truth(r["robustness_3plus_supported"]) for r in rolling),
      "valid_convention_works":len(works),
      "unique_canonical_authors_in_convention_sample":len({
        a for r in works for a in str(r.get("canonical_author_ids") or "").split(";") if a
      }),
      "exclusions":{},
      "field_assignment":"primary_topic.field.id",
      "work_types":["article","conference-paper"],
      "china_filter":"at least one CN-affiliated authorship",
      "authorship_cap_rule":"exclude len(authorships)>=100",
      "outcomes_opened":False,
      "chunked_fallback":True,
      "chunk_manifests":len(mans),
      "duplicate_annual_rows_verified_identical":dup_a,
      "duplicate_rolling_rows_verified_identical":dup_r,
      "duplicate_work_rows_verified_identical":dup_w,
      "note":"Overlap-year exclusion counters are not summed because chunk overlap would double-count exclusions; no acceptance rule depends on exclusion totals."
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"convention":manifest},indent=2,ensure_ascii=False))

def merge_primary(root,outdir):
    counts=read_rows(root,"field_year_counts.csv")
    focal=read_rows(root,"primary_focal_rows.csv")
    works=read_rows(root,"primary_work_rows.csv")
    mans=load_manifests(root,"24_materialize_primary_frame.py")
    if not mans:raise SystemExit("no primary chunk manifests")

    counts,dup_c=dedupe_exact(counts,["field_id","year"])
    works,dup_w=dedupe_exact(works,["field_id","year","work_id"])
    focal,dup_f=dedupe_exact(focal,["field_id","year","work_id","canonical_author_id"])

    counts=sorted(counts,key=lambda r:int(r["year"]))
    works=sorted(works,key=lambda r:(int(r["year"]),r["work_id"]))
    focal=sorted(focal,key=lambda r:(int(r["year"]),r["work_id"],r["canonical_author_id"]))

    if {int(r["field_id"]) for r in counts}!={36}:raise SystemExit("primary merge field !=36")
    if [int(r["year"]) for r in counts]!=list(range(2011,2026)):
        raise SystemExit("field36 primary years incomplete")

    status=Counter(r["cell_status"] for r in counts)
    exclusions=Counter()
    for m in mans:
        exclusions.update({k:int(v) for k,v in (m.get("exclusions") or {}).items()})

    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    write_rows(out/"field_year_counts.csv",counts)
    write_rows(out/"primary_focal_rows.csv",focal)
    write_rows(out/"primary_work_rows.csv",works)
    manifest={
      "script":"24_materialize_primary_frame.py",
      "confirmatory_effect_estimation_allowed":False,
      "field_id":36,
      "field_name":counts[0]["field_name"],
      "focal_years":[2011,2025],
      "target_works_per_field_year":40,
      "minimum_works_per_field_year":20,
      "max_blocks":5,
      "field_year_cells":len(counts),
      "cells_target_met":status.get("target_met",0),
      "cells_retained_below_target":status.get("retain_below_target",0),
      "cells_excluded_below_minimum":status.get("exclude_below_minimum",0),
      "works_retained":len(works),
      "focal_rows_retained":len(focal),
      "unique_focal_authors_retained":len({r["canonical_author_id"] for r in focal}),
      "exclusions":dict(exclusions),
      "surname_map":"aris4c006-surname-map-v2-ccnc",
      "effects_or_pvalues_computed":False,
      "chunked_fallback":True,
      "chunk_manifests":len(mans),
      "duplicate_count_rows_verified_identical":dup_c,
      "duplicate_work_rows_verified_identical":dup_w,
      "duplicate_focal_rows_verified_identical":dup_f
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"primary_frame":manifest},indent=2,ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--convention-root",required=True)
    ap.add_argument("--primary-root",required=True)
    ap.add_argument("--convention-out",required=True)
    ap.add_argument("--primary-out",required=True)
    a=ap.parse_args()
    merge_convention(a.convention_root,a.convention_out)
    merge_primary(a.primary_root,a.primary_out)

if __name__=="__main__":
    main()
