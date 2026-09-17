#!/usr/bin/env python3
"""Summarize a classified Retraction Watch CSV without redistributing raw data.

Outputs both event-row counts and unique-original-DOI counts. This distinction is
critical because one original work can have several notices/events.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

FLAG_COLUMNS = [
    "e1s_narrow_auto",
    "e1m_strong_auto",
    "e1p_strong_auto",
    "paper_mill_signal",
    "e3_error_signal",
    "manual_scientific_review",
    "manual_process_review",
    "context_only_reasons",
    "manual_review_required",
]

DATE_FORMATS = (
    "%m/%d/%Y %H:%M",
    "%m/%d/%Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_doi(raw: str | None) -> str | None:
    if not raw:
        return None
    value = raw.strip().lower()
    if not value or value in {"unavailable", "0", "none", "nan"}:
        return None
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix) :]
    return value.strip() or None


def split_reasons(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [x.strip() for x in raw.split(";") if x.strip()]


def parse_rw_date(raw: str | None) -> dt.datetime | None:
    if not raw:
        return None
    value = raw.strip()
    if not value:
        return None
    for fmt in DATE_FORMATS:
        try:
            return dt.datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def summarize(path: Path) -> dict[str, Any]:
    nature_row_counts: collections.Counter[str] = collections.Counter()
    reason_row_counts: collections.Counter[str] = collections.Counter()
    flag_row_counts: collections.Counter[str] = collections.Counter()

    nature_dois: dict[str, set[str]] = collections.defaultdict(set)
    reason_dois: dict[str, set[str]] = collections.defaultdict(set)
    flag_dois: dict[str, set[str]] = collections.defaultdict(set)

    original_dois: set[str] = set()
    duplicate_doi_rows = 0
    missing_doi_rows = 0
    total = 0
    fields: list[str] = []
    parsed_dates: list[dt.datetime] = []
    unparsed_date_rows = 0

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        for row in reader:
            total += 1
            nature = (row.get("RetractionNature") or "UNKNOWN").strip() or "UNKNOWN"
            nature_row_counts[nature] += 1

            reasons = split_reasons(row.get("Reason"))
            for reason in reasons:
                reason_row_counts[reason] += 1

            active_flags: list[str] = []
            for flag in FLAG_COLUMNS:
                try:
                    active = int(row.get(flag) or 0)
                except ValueError:
                    active = 0
                if active:
                    flag_row_counts[flag] += 1
                    active_flags.append(flag)

            doi = norm_doi(row.get("OriginalPaperDOI"))
            if doi is None:
                missing_doi_rows += 1
            else:
                if doi in original_dois:
                    duplicate_doi_rows += 1
                original_dois.add(doi)
                nature_dois[nature].add(doi)
                for reason in reasons:
                    reason_dois[reason].add(doi)
                for flag in active_flags:
                    flag_dois[flag].add(doi)

            raw_date = (row.get("RetractionDate") or "").strip()
            if raw_date:
                parsed = parse_rw_date(raw_date)
                if parsed is None:
                    unparsed_date_rows += 1
                else:
                    parsed_dates.append(parsed)

    return {
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "classification": "DETECTED_CORRECTION_SNAPSHOT_SUMMARY_NOT_PREVALENCE",
        "source_file_sha256": sha256_file(path),
        "rows": total,
        "columns": fields,
        "unique_original_paper_dois": len(original_dois),
        "rows_without_resolvable_original_doi": missing_doi_rows,
        "duplicate_original_doi_rows_after_normalization": duplicate_doi_rows,
        "event_row_counts_by_nature": dict(nature_row_counts.most_common()),
        "unique_original_doi_counts_by_nature": {
            nature: len(dois)
            for nature, dois in sorted(
                nature_dois.items(), key=lambda item: (-len(item[1]), item[0])
            )
        },
        "auto_flag_event_row_counts": {
            flag: int(flag_row_counts[flag]) for flag in FLAG_COLUMNS
        },
        "auto_flag_unique_original_doi_counts": {
            flag: len(flag_dois[flag]) for flag in FLAG_COLUMNS
        },
        "top_reasons_by_event_rows": [
            {
                "reason": reason,
                "event_rows": count,
                "unique_original_dois": len(reason_dois[reason]),
            }
            for reason, count in reason_row_counts.most_common(40)
        ],
        "parsed_retraction_date_rows": len(parsed_dates),
        "unparsed_retraction_date_rows": unparsed_date_rows,
        "retraction_date_min": (
            min(parsed_dates).date().isoformat() if parsed_dates else None
        ),
        "retraction_date_max": (
            max(parsed_dates).date().isoformat() if parsed_dates else None
        ),
        "warning": (
            "Counts describe Retraction Watch/Crossref detected correction records. "
            "They are not estimates of underlying misconduct prevalence. Event-row "
            "counts must not be substituted for unique-work counts. Auto flags are "
            "screening variables and ambiguous records require adjudication."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("classified_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    result = summarize(args.classified_csv)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {args.output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
