#!/usr/bin/env python3
"""Exact evidence-availability census for the frozen ARIS4C005 10,000-work sample.

Reads only the frozen AI batch files already pinned as a CI artifact, queries
OpenAlex for each work, and records what text an AI adjudicator could actually
be given. No verdicts are produced here.
"""
from __future__ import annotations

import csv
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
HERE = Path(os.environ.get("ARIS4C005_SCRATCH") or (CODE_DIR / "_evidence_scratch"))
BATCH_DIR = HERE / "aris4c005_ai_batches"
KEY = os.environ.get("OPENALEX_API_KEY", "")
OUT = HERE / "evidence_census.jsonl"
SUMMARY = HERE / "evidence_census_summary.json"
SELECT = ",".join(
    [
        "id",
        "doi",
        "title",
        "display_name",
        "abstract_inverted_index",
        "has_content",
        "open_access",
        "best_oa_location",
        "primary_location",
        "is_retracted",
    ]
)
UA = {"User-Agent": "ARIS4C005-evidence-census/1.0 (research audit)"}


def sample_ids() -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for path in sorted(BATCH_DIR.glob("AI_A_batch_*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                oid = (row.get("openalex_id") or "").strip()
                short = oid.rsplit("/", 1)[-1]
                if short and short not in seen:
                    seen.add(short)
                    ids.append(short)
    return ids


def get(url: str, tries: int = 8) -> dict:
    last = ""
    for i in range(tries):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code not in (429, 500, 502, 503, 504):
                raise
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}"
        time.sleep(min(120, 3 * (i + 1) + random.random() * 3))
    raise RuntimeError(f"exhausted retries ({last})")


def fetch_chunk(chunk: list[str]) -> list[dict]:
    q = urllib.parse.urlencode(
        {
            "filter": "openalex_id:" + "|".join(chunk),
            "select": SELECT,
            "per-page": str(len(chunk)),
        }
    )
    url = f"https://api.openalex.org/works?{q}"
    if KEY:
        url += f"&api_key={KEY}"
    return get(url).get("results", [])


def summarize(w: dict) -> dict:
    inv = w.get("abstract_inverted_index")
    oa = w.get("open_access") or {}
    best = w.get("best_oa_location") or {}
    prim = w.get("primary_location") or {}
    landing = prim.get("landing_page_url") or best.get("landing_page_url") or ""
    return {
        "openalex_id": (w.get("id") or "").rsplit("/", 1)[-1],
        "has_title": bool(w.get("title") or w.get("display_name")),
        "abstract_words": sum(len(v) for v in inv.values()) if inv else 0,
        "has_abstract": bool(inv),
        "has_content": bool(w.get("has_content")),
        "is_oa": bool(oa.get("is_oa")),
        "has_pdf_url": bool(best.get("pdf_url")) or str(oa.get("oa_url") or "").endswith(".pdf"),
        "has_landing_page": bool(landing),
        "oa_color": oa.get("oa_status"),
        "is_retracted": bool(w.get("is_retracted")),
    }


def main() -> None:
    ids = sample_ids()
    print(f"sample works: {len(ids)}", flush=True)
    have = set()
    if OUT.exists():
        have = {json.loads(l)["openalex_id"] for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()}
        print(f"resuming, {len(have)} already censused", flush=True)
    todo = [i for i in ids if i not in have]
    chunks = [todo[i : i + 50] for i in range(0, len(todo), 50)]
    print(f"requests remaining: {len(chunks)}", flush=True)
    done = 0
    with OUT.open("a", encoding="utf-8") as fh, ThreadPoolExecutor(max_workers=3) as ex:
        for res in ex.map(lambda c: (c, fetch_chunk(c)), chunks):
            c, results = res
            got = {summarize(w)["openalex_id"] for w in results}
            for w in results:
                fh.write(json.dumps(summarize(w), ensure_ascii=False) + "\n")
            for missing in set(c) - got:
                fh.write(json.dumps({"openalex_id": missing, "not_found": True}) + "\n")
            fh.flush()
            done += 1
            if done % 10 == 0 or done == len(chunks):
                print(f"  {done}/{len(chunks)} chunks", flush=True)
            time.sleep(0.4)

    rows = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()]
    n = len(rows)
    found = [r for r in rows if not r.get("not_found")]
    c: Counter = Counter()
    for r in found:
        c["resolved"] += 1
        for k in (
            "has_title", "has_abstract", "has_content", "is_oa", "has_pdf_url",
            "has_landing_page", "is_retracted",
        ):
            c[k] += bool(r.get(k))
        if r.get("has_abstract") and r.get("has_pdf_url"):
            c["abstract_and_pdf"] += 1
        if not r.get("has_abstract") and not r.get("has_pdf_url"):
            c["no_text_at_all"] += 1
    words = sorted(r.get("abstract_words", 0) for r in found)
    summary = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sample_rows_in_census": n,
        "not_found_in_openalex": n - len(found),
        "counts": dict(c),
        "rates": {k: round(v / max(1, len(found)), 4) for k, v in c.items() if k != "resolved"},
        "abstract_word_median": words[len(words) // 2] if words else None,
        "abstract_p10": words[len(words) // 10] if words else None,
        "oa_color": dict(Counter(r.get("oa_color") for r in found)),
        "adjudication_implication": (
            "Works with neither an abstract nor an OA PDF cannot be given any article text "
            "to an AI adjudicator under the current packet design; they must abstain with "
            "abstain_reason=EVIDENCE_UNAVAILABLE rather than be judged from metadata."
        ),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    sys.exit(main())
