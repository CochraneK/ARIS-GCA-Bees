from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from merge_ai_adjudications import merge  # noqa: E402


def row(aid, adjudicator, state, materiality="MATERIAL", confidence="HIGH", formal="NO"):
    return {
        "assignment_id": aid,
        "paper_id": "P1",
        "adjudicator_id": adjudicator,
        "scientific_state": state,
        "materiality": materiality,
        "review_confidence": confidence,
        "formal_finding_seen": formal,
        "model_name": adjudicator,
        "model_version_or_snapshot": "v1",
        "evidence_locator": "notice",
    }


class AIConsensusTests(unittest.TestCase):
    def test_exact_high_confidence_agreement_auto_consensus(self):
        a = [row("A1", "M1", "SEVERE_SUPPORTED")]
        b = [row("A1", "M2", "SEVERE_SUPPORTED")]
        consensus, arbitration, summary = merge(a, b)
        self.assertEqual(len(consensus), 1)
        self.assertEqual(len(arbitration), 0)
        self.assertEqual(consensus[0]["label_provenance"], "AI_DUAL_AGREEMENT_NOT_GOLD_STANDARD")

    def test_state_disagreement_routes_to_arbitration(self):
        a = [row("A1", "M1", "SEVERE_SUPPORTED")]
        b = [row("A1", "M2", "SERIOUS_UNRESOLVED")]
        consensus, arbitration, _ = merge(a, b)
        self.assertEqual(len(consensus), 0)
        self.assertIn("SCIENTIFIC_STATE_DISAGREEMENT", arbitration[0]["arbitration_reasons"])

    def test_low_confidence_routes_to_arbitration(self):
        a = [row("A1", "M1", "NO_MATERIAL_PROBLEM_FOUND", "IMMATERIAL", "LOW")]
        b = [row("A1", "M2", "NO_MATERIAL_PROBLEM_FOUND", "IMMATERIAL", "HIGH")]
        _, arbitration, _ = merge(a, b)
        self.assertIn("LOW_CONFIDENCE", arbitration[0]["arbitration_reasons"])

    def test_assignment_mismatch_fails_closed(self):
        with self.assertRaises(ValueError):
            merge([row("A1", "M1", "SEVERE_SUPPORTED")], [row("A2", "M2", "SEVERE_SUPPORTED")])


if __name__ == "__main__":
    unittest.main()
