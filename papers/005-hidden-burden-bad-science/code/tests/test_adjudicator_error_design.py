from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from adjudicator_error_design import metrics, min_specificity_for_ppv, independent_and_consensus  # noqa: E402


class AdjudicatorErrorDesignTests(unittest.TestCase):
    def test_perfect_classifier(self):
        out = metrics(0.01, 1.0, 1.0)
        self.assertAlmostEqual(out["observed_positive_rate"], 0.01)
        self.assertAlmostEqual(out["ppv"], 1.0)

    def test_rare_prevalence_can_have_low_ppv(self):
        out = metrics(0.005, 0.9, 0.99)
        self.assertLess(out["ppv"], 0.5)

    def test_required_specificity_is_high_for_rare_outcome(self):
        required = min_specificity_for_ppv(0.005, 0.9, 0.8)
        self.assertGreater(required, 0.998)

    def test_independent_and_reduces_false_positive_rate(self):
        single = metrics(0.005, 0.9, 0.99)
        dual = independent_and_consensus(0.005, 0.9, 0.99)
        self.assertGreater(dual["specificity"], single["specificity"])


if __name__ == "__main__":
    unittest.main()
