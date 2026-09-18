import math
import unittest

from sb_metrics import awakening_time, beauty_coefficient, peak_time, retrospective_summary


class SleepingBeautyMetricTests(unittest.TestCase):
    def test_dormant_then_spike_has_positive_beauty(self):
        citations = [0, 0, 0, 1, 10, 20]
        self.assertAlmostEqual(beauty_coefficient(citations), 23.6)
        self.assertEqual(awakening_time(citations), 3)
        self.assertEqual(peak_time(citations), 5)

    def test_immediate_peak_has_zero_beauty(self):
        citations = [10, 8, 6, 4, 2, 1]
        self.assertEqual(peak_time(citations), 0)
        self.assertEqual(beauty_coefficient(citations), 0.0)
        self.assertEqual(awakening_time(citations), 0)

    def test_stronger_delayed_curve(self):
        citations = [0, 1, 0, 0, 2, 20, 50]
        self.assertAlmostEqual(beauty_coefficient(citations), 65.75)
        self.assertEqual(awakening_time(citations), 4)

    def test_earliest_peak_tie_policy(self):
        citations = [0, 5, 5, 1]
        self.assertEqual(peak_time(citations), 1)

    def test_summary_is_unlabeled(self):
        result = retrospective_summary([0, 0, 1, 5])
        self.assertIn("beauty_coefficient", result)
        self.assertNotIn("is_sleeping_beauty", result)

    def test_invalid_inputs(self):
        for bad in ([], [-1, 0, 1], [0, math.inf, 1], [0, math.nan, 1]):
            with self.assertRaises(ValueError):
                beauty_coefficient(bad)


if __name__ == "__main__":
    unittest.main()
