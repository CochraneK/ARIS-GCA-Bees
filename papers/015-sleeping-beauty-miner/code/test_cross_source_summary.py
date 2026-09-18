import unittest

from cross_source_summary import summarize_results


class CrossSourceSummaryTests(unittest.TestCase):
    def test_summary(self):
        rows = [
            {
                "cross_source_difference": {
                    "beauty_coefficient_relative": 0.10,
                    "awakening_year": 0,
                }
            },
            {
                "cross_source_difference": {
                    "beauty_coefficient_relative": -0.20,
                    "awakening_year": -4,
                }
            },
        ]
        result = summarize_results(rows)
        self.assertEqual(result["n_cases"], 2)
        self.assertAlmostEqual(
            result["mean_absolute_relative_B_difference"],
            0.15,
        )
        self.assertAlmostEqual(
            result["mean_absolute_awakening_year_difference"],
            2.0,
        )
        self.assertEqual(result["max_absolute_awakening_year_difference"], 4)


if __name__ == "__main__":
    unittest.main()
