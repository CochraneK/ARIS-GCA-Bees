#!/usr/bin/env python3
"""Summarize a classified Retraction Watch CSV without redistributing raw data."""

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
    "context_only_reasons",
    "manual_review_required",
]


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


def summarize(path: Path) -> dict[str, Any]:
    nature_counts: collections.Counter[str] = collections.Counter()
    reason_counts: collections.Counter[str] = collections.Counter()
    flag_counts: collections.Counter[str] = collections.Counter()
    original_dois: set[str] = set()
    duplicate_doi_rows = 0
    missing_doi_rows = 0
    total = 0
    fields: list[str] = []
    date_values: list[str] = []

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        for row in reader:
            total += 1
            nature_counts[(row.get("RetractionNature") or "UNKNOWN").strip()] += 1
            for reason in split_reasons(row.get("Reason")):
                reason_counts[reason] += 1
            for flag in FLAG_COLUMNS:
                try:
                    flag_counts[flag] += int(row.get(flag) or 0)
                except ValueError:
                    pass

            doi = norm_doi(row.get("OriginalPaperDOI"))
            if doi is None:
                missing_doi_rows += 1
            elif doi in original_dois:
                duplicate_doi_rows += 1
            else:
                original_dois.add(doi)

            date = (row.get("RetractionDate") or "").strip()
            if date:
                date_values.append(date)

    return {
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "classification": "DETECTED_CORRECTION_SNAPSHOT_SUMMARY_NOT_PREVALENCE",
        "source_file_sha256": sha256_file(path),
        "rows": total,
        "columns": fields,
        "unique_original_paper_dois": len(original_dois),
        "rows_without_resolvable_original_doi": missing_doi_rows,
        "duplicate_original_doi_rows_after_normalization": duplicate_doi_rows,
        "retraction_nature_counts": dict(nature_counts.most_common()),
        "auto_flag_counts": {flag: int(flag_counts[flag]) for flag in FLAG_COLUMNS},
        "top_reasons": [
            {"reason": reason, "count": count}
            for reason, count in reason_counts.most_common(30)
        ],
        "raw_retraction_date_min_lexical": min(date_values) if date_values else None,
        "raw_retraction_date_max_lexical": max(date_values) if date_values else None,
        "warning": (
            "Counts describe Retraction Watch/Crossref detected correction records. "
            "They are not estimates of underlying misconduct prevalence. Auto flags "
            "are screening variables and ambiguous records require adjudication."
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
