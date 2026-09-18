from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from prevalence_design import beta_cdf, beta_ppf, binomial_rare, jeffreys_interval  # noqa: E402


class PrevalenceDesignTests(unittest.TestCase):
    def test_beta_ppf_inverts_cdf(self):
        for q in (0.025, 0.5, 0.975):
            x = beta_ppf(q, 2.5, 8.5)
            self.assertAlmostEqual(beta_cdf(x, 2.5, 8.5), q, places=7)

    def test_jeffreys_interval_is_ordered(self):
        lo, hi = jeffreys_interval(5, 1000)
        self.assertGreaterEqual(lo, 0)
        self.assertLess(lo, hi)
        self.assertLessEqual(hi, 1)

    def test_rare_binomial_sampler_is_reproducible(self):
        a = binomial_rare(random.Random(7), 1000, 0.01)
        b = binomial_rare(random.Random(7), 1000, 0.01)
        self.assertEqual(a, b)

    def test_zero_prevalence_gives_zero(self):
        self.assertEqual(binomial_rare(random.Random(1), 1000, 0.0), 0)


if __name__ == "__main__":
    unittest.main()
