"""Resumable citation-history reconstruction for Pilot-M complete frames.

Input is the metadata-only inventory produced by pilotM_full_frame_inventory.py.
Successful papers are appended one JSON object per line to a checkpoint file.
Re-running with the same checkpoint skips completed OpenAlex IDs, so API-rate
interruptions do not discard prior work.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from openalex_adapter import OpenAlexWork, reconstruct_history_for_known_work


def _load_completed(path: Path) -> set[str]:
    if not path.exists():
        return set()
    completed = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        row = json.loads(raw)
        paper_id = row.get("paper_id")
        if paper_id:
            completed.add(str(paper_id))
    return completed


def _metadata_work(row: dict[str, Any]) -> OpenAlexWork:
    return OpenAlexWork(
        openalex_id=str(row["openalex_id"]),
        title=row.get("title"),
        publication_year=(
            int(row["publication_year"])
            if row.get("publication_year") is not None
            else None
        ),
        doi=row.get("doi"),
        cited_by_count=row.get("cited_by_count"),
        primary_topic=row.get("primary_topic"),
        primary_field_id=(
            str(row["primary_field_id"])
            if row.get("primary_field_id") is not None
            else None
        ),
        referenced_works_count=row.get("reference_count"),
        authorship_count=row.get("author_count"),
    )


def reconstruct_inventory(
    inventory: dict[str, Any],
    *,
    checkpoint_path: Path,
    observation_end_year: int = 2011,
    api_key: str | None = None,
    max_new_records: int | None = None,
    only_case_id: str | None = None,
) -> dict[str, Any]:
    if max_new_records is not None and max_new_records < 1:
        raise ValueError("max_new_records must be >= 1 when provided")

    completed = _load_completed(checkpoint_path)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

    frames = sorted(
        inventory.get("frames", []),
        key=lambda x: str(x.get("case_id", "")),
    )
    if only_case_id is not None:
        frames = [
            frame
            for frame in frames
            if str(frame.get("case_id")) == only_case_id
        ]
        if not frames:
            raise ValueError(f"unknown case_id: {only_case_id}")

    new_count = 0
    skipped_count = 0
    with checkpoint_path.open("a", encoding="utf-8") as handle:
        for frame in frames:
            frame_case_id = str(frame["case_id"])
            year = int(frame["publication_year"])
            field_id = str(frame["primary_field_id"])
            works = sorted(
                frame.get("works", []),
                key=lambda x: str(x.get("openalex_id", "")),
            )
            for metadata in works:
                paper_id = str(metadata["openalex_id"])
                if paper_id in completed:
                    skipped_count += 1
                    continue
                if (
                    max_new_records is not None
                    and new_count >= max_new_records
                ):
                    return {
                        "status": "bounded_batch_complete",
                        "new_records": new_count,
                        "skipped_completed": skipped_count,
                        "checkpoint_records": len(completed) + new_count,
                    }

                work = _metadata_work(metadata)
                history = reconstruct_history_for_known_work(
                    work,
                    publication_year=year,
                    end_year=observation_end_year,
                    api_key=api_key,
                    max_records=None,
                )
                out = {
                    "frame_case_id": frame_case_id,
                    "paper_id": paper_id,
                    "publication_year": year,
                    "primary_field_id": field_id,
                    "title": metadata.get("title"),
                    "doi": metadata.get("doi"),
                    "reference_count": metadata.get("reference_count"),
                    "author_count": metadata.get("author_count"),
                    "observation_end_year": observation_end_year,
                    "annual_citation_counts": list(history.counts),
                    "citations_through_endpoint": history.total_citations,
                    "valid_citation_edges": history.valid_edges,
                }
                handle.write(json.dumps(out, ensure_ascii=False) + "\n")
                handle.flush()
                completed.add(paper_id)
                new_count += 1

    return {
        "status": "complete",
        "new_records": new_count,
        "skipped_completed": skipped_count,
        "checkpoint_records": len(completed),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--observation-end-year", type=int, default=2011)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--max-new-records", type=int, default=None)
    parser.add_argument("--only-case-id", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    result = reconstruct_inventory(
        inventory,
        checkpoint_path=args.checkpoint,
        observation_end_year=args.observation_end_year,
        api_key=args.api_key,
        max_new_records=args.max_new_records,
        only_case_id=args.only_case_id,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
