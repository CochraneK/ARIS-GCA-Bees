#!/usr/bin/env python3
"""Validate ARIS4C004 person -> OpenAlex identity decisions."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

ALLOWED = {
    "VERIFIED_SINGLE",
    "VERIFIED_CLUSTER",
    "PROVISIONAL_SINGLE",
    "PROVISIONAL_CLUSTER",
    "AMBIGUOUS_COLLISION",
    "NO_GRAPH_RECORD",
    "EXCLUDED_IDENTITY_ERROR",
}
VERIFY_STATES = {"VERIFIED_SINGLE", "VERIFIED_CLUSTER"}
REQUIRED_COLUMNS = {
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
    "adjudication_status",
    "mh_blinded_at_identity_lock",
}


def truthy(value: str) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def parse_int(value: str) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def split_ids(value: str) -> list[str]:
    ids = [x.strip() for x in (value or "").split(";") if x.strip()]
    return ids


def has_bibliographic_support(row: dict[str, str]) -> bool:
    signals = 0
    if (parse_int(row.get("known_work_match_n", "")) or 0) > 0:
        signals += 1
    for field in ("institution_match", "coauthor_match", "topic_field_match", "career_timing_match"):
        if truthy(row.get(field, "")):
            signals += 1
    return signals >= 2


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    seen_people: set[str] = set()

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - headers)
        if missing:
            return [f"missing required columns: {', '.join(missing)}"]

        for lineno, row in enumerate(reader, start=2):
            pid = (row.get("person_id") or "").strip()
            name = (row.get("canonical_name") or "").strip() or "<unnamed>"
            prefix = f"line {lineno} ({pid or name})"
            status = (row.get("identity_status") or "").strip()

            if not pid:
                errors.append(f"{prefix}: person_id is required")
            elif pid in seen_people:
                errors.append(f"{prefix}: duplicate person_id")
            else:
                seen_people.add(pid)

            if status not in ALLOWED:
                errors.append(f"{prefix}: invalid identity_status={status!r}")
                continue

            death = parse_int(row.get("death_year", ""))
            if death is None:
                errors.append(f"{prefix}: death_year missing; primary analytic frame is deceased-only")
            elif death > date.today().year:
                errors.append(f"{prefix}: death_year is in the future")

            ids = split_ids(row.get("verified_openalex_ids", ""))
            if len(ids) != len(set(ids)):
                errors.append(f"{prefix}: duplicate OpenAlex ID inside verified_openalex_ids")

            if status == "VERIFIED_SINGLE" and len(ids) != 1:
                errors.append(f"{prefix}: VERIFIED_SINGLE requires exactly 1 OpenAlex ID")
            if status == "VERIFIED_CLUSTER" and len(ids) < 2:
                errors.append(f"{prefix}: VERIFIED_CLUSTER requires at least 2 OpenAlex IDs")
            if status in VERIFY_STATES and not ids:
                errors.append(f"{prefix}: verified identity requires OpenAlex ID provenance")

            if status in VERIFY_STATES:
                if not (row.get("reviewer") or "").strip():
                    errors.append(f"{prefix}: verified identity requires reviewer")
                if not (row.get("adjudication_status") or "").strip():
                    errors.append(f"{prefix}: verified identity requires adjudication_status")
                if not (row.get("mh_blinded_at_identity_lock") or "").strip():
                    errors.append(f"{prefix}: verified identity requires MH blinding field")

                strong_id = bool((row.get("strong_identifier_evidence") or "").strip())
                if not strong_id and not has_bibliographic_support(row):
                    errors.append(
                        f"{prefix}: verified identity requires strong identifier evidence or >=2 bibliographic support signals"
                    )

            if status == "VERIFIED_CLUSTER" and truthy(row.get("conflicting_orcid", "")):
                errors.append(f"{prefix}: VERIFIED_CLUSTER cannot retain conflicting_orcid=true")

            observable = truthy(row.get("network_observable", ""))
            if observable and status not in VERIFY_STATES:
                errors.append(
                    f"{prefix}: network_observable=true is confirmatory-only and requires a verified identity state"
                )

            completeness = (row.get("cluster_completeness") or "").strip().lower()
            if status == "VERIFIED_CLUSTER" and completeness not in {"high", "moderate", "low"}:
                errors.append(f"{prefix}: VERIFIED_CLUSTER requires cluster_completeness high/moderate/low")
            if status == "VERIFIED_SINGLE" and completeness not in {"", "not_applicable", "na"}:
                errors.append(f"{prefix}: VERIFIED_SINGLE should not carry cluster completeness")

    return errors


def validate_against_candidate_frame(decision_path: Path, candidate_path: Path) -> list[str]:
    """Check that identity decisions refer to the canonical frozen candidate rows."""
    errors: list[str] = []
    with candidate_path.open("r", encoding="utf-8-sig", newline="") as handle:
        candidates = {row["person_id"]: row for row in csv.DictReader(handle)}

    with decision_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for lineno, row in enumerate(csv.DictReader(handle), start=2):
            pid = (row.get("person_id") or "").strip()
            candidate = candidates.get(pid)
            prefix = f"line {lineno} ({pid or row.get('canonical_name') or '<unnamed>'})"
            if candidate is None:
                errors.append(f"{prefix}: person_id is not present in canonical candidate frame")
                continue
            checks = (
                ("canonical_name", str(candidate.get("canonical_name") or "").strip(), str(row.get("canonical_name") or "").strip()),
                ("birth_year", str(candidate.get("birth_year") or "").strip(), str(row.get("birth_year") or "").strip()),
                ("death_year", str(candidate.get("death_year") or "").strip(), str(row.get("death_year") or "").strip()),
            )
            for field, expected, observed in checks:
                if expected != observed:
                    errors.append(
                        f"{prefix}: {field} mismatch vs canonical candidate frame "
                        f"(expected={expected!r}, observed={observed!r})"
                    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--candidate-frame", type=Path)
    args = parser.parse_args()
    errors = validate(args.csv_path)
    if args.candidate_frame:
        errors.extend(validate_against_candidate_frame(args.csv_path, args.candidate_frame))
    if errors:
        print(f"FAIL: {len(errors)} identity validation error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    suffix = (
        f" and matches canonical frame {args.candidate_frame}"
        if args.candidate_frame
        else ""
    )
    print(f"PASS: {args.csv_path} satisfies ARIS4C004 identity-decision invariants{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
