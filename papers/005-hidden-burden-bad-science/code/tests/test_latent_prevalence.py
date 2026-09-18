from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from latent_prevalence import fit, pattern_prob  # noqa: E402


def rows_from_patterns(patterns, N=1000000):
    rows = []
    i = 0
    for (a, b), n in patterns.items():
        for _ in range(n):
            i += 1
            rows.append({
                "paper_id": f"P{i}",
                "audit_stratum": "s",
                "stratum_population_N": str(N),
                "a_binary_severe": "" if a is None else str(a),
                "b_binary_severe": "" if b is None else str(b),
            })
    return rows


class LatentPrevalenceTests(unittest.TestCase):
    def test_pattern_probability_perfect_tests(self):
        self.assertAlmostEqual(
            pattern_prob(0.01, 1, 1, 1.0, 1.0, 1.0, 1.0),
            0.01,
        )
        self.assertAlmostEqual(
            pattern_prob(0.01, 0, 0, 1.0, 1.0, 1.0, 1.0),
            0.99,
        )
        self.assertAlmostEqual(
            pattern_prob(0.01, None, 1, 0.9, 0.99, 0.8, 0.999),
            0.01 * 0.8 + 0.99 * 0.001,
        )

    def test_synthetic_recovery_near_half_percent(self):
        # Approximate expected 2-test pattern counts for:
        # p=.005, A Se=.90 Sp=.999, B Se=.92 Sp=.9995.
        patterns = {
            (1, 1): 41,
            (1, 0): 14,
            (0, 1): 10,
            (0, 0): 9935,
        }
        rows = rows_from_patterns(patterns)
        calibration = {
            "AI_A": {"tp": 9000, "fn": 1000, "tn": 999000, "fp": 1000},
            "AI_B": {"tp": 9200, "fn": 800, "tn": 999500, "fp": 500},
        }
        out = fit(
            rows,
            calibration,
            draws=300,
            seed=7,
            grid_points=500,
            p_max=0.03,
        )
        median = out["global_prevalence"]["median"]
        self.assertGreater(median, 0.002)
        self.assertLess(median, 0.008)
        self.assertLess(out["global_prevalence"]["q025"], 0.0055)
        self.assertGreater(out["global_prevalence"]["q975"], 0.0045)

    def test_both_missing_adds_no_forced_negative(self):
        rows = rows_from_patterns({
            (1, 1): 4,
            (0, 0): 990,
            (None, None): 6,
        })
        calibration = {
            "AI_A": {"tp": 900, "fn": 100, "tn": 9990, "fp": 10},
            "AI_B": {"tp": 900, "fn": 100, "tn": 9990, "fp": 10},
        }
        out = fit(
            rows,
            calibration,
            draws=80,
            seed=8,
            grid_points=300,
            p_max=0.05,
        )
        self.assertEqual(
            out["sample"]["both_measurements_missing_by_stratum"]["s"],
            6,
        )


if __name__ == "__main__":
    unittest.main()
