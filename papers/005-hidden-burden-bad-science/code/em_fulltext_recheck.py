#!/usr/bin/env python3
"""Recompute real Europe PMC full-text availability for the ARIS4C005 gap works.

`alt_databases_probe.py` first recorded `em_fulltext` as
`bool(record["isOpenAccess"]) and bool(record["fullTextUrlList"])`. Europe PMC
returns "Y"/"N" strings, so `bool("N")` is true and every hit was scored as
full-text available. Europe PMC's own full-text-in-PMC flag is `inEPMC`.

This script re-queries only the rows the probe marked `em_found` and records the
corrected flags, so the published coverage rates can separate "Europe PMC knows
the record" from "Europe PMC can show you the article". Resumable.
"""
from __future__ import annotations

import csv
import glob
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
HERE = Path(os.environ.get("ARIS4C005_SCRATCH") or (CODE_DIR / "_evidence_scratch"))
PROBE = HERE / "alt_databases_probe.jsonl"
BATCH_GLOB = "aris4c005_ai_batches/AI_A_batch_*.csv"
OUT = HERE / "em_fulltext_recheck.jsonl"
DOI_PREFIX = re.compile(r"^https?://(dx\.)?doi\.org/", re.I)
MAILTO = os.environ.get("CONTACT_EMAIL", "cuneyi@example.org")
UA = {"User-Agent": f"ARIS4C005-em-recheck/1.0 (mailto:{MAILTO})"}


def bare_doi(value: str) -> str:
    return DOI_PREFIX.sub("", (value or "").strip())


def get(url: str, tries: int = 5):
    for i in range(tries):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in (408, 429, 500, 502, 503, 504):
                return {}
        except Exception:
            pass
        time.sleep(2 * (i + 1))
    return {}


def dois_by_openalex() -> dict:
    out = {}
    for path in sorted(glob.glob(str(HERE / BATCH_GLOB))):
        with open(path, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                oid = (row.get("openalex_id") or "").rsplit("/", 1)[-1]
                doi = bare_doi(row.get("doi"))
                if oid and doi:
                    out[oid] = doi
    return out


def main() -> None:
    hits = []
    with PROBE.open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            rec = json.loads(line)
            if rec.get("em_found"):
                hits.append(rec["openalex_id"].rsplit("/", 1)[-1])
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["openalex_id"])
    todo = [oid for oid in dict.fromkeys(hits) if oid not in done]
    doi_map = dois_by_openalex()
    print(f"em_found rows: {len(set(hits))} | already checked: {len(done)} | todo: {len(todo)}", flush=True)

    with OUT.open("a", encoding="utf-8") as fh:
        for n, oid in enumerate(todo, 1):
            doi = doi_map.get(oid)
            if not doi:
                rec = {"openalex_id": oid, "doi_present": False}
            else:
                q = urllib.parse.urlencode(
                    {"query": f'DOI:"{doi}"', "format": "json",
                     "resultType": "core", "pageSize": "1"}
                )
                d = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + q) or {}
                rs = (d.get("resultList") or {}).get("result") or []
                x = rs[0] if rs else {}
                rec = {
                    "openalex_id": oid,
                    "doi_present": True,
                    "still_found": bool(x),
                    "returned_doi_matches": bool(x)
                    and bare_doi(str(x.get("doi") or "")).lower() == doi.lower(),
                    "in_epmc": x.get("inEPMC") == "Y",
                    "is_oa_flag": x.get("isOpenAccess") == "Y",
                    "has_abstract": bool(x.get("abstractText")),
                    "pmcid": x.get("pmcid"),
                }
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            if n % 50 == 0:
                print(f"  recheck {n}/{len(todo)}", flush=True)
            time.sleep(0.35)

    rows = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()]
    with_abs = sum(1 for r in rows if r.get("has_abstract"))
    in_epmc = sum(1 for r in rows if r.get("in_epmc"))
    mismatch = sum(1 for r in rows if r.get("doi_present") and not r.get("returned_doi_matches"))
    print(json.dumps({
        "checked": len(rows),
        "europepmc_abstract": with_abs,
        "europepmc_fulltext_in_epmc": in_epmc,
        "returned_doi_not_equal_requested": mismatch,
    }, indent=2))


if __name__ == "__main__":
    main()
