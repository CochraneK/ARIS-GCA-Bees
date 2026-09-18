#!/usr/bin/env python3
"""Validate ARIS4C004 work-level adjudication tables."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ALLOWED = {
    "KEEP_ORIGINAL",
    "KEEP_POSTHUMOUS_ORIGINAL",
    "EXCLUDE_NAME_COLLISION",
    "EXCLUDE_CONTAINER_FRAGMENT",
    "EXCLUDE_MODERN_REPRINT",
    "DUPLICATE_MANIFESTATION",
    "EXCLUDE_NON_SCHOLARLY_ARCHIVAL_RECORD",
    "NEEDS_REVIEW",
}
KEEP = {"KEEP_ORIGINAL", "KEEP_POSTHUMOUS_ORIGINAL"}
VERIFIED = {"VERIFIED_SINGLE", "VERIFIED_CLUSTER"}
REQUIRED_COLUMNS = {
    "person_id",
    "canonical_name",
    "openalex_work_id",
    "work_decision",
    "include_in_network",
    "canonical_work_id",
    "decision_evidence",
    "reviewer",
    "adjudication_status",
    "mh_blinded_at_work_lock",
}


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(
    path: Path,
    identity_path: Path | None = None,
    review_queue_path: Path | None = None,
    require_complete_queue: bool = False,
) -> list[str]:
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()

    identities: dict[str, dict[str, str]] = {}
    if identity_path:
        identities = {row["person_id"]: row for row in read_csv(identity_path)}

    queue: dict[tuple[str, str], dict[str, str]] = {}
    if review_queue_path:
        for row in read_csv(review_queue_path):
            key = ((row.get("person_id") or "").strip(), (row.get("openalex_work_id") or "").strip())
            if key in queue:
                errors.append(f"review queue duplicate key: {key[0]} / {key[1]}")
            queue[key] = row

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - headers)
        if missing:
            return [f"missing required columns: {', '.join(missing)}"]

        for lineno, row in enumerate(reader, start=2):
            pid = (row.get("person_id") or "").strip()
            name = (row.get("canonical_name") or "").strip()
            wid = (row.get("openalex_work_id") or "").strip()
            prefix = f"line {lineno} ({pid or name or '<unnamed>'} / {wid or '<no-work-id>'})"

            if row.get(None):
                errors.append(f"{prefix}: malformed CSV row has unexpected extra field(s)")

            if not pid or not wid:
                errors.append(f"{prefix}: person_id and openalex_work_id are required")
                continue

            key = (pid, wid)
            if key in seen:
                errors.append(f"{prefix}: duplicate person/work decision")
            seen.add(key)

            decision = (row.get("work_decision") or "").strip()
            if decision not in ALLOWED:
                errors.append(f"{prefix}: invalid work_decision={decision!r}")
                continue

            include = truthy(row.get("include_in_network"))
            if include != (decision in KEEP):
                errors.append(
                    f"{prefix}: include_in_network must be true exactly for KEEP decisions"
                )

            canonical = (row.get("canonical_work_id") or "").strip()
            if include and not canonical:
                errors.append(f"{prefix}: retained work requires canonical_work_id")
            if include and canonical != wid:
                errors.append(
                    f"{prefix}: pilot retained canonical_work_id must equal openalex_work_id"
                )

            if not (row.get("decision_evidence") or "").strip():
                errors.append(f"{prefix}: decision_evidence is required")
            if not (row.get("reviewer") or "").strip():
                errors.append(f"{prefix}: reviewer is required")
            if not (row.get("adjudication_status") or "").strip():
                errors.append(f"{prefix}: adjudication_status is required")
            if not truthy(row.get("mh_blinded_at_work_lock")):
                errors.append(f"{prefix}: work adjudication must be MH-blinded")

            if decision == "NEEDS_REVIEW" and include:
                errors.append(f"{prefix}: NEEDS_REVIEW cannot enter network")

            if identity_path:
                identity = identities.get(pid)
                if not identity:
                    errors.append(f"{prefix}: person_id missing from identity decision table")
                else:
                    if identity.get("identity_status") not in VERIFIED:
                        errors.append(
                            f"{prefix}: work review is only valid for VERIFIED identities"
                        )
                    if (identity.get("canonical_name") or "").strip() != name:
                        errors.append(f"{prefix}: canonical_name mismatch vs identity table")

            if review_queue_path:
                q = queue.get(key)
                if not q:
                    errors.append(f"{prefix}: decision key not present in regenerated review queue")
                elif (q.get("canonical_name") or "").strip() != name:
                    errors.append(f"{prefix}: canonical_name mismatch vs review queue")

    if require_complete_queue and review_queue_path:
        missing_decisions = sorted(set(queue) - seen)
        extra_decisions = sorted(seen - set(queue))
        for pid, wid in missing_decisions:
            errors.append(f"missing decision for review-queue work: {pid} / {wid}")
        for pid, wid in extra_decisions:
            errors.append(f"decision not present in review queue: {pid} / {wid}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--identity-decisions", type=Path)
    parser.add_argument("--review-queue", type=Path)
    parser.add_argument("--require-complete-queue", action="store_true")
    args = parser.parse_args()

    if args.require_complete_queue and not args.review_queue:
        parser.error("--require-complete-queue requires --review-queue")

    errors = validate(
        args.csv_path,
        identity_path=args.identity_decisions,
        review_queue_path=args.review_queue,
        require_complete_queue=args.require_complete_queue,
    )
    if errors:
        print(f"FAIL: {len(errors)} work-decision validation error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.csv_path} satisfies ARIS4C004 work-decision invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
