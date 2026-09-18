#!/usr/bin/env python3
"""Build a mature historical delayed-recognition pilot from OpenAlex.

Sampling:
- OpenAlex core
- article|review
- publication years 1990–2005
- cited_by_count > 0
- reproducible random sample

For each sampled work, annual incoming citations are reconstructed with a live:
    filter=cites:<WORK_ID>&group_by=publication_year

The nested Work counts_by_year field is deliberately NOT used because current
OpenAlex documentation retains only roughly the last ten years for Works.

Outputs:
- private row-level annual citation history CSV;
- private row-level delayed-recognition metrics CSV;
- public-safe aggregate JSON.

This is a historical measurement pilot, not an estimate of lost discoveries.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import os
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

from sleeping_beauty import paper_metrics

BASE = "https://api.openalex.org/works"
UA = "ARIS4C005-sleeping-beauty-pilot/0.1"


def request(params: dict[str, Any], retries: int = 5) -> dict[str, Any]:
    params = dict(params)
    key = os.getenv("OPENALEX_API_KEY", "").strip()
    mailto = os.getenv("OPENALEX_MAILTO", "").strip()
    if key:
        params["api_key"] = key
    if mailto:
        params["mailto"] = mailto
    url = BASE + "?" + urllib.parse.urlencode(params, safe="|,:/")
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


def bare_id(raw: str) -> str:
    return raw.rstrip("/").split("/")[-1]


def random_mature_sample(
    start: int,
    end: int,
    n: int,
    seed: int,
) -> list[dict[str, Any]]:
    if not (1 <= n <= 10000):
        raise ValueError("sample n must be 1..10000")
    per_page = 100
    pages = math.ceil(n / per_page)
    rows: list[dict[str, Any]] = []
    filt = (
        f"publication_year:{start}-{end},"
        "type:article|review,cited_by_count:>0"
    )
    for page in range(1, pages + 1):
        data = request(
            {
                "filter": filt,
                "corpus": "core",
                "sample": n,
                "seed": seed,
                "page": page,
                "per_page": per_page,
                "select": (
                    "id,doi,display_name,publication_year,type,"
                    "cited_by_count,primary_topic"
                ),
            }
        )
        rows.extend(data.get("results", []))

    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for w in rows:
        wid = str(w.get("id") or "")
        if wid and wid not in seen:
            seen.add(wid)
            out.append(w)
    return out[:n]


def citation_counts_by_year(work_id: str) -> dict[int, int]:
    data = request(
        {
            "filter": f"cites:{bare_id(work_id)}",
            "group_by": "publication_year",
            "per_page": 100,
        }
    )
    out: dict[int, int] = {}
    for group in data.get("group_by", []):
        try:
            year = int(group["key"])
            count = int(group["count"])
        except (KeyError, TypeError, ValueError):
            continue
        out[year] = count
    return out


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


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    xs = sorted(values)
    if q <= 0:
        return xs[0]
    if q >= 1:
        return xs[-1]
    pos = q * (len(xs) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return xs[lo]
    frac = pos - lo
    return xs[lo] * (1.0 - frac) + xs[hi] * frac


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("history_csv", type=Path)
    p.add_argument("metrics_csv", type=Path)
    p.add_argument("summary_json", type=Path)
    p.add_argument("--start", type=int, default=1990)
    p.add_argument("--end", type=int, default=2005)
    p.add_argument("--sample-n", type=int, default=200)
    p.add_argument("--seed", type=int, default=20260918)
    p.add_argument("--observation-end-year", type=int, default=2025)
    args = p.parse_args()

    works = random_mature_sample(args.start, args.end, args.sample_n, args.seed)
    histories: list[dict[str, Any]] = []
    metrics_rows: list[dict[str, Any]] = []
    domain_counts: Counter[str] = Counter()

    for index, work in enumerate(works, start=1):
        wid = str(work["id"])
        pub_year = int(work["publication_year"])
        counts = citation_counts_by_year(wid)

        # Citation groups can include metadata errors predating publication;
        # those are excluded and counted in aggregate QA.
        valid_counts = {
            year: count
            for year, count in counts.items()
            if pub_year <= year <= args.observation_end_year
        }
        for year in range(pub_year, args.observation_end_year + 1):
            histories.append(
                {
                    "paper_id": f"SBP{index:04d}",
                    "openalex_id": wid,
                    "publication_year": pub_year,
                    "citation_year": year,
                    "citations": int(valid_counts.get(year, 0)),
                }
            )

        metric = paper_metrics(
            f"SBP{index:04d}",
            pub_year,
            valid_counts,
            observation_end_year=args.observation_end_year,
        )
        domain, field, subfield = topic_fields(work)
        metric.update(
            {
                "openalex_id": wid,
                "doi": work.get("doi") or "",
                "work_type": work.get("type") or "",
                "primary_domain": domain,
                "primary_field": field,
                "primary_subfield": subfield,
                "openalex_cited_by_count_snapshot": int(
                    work.get("cited_by_count") or 0
                ),
                "grouped_live_citations_through_observation_end": sum(
                    valid_counts.values()
                ),
            }
        )
        metrics_rows.append(metric)
        domain_counts[domain or "missing"] += 1

    write_csv(args.history_csv, histories)
    write_csv(args.metrics_csv, metrics_rows)

    b = [float(r["beauty_coefficient"]) for r in metrics_rows]
    peak_ages = [float(r["peak_citation_age"]) for r in metrics_rows]
    awakening_ages = [float(r["awakening_age"]) for r in metrics_rows]

    summary = {
        "classification": "MATURE_RANDOM_DELAYED_RECOGNITION_PILOT_NOT_LOST_DISCOVERY_COUNT",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sampling": {
            "database": "OpenAlex",
            "corpus": "core",
            "types": ["article", "review"],
            "publication_years": [args.start, args.end],
            "filter_requires_cited_by_count_gt_zero": True,
            "sample_n_requested": args.sample_n,
            "sample_n_realized": len(metrics_rows),
            "seed": args.seed,
            "observation_end_year": args.observation_end_year,
        },
        "citation_history_method": (
            "live incoming-citation works grouped by publication_year for each source; "
            "nested Work counts_by_year is not used"
        ),
        "domain_counts": dict(domain_counts),
        "beauty_coefficient": {
            "min": min(b) if b else None,
            "q25": quantile(b, 0.25),
            "median": quantile(b, 0.50),
            "q75": quantile(b, 0.75),
            "q90": quantile(b, 0.90),
            "q95": quantile(b, 0.95),
            "q99": quantile(b, 0.99),
            "max": max(b) if b else None,
        },
        "peak_citation_age": {
            "median": quantile(peak_ages, 0.50),
            "q90": quantile(peak_ages, 0.90),
            "max": max(peak_ages) if peak_ages else None,
        },
        "awakening_age": {
            "median": quantile(awakening_ages, 0.50),
            "q90": quantile(awakening_ages, 0.90),
            "max": max(awakening_ages) if awakening_ages else None,
        },
        "warnings": [
            "This is a small engineering pilot, not a global Sleeping Beauty prevalence estimate.",
            "Sampling conditions on having at least one matched citation.",
            "Beauty Coefficient is continuous; no natural universal threshold is inferred.",
            "OpenAlex citation links depend on reference matching and can miss printed citations.",
            "Citation graph and counts can drift across database snapshots.",
            "Historical delayed recognition does not establish integrity-related suppression.",
        ],
    }
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
