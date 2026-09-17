#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "resolve"))

from openalex_cluster_evidence import AuthorEvidence, pairwise_evidence  # noqa: E402


class ClusterEvidenceTests(unittest.TestCase):
    def test_same_orcid_and_duplicate_work_create_support_evidence(self) -> None:
        a = AuthorEvidence(
            "A1",
            {"orcid": "https://orcid.org/0000-0001", "topics": [{"id": "T1"}]},
            [
                {
                    "doi": "https://doi.org/10.1/example",
                    "display_name": "A Distinctive Paper",
                    "publication_year": 1950,
                    "authorships": [
                        {"author": {"id": "https://openalex.org/A1"}, "institutions": [{"id": "I1"}]},
                        {"author": {"id": "https://openalex.org/C1"}, "institutions": [{"id": "I1"}]},
                    ],
                    "primary_topic": {"id": "T1"},
                }
            ],
        )
        b = AuthorEvidence(
            "A2",
            {"orcid": "0000-0001", "topics": [{"id": "T1"}]},
            [
                {
                    "doi": "10.1/example",
                    "display_name": "A Distinctive Paper",
                    "publication_year": 1950,
                    "authorships": [
                        {"author": {"id": "https://openalex.org/A2"}, "institutions": [{"id": "I1"}]},
                        {"author": {"id": "https://openalex.org/C1"}, "institutions": [{"id": "I1"}]},
                    ],
                    "primary_topic": {"id": "T1"},
                }
            ],
        )
        result = pairwise_evidence(a, b)
        self.assertTrue(result["same_orcid"])
        self.assertEqual(result["doi_overlap_n"], 1)
        self.assertEqual(result["title_overlap_n"], 1)
        self.assertEqual(result["review_label"], "support")

    def test_conflicting_orcid_is_conflict_even_with_same_name_context(self) -> None:
        a = AuthorEvidence("A1", {"orcid": "0000-0001"}, [])
        b = AuthorEvidence("A2", {"orcid": "0000-0002"}, [])
        result = pairwise_evidence(a, b)
        self.assertTrue(result["conflicting_orcid"])
        self.assertEqual(result["review_label"], "conflict")

    def test_no_shared_evidence_stays_needs_review(self) -> None:
        a = AuthorEvidence(
            "A1",
            {},
            [{"display_name": "Paper Alpha", "publication_year": 1900, "authorships": []}],
        )
        b = AuthorEvidence(
            "A2",
            {},
            [{"display_name": "Completely Different", "publication_year": 1910, "authorships": []}],
        )
        result = pairwise_evidence(a, b)
        self.assertEqual(result["review_label"], "needs_review")
        self.assertEqual(result["support_points_for_review_only"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
