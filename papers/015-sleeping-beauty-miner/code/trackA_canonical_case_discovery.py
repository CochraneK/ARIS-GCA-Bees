"""Canonical Sleeping-Beauty case discovery for ARIS4C015.

A candidate is promoted to the Track-M mechanism case library only when it
passes BOTH:
1) the absolute retrospective robust-SB gate; and
2) cohort-relative early-low / late-high state against an independently
   sampled unselected same-field/year reference pool.

The candidate pool may be outcome-enriched to reduce discovery cost. Therefore
this workflow is for case discovery only, never prevalence or prospective
performance estimation.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

from mechanism_labels import classify_mechanism_state, robust_sleeping_beauty_gate
from openalex_adapter import reconstruct_history_for_known_work, sample_works


def pct(value:int, ref:list[int]) -> float:
    if not ref:
        raise ValueError("reference distribution is empty")
    less=sum(x<value for x in ref)
    equal=sum(x==value for x in ref)
    return (less+0.5*equal)/len(ref)


def acquire(filters:str,n:int,seed:int,end_year:int):
    works=sample_works(filters=filters,sample_size=n,seed=seed)
    rows=[]
    for w in works:
        if w.publication_year is None:
            continue
        h=reconstruct_history_for_known_work(
            w,publication_year=int(w.publication_year),end_year=end_year,max_records=None
        )
        rows.append((w,h))
    return rows


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base-filters",required=True)
    p.add_argument("--field",required=True)
    p.add_argument("--reference-seed",type=int,required=True)
    p.add_argument("--candidate-seed",type=int,required=True)
    p.add_argument("--reference-n",type=int,default=100)
    p.add_argument("--candidate-n",type=int,default=100)
    p.add_argument("--end-year",type=int,default=2025)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()

    ref=acquire(a.base_filters,a.reference_n,a.reference_seed,a.end_year)
    candidates=acquire(a.base_filters+",cited_by_count:>50",a.candidate_n,a.candidate_seed,a.end_year)

    early_ref=[sum(h.counts[:5]) for _,h in ref]
    late_ref=[sum(h.counts[-5:]) for _,h in ref]

    records=[]
    for w,h in candidates:
        gate=robust_sleeping_beauty_gate(
            h.counts,
            sleep_mode="VARIABLE_SLEEP",
            min_sleep_years=5,
            wake_years=4,
            max_sleep_rate=2.0,
            min_wake_rate=5.0,
            min_total_citations=50,
        )
        early=sum(h.counts[:5]); late=sum(h.counts[-5:])
        ep=pct(early,early_ref); lp=pct(late,late_ref)
        state=classify_mechanism_state(
            early_percentile=ep,
            late_percentile=lp,
            robust_sb=gate.robust_sb,
            early_count=early,
            late_count=late,
            zero_counts_are_low=True,
            require_robust_sb_for_sleeping_beauty=True,
        )
        records.append({
            "openalex_id":w.openalex_id,
            "doi":w.doi,
            "title":w.title,
            "publication_year":w.publication_year,
            "reference_count":w.referenced_works_count,
            "author_count":w.authorship_count,
            "current_cited_by_count":w.cited_by_count,
            "citations_through_endpoint":h.total_citations,
            "early_5y_citations":early,
            "late_5y_citations":late,
            "early_percentile_vs_unselected_reference":ep,
            "late_percentile_vs_unselected_reference":lp,
            "robust_gate":gate.robust_sb,
            "beauty_coefficient":gate.beauty_coefficient,
            "awakening_age":gate.awakening_age,
            "canonical_mechanism_state":state.state,
            "canonical_sb":state.state=="SLEEPING_BEAUTY",
        })

    canonical=[r for r in records if r["canonical_sb"]]
    robust=[r for r in records if r["robust_gate"]]
    result={
        "track":"A_CANONICAL_CASE_DISCOVERY_FOR_M",
        "field":a.field,
        "base_filters":a.base_filters,
        "observation_end_year":a.end_year,
        "reference_pool":{
            "selection_on_present_day_citation_count":False,
            "requested_n":a.reference_n,
            "analyzed_n":len(ref),
            "seed":a.reference_seed,
        },
        "candidate_pool":{
            "selection_on_present_day_citation_count":True,
            "requested_n":a.candidate_n,
            "analyzed_n":len(candidates),
            "seed":a.candidate_seed,
        },
        "canonical_rule":{
            "absolute_robust_gate":True,
            "early_low_rule":"early_5y_percentile <= 0.25 OR exact early_5y_citations == 0",
            "late_high_rule":"late_5y_percentile >= 0.75 with nonzero late attention",
            "reference_population":"independent unselected same-field/year OpenAlex sample",
            "zero_counts_are_low":True
        },
        "robust_gate_candidates_n":len(robust),
        "canonical_sb_n":len(canonical),
        "robust_noncanonical_n":len(robust)-len(canonical),
        "prevalence_estimation_allowed":False,
        "prospective_performance_allowed":False,
        "canonical_cases":canonical,
        "candidate_records":records,
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "field":a.field,
        "reference_n":len(ref),
        "candidate_n":len(candidates),
        "robust_gate_candidates_n":len(robust),
        "canonical_sb_n":len(canonical),
        "robust_noncanonical_n":len(robust)-len(canonical),
        "canonical_ids":[x["openalex_id"] for x in canonical],
    },indent=2))

if __name__=="__main__":
    main()
