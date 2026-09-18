#!/usr/bin/env python3
"""Build pre-shock semantic-neighborhood candidates for Innovation Delay.

This is candidate discovery only. It does not create causal controls and does
not estimate treatment effects.

For each source:
1. fetch the source OpenAlex record;
2. reconstruct title + abstract text;
3. semantic-search OpenAlex for works published before the event date;
4. optionally constrain to the source's primary field;
5. retain article/review candidates and query provenance.

No post-event outcome is used for selection.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE = "https://api.openalex.org"
UA = "ARIS4C005-innovation-delay/0.1"


def bare_id(raw: str) -> str:
    return raw.rstrip("/").split("/")[-1]


def request(path: str, params: dict[str, Any] | None = None, retries: int = 5):
    params = dict(params or {})
    key = os.getenv("OPENALEX_API_KEY", "").strip()
    mailto = os.getenv("OPENALEX_MAILTO", "").strip()
    if key:
        params["api_key"] = key
    if mailto:
        params["mailto"] = mailto
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params, safe="|,:/")
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


def reconstruct_abstract(inverted: dict[str, list[int]] | None) -> str:
    if not inverted:
        return ""
    positions: list[tuple[int, str]] = []
    for token, locs in inverted.items():
        for pos in locs:
            positions.append((int(pos), token))
    positions.sort()
    return " ".join(token for _, token in positions)


def semantic_query_text(work: dict[str, Any], max_chars: int = 2000) -> str:
    title = str(work.get("display_name") or work.get("title") or "").strip()
    abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
    text = (title + "\n" + abstract).strip()
    if not text:
        raise ValueError("Source has neither title nor abstract")
    return text[:max_chars]


def source_field_id(work: dict[str, Any]) -> str:
    topic = work.get("primary_topic") or {}
    field = topic.get("field") or {}
    raw = str(field.get("id") or "")
    return bare_id(raw) if raw else ""


def day_before(date_text: str) -> str:
    date = dt.date.fromisoformat(date_text)
    return (date - dt.timedelta(days=1)).isoformat()


def discover_candidates(
    source_work: dict[str, Any],
    event_date: str,
    *,
    n: int,
    constrain_field: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not 1 <= n <= 50:
        raise ValueError("semantic-search candidate count must be 1..50")

    query = semantic_query_text(source_work)
    field_id = source_field_id(source_work)
    filters = [
        f"to_publication_date:{day_before(event_date)}",
        "type:article|review",
    ]
    if constrain_field and field_id:
        filters.append(f"primary_topic.field.id:{field_id}")

    params = {
        "search.semantic": query,
        "filter": ",".join(filters),
        "corpus": "core",
        "per_page": n,
        "select": (
            "id,doi,display_name,publication_date,publication_year,type,"
            "primary_topic,cited_by_count"
        ),
    }
    data = request("/works", params)
    source_id = bare_id(str(source_work["id"]))

    candidates = []
    for rank, work in enumerate(data.get("results", []), start=1):
        if bare_id(str(work.get("id") or "")) == source_id:
            continue
        candidates.append(
            {
                "candidate_rank": rank,
                "candidate_openalex_id": work.get("id", ""),
                "candidate_doi": work.get("doi") or "",
                "candidate_title": work.get("display_name") or "",
                "candidate_publication_date": work.get("publication_date") or "",
                "candidate_publication_year": work.get("publication_year") or "",
                "candidate_type": work.get("type") or "",
                "candidate_primary_topic": json.dumps(
                    work.get("primary_topic") or {},
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
                # relevance_score is returned by search but can be absent from
                # select-constrained responses; retain blank if unavailable.
                "semantic_relevance_score": work.get("relevance_score", ""),
                "candidate_cited_by_count_snapshot": work.get("cited_by_count", ""),
            }
        )

    provenance = {
        "source_openalex_id": source_work["id"],
        "event_date": event_date,
        "semantic_query_sha256": hashlib.sha256(
            query.encode("utf-8")
        ).hexdigest(),
        "semantic_query_chars": len(query),
        "candidate_count_requested": n,
        "candidate_count_returned_excluding_source": len(candidates),
        "constrain_primary_field": constrain_field,
        "source_primary_field_id": field_id,
        "filters": filters,
        "corpus": "core",
        "warning": (
            "Candidate discovery uses pre-event publications only. "
            "cited_by_count_snapshot is retained for provenance/diagnostics and "
            "must not be used as a post-treatment matching feature."
        ),
    }
    return candidates, provenance


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("sources_csv", type=Path)
    p.add_argument("candidates_csv", type=Path)
    p.add_argument("provenance_json", type=Path)
    p.add_argument("--n", type=int, default=30)
    p.add_argument("--no-field-constraint", action="store_true")
    args = p.parse_args()

    with args.sources_csv.open("r", encoding="utf-8-sig", newline="") as f:
        sources = list(csv.DictReader(f))

    output = []
    provenance = {
        "classification": "PRE_SHOCK_SEMANTIC_NEIGHBOR_CANDIDATES_NOT_CAUSAL_MATCHES",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sources": [],
        "warnings": [
            "Candidates are not final matched controls.",
            "Only pre-event candidate publications are eligible.",
            "Post-event outcomes must not be used for matching.",
            "OpenAlex semantic ranking/version can change over time.",
        ],
    }

    for row in sources:
        source_id = (row.get("source_openalex_id") or "").strip()
        event_date = (row.get("event_date") or row.get("source_retraction_date") or "").strip()
        if not source_id or not event_date:
            raise ValueError("Each source needs source_openalex_id and event_date/source_retraction_date")

        work = request(
            "/works/" + bare_id(source_id),
            {
                "select": (
                    "id,doi,display_name,abstract_inverted_index,"
                    "publication_date,primary_topic"
                )
            },
        )
        candidates, prov = discover_candidates(
            work,
            event_date,
            n=args.n,
            constrain_field=not args.no_field_constraint,
        )
        source_local_id = row.get("source_id") or bare_id(source_id)
        for cand in candidates:
            output.append(
                {
                    "source_id": source_local_id,
                    "source_openalex_id": source_id,
                    "event_date": event_date,
                    "exposure_family": row.get("exposure_family") or "",
                    **cand,
                }
            )
        provenance["sources"].append(prov)

    args.candidates_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = list(output[0].keys()) if output else []
    with args.candidates_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)

    args.provenance_json.parent.mkdir(parents=True, exist_ok=True)
    args.provenance_json.write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(provenance, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
