#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "review"))

from select_identity_second_review import hash_fraction, select  # noqa: E402


class IdentitySecondReviewTests(unittest.TestCase):
    def test_clusters_and_collisions_are_always_selected(self) -> None:
        rows = [
            {"person_id": "p1", "canonical_name": "A", "identity_status": "VERIFIED_CLUSTER"},
            {"person_id": "p2", "canonical_name": "B", "identity_status": "AMBIGUOUS_COLLISION"},
            {"person_id": "p3", "canonical_name": "C", "identity_status": "EXCLUDED_IDENTITY_ERROR"},
        ]
        selected = select(rows, 0.0, "seed")
        self.assertEqual({row["person_id"] for row in selected}, {"p1", "p2", "p3"})

    def test_single_sampling_is_deterministic(self) -> None:
        rows = [
            {"person_id": f"p{i}", "canonical_name": str(i), "identity_status": "VERIFIED_SINGLE"}
            for i in range(20)
        ]
        a = select(rows, 0.25, "seed")
        b = select(rows, 0.25, "seed")
        self.assertEqual([row["person_id"] for row in a], [row["person_id"] for row in b])
        self.assertTrue(all(hash_fraction(row["person_id"], "seed") < 0.25 for row in a))

    def test_no_graph_not_in_precision_sample_by_default(self) -> None:
        rows = [{"person_id": "p1", "canonical_name": "A", "identity_status": "NO_GRAPH_RECORD"}]
        self.assertEqual(select(rows, 1.0, "seed"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
