#!/usr/bin/env python3
"""Enrich frozen candidate rows with Wikidata identifier *leads*.

This script fetches ORCID (P496) and OpenAlex ID (P10283) from Wikidata for
already-selected candidates. Values are leads, not accepted identity matches:
OpenAlex author IDs can change and must be validated against the OpenAlex record.

Input: candidate CSV with person_id,wikidata_qid.
Output: same rows with orcid/openalex_author_id populated when available, plus
resolver metadata columns.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

WDQS = "https://query.wikidata.org/sparql"
USER_AGENT = "ARIS4C004/0.1 (historical science network feasibility study)"


def chunks(values: list[str], n: int):
    for i in range(0, len(values), n):
        yield values[i : i + n]


def query_batch(qids: list[str], retries: int = 4) -> dict[str, dict[str, str]]:
    values = " ".join(f"wd:{qid}" for qid in qids)
    sparql = f"""
SELECT ?item ?orcid ?openalex WHERE {{
  VALUES ?item {{ {values} }}
  OPTIONAL {{ ?item wdt:P496 ?orcid. }}
  OPTIONAL {{ ?item wdt:P10283 ?openalex. }}
}}
""".strip()
    params = urllib.parse.urlencode({"query": sparql, "format": "json"})
    url = f"{WDQS}?{params}"
    for attempt in range(retries + 1):
        request = urllib.request.Request(
            url,
            headers={"Accept": "application/sparql-results+json", "User-Agent": USER_AGENT},
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except (urllib.error.HTTPError, urllib.error.URLError):
            if attempt >= retries:
                raise
            time.sleep(min(2**attempt, 20))

    out: dict[str, dict[str, str]] = {}
    for binding in payload.get("results", {}).get("bindings", []):
        item = binding.get("item", {}).get("value", "")
        qid = item.rsplit("/", 1)[-1]
        rec = out.setdefault(qid, {"orcid": "", "openalex_author_id": ""})
        if binding.get("orcid", {}).get("value"):
            rec["orcid"] = binding["orcid"]["value"]
        if binding.get("openalex", {}).get("value"):
            value = binding["openalex"]["value"]
            # Preserve Wikidata value as a lead; the OpenAlex stage validates it.
            rec["openalex_author_id"] = value
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=50)
    args = parser.parse_args()

    with args.input_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = list(reader.fieldnames or [])

    if "wikidata_qid" not in fields:
        raise SystemExit("input CSV needs wikidata_qid")
    qids = sorted({(row.get("wikidata_qid") or "").strip() for row in rows if row.get("wikidata_qid")})
    leads: dict[str, dict[str, str]] = {}
    for batch in chunks(qids, max(1, min(args.batch_size, 100))):
        leads.update(query_batch(batch))
        time.sleep(0.2)

    for extra in ("wikidata_identifier_lookup", "wikidata_openalex_needs_validation"):
        if extra not in fields:
            fields.append(extra)
    for field in ("orcid", "openalex_author_id"):
        if field not in fields:
            fields.append(field)

    found_orcid = found_openalex = 0
    for row in rows:
        qid = (row.get("wikidata_qid") or "").strip()
        lead = leads.get(qid, {})
        if lead.get("orcid") and not (row.get("orcid") or "").strip():
            row["orcid"] = lead["orcid"]
            found_orcid += 1
        if lead.get("openalex_author_id") and not (row.get("openalex_author_id") or "").strip():
            row["openalex_author_id"] = lead["openalex_author_id"]
            found_openalex += 1
        row["wikidata_identifier_lookup"] = "queried"
        row["wikidata_openalex_needs_validation"] = "true" if row.get("openalex_author_id") else ""

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(
        json.dumps(
            {
                "candidates": len(rows),
                "wikidata_qids": len(qids),
                "new_orcid_leads": found_orcid,
                "new_openalex_id_leads": found_openalex,
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
