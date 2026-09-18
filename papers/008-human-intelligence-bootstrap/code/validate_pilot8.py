"""Structural validation for ARIS4C008 Pilot 8.

No network calls. Validates committed derived artifacts and design invariants.
"""
from __future__ import annotations
import csv, json
from collections import Counter,defaultdict
from pathlib import Path

def read(path):
    return list(csv.DictReader(open(path,encoding="utf-8-sig")))

def require(ok,msg):
    if not ok: raise AssertionError(msg)
    print("PASS",msg)

def main():
    base=Path(__file__).resolve().parents[1]
    pool=read(base/"data"/"screening_pool_expanded_v1.csv")
    wave=read(base/"data"/"screening_next_wave_v0.csv")
    tax=read(base/"data"/"screening_pool_taxonomy_v0.csv")
    tier=read(base/"data"/"module_evidence_state_tier1_v0.csv")
    features=read(base/"data"/"screening_features_v0.csv")
    queue=read(base/"data"/"deep_coding_queue_v0.csv")
    evidence=read(base/"data"/"theory_candidate_evidence_seed_v0.csv")
    rec=read(base/"data"/"tier1_recoverability_v2.csv")
    gates=json.load(open(base/"process"/"DESIGN_GATES.json",encoding="utf-8"))

    pnames=[r["scientific_name"] for r in pool]
    require(len(pool)==238,"screening pool has 238 rows")
    require(len(set(pnames))==238,"screening pool scientific names are unique")
    require(sum(r["current_panel"]=="yes" for r in pool)==29,"screening pool retains exactly 29 Pilot-7 taxa")

    require(len(wave)==50,"Tier-1 next wave has exactly 50 new taxa")
    require(len(set(r["scientific_name"] for r in wave))==50,"Tier-1 next-wave taxa are unique")
    require(not (set(r["scientific_name"] for r in wave)&{r["scientific_name"] for r in pool if r["current_panel"]=="yes"}),"Tier-1 next wave excludes the retained 29")

    roles=Counter(r["pool_role"] for r in wave)
    require(roles["theory_discriminating_candidate"]==14,"Tier-1 contains 14 theory-discriminating taxa")
    require(roles["data_rich_underrepresented_clade_calibration"]==15,"Tier-1 contains 15 underrepresented-clade controls")
    require(roles["database_unrepresented_family_mass_calibration"]==10,"Tier-1 contains 10 matched-family controls")
    require(sum(v for k,v in roles.items() if k not in {"theory_discriminating_candidate","data_rich_underrepresented_clade_calibration","database_unrepresented_family_mass_calibration"})==11,"Tier-1 contains 11 source candidates")

    require(len(features)==238,"screening feature matrix has one row per pool taxon")
    require(set(r["scientific_name"] for r in features)==set(pnames),"screening features cover the exact 238-taxon pool")

    require(len(tax)==238,"taxonomy table has one row per operational taxon")
    require(set(r["query_name"] for r in tax)==set(pnames),"taxonomy table covers the exact 238-taxon pool")
    require(sum(r["resolution_status"]=="manual_legacy_ott_crosswalk" for r in tax)==1,"taxonomy table has one manual legacy OTT crosswalk")

    require(len(queue)==50,"deep-coding queue has exactly 50 rows")
    require(set(r["scientific_name"] for r in queue)==set(r["scientific_name"] for r in wave),"deep-coding queue equals Tier-1 next wave")

    require(len(evidence)>=21,"theory-candidate exact-species seed has at least 21 rows")
    require(len({r["scientific_name"] for r in evidence})==14,"all 14 theory candidates have evidence seed coverage")

    require(len(tier)==790,"Tier-1 module matrix has 79 x 10 = 790 rows")
    taxa=list(dict.fromkeys(r["scientific_name"] for r in tier))
    mods=list(dict.fromkeys(r["module_id"] for r in tier))
    require(len(taxa)==79,"Tier-1 module matrix has 79 taxa")
    require(len(mods)==10 and set(mods)==set("ABCDEFGHIJ"),"Tier-1 module matrix has A-J exactly once per taxon")
    counts=Counter((r["scientific_name"],r["module_id"]) for r in tier)
    require(all(v==1 for v in counts.values()) and len(counts)==790,"Tier-1 module matrix has no duplicate/missing taxon-module cell")

    expected={"A":9,"B":16,"C":11,"D":8,"E":10,"F":21,"G":60,"H":55,"I":53,"J":41}
    actual={m:sum(r["module_id"]==m and r["observed_now"]=="1" for r in tier) for m in "ABCDEFGHIJ"}
    require(actual==expected,f"Tier-1 observed counts match canonical report {expected}")

    scenarios={r["scenario"] for r in rec}
    require("tier1_complete79_oracle_geometry" in scenarios,"v2 recoverability includes oracle-geometry upper bound")
    require("tier1_empirical79" in scenarios and "tier1_complete79" in scenarios,"v2 recoverability includes empirical and complete 79 benchmarks")

    mg=next(g for g in gates["gates"] if g["id"]=="model_recoverability")
    require(mg["status"]=="blocked","model recoverability gate remains blocked")

    print("VALIDATION_OK")

if __name__=="__main__":
    main()
