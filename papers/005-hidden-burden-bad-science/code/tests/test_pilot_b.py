from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from calibrate_detectors import summarize  # noqa: E402
from pilot_b_sample import (  # noqa: E402
    enrichment_stratum,
    probability_from_expected_target,
    sample_rows,
)


class PilotBSamplingTests(unittest.TestCase):
    def test_strata_are_mutually_exclusive(self):
        detectors = ["det_a", "det_b"]
        hs = {"det_a"}
        self.assertEqual(
            enrichment_stratum({"det_a": "1", "det_b": "1"}, detectors, hs),
            "high_specificity_positive",
        )
        self.assertEqual(
            enrichment_stratum({"det_a": "0", "det_b": "1"}, detectors, hs),
            "single_signal_positive",
        )
        self.assertEqual(
            enrichment_stratum({"det_a": "0", "det_b": "0"}, detectors, hs),
            "signal_negative",
        )
        self.assertEqual(
            enrichment_stratum({"det_a": "", "det_b": ""}, detectors, hs),
            "no_applicable_detector",
        )

    def test_probability_from_target_is_bounded(self):
        self.assertEqual(probability_from_expected_target(0, 100), 0.0)
        self.assertAlmostEqual(probability_from_expected_target(25, 100), 0.25)
        self.assertEqual(probability_from_expected_target(200, 100), 1.0)

    def test_sampled_rows_have_exact_union_probability(self):
        rows = []
        for i in range(1000):
            rows.append(
                {
                    "paper_id": str(i),
                    "det_a": "1" if i < 100 else "0",
                    "det_b": "1" if 100 <= i < 200 else "0",
                }
            )
        sampled = sample_rows(
            rows=rows,
            detector_cols=["det_a", "det_b"],
            high_specificity_cols={"det_a"},
            n_random=100,
            n_per_enrichment={
                "high_specificity_positive": 50,
                "single_signal_positive": 50,
                "signal_negative": 50,
            },
            seed=7,
        )
        self.assertGreater(len(sampled), 0)
        for row in sampled:
            pr = float(row["aris_pi_random"])
            pe = float(row["aris_pi_enrich"])
            pi = float(row["aris_inclusion_probability"])
            self.assertAlmostEqual(pi, 1 - (1 - pr) * (1 - pe), places=10)
            self.assertAlmostEqual(float(row["aris_design_weight"]), 1 / pi, places=8)


class DetectorCalibrationTests(unittest.TestCase):
    def test_weighted_calibration_separates_unresolved(self):
        rows = [
            {
                "scientific_state": "SEVERE_SUPPORTED",
                "aris_design_weight": "2",
                "aris_selected_via": "population_random",
                "det_a": "1",
            },
            {
                "scientific_state": "NO_MATERIAL_PROBLEM_FOUND",
                "aris_design_weight": "1",
                "aris_selected_via": "population_random",
                "det_a": "0",
            },
            {
                "scientific_state": "SERIOUS_UNRESOLVED",
                "aris_design_weight": "10",
                "aris_selected_via": "enrichment:single_signal_positive",
                "det_a": "1",
            },
        ]
        out = summarize(rows, ["det_a"], "scientific_state", "aris_design_weight")
        self.assertEqual(out["resolved_binary_rows"], 2)
        self.assertAlmostEqual(out["design_weighted_severe_prevalence"], 2 / 3)
        self.assertAlmostEqual(out["detectors"]["det_a"]["sensitivity"], 1.0)
        self.assertAlmostEqual(out["detectors"]["det_a"]["specificity"], 1.0)
        self.assertEqual(out["label_counts"]["SERIOUS_UNRESOLVED"], 1)


if __name__ == "__main__":
    unittest.main()
