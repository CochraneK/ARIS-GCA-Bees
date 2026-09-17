#!/usr/bin/env python3
"""ARIS4C006 — OpenAlex author-order feasibility pilot.

This script is deliberately NOT a confirmatory surname-effect analysis.
It tests whether we can extract China-affiliated works, preserve listed author
order, and estimate crude observed-vs-chance alphabetization rates.

The surname parser used here is HEURISTIC ONLY (last Latin token). Its outputs
must not be used for substantive inference. See process/DATA_SOURCES.md.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

API = "https://api.openalex.org/works"
USER_AGENT = "ARIS4C006/0.1 (research feasibility pilot)"
LATIN_TOKEN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ'’-]+")


def fetch_json(url: str) -> dict:
    headers = {"User-Agent": USER_AGENT}
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def heuristic_family_token(name: str | None) -> str | None:
    """Engineering-only parser: return final Latin token.

    WARNING: unsafe for confirmatory Chinese-name inference because Chinese
    names can be written in either family-given or given-family order.
    """
    if not name:
        return None
    tokens = LATIN_TOKEN.findall(name.strip())
    if not tokens:
        return None
    return tokens[-1].lower()


def is_sorted(keys: list[str]) -> bool:
    return keys == sorted(keys)


def chance_alphabetical_probability(keys: list[str]) -> float:
    """Exact random-order probability for a multiset of surname keys.

    Number of unique distinguishable permutations is n! / product(m_j!).
    Exactly one non-decreasing ordering exists, so probability is its inverse.
    """
    n = len(keys)
    if n < 2:
        return float("nan")
    counts: dict[str, int] = defaultdict(int)
    for key in keys:
        counts[key] += 1
    unique_permutations = math.factorial(n)
    for count in counts.values():
        unique_permutations //= math.factorial(count)
    return 1.0 / unique_permutations


def iter_works(year: int, max_works: int, api_key: str | None, mailto: str | None):
    cursor = "*"
    yielded = 0
    select = ",".join([
        "id", "doi", "display_name", "publication_year", "authorships",
        "primary_topic", "primary_location", "cited_by_count"
    ])
    filters = ",".join([
        "authorships.institutions.country_code:CN",
        f"from_publication_date:{year}-01-01",
        f"to_publication_date:{year}-12-31",
    ])

    while yielded < max_works:
        params = {
            "filter": filters,
            "select": select,
            "per-page": min(100, max_works - yielded),
            "cursor": cursor,
        }
        if api_key:
            params["api_key"] = api_key
        if mailto:
            params["mailto"] = mailto

        url = API + "?" + urllib.parse.urlencode(params)
        payload = fetch_json(url)
        results = payload.get("results", [])
        if not results:
            break

        for work in results:
            yield work
            yielded += 1
            if yielded >= max_works:
                break

        cursor = payload.get("meta", {}).get("next_cursor")
        if not cursor:
            break
        time.sleep(0.1)


def work_row(work: dict) -> dict | None:
    authorships = work.get("authorships") or []
    if len(authorships) < 2:
        return None

    names = []
    keys = []
    for authorship in authorships:
        raw = authorship.get("raw_author_name")
        display = (authorship.get("author") or {}).get("display_name")
        name_for_pilot = raw or display
        key = heuristic_family_token(name_for_pilot)
        if not key:
            return None
        names.append(name_for_pilot)
        keys.append(key)

    topic = work.get("primary_topic") or {}
    field = topic.get("field") or {}
    source = ((work.get("primary_location") or {}).get("source") or {})

    chance = chance_alphabetical_probability(keys)
    return {
        "work_id": work.get("id"),
        "doi": work.get("doi"),
        "year": work.get("publication_year"),
        "source_id": source.get("id"),
        "source_name": source.get("display_name"),
        "field_id": field.get("id"),
        "field_name": field.get("display_name"),
        "team_size": len(keys),
        "is_alphabetical_heuristic": int(is_sorted(keys)),
        "chance_probability": chance,
        "author_names_json": json.dumps(names, ensure_ascii=False),
        "family_tokens_json": json.dumps(keys, ensure_ascii=False),
        "parser_tier": "HEURISTIC_ONLY_LAST_LATIN_TOKEN",
    }


def summarize(rows: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = (row["field_id"], row["field_name"], row["team_size"])
        groups[key].append(row)

    out = []
    for (field_id, field_name, team_size), items in sorted(groups.items(), key=lambda x: str(x[0])):
        n = len(items)
        observed = sum(x["is_alphabetical_heuristic"] for x in items) / n
        expected = sum(x["chance_probability"] for x in items) / n
        excess = (observed - expected) / (1 - expected) if expected < 1 else float("nan")
        out.append({
            "field_id": field_id,
            "field_name": field_name,
            "team_size": team_size,
            "n_works": n,
            "observed_alpha_rate": observed,
            "expected_chance_rate": expected,
            "excess_alpha_rate": excess,
            "warning": "surname parser is heuristic-only; feasibility output, not substantive result",
        })
    return out


def write_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--max-works", type=int, default=1000)
    parser.add_argument("--outdir", default="data/pilot/openalex")
    args = parser.parse_args()

    api_key = os.getenv("OPENALEX_API_KEY")
    mailto = os.getenv("OPENALEX_MAILTO")

    rows = []
    for work in iter_works(args.year, args.max_works, api_key, mailto):
        row = work_row(work)
        if row:
            rows.append(row)

    outdir = Path(args.outdir)
    write_csv(outdir / f"works_{args.year}_heuristic.csv", rows)
    summary = summarize(rows)
    write_csv(outdir / f"alphabetization_summary_{args.year}_heuristic.csv", summary)

    manifest = {
        "script": "01_openalex_alphabetization_pilot.py",
        "year": args.year,
        "requested_max_works": args.max_works,
        "eligible_multi_author_works": len(rows),
        "api_key_present": bool(api_key),
        "parser": "HEURISTIC_ONLY_LAST_LATIN_TOKEN",
        "confirmatory_use_allowed": False,
        "note": (
            "This pilot validates extraction/order mechanics only. Replace the surname parser "
            "with the validated ARIS4C006 parser before substantive inference."
        ),
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"manifest_{args.year}.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
