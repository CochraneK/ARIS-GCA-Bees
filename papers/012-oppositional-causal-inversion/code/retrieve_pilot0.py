#!/usr/bin/env python3
"""Reproducible dual-source retrieval for ARIS4C012 Gate R.

Queries and outcome-independent relevance gates are loaded from
process/RETRIEVAL_SPEC.json. The script writes:
- provider/query-level JSON responses (field-limited but otherwise unedited);
- a deterministic de-duplicated candidate CSV;
- a rejection CSV with topical/type exclusion reasons;
- a manifest with timestamps, request URLs, hashes and row counts.

This script retrieves candidates only. It never labels a record as OCI-positive.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USER_AGENT = "ARIS4C012-retrieval/0.2 (+https://github.com/CochraneK/ARIS4C)"
DOI_RE = re.compile(r"^https?://(?:dx\.)?doi\.org/", re.I)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_doi(value: str | None) -> str:
    if not value:
        return ""
    value = DOI_RE.sub("", value.strip())
    return value.lower().rstrip(" .")


def normalize_title(value: str | None) -> str:
    if not value:
        return ""
    s = unicodedata.normalize("NFKC", value).lower()
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    return " ".join(s.split())


def published_year_crossref(item: dict[str, Any]) -> str:
    parts = ((item.get("published") or {}).get("date-parts") or [])
    if parts and parts[0]:
        return str(parts[0][0])
    return ""


def first_text(value: Any) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value or "")


def dedupe_key(record: dict[str, Any]) -> str:
    doi = normalize_doi(record.get("doi"))
    if doi:
        return "doi:" + doi
    return "ty:" + normalize_title(record.get("title")) + "|" + str(record.get("year") or "")


def http_json(url: str, retries: int = 4, timeout: int = 45) -> tuple[dict[str, Any], bytes]:
    last: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
            return json.loads(data), data
        except Exception as exc:
            last = exc
            if attempt + 1 < retries:
                time.sleep(2 ** attempt)
    assert last is not None
    raise last


def build_openalex_url(endpoint: str, query: str, cfg: dict[str, Any], mailto: str) -> str:
    params = {
        "search": query,
        "per-page": str(cfg["rows_per_query"]),
        "sort": cfg["sort"],
        "select": ",".join(cfg["select"]),
    }
    if mailto:
        params["mailto"] = mailto
    return endpoint + "?" + urllib.parse.urlencode(params)


def build_crossref_url(endpoint: str, query: str, cfg: dict[str, Any], mailto: str) -> str:
    params = {
        "query.bibliographic": query,
        "rows": str(cfg["rows_per_query"]),
        "select": ",".join(cfg["select"]),
    }
    if mailto:
        params["mailto"] = mailto
    return endpoint + "?" + urllib.parse.urlencode(params)


def records_openalex(payload: dict[str, Any], *, stratum: str, query: str, query_index: int) -> list[dict[str, Any]]:
    out = []
    for rank, item in enumerate(payload.get("results") or [], start=1):
        topic = item.get("primary_topic") or {}
        out.append({
            "provider": "openalex",
            "stratum": stratum,
            "query": query,
            "query_index": query_index,
            "source_rank": rank,
            "provider_id": item.get("id") or "",
            "doi": normalize_doi(item.get("doi")),
            "title": item.get("display_name") or "",
            "year": item.get("publication_year") or "",
            "type": item.get("type") or "",
            "venue_or_topic": topic.get("display_name") or "",
            "cited_by_count": item.get("cited_by_count") or 0,
            "landing_url": (item.get("ids") or {}).get("openalex") or item.get("id") or "",
        })
    return out


def records_crossref(payload: dict[str, Any], *, stratum: str, query: str, query_index: int) -> list[dict[str, Any]]:
    out = []
    message = payload.get("message") or {}
    for rank, item in enumerate(message.get("items") or [], start=1):
        containers = item.get("container-title") or []
        out.append({
            "provider": "crossref",
            "stratum": stratum,
            "query": query,
            "query_index": query_index,
            "source_rank": rank,
            "provider_id": normalize_doi(item.get("DOI")),
            "doi": normalize_doi(item.get("DOI")),
            "title": first_text(item.get("title")),
            "year": published_year_crossref(item),
            "type": item.get("type") or "",
            "venue_or_topic": first_text(containers),
            "cited_by_count": item.get("is-referenced-by-count") or 0,
            "landing_url": item.get("URL") or "",
        })
    return out


def title_passes_anchor_groups(title: str | None, anchor_groups: list[list[str]]) -> tuple[bool, list[str]]:
    """Require >=1 title phrase from every prespecified anchor group."""
    normalized = normalize_title(title)
    missing: list[str] = []
    for group in anchor_groups:
        if not any(normalize_title(anchor) in normalized for anchor in group):
            missing.append("|".join(group))
    return not missing, missing


def filter_records(
    records: list[dict[str, Any]],
    query_spec: dict[str, Any],
    allowed_types: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    allowed = set(allowed_types)
    anchors = query_spec.get("anchor_groups") or []

    for record in records:
        reasons: list[str] = []
        if allowed and record.get("type") not in allowed:
            reasons.append("type_not_allowed:" + str(record.get("type") or ""))
        passes, missing = title_passes_anchor_groups(record.get("title"), anchors)
        if not passes:
            reasons.extend("missing_anchor_group:" + group for group in missing)

        if reasons:
            row = dict(record)
            row["rejection_reasons"] = ";".join(reasons)
            rejected.append(row)
        else:
            accepted.append(record)

    return accepted, rejected


def interleave_unique(groups: list[list[dict[str, Any]]], limit: int) -> list[dict[str, Any]]:
    """Round-robin across filtered provider/query lists, preserving source rank."""
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    max_len = max((len(g) for g in groups), default=0)
    for rank0 in range(max_len):
        for group in groups:
            if rank0 >= len(group):
                continue
            record = group[rank0]
            key = dedupe_key(record)
            if not key or key in seen:
                continue
            seen.add(key)
            selected.append(record)
            if len(selected) >= limit:
                return selected
    return selected


def write_candidates_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fields = [
        "selection_rank","provider","stratum","query_index","query","source_rank",
        "provider_id","doi","title","year","type","venue_or_topic",
        "cited_by_count","landing_url","dedupe_key",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, record in enumerate(records, start=1):
            row = dict(record)
            row["selection_rank"] = i
            row["dedupe_key"] = dedupe_key(record)
            w.writerow({k: row.get(k, "") for k in fields})


def write_rejections_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fields = [
        "provider","stratum","query_index","query","source_rank","provider_id",
        "doi","title","year","type","venue_or_topic","rejection_reasons",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for record in records:
            w.writerow({k: record.get(k, "") for k in fields})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--sleep", type=float, default=0.25)
    args = parser.parse_args()

    spec_path = Path(args.spec)
    out = Path(args.out)
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    mailto = os.environ.get("ARIS4C_CONTACT_EMAIL", "").strip()
    manifest: dict[str, Any] = {
        "classification": "RETRIEVAL_CANDIDATES_NOT_OCI_LABELS",
        "protocol_version": spec["protocol_version"],
        "spec_sha256": sha256_bytes(spec_path.read_bytes()),
        "retrieved_at_utc": utc_now(),
        "requests": [],
        "strata": {},
    }
    all_selected: list[dict[str, Any]] = []
    all_rejected: list[dict[str, Any]] = []

    oa_cfg = spec["providers"]["openalex"]
    cr_cfg = spec["providers"]["crossref"]

    for stratum in spec["strata"]:
        sid = stratum["id"]
        source_groups: list[list[dict[str, Any]]] = []
        stratum_rejected = 0
        for qi, query_spec in enumerate(stratum["queries"], start=1):
            query = query_spec["text"]
            calls = [
                ("openalex", oa_cfg, build_openalex_url(oa_cfg["endpoint"], query, oa_cfg, mailto)),
                ("crossref", cr_cfg, build_crossref_url(cr_cfg["endpoint"], query, cr_cfg, mailto)),
            ]
            for provider, provider_cfg, url in calls:
                payload, raw = http_json(url)
                raw_path = raw_dir / f"{sid}__q{qi}__{provider}.json"
                raw_path.write_bytes(raw)
                if provider == "openalex":
                    records = records_openalex(payload, stratum=sid, query=query, query_index=qi)
                else:
                    records = records_crossref(payload, stratum=sid, query=query, query_index=qi)

                accepted, rejected = filter_records(
                    records,
                    query_spec=query_spec,
                    allowed_types=provider_cfg.get("allowed_types") or [],
                )
                source_groups.append(accepted)
                all_rejected.extend(rejected)
                stratum_rejected += len(rejected)

                manifest["requests"].append({
                    "provider": provider,
                    "stratum": sid,
                    "query_index": qi,
                    "query": query,
                    "anchor_groups": query_spec.get("anchor_groups") or [],
                    "request_url": url,
                    "raw_file": str(raw_path.relative_to(out)),
                    "raw_sha256": sha256_bytes(raw),
                    "records_returned": len(records),
                    "records_accepted_topical_type": len(accepted),
                    "records_rejected_topical_type": len(rejected),
                })
                time.sleep(args.sleep)

        selected = interleave_unique(source_groups, int(spec["selection"]["selected_per_stratum"]))
        all_selected.extend(selected)
        manifest["strata"][sid] = {
            "source_groups": len(source_groups),
            "selected_unique": len(selected),
            "rejected_before_dedup_selection": stratum_rejected,
            "selected_by_provider": {
                "openalex": sum(1 for r in selected if r["provider"] == "openalex"),
                "crossref": sum(1 for r in selected if r["provider"] == "crossref"),
            },
        }

    csv_path = out / "retrieval_candidates.csv"
    reject_path = out / "retrieval_rejections.csv"
    write_candidates_csv(csv_path, all_selected)
    write_rejections_csv(reject_path, all_rejected)

    manifest["candidate_rows"] = len(all_selected)
    manifest["rejection_rows"] = len(all_rejected)
    manifest["candidate_csv"] = csv_path.name
    manifest["candidate_csv_sha256"] = sha256_bytes(csv_path.read_bytes())
    manifest["rejection_csv"] = reject_path.name
    manifest["rejection_csv_sha256"] = sha256_bytes(reject_path.read_bytes())
    manifest["completed_at_utc"] = utc_now()

    (out / "retrieval_manifest.json").write_bytes(canonical_json(manifest))
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
