import math
import unittest

from age_mappings import (
    SpeciesTime,
    age_from_loglinear,
    age_from_relative,
    loglinear_coordinate,
    map_by_loglinear,
    map_by_relative_age,
    relative_age,
)


class AgeMappingTests(unittest.TestCase):
    def setUp(self):
        self.human = SpeciesTime("human", 280 / 365.25, 13.5, 122.5)
        self.mouse = SpeciesTime("mouse", 19 / 365.25, 42 / 365.25, 4.0)

    def test_relative_round_trip(self):
        for age in (0.0, 0.1, 1.0, 3.0):
            self.assertAlmostEqual(
                age_from_relative(relative_age(age, self.mouse), self.mouse),
                age,
                places=10,
            )

    def test_loglinear_round_trip(self):
        for age in (0.0, 0.1, 1.0, 3.0):
            y = loglinear_coordinate(age, self.mouse)
            self.assertAlmostEqual(age_from_loglinear(y, self.mouse), age, places=10)

    def test_identity_mapping(self):
        for age in (0.0, 0.1, 1.0, 3.0):
            self.assertAlmostEqual(
                map_by_relative_age(age, self.mouse, self.mouse), age, places=10
            )
            self.assertAlmostEqual(
                map_by_loglinear(age, self.mouse, self.mouse), age, places=10
            )

    def test_monotonicity(self):
        ages = [0.0, 0.1, 0.5, 1.0, 2.0, 3.0]
        rel = [map_by_relative_age(a, self.mouse, self.human) for a in ages]
        loglin = [map_by_loglinear(a, self.mouse, self.human) for a in ages]
        self.assertTrue(all(b > a for a, b in zip(rel, rel[1:])))
        self.assertTrue(all(b > a for a, b in zip(loglin, loglin[1:])))

    def test_finite_values(self):
        for age in (0.0, 0.1, 1.0, 3.0):
            self.assertTrue(math.isfinite(map_by_relative_age(age, self.mouse, self.human)))
            self.assertTrue(math.isfinite(map_by_loglinear(age, self.mouse, self.human)))


if __name__ == "__main__":
    unittest.main()
