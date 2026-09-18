import unittest

from mechanism_labels import (
    SCISCINET_V1_CALIBRATION,
    classify_mechanism_state,
    early_late_percentiles,
    robust_sleeping_beauty_gate,
    van_raan_gate,
    variable_van_raan_gate,
)


class MechanismLabelTests(unittest.TestCase):
    def test_van_raan_gate_passes_deep_sleep_then_wake(self):
        counts = [0] * 10 + [6, 7, 8, 9] + [10, 12]
        result = van_raan_gate(counts)
        self.assertTrue(result.passed)
        self.assertLessEqual(result.sleep_rate, 1.0)
        self.assertGreater(result.wake_rate, 5.0)

    def test_van_raan_gate_rejects_immediate_hit(self):
        counts = [10] * 10 + [20, 20, 20, 20]
        result = van_raan_gate(counts)
        self.assertFalse(result.passed)

    def test_robust_gate_requires_converging_evidence(self):
        counts = [0] * 10 + [6, 8, 10, 12] + [20, 30, 40, 50]
        result = robust_sleeping_beauty_gate(
            counts,
            min_total_citations=50,
        )
        self.assertTrue(result.van_raan.passed)
        self.assertTrue(result.b_high_pass)
        self.assertTrue(result.later_recognition_pass)
        self.assertTrue(result.robust_sb)
        self.assertEqual(result.state, "ROBUST_SLEEPING_BEAUTY")
        self.assertEqual(
            result.calibration["source"],
            SCISCINET_V1_CALIBRATION.source,
        )

    def test_variable_sleep_detects_long_delayed_wake(self):
        counts = [0] * 25 + [6, 8, 10, 12] + [20, 25]
        variable = variable_van_raan_gate(
            counts,
            min_sleep_years=5,
            wake_years=4,
        )
        fixed = van_raan_gate(
            counts,
            sleep_years=10,
            wake_years=4,
        )
        self.assertTrue(variable.passed)
        self.assertGreaterEqual(variable.sleep_years, 20)
        self.assertEqual(variable.mode, "VARIABLE_SLEEP")
        self.assertFalse(fixed.passed)

    def test_robust_gate_defaults_to_variable_sleep(self):
        counts = [0] * 25 + [6, 8, 10, 12] + [20, 25, 30, 40]
        result = robust_sleeping_beauty_gate(
            counts,
            min_total_citations=50,
        )
        self.assertEqual(result.van_raan.mode, "VARIABLE_SLEEP")
        self.assertTrue(result.van_raan.passed)
        self.assertTrue(result.robust_sb)

    def test_high_b_alone_is_not_enough(self):
        counts = [0] * 10 + [6, 6, 6, 6]
        result = robust_sleeping_beauty_gate(
            counts,
            min_total_citations=1000,
        )
        self.assertFalse(result.robust_sb)
        self.assertFalse(result.later_recognition_pass)

    def test_four_canonical_states(self):
        self.assertEqual(
            classify_mechanism_state(
                early_percentile=0.10,
                late_percentile=0.90,
                robust_sb=True,
            ).state,
            "SLEEPING_BEAUTY",
        )
        self.assertEqual(
            classify_mechanism_state(
                early_percentile=0.10,
                late_percentile=0.10,
                robust_sb=False,
            ).state,
            "FORGOTTEN",
        )
        self.assertEqual(
            classify_mechanism_state(
                early_percentile=0.90,
                late_percentile=0.90,
                robust_sb=False,
            ).state,
            "IMMEDIATE_HIT",
        )
        self.assertEqual(
            classify_mechanism_state(
                early_percentile=0.90,
                late_percentile=0.10,
                robust_sb=False,
            ).state,
            "FADING",
        )

    def test_low_early_high_late_without_robust_gate_is_not_called_sb(self):
        result = classify_mechanism_state(
            early_percentile=0.10,
            late_percentile=0.90,
            robust_sb=False,
        )
        self.assertEqual(
            result.state,
            "LOW_EARLY_HIGH_LATE_UNCONFIRMED",
        )

    def test_zero_late_count_is_low_even_with_tied_percentile(self):
        result = classify_mechanism_state(
            early_percentile=0.10,
            late_percentile=0.35,
            early_count=0,
            late_count=0,
            robust_sb=False,
        )
        self.assertEqual(result.state, "FORGOTTEN")

    def test_middle_zone_is_ambiguous(self):
        result = classify_mechanism_state(
            early_percentile=0.50,
            late_percentile=0.90,
            robust_sb=True,
        )
        self.assertEqual(result.state, "AMBIGUOUS")

    def test_early_late_percentiles_are_within_stratum(self):
        result = early_late_percentiles(
            {
                "low_low": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "low_high": [0, 0, 0, 0, 0, 10, 10, 10, 10, 10],
                "high_high": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            },
            early_years=5,
            late_years=5,
        )
        self.assertLess(
            result["low_high"][0],
            result["high_high"][0],
        )
        self.assertGreater(
            result["low_high"][1],
            result["low_low"][1],
        )


if __name__ == "__main__":
    unittest.main()
