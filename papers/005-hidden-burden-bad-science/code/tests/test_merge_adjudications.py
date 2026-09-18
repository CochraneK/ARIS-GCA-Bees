from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from merge_adjudications import merge  # noqa: E402


class MergeAdjudicationTests(unittest.TestCase):
    def test_valid_double_coding_and_disagreement_are_preserved(self):
        manager = [
            {
                "assignment_id": "A1",
                "paper_id": "P1",
                "reviewer_id": "R1",
                "review_round": "1",
                "aris_design_weight": "10",
                "det_formal_retraction": "1",
            },
            {
                "assignment_id": "A2",
                "paper_id": "P1",
                "reviewer_id": "R2",
                "review_round": "1",
                "aris_design_weight": "10",
                "det_formal_retraction": "1",
            },
        ]
        reviews = [
            {
                "assignment_id": "A1",
                "paper_id": "P1",
                "scientific_state": "SEVERE_SUPPORTED",
                "materiality": "MATERIAL",
                "misconduct_evidence": "FORMAL_FINDING",
                "review_confidence": "HIGH",
            },
            {
                "assignment_id": "A2",
                "paper_id": "P1",
                "scientific_state": "SERIOUS_UNRESOLVED",
                "materiality": "POTENTIALLY_MATERIAL",
                "misconduct_evidence": "SUSPECTED_NOT_ESTABLISHED",
                "review_confidence": "MEDIUM",
            },
        ]
        merged, qa = merge(reviews, manager)
        self.assertEqual(len(merged), 2)
        self.assertEqual(qa["double_coded_papers"], 1)
        self.assertEqual(qa["disagreement_count"], 1)
        self.assertIn("aris_design_weight", merged[0])
        self.assertIn("det_formal_retraction", merged[0])

    def test_invalid_state_fails_closed(self):
        manager = [
            {
                "assignment_id": "A1",
                "paper_id": "P1",
                "reviewer_id": "R1",
                "review_round": "1",
            }
        ]
        reviews = [
            {
                "assignment_id": "A1",
                "paper_id": "P1",
                "scientific_state": "FRAUD",
                "materiality": "MATERIAL",
                "misconduct_evidence": "FORMAL_FINDING",
                "review_confidence": "HIGH",
            }
        ]
        with self.assertRaises(ValueError):
            merge(reviews, manager)


if __name__ == "__main__":
    unittest.main()
