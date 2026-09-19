from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from calibration_anchor_design import (  # noqa: E402
    build_design,
    ppv,
    required_n_for_zero_error_bound,
    zero_error_upper_bound,
)


class CalibrationAnchorDesignTests(unittest.TestCase):
    def test_required_n_hits_target(self):
        n = required_n_for_zero_error_bound(0.001, confidence=0.95)
        self.assertGreaterEqual(n, 2995)
        self.assertLessEqual(
            zero_error_upper_bound(n, confidence=0.95),
            0.001,
        )

    def test_smaller_n_misses_target(self):
        n = required_n_for_zero_error_bound(0.001, confidence=0.95)
        self.assertGreater(
            zero_error_upper_bound(n - 1, confidence=0.95),
            0.001,
        )

    def test_ppv_rare_event_specificity_matters(self):
        low = ppv(0.005, 0.9, 0.99)
        high = ppv(0.005, 0.9, 0.999)
        self.assertGreater(high, low)
        self.assertLess(low, 0.5)
        self.assertGreater(high, 0.8)

    def test_design_classification(self):
        out = build_design(confidence=0.95)
        self.assertEqual(
            out["classification"],
            "CALIBRATION_ANCHOR_ZERO_ERROR_DESIGN_NOT_MODEL_ACCURACY",
        )
        self.assertTrue(out["zero_error_design"])
        self.assertTrue(out["ppv_scenarios"])


if __name__ == "__main__":
    unittest.main()
