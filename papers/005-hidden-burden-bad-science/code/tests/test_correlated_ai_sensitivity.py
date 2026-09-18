from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from correlated_ai_sensitivity import (  # noqa: E402
    conditional_pattern_prob,
    joint_positive_cells,
    pattern_prob_correlated,
)
from latent_prevalence import pattern_prob


class CorrelatedAIErrorTests(unittest.TestCase):
    def test_joint_cells_preserve_marginals(self):
        cells = joint_positive_cells(0.9, 0.8, 0.6)
        self.assertAlmostEqual(cells[(1, 1)] + cells[(1, 0)], 0.9)
        self.assertAlmostEqual(cells[(1, 1)] + cells[(0, 1)], 0.8)
        self.assertAlmostEqual(sum(cells.values()), 1.0)

    def test_zero_dependence_matches_independence(self):
        p = pattern_prob_correlated(
            0.01,
            1,
            0,
            se_a=0.9,
            sp_a=0.99,
            se_b=0.8,
            sp_b=0.995,
            lambda_se=0.0,
            lambda_fpr=0.0,
        )
        q = pattern_prob(
            0.01,
            1,
            0,
            0.9,
            0.99,
            0.8,
            0.995,
        )
        self.assertAlmostEqual(p, q)

    def test_maximal_positive_dependence_increases_joint_false_positive(self):
        ind = conditional_pattern_prob(
            1, 1, z=0,
            se_a=0.9, sp_a=0.99,
            se_b=0.9, sp_b=0.995,
            lambda_se=0.0, lambda_fpr=0.0,
        )
        dep = conditional_pattern_prob(
            1, 1, z=0,
            se_a=0.9, sp_a=0.99,
            se_b=0.9, sp_b=0.995,
            lambda_se=0.0, lambda_fpr=1.0,
        )
        self.assertGreater(dep, ind)

    def test_missing_one_measurement_uses_marginal_only(self):
        low = conditional_pattern_prob(
            None, 1, z=1,
            se_a=0.9, sp_a=0.99,
            se_b=0.8, sp_b=0.995,
            lambda_se=0.0, lambda_fpr=0.0,
        )
        high = conditional_pattern_prob(
            None, 1, z=1,
            se_a=0.9, sp_a=0.99,
            se_b=0.8, sp_b=0.995,
            lambda_se=1.0, lambda_fpr=1.0,
        )
        self.assertAlmostEqual(low, 0.8)
        self.assertAlmostEqual(high, 0.8)


if __name__ == "__main__":
    unittest.main()
