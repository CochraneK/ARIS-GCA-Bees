"""Build the Pilot-9 cell-level deep-coding queue.

The queue prioritizes missing A-F cells by:
- module-level coverage deficit;
- extra architecture-discrimination weight for A/B/E;
- within-taxon sparsity;
- cohort stage (remaining21 first pass > retained29 backfill > already-searched second pass).

Scores allocate literature-search effort only. They are not biological importance scores.
"""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

MODULES=list("ABCDEF")
ARCH={"A":1.25,"B":1.30,"C":0.95,"D":1.00,"E":1.25,"F":0.90}
FOCUS={
"A":"innovation / transfer / reversal / planning / novel problem solving",
"B":"social learning / transmission / imitation / teaching / tradition",
"C":"communication / referential / audience / vocal learning / combinatorial",
"D":"tool use / manipulation / construction / object modification",
"E":"persistent externalization / cache / nest / dam / web / modified site",
"F":"cooperation / social tolerance / network / division of labour / collective decision",
}

def read(p):
    return list(csv.DictReader(open(p,encoding="utf-8-sig")))

def main():
    base=Path(__file__).resolve().parents[1]
    matrix=read(base/"data"/"module_evidence_state_tier1_v1.csv")
    queue=read(base/"data"/"deep_coding_queue_v0.csv")
    roles={r["scientific_name"]:r["pool_role"] for r in queue}

    module_observed={m:sum(r["module_id"]==m and r["observed_now"]=="1" for r in matrix) for m in MODULES}
    tax_observed=defaultdict(int)
    for r in matrix:
        if r["module_id"] in MODULES and r["observed_now"]=="1":
            tax_observed[r["scientific_name"]]+=1

    out=[]
    for r in matrix:
        m=r["module_id"]
        if m not in MODULES or r["observed_now"]=="1":
            continue
        if r["matrix_segment"]=="current29":
            cohort,cohort_weight,round_="retained29_backfill",1.25,"systematic_backfill"
        elif r["evidence_level"]=="pilot9_deep_code":
            cohort,cohort_weight,round_="pilot9_deep29_second_pass",0.85,"targeted_second_pass"
        else:
            cohort,cohort_weight,round_="remaining21_first_pass",1.35,"standardized_first_pass"

        deficit=(79-module_observed[m])/79
        sparse=(6-tax_observed[r["scientific_name"]])/6
        raw=0.42*deficit*ARCH[m]+0.33*sparse+0.25*(cohort_weight/1.35)
        out.append({
            "scientific_name":r["scientific_name"],"module_id":m,
            "module_bundle":"ABE_core" if m in "ABE" else "CDF_support",
            "cohort":cohort,"pool_role":roles.get(r["scientific_name"],"retained_pilot7"),
            "current_state":r["evidence_state"],"current_AF_observed":tax_observed[r["scientific_name"]],
            "module_observed_79":module_observed[m],"raw_score":raw,
            "search_round":round_,"search_focus":FOCUS[m],
        })

    max_score=max(r["raw_score"] for r in out)
    for r in out:r["priority_score"]=100*r["raw_score"]/max_score
    out.sort(key=lambda r:(-r["priority_score"],r["scientific_name"],r["module_id"]))
    for i,r in enumerate(out,1):r["queue_rank"]=i

    fields=["queue_rank","scientific_name","module_id","module_bundle","cohort","pool_role","current_state",
            "current_AF_observed","module_observed_79","priority_score","search_round","search_focus"]
    with open(base/"data"/"deep_coding_cell_queue_v1.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in out:
            z={k:r[k] for k in fields};z["priority_score"]=f'{r["priority_score"]:.2f}';w.writerow(z)
    print("cells",len(out))
    print("module_observed",module_observed)

if __name__=="__main__":
    main()
