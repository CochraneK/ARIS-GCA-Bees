"""Export one reproducible OpenAlex historical shard for Pilot M.

The exporter performs no Sleeping Beauty classification. It only freezes the
raw ingredients needed by the merged mechanism cohort:

- sampled work identifiers and metadata;
- annual citation histories through a fixed endpoint;
- reference and author counts.

Multiple shards can then be merged before field/cohort percentile
normalization, avoiding shard-specific trajectory labels.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from openalex_adapter import reconstruct_history_for_known_work, sample_works


DEFAULT_FILTERS = (
    "publication_year:1980,type:article,primary_topic.field.id:31"
)


def export_shard(
    *,
    sample_size: int = 100,
    seed: int,
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

        papers.append(
            {
                "paper_id": work.openalex_id,
                "publication_year": int(work.publication_year),
                "field": "OPENALEX_PRIMARY_FIELD_31",
                "annual_citation_counts": list(history.counts),
                "reference_count": work.referenced_works_count,
                "author_count": work.authorship_count,
                "source_id": None,
                "title": work.title,
                "doi": work.doi,
                "primary_topic": work.primary_topic,
                "current_cited_by_count": work.cited_by_count,
                "citations_through_endpoint": history.total_citations,
            }
        )

    return {
        "dataset_type": "raw historical mechanism shard",
        "provenance": {
            "source": "OpenAlex live API",
            "filters": filters,
            "sample_size_requested": sample_size,
            "sample_size_exported": len(papers),
            "seed": seed,
            "observation_end_year": observation_end_year,
            "selection_on_future_citation_count": False,
        },
        "papers": papers,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=100)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--filters", default=DEFAULT_FILTERS)
    parser.add_argument("--observation-end-year", type=int, default=2011)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = export_shard(
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
