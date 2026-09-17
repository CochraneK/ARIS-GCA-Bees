#!/usr/bin/env python3
"""Validate ARIS4C004 historical mental-health evidence coding tables.

This validator enforces a small set of non-negotiable pre-analysis rules from
process/EXPOSURE_CODEBOOK.md. It intentionally does not decide whether a
historical diagnosis is true; it checks whether coded claims have the required
provenance and whether forbidden shortcuts have slipped into the table.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

ALLOWED_CLASSES = {"A1", "A2", "B1", "B2", "C", "U"}
CLINICAL_SOURCE_CLASSES = {"primary_clinical"}
STRONG_B_SOURCE_CLASSES = {
    "primary_nonclinical",
    "scholarly_history",
    "authoritative_biography",
}
REQUIRED_COLUMNS = {
    "person_id",
    "canonical_name",
    "birth_year",
    "death_year",
    "domain",
    "mh_evidence_class",
    "source_class_best",
    "source_primary_identifier",
    "search_status",
    "outcome_blinded_at_lock",
}


def parse_year(value: str) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def truthy(value: str) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()

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

            if not pid:
                errors.append(f"{prefix}: person_id is required")
            elif pid in seen_ids:
                errors.append(f"{prefix}: duplicate person_id")
            else:
                seen_ids.add(pid)

            cls = (row.get("mh_evidence_class") or "").strip()
            if cls not in ALLOWED_CLASSES:
                errors.append(f"{prefix}: invalid mh_evidence_class={cls!r}")
                continue

            birth = parse_year(row.get("birth_year", ""))
            death = parse_year(row.get("death_year", ""))
            if death is None:
                errors.append(f"{prefix}: death_year missing; primary dataset is deceased-only")
            elif death > date.today().year:
                errors.append(f"{prefix}: death_year is in the future")
            if birth is not None and death is not None and birth > death:
                errors.append(f"{prefix}: birth_year exceeds death_year")

            source_class = (row.get("source_class_best") or "").strip()
            source_id = (row.get("source_primary_identifier") or "").strip()

            if cls in {"A1", "A2"}:
                if source_class not in CLINICAL_SOURCE_CLASSES:
                    errors.append(
                        f"{prefix}: {cls} requires source_class_best=primary_clinical"
                    )
                if not source_id:
                    errors.append(f"{prefix}: {cls} requires source provenance")

            if cls in {"B1", "B2"}:
                if source_class not in STRONG_B_SOURCE_CLASSES:
                    errors.append(
                        f"{prefix}: {cls} requires primary_nonclinical, scholarly_history, "
                        "or authoritative_biography as best source"
                    )
                if not source_id:
                    errors.append(f"{prefix}: {cls} requires source provenance")

            # Explicitly reject shortcuts sometimes introduced in ad-hoc spreadsheets.
            for forbidden in ("healthy", "control_negative", "no_disorder"):
                if forbidden in headers and truthy(row.get(forbidden, "")) and cls == "U":
                    errors.append(
                        f"{prefix}: Unknown evidence cannot be coded as {forbidden}=true"
                    )

            historical_term = (row.get("historical_term_normalized") or "").strip()
            modern_mapping = (row.get("modern_mapping_family") or "").strip()
            if modern_mapping and cls == "U" and not historical_term:
                errors.append(
                    f"{prefix}: modern mapping present despite unknown evidence and no historical term"
                )

            first_year = parse_year(row.get("first_evidence_year", ""))
            last_year = parse_year(row.get("last_evidence_year", ""))
            if birth is not None and first_year is not None and first_year < birth:
                errors.append(f"{prefix}: first_evidence_year predates birth")
            if death is not None and first_year is not None and first_year > death:
                errors.append(f"{prefix}: first_evidence_year postdates death")
            if first_year is not None and last_year is not None and first_year > last_year:
                errors.append(f"{prefix}: first_evidence_year exceeds last_evidence_year")

            search_status = (row.get("search_status") or "").strip()
            if search_status not in {"not_started", "basic", "expanded", "adjudicated"}:
                errors.append(f"{prefix}: invalid search_status={search_status!r}")

            if cls in {"A1", "A2", "B1", "B2"} and search_status == "not_started":
                errors.append(f"{prefix}: affirmative A/B code cannot have search_status=not_started")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    errors = validate(args.csv_path)
    if errors:
        print(f"FAIL: {len(errors)} validation error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"PASS: {args.csv_path} satisfies ARIS4C004 exposure-table invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
