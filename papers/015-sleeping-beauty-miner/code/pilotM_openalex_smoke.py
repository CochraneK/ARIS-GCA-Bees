"""Real-data smoke test for the ARIS4C015 mechanism track.

This is NOT the final mechanism study.

It samples a reproducible, unfiltered historical field/year cohort from
OpenAlex, reconstructs complete annual citation histories through a fixed
endpoint, then runs the exact robust-SB / four-state / matching pipeline.

Why unfiltered?
---------------
The smoke cohort must retain Forgotten controls. Filtering the entire cohort on
present-day citation count would remove many scientifically important controls
and distort state normalization.

If no robust SB appears, the correct result is mechanism_ready=false.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mechanism_cohort import CorpusPaper, build_mechanism_cohort
from openalex_adapter import (
    reconstruct_history_for_known_work,
    sample_works,
)


DEFAULT_FILTERS = (
    "publication_year:1980,type:article,primary_topic.field.id:31"
)


def run_smoke(
    *,
    sample_size: int = 100,
    seed: int = 15015,
    filters: str = DEFAULT_FILTERS,
    observation_end_year: int = 2011,
    api_key: str | None = None,
) -> dict:
    works = sample_works(
        filters=filters,
        sample_size=sample_size,
        seed=seed,
        api_key=api_key,
    )
    papers = []
    source_rows = []

    for work in works:
        if work.publication_year is None:
            continue
        history = reconstruct_history_for_known_work(
            work,
            publication_year=int(work.publication_year),
            end_year=observation_end_year,
            api_key=api_key,
            max_records=None,
        )
        field = work.primary_topic or "UNKNOWN_PRIMARY_TOPIC"
        papers.append(
            CorpusPaper(
                paper_id=work.openalex_id,
                publication_year=int(work.publication_year),
                field=field,
                annual_citation_counts=history.counts,
                reference_count=work.referenced_works_count,
                author_count=work.authorship_count,
            )
        )
        source_rows.append(
            {
                "paper_id": work.openalex_id,
                "title": work.title,
                "doi": work.doi,
                "current_cited_by_count": work.cited_by_count,
                "primary_topic": work.primary_topic,
                "reference_count": work.referenced_works_count,
                "author_count": work.authorship_count,
                "citations_through_endpoint": history.total_citations,
            }
        )

    # All papers were sampled using the same primary-field filter, but
    # primary_topic display names are finer-grained topics. Use one explicit
    # mechanism stratum label rather than splitting by topic display text.
    normalized = [
        CorpusPaper(
            paper_id=p.paper_id,
            publication_year=p.publication_year,
            field="OPENALEX_PRIMARY_FIELD_31",
            annual_citation_counts=p.annual_citation_counts,
            reference_count=p.reference_count,
            author_count=p.author_count,
            source_id=p.source_id,
        )
        for p in papers
    ]

    result = build_mechanism_cohort(
        normalized,
        min_stratum_size=min(50, len(normalized)),
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
    result["smoke_design"] = {
        "source": "OpenAlex live API",
        "filters": filters,
        "sample_size_requested": sample_size,
        "sample_size_analyzed": len(normalized),
        "seed": seed,
        "observation_end_year": observation_end_year,
        "selection_on_future_citation_count": False,
        "purpose": (
            "real-data mechanism plumbing and rough case-yield diagnostic; "
            "not a prevalence estimate or final mechanism analysis"
        ),
    }
    result["source_metadata"] = source_rows
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=100)
    parser.add_argument("--seed", type=int, default=15015)
    parser.add_argument("--filters", default=DEFAULT_FILTERS)
    parser.add_argument("--observation-end-year", type=int, default=2011)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_smoke(
        sample_size=args.sample_size,
        seed=args.seed,
        filters=args.filters,
        observation_end_year=args.observation_end_year,
        api_key=args.api_key,
    )
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
