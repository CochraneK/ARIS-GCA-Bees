#!/usr/bin/env python3
"""ARIS4C006 — Crossref structured family-name feasibility pilot.

Join China-affiliated OpenAlex works to Crossref by DOI and test whether Crossref
`author[].family` can serve as structured surname evidence for the surname parser.

This is a measurement pilot, not a substantive surname-effect analysis.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

OPENALEX = "https://api.openalex.org/works"
CROSSREF = "https://api.crossref.org/works/"
USER_AGENT = "ARIS4C006/0.3 structured-family feasibility pilot"
FIELD_SET = {
    20: "Economics, Econometrics and Finance",
    26: "Mathematics",
    14: "Business, Management and Accounting",
    32: "Psychology",
    27: "Medicine",
    22: "Engineering",
}
TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ'’-]+")


def fetch_json(url: str, retries: int = 3) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception:
            if attempt + 1 == retries:
                return None
            time.sleep(0.5 * (attempt + 1))
    return None


def norm(text: str | None) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z]", "", text.lower())


def tokens(text: str | None) -> list[str]:
    return [norm(x) for x in TOKEN_RE.findall(text or "") if norm(x)]


def openalex_field_works(field_id: int, year: int, target_doi_works: int):
    cursor = "*"
    yielded = 0
    while yielded < target_doi_works:
        params = {
            "filter": ",".join([
                "authorships.institutions.country_code:CN",
                f"topics.field.id:{field_id}",
                f"from_publication_date:{year}-01-01",
                f"to_publication_date:{year}-12-31",
            ]),
            "select": "id,doi,publication_year,authorships",
            "per-page": 100,
            "cursor": cursor,
        }
        api_key = os.getenv("OPENALEX_API_KEY")
        mailto = os.getenv("OPENALEX_MAILTO")
        if api_key:
            params["api_key"] = api_key
        if mailto:
            params["mailto"] = mailto
        payload = fetch_json(OPENALEX + "?" + urllib.parse.urlencode(params))
        if not payload:
            break
        results = payload.get("results", [])
        if not results:
            break
        for work in results:
            doi = work.get("doi")
            if doi and len(work.get("authorships") or []) >= 2:
                yield work
                yielded += 1
                if yielded >= target_doi_works:
                    break
        cursor = payload.get("meta", {}).get("next_cursor")
        if not cursor:
            break
        time.sleep(0.1)


def crossref_record(doi_url: str) -> dict | None:
    doi = doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    url = CROSSREF + urllib.parse.quote(doi, safe="")
    payload = fetch_json(url)
    if not payload:
        return None
    return payload.get("message") or None


def authorship_is_cn(authorship: dict) -> bool:
    for inst in authorship.get("institutions") or []:
        if inst.get("country_code") == "CN":
            return True
    return "CN" in (authorship.get("countries") or [])


def compare_work(work: dict, cr: dict) -> tuple[dict, list[dict]]:
    oa = work.get("authorships") or []
    ca = cr.get("author") or []
    row = {
        "openalex_id": work.get("id"),
        "doi": work.get("doi"),
        "oa_author_count": len(oa),
        "crossref_author_count": len(ca),
        "same_author_count": int(len(oa) == len(ca) and len(oa) > 0),
        "crossref_has_authors": int(bool(ca)),
        "all_crossref_family_present": int(bool(ca) and all(a.get("family") for a in ca)),
    }

    author_rows: list[dict] = []
    if not row["same_author_count"]:
        return row, author_rows

    for pos, (o, c) in enumerate(zip(oa, ca), start=1):
        raw = o.get("raw_author_name") or (o.get("author") or {}).get("display_name") or ""
        family = c.get("family") or ""
        given = c.get("given") or ""
        ts = tokens(raw)
        nf = norm(family)
        first_match = int(bool(ts and nf and ts[0] == nf))
        last_match = int(bool(ts and nf and ts[-1] == nf))
        anywhere_match = int(bool(nf and nf in ts))
        structured_full = norm((given or "") + (family or ""))
        raw_full = norm(raw)
        full_component_match = int(bool(structured_full and raw_full and sorted([norm(given), nf]) == sorted([t for t in ts if t]))) if len(ts) == 2 else 0

        author_rows.append({
            "position": pos,
            "is_cn_authorship": int(authorship_is_cn(o)),
            "raw_name": raw,
            "crossref_given": given,
            "crossref_family": family,
            "first_token_family_match": first_match,
            "last_token_family_match": last_match,
            "family_token_anywhere_match": anywhere_match,
            "two_token_component_match": full_component_match,
            "openalex_orcid": (o.get("author") or {}).get("orcid") or "",
        })
    return row, author_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarize(field_id: int, field_name: str, works: list[dict], authors: list[dict], requested: int) -> dict:
    same = [w for w in works if w["same_author_count"]]
    cn = [a for a in authors if a["is_cn_authorship"]]
    noncn = [a for a in authors if not a["is_cn_authorship"]]

    def rate(items: list[dict], key: str) -> float | None:
        return sum(x[key] for x in items) / len(items) if items else None

    return {
        "field_id": field_id,
        "field_name": field_name,
        "requested_doi_works": requested,
        "crossref_records_found": len(works),
        "same_author_count_works": len(same),
        "same_author_count_rate": len(same) / len(works) if works else None,
        "all_family_present_rate_among_found": sum(w["all_crossref_family_present"] for w in works) / len(works) if works else None,
        "aligned_author_rows": len(authors),
        "aligned_cn_author_rows": len(cn),
        "cn_family_matches_any_token": rate(cn, "family_token_anywhere_match"),
        "cn_family_matches_first_token": rate(cn, "first_token_family_match"),
        "cn_family_matches_last_token": rate(cn, "last_token_family_match"),
        "noncn_family_matches_any_token": rate(noncn, "family_token_anywhere_match"),
        "noncn_family_matches_first_token": rate(noncn, "first_token_family_match"),
        "noncn_family_matches_last_token": rate(noncn, "last_token_family_match"),
        "confirmatory_use_allowed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--per-field", type=int, default=30)
    parser.add_argument("--outdir", default="data/pilot/crossref")
    args = parser.parse_args()

    summary_rows: list[dict] = []
    global_works: list[dict] = []
    global_authors: list[dict] = []

    for field_id, field_name in FIELD_SET.items():
        work_rows: list[dict] = []
        author_rows: list[dict] = []
        for work in openalex_field_works(field_id, args.year, args.per_field):
            cr = crossref_record(work["doi"])
            if not cr:
                continue
            wrow, arows = compare_work(work, cr)
            wrow["field_id"] = field_id
            wrow["field_name"] = field_name
            for a in arows:
                a["field_id"] = field_id
                a["field_name"] = field_name
                a["doi"] = work["doi"]
            work_rows.append(wrow)
            author_rows.extend(arows)
            time.sleep(0.08)

        summary_rows.append(summarize(field_id, field_name, work_rows, author_rows, args.per_field))
        global_works.extend(work_rows)
        global_authors.extend(author_rows)

    outdir = Path(args.outdir)
    write_csv(outdir / f"crossref_family_summary_{args.year}.csv", summary_rows)

    # Keep only aggregate public-safe outputs in the standard artifact. The raw
    # name-level rows are intentionally not written by this pilot.
    manifest = {
        "script": "03_crossref_structured_family_pilot.py",
        "year": args.year,
        "per_field_requested": args.per_field,
        "crossref_records_found_total": len(global_works),
        "aligned_author_rows_total": len(global_authors),
        "confirmatory_use_allowed": False,
        "purpose": "Assess Crossref structured family-name coverage/alignment as parser evidence.",
        "privacy": "Only aggregate summaries are persisted; raw author-name comparison rows are not written.",
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"manifest_{args.year}.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    for row in summary_rows:
        print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
