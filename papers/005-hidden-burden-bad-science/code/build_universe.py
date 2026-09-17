#!/usr/bin/env python3
"""Build a versioned annual publication-universe count from OpenAlex.

ARIS4C005 uses this script for *denominator construction*, not for estimating
misconduct. By default it queries the curated OpenAlex core corpus and counts
journal-style work types article + review by publication year.

Example
-------
python build_universe.py --start 2000 --end 2025 --output ../data/openalex_universe_counts.csv

Optional environment variables
------------------------------
OPENALEX_API_KEY   API key if your access tier requires/provides one.
OPENALEX_MAILTO    Contact email included in the User-Agent for polite use.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE_URL = "https://api.openalex.org/works"


def _request_json(url: str) -> dict[str, Any]:
    email = os.environ.get("OPENALEX_MAILTO", "")
    ua = "ARIS4C005/0.1"
    if email:
        ua += f" (mailto:{email})"
    headers = {"User-Agent": ua, "Accept": "application/json"}
    api_key = os.environ.get("OPENALEX_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAlex HTTP {exc.code}: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenAlex request failed: {exc}") from exc


def fetch_year_counts(
    start_year: int,
    end_year: int,
    work_types: list[str],
    corpus: str = "core",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return annual counts plus retrieval provenance."""
    type_expr = "|".join(work_types)
    filters = f"publication_year:{start_year}-{end_year},type:{type_expr}"
    params = {
        "filter": filters,
        "group_by": "publication_year",
        "per_page": "200",
        "corpus": corpus,
    }
    url = BASE_URL + "?" + urllib.parse.urlencode(params, safe=":,|-")
    payload = _request_json(url)

    groups = payload.get("group_by") or []
    by_year: dict[int, int] = {}
    for group in groups:
        key = group.get("key")
        try:
            year = int(key)
        except (TypeError, ValueError):
            continue
        if start_year <= year <= end_year:
            by_year[year] = int(group.get("count", 0))

    rows = [
        {
            "year": year,
            "count": by_year.get(year, 0),
            "work_types": "|".join(work_types),
            "corpus": corpus,
        }
        for year in range(start_year, end_year + 1)
    ]

    provenance = {
        "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": "OpenAlex Works API",
        "endpoint": BASE_URL,
        "query_url": url,
        "filter": filters,
        "group_by": "publication_year",
        "corpus": corpus,
        "work_types": work_types,
        "meta_count": (payload.get("meta") or {}).get("count"),
    }
    return rows, provenance


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["year", "count", "work_types", "corpus"]
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=2000)
    parser.add_argument("--end", type=int, default=2025)
    parser.add_argument(
        "--types",
        default="article,review",
        help="Comma-separated OpenAlex work types (default: article,review)",
    )
    parser.add_argument(
        "--corpus", choices=["core", "expansion", "all"], default="core"
    )
    parser.add_argument(
        "--output", type=Path, default=Path("../data/openalex_universe_counts.csv")
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=Path("../data/openalex_universe_provenance.json"),
    )
    args = parser.parse_args()

    if args.start > args.end:
        parser.error("--start must be <= --end")

    work_types = [x.strip() for x in args.types.split(",") if x.strip()]
    if not work_types:
        parser.error("At least one work type is required")

    rows, provenance = fetch_year_counts(
        args.start, args.end, work_types=work_types, corpus=args.corpus
    )
    write_csv(rows, args.output)
    args.provenance.parent.mkdir(parents=True, exist_ok=True)
    args.provenance.write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    total = sum(row["count"] for row in rows)
    print(f"Wrote {len(rows)} annual rows; total={total:,}")
    print(f"CSV: {args.output}")
    print(f"Provenance: {args.provenance}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
