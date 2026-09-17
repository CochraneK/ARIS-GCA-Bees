#!/usr/bin/env python3
"""Collect candidate-lifetime-aware evidence for plausible OpenAlex fragments.

This is a review aid, NOT an automatic identity merger. Historical OpenAlex
records are often fragmented or contaminated by namesakes. Evidence is therefore
computed primarily from works in a candidate-specific plausible career window,
not from all works attached to an OpenAlex Author ID.

For every possible-fragmentation candidate the script reports:
- ORCID agreement/conflict;
- DOI/title overlap inside the candidate's plausible career window;
- shared coauthors/institutions/topics inside that window;
- publication timing and out-of-lifetime contamination;
- representative plausible and implausible works.

`support`, `conflict`, and `needs_review` are review-priority labels only. They
must never be converted directly into VERIFIED_CLUSTER.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable

ACQUIRE = Path(__file__).resolve().parents[1] / "acquire"
sys.path.insert(0, str(ACQUIRE))
from openalex_pilot import OpenAlexClient, normalize_openalex_id  # noqa: E402


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    return " ".join(value.split())


def jaccard(a: set[str], b: set[str]) -> float | None:
    union = a | b
    if not union:
        return None
    return len(a & b) / len(union)


def overlap_coefficient(a: set[str], b: set[str]) -> float | None:
    if not a or not b:
        return None
    return len(a & b) / min(len(a), len(b))


def safe_year(value: Any) -> int | None:
    try:
        year = int(value)
    except (TypeError, ValueError):
        return None
    return year if 1000 <= year <= 2200 else None


def parse_year(value: Any) -> int | None:
    try:
        year = int(float(value))
    except (TypeError, ValueError):
        return None
    return year if 1000 <= year <= 2200 else None


def career_window(
    birth_year: int | None,
    death_year: int | None,
    min_career_age: int = 15,
    posthumous_slack_years: int = 5,
) -> tuple[int | None, int | None]:
    """A permissive identity-review window, not a substantive career model."""
    lo = birth_year + min_career_age if birth_year is not None else None
    hi = death_year + posthumous_slack_years if death_year is not None else None
    return lo, hi


def within_window(year: int | None, lo: int | None, hi: int | None) -> bool:
    if year is None:
        return False
    if lo is not None and year < lo:
        return False
    if hi is not None and year > hi:
        return False
    return True


def canonical_orcid(value: str | None) -> str:
    value = (value or "").strip().lower()
    value = value.removeprefix("https://orcid.org/")
    return value


def work_title_key(work: dict[str, Any]) -> str:
    return normalize_text(str(work.get("display_name") or work.get("title") or ""))


def work_doi_key(work: dict[str, Any]) -> str:
    doi = str(work.get("doi") or "").strip().lower()
    return doi.removeprefix("https://doi.org/").removeprefix("http://doi.org/")


def iter_authorship_institutions(work: dict[str, Any]) -> Iterable[str]:
    for authorship in work.get("authorships") or []:
        for inst in authorship.get("institutions") or []:
            iid = str(inst.get("id") or "").strip()
            if iid:
                yield iid


def iter_coauthors(work: dict[str, Any], focal_author_id: str) -> Iterable[str]:
    focal = normalize_openalex_id(focal_author_id)
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        aid = normalize_openalex_id(str(author.get("id") or ""))
        if aid and aid != focal:
            yield aid


def iter_work_topic_ids(works: list[dict[str, Any]]) -> Iterable[str]:
    for work in works:
        primary = work.get("primary_topic") or {}
        tid = str(primary.get("id") or "").strip()
        if tid:
            yield tid
        for topic in work.get("topics") or []:
            tid = str(topic.get("id") or "").strip()
            if tid:
                yield tid


@dataclass
class AuthorEvidence:
    author_id: str
    author: dict[str, Any]
    works: list[dict[str, Any]]

    @property
    def orcid(self) -> str:
        return canonical_orcid(str(self.author.get("orcid") or ""))

    def works_in_window(self, lo: int | None, hi: int | None) -> list[dict[str, Any]]:
        return [
            work
            for work in self.works
            if within_window(safe_year(work.get("publication_year")), lo, hi)
        ]

    def works_outside_window(self, lo: int | None, hi: int | None) -> list[dict[str, Any]]:
        return [
            work
            for work in self.works
            if (year := safe_year(work.get("publication_year"))) is not None
            and not within_window(year, lo, hi)
        ]

    def years(self, works: list[dict[str, Any]] | None = None) -> set[int]:
        source = self.works if works is None else works
        return {
            year
            for work in source
            if (year := safe_year(work.get("publication_year"))) is not None
        }

    def dois(self, works: list[dict[str, Any]]) -> set[str]:
        return {key for work in works if (key := work_doi_key(work))}

    def titles(self, works: list[dict[str, Any]]) -> set[str]:
        return {
            key for work in works if (key := work_title_key(work)) and len(key) >= 8
        }

    def coauthors(self, works: list[dict[str, Any]]) -> set[str]:
        return {
            aid
            for work in works
            for aid in iter_coauthors(work, self.author_id)
        }

    def institutions(self, works: list[dict[str, Any]]) -> set[str]:
        # Author-level `last_known_institutions` is intentionally excluded from
        # merge support because a contaminated Author ID can make it misleading.
        return {
            iid
            for work in works
            for iid in iter_authorship_institutions(work)
        }

    def topics(self, works: list[dict[str, Any]]) -> set[str]:
        return set(iter_work_topic_ids(works))

    def representative_works(
        self, works: list[dict[str, Any]], n: int = 5
    ) -> list[dict[str, Any]]:
        ordered = sorted(
            works,
            key=lambda work: (
                int(work.get("cited_by_count") or 0),
                safe_year(work.get("publication_year")) or 0,
            ),
            reverse=True,
        )
        return [
            {
                "id": work.get("id"),
                "doi": work.get("doi"),
                "title": work.get("display_name"),
                "year": work.get("publication_year"),
                "cited_by_count": work.get("cited_by_count"),
            }
            for work in ordered[:n]
        ]


def temporal_summary(years_a: set[int], years_b: set[int]) -> dict[str, Any]:
    if not years_a or not years_b:
        return {
            "year_overlap": None,
            "year_gap": None,
            "a_min": min(years_a) if years_a else None,
            "a_max": max(years_a) if years_a else None,
            "b_min": min(years_b) if years_b else None,
            "b_max": max(years_b) if years_b else None,
        }
    a_min, a_max = min(years_a), max(years_a)
    b_min, b_max = min(years_b), max(years_b)
    overlap = max(0, min(a_max, b_max) - max(a_min, b_min) + 1)
    if overlap:
        gap = 0
    elif a_max < b_min:
        gap = b_min - a_max
    else:
        gap = a_min - b_max
    return {
        "year_overlap": overlap,
        "year_gap": gap,
        "a_min": a_min,
        "a_max": a_max,
        "b_min": b_min,
        "b_max": b_max,
    }


def contamination_summary(
    evidence: AuthorEvidence,
    birth_year: int | None,
    death_year: int | None,
    lo: int | None,
    hi: int | None,
) -> dict[str, Any]:
    all_years = evidence.years()
    plausible = evidence.works_in_window(lo, hi)
    outside = evidence.works_outside_window(lo, hi)
    dated_n = len(plausible) + len(outside)
    before_birth_n = 0
    after_death_slack_n = 0
    if birth_year is not None:
        before_birth_n = sum(
            (year := safe_year(work.get("publication_year"))) is not None
            and year < birth_year
            for work in evidence.works
        )
    if hi is not None:
        after_death_slack_n = sum(
            (year := safe_year(work.get("publication_year"))) is not None and year > hi
            for work in evidence.works
        )
    return {
        "api_attached_works_n": int(evidence.author.get("works_count") or 0),
        "fetched_works_n": len(evidence.works),
        "dated_works_n": dated_n,
        "plausible_works_n": len(plausible),
        "outside_window_works_n": len(outside),
        "outside_window_share": (len(outside) / dated_n) if dated_n else None,
        "before_birth_works_n": before_birth_n,
        "after_death_slack_works_n": after_death_slack_n,
        "all_year_min": min(all_years) if all_years else None,
        "all_year_max": max(all_years) if all_years else None,
    }


def pairwise_evidence(
    a: AuthorEvidence,
    b: AuthorEvidence,
    birth_year: int | None = None,
    death_year: int | None = None,
) -> dict[str, Any]:
    lo, hi = career_window(birth_year, death_year)
    a_works = a.works_in_window(lo, hi)
    b_works = b.works_in_window(lo, hi)

    a_dois, b_dois = a.dois(a_works), b.dois(b_works)
    a_titles, b_titles = a.titles(a_works), b.titles(b_works)
    a_coauthors, b_coauthors = a.coauthors(a_works), b.coauthors(b_works)
    a_institutions, b_institutions = a.institutions(a_works), b.institutions(b_works)
    a_topics, b_topics = a.topics(a_works), b.topics(b_works)

    doi_overlap = a_dois & b_dois
    title_overlap = a_titles & b_titles
    coauthor_overlap = a_coauthors & b_coauthors
    institution_overlap = a_institutions & b_institutions
    topic_overlap = a_topics & b_topics
    temporal = temporal_summary(a.years(a_works), b.years(b_works))
    contam_a = contamination_summary(a, birth_year, death_year, lo, hi)
    contam_b = contamination_summary(b, birth_year, death_year, lo, hi)

    same_orcid = bool(a.orcid and b.orcid and a.orcid == b.orcid)
    conflicting_orcid = bool(a.orcid and b.orcid and a.orcid != b.orcid)

    support_points = 0
    reasons: list[str] = []
    conflicts: list[str] = []

    if same_orcid:
        support_points += 8
        reasons.append("same_nonempty_orcid")
    if doi_overlap:
        support_points += 5
        reasons.append("lifetime_duplicate_doi")
    if title_overlap:
        support_points += 3
        reasons.append("lifetime_normalized_title_overlap")
    if len(coauthor_overlap) >= 2:
        support_points += 3
        reasons.append("lifetime_multiple_shared_coauthors")
    elif len(coauthor_overlap) == 1:
        support_points += 1
        reasons.append("lifetime_one_shared_coauthor")
    if institution_overlap:
        support_points += 2
        reasons.append("lifetime_shared_institution")
    topic_j = jaccard(a_topics, b_topics)
    if topic_j is not None and topic_j >= 0.25:
        support_points += 1
        reasons.append("lifetime_topic_overlap")

    if conflicting_orcid:
        conflicts.append("conflicting_nonempty_orcid")
    if len(a_works) == 0:
        conflicts.append("author_a_no_lifetime_plausible_work")
    if len(b_works) == 0:
        conflicts.append("author_b_no_lifetime_plausible_work")

    contamination_warning = any(
        share is not None and share > 0.50
        for share in (contam_a["outside_window_share"], contam_b["outside_window_share"])
    )
    if contamination_warning:
        reasons.append("temporal_contamination_over_50pct")

    if conflicts:
        review_label = "conflict"
    elif support_points >= 5 and not contamination_warning:
        review_label = "support"
    else:
        review_label = "needs_review"

    return {
        "candidate_birth_year": birth_year,
        "candidate_death_year": death_year,
        "plausible_career_year_min": lo,
        "plausible_career_year_max": hi,
        "author_id_a": a.author_id,
        "author_id_b": b.author_id,
        "orcid_a": a.orcid,
        "orcid_b": b.orcid,
        "same_orcid": same_orcid,
        "conflicting_orcid": conflicting_orcid,
        "lifetime_doi_overlap_n": len(doi_overlap),
        "lifetime_title_overlap_n": len(title_overlap),
        "lifetime_shared_coauthors_n": len(coauthor_overlap),
        "lifetime_coauthor_jaccard": jaccard(a_coauthors, b_coauthors),
        "lifetime_coauthor_overlap_coefficient": overlap_coefficient(a_coauthors, b_coauthors),
        "lifetime_shared_institutions_n": len(institution_overlap),
        "lifetime_institution_jaccard": jaccard(a_institutions, b_institutions),
        "lifetime_shared_topics_n": len(topic_overlap),
        "lifetime_topic_jaccard": topic_j,
        **temporal,
        "author_a_contamination": contam_a,
        "author_b_contamination": contam_b,
        "support_points_for_review_only": support_points,
        "support_reasons": reasons,
        "conflict_reasons": conflicts,
        "review_label": review_label,
    }


def read_fragment_queue(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row.get("review_class") == "possible_author_fragmentation"]


def parse_ids(value: str) -> list[str]:
    return [normalize_openalex_id(x) for x in (value or "").split(";") if x.strip()]


def fetch_evidence(
    client: OpenAlexClient,
    author_id: str,
    year_min: int,
    year_max: int,
    max_works: int,
) -> AuthorEvidence:
    author = client.get_author(author_id)
    works = list(
        client.iter_author_works(
            author_id,
            year_min,
            year_max,
            max_works=max_works,
        )
    )
    return AuthorEvidence(author_id=normalize_openalex_id(author_id), author=author, works=works)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("identity_review_queue", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--year-min", type=int, default=1800)
    parser.add_argument("--year-max", type=int, default=2026)
    parser.add_argument("--max-works-per-id", type=int, default=200)
    parser.add_argument("--sleep-rps", type=float, default=2.0)
    args = parser.parse_args()

    rows = read_fragment_queue(args.identity_review_queue)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    client = OpenAlexClient(
        api_key=os.getenv("OPENALEX_API_KEY") or None,
        requests_per_second=args.sleep_rps,
    )

    pairwise_path = args.out_dir / "cluster_pairwise_evidence.jsonl"
    profiles_path = args.out_dir / "cluster_author_profiles.jsonl"
    summary_path = args.out_dir / "cluster_evidence_summary.json"
    errors_path = args.out_dir / "cluster_evidence_errors.csv"

    errors: list[dict[str, str]] = []
    pair_counts = {"support": 0, "conflict": 0, "needs_review": 0}
    persons_completed = 0
    author_ids_fetched = 0
    contaminated_profiles_n = 0

    with pairwise_path.open("w", encoding="utf-8") as pair_file, profiles_path.open(
        "w", encoding="utf-8"
    ) as profile_file:
        for row in rows:
            person_id = row.get("person_id", "")
            name = row.get("canonical_name", "")
            birth_year = parse_year(row.get("birth_year"))
            death_year = parse_year(row.get("death_year"))
            lo, hi = career_window(birth_year, death_year)
            ids = parse_ids(row.get("plausible_openalex_ids", ""))
            evidences: list[AuthorEvidence] = []

            for author_id in ids:
                try:
                    evidence = fetch_evidence(
                        client,
                        author_id,
                        args.year_min,
                        args.year_max,
                        args.max_works_per_id,
                    )
                    evidences.append(evidence)
                    author_ids_fetched += 1
                    plausible = evidence.works_in_window(lo, hi)
                    outside = evidence.works_outside_window(lo, hi)
                    contamination = contamination_summary(
                        evidence, birth_year, death_year, lo, hi
                    )
                    if (
                        contamination["outside_window_share"] is not None
                        and contamination["outside_window_share"] > 0.50
                    ):
                        contaminated_profiles_n += 1
                    profile_file.write(
                        json.dumps(
                            {
                                "person_id": person_id,
                                "canonical_name": name,
                                "wikidata_qid": row.get("wikidata_qid", ""),
                                "birth_year": birth_year,
                                "death_year": death_year,
                                "plausible_career_year_min": lo,
                                "plausible_career_year_max": hi,
                                "author_id": evidence.author_id,
                                "display_name": evidence.author.get("display_name"),
                                "orcid": evidence.orcid,
                                "contamination": contamination,
                                "plausible_coauthors_n": len(evidence.coauthors(plausible)),
                                "plausible_institutions_n": len(evidence.institutions(plausible)),
                                "plausible_topics_n": len(evidence.topics(plausible)),
                                "representative_plausible_works": evidence.representative_works(plausible),
                                "representative_outside_window_works": evidence.representative_works(outside),
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                except Exception as exc:
                    errors.append(
                        {
                            "person_id": person_id,
                            "canonical_name": name,
                            "author_id": author_id,
                            "error": f"{type(exc).__name__}:{exc}",
                        }
                    )

            if len(evidences) >= 2:
                persons_completed += 1
            for a, b in combinations(evidences, 2):
                result = pairwise_evidence(a, b, birth_year, death_year)
                pair_counts[result["review_label"]] += 1
                pair_file.write(
                    json.dumps(
                        {
                            "person_id": person_id,
                            "canonical_name": name,
                            "wikidata_qid": row.get("wikidata_qid", ""),
                            **result,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )

    with errors_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["person_id", "canonical_name", "author_id", "error"],
        )
        writer.writeheader()
        writer.writerows(errors)

    summary = {
        "fragmentation_persons_input": len(rows),
        "fragmentation_persons_with_at_least_two_ids_fetched": persons_completed,
        "author_ids_fetched": author_ids_fetched,
        "author_profiles_with_gt50pct_temporal_contamination": contaminated_profiles_n,
        "pair_review_label_counts": pair_counts,
        "fetch_errors_n": len(errors),
        "year_min": args.year_min,
        "year_max": args.year_max,
        "max_works_per_id": args.max_works_per_id,
        "api_key_used": bool(os.getenv("OPENALEX_API_KEY")),
        "interpretation": (
            "Pair labels are lifetime-aware review-priority evidence only. They are "
            "not identity decisions and must not auto-create VERIFIED_CLUSTER."
        ),
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if author_ids_fetched else 2


if __name__ == "__main__":
    raise SystemExit(main())
