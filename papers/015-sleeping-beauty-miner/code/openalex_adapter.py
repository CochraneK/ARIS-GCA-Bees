"""Bounded OpenAlex adapter for ARIS4C015.

This adapter supports small pilots, historical-cutoff validation, and metadata
enrichment. It is not intended to crawl the entire OpenAlex graph.

Important implementation rules:
- reconstruct long citation histories from incoming citation edges + citing
  publication years, not from truncated recent-year counters;
- push historical cutoffs into the OpenAlex query;
- reuse metadata already returned by a sampled Work instead of refetching it;
- retry transient 429/5xx responses with bounded exponential backoff;
- use an API key for sustained work when available.

The module uses only Python's standard library.
"""

from __future__ import annotations

import json
import time
import urllib.error
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
    primary_field_id: str | None = None
    referenced_works_count: int | None = None
    authorship_count: int | None = None

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
            primary_field_id=_short_id((topic.get("field") or {}).get("id")),
            referenced_works_count=payload.get("referenced_works_count"),
            authorship_count=(
                len(payload.get("authorships") or [])
                if "authorships" in payload
                else None
            ),
        )


def _short_id(value: str | None) -> str:
    if not value:
        return ""
    return value.rstrip("/").split("/")[-1]


def _retry_delay(
    exc: urllib.error.HTTPError,
    *,
    attempt: int,
    max_server_delay: float = 60.0,
) -> float:
    """Choose a bounded retry delay from headers or exponential backoff."""
    retry_after = exc.headers.get("Retry-After") if exc.headers else None
    if retry_after:
        try:
            delay = float(retry_after)
            if 0 <= delay <= max_server_delay:
                return delay
        except ValueError:
            pass
    return min(float(2**attempt), max_server_delay)


def _rate_limit_context(exc: urllib.error.HTTPError) -> str:
    if not exc.headers:
        return ""
    bits = []
    for header in (
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
        "X-RateLimit-Credits-Used",
    ):
        value = exc.headers.get(header)
        if value is not None:
            bits.append(f"{header}={value}")
    return "; ".join(bits)


def _request_json(
    path: str,
    *,
    params: dict[str, str | int] | None = None,
    api_key: str | None = None,
    timeout: int = 30,
    max_retries: int = 5,
    base_sleep_seconds: float = 0.0,
) -> dict[str, Any]:
    """Issue an OpenAlex request with bounded retry for transient failures."""
    query = dict(params or {})
    if api_key:
        query["api_key"] = api_key
    url = BASE_URL + path
    if query:
        url += "?" + urllib.parse.urlencode(query, safe=":,|")

    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        if base_sleep_seconds:
            time.sleep(base_sleep_seconds)

        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "ARIS4C015-Sleeping-Beauty-Miner/0.2",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status != 200:
                    raise OpenAlexError(f"OpenAlex HTTP {response.status}")
                return json.loads(response.read().decode("utf-8"))

        except urllib.error.HTTPError as exc:
            last_error = exc
            transient = exc.code == 429 or 500 <= exc.code < 600
            if transient and attempt < max_retries:
                time.sleep(_retry_delay(exc, attempt=attempt))
                continue

            context = _rate_limit_context(exc)
            detail = f"HTTP Error {exc.code}: {exc.reason}"
            if context:
                detail += f" ({context})"
            raise OpenAlexError(detail) from exc

        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < max_retries:
                time.sleep(min(float(2**attempt), 30.0))
                continue
            raise OpenAlexError(str(exc)) from exc

        except OpenAlexError:
            raise

        except Exception as exc:
            raise OpenAlexError(str(exc)) from exc

    raise OpenAlexError(str(last_error or "OpenAlex request failed"))


def fetch_work(identifier: str, *, api_key: str | None = None) -> OpenAlexWork:
    """Fetch one work by OpenAlex ID or DOI."""
    encoded = urllib.parse.quote(identifier, safe=":/")
    payload = _request_json(f"/works/{encoded}", api_key=api_key)
    return OpenAlexWork.from_payload(payload)


WORK_METADATA_SELECT = (
    "id,display_name,publication_year,doi,cited_by_count,"
    "primary_topic,referenced_works_count,authorships"
)


def count_works(
    *,
    filters: str,
    api_key: str | None = None,
) -> int:
    """Return the OpenAlex result count for a filtered Works frame."""
    payload = _request_json(
        "/works",
        params={
            "filter": filters,
            "per_page": 1,
            "select": "id",
        },
        api_key=api_key,
    )
    count = (payload.get("meta") or {}).get("count")
    if count is None:
        raise OpenAlexError("OpenAlex response did not include meta.count")
    return int(count)


def iter_works(
    *,
    filters: str,
    api_key: str | None = None,
    max_records: int | None = None,
    per_page: int = 100,
    polite_sleep_seconds: float = 0.05,
) -> Iterator[OpenAlexWork]:
    """Yield a complete filtered Works frame using cursor pagination.

    This is the non-random counterpart to sample_works and is intended for
    bounded exact frames such as publication_year x primary field. It does not
    reconstruct citation histories; callers should persist metadata first and
    perform expensive edge reconstruction as a separate resumable stage.
    """
    if not filters:
        raise ValueError("filters is required")
    if per_page < 1 or per_page > 100:
        raise ValueError("per_page must be between 1 and 100")
    if max_records is not None and max_records < 1:
        raise ValueError("max_records must be >= 1 when provided")

    cursor = "*"
    yielded = 0
    while cursor:
        payload = _request_json(
            "/works",
            params={
                "filter": filters,
                "per_page": per_page,
                "cursor": cursor,
                "select": WORK_METADATA_SELECT,
            },
            api_key=api_key,
        )
        results = payload.get("results") or []
        for row in results:
            yield OpenAlexWork.from_payload(row)
            yielded += 1
            if max_records is not None and yielded >= max_records:
                return

        cursor = (payload.get("meta") or {}).get("next_cursor")
        if not results:
            return
        if polite_sleep_seconds:
            time.sleep(polite_sleep_seconds)


def iter_citing_works(
    work_id: str,
    *,
    api_key: str | None = None,
    max_records: int | None = None,
    per_page: int = 100,
    polite_sleep_seconds: float = 0.05,
    to_publication_year: int | None = None,
) -> Iterator[dict[str, Any]]:
    """Yield works that cite the target using cursor pagination.

    For historical-cutoff work, to_publication_year adds the OpenAlex
    to_publication_date filter at query time. The small default inter-page
    delay reduces burst pressure in matrix CI runs.
    """
    target = _short_id(work_id)
    if not target:
        raise ValueError("work_id is required")
    if per_page < 1 or per_page > 100:
        raise ValueError("per_page must be between 1 and 100")

    filters = [f"cites:{target}"]
    if to_publication_year is not None:
        year = int(to_publication_year)
        if year < 0:
            raise ValueError("to_publication_year must be non-negative")
        filters.append(f"to_publication_date:{year:04d}-12-31")

    cursor = "*"
    yielded = 0

    while cursor:
        payload = _request_json(
            "/works",
            params={
                "filter": ",".join(filters),
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


def reconstruct_history_for_known_work(
    work: OpenAlexWork,
    *,
    publication_year: int | None = None,
    end_year: int | None = None,
    api_key: str | None = None,
    max_records: int | None = None,
) -> CitationHistory:
    """Reconstruct history when target metadata is already available.

    This avoids one redundant Work lookup per sampled target, which materially
    lowers request volume in historical cohort workflows.
    """
    year = (
        publication_year
        if publication_year is not None
        else work.publication_year
    )
    if year is None:
        raise OpenAlexError("Target work has no publication_year")

    citing_years = [
        row["publication_year"]
        for row in iter_citing_works(
            work.openalex_id,
            api_key=api_key,
            max_records=max_records,
            to_publication_year=end_year,
        )
        if row.get("publication_year") is not None
    ]
    return citation_history_from_citing_years(
        int(year),
        citing_years,
        end_year=end_year,
        strict=False,
    )


def reconstruct_history_from_openalex(
    work_id: str,
    *,
    publication_year: int | None = None,
    end_year: int | None = None,
    api_key: str | None = None,
    max_records: int | None = None,
) -> tuple[OpenAlexWork, CitationHistory]:
    """Fetch target metadata and reconstruct a zero-filled citation history."""
    work = fetch_work(work_id, api_key=api_key)
    history = reconstruct_history_for_known_work(
        work,
        publication_year=publication_year,
        end_year=end_year,
        api_key=api_key,
        max_records=max_records,
    )
    return work, history


def history_is_complete(
    work: OpenAlexWork,
    history: CitationHistory,
) -> bool | None:
    """Best-effort whole-lifetime completeness check against cited_by_count."""
    if work.cited_by_count is None:
        return None
    return history.valid_edges >= int(work.cited_by_count)


def sample_works(
    *,
    filters: str,
    sample_size: int,
    seed: int,
    api_key: str | None = None,
) -> list[OpenAlexWork]:
    """Return a reproducible random sample of works.

    Sampling-frame filters should avoid outcome-bearing present-day variables
    such as current citation counts, later awards, or post-publication status.
    """
    if sample_size < 1 or sample_size > 100:
        raise ValueError(
            "sample_size must be between 1 and 100 for one-page sampling"
        )
    payload = _request_json(
        "/works",
        params={
            "filter": filters,
            "sample": int(sample_size),
            "seed": int(seed),
            "per_page": int(sample_size),
            "select": WORK_METADATA_SELECT,
        },
        api_key=api_key,
    )
    return [
        OpenAlexWork.from_payload(row)
        for row in (payload.get("results") or [])
    ]
