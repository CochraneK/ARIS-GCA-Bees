from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from rly_cost import calculate  # noqa: E402


class RLYCostTests(unittest.TestCase):
    def test_empirical_total_requires_calibrated_conversion_and_components(self):
        cfg = {
            "hours_per_research_year": {
                "value": {"low": 1500, "central": 1800, "high": 2000},
                "calibration_status": "EMPIRICALLY_CALIBRATED",
                "evidence_id": "X",
            },
            "components": [
                {
                    "component_id": "C1",
                    "rly_component": "RLY-C",
                    "calibration_status": "EMPIRICALLY_CALIBRATED",
                    "overlap_group": "correction",
                    "evidence_id": "Y",
                    "affected_units": {"low": 100, "central": 120, "high": 140},
                    "hours_per_unit": {"low": 2, "central": 3, "high": 4},
                    "attribution_fraction": {"low": 0.5, "central": 0.7, "high": 0.9},
                }
            ],
        }
        out = calculate(cfg)
        self.assertTrue(out["empirical_total_allowed"])
        self.assertIn("empirical_rly", out)
        self.assertGreater(out["empirical_rly"]["central"], 0)

    def test_scenario_component_does_not_enter_empirical_total(self):
        cfg = {
            "hours_per_research_year": {
                "value": {"low": 1500, "central": 1800, "high": 2000},
                "calibration_status": "EMPIRICALLY_CALIBRATED",
                "evidence_id": "X",
            },
            "components": [
                {
                    "component_id": "C1",
                    "rly_component": "RLY-D",
                    "calibration_status": "SCENARIO_ONLY",
                    "overlap_group": "downstream",
                    "evidence_id": "",
                    "affected_units": {"low": 100, "central": 120, "high": 140},
                    "hours_per_unit": {"low": 2, "central": 3, "high": 4},
                    "attribution_fraction": {"low": 0.5, "central": 0.7, "high": 0.9},
                }
            ],
        }
        out = calculate(cfg)
        self.assertFalse(out["empirical_total_allowed"])
        self.assertIn("NO_EMPIRICALLY_CALIBRATED_COMPONENTS", out["empirical_rly_blocked_reasons"])
        self.assertGreater(out["scenario_rly"]["central"], 0)

    def test_overlap_conflict_blocks_empirical_total(self):
        base = {
            "rly_component": "RLY-P",
            "calibration_status": "EMPIRICALLY_CALIBRATED",
            "overlap_group": "same_labor",
            "evidence_id": "X",
            "affected_units": {"low": 10, "central": 10, "high": 10},
            "hours_per_unit": {"low": 2, "central": 2, "high": 2},
            "attribution_fraction": {"low": 1, "central": 1, "high": 1},
        }
        cfg = {
            "hours_per_research_year": {
                "value": {"low": 1800, "central": 1800, "high": 1800},
                "calibration_status": "EMPIRICALLY_CALIBRATED",
                "evidence_id": "X",
            },
            "components": [
                {"component_id": "A", **base},
                {"component_id": "B", **base},
            ],
        }
        out = calculate(cfg)
        self.assertFalse(out["empirical_total_allowed"])
        self.assertIn("same_labor", out["overlap_conflicts"])
        self.assertIn("OVERLAP_DOUBLE_COUNT_RISK", out["empirical_rly_blocked_reasons"])

    def test_not_identified_component_needs_no_fake_numbers(self):
        cfg = {
            "hours_per_research_year": {
                "value": {"low": 1800, "central": 1800, "high": 1800},
                "calibration_status": "SCENARIO_ONLY",
                "evidence_id": "",
            },
            "components": [
                {
                    "component_id": "U1",
                    "rly_component": "RLY-I",
                    "calibration_status": "NOT_IDENTIFIED",
                    "overlap_group": "review",
                    "evidence_id": "SRC_ACZEL_2021",
                    "reason_not_identified": "Attributable fraction unknown",
                }
            ],
        }
        out = calculate(cfg)
        self.assertEqual(out["components"][0]["identified"], False)
        self.assertEqual(out["scenario_rly"]["central"], 0.0)


if __name__ == "__main__":
    unittest.main()
