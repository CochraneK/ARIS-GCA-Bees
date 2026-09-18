"""Outcome-enriched retrospective Track-A case discovery for ARIS4C015.

This is deliberately NOT the prospective benchmark. Present-day citation count
may be used to reduce search cost because this stage only discovers candidate
Sleeping Beauties for later retrospective mechanism work. The resulting sample
must never be used to estimate SB prevalence or prospective predictive accuracy.
"""
from __future__ import annotations

import argparse, json
from pathlib import Path

from mechanism_labels import robust_sleeping_beauty_gate
from openalex_adapter import reconstruct_history_for_known_work, sample_works


def run(*, filters: str, sample_size: int, seed: int, end_year: int, output: Path):
    works=sample_works(filters=filters,sample_size=sample_size,seed=seed)
    rows=[]
    for work in works:
        if work.publication_year is None:
            continue
        history=reconstruct_history_for_known_work(
            work,
            publication_year=int(work.publication_year),
            end_year=end_year,
            max_records=None,
        )
        gate=robust_sleeping_beauty_gate(
            history.counts,
            sleep_mode="VARIABLE_SLEEP",
            min_sleep_years=5,
            wake_years=4,
            max_sleep_rate=2.0,
            min_wake_rate=5.0,
            min_total_citations=50,
        )
        rows.append({
            "openalex_id":work.openalex_id,
            "title":work.title,
            "doi":work.doi,
            "publication_year":work.publication_year,
            "current_cited_by_count":work.cited_by_count,
            "citations_through_endpoint":history.total_citations,
            "reference_count":work.referenced_works_count,
            "author_count":work.authorship_count,
            "robust_sb":gate.robust_sb,
            "beauty_coefficient":gate.beauty_coefficient,
            "awakening_age":gate.awakening_age,
            "van_raan":gate.van_raan.as_dict(),
            "component_passes":gate.component_passes,
            "warnings":list(gate.warnings),
        })
    robust=[r for r in rows if r["robust_sb"]]
    near=[r for r in rows if not r["robust_sb"] and r["component_passes"]>=2]
    robust.sort(key=lambda r:(-r["beauty_coefficient"],r["openalex_id"]))
    near.sort(key=lambda r:(-r["component_passes"],-r["beauty_coefficient"],r["openalex_id"]))
    result={
        "track":"A_RETROSPECTIVE_CASE_DISCOVERY",
        "claim_boundary":"Outcome-enriched case discovery only. Not an SB prevalence sample and not valid for prospective predictive evaluation.",
        "filters":filters,
        "sample_size_requested":sample_size,
        "sample_size_analyzed":len(rows),
        "seed":seed,
        "observation_end_year":end_year,
        "selection_on_present_day_citation_count":True,
        "prevalence_estimation_allowed":False,
        "prospective_performance_allowed":False,
        "robust_sb_n":len(robust),
        "near_gate_n":len(near),
        "robust_cases":robust,
        "near_gate_cases":near,
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "track":result["track"],
        "filters":filters,
        "n":len(rows),
        "robust_sb_n":len(robust),
        "near_gate_n":len(near),
        "prevalence_estimation_allowed":False,
        "prospective_performance_allowed":False,
        "top_robust":[{"id":x["openalex_id"],"B":round(x["beauty_coefficient"],2),"awakening_age":x["awakening_age"]} for x in robust[:10]],
    },ensure_ascii=False,indent=2))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--filters",required=True)
    p.add_argument("--sample-size",type=int,default=100)
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--end-year",type=int,default=2025)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    run(filters=a.filters,sample_size=a.sample_size,seed=a.seed,end_year=a.end_year,output=a.output)


if __name__=="__main__":
    main()
