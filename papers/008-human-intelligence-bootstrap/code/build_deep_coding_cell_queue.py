"""Build the current Pilot-9 cell-level A-F deep-coding queue.

Input: module_evidence_state_tier1_v2.csv.
All 50 added taxa have completed standardized first-pass deep coding.
Therefore remaining cells are either:
- retained29_backfill; or
- new50_targeted_second_pass.

Priority is for search allocation only, not biological importance.
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
def read(p): return list(csv.DictReader(open(p,encoding="utf-8-sig")))
def main():
    base=Path(__file__).resolve().parents[1]
    matrix=read(base/"data"/"module_evidence_state_tier1_v2.csv")
    seed=read(base/"data"/"deep_coding_queue_v0.csv")
    roles={r["scientific_name"]:r["pool_role"] for r in seed}
    mo={m:sum(r["module_id"]==m and r["observed_now"]=="1" for r in matrix) for m in MODULES}
    to=defaultdict(int)
    for r in matrix:
        if r["module_id"] in MODULES and r["observed_now"]=="1": to[r["scientific_name"]]+=1
    out=[]
    for r in matrix:
        m=r["module_id"]
        if m not in MODULES or r["observed_now"]=="1": continue
        old=r["matrix_segment"]=="current29"
        cohort="retained29_backfill" if old else "new50_targeted_second_pass"
        cw=1.30 if old else 1.00
        round_="systematic_backfill" if old else "targeted_second_pass"
        deficit=(79-mo[m])/79
        sparse=(6-to[r["scientific_name"]])/6
        raw=0.44*deficit*ARCH[m]+0.34*sparse+0.22*(cw/1.30)
        out.append({"scientific_name":r["scientific_name"],"module_id":m,
                    "module_bundle":"ABE_core" if m in "ABE" else "CDF_support",
                    "cohort":cohort,"pool_role":roles.get(r["scientific_name"],"retained_pilot7"),
                    "current_state":r["evidence_state"],"current_AF_observed":to[r["scientific_name"]],
                    "module_observed_79":mo[m],"raw_score":raw,"search_round":round_,
                    "search_focus":FOCUS[m]})
    mx=max(r["raw_score"] for r in out)
    for r in out:r["priority_score"]=100*r["raw_score"]/mx
    out.sort(key=lambda r:(-r["priority_score"],r["scientific_name"],r["module_id"]))
    for i,r in enumerate(out,1):r["queue_rank"]=i
    fields=["queue_rank","scientific_name","module_id","module_bundle","cohort","pool_role","current_state",
            "current_AF_observed","module_observed_79","priority_score","search_round","search_focus"]
    with open(base/"data"/"deep_coding_cell_queue_v2.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in out:
            z={k:r[k] for k in fields};z["priority_score"]=f'{r["priority_score"]:.2f}';w.writerow(z)
    print("cells",len(out));print("module_observed",mo)
if __name__=="__main__": main()
