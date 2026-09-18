#!/usr/bin/env python3
"""Create/refresh a canonical 100-person identity-decision draft for ARIS4C004.

The frozen candidate frame is the source of identity metadata. Existing reviewed
rows (e.g. pilot30) are copied by person_id after exact metadata checks. New rows
are initialized from the current OpenAlex review class without using mental-health
information.

This prevents manual QID/name transcription drift during scale-up.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

FIELDS = [
    "person_id",
    "canonical_name",
    "birth_year",
    "death_year",
    "identity_status",
    "verified_openalex_ids",
    "cluster_completeness",
    "network_observable",
    "strong_identifier_evidence",
    "known_work_match_n",
    "institution_match",
    "coauthor_match",
    "topic_field_match",
    "career_timing_match",
    "conflicting_orcid",
    "reviewer",
    "second_reviewer",
    "adjudication_status",
    "mh_blinded_at_identity_lock",
    "review_date",
    "notes",
]

CLASS_TO_STATUS = {
    "possible_author_fragmentation": "PROVISIONAL_CLUSTER",
    "single_plausible_author_record": "PROVISIONAL_SINGLE",
    "single_low_confidence_record": "PROVISIONAL_SINGLE",
    "no_openalex_search_hit": "NO_GRAPH_RECORD",
    "name_collision_or_low_similarity": "AMBIGUOUS_COLLISION",
    "possible_name_collision_conflicting_orcid": "AMBIGUOUS_COLLISION",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def blank_row(candidate: dict[str, str], queue: dict[str, str] | None) -> dict[str, str]:
    review_class = (queue or {}).get("review_class", "no_openalex_search_hit")
    status = CLASS_TO_STATUS.get(review_class, "PROVISIONAL_SINGLE")
    final_triage = status in {"NO_GRAPH_RECORD", "AMBIGUOUS_COLLISION"}
    plausible = (queue or {}).get("plausible_openalex_ids", "")
    return {
        "person_id": candidate["person_id"],
        "canonical_name": candidate["canonical_name"],
        "birth_year": candidate["birth_year"],
        "death_year": candidate["death_year"],
        "identity_status": status,
        "verified_openalex_ids": "",
        "cluster_completeness": "",
        "network_observable": "false",
        "strong_identifier_evidence": "",
        "known_work_match_n": "0",
        "institution_match": "false",
        "coauthor_match": "false",
        "topic_field_match": "false",
        "career_timing_match": "false",
        "conflicting_orcid": "false",
        "reviewer": "ARIS4C automated pre-exposure triage" if final_triage else "",
        "second_reviewer": "",
        "adjudication_status": "protocol-derived" if final_triage else "pending",
        "mh_blinded_at_identity_lock": "true" if final_triage else "",
        "review_date": "",
        "notes": (
            f"MH-blind identity100 initialization; review_class={review_class}; "
            f"plausible_openalex_ids={plausible}"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--existing-decisions", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    args = parser.parse_args()

    candidates = read_csv(args.candidates)
    queue_rows = read_csv(args.queue)
    queue = {row["person_id"]: row for row in queue_rows}

    existing: dict[str, dict[str, str]] = {}
    if args.existing_decisions and args.existing_decisions.exists():
        for row in read_csv(args.existing_decisions):
            existing[row["person_id"]] = row

    output: list[dict[str, str]] = []
    reused_n = 0
    for candidate in candidates:
        pid = candidate["person_id"]
        if pid in existing:
            row = existing[pid]
            for field in ("canonical_name", "birth_year", "death_year"):
                if (row.get(field) or "").strip() != (candidate.get(field) or "").strip():
                    raise SystemExit(
                        f"existing decision metadata mismatch for {pid}: {field} "
                        f"{row.get(field)!r} != {candidate.get(field)!r}"
                    )
            output.append({field: row.get(field, "") for field in FIELDS})
            reused_n += 1
        else:
            output.append(blank_row(candidate, queue.get(pid)))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output)

    counts = Counter(row["identity_status"] for row in output)
    summary = {
        "candidate_n": len(candidates),
        "existing_reviewed_rows_reused_n": reused_n,
        "new_rows_initialized_n": len(candidates) - reused_n,
        "status_counts": dict(counts),
        "network_observable_n": sum((row.get("network_observable") or "").lower() == "true" for row in output),
        "mental_health_information_used": False,
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
