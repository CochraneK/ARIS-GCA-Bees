from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from prepare_dual_ai_latent_input import prepare  # noqa: E402


class PrepareLatentInputTests(unittest.TestCase):
    def test_preserves_sampling_design_and_unresolved_as_missing(self):
        manager = [
            {
                "assignment_id": "A1",
                "paper_id": "P1",
                "reviewer_id": "AI_A",
                "openalex_id": "W1",
                "doi": "",
                "publication_year": "2020",
                "primary_domain": "Health Sciences",
                "audit_stratum": "2020_2024",
                "stratum_population_N": "100000",
                "stratum_sample_n": "1000",
                "aris_inclusion_probability": "0.01",
                "aris_design_weight": "100",
            },
            {
                "assignment_id": "B1",
                "paper_id": "P1",
                "reviewer_id": "AI_B",
                "openalex_id": "W1",
                "doi": "",
                "publication_year": "2020",
                "primary_domain": "Health Sciences",
                "audit_stratum": "2020_2024",
                "stratum_population_N": "100000",
                "stratum_sample_n": "1000",
                "aris_inclusion_probability": "0.01",
                "aris_design_weight": "100",
            },
        ]
        ai_a = [{
            "assignment_id": "A1",
            "paper_id": "P1",
            "scientific_state": "SERIOUS_UNRESOLVED",
            "review_confidence": "LOW",
        }]
        ai_b = [{
            "assignment_id": "B1",
            "paper_id": "P1",
            "scientific_state": "NO_MATERIAL_PROBLEM_FOUND",
            "review_confidence": "HIGH",
        }]

        rows, summary = prepare(ai_a, ai_b, manager)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["audit_stratum"], "2020_2024")
        self.assertEqual(rows[0]["stratum_population_N"], "100000")
        self.assertEqual(rows[0]["a_binary_severe"], "")
        self.assertEqual(rows[0]["b_binary_severe"], "0")
        self.assertEqual(summary["a_unresolved_or_indeterminate"], 1)
        self.assertEqual(summary["b_unresolved_or_indeterminate"], 0)

    def test_severe_is_only_positive(self):
        manager = []
        a = []
        b = []
        states = [
            ("P1", "SEVERE_SUPPORTED", "1"),
            ("P2", "HONEST_MAJOR_ERROR", "0"),
            ("P3", "MINOR_OR_IMMATERIAL", "0"),
            ("P4", "NO_MATERIAL_PROBLEM_FOUND", "0"),
            ("P5", "INDETERMINATE", ""),
        ]
        for i, (paper, state, _) in enumerate(states):
            for reviewer, prefix in (("AI_A", "A"), ("AI_B", "B")):
                aid = f"{prefix}{i}"
                manager.append({
                    "assignment_id": aid,
                    "paper_id": paper,
                    "reviewer_id": reviewer,
                    "openalex_id": f"W{i}",
                    "audit_stratum": "s",
                    "stratum_population_N": "100",
                    "stratum_sample_n": "5",
                    "aris_inclusion_probability": "0.05",
                    "aris_design_weight": "20",
                })
                row = {
                    "assignment_id": aid,
                    "paper_id": paper,
                    "scientific_state": state,
                    "review_confidence": "HIGH",
                }
                (a if reviewer == "AI_A" else b).append(row)

        rows, _ = prepare(a, b, manager)
        observed = {r["paper_id"]: r["a_binary_severe"] for r in rows}
        for paper, _, expected in states:
            self.assertEqual(observed[paper], expected)


if __name__ == "__main__":
    unittest.main()
