#!/usr/bin/env python3
"""Build a real, probability-traceable Pilot B seed sample for ARIS4C005.

Two independent selection mechanisms are combined:
A) a reproducible population-random OpenAlex sample from the frozen target universe;
B) stratified enrichment from Retraction Watch screening strata, after DOI resolution
   into the same OpenAlex target universe.

For a work in enrichment stratum s:
    pi_i = 1 - (1 - p_random) * (1 - p_enrich_s)

For a work outside all enrichment strata:
    pi_i = p_random

This output is a sampling/adjudication frame, NOT a prevalence estimate and NOT
an accusation list.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import os
import random
import re
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

BASE_URL = "https://api.openalex.org/works"
UA = "ARIS4C005/0.1 meta-research pilot"

FLAG_COLS = [
    "e1s_narrow_auto",
    "e1m_strong_auto",
    "e1p_strong_auto",
    "paper_mill_signal",
    "e3_error_signal",
    "manual_scientific_review",
    "manual_process_review",
    "context_only_reasons",
    "manual_review_required",
]


def norm_doi(raw: str | None) -> str | None:
    if not raw:
        return None
    value = raw.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix):]
    if not value or value in {"unavailable", "none", "nan", "0"}:
        return None
    return value.strip()


def doi_url(doi: str) -> str:
    return f"https://doi.org/{doi}"


def parse_year(raw: str | None) -> int | None:
    if not raw:
        return None
    text = raw.strip()
    for fmt in ("%m/%d/%Y %H:%M", "%m/%d/%Y", "%Y-%m-%d", "%Y"):
        try:
            return dt.datetime.strptime(text, fmt).year
        except ValueError:
            pass
    match = re.search(r"(?<!\d)(1[6-9]\d{2}|20\d{2}|2100)(?!\d)", text)
    return int(match.group(1)) if match else None


def parse_int_flag(value: str | None) -> int:
    try:
        return 1 if int(value or 0) else 0
    except ValueError:
        return 0


def openalex_request(params: dict[str, Any], retries: int = 4) -> dict[str, Any]:
    params = dict(params)
    api_key = os.getenv("OPENALEX_API_KEY", "").strip()
    mailto = os.getenv("OPENALEX_MAILTO", "").strip()
    if api_key:
        params["api_key"] = api_key
    if mailto:
        params["mailto"] = mailto

    url = BASE_URL + "?" + urllib.parse.urlencode(params, safe="|,:/")
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    delay = 1.0
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception:
            if attempt + 1 >= retries:
                raise
            time.sleep(delay)
            delay *= 2
    raise AssertionError("unreachable")


def target_filter(start: int, end: int) -> str:
    return f"publication_year:{start}-{end},type:article|review"


def target_universe_count(start: int, end: int, corpus: str) -> int:
    data = openalex_request(
        {
            "filter": target_filter(start, end),
            "corpus": corpus,
            "per_page": 1,
            "select": "id",
        }
    )
    return int(data["meta"]["count"])


def random_openalex_sample(
    start: int,
    end: int,
    corpus: str,
    n: int,
    seed: int,
) -> list[dict[str, Any]]:
    if not (0 <= n <= 10000):
        raise ValueError("OpenAlex random sample size must be between 0 and 10,000")
    if n == 0:
        return []

    per_page = 100
    pages = math.ceil(n / per_page)
    output: list[dict[str, Any]] = []
    for page in range(1, pages + 1):
        data = openalex_request(
            {
                "filter": target_filter(start, end),
                "corpus": corpus,
                "sample": n,
                "seed": seed,
                "per_page": per_page,
                "page": page,
                "select": "id,doi,publication_year,type,primary_topic",
            }
        )
        output.extend(data.get("results", []))

    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for work in output:
        work_id = str(work.get("id") or "")
        if work_id and work_id not in seen:
            seen.add(work_id)
            deduped.append(work)
    return deduped[:n]


def collapse_rw(path: Path, start: int, end: int) -> dict[str, dict[str, Any]]:
    papers: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            doi = norm_doi(row.get("OriginalPaperDOI"))
            year = parse_year(row.get("OriginalPaperDate"))
            if doi is None or year is None or not (start <= year <= end):
                continue
            paper = papers.setdefault(
                doi,
                {
                    "doi": doi,
                    "original_year": year,
                    "natures": set(),
                    **{flag: 0 for flag in FLAG_COLS},
                },
            )
            nature = (row.get("RetractionNature") or "").strip()
            if nature:
                paper["natures"].add(nature)
            for flag in FLAG_COLS:
                paper[flag] = max(paper[flag], parse_int_flag(row.get(flag)))
    return papers


def rw_stratum(paper: dict[str, Any]) -> str | None:
    """Mutually exclusive enrichment strata, ordered by scientific specificity."""
    if paper.get("e1s_narrow_auto"):
        return "rw_e1s_narrow"
    if paper.get("paper_mill_signal"):
        return "rw_paper_mill"
    if paper.get("e3_error_signal"):
        return "rw_major_error"
    if "Expression of concern" in paper.get("natures", set()):
        return "rw_expression_of_concern"
    if paper.get("e1p_strong_auto"):
        return "rw_process_integrity"
    return None


def chunks(items: list[str], size: int = 100) -> Iterable[list[str]]:
    for index in range(0, len(items), size):
        yield items[index:index + size]


def bulk_lookup_dois(
    dois: list[str],
    start: int,
    end: int,
    corpus: str,
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for batch in chunks(dois, 100):
        filter_expr = "doi:" + "|".join(doi_url(doi) for doi in batch)
        data = openalex_request(
            {
                "filter": filter_expr,
                "corpus": corpus,
                "per_page": 100,
                "select": "id,doi,publication_year,type,primary_topic",
            }
        )
        for work in data.get("results", []):
            doi = norm_doi(work.get("doi"))
            year = work.get("publication_year")
            if (
                doi
                and work.get("type") in {"article", "review"}
                and isinstance(year, int)
                and start <= year <= end
            ):
                output[doi] = work
    return output


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


def stable_paper_id(openalex_id: str) -> str:
    return "P" + hashlib.sha256(openalex_id.encode("utf-8")).hexdigest()[:16]


def inclusion_probability(p_random: float, p_enrich: float) -> float:
    return 1.0 - (1.0 - p_random) * (1.0 - p_enrich)


def parse_targets(items: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Target must be stratum=n, got {item!r}")
        key, raw = item.split("=", 1)
        result[key.strip()] = int(raw)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("rw_classified_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("provenance_json", type=Path)
    parser.add_argument("--start", type=int, default=2015)
    parser.add_argument("--end", type=int, default=2020)
    parser.add_argument("--corpus", default="core", choices=["core", "expansion", "all"])
    parser.add_argument("--random-n", type=int, default=600)
    parser.add_argument("--seed", type=int, default=20260918)
    parser.add_argument("--target", action="append", default=[])
    args = parser.parse_args()

    targets = {
        "rw_e1s_narrow": 200,
        "rw_paper_mill": 200,
        "rw_major_error": 150,
        "rw_expression_of_concern": 100,
        "rw_process_integrity": 150,
    }
    targets.update(parse_targets(args.target))

    denominator = target_universe_count(args.start, args.end, args.corpus)
    p_random = min(1.0, args.random_n / denominator)

    rw = collapse_rw(args.rw_classified_csv, args.start, args.end)
    raw_strata: dict[str, list[str]] = defaultdict(list)
    for doi, paper in rw.items():
        stratum = rw_stratum(paper)
        if stratum:
            raw_strata[stratum].append(doi)

    candidate_dois = sorted({doi for values in raw_strata.values() for doi in values})
    resolved = bulk_lookup_dois(candidate_dois, args.start, args.end, args.corpus)

    resolved_strata: dict[str, list[str]] = defaultdict(list)
    for stratum, dois in raw_strata.items():
        resolved_strata[stratum] = sorted({doi for doi in dois if doi in resolved})

    rng = random.Random(args.seed)
    p_enrich_by_stratum: dict[str, float] = {}
    enrichment_selected: dict[str, str] = {}
    for stratum, population in sorted(resolved_strata.items()):
        target_n = min(max(targets.get(stratum, 0), 0), len(population))
        p_enrich_by_stratum[stratum] = (
            target_n / len(population) if population else 0.0
        )
        chosen = (
            population
            if target_n == len(population)
            else rng.sample(population, target_n)
        )
        for doi in chosen:
            enrichment_selected[doi] = stratum

    random_works = random_openalex_sample(
        args.start, args.end, args.corpus, args.random_n, args.seed
    )

    selected: dict[str, dict[str, Any]] = {}
    for work in random_works:
        work_id = str(work.get("id") or "")
        if work_id:
            selected[work_id] = {
                "work": work,
                "selected_random": True,
                "selected_enrich": False,
            }

    for doi, stratum in enrichment_selected.items():
        work = resolved[doi]
        work_id = str(work["id"])
        record = selected.setdefault(
            work_id,
            {"work": work, "selected_random": False, "selected_enrich": False},
        )
        record["selected_enrich"] = True
        record["enrichment_stratum"] = stratum

    doi_to_stratum: dict[str, str] = {}
    for stratum, dois in resolved_strata.items():
        for doi in dois:
            doi_to_stratum[doi] = stratum

    rows: list[dict[str, Any]] = []
    for work_id, record in selected.items():
        work = record["work"]
        doi = norm_doi(work.get("doi"))
        stratum = doi_to_stratum.get(doi or "")
        p_enrich = p_enrich_by_stratum.get(stratum or "", 0.0)
        pi = inclusion_probability(p_random, p_enrich)
        if pi <= 0:
            raise AssertionError("Selected work has zero inclusion probability")

        domain, field, subfield = topic_fields(work)
        selected_random = bool(record.get("selected_random"))
        selected_enrich = bool(record.get("selected_enrich"))
        if selected_random and selected_enrich:
            selected_via = "population_random+rw_enrichment"
        elif selected_random:
            selected_via = "population_random"
        else:
            selected_via = "rw_enrichment"

        rw_paper = rw.get(doi or "", {})
        rows.append(
            {
                "paper_id": stable_paper_id(work_id),
                "openalex_id": work_id,
                "doi": doi or "",
                "publication_year": work.get("publication_year") or "",
                "work_type": work.get("type") or "",
                "primary_domain": domain,
                "primary_field": field,
                "primary_subfield": subfield,
                "selected_via": selected_via,
                "rw_enrichment_stratum": stratum or "",
                "det_formal_retraction": int(
                    "Retraction" in rw_paper.get("natures", set())
                ),
                "det_expression_of_concern": int(
                    "Expression of concern" in rw_paper.get("natures", set())
                ),
                "det_e1s_narrow_reason": int(
                    rw_paper.get("e1s_narrow_auto", 0)
                ),
                "det_paper_mill_high_specificity": int(
                    rw_paper.get("paper_mill_signal", 0)
                ),
                "det_e3_major_error": int(rw_paper.get("e3_error_signal", 0)),
                "det_process_integrity": int(
                    rw_paper.get("e1p_strong_auto", 0)
                ),
                "aris_pi_random": f"{p_random:.12g}",
                "aris_pi_enrich": f"{p_enrich:.12g}",
                "aris_inclusion_probability": f"{pi:.12g}",
                "aris_design_weight": f"{1.0 / pi:.12g}",
                "aris_sampling_seed": args.seed,
            }
        )

    rows.sort(key=lambda row: row["paper_id"])
    fields = list(rows[0].keys()) if rows else []
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    provenance = {
        "classification": "PILOT_B_SEED_SAMPLE_NOT_PREVALENCE_ESTIMATE",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "openalex_target": {
            "start": args.start,
            "end": args.end,
            "types": ["article", "review"],
            "corpus": args.corpus,
            "denominator": denominator,
            "random_n_requested": args.random_n,
            "random_n_resolved_unique": len(
                {str(work.get("id")) for work in random_works if work.get("id")}
            ),
            "p_random": p_random,
            "seed": args.seed,
        },
        "rw_enrichment": {
            "raw_unique_candidate_dois": len(candidate_dois),
            "resolved_target_universe_dois": len(resolved),
            "raw_stratum_sizes": {
                key: len(set(values)) for key, values in raw_strata.items()
            },
            "resolved_stratum_sizes": {
                key: len(values) for key, values in resolved_strata.items()
            },
            "targets": targets,
            "p_enrich_by_stratum": p_enrich_by_stratum,
        },
        "sample": {
            "unique_selected_works": len(rows),
            "selected_via_counts": dict(
                Counter(row["selected_via"] for row in rows)
            ),
            "sample_stratum_counts": dict(
                Counter(row["rw_enrichment_stratum"] or "none" for row in rows)
            ),
        },
        "warnings": [
            "Retraction Watch/OpenAlex signals are screening variables, not adjudicated truth.",
            "The population-random component is required for prevalence inference.",
            "No nationality, institution, or language feature is used as a suspicion detector.",
            "This seed sample cannot identify latent prevalence without manual adjudication and calibrated detector performance.",
        ],
    }
    args.provenance_json.parent.mkdir(parents=True, exist_ok=True)
    args.provenance_json.write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(provenance, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
