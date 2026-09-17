#!/usr/bin/env python3
"""Collect pairwise evidence for plausible OpenAlex author fragments.

This script is a review aid, NOT an automatic identity merger. For every
candidate marked as possible fragmentation, it fetches bounded author/work data
for each plausible OpenAlex Author ID and summarizes pairwise evidence:

- ORCID agreement/conflict
- duplicate DOI / normalized-title overlap
- shared coauthors
- shared institutions
- topic overlap
- publication-year overlap
- representative works

The resulting `support`, `conflict`, and `needs_review` labels prioritize human
identity review under process/IDENTITY_CODEBOOK.md. They are not confirmatory
identity decisions and must never be converted directly into VERIFIED_CLUSTER.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
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


def iter_topic_ids(author: dict[str, Any], works: list[dict[str, Any]]) -> Iterable[str]:
    for topic in author.get("topics") or []:
        tid = str(topic.get("id") or "").strip()
        if tid:
            yield tid
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

    @property
    def dois(self) -> set[str]:
        return {key for work in self.works if (key := work_doi_key(work))}

    @property
    def titles(self) -> set[str]:
        return {
            key
            for work in self.works
            if (key := work_title_key(work)) and len(key) >= 8
        }

    @property
    def coauthors(self) -> set[str]:
        return {
            aid
            for work in self.works
            for aid in iter_coauthors(work, self.author_id)
        }

    @property
    def institutions(self) -> set[str]:
        ids = {
            str(inst.get("id") or "").strip()
            for inst in self.author.get("last_known_institutions") or []
            if inst.get("id")
        }
        ids.update(
            iid
            for work in self.works
            for iid in iter_authorship_institutions(work)
        )
        return {x for x in ids if x}

    @property
    def topics(self) -> set[str]:
        return set(iter_topic_ids(self.author, self.works))

    @property
    def years(self) -> set[int]:
        return {
            year
            for work in self.works
            if (year := safe_year(work.get("publication_year"))) is not None
        }

    def representative_works(self, n: int = 5) -> list[dict[str, Any]]:
        ordered = sorted(
            self.works,
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


def pairwise_evidence(a: AuthorEvidence, b: AuthorEvidence) -> dict[str, Any]:
    doi_overlap = a.dois & b.dois
    title_overlap = a.titles & b.titles
    coauthor_overlap = a.coauthors & b.coauthors
    institution_overlap = a.institutions & b.institutions
    topic_overlap = a.topics & b.topics
    temporal = temporal_summary(a.years, b.years)

    same_orcid = bool(a.orcid and b.orcid and a.orcid == b.orcid)
    conflicting_orcid = bool(a.orcid and b.orcid and a.orcid != b.orcid)

    # This score is strictly a *review-priority heuristic*. It is deliberately
    # transparent and is never used as an automatic merge threshold.
    support_points = 0
    reasons: list[str] = []
    conflicts: list[str] = []

    if same_orcid:
        support_points += 8
        reasons.append("same_nonempty_orcid")
    if doi_overlap:
        support_points += 5
        reasons.append("duplicate_doi")
    if title_overlap:
        support_points += 3
        reasons.append("normalized_title_overlap")
    if len(coauthor_overlap) >= 2:
        support_points += 3
        reasons.append("multiple_shared_coauthors")
    elif len(coauthor_overlap) == 1:
        support_points += 1
        reasons.append("one_shared_coauthor")
    if institution_overlap:
        support_points += 2
        reasons.append("shared_institution")
    topic_j = jaccard(a.topics, b.topics)
    if topic_j is not None and topic_j >= 0.25:
        support_points += 1
        reasons.append("topic_overlap")

    if conflicting_orcid:
        conflicts.append("conflicting_nonempty_orcid")
    if temporal["year_gap"] is not None and temporal["year_gap"] > 60:
        conflicts.append("extreme_publication_year_gap")

    if conflicts:
        review_label = "conflict"
    elif support_points >= 5:
        review_label = "support"
    else:
        review_label = "needs_review"

    return {
        "author_id_a": a.author_id,
        "author_id_b": b.author_id,
        "orcid_a": a.orcid,
        "orcid_b": b.orcid,
        "same_orcid": same_orcid,
        "conflicting_orcid": conflicting_orcid,
        "doi_overlap_n": len(doi_overlap),
        "title_overlap_n": len(title_overlap),
        "shared_coauthors_n": len(coauthor_overlap),
        "coauthor_jaccard": jaccard(a.coauthors, b.coauthors),
        "coauthor_overlap_coefficient": overlap_coefficient(a.coauthors, b.coauthors),
        "shared_institutions_n": len(institution_overlap),
        "institution_jaccard": jaccard(a.institutions, b.institutions),
        "shared_topics_n": len(topic_overlap),
        "topic_jaccard": topic_j,
        **temporal,
        "works_a_n": len(a.works),
        "works_b_n": len(b.works),
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
    parser.add_argument("--year-max", type=int, default=2005)
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

    with pairwise_path.open("w", encoding="utf-8") as pair_file, profiles_path.open(
        "w", encoding="utf-8"
    ) as profile_file:
        for row in rows:
            person_id = row.get("person_id", "")
            name = row.get("canonical_name", "")
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
                    profile_file.write(
                        json.dumps(
                            {
                                "person_id": person_id,
                                "canonical_name": name,
                                "wikidata_qid": row.get("wikidata_qid", ""),
                                "author_id": evidence.author_id,
                                "display_name": evidence.author.get("display_name"),
                                "orcid": evidence.orcid,
                                "api_works_count": evidence.author.get("works_count"),
                                "fetched_works_n": len(evidence.works),
                                "year_min": min(evidence.years) if evidence.years else None,
                                "year_max": max(evidence.years) if evidence.years else None,
                                "coauthors_n": len(evidence.coauthors),
                                "institutions_n": len(evidence.institutions),
                                "topics_n": len(evidence.topics),
                                "representative_works": evidence.representative_works(),
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
                result = pairwise_evidence(a, b)
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
        "pair_review_label_counts": pair_counts,
        "fetch_errors_n": len(errors),
        "year_min": args.year_min,
        "year_max": args.year_max,
        "max_works_per_id": args.max_works_per_id,
        "api_key_used": bool(os.getenv("OPENALEX_API_KEY")),
        "interpretation": (
            "Pair labels are review-priority evidence only. They are not identity "
            "decisions and must not be used to auto-create VERIFIED_CLUSTER."
        ),
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if author_ids_fetched else 2


if __name__ == "__main__":
    raise SystemExit(main())
