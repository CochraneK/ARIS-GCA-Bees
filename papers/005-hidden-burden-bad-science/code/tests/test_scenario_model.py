from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from scenario_model import run_scenario  # noqa: E402


class ScenarioModelTests(unittest.TestCase):
    def setUp(self):
        self.params = {
            "scenario_name": "test",
            "annual_target_works": 1000,
            "paper_problem_prevalence": {"low": 0.01, "mode": 0.02, "high": 0.03},
            "direct_researcher_years_per_problematic_work": {
                "low": 0.5,
                "mode": 1.0,
                "high": 1.5,
            },
            "followup_probability": {"low": 0.1, "mode": 0.2, "high": 0.3},
            "followup_researcher_years_if_triggered": {
                "low": 0.25,
                "mode": 0.5,
                "high": 1.0,
            },
            "sleeping_beauty_extension": {"enabled": False},
            "simulation_draws": 500,
            "seed": 1,
        }

    def test_result_is_explicitly_scenario(self):
        result = run_scenario(self.params)
        self.assertEqual(result["classification"], "SCENARIO_NOT_EMPIRICAL_ESTIMATE")
        self.assertIn("warning", result)

    def test_outputs_are_nonnegative(self):
        result = run_scenario(self.params)
        for metric in result["metrics"].values():
            self.assertGreaterEqual(metric["p025"], 0)
            self.assertGreaterEqual(metric["median"], 0)
            self.assertGreaterEqual(metric["p975"], 0)

    def test_quantiles_are_ordered(self):
        result = run_scenario(self.params)
        for metric in result["metrics"].values():
            self.assertLessEqual(metric["p025"], metric["median"])
            self.assertLessEqual(metric["median"], metric["p975"])

    def test_reproducible_seed(self):
        first = run_scenario(self.params)
        second = run_scenario(self.params)
        self.assertEqual(first["metrics"], second["metrics"])


if __name__ == "__main__":
    unittest.main()
