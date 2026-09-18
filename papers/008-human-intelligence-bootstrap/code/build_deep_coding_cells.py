"""Build a cell-level A-F deep-coding queue for ARIS4C008.

The queue converts Pilot 8's taxon-level plan into atomic taxon × module tasks.
Missing/not-coded is never treated as absence. Calibration taxa receive higher
priority for explicit tested-negative searches to reduce spectacular-animal bias.
"""
from __future__ import annotations
import csv, json
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
MODULES=set("ABCDEF")

def read(path):
    with open(path,encoding="utf-8-sig",newline="") as h:
        return list(csv.DictReader(h))

def main():
    tier=read(BASE/"data"/"module_evidence_state_tier1_v0.csv")
    taxon_queue={r["scientific_name"]:r for r in read(BASE/"data"/"deep_coding_queue_v0.csv")}
    rows=[]
    for r in tier:
        if r["module_id"] not in MODULES or r["observed_now"]=="1":
            continue
        sp=r["scientific_name"]
        q=taxon_queue.get(sp)
        if q:
            role=q["pool_role"]
            tn=q["tested_negative_priority"]
            base_rank=int(q["tier1_rank"])
            if role in {"data_rich_underrepresented_clade_calibration","database_unrepresented_family_mass_calibration"}:
                priority=1
            elif role=="theory_discriminating_candidate":
                priority=2
            else:
                priority=3
            segment="tier1_new50"
        else:
            role="retained_pilot7_backfill"
            tn="high"
            base_rank=1000
            priority=2
            segment="current29"
        rows.append({
            "priority_band":priority,
            "scientific_name":sp,
            "module_id":r["module_id"],
            "module_name":r["module_name"],
            "matrix_segment":segment,
            "pool_role":role,
            "tested_negative_priority":tn,
            "current_state":r["evidence_state"],
            "required_search":"positive + explicit tested-negative + not-tested documentation",
            "completion_rule":"exact-species evidence state + context + source provenance; silence is missingness",
            "_taxon_rank":base_rank,
        })
    rows.sort(key=lambda x:(x["priority_band"],x["_taxon_rank"],x["scientific_name"],x["module_id"]))
    for i,r in enumerate(rows,1):
        r["cell_rank"]=i
        r.pop("_taxon_rank",None)
    fields=["cell_rank","priority_band","scientific_name","module_id","module_name","matrix_segment","pool_role","tested_negative_priority","current_state","required_search","completion_rule"]
    out=BASE/"data"/"deep_coding_cells_v1.csv"
    with open(out,"w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
    summary={
        "open_A_F_cells":len(rows),
        "priority1_calibration_cells":sum(r["priority_band"]==1 for r in rows),
        "priority2_theory_or_backfill_cells":sum(r["priority_band"]==2 for r in rows),
        "priority3_source_candidate_cells":sum(r["priority_band"]==3 for r in rows),
        "open_by_module":{m:sum(r["module_id"]==m for r in rows) for m in "ABCDEF"},
        "open_by_segment":{s:sum(r["matrix_segment"]==s for r in rows) for s in ["current29","tier1_new50"]},
        "missingness_is_absence":False,
    }
    (BASE/"data"/"deep_coding_cells_v1_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
