#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "resolve"))

from openalex_cluster_evidence import AuthorEvidence, pairwise_evidence  # noqa: E402


def authored_work(author_id: str, title: str, year: int, doi: str | None = None, coauthor: str | None = None):
    authorships = [{"author": {"id": f"https://openalex.org/{author_id}"}, "institutions": [{"id": "I1"}]}]
    if coauthor:
        authorships.append({"author": {"id": f"https://openalex.org/{coauthor}"}, "institutions": [{"id": "I1"}]})
    return {
        "doi": doi,
        "display_name": title,
        "publication_year": year,
        "authorships": authorships,
        "primary_topic": {"id": "T1"},
    }


class ClusterEvidenceTests(unittest.TestCase):
    def test_same_orcid_and_duplicate_lifetime_work_create_support_evidence(self) -> None:
        a = AuthorEvidence(
            "A1",
            {"orcid": "https://orcid.org/0000-0001"},
            [authored_work("A1", "A Distinctive Paper", 1950, "https://doi.org/10.1/example", "C1")],
        )
        b = AuthorEvidence(
            "A2",
            {"orcid": "0000-0001"},
            [authored_work("A2", "A Distinctive Paper", 1950, "10.1/example", "C1")],
        )
        result = pairwise_evidence(a, b, birth_year=1920, death_year=2000)
        self.assertTrue(result["same_orcid"])
        self.assertEqual(result["lifetime_doi_overlap_n"], 1)
        self.assertEqual(result["lifetime_title_overlap_n"], 1)
        self.assertEqual(result["review_label"], "support")

    def test_conflicting_orcid_is_conflict_even_with_same_name_context(self) -> None:
        a = AuthorEvidence("A1", {"orcid": "0000-0001"}, [authored_work("A1", "Paper A", 1950)])
        b = AuthorEvidence("A2", {"orcid": "0000-0002"}, [authored_work("A2", "Paper B", 1951)])
        result = pairwise_evidence(a, b, birth_year=1920, death_year=2000)
        self.assertTrue(result["conflicting_orcid"])
        self.assertEqual(result["review_label"], "conflict")

    def test_no_shared_lifetime_evidence_stays_needs_review(self) -> None:
        a = AuthorEvidence("A1", {}, [authored_work("A1", "Paper Alpha", 1950)])
        b = AuthorEvidence("A2", {}, [authored_work("A2", "Completely Different", 1960)])
        result = pairwise_evidence(a, b, birth_year=1920, death_year=2000)
        self.assertEqual(result["review_label"], "needs_review")
        self.assertEqual(result["support_points_for_review_only"], 0)

    def test_posthumous_namesake_record_cannot_create_false_support(self) -> None:
        # Models the failure found in the real pilot: a deceased candidate had a
        # same-name OpenAlex record whose only works were published much later.
        a = AuthorEvidence(
            "A1",
            {},
            [
                authored_work("A1", "Real Career Work", 2005, coauthor="C1"),
                authored_work("A1", "Real Career Work Two", 2010, coauthor="C2"),
            ],
        )
        b = AuthorEvidence(
            "A2",
            {},
            [
                authored_work("A2", "Namesake Work", 2026, coauthor="C1"),
                authored_work("A2", "Another Namesake Work", 2026, coauthor="C2"),
            ],
        )
        result = pairwise_evidence(a, b, birth_year=1967, death_year=2012)
        self.assertEqual(result["author_b_contamination"]["plausible_works_n"], 0)
        self.assertIn("author_b_no_lifetime_plausible_work", result["conflict_reasons"])
        self.assertEqual(result["review_label"], "conflict")

    def test_heavily_contaminated_record_cannot_be_auto_support(self) -> None:
        # Shared in-window context may exist, but a record mostly outside the
        # candidate lifespan is too contaminated to receive a support label.
        a = AuthorEvidence(
            "A1",
            {},
            [
                authored_work("A1", "Plausible A", 1940, coauthor="C1"),
                authored_work("A1", "Wrong Early", 1882),
                authored_work("A1", "Wrong Late", 2016),
                authored_work("A1", "Wrong Later", 2015),
            ],
        )
        b = AuthorEvidence(
            "A2",
            {},
            [
                authored_work("A2", "Plausible B", 1941, coauthor="C1"),
                authored_work("A2", "Plausible C", 1942, coauthor="C2"),
            ],
        )
        result = pairwise_evidence(a, b, birth_year=1902, death_year=1980)
        self.assertGreater(result["author_a_contamination"]["outside_window_share"], 0.5)
        self.assertNotEqual(result["review_label"], "support")


if __name__ == "__main__":
    unittest.main(verbosity=2)
