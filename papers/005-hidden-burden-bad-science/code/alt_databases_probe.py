#!/usr/bin/env python3
"""Can other research databases cover the ARIS4C005 works OpenAlex cannot?

Targets exactly the sample rows with neither an OpenAlex abstract nor an OpenAlex
OA-PDF URL and measures what free, researcher-facing sources can add:

  * Crossref        - publisher-deposited abstract, keyed on DOI; plus a
                      bibliographic title search for rows that carry no DOI at all
  * Europe PMC      - abstract and (for OA biomedicine) full text, keyed on DOI
  * Unpaywall       - any OA PDF location, keyed on DOI

Semantic Scholar was probed first and is excluded: its unauthenticated batch and
single-record endpoints returned 400/429 from this host, so it is only usable with
an API key. Writes a resumable per-work JSONL and an aggregate summary.
"""
from __future__ import annotations

import csv
import difflib
import json
import os
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
HERE = Path(os.environ.get("ARIS4C005_SCRATCH") or (CODE_DIR / "_evidence_scratch"))
BATCH_DIR = HERE / "aris4c005_ai_batches"
CENSUS = HERE / "evidence_census.jsonl"
OUT = HERE / "alt_databases_probe.jsonl"
SUMMARY = HERE / "alt_databases_summary.json"
MAILTO = os.environ.get("CONTACT_EMAIL", "cuneyi@example.org")
UA = {"User-Agent": f"ARIS4C005-alt-db-probe/1.0 (mailto:{MAILTO})"}


DOI_PREFIX = re.compile(r"^https?://(dx\.)?doi\.org/", re.I)


def bare_doi(value: str) -> str:
    """Europe PMC indexes the bare DOI; Crossref/Unpaywall tolerate both forms.

    Passing the https://doi.org/ URL to Europe PMC silently returns zero hits,
    which is how the first run of this probe reported 0% coverage.
    """
    return DOI_PREFIX.sub("", (value or "").strip())


def get(url: str, tries: int = 5):
    last = ""
    for i in range(tries):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (400, 401, 404, 422):
                return None
            if e.code not in (408, 429, 500, 502, 503, 504):
                raise
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}"
        time.sleep(min(60, 2.5 * (i + 1) + random.random() * 2))
    print(f"    gave up on {url[:70]} ({last})", flush=True)
    return None


def targets() -> list[dict]:
    cens = {}
    for line in CENSUS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            cens[r["openalex_id"]] = r
    gap = {k for k, v in cens.items() if not v.get("has_abstract") and not v.get("has_pdf_url")}
    rows = {}
    for i in range(1, 41):
        with (BATCH_DIR / f"AI_A_batch_{i:03d}.csv").open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                oid = (row.get("openalex_id") or "").rsplit("/", 1)[-1]
                if oid in gap and oid not in rows:
                    rows[oid] = {
                        "openalex_id": oid,
                        "doi": bare_doi(row.get("doi")),
                        "title": (row.get("title") or "").strip(),
                        "year": row.get("publication_year") or "",
                    }
    # batch files carry no title column; pull titles from OpenAlex in one pass
    return list(rows.values())


def titles_for(ids: list[str]) -> dict[str, str]:
    out = {}
    key = os.environ.get("OPENALEX_API_KEY", "")
    for i in range(0, len(ids), 50):
        chunk = ids[i : i + 50]
        q = urllib.parse.urlencode(
            {"filter": "openalex_id:" + "|".join(chunk), "select": "id,title", "per-page": "50"}
        )
        url = f"https://api.openalex.org/works?{q}"
        if key:
            url += f"&api_key={key}"
        req = urllib.request.Request(url, headers={"User-Agent": UA["User-Agent"]})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                for w in json.load(r).get("results", []):
                    out[(w.get("id") or "").rsplit("/", 1)[-1]] = w.get("title") or ""
        except Exception as e:  # noqa: BLE001
            print(f"    title fetch skipped a chunk ({type(e).__name__})", flush=True)
        time.sleep(0.2)
    return out


def crossref_work(doi: str) -> dict:
    # /works/{doi} does not accept select; the full message object is small enough
    d = get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}") or {}
    return d.get("message") or {}


def crossref_search(title: str) -> dict:
    q = urllib.parse.urlencode(
        {
            "query.bibliographic": title[:220],
            "select": "DOI,title,abstract,container-title",
            "rows": "1",
            "mailto": MAILTO,
        }
    )
    d = get(f"https://api.crossref.org/works?{q}") or {}
    items = (d.get("message") or {}).get("items") or []
    return items[0] if items else {}


def europepmc(doi: str) -> dict:
    q = urllib.parse.urlencode(
        {"query": f'DOI:"{doi}"', "format": "json", "resultType": "core", "pageSize": "1"}
    )
    d = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{q}") or {}
    rs = (d.get("resultList") or {}).get("result") or []
    return rs[0] if rs else {}


def unpaywall(doi: str) -> dict:
    return get(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={MAILTO}") or {}


def norm_title(s: str) -> str:
    # Unicode-aware: an ASCII-only filter would score every Cyrillic/CJK title as
    # a 0.0 non-match purely because of script.
    return " ".join(re.sub(r"[^\w]+", " ", (s or "").lower(), flags=re.UNICODE).split())


def title_match(want: str, got: str) -> tuple[bool, float]:
    """Is the Crossref top hit the same work? query.bibliographic is fuzzy, so a
    returned DOI is not evidence about the target work unless the titles agree."""
    a, b = norm_title(want), norm_title(got)
    if not a or not b:
        return False, 0.0
    return a == b, difflib.SequenceMatcher(None, a, b).ratio()


def record(t: dict, cr: dict, em: dict, up: dict, route: str) -> dict:
    best = up.get("best_oa_location") or {}
    return {
        "openalex_id": t["openalex_id"],
        "route": route,
        "has_doi": bool(t.get("doi")),
        "cr_found": bool(cr.get("DOI")),
        "cr_abstract": bool(cr.get("abstract")),
        "cr_abstract_words": len(str(cr.get("abstract", "")).split()) if cr.get("abstract") else 0,
        "em_found": bool(em),
        "em_abstract": bool(em.get("abstractText")),
        "em_in_epmc": em.get("inEPMC") == "Y",
        "em_is_oa": em.get("isOpenAccess") == "Y",
        "em_fulltext": em.get("inEPMC") == "Y",
        "em_pmcid": em.get("pmcid"),
        "up_found": bool(up.get("doi")),
        "up_pdf": bool(best.get("url_for_pdf")),
    }


def main() -> None:
    todo = targets()
    have = set()
    if OUT.exists():
        have = {
            json.loads(l)["openalex_id"]
            for l in OUT.read_text(encoding="utf-8").splitlines()
            if l.strip()
        }
        print(f"resuming, {len(have)} already probed", flush=True)
    todo = [t for t in todo if t["openalex_id"] not in have]
    tit = titles_for([t["openalex_id"] for t in todo])
    for t in todo:
        t["title"] = tit.get(t["openalex_id"], "") or t.get("title", "")
    with_doi = [t for t in todo if t["doi"]]
    no_doi = [t for t in todo if not t["doi"] and t["title"]]
    print(
        f"gap works: {len(todo)}  | with DOI: {len(with_doi)}  | title-only: {len(no_doi)}",
        flush=True,
    )

    def doi_row(t: dict) -> dict:
        return record(
            t, crossref_work(t["doi"]), europepmc(t["doi"]), unpaywall(t["doi"]), "doi"
        )

    def title_row(t: dict) -> dict:
        hit = crossref_search(t["title"])
        doi = hit.get("DOI") or ""
        rec = record({**t, "doi": doi}, hit, {}, {}, "title_search")
        rec["title_search_returned_doi"] = bool(doi)
        got = (hit.get("title") or [""])[0] if isinstance(hit.get("title"), list) else ""
        exact, ratio = title_match(t["title"], got)
        rec["returned_title"] = got[:300]
        rec["title_exact_match"] = exact
        rec["title_similarity"] = round(ratio, 3)
        if doi:
            em = europepmc(doi)
            up = unpaywall(doi)
            rec["em_found"] = bool(em)
            rec["em_abstract"] = bool(em.get("abstractText"))
            rec["em_in_epmc"] = em.get("inEPMC") == "Y"
            rec["em_is_oa"] = em.get("isOpenAccess") == "Y"
            rec["em_fulltext"] = em.get("inEPMC") == "Y"
            rec["up_found"] = bool(up.get("doi"))
            rec["up_pdf"] = bool((up.get("best_oa_location") or {}).get("url_for_pdf"))
        return rec

    with OUT.open("a", encoding="utf-8") as fh, ThreadPoolExecutor(max_workers=6) as ex:
        for label, work, items in (("doi", doi_row, with_doi), ("title", title_row, no_doi)):
            total = len(items)
            done = 0
            for rec in ex.map(work, items):
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                done += 1
                if done % 100 == 0 or done == total:
                    fh.flush()
                    print(f"  {label} route {done}/{total}", flush=True)

    agg: dict[str, dict] = {}
    for line in OUT.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            agg.setdefault(r["openalex_id"], {}).update(r)
    keys = ("cr_abstract", "em_abstract", "em_fulltext", "up_pdf")
    per = {k: sum(1 for r in agg.values() if r.get(k)) for k in keys}
    per["cr_found"] = sum(1 for r in agg.values() if r.get("cr_found"))
    per["title_search_returned_doi"] = sum(1 for r in agg.values() if r.get("title_search_returned_doi"))
    either = sum(1 for r in agg.values() if any(r.get(k) for k in keys))
    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gap_works": len(agg),
        "gap_share_of_10000_sample": round(len(agg) / 10000, 4),
        "gap_works_with_doi": sum(1 for r in agg.values() if r.get("has_doi")),
        "per_source_hits": per,
        "recovered_by_any_free_alt_db": either,
        "still_unrecoverable_free": len(agg) - either,
        "note_semantic_scholar": (
            "Excluded: unauthenticated Semantic Scholar endpoints returned HTTP 400/429 "
            "from this host; re-probe with an API key before ruling it out."
        ),
        "reading": (
            "gap_works have no OpenAlex abstract and no OpenAlex OA-PDF. "
            "DOI-keyed sources can only reach gap_works_with_doi; the title-search route "
            "measures whether Crossref can even mint a DOI handle for the remainder."
        ),
    }
    SUMMARY.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
