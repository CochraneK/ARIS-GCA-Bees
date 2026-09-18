"""Build auditable historical-artifact search manifests for ARIS4C011."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List

from wayback_discovery import build_cdx_url


REQUIRED_COLUMNS = {
    "target_doi",
    "event_date",
    "issue_code",
    "object_role",
    "candidate_url",
    "archive_query_pattern",
    "identity_marker",
    "source_kind",
    "equivalence_intent",
    "current_state",
    "note",
}


def build_rows(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    output: List[Dict[str, str]] = []
    for i, row in enumerate(rows):
        missing = REQUIRED_COLUMNS - set(row)
        if missing:
            raise ValueError(f"Candidate row {i} missing columns: {sorted(missing)}")
        if not row["target_doi"].strip():
            raise ValueError(f"Candidate row {i} has no target_doi")
        if not row["event_date"].strip():
            raise ValueError(f"Candidate row {i} has no event_date")
        pattern = row["archive_query_pattern"].strip() or row["candidate_url"].strip()
        if not pattern:
            raise ValueError(f"Candidate row {i} has no URL")

        out = dict(row)
        out["candidate_id"] = f"c{i+1:03d}"
        out["cdx_query_url"] = build_cdx_url(
            pattern,
            event_date=row["event_date"],
        )
        out["qualification_status"] = "DISCOVERY_ONLY"
        output.append(out)
    return output


def load_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: List[Dict[str, str]], path: Path) -> None:
    if not rows:
        raise ValueError("Refusing to write an empty search manifest")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    write_csv(build_rows(load_csv(args.input)), args.output)


if __name__ == "__main__":
    main()
