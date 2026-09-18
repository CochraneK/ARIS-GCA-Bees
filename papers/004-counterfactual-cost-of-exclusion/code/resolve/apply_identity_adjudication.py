#!/usr/bin/env python3
"""Apply MH-blind first-review adjudications to the ARIS4C004 identity100 draft.

Only rows explicitly listed in the override table may change. The override table
stores evidence decisions for candidates that remained PROVISIONAL after the
automated identity100 triage. Existing pilot30 reviewed rows and protocol-derived
NO_GRAPH/COLLISION rows are preserved.

The output is eligible to become the canonical first-review identity100 table
only when zero PROVISIONAL states remain.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

PROVISIONAL = {"PROVISIONAL_SINGLE", "PROVISIONAL_CLUSTER"}
FINAL_ALLOWED = {
    "VERIFIED_SINGLE",
    "VERIFIED_CLUSTER",
    "AMBIGUOUS_COLLISION",
    "NO_GRAPH_RECORD",
    "EXCLUDED_IDENTITY_ERROR",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def truthy(value: str) -> str:
    return "true" if (value or "").strip().lower() in {"1", "true", "yes", "y"} else "false"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--overrides", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--review-date", default="2026-09-18")
    args = parser.parse_args()

    rows = read_csv(args.draft)
    overrides = read_csv(args.overrides)
    by_pid = {row["person_id"]: row for row in rows}
    if len(by_pid) != len(rows):
        raise SystemExit("draft contains duplicate person_id")

    seen: set[str] = set()
    for override in overrides:
        pid = (override.get("person_id") or "").strip()
        if not pid or pid in seen:
            raise SystemExit(f"invalid/duplicate override person_id: {pid!r}")
        seen.add(pid)
        row = by_pid.get(pid)
        if row is None:
            raise SystemExit(f"override person_id absent from draft: {pid}")
        expected_name = (override.get("canonical_name") or "").strip()
        if expected_name and expected_name != (row.get("canonical_name") or "").strip():
            raise SystemExit(
                f"{pid}: override name {expected_name!r} != draft {(row.get('canonical_name') or '')!r}"
            )
        if (row.get("identity_status") or "").strip() not in PROVISIONAL:
            raise SystemExit(
                f"{pid}: overrides may only adjudicate PROVISIONAL rows; "
                f"draft status={row.get('identity_status')!r}"
            )

        status = (override.get("identity_status") or "").strip()
        if status not in FINAL_ALLOWED:
            raise SystemExit(f"{pid}: invalid final identity_status={status!r}")

        ids = (override.get("verified_openalex_ids") or "").strip()
        row["identity_status"] = status
        row["verified_openalex_ids"] = ids
        row["cluster_completeness"] = (override.get("cluster_completeness") or "").strip()
        row["network_observable"] = "false"
        row["strong_identifier_evidence"] = (override.get("strong_identifier_evidence") or "").strip()
        row["known_work_match_n"] = (override.get("known_work_match_n") or "0").strip()
        row["institution_match"] = truthy(override.get("institution_match", "false"))
        row["coauthor_match"] = truthy(override.get("coauthor_match", "false"))
        row["topic_field_match"] = truthy(override.get("topic_field_match", "false"))
        row["career_timing_match"] = truthy(override.get("career_timing_match", "false"))
        row["conflicting_orcid"] = truthy(override.get("conflicting_orcid", "false"))
        row["reviewer"] = "ARIS4C pre-exposure evidence review"
        row["second_reviewer"] = ""
        row["adjudication_status"] = (override.get("adjudication_status") or "").strip()
        row["mh_blinded_at_identity_lock"] = "true"
        row["review_date"] = args.review_date
        row["notes"] = (override.get("notes") or "").strip()

    remaining = [
        row for row in rows
        if (row.get("identity_status") or "").strip() in PROVISIONAL
    ]
    if remaining:
        raise SystemExit(
            "first-review freeze blocked: PROVISIONAL rows remain: "
            + ", ".join(f"{x['person_id']}:{x['canonical_name']}" for x in remaining)
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(row["identity_status"] for row in rows)
    summary = {
        "candidate_n": len(rows),
        "override_rows_n": len(overrides),
        "status_counts": dict(counts),
        "verified_n": counts["VERIFIED_SINGLE"] + counts["VERIFIED_CLUSTER"],
        "network_observable_n": sum(
            (row.get("network_observable") or "").lower() == "true" for row in rows
        ),
        "provisional_n": 0,
        "mental_health_information_used": False,
        "note": "First-review identity freeze only; required independent second review remains pending.",
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
