#!/usr/bin/env python3
"""ARIS4C006 — stratified author-order exposure feasibility pilot.

Purpose
-------
Verify that China-affiliated OpenAlex works contain enough between-field
variation in alphabetical ordering to support the planned exposure moderator.

This is NOT a confirmatory surname-effect analysis. It deliberately reuses the
engineering-only final-Latin-token parser so that field sampling and chance-
correction mechanics can be tested before the validated Chinese surname parser
exists. No substantive effect should be inferred from these rates.
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
from collections import Counter, defaultdict
from pathlib import Path

API = "https://api.openalex.org/works"
USER_AGENT = "ARIS4C006/0.2 (stratified feasibility pilot)"
LATIN_TOKEN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ'’-]+")

# OpenAlex field IDs are stable concept-like Field entity IDs. The selected
# contrast is theory/literature motivated and is fixed before this pilot runs.
FIELD_SET = {
    20: "Economics, Econometrics and Finance",
    26: "Mathematics",
    14: "Business, Management and Accounting",
    32: "Psychology",
    27: "Medicine",
    22: "Engineering",
}


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def heuristic_family_token(name: str | None) -> str | None:
    if not name:
        return None
    tokens = LATIN_TOKEN.findall(name.strip())
    return tokens[-1].lower() if tokens else None


def chance_alpha_probability(keys: list[str]) -> float:
    n = len(keys)
    counts = Counter(keys)
    distinguishable = math.factorial(n)
    for count in counts.values():
        distinguishable //= math.factorial(count)
    return 1.0 / distinguishable


def country_set(authorships: list[dict]) -> set[str]:
    countries: set[str] = set()
    for authorship in authorships:
        for inst in authorship.get("institutions") or []:
            code = inst.get("country_code")
            if code:
                countries.add(code)
        for code in authorship.get("countries") or []:
            if code:
                countries.add(code)
    return countries


def iter_field_works(field_id: int, year: int, max_works: int):
    cursor = "*"
    yielded = 0
    while yielded < max_works:
        params = {
            "filter": ",".join([
                "authorships.institutions.country_code:CN",
                f"topics.field.id:{field_id}",
                f"from_publication_date:{year}-01-01",
                f"to_publication_date:{year}-12-31",
            ]),
            "select": "id,publication_year,authorships,primary_topic",
            "per-page": min(100, max_works - yielded),
            "cursor": cursor,
        }
        mailto = os.getenv("OPENALEX_MAILTO")
        api_key = os.getenv("OPENALEX_API_KEY")
        if mailto:
            params["mailto"] = mailto
        if api_key:
            params["api_key"] = api_key

        payload = fetch_json(API + "?" + urllib.parse.urlencode(params))
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
        time.sleep(0.12)


def classify_work(work: dict) -> dict | None:
    authorships = work.get("authorships") or []
    if len(authorships) < 2:
        return None

    keys: list[str] = []
    for authorship in authorships:
        raw = authorship.get("raw_author_name")
        display = (authorship.get("author") or {}).get("display_name")
        key = heuristic_family_token(raw or display)
        if key is None:
            return None
        keys.append(key)

    countries = country_set(authorships)
    observed = int(keys == sorted(keys))
    return {
        "team_size": len(keys),
        "team_bucket": "2" if len(keys) == 2 else "3+",
        "observed_alpha": observed,
        "chance_alpha": chance_alpha_probability(keys),
        "international_mixed": int("CN" in countries and len(countries - {"CN"}) > 0),
    }


def summarize_field(field_id: int, field_name: str, records: list[dict], requested: int) -> list[dict]:
    outputs: list[dict] = []
    for bucket in ["all", "2", "3+"]:
        subset = records if bucket == "all" else [r for r in records if r["team_bucket"] == bucket]
        if not subset:
            continue
        n = len(subset)
        observed = sum(r["observed_alpha"] for r in subset) / n
        expected = sum(r["chance_alpha"] for r in subset) / n
        excess = (observed - expected) / (1 - expected) if expected < 1 else float("nan")
        outputs.append({
            "field_id": field_id,
            "field_name": field_name,
            "team_bucket": bucket,
            "requested_works": requested,
            "eligible_multi_author_works": n,
            "observed_alpha_rate_heuristic": observed,
            "expected_chance_rate": expected,
            "excess_alpha_rate_heuristic": excess,
            "mixed_international_share": sum(r["international_mixed"] for r in subset) / n,
            "parser": "HEURISTIC_ONLY_LAST_LATIN_TOKEN",
            "confirmatory_use_allowed": False,
        })
    return outputs


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--per-field", type=int, default=300)
    parser.add_argument("--outdir", default="data/pilot/stratified")
    args = parser.parse_args()

    all_summary: list[dict] = []
    field_manifest: list[dict] = []

    for field_id, field_name in FIELD_SET.items():
        records: list[dict] = []
        raw_n = 0
        for work in iter_field_works(field_id, args.year, args.per_field):
            raw_n += 1
            record = classify_work(work)
            if record is not None:
                records.append(record)

        all_summary.extend(summarize_field(field_id, field_name, records, args.per_field))
        field_manifest.append({
            "field_id": field_id,
            "field_name": field_name,
            "retrieved_works": raw_n,
            "eligible_multi_author_parseable_works": len(records),
        })

    outdir = Path(args.outdir)
    write_csv(outdir / f"field_exposure_summary_{args.year}_heuristic.csv", all_summary)

    manifest = {
        "script": "02_stratified_exposure_pilot.py",
        "year": args.year,
        "per_field_requested": args.per_field,
        "fields": field_manifest,
        "parser": "HEURISTIC_ONLY_LAST_LATIN_TOKEN",
        "confirmatory_use_allowed": False,
        "interpretation": (
            "Use only to assess whether field-stratified OpenAlex extraction and convention variation are feasible. "
            "Rates must be recomputed after validated surname parsing."
        ),
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"manifest_{args.year}.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    for row in all_summary:
        if row["team_bucket"] == "all":
            print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
