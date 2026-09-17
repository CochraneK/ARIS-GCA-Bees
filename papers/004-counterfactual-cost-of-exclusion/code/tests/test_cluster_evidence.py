#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "resolve"))

from cluster_evidence_guard import guard_pair_evidence  # noqa: E402
from openalex_cluster_evidence import AuthorEvidence, pairwise_evidence  # noqa: E402


def authored_work(
    author_id: str,
    title: str,
    year: int,
    doi: str | None = None,
    coauthor: str | None = None,
    institution: str = "I1",
    topic: str = "T1",
):
    authorships = [
        {
            "author": {"id": f"https://openalex.org/{author_id}"},
            "institutions": [{"id": institution}] if institution else [],
        }
    ]
    if coauthor:
        authorships.append(
            {
                "author": {"id": f"https://openalex.org/{coauthor}"},
                "institutions": [{"id": institution}] if institution else [],
            }
        )
    return {
        "doi": doi,
        "display_name": title,
        "publication_year": year,
        "authorships": authorships,
        "primary_topic": {"id": topic} if topic else {},
    }


def guarded(a: AuthorEvidence, b: AuthorEvidence, birth: int, death: int):
    return guard_pair_evidence(pairwise_evidence(a, b, birth_year=birth, death_year=death))


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
        result = guarded(a, b, 1920, 2000)
        self.assertTrue(result["same_orcid"])
        self.assertEqual(result["lifetime_doi_overlap_n"], 1)
        self.assertEqual(result["lifetime_title_overlap_n"], 1)
        self.assertTrue(result["strong_identity_anchor"])
        self.assertEqual(result["guarded_review_label"], "support")

    def test_conflicting_orcid_is_conflict_even_with_same_name_context(self) -> None:
        a = AuthorEvidence("A1", {"orcid": "0000-0001"}, [authored_work("A1", "Paper A", 1950)])
        b = AuthorEvidence("A2", {"orcid": "0000-0002"}, [authored_work("A2", "Paper B", 1951)])
        result = guarded(a, b, 1920, 2000)
        self.assertTrue(result["conflicting_orcid"])
        self.assertEqual(result["guarded_review_label"], "conflict")

    def test_weak_shared_context_stays_needs_review(self) -> None:
        # Same institution/topic alone are weak contextual similarity, not a
        # fragment identity anchor. The 3 raw heuristic points are expected.
        a = AuthorEvidence("A1", {}, [authored_work("A1", "Paper Alpha", 1950)])
        b = AuthorEvidence("A2", {}, [authored_work("A2", "Completely Different", 1960)])
        result = guarded(a, b, 1920, 2000)
        self.assertEqual(result["support_points_for_review_only"], 3)
        self.assertFalse(result["strong_identity_anchor"])
        self.assertEqual(result["guarded_review_label"], "needs_review")

    def test_low_proportion_coauthor_overlap_cannot_anchor_support(self) -> None:
        # Models the residual Fritz Strassmann false-positive pattern: two shared
        # coauthors plus an institution can accumulate 5 raw points even though
        # they are tiny fractions of large, topically unrelated neighborhoods.
        a_works = [
            authored_work("A1", f"Chemistry {i}", 1940 + i % 20, coauthor=f"A_CO_{i}", topic="CHEM")
            for i in range(40)
        ]
        b_works = [
            authored_work("A2", "Medical One", 1928, coauthor="A_CO_1", topic="MED"),
            authored_work("A2", "Medical Two", 1933, coauthor="A_CO_2", topic="MED"),
        ]
        a = AuthorEvidence("A1", {}, a_works)
        b = AuthorEvidence("A2", {}, b_works)
        result = guarded(a, b, 1902, 1980)
        self.assertEqual(result["lifetime_shared_coauthors_n"], 2)
        self.assertEqual(result["raw_review_label"], "support")
        self.assertLess(result["lifetime_coauthor_overlap_coefficient"], 0.10)
        self.assertFalse(result["strong_identity_anchor"])
        self.assertEqual(result["guarded_review_label"], "needs_review")
        self.assertEqual(result["guard_action"], "downgrade_weak_context_only_support")

    def test_posthumous_namesake_record_cannot_create_false_support(self) -> None:
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
        result = guarded(a, b, 1967, 2012)
        self.assertEqual(result["author_b_contamination"]["plausible_works_n"], 0)
        self.assertIn("author_b_no_lifetime_plausible_work", result["conflict_reasons"])
        self.assertEqual(result["guarded_review_label"], "conflict")

    def test_heavily_contaminated_record_cannot_be_auto_support(self) -> None:
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
        result = guarded(a, b, 1902, 1980)
        self.assertGreater(result["author_a_contamination"]["outside_window_share"], 0.5)
        self.assertNotEqual(result["guarded_review_label"], "support")


if __name__ == "__main__":
    unittest.main(verbosity=2)
