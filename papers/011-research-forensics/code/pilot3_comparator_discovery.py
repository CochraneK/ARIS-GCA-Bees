#!/usr/bin/env python3
"""Discover matched no-known-integrity-concern comparator candidates.

Development-stage only. This script does NOT prove that a paper is error-free
or integrity-concern-free. It finds same-journal / near-date candidates that
Crossref currently reports as having no registered update, excludes every DOI
already present in the ARIS4C011 issue/correction development registry, and
writes an auditable provisional candidate set for secondary negative screening.

Detector outputs are never used for matching.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PILOT3 = ROOT / "data" / "pilot" / "pilot3_correction_candidates.csv"

PLOS_ONE_ISSN = "1932-6203"
USER_AGENT = "ARIS4C011-comparator-discovery/0.1 (https://github.com/CochraneK/ARIS4C)"

TARGETS = [
    {
        "target_id": "p2b-plos-morality",
        "target_doi": "10.1371/journal.pone.0258910",
        "published": "2021-10-22",
    },
    {
        "target_id": "p3-music-country-table",
        "target_doi": "10.1371/journal.pone.0293412",
        "published": "2023-10-26",
    },
    {
        "target_id": "p3-toxo-missing-columns",
        "target_doi": "10.1371/journal.pone.0180906",
        "published": "2017-07-21",
    },
    {
        "target_id": "p3-adaptive-pvalues",
        "target_doi": "10.1371/journal.pone.0180395",
        "published": "2017-08-01",
    },
]

STATUS_MARKER = re.compile(
    r"\b(retracted?|withdrawn?|correction|corrigendum|erratum|"
    r"expression\s+of\s+concern)\b",
    re.I,
)


def normalize_doi(value: str) -> str:
    x = (value or "").strip().lower()
    x = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", x)
    x = re.sub(r"^doi:\s*", "", x)
    return x.strip()


def first_text(value: Any) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value or "")


def crossref_date(item: dict[str, Any]) -> str:
    for key in ("published-online", "published-print", "published", "issued"):
        parts = ((item.get(key) or {}).get("date-parts") or [])
        if not parts or not parts[0]:
            continue
        p = list(parts[0])
        y = int(p[0])
        m = int(p[1]) if len(p) > 1 else 1
        d = int(p[2]) if len(p) > 2 else 1
        return f"{y:04d}-{m:02d}-{d:02d}"
    return ""


def get_json(url: str, *, attempts: int = 4) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.load(response)
        except Exception as exc:
            last = exc
            if attempt + 1 >= attempts:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(last)


def known_registry_dois(path: Path = PILOT3) -> set[str]:
    out: set[str] = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            for key in ("target_doi", "correction_doi"):
                doi = normalize_doi(row.get(key, ""))
                if doi:
                    out.add(doi)
    return out


def query_window(
    published: str,
    *,
    window_days: int,
    rows: int,
) -> list[dict[str, Any]]:
    center = dt.date.fromisoformat(published)
    lo = center - dt.timedelta(days=window_days)
    hi = center + dt.timedelta(days=window_days)
    params = {
        "filter": ",".join(
            [
                f"from-pub-date:{lo.isoformat()}",
                f"until-pub-date:{hi.isoformat()}",
                "type:journal-article",
                "has-update:0",
            ]
        ),
        "rows": str(rows),
    }
    url = (
        f"https://api.crossref.org/journals/{PLOS_ONE_ISSN}/works?"
        + urllib.parse.urlencode(params)
    )
    payload = get_json(url)
    return ((payload.get("message") or {}).get("items") or [])


def score_candidate(
    item: dict[str, Any],
    *,
    target_date: dt.date,
    excluded: set[str],
) -> dict[str, Any] | None:
    doi = normalize_doi(item.get("DOI", ""))
    title = first_text(item.get("title")).strip()
    pub = crossref_date(item)
    if not doi or not title or not pub or doi in excluded:
        return None
    if STATUS_MARKER.search(title):
        return None
    if item.get("type") != "journal-article":
        return None

    pub_date = dt.date.fromisoformat(pub)
    return {
        "candidate_doi": doi,
        "candidate_title": title,
        "candidate_published": pub,
        "date_distance_days": abs((pub_date - target_date).days),
        "crossref_type": str(item.get("type") or ""),
        "reference_count": item.get("reference-count"),
        "is_referenced_by_count": item.get("is-referenced-by-count"),
        "crossref_has_update_filter": False,
        "status_marker_in_title": False,
        "screen_state": "PROVISIONAL_CROSSREF_NEGATIVE",
        "required_next_screen": "PLOS/PubMed notice screen + full-text/artifact qualification",
    }


def discover(
    *,
    per_target: int = 3,
    window_days: int = 45,
    query_rows: int = 100,
) -> dict[str, Any]:
    excluded = known_registry_dois()
    excluded.update(normalize_doi(t["target_doi"]) for t in TARGETS)

    matches: list[dict[str, Any]] = []
    for target in TARGETS:
        tdate = dt.date.fromisoformat(target["published"])
        items = query_window(
            target["published"],
            window_days=window_days,
            rows=query_rows,
        )
        scored = []
        for item in items:
            row = score_candidate(item, target_date=tdate, excluded=excluded)
            if row is not None:
                scored.append(row)
        scored.sort(
            key=lambda x: (
                int(x["date_distance_days"]),
                str(x["candidate_doi"]),
            )
        )

        # Keep candidate DOIs unique across target matches.
        chosen = []
        for row in scored:
            if row["candidate_doi"] in excluded:
                continue
            chosen.append(row)
            excluded.add(row["candidate_doi"])
            if len(chosen) >= per_target:
                break

        for rank, row in enumerate(chosen, 1):
            matches.append(
                {
                    "target_id": target["target_id"],
                    "target_doi": normalize_doi(target["target_doi"]),
                    "target_published": target["published"],
                    "match_rank": rank,
                    **row,
                }
            )

    by_target = {
        target["target_id"]: sum(
            1 for row in matches if row["target_id"] == target["target_id"]
        )
        for target in TARGETS
    }
    return {
        "analysis": "ARIS4C011 development comparator discovery",
        "benchmark_role": "NO_KNOWN_INTEGRITY_CONCERN_COMPARATOR_CANDIDATE",
        "claim_boundary": (
            "Crossref has-update=0 and absence of title status markers are only "
            "negative-screen signals as of retrieval; they do not establish "
            "that a paper is error-free or integrity-concern-free. No "
            "specificity/false-positive estimate is permitted from this "
            "development candidate set."
        ),
        "journal_issn": PLOS_ONE_ISSN,
        "matching_variables": [
            "same journal",
            "same article type",
            f"publication date within +/-{window_days} days",
        ],
        "explicit_nonmatching_variables": [
            "detector output",
            "review priority",
            "finding count",
            "integrity-model score",
        ],
        "crossref_screen": {
            "has_update": False,
            "title_status_marker": False,
            "known_issue_registry_doi_excluded": True,
        },
        "secondary_screen_required": True,
        "targets": TARGETS,
        "candidate_count": len(matches),
        "candidate_count_by_target": by_target,
        "matches": matches,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--per-target", type=int, default=3)
    p.add_argument("--window-days", type=int, default=45)
    p.add_argument("--query-rows", type=int, default=100)
    args = p.parse_args()

    if args.per_target < 1 or args.per_target > 10:
        raise SystemExit("--per-target must be 1..10")
    result = discover(
        per_target=args.per_target,
        window_days=args.window_days,
        query_rows=args.query_rows,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "candidate_count": result["candidate_count"],
                "candidate_count_by_target": result["candidate_count_by_target"],
                "secondary_screen_required": True,
            },
            indent=2,
        )
    )
    if min(result["candidate_count_by_target"].values()) < args.per_target:
        raise SystemExit("Insufficient provisional comparators for at least one target")


if __name__ == "__main__":
    main()
