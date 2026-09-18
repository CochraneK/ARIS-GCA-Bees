#!/usr/bin/env python3
"""Build a raw citation-exposure pilot for ARIS4C005.

This pilot deliberately selects highly cited, narrow E1-S Retraction Watch
sources to stress-test propagation infrastructure. It is NOT a representative
sample and MUST NOT be used for global contamination prevalence.

Outputs:
- public-safe aggregate JSON (no source identities);
- private/ephemeral source CSV;
- private/ephemeral sampled post-retraction citation-edge CSV.

Citation exposure is NOT semantic contamination.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import random
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

BASE_URL = "https://api.openalex.org/works"
UA = "ARIS4C005-contamination-pilot/0.1"


def norm_doi(raw: str | None) -> str | None:
    if not raw:
        return None
    v = raw.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if v.startswith(prefix):
            v = v[len(prefix):]
    if not v or v in {"unavailable", "0", "none", "nan"}:
        return None
    return v


def parse_date(raw: str | None) -> dt.date | None:
    if not raw:
        return None
    value = raw.strip()
    for fmt in ("%m/%d/%Y %H:%M", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    return None


def bare_oa_id(raw: str) -> str:
    return raw.rstrip("/").split("/")[-1]


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


def chunks(xs: list[str], n: int = 100) -> Iterable[list[str]]:
    for i in range(0, len(xs), n):
        yield xs[i:i+n]


def collapse_sources(path: Path, start: int, end: int) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if str(row.get("e1s_narrow_auto") or "0") != "1":
                continue
            doi = norm_doi(row.get("OriginalPaperDOI"))
            pub_date = parse_date(row.get("OriginalPaperDate"))
            ret_date = parse_date(row.get("RetractionDate"))
            if doi is None or pub_date is None or ret_date is None:
                continue
            if not (start <= pub_date.year <= end):
                continue
            # Restrict this pilot to formal Retraction nature, not EOC/correction.
            if (row.get("RetractionNature") or "").strip() != "Retraction":
                continue

            rec = out.setdefault(
                doi,
                {
                    "doi": doi,
                    "publication_date": pub_date,
                    "retraction_date": ret_date,
                },
            )
            rec["publication_date"] = min(rec["publication_date"], pub_date)
            rec["retraction_date"] = min(rec["retraction_date"], ret_date)
    return out


def lookup_openalex(dois: list[str]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for batch in chunks(dois, 100):
        data = request(
            {
                "filter": "doi:" + "|".join(f"https://doi.org/{d}" for d in batch),
                "per_page": 100,
                "select": (
                    "id,doi,display_name,publication_date,publication_year,type,"
                    "cited_by_count,primary_topic"
                ),
            }
        )
        for work in data.get("results", []):
            doi = norm_doi(work.get("doi"))
            if doi:
                out[doi] = work
    return out


def source_seed(openalex_id: str, seed: int) -> int:
    digest = hashlib.sha256(f"{openalex_id}|{seed}".encode()).hexdigest()
    return int(digest[:8], 16)


def citing_count(openalex_id: str, extra_filter: str | None = None) -> int:
    filters = [f"cites:{bare_oa_id(openalex_id)}"]
    if extra_filter:
        filters.append(extra_filter)
    data = request(
        {
            "filter": ",".join(filters),
            "per_page": 1,
            "select": "id",
        }
    )
    return int(data["meta"]["count"])


def citing_by_year(openalex_id: str) -> dict[int, int]:
    data = request(
        {
            "filter": f"cites:{bare_oa_id(openalex_id)}",
            "group_by": "publication_year",
            "per_page": 1,
        }
    )
    out: dict[int, int] = {}
    for group in data.get("group_by", []):
        try:
            out[int(group["key"])] = int(group["count"])
        except (KeyError, TypeError, ValueError):
            continue
    return out


def sample_post_retraction_citers(
    source: dict[str, Any],
    n: int,
    seed: int,
) -> list[dict[str, Any]]:
    if n <= 0:
        return []
    retraction_date = source["retraction_date"].isoformat()
    oa_id = bare_oa_id(source["openalex_id"])
    data = request(
        {
            "filter": f"cites:{oa_id},from_publication_date:{retraction_date}",
            "sample": min(n, 10000),
            "seed": source_seed(source["openalex_id"], seed),
            "per_page": min(n, 100),
            "select": (
                "id,doi,display_name,publication_date,publication_year,type,"
                "primary_topic,has_fulltext,open_access"
            ),
        }
    )
    return data.get("results", [])[:n]


def topic_names(work: dict[str, Any]) -> tuple[str, str, str]:
    topic = work.get("primary_topic") or {}
    domain = topic.get("domain") or {}
    field = topic.get("field") or {}
    subfield = topic.get("subfield") or {}
    return (
        str(domain.get("display_name") or ""),
        str(field.get("display_name") or ""),
        str(subfield.get("display_name") or ""),
    )


def edge_id(source_id: str, citing_id: str) -> str:
    raw = f"{source_id}|{citing_id}".encode()
    return "E" + hashlib.sha256(raw).hexdigest()[:18]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("classified_rw_csv", type=Path)
    p.add_argument("summary_json", type=Path)
    p.add_argument("sources_csv", type=Path)
    p.add_argument("edges_csv", type=Path)
    p.add_argument("--start", type=int, default=2010)
    p.add_argument("--end", type=int, default=2020)
    p.add_argument("--source-n", type=int, default=25)
    p.add_argument("--edge-sample-per-source", type=int, default=20)
    p.add_argument("--seed", type=int, default=20260918)
    args = p.parse_args()

    rw = collapse_sources(args.classified_rw_csv, args.start, args.end)
    resolved = lookup_openalex(sorted(rw))

    candidates: list[dict[str, Any]] = []
    for doi, meta in rw.items():
        work = resolved.get(doi)
        if not work:
            continue
        candidates.append(
            {
                **meta,
                "openalex_id": work["id"],
                "title": work.get("display_name") or "",
                "work_type": work.get("type") or "",
                "openalex_cited_by_count": int(work.get("cited_by_count") or 0),
                "primary_topic": work.get("primary_topic"),
            }
        )

    candidates.sort(
        key=lambda x: (x["openalex_cited_by_count"], x["doi"]), reverse=True
    )
    sources = candidates[: args.source_n]

    source_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    exposure_totals: list[int] = []
    post_totals: list[int] = []
    yearly_post_counts: Counter[int] = Counter()

    for source in sources:
        total = citing_count(source["openalex_id"])
        post = citing_count(
            source["openalex_id"],
            f"from_publication_date:{source['retraction_date'].isoformat()}",
        )
        by_year = citing_by_year(source["openalex_id"])
        domain, field, subfield = topic_names({"primary_topic": source.get("primary_topic")})

        source_rows.append(
            {
                "source_openalex_id": source["openalex_id"],
                "source_doi": source["doi"],
                "source_publication_date": source["publication_date"].isoformat(),
                "source_retraction_date": source["retraction_date"].isoformat(),
                "source_work_type": source["work_type"],
                "source_domain": domain,
                "source_field": field,
                "source_subfield": subfield,
                "openalex_cited_by_count_field": source["openalex_cited_by_count"],
                "live_incoming_citation_count": total,
                "post_retraction_incoming_count": post,
                "post_retraction_fraction_of_live_exposure": (
                    post / total if total else None
                ),
                "citation_counts_by_year_json": json.dumps(
                    dict(sorted(by_year.items())), separators=(",", ":")
                ),
            }
        )
        exposure_totals.append(total)
        post_totals.append(post)
        for year, count in by_year.items():
            if year >= source["retraction_date"].year:
                yearly_post_counts[year] += count

        citers = sample_post_retraction_citers(
            source, args.edge_sample_per_source, args.seed
        )
        for citing in citers:
            citing_date = citing.get("publication_date") or ""
            c_domain, c_field, c_subfield = topic_names(citing)
            edge_rows.append(
                {
                    "edge_id": edge_id(source["openalex_id"], citing["id"]),
                    "source_openalex_id": source["openalex_id"],
                    "source_doi": source["doi"],
                    "source_retraction_date": source["retraction_date"].isoformat(),
                    "citing_openalex_id": citing["id"],
                    "citing_doi": norm_doi(citing.get("doi")) or "",
                    "citing_title": citing.get("display_name") or "",
                    "citing_publication_date": citing_date,
                    "citing_work_type": citing.get("type") or "",
                    "citing_domain": c_domain,
                    "citing_field": c_field,
                    "citing_subfield": c_subfield,
                    "citing_has_fulltext": int(bool(citing.get("has_fulltext"))),
                    "citing_is_oa": int(bool((citing.get("open_access") or {}).get("is_oa"))),
                    "citation_after_retraction": "YES",
                    "semantic_class": "",
                    "component_implicated": "",
                    "material_to_downstream_claim": "",
                    "source_retraction_known_in_text": "",
                    "context_access": "",
                    "reviewer_id": "",
                    "review_confidence": "",
                    "evidence_locator": "",
                    "adjudication_note": "",
                }
            )

    def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = list(rows[0].keys()) if rows else []
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    write_csv(args.sources_csv, source_rows)
    write_csv(args.edges_csv, edge_rows)

    summary = {
        "classification": "HIGH_PROPAGATION_CITATION_EXPOSURE_PILOT_NOT_CONTAMINATION_PREVALENCE",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_selection": {
            "rw_screen": "e1s_narrow_auto==1 and RetractionNature==Retraction",
            "source_publication_years": [args.start, args.end],
            "resolved_candidate_sources": len(candidates),
            "selected_sources": len(sources),
            "selection_rule": "top OpenAlex cited_by_count among resolved candidates",
            "representative_sample": False,
        },
        "citation_exposure": {
            "sum_live_incoming_citation_edges_across_sources": sum(exposure_totals),
            "sum_post_retraction_incoming_edges_across_sources": sum(post_totals),
            "post_retraction_fraction_of_live_exposure": (
                sum(post_totals) / sum(exposure_totals)
                if sum(exposure_totals)
                else None
            ),
            "aggregate_post_retraction_exposure_by_publication_year": dict(
                sorted(yearly_post_counts.items())
            ),
            "sampled_post_retraction_edges_for_semantic_review": len(edge_rows),
            "sample_per_source_target": args.edge_sample_per_source,
        },
        "warnings": [
            "Citation exposure is not semantic contamination.",
            "Sources are intentionally selected for high citation exposure; do not infer global averages.",
            "OpenAlex citation links are reference-matching observations and may miss printed references.",
            "Post-retraction citation timing does not establish knowledge, negligence, or misconduct by citing authors.",
            "Semantic SCF requires full-text/context adjudication of sampled edges.",
        ],
    }
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
