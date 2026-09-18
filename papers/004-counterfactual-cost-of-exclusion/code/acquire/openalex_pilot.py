#!/usr/bin/env python3
"""Fetch a bounded OpenAlex author/work pilot for ARIS4C004.

Input is a mental-health-independent candidate CSV. The script never searches
for psychiatric terms and therefore cannot define the exposure sample.

Resolution is deliberately conservative:
1. validate an explicit OpenAlex ID when present;
2. use exact ORCID when present;
3. otherwise search OpenAlex Authors by canonical name and score candidates with
   name similarity plus temporal plausibility from OpenAlex `counts_by_year`.

Low-score or close-tie matches are left ambiguous instead of being forced.
Every accepted match and every search candidate is written with provenance so
manual auditing can precede confirmatory analysis.

OPENALEX_API_KEY is optional. Never commit it.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

BASE_URL = "https://api.openalex.org"
USER_AGENT = "ARIS4C004-feasibility/0.2 (research reproducibility pilot)"


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


def parse_int(value: str) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def normalize_name(value: str) -> str:
    """ASCII-ish comparison key; source/display strings are still retained."""
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.casefold()
    value = re.sub(r"[^\w\s-]", " ", value)
    value = value.replace("_", " ").replace("-", " ")
    return " ".join(value.split())


def name_similarity(a: str, b: str) -> float:
    a_n, b_n = normalize_name(a), normalize_name(b)
    if not a_n or not b_n:
        return 0.0
    if a_n == b_n:
        return 1.0
    seq = SequenceMatcher(None, a_n, b_n).ratio()
    a_tokens, b_tokens = set(a_n.split()), set(b_n.split())
    union = a_tokens | b_tokens
    jaccard = len(a_tokens & b_tokens) / len(union) if union else 0.0
    # Token overlap helps with middle initials/name-order noise, but sequence still
    # dominates to avoid accepting common surname collisions.
    return max(seq, 0.65 * seq + 0.35 * jaccard)


def author_name_score(candidate_name: str, author: dict[str, Any]) -> float:
    alternatives = [str(author.get("display_name") or "")]
    alternatives.extend(str(x) for x in (author.get("display_name_alternatives") or []) if x)
    return max((name_similarity(candidate_name, alt) for alt in alternatives), default=0.0)


def career_plausibility(author: dict[str, Any], birth_year: int | None, death_year: int | None) -> float:
    """Return [0,1] from publication-year overlap with a plausible lifetime career.

    This is evidence for identity, not a hard historical truth. Publications can
    appear posthumously and OpenAlex years may be noisy, so the plausible window
    intentionally has slack.
    """
    if birth_year is None and death_year is None:
        return 0.5
    counts = author.get("counts_by_year") or []
    years = [
        int(item.get("year"))
        for item in counts
        if item.get("year") is not None and int(item.get("works_count") or 0) > 0
    ]
    if not years:
        return 0.35
    lo = (birth_year + 15) if birth_year is not None else min(years) - 1
    hi = (death_year + 5) if death_year is not None else max(years) + 1
    plausible = sum(lo <= year <= hi for year in years)
    share = plausible / len(years)
    if plausible == 0:
        return 0.0
    return min(1.0, 0.4 + 0.6 * share)


@dataclass
class Resolution:
    author: dict[str, Any] | None
    status: str
    method: str
    score: float | None = None
    margin: float | None = None
    name_score: float | None = None
    career_score: float | None = None
    searched_candidates: list[dict[str, Any]] | None = None
    reason: str = ""


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

    def get_author(self, openalex_id: str) -> dict[str, Any]:
        return self._request(f"/authors/{normalize_openalex_id(openalex_id)}")

    def author_by_orcid(self, orcid: str) -> list[dict[str, Any]]:
        oid = normalize_orcid(orcid)
        data = self._request(
            "/authors",
            {
                "filter": f"orcid:{oid}",
                "per_page": "5",
            },
        )
        return list(data.get("results", []))

    def search_authors(self, name: str, per_page: int = 10) -> list[dict[str, Any]]:
        data = self._request(
            "/authors",
            {
                "search": name,
                "per_page": str(max(1, min(per_page, 100))),
            },
        )
        return list(data.get("results", []))

    def resolve_candidate(
        self,
        row: dict[str, str],
        min_score: float = 0.80,
        min_name_score: float = 0.82,
        min_margin: float = 0.05,
        search_n: int = 10,
    ) -> Resolution:
        name = (row.get("canonical_name") or "").strip()
        birth = parse_int(row.get("birth_year", ""))
        death = parse_int(row.get("death_year", ""))
        explicit_id = (row.get("openalex_author_id") or "").strip()
        orcid = (row.get("orcid") or "").strip()

        if explicit_id:
            author = self.get_author(explicit_id)
            ns = author_name_score(name, author) if name else 1.0
            cs = career_plausibility(author, birth, death)
            score = 0.8 * ns + 0.2 * cs
            # Wikidata OpenAlex IDs are only leads. Do not silently accept a stale
            # identifier if it disagrees strongly with the candidate name/lifetime.
            if ns >= min_name_score and score >= min_score:
                return Resolution(author, "accepted", "explicit_openalex_id", score, 1.0, ns, cs, [])
            return Resolution(
                None,
                "ambiguous",
                "explicit_openalex_id",
                score,
                0.0,
                ns,
                cs,
                [],
                reason="explicit_id_failed_identity_validation",
            )

        if orcid:
            matches = self.author_by_orcid(orcid)
            if len(matches) == 1:
                author = matches[0]
                ns = author_name_score(name, author) if name else 1.0
                cs = career_plausibility(author, birth, death)
                score = 0.85 * ns + 0.15 * cs
                if ns >= 0.70:  # ORCID is strong evidence; tolerate name variation.
                    return Resolution(author, "accepted", "orcid", score, 1.0, ns, cs, matches)
            if len(matches) > 1:
                return Resolution(None, "ambiguous", "orcid", searched_candidates=matches, reason="multiple_orcid_matches")

        if not name:
            return Resolution(None, "unresolved", "none", reason="missing_name_and_identifiers")

        matches = self.search_authors(name, per_page=search_n)
        scored: list[tuple[float, float, float, dict[str, Any]]] = []
        audit_rows: list[dict[str, Any]] = []
        for author in matches:
            ns = author_name_score(name, author)
            cs = career_plausibility(author, birth, death)
            score = 0.8 * ns + 0.2 * cs
            scored.append((score, ns, cs, author))
            audit_rows.append(
                {
                    "id": author.get("id"),
                    "display_name": author.get("display_name"),
                    "orcid": author.get("orcid"),
                    "works_count": author.get("works_count"),
                    "score": round(score, 6),
                    "name_score": round(ns, 6),
                    "career_score": round(cs, 6),
                }
            )
        scored.sort(key=lambda item: item[0], reverse=True)
        audit_rows.sort(key=lambda item: item["score"], reverse=True)

        if not scored:
            return Resolution(None, "unresolved", "name_search", searched_candidates=[], reason="no_search_results")

        best_score, best_ns, best_cs, best = scored[0]
        second_score = scored[1][0] if len(scored) > 1 else 0.0
        margin = best_score - second_score
        exact_name = normalize_name(name) == normalize_name(str(best.get("display_name") or ""))
        accepted = (
            best_score >= min_score
            and best_ns >= min_name_score
            and (margin >= min_margin or (exact_name and best_cs >= 0.70))
        )
        if accepted:
            return Resolution(
                best,
                "accepted",
                "name_search",
                best_score,
                margin,
                best_ns,
                best_cs,
                audit_rows,
            )
        return Resolution(
            None,
            "ambiguous" if best_ns >= 0.65 else "unresolved",
            "name_search",
            best_score,
            margin,
            best_ns,
            best_cs,
            audit_rows,
            reason="below_acceptance_threshold_or_close_tie",
        )

    def iter_citing_works(
        self,
        work_id: str,
        year_min: int,
        year_max: int,
        max_works: int | None = None,
    ) -> Iterable[dict[str, Any]]:
        """Yield works that cite one focal work inside a bounded date window.

        OpenAlex documents the `cites:W...` Works filter as incoming citations
        to the focal work. Results are sorted earliest-first so a bounded pilot
        preserves early diffusion rather than only highly cited late descendants.
        """
        work_id = normalize_openalex_id(work_id)
        cursor = "*"
        yielded = 0
        while cursor:
            data = self._request(
                "/works",
                {
                    "filter": (
                        f"cites:{work_id},"
                        f"from_publication_date:{year_min}-01-01,"
                        f"to_publication_date:{year_max}-12-31"
                    ),
                    "per_page": "100",
                    "cursor": cursor,
                    "sort": "publication_date:asc",
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
    parser.add_argument("--search-n", type=int, default=10)
    parser.add_argument("--min-resolution-score", type=float, default=0.80)
    parser.add_argument("--min-name-score", type=float, default=0.82)
    parser.add_argument("--min-resolution-margin", type=float, default=0.05)
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
    resolution_audit_path = out / "openalex_resolution_audit.jsonl"
    unresolved_path = out / "openalex_unresolved.csv"

    client = OpenAlexClient(
        api_key=os.getenv("OPENALEX_API_KEY") or None,
        requests_per_second=args.sleep_rps,
    )

    unresolved: list[dict[str, str]] = []
    status_counts: dict[str, int] = {"accepted": 0, "ambiguous": 0, "unresolved": 0, "error": 0}
    method_counts: dict[str, int] = {}
    works_n = 0
    resolved_with_works_n = 0

    with (
        authors_path.open("w", encoding="utf-8") as authors_file,
        works_path.open("w", encoding="utf-8") as works_file,
        resolution_audit_path.open("w", encoding="utf-8") as audit_file,
    ):
        for row in candidates:
            pid = (row.get("person_id") or "").strip()
            name = (row.get("canonical_name") or "").strip()
            try:
                resolution = client.resolve_candidate(
                    row,
                    min_score=args.min_resolution_score,
                    min_name_score=args.min_name_score,
                    min_margin=args.min_resolution_margin,
                    search_n=args.search_n,
                )
            except Exception as exc:
                status_counts["error"] += 1
                unresolved.append({"person_id": pid, "canonical_name": name, "status": "error", "reason": f"{type(exc).__name__}:{exc}"})
                continue

            status_counts[resolution.status] = status_counts.get(resolution.status, 0) + 1
            method_counts[resolution.method] = method_counts.get(resolution.method, 0) + 1
            audit_file.write(
                json.dumps(
                    {
                        "person_id": pid,
                        "canonical_name": name,
                        "birth_year": row.get("birth_year"),
                        "death_year": row.get("death_year"),
                        "wikidata_qid": row.get("wikidata_qid"),
                        "status": resolution.status,
                        "method": resolution.method,
                        "score": resolution.score,
                        "margin": resolution.margin,
                        "name_score": resolution.name_score,
                        "career_score": resolution.career_score,
                        "reason": resolution.reason,
                        "search_candidates": resolution.searched_candidates or [],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

            author = resolution.author
            if resolution.status != "accepted" or not author:
                unresolved.append(
                    {
                        "person_id": pid,
                        "canonical_name": name,
                        "status": resolution.status,
                        "reason": resolution.reason or "not_accepted",
                    }
                )
                continue

            author_id = normalize_openalex_id(str(author.get("id", "")))
            if not author_id or not author_id.upper().startswith("A"):
                status_counts["accepted"] -= 1
                status_counts["error"] += 1
                unresolved.append({"person_id": pid, "canonical_name": name, "status": "error", "reason": "accepted_record_missing_author_id"})
                continue

            authors_file.write(
                json.dumps(
                    {
                        "person_id": pid,
                        "canonical_name": name,
                        "resolution_method": resolution.method,
                        "resolution_score": resolution.score,
                        "resolution_margin": resolution.margin,
                        "name_score": resolution.name_score,
                        "career_score": resolution.career_score,
                        "author": author,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

            author_works_n = 0
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
                    author_works_n += 1
            except Exception as exc:
                unresolved.append({"person_id": pid, "canonical_name": name, "status": "works_error", "reason": f"{type(exc).__name__}:{exc}"})
            if author_works_n > 0:
                resolved_with_works_n += 1

    with unresolved_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["person_id", "canonical_name", "status", "reason"])
        writer.writeheader()
        writer.writerows(unresolved)

    accepted_n = status_counts.get("accepted", 0)
    summary = {
        "input_candidates": len(candidates),
        "accepted_candidates": accepted_n,
        "ambiguous_candidates": status_counts.get("ambiguous", 0),
        "unresolved_candidates": status_counts.get("unresolved", 0),
        "resolver_errors": status_counts.get("error", 0),
        "resolution_rate": (accepted_n / len(candidates)) if candidates else 0.0,
        "resolved_with_works_n": resolved_with_works_n,
        "resolved_with_works_rate": (resolved_with_works_n / len(candidates)) if candidates else 0.0,
        "resolution_methods": method_counts,
        "works_written": works_n,
        "unresolved_rows": len(unresolved),
        "year_min": args.year_min,
        "year_max": args.year_max,
        "thresholds": {
            "min_resolution_score": args.min_resolution_score,
            "min_name_score": args.min_name_score,
            "min_resolution_margin": args.min_resolution_margin,
            "search_n": args.search_n,
        },
        "api_key_used": bool(os.getenv("OPENALEX_API_KEY")),
    }
    (out / "openalex_acquisition_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0 if accepted_n else 2


if __name__ == "__main__":
    raise SystemExit(main())
