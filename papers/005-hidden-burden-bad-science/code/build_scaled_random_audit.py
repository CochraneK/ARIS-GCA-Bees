#!/usr/bin/env python3
"""Build the scaled 2000–2025 confirmatory random-audit frame for ARIS4C005.

Design:
- OpenAlex core, article|review, publication years 2000–2025;
- six non-overlapping time strata;
- each stratum receives a minimum allocation, then remaining sample is
  distributed proportional to stratum population size;
- exact first-order inclusion probability within stratum: pi_h = n_h / N_h;
- each selected work stores design weight 1/pi_h.

This frame is for prevalence inference. It contains no detector enrichment and
no integrity label. AI adjudicators are downstream measurement instruments,
not sampling mechanisms."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

BASE_URL = "https://api.openalex.org/works"
UA = "ARIS4C005-scaled-audit/0.1"

DEFAULT_STRATA = [
    ("2000_2004", 2000, 2004),
    ("2005_2009", 2005, 2009),
    ("2010_2014", 2010, 2014),
    ("2015_2019", 2015, 2019),
    ("2020_2024", 2020, 2024),
    ("2025", 2025, 2025),
]


def request(params: dict[str, Any], retries: int = 5) -> dict[str, Any]:
    params = dict(params)
    key = os.getenv("OPENALEX_API_KEY", "").strip()
    mailto = os.getenv("OPENALEX_MAILTO", "").strip()
    if key:
        params["api_key"] = key
    if mailto:
        params["mailto"] = mailto
    url = BASE_URL + "?" + urllib.parse.urlencode(params, safe="|,:/")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    delay = 1.0
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            if attempt + 1 >= retries:
                raise
            time.sleep(delay)
            delay *= 2
    raise AssertionError("unreachable")


def filter_expr(start: int, end: int) -> str:
    return f"publication_year:{start}-{end},type:article|review"


def count_stratum(start: int, end: int, corpus: str) -> int:
    data = request({
        "filter": filter_expr(start, end),
        "corpus": corpus,
        "per_page": 1,
        "select": "id",
    })
    return int(data["meta"]["count"])


def allocate(counts: dict[str, int], total_n: int, minimum_per_stratum: int) -> dict[str, int]:
    keys = list(counts)
    if total_n < minimum_per_stratum * len(keys):
        raise ValueError("total_n smaller than minimum allocation across strata")
    alloc = {k: min(minimum_per_stratum, counts[k]) for k in keys}
    remaining = total_n - sum(alloc.values())
    available = {k: max(counts[k] - alloc[k], 0) for k in keys}
    total_available = sum(available.values())
    if remaining <= 0 or total_available <= 0:
        return alloc

    raw = {k: remaining * available[k] / total_available for k in keys}
    floors = {k: int(math.floor(raw[k])) for k in keys}
    for k in keys:
        alloc[k] += min(floors[k], available[k])

    leftover = total_n - sum(alloc.values())
    order = sorted(
        keys,
        key=lambda k: (raw[k] - floors[k], available[k] - floors[k]),
        reverse=True,
    )
    i = 0
    while leftover > 0:
        k = order[i % len(order)]
        if alloc[k] < counts[k]:
            alloc[k] += 1
            leftover -= 1
        i += 1
        if i > total_n * len(order) * 2:
            raise RuntimeError("allocation loop failed")
    return alloc


def stable_id(openalex_id: str) -> str:
    return "P" + hashlib.sha256(openalex_id.encode()).hexdigest()[:16]


def topic_fields(work: dict[str, Any]) -> tuple[str, str, str]:
    topic = work.get("primary_topic") or {}
    domain = topic.get("domain") or {}
    field = topic.get("field") or {}
    subfield = topic.get("subfield") or {}
    return (
        str(domain.get("display_name") or ""),
        str(field.get("display_name") or ""),
        str(subfield.get("display_name") or ""),
    )


def sample_stratum(start: int, end: int, n: int, seed: int, corpus: str) -> list[dict[str, Any]]:
    if n <= 0:
        return []
    if n > 10000:
        raise ValueError("OpenAlex sample endpoint supports at most 10,000 per stratum")
    per_page = 200
    pages = math.ceil(n / per_page)
    rows = []
    for page in range(1, pages + 1):
        data = request({
            "filter": filter_expr(start, end),
            "corpus": corpus,
            "sample": n,
            "seed": seed,
            "per_page": per_page,
            "page": page,
            "select": "id,doi,publication_year,type,primary_topic",
        })
        rows.extend(data.get("results", []))
    seen = set()
    out = []
    for w in rows:
        wid = str(w.get("id") or "")
        if wid and wid not in seen:
            seen.add(wid)
            out.append(w)
    return out[:n]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("output_csv", type=Path)
    p.add_argument("summary_json", type=Path)
    p.add_argument("--total-n", type=int, default=10000)
    p.add_argument("--minimum-per-stratum", type=int, default=1000)
    p.add_argument("--corpus", default="core", choices=["core", "expansion", "all"])
    p.add_argument("--seed", type=int, default=20260918)
    args = p.parse_args()

    counts = {}
    for name, start, end in DEFAULT_STRATA:
        counts[name] = count_stratum(start, end, args.corpus)

    alloc = allocate(counts, args.total_n, args.minimum_per_stratum)
    all_rows = []
    stratum_summary = {}

    for idx, (name, start, end) in enumerate(DEFAULT_STRATA):
        n = alloc[name]
        N = counts[name]
        pi = n / N if N else 0.0
        works = sample_stratum(start, end, n, args.seed + idx * 100003, args.corpus)
        for w in works:
            domain, field, subfield = topic_fields(w)
            all_rows.append({
                "paper_id": stable_id(w["id"]),
                "openalex_id": w["id"],
                "doi": w.get("doi") or "",
                "publication_year": w.get("publication_year") or "",
                "work_type": w.get("type") or "",
                "primary_domain": domain,
                "primary_field": field,
                "primary_subfield": subfield,
                "audit_stratum": name,
                "stratum_population_N": N,
                "stratum_sample_n": n,
                "aris_inclusion_probability": f"{pi:.12g}",
                "aris_design_weight": f"{(1.0/pi):.12g}" if pi else "",
                "aris_sampling_seed": args.seed + idx * 100003,
            })
        stratum_summary[name] = {
            "start_year": start,
            "end_year": end,
            "population_N": N,
            "target_n": n,
            "realized_unique_n": len({w["id"] for w in works}),
            "inclusion_probability": pi,
            "design_weight": (1.0 / pi) if pi else None,
        }

    ids = [r["openalex_id"] for r in all_rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate OpenAlex IDs across scaled audit strata")

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    domain_counts = Counter(r["primary_domain"] or "missing" for r in all_rows)
    year_counts = Counter(str(r["publication_year"]) for r in all_rows)
    doi_missing = sum(1 for r in all_rows if not r["doi"])
    summary = {
        "classification": "SCALED_RANDOM_AUDIT_FRAME_NOT_ADJUDICATION_RESULTS",
        "target_universe": "OpenAlex core article|review 2000-2025",
        "total_population_N": sum(counts.values()),
        "target_total_n": args.total_n,
        "realized_total_n": len(all_rows),
        "allocation_rule": (
            "minimum_per_stratum then remaining sample proportional to remaining "
            "stratum population; design weights recover target-universe prevalence"
        ),
        "minimum_per_stratum": args.minimum_per_stratum,
        "strata": stratum_summary,
        "realized_domain_counts": dict(domain_counts),
        "realized_year_counts": dict(sorted(year_counts.items())),
        "works_without_doi": doi_missing,
        "warnings": [
            "This frame contains no integrity labels.",
            "AI adjudication error must be calibrated or sensitivity-tested.",
            "Weighted analysis is required because time strata have unequal inclusion probabilities.",
            "OpenAlex metadata coverage and type classification remain denominator limitations.",
        ],
    }
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
