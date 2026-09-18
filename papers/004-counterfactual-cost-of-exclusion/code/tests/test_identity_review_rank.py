#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "resolve"))

from rank_identity_review import rank_packet  # noqa: E402


class IdentityReviewRankTests(unittest.TestCase):
    def test_single_with_authority_outranks_fragmented_case(self) -> None:
        single = {
            "person_id": "p1",
            "canonical_name": "A",
            "review_class": "single_plausible_author_record",
            "plausible_openalex_ids": ["A1"],
            "openalex_profiles": [{"contamination": {"outside_fraction": 0.05}}],
            "authority_evidence": {"viaf": ["1"], "occupations": [{"label": "scientist"}]},
        }
        cluster = {
            "person_id": "p2",
            "canonical_name": "B",
            "review_class": "possible_author_fragmentation",
            "plausible_openalex_ids": ["A2", "A3", "A4"],
            "openalex_profiles": [],
            "authority_evidence": {},
        }
        self.assertGreater(rank_packet(single)["priority_score"], rank_packet(cluster)["priority_score"])

    def test_no_graph_is_closed_bucket_not_confidence_score(self) -> None:
        packet = {
            "person_id": "p1",
            "canonical_name": "A",
            "review_class": "no_openalex_search_hit",
            "plausible_openalex_ids": [],
            "openalex_profiles": [],
            "authority_evidence": {},
        }
        result = rank_packet(packet)
        self.assertEqual(result["priority_bucket"], "closed_no_graph")
        self.assertFalse(result["mental_health_evidence_used"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
