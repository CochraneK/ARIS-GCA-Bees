#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "network"))

from acquire_downstream_neighborhood import select_anchors  # noqa: E402


class DownstreamAnchorTests(unittest.TestCase):
    def test_anchor_selection_preserves_temporal_spread_then_high_citation(self) -> None:
        rows = [
            {"openalex_work_id": "W1", "publication_year": 1900, "cited_by_count": 1},
            {"openalex_work_id": "W2", "publication_year": 1910, "cited_by_count": 100},
            {"openalex_work_id": "W3", "publication_year": 1920, "cited_by_count": 2},
            {"openalex_work_id": "W4", "publication_year": 1930, "cited_by_count": 50},
            {"openalex_work_id": "W5", "publication_year": 1940, "cited_by_count": 3},
        ]
        anchors = select_anchors(rows, 4)
        ids = [row["openalex_work_id"] for row in anchors]
        self.assertEqual(ids[:3], ["W1", "W3", "W5"])
        self.assertEqual(ids[3], "W2")

    def test_anchor_selection_deduplicates_temporal_landmarks(self) -> None:
        rows = [
            {"openalex_work_id": "W1", "publication_year": 1900, "cited_by_count": 5},
            {"openalex_work_id": "W2", "publication_year": 1910, "cited_by_count": 4},
        ]
        anchors = select_anchors(rows, 6)
        self.assertEqual({row["openalex_work_id"] for row in anchors}, {"W1", "W2"})
        self.assertEqual(len(anchors), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
