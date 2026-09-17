#!/usr/bin/env python3
"""Build lifetime-aware review profiles for accepted top OpenAlex records.

These profiles support human identity review for candidates that may have a
single plausible record. They are not identity verification. Fragmentation cases
are separately profiled by `openalex_cluster_evidence.py` and can be merged with
this output for a unified review packet.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from openalex_cluster_evidence import AuthorEvidence, career_window, contamination_summary


def parse_year(value: Any) -> int | None:
    try:
        year = int(float(value))
    except (TypeError, ValueError):
        return None
    return year if 1000 <= year <= 2200 else None


def read_candidates(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["person_id"]: row for row in csv.DictReader(handle)}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--authors", type=Path, required=True)
    parser.add_argument("--works", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    args = parser.parse_args()

    candidates = read_candidates(args.candidates)
    author_rows = read_jsonl(args.authors)
    work_rows = read_jsonl(args.works)

    works_by_person: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in work_rows:
        pid = str(row.get("person_id") or "")
        work = row.get("work") or {}
        if pid and work:
            works_by_person[pid].append(work)

    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with args.output_jsonl.open("w", encoding="utf-8") as handle:
        for row in author_rows:
            pid = str(row.get("person_id") or "")
            candidate = candidates.get(pid, {})
            author = row.get("author") or {}
            author_id = str(author.get("id") or "").rstrip("/").split("/")[-1]
            birth = parse_year(candidate.get("birth_year"))
            death = parse_year(candidate.get("death_year"))
            lo, hi = career_window(birth, death)
            evidence = AuthorEvidence(author_id, author, works_by_person.get(pid, []))
            plausible = evidence.works_in_window(lo, hi)
            outside = evidence.works_outside_window(lo, hi)
            contamination = contamination_summary(evidence, birth, death, lo, hi)
            profile = {
                "person_id": pid,
                "canonical_name": candidate.get("canonical_name") or row.get("canonical_name") or "",
                "wikidata_qid": candidate.get("wikidata_qid", ""),
                "birth_year": birth,
                "death_year": death,
                "plausible_career_year_min": lo,
                "plausible_career_year_max": hi,
                "author_id": author_id,
                "display_name": author.get("display_name"),
                "orcid": author.get("orcid") or "",
                "resolution_method": row.get("resolution_method"),
                "resolution_score": row.get("resolution_score"),
                "resolution_margin": row.get("resolution_margin"),
                "profile_source": "accepted_top_record",
                "contamination": contamination,
                "plausible_coauthors_n": len(evidence.coauthors(plausible)),
                "plausible_institutions_n": len(evidence.institutions(plausible)),
                "plausible_topics_n": len(evidence.topics(plausible)),
                "representative_plausible_works": evidence.representative_works(plausible),
                "representative_outside_window_works": evidence.representative_works(outside),
            }
            handle.write(json.dumps(profile, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
