"""Build a bounded matched-control mechanism cohort for ARIS4C015.

Cases are discovered retrospectively from an outcome-enriched pool. Controls are
sampled independently from an unselected same-field/year pool and reconstructed
to the same observation endpoint. The enriched case pool is never used for
prevalence or prospective-performance estimation.
"""
from __future__ import annotations

import argparse, json
from pathlib import Path

from mechanism_cohort import CorpusPaper, build_mechanism_cohort
from mechanism_labels import robust_sleeping_beauty_gate
from mechanism_matching import MechanismPaper, nearest_controls, match_balance_diagnostics
from openalex_adapter import reconstruct_history_for_known_work, sample_works


def empirical_percentile(value: int, reference: list[int]) -> float:
    if not reference:
        return 0.5
    less=sum(x < value for x in reference)
    equal=sum(x == value for x in reference)
    return (less + 0.5 * equal) / len(reference)


def acquire(works, *, field: str, end_year: int):
    out=[]
    for work in works:
        if work.publication_year is None:
            continue
        h=reconstruct_history_for_known_work(
            work,
            publication_year=int(work.publication_year),
            end_year=end_year,
            max_records=None,
        )
        out.append((work,h))
    return out


def run(*, base_filters: str, field: str, case_seed: int, control_seed: int,
        sample_size: int, end_year: int, output: Path):
    case_works=sample_works(
        filters=base_filters+",cited_by_count:>50",
        sample_size=sample_size,
        seed=case_seed,
    )
    control_works=sample_works(
        filters=base_filters,
        sample_size=sample_size,
        seed=control_seed,
    )
    case_raw=acquire(case_works,field=field,end_year=end_year)
    control_raw=acquire(control_works,field=field,end_year=end_year)

    robust_cases=[]
    for work,h in case_raw:
        gate=robust_sleeping_beauty_gate(
            h.counts,
            sleep_mode="VARIABLE_SLEEP",
            min_sleep_years=5,
            wake_years=4,
            max_sleep_rate=2.0,
            min_wake_rate=5.0,
            min_total_citations=50,
        )
        if gate.robust_sb:
            robust_cases.append((work,h,gate))

    control_papers=[
        CorpusPaper(
            paper_id=work.openalex_id,
            publication_year=int(work.publication_year),
            field=field,
            annual_citation_counts=tuple(h.counts),
            reference_count=work.referenced_works_count,
            author_count=work.authorship_count,
        )
        for work,h in control_raw
    ]
    control_result=build_mechanism_cohort(
        control_papers,
        min_stratum_size=min(40,len(control_papers)),
        sb_sleep_mode="VARIABLE_SLEEP",
        sb_min_sleep_years=5,
        sb_wake_years=4,
        sb_max_sleep_rate=2.0,
        sb_min_wake_rate=5.0,
        sb_min_total_citations=50,
        controls_per_case=1,
        matching_early_percentile_caliper=0.15,
        matching_max_abs_smd=0.10,
        min_primary_match_rate=0.50,
    )
    forgotten=[
        r for r in control_result["records"]
        if r.get("state")=="FORGOTTEN"
    ]
    early_reference=[
        sum(p.annual_citation_counts[:5])
        for p in control_papers
    ]

    case_models=[]
    case_detail=[]
    for work,h,gate in robust_cases:
        early=sum(h.counts[:5])
        ep=empirical_percentile(early,early_reference)
        case_models.append(MechanismPaper(
            paper_id=work.openalex_id,
            state="SLEEPING_BEAUTY",
            publication_year=int(work.publication_year),
            field=field,
            early_citation_percentile=ep,
            reference_count=work.referenced_works_count,
            author_count=work.authorship_count,
            early_citation_count=early,
        ))
        case_detail.append({
            "paper_id":work.openalex_id,
            "doi":work.doi,
            "title":work.title,
            "early_citation_count":early,
            "early_percentile_vs_unselected_reference":ep,
            "beauty_coefficient":gate.beauty_coefficient,
            "awakening_age":gate.awakening_age,
        })

    control_models=[]
    for r in forgotten:
        ms=r["mechanism_state"]
        control_models.append(MechanismPaper(
            paper_id=r["paper_id"],
            state="FORGOTTEN",
            publication_year=int(r["publication_year"]),
            field=field,
            early_citation_percentile=float(ms["early_percentile"]),
            reference_count=r.get("reference_count"),
            author_count=r.get("author_count"),
            early_citation_count=int(r.get("early_citation_count") or 0),
        ))

    matches,unmatched=nearest_controls(
        case_models,
        control_models,
        control_state="FORGOTTEN",
        controls_per_case=1,
        with_replacement=False,
        year_tolerance=0,
        require_same_field=True,
        early_percentile_caliper=0.15,
    )
    all_models=case_models+control_models
    balance=match_balance_diagnostics(
        matches,
        all_models,
        include_early_attention=True,
        max_abs_smd=0.10,
    )
    match_rate=(len(matches)/len(case_models)) if case_models else 0.0

    result={
        "track":"M_CASE_ENRICHED_MATCHED_CONTROL_PILOT",
        "claim_boundary":"Retrospective mechanism pilot only. Cases are outcome-enriched; controls are unselected. No prevalence or prospective-performance inference.",
        "base_filters":base_filters,
        "field":field,
        "sample_size_each_pool":sample_size,
        "observation_end_year":end_year,
        "case_selection_on_present_day_citations":True,
        "control_selection_on_present_day_citations":False,
        "prevalence_estimation_allowed":False,
        "prospective_performance_allowed":False,
        "case_pool_analyzed_n":len(case_raw),
        "unselected_control_pool_analyzed_n":len(control_raw),
        "robust_case_n":len(case_models),
        "forgotten_control_n":len(control_models),
        "matched_n":len(matches),
        "match_rate":match_rate,
        "unmatched_case_ids":unmatched,
        "balance":balance,
        "mechanism_analysis_ready":(
            len(matches)>=3
            and match_rate>=0.50
            and balance.get("balance_pass") is True
        ),
        "cases":case_detail,
        "matches":[m.as_dict() for m in matches],
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "field":field,
        "case_pool":len(case_raw),
        "control_pool":len(control_raw),
        "robust_cases":len(case_models),
        "forgotten_controls":len(control_models),
        "matched":len(matches),
        "match_rate":match_rate,
        "balance_pass":balance.get("balance_pass"),
        "mechanism_analysis_ready":result["mechanism_analysis_ready"],
    },indent=2))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base-filters",required=True)
    p.add_argument("--field",required=True)
    p.add_argument("--case-seed",type=int,required=True)
    p.add_argument("--control-seed",type=int,required=True)
    p.add_argument("--sample-size",type=int,default=50)
    p.add_argument("--end-year",type=int,default=2025)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    run(
        base_filters=a.base_filters,field=a.field,case_seed=a.case_seed,
        control_seed=a.control_seed,sample_size=a.sample_size,
        end_year=a.end_year,output=a.output,
    )


if __name__=="__main__":
    main()
