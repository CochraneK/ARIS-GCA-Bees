import itertools
import math
import unittest

import numpy as np

import effect_size as eff


class EffectSizeTest(unittest.TestCase):
    def test_fixed_margin_variance_matches_bruteforce(self):
        births = [0, 0, 1]
        deaths = [0, 1, 1]
        xs = []
        for perm in set(itertools.permutations(deaths)):
            xs.append(
                sum(
                    1
                    for b, d in zip(births, perm)
                    if d == b
                )
            )
        brute_mean = float(np.mean(xs))
        brute_var = float(np.var(xs))
        mean, var = eff.fixed_margin_mean_variance(
            [2, 1], [1, 2], offset=0
        )
        self.assertAlmostEqual(mean, brute_mean, places=12)
        self.assertAlmostEqual(var, brute_var, places=12)

    def test_practical_null_equivalence(self):
        cls = eff.practical_classification(
            1.001, 0.997, 1.006, 0.996, 1.007
        )
        self.assertEqual(cls, "practically-null-equivalent")

    def test_substantive_positive(self):
        cls = eff.practical_classification(
            1.03, 1.02, 1.04, 1.018, 1.042
        )
        self.assertEqual(cls, "substantive-positive")

    def test_attenuation_categories(self):
        self.assertEqual(
            eff.attenuation_class(1.04, 1.039),
            "magnitude-consistent",
        )
        self.assertEqual(
            eff.attenuation_class(1.04, 0.99),
            "sign-reversal",
        )

    def test_temporal_stability(self):
        values = [1.02] * 7 + [0.999, 0.998]
        frac = eff.temporal_direction_fraction(values, 1.015)
        self.assertAlmostEqual(frac, 7 / 9)


if __name__ == "__main__":
    unittest.main()
