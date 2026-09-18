"""Bounded OpenAlex adapter for ARIS4C015.

Purpose
-------
This adapter is for small pilots, validation cases, and ID/metadata enrichment.
It is not intended to crawl the complete OpenAlex graph.

OpenAlex semantics used here:
- a target Work contains publication_year and referenced_works;
- works that cite a target can be retrieved with the Works filter
  `cites:<OPENALEX_WORK_ID>`;
- yearly histories for long-lived papers should be reconstructed from the
  publication years of incoming citing works, not from a truncated
  counts_by_year field.

The module uses only Python's standard library so the deterministic core of
ARIS4C015 remains lightweight.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Iterator

from citation_history import CitationHistory, citation_history_from_citing_years


BASE_URL = "https://api.openalex.org"


class OpenAlexError(RuntimeError):
    """Raised when the OpenAlex API returns an unusable response."""


@dataclass(frozen=True)
class OpenAlexWork:
    openalex_id: str
    title: str | None
    publication_year: int | None
    doi: str | None
    cited_by_count: int | None
    primary_topic: str | None

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "OpenAlexWork":
        topic = payload.get("primary_topic") or {}
        return cls(
            openalex_id=_short_id(payload.get("id")),
            title=payload.get("display_name") or payload.get("title"),
            publication_year=payload.get("publication_year"),
            doi=payload.get("doi"),
            cited_by_count=payload.get("cited_by_count"),
            primary_topic=topic.get("display_name"),
        )


def _short_id(value: str | None) -> str:
    if not value:
        return ""
    return value.rstrip("/").split("/")[-1]


def _request_json(
    path: str,
    *,
    params: dict[str, str | int] | None = None,
    api_key: str | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    query = dict(params or {})
    if api_key:
        query["api_key"] = api_key
    url = BASE_URL + path
    if query:
        url += "?" + urllib.parse.urlencode(query, safe=":,|")
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "ARIS4C015-Sleeping-Beauty-Miner/0.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status != 200:
                raise OpenAlexError(f"OpenAlex HTTP {response.status}")
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        if isinstance(exc, OpenAlexError):
            raise
        raise OpenAlexError(str(exc)) from exc


def fetch_work(identifier: str, *, api_key: str | None = None) -> OpenAlexWork:
    """Fetch one work by OpenAlex ID or DOI."""
    encoded = urllib.parse.quote(identifier, safe=":/")
    payload = _request_json(f"/works/{encoded}", api_key=api_key)
    return OpenAlexWork.from_payload(payload)


def iter_citing_works(
    work_id: str,
    *,
    api_key: str | None = None,
    max_records: int | None = None,
    per_page: int = 200,
    polite_sleep_seconds: float = 0.0,
) -> Iterator[dict[str, Any]]:
    """Yield works that cite the target work using cursor pagination.

    The query selects only fields needed for trajectory reconstruction and
    basic provenance. max_records should be set for bounded pilots.
    """
    target = _short_id(work_id)
    if not target:
        raise ValueError("work_id is required")
    if per_page < 1 or per_page > 200:
        raise ValueError("per_page must be between 1 and 200")

    cursor = "*"
    yielded = 0

    while cursor:
        payload = _request_json(
            "/works",
            params={
                "filter": f"cites:{target}",
                "per_page": per_page,
                "cursor": cursor,
                "select": "id,display_name,publication_year,doi",
            },
            api_key=api_key,
        )
        results = payload.get("results") or []
        for row in results:
            yield row
            yielded += 1
            if max_records is not None and yielded >= max_records:
                return

        cursor = (payload.get("meta") or {}).get("next_cursor")
        if not results:
            return
        if polite_sleep_seconds:
            time.sleep(polite_sleep_seconds)


def reconstruct_history_from_openalex(
    work_id: str,
    *,
    publication_year: int | None = None,
    end_year: int | None = None,
    api_key: str | None = None,
    max_records: int | None = None,
) -> tuple[OpenAlexWork, CitationHistory]:
    """Fetch a target work and reconstruct a zero-filled citation history.

    If max_records is not None and the work has more incoming citations than
    the cap, the returned history is explicitly incomplete and should not be
    used for confirmatory Sleeping Beauty metrics.
    """
    work = fetch_work(work_id, api_key=api_key)
    year = publication_year if publication_year is not None else work.publication_year
    if year is None:
        raise OpenAlexError("Target work has no publication_year")

    citing_years = [
        row["publication_year"]
        for row in iter_citing_works(
            work.openalex_id,
            api_key=api_key,
            max_records=max_records,
        )
        if row.get("publication_year") is not None
    ]
    history = citation_history_from_citing_years(
        int(year),
        citing_years,
        end_year=end_year,
        strict=False,
    )
    return work, history


def history_is_complete(work: OpenAlexWork, history: CitationHistory) -> bool | None:
    """Best-effort completeness check against cited_by_count.

    OpenAlex documents that filtered citation results and cited_by_count can
    differ slightly because of update timing, so this is a diagnostic rather
    than a hard integrity assertion.
    """
    if work.cited_by_count is None:
        return None
    return history.valid_edges >= int(work.cited_by_count)
