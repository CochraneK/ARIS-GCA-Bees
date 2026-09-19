"""Inventory the complete exact OpenAlex control frames for Pilot M.

This stage is deliberately metadata-only. It enumerates every article in the
same publication year x current OpenAlex primary field as each frozen
literature-known Sleeping Beauty, persists that bounded frame, and records the
API-reported frame size. Citation-history reconstruction is a separate,
resumable stage so rate limits cannot force the frame definition to change.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from openalex_adapter import count_works, fetch_work, iter_works
from pilotM_known_case_enrichment import KNOWN_CASES


def _work_dict(work) -> dict[str, Any]:
    return {
        "openalex_id": work.openalex_id,
        "title": work.title,
        "publication_year": work.publication_year,
        "doi": work.doi,
        "cited_by_count": work.cited_by_count,
        "primary_topic": work.primary_topic,
        "primary_field_id": work.primary_field_id,
        "reference_count": work.referenced_works_count,
        "author_count": work.authorship_count,
    }


def build_inventory(
    *,
    api_key: str | None = None,
    max_records_per_case: int | None = None,
) -> dict[str, Any]:
    frames = []
    frozen_case_ids = []

    for spec in KNOWN_CASES:
        case_work = fetch_work(
            f"https://doi.org/{spec['doi']}",
            api_key=api_key,
        )
        if not case_work.openalex_id:
            raise ValueError(f"{spec['case_id']} has no OpenAlex ID")
        if case_work.primary_field_id is None:
            raise ValueError(f"{spec['case_id']} has no primary field")

        year = int(spec["publication_year"])
        field_id = str(case_work.primary_field_id)
        filters = (
            f"publication_year:{year},type:article,"
            f"primary_topic.field.id:{field_id}"
        )
        reported_count = count_works(filters=filters, api_key=api_key)
        works = list(
            iter_works(
                filters=filters,
                api_key=api_key,
                max_records=max_records_per_case,
            )
        )
        ids = [w.openalex_id for w in works if w.openalex_id]
        if len(ids) != len(set(ids)):
            raise ValueError(
                f"duplicate OpenAlex IDs in frame for {spec['case_id']}"
            )
        if max_records_per_case is None and len(works) != reported_count:
            raise ValueError(
                "complete-frame enumeration count mismatch for "
                f"{spec['case_id']}: reported={reported_count}, "
                f"enumerated={len(works)}"
            )

        frozen_case_ids.append(case_work.openalex_id)
        frames.append(
            {
                "case_id": spec["case_id"],
                "case_openalex_id": case_work.openalex_id,
                "case_title": case_work.title,
                "case_doi": spec["doi"],
                "publication_year": year,
                "primary_field_id": field_id,
                "filter": filters,
                "api_reported_count": reported_count,
                "enumerated_count": len(works),
                "complete": (
                    max_records_per_case is None
                    and len(works) == reported_count
                ),
                "works": [_work_dict(w) for w in works],
            }
        )

    return {
        "analysis": "Pilot M exact control-frame inventory",
        "claim_boundary": (
            "Metadata-only acquisition. No mechanism inference and no "
            "citation-trajectory matching are performed at this stage."
        ),
        "frame_definition": (
            "exact publication year x current OpenAlex primary field x article"
        ),
        "sampling": "none; cursor-enumerated complete frame",
        "frozen_primary_case_ids": sorted(frozen_case_ids),
        "max_records_per_case": max_records_per_case,
        "frames": frames,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--max-records-per-case", type=int, default=None)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = build_inventory(
        api_key=args.api_key,
        max_records_per_case=args.max_records_per_case,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "frozen_primary_case_ids": result[
                    "frozen_primary_case_ids"
                ],
                "frames": [
                    {
                        "case_id": x["case_id"],
                        "api_reported_count": x["api_reported_count"],
                        "enumerated_count": x["enumerated_count"],
                        "complete": x["complete"],
                    }
                    for x in result["frames"]
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
