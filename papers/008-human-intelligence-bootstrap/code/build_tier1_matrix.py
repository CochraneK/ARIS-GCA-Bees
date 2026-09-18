"""Build the 79-taxon Tier-1 A-J evidence-state matrix.

Inputs:
- module_evidence_state_v2.csv: retained 29-taxon Pilot-7 states
- screening_next_wave_v0.csv: 50 new Tier-1 taxa
- screening_features_v0.csv: low-cost G-J/F screening proxies
- theory_candidate_evidence_seed_v0.csv: exact-species A-F seed evidence

Missing/not-coded is never converted to absence.
"""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

OBSERVED_STATES={
 "measured","partial_measured","measured_multi_axis","measured_ecology",
 "measured_network_proxy","measured_multi_source_proxy","measured_social_demography",
 "measured_cultural_context","positive","positive_with_uncertainty",
 "tested_negative","ambiguous"
}
PROXY_MAP={
 "F":"F_network_proxy",
 "G":"G_life_history_proxy",
 "H":"H_neural_energy_proxy",
 "I":"I_ecology_proxy",
 "J":"J_demography_proxy",
}

def read(path):
    return list(csv.DictReader(open(path,encoding="utf-8-sig")))

def main():
    base=Path(__file__).resolve().parents[1]
    current=read(base/"data"/"module_evidence_state_v2.csv")
    wave=read(base/"data"/"screening_next_wave_v0.csv")
    features=read(base/"data"/"screening_features_v0.csv")
    evidence=read(base/"data"/"theory_candidate_evidence_seed_v0.csv")

    feat={r["scientific_name"]:r for r in features}
    modules=list(dict.fromkeys(r["module_id"] for r in current))
    names={}
    for r in current:
        names.setdefault(r["module_id"],r["module_name"])

    ev=defaultdict(list)
    for r in evidence:
        ev[(r["scientific_name"],r["module_id"])].append(r)

    out=[]
    for r in current:
        observed=(r["evidence_state"] in OBSERVED_STATES or bool((r.get("measurement_coverage") or "").strip()))
        out.append({
          "scientific_name":r["scientific_name"],"module_id":r["module_id"],
          "module_name":r["module_name"],"matrix_segment":"current29",
          "evidence_state":r["evidence_state"],"observed_now":int(observed),
          "evidence_level":"pilot7","source":r.get("measurement_sources",""),
          "basis":r.get("basis",""),
        })

    for w in wave:
        sp=w["scientific_name"]; f=feat.get(sp,{})
        for m in modules:
            ee=ev.get((sp,m),[])
            state="not_systematically_coded"; observed=0
            level=""; source=""; basis=""
            if ee:
                direct=next((x for x in ee if x["evidence_state"]=="positive"),ee[0])
                state=direct["evidence_state"]; observed=1; level="exact_species_seed"
                source=";".join(dict.fromkeys(x["source_id"] for x in ee))
                basis=";".join(dict.fromkeys(x["trait_name"] for x in ee))
            key=PROXY_MAP.get(m)
            proxy=(key is not None and str(f.get(key,"")).strip()=="1")
            if proxy:
                if observed:
                    level=(level+"+screening_proxy").strip("+")
                    source=";".join(x for x in [source,"screening_features_v0"] if x)
                else:
                    state="measured_screening_proxy"; observed=1
                    level="screening_proxy";source="screening_features_v0";basis=key
            out.append({
              "scientific_name":sp,"module_id":m,"module_name":names.get(m,m),
              "matrix_segment":"tier1_new50","evidence_state":state,
              "observed_now":observed,"evidence_level":level,
              "source":source,"basis":basis,
            })

    fields=["scientific_name","module_id","module_name","matrix_segment","evidence_state",
            "observed_now","evidence_level","source","basis"]
    with open(base/"data"/"module_evidence_state_tier1_v0.csv","w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=fields);w.writeheader();w.writerows(out)

    counts={}
    for m in modules:
        rr=[r for r in out if r["module_id"]==m]
        counts[m]={
          "observed":sum(int(r["observed_now"]) for r in rr),
          "total":len(rr),
          "new50_observed":sum(int(r["observed_now"]) for r in rr if r["matrix_segment"]=="tier1_new50"),
        }

    lines=[
      "# Tier-1 79-taxon module matrix · Pilot 8","",
      "This matrix joins the retained 29-taxon Pilot-7 evidence states to the 50 new Tier-1 screening taxa.","",
      "## Current observed coverage",""
    ]
    for m in modules:
        c=counts[m]
        lines.append(f"- **{m} · {names.get(m,m)}:** {c['observed']}/79 observed now; {c['new50_observed']}/50 new-wave taxa already have an exact seed or low-cost screening proxy.")
    lines += [
      "","## Interpretation","",
      "- A–F for new taxa are observed only where exact-species seed evidence exists or an ASNR F proxy is available.",
      "- G–J can be marked measured_screening_proxy from standardized low-cost sources.",
      "- Screening proxies are not confirmatory A–J scores.",
      "- not_systematically_coded is missingness, not biological absence.",
      "","This is the empirical starting mask for Tier-1 deep coding."
    ]
    (base/"process"/"TIER1_MODULE_MATRIX.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("rows",len(out))
    print("counts",counts)

if __name__=="__main__":
    main()
