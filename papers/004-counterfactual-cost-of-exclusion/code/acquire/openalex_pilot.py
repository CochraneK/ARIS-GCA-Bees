#!/usr/bin/env python3
"""Fetch a bounded OpenAlex author/work pilot for ARIS4C004.

Input is a mental-health-independent candidate CSV. The script does not search
for psychiatric terms and therefore cannot define the exposure sample.

Required input column: person_id
At least one resolver column: openalex_author_id OR orcid

OPENALEX_API_KEY is optional. Current OpenAlex documentation allows keyless
casual API use; a free key increases the request budget. Never commit the key.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

BASE_URL = "https://api.openalex.org"
USER_AGENT = "ARIS4C004-feasibility/0.1 (research reproducibility pilot)"


def normalize_openalex_id(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    value = value.rstrip("/")
    if value.startswith("https://openalex.org/"):
        return value.rsplit("/", 1)[-1]
    return value


def normalize_orcid(value: str) -> str:
    value = (value or "").strip()
    if value.startswith("https://orcid.org/"):
        value = value.rsplit("/", 1)[-1]
    return value


class OpenAlexClient:
    def __init__(
        self,
        api_key: str | None,
        timeout: int = 30,
        max_retries: int = 5,
        requests_per_second: float = 5.0,
    ) -> None:
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.min_interval = 1.0 / max(requests_per_second, 0.1)
        self._last_request = 0.0

    def _request(self, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        params = dict(params or {})
        if self.api_key:
            params["api_key"] = self.api_key
        url = f"{BASE_URL}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params, safe=":,|*")

        for attempt in range(self.max_retries + 1):
            wait = self.min_interval - (time.monotonic() - self._last_request)
            if wait > 0:
                time.sleep(wait)
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            try:
                self._last_request = time.monotonic()
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                if exc.code not in {429, 500, 502, 503, 504} or attempt >= self.max_retries:
                    raise
                retry_after = exc.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else min(2**attempt, 30)
                time.sleep(delay)
            except urllib.error.URLError:
                if attempt >= self.max_retries:
                    raise
                time.sleep(min(2**attempt, 30))
        raise RuntimeError("unreachable retry loop")

    def resolve_author(self, openalex_id: str = "", orcid: str = "") -> dict[str, Any] | None:
        if openalex_id:
            return self._request(f"/authors/{normalize_openalex_id(openalex_id)}")
        if orcid:
            oid = normalize_orcid(orcid)
            data = self._request(
                "/authors",
                {
                    "filter": f"orcid:{oid}",
                    "per_page": "5",
                    "select": "id,display_name,orcid,works_count,cited_by_count,last_known_institutions,topics",
                },
            )
            results = data.get("results", [])
            if len(results) == 1:
                return results[0]
            if len(results) > 1:
                raise RuntimeError(f"ORCID {oid} unexpectedly resolved to {len(results)} OpenAlex authors")
        return None

    def iter_author_works(
        self,
        author_id: str,
        year_min: int,
        year_max: int,
        max_works: int | None = None,
    ) -> Iterable[dict[str, Any]]:
        author_id = normalize_openalex_id(author_id)
        cursor = "*"
        yielded = 0
        while cursor:
            data = self._request(
                "/works",
                {
                    "filter": (
                        f"authorships.author.id:{author_id},"
                        f"from_publication_date:{year_min}-01-01,"
                        f"to_publication_date:{year_max}-12-31"
                    ),
                    "per_page": "100",
                    "cursor": cursor,
                    "select": (
                        "id,doi,display_name,publication_year,publication_date,type,"
                        "authorships,referenced_works,cited_by_count,"
                        "citation_normalized_percentile,primary_topic,topics"
                    ),
                },
            )
            for work in data.get("results", []):
                yield work
                yielded += 1
                if max_works is not None and yielded >= max_works:
                    return
            cursor = data.get("meta", {}).get("next_cursor")


def read_candidates(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "person_id" not in rows[0]:
        raise ValueError("candidate CSV must contain person_id")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidates", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--year-min", type=int, default=1900)
    parser.add_argument("--year-max", type=int, default=2000)
    parser.add_argument("--max-candidates", type=int)
    parser.add_argument("--max-works-per-author", type=int)
    parser.add_argument("--sleep-rps", type=float, default=5.0)
    args = parser.parse_args()

    if args.year_min > args.year_max:
        parser.error("year-min must be <= year-max")

    candidates = read_candidates(args.candidates)
    if args.max_candidates:
        candidates = candidates[: args.max_candidates]

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    authors_path = out / "openalex_authors.jsonl"
    works_path = out / "openalex_works.jsonl"
    unresolved_path = out / "openalex_unresolved.csv"

    client = OpenAlexClient(
        api_key=os.getenv("OPENALEX_API_KEY") or None,
        requests_per_second=args.sleep_rps,
    )

    unresolved: list[dict[str, str]] = []
    resolved_n = 0
    works_n = 0

    with authors_path.open("w", encoding="utf-8") as authors_file, works_path.open(
        "w", encoding="utf-8"
    ) as works_file:
        for row in candidates:
            pid = (row.get("person_id") or "").strip()
            openalex_id = (row.get("openalex_author_id") or "").strip()
            orcid = (row.get("orcid") or "").strip()
            try:
                author = client.resolve_author(openalex_id=openalex_id, orcid=orcid)
            except Exception as exc:  # network/API errors recorded rather than silently dropped
                unresolved.append({"person_id": pid, "reason": f"resolver_error:{type(exc).__name__}:{exc}"})
                continue

            if not author:
                unresolved.append({"person_id": pid, "reason": "no_openalex_id_or_unique_orcid_match"})
                continue

            author_id = normalize_openalex_id(str(author.get("id", "")))
            if not author_id:
                unresolved.append({"person_id": pid, "reason": "resolved_record_missing_id"})
                continue

            resolved_n += 1
            authors_file.write(json.dumps({"person_id": pid, "author": author}, ensure_ascii=False) + "\n")

            try:
                for work in client.iter_author_works(
                    author_id,
                    args.year_min,
                    args.year_max,
                    max_works=args.max_works_per_author,
                ):
                    works_file.write(
                        json.dumps({"person_id": pid, "author_id": author_id, "work": work}, ensure_ascii=False)
                        + "\n"
                    )
                    works_n += 1
            except Exception as exc:
                unresolved.append({"person_id": pid, "reason": f"works_error:{type(exc).__name__}:{exc}"})

    with unresolved_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["person_id", "reason"])
        writer.writeheader()
        writer.writerows(unresolved)

    summary = {
        "input_candidates": len(candidates),
        "resolved_candidates": resolved_n,
        "resolution_rate": (resolved_n / len(candidates)) if candidates else 0.0,
        "works_written": works_n,
        "unresolved_rows": len(unresolved),
        "year_min": args.year_min,
        "year_max": args.year_max,
        "api_key_used": bool(os.getenv("OPENALEX_API_KEY")),
    }
    (out / "openalex_acquisition_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0 if resolved_n else 2


if __name__ == "__main__":
    raise SystemExit(main())
