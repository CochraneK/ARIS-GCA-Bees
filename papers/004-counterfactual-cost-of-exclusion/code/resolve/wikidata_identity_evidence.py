#!/usr/bin/env python3
"""Fetch Wikidata authority/bibliographic context for ARIS4C004 identity review.

This script is deliberately mental-health blind. It retrieves identity-relevant
context for already-frozen candidates so reviewers can evaluate OpenAlex records
against independent authority evidence.

Wikidata is a lead/context source, not final identity truth. No retrieved claim
automatically creates VERIFIED_SINGLE/VERIFIED_CLUSTER.
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
from typing import Any, Iterable

API = "https://www.wikidata.org/w/api.php"
USER_AGENT = "ARIS4C004/0.1 historical identity review"

ENTITY_PROPERTIES = {
    "P106": "occupations",
    "P101": "fields_of_work",
    "P108": "employers",
    "P69": "educated_at",
    "P800": "notable_works",
    "P463": "member_of",
    "P512": "academic_degrees",
    "P166": "awards",
    "P27": "citizenships",
}
STRING_PROPERTIES = {
    "P496": "orcid",
    "P214": "viaf",
    "P213": "isni",
    "P227": "gnd",
    "P244": "loc",
}


def chunks(values: list[str], n: int = 25) -> Iterable[list[str]]:
    for i in range(0, len(values), n):
        yield values[i : i + n]


def request_json(params: dict[str, str], retries: int = 7) -> dict[str, Any]:
    """Request Wikidata with explicit 429/5xx backoff.

    Identity review is batch work rather than latency-sensitive work, so obeying
    Retry-After and backing off conservatively is preferable to silently losing
    authority evidence after a transient rate limit.
    """
    params = dict(params)
    params.update({"format": "json", "formatversion": "2"})
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if not retryable or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After") if exc.headers else None
            try:
                delay = float(retry_after) if retry_after else 0.0
            except ValueError:
                delay = 0.0
            if delay <= 0:
                delay = min(2 ** (attempt + 1), 60)
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError):
            if attempt >= retries:
                raise
            time.sleep(min(2 ** (attempt + 1), 60))
    raise RuntimeError("unreachable retry loop")


def fetch_entities(qids: list[str], languages: str = "en|de|fr|es|zh") -> dict[str, Any]:
    out: dict[str, Any] = {}
    for batch in chunks(qids):
        payload = request_json(
            {
                "action": "wbgetentities",
                "ids": "|".join(batch),
                "props": "labels|aliases|claims|descriptions",
                "languages": languages,
                "languagefallback": "1",
            }
        )
        entity_payload = payload.get("entities", {})
        if isinstance(entity_payload, dict):
            entity_iter = entity_payload.values()
        elif isinstance(entity_payload, list):
            entity_iter = entity_payload
        else:
            entity_iter = []
        for entity in entity_iter:
            if isinstance(entity, dict) and entity.get("id"):
                out[entity["id"]] = entity
        time.sleep(0.35)
    return out


def claim_entity_ids(entity: dict[str, Any], prop: str) -> list[str]:
    values: list[str] = []
    for claim in (entity.get("claims") or {}).get(prop, []):
        mainsnak = claim.get("mainsnak") or {}
        datavalue = mainsnak.get("datavalue") or {}
        value = datavalue.get("value")
        if isinstance(value, dict) and value.get("id"):
            values.append(str(value["id"]))
    return sorted(set(values))


def claim_strings(entity: dict[str, Any], prop: str) -> list[str]:
    values: list[str] = []
    for claim in (entity.get("claims") or {}).get(prop, []):
        mainsnak = claim.get("mainsnak") or {}
        datavalue = mainsnak.get("datavalue") or {}
        value = datavalue.get("value")
        if isinstance(value, str) and value.strip():
            values.append(value.strip())
    return sorted(set(values))


def first_text(mapping: dict[str, Any] | None) -> str:
    mapping = mapping or {}
    for lang in ("en", "de", "fr", "es", "zh"):
        item = mapping.get(lang)
        if item and item.get("value"):
            return str(item["value"])
    for item in mapping.values():
        if item and item.get("value"):
            return str(item["value"])
    return ""


def label_record(qid: str, entity: dict[str, Any] | None) -> dict[str, str]:
    entity = entity or {}
    return {
        "qid": qid,
        "label": first_text(entity.get("labels")),
        "description": first_text(entity.get("descriptions")),
    }


def read_candidates(path: Path, max_candidates: int | None) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if max_candidates is not None:
        rows = rows[:max_candidates]
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidates_csv", type=Path)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--max-candidates", type=int, default=30)
    args = parser.parse_args()

    rows = read_candidates(args.candidates_csv, args.max_candidates)
    qids = [
        (row.get("wikidata_qid") or "").strip()
        for row in rows
        if (row.get("wikidata_qid") or "").strip()
    ]
    entities = fetch_entities(sorted(set(qids)))

    linked_qids: set[str] = set()
    for qid in qids:
        entity = entities.get(qid, {})
        for prop in ENTITY_PROPERTIES:
            linked_qids.update(claim_entity_ids(entity, prop))

    linked_entities = fetch_entities(sorted(linked_qids), languages="en|de|fr|es|zh") if linked_qids else {}

    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    with args.output_jsonl.open("w", encoding="utf-8") as handle:
        for row in rows:
            qid = (row.get("wikidata_qid") or "").strip()
            entity = entities.get(qid, {})
            evidence: dict[str, Any] = {
                "person_id": row.get("person_id", ""),
                "canonical_name": row.get("canonical_name", ""),
                "wikidata_qid": qid,
                "candidate_birth_year": row.get("birth_year", ""),
                "candidate_death_year": row.get("death_year", ""),
                "candidate_source_occupation": row.get("level3_main_occ", ""),
                "candidate_source_region": row.get("region", ""),
                "wikidata_label": first_text(entity.get("labels")),
                "wikidata_description": first_text(entity.get("descriptions")),
                "aliases": sorted(
                    {
                        alias.get("value", "")
                        for aliases in (entity.get("aliases") or {}).values()
                        for alias in aliases
                        if alias.get("value")
                    }
                ),
            }
            for prop, field in ENTITY_PROPERTIES.items():
                ids = claim_entity_ids(entity, prop)
                evidence[field] = [label_record(item, linked_entities.get(item)) for item in ids]
            for prop, field in STRING_PROPERTIES.items():
                evidence[field] = claim_strings(entity, prop)

            records.append(evidence)
            handle.write(json.dumps(evidence, ensure_ascii=False) + "\n")

    summary = {
        "candidates_requested": len(rows),
        "wikidata_entities_found": sum(bool(entities.get(qid)) for qid in qids),
        "with_occupation_or_field_evidence": sum(
            bool(record.get("occupations") or record.get("fields_of_work")) for record in records
        ),
        "with_employer_or_education_evidence": sum(
            bool(record.get("employers") or record.get("educated_at")) for record in records
        ),
        "with_notable_work_evidence": sum(bool(record.get("notable_works")) for record in records),
        "with_external_authority_id": sum(
            bool(record.get("orcid") or record.get("viaf") or record.get("isni") or record.get("gnd") or record.get("loc"))
            for record in records
        ),
        "mental_health_fields_requested": False,
        "note": "Wikidata evidence is contextual/authority evidence for review only; it does not verify an OpenAlex identity automatically.",
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
