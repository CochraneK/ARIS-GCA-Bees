from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from batch_citation_ai_packets import batch_rows  # noqa: E402


class CitationBatchTests(unittest.TestCase):
    def test_batches_two_adjudicators(self):
        rows = []
        for adjudicator in ("A", "B"):
            for i in range(5):
                rows.append({
                    "assignment_id": f"{adjudicator}{i}",
                    "edge_id": f"E{i}",
                    "adjudicator_id": adjudicator,
                })
        batched, manifest = batch_rows(rows, 2)
        self.assertEqual(manifest["assignments_total"], 10)
        self.assertEqual(manifest["adjudicators"]["A"], 5)
        self.assertEqual(len(batched["A"]), 3)
        self.assertEqual(len(manifest["batches"]), 6)

    def test_duplicate_assignment_fails(self):
        rows = [
            {"assignment_id": "A1", "edge_id": "E1", "adjudicator_id": "A"},
            {"assignment_id": "A1", "edge_id": "E2", "adjudicator_id": "B"},
        ]
        with self.assertRaises(ValueError):
            batch_rows(rows, 10)


if __name__ == "__main__":
    unittest.main()
