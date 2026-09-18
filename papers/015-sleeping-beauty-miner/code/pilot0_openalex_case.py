"""Run one literature-reference Sleeping Beauty case against OpenAlex.

This is a cross-source replication probe, not an exact reproduction of the
Web of Science values in Ke et al. (2015).

Example
-------
python pilot0_openalex_case.py \
  --doi 10.1021/ja01539a017 \
  --case-id ke2015_02 \
  --publication-year 1958 \
  --published-b 10769 \
  --published-awakening-year 2007 \
  --observation-end-year 2011 \
  --output result.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from openalex_adapter import reconstruct_history_from_openalex
from sb_metrics import retrospective_summary


def run_case(
    *,
    doi: str,
    case_id: str,
    publication_year: int,
    published_b: float,
    published_awakening_year: int,
    observation_end_year: int,
    api_key: str | None = None,
) -> dict:
    work, history = reconstruct_history_from_openalex(
        f"https://doi.org/{doi}",
        publication_year=publication_year,
        end_year=observation_end_year,
        api_key=api_key,
        max_records=None,
    )
    metrics = retrospective_summary(history.counts)
    reconstructed_awakening_year = (
        publication_year + int(metrics["awakening_time"])
    )
    reconstructed_b = float(metrics["beauty_coefficient"])

    return {
        "case_id": case_id,
        "target": {
            "doi": doi,
            "openalex_id": work.openalex_id,
            "title": work.title,
            "publication_year": publication_year,
            "primary_topic": work.primary_topic,
        },
        "source": {
            "name": "OpenAlex live API",
            "observation_end_year": observation_end_year,
            "query_semantics": (
                "incoming works citing target with "
                f"to_publication_date:{observation_end_year}-12-31"
            ),
        },
        "trajectory": history.as_dict(),
        "reconstructed": {
            **metrics,
            "awakening_year": reconstructed_awakening_year,
        },
        "reference_ke2015": {
            "beauty_coefficient": published_b,
            "awakening_year": published_awakening_year,
            "source_dataset": "Web of Science",
            "reference_doi": "10.1073/pnas.1424329112",
        },
        "cross_source_difference": {
            "beauty_coefficient_absolute": reconstructed_b - published_b,
            "beauty_coefficient_relative": (
                (reconstructed_b - published_b) / published_b
                if published_b
                else None
            ),
            "awakening_year": (
                reconstructed_awakening_year - published_awakening_year
            ),
        },
        "interpretation": (
            "Differences from Ke et al. are expected because OpenAlex and "
            "Web of Science have different citation coverage. This probe "
            "tests cross-source robustness and data plumbing, not exact "
            "numerical equality across bibliographic databases."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--publication-year", required=True, type=int)
    parser.add_argument("--published-b", required=True, type=float)
    parser.add_argument("--published-awakening-year", required=True, type=int)
    parser.add_argument("--observation-end-year", type=int, default=2011)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_case(
        doi=args.doi,
        case_id=args.case_id,
        publication_year=args.publication_year,
        published_b=args.published_b,
        published_awakening_year=args.published_awakening_year,
        observation_end_year=args.observation_end_year,
        api_key=args.api_key,
    )
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
