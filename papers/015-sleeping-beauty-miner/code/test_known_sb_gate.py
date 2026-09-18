import json
import unittest
from pathlib import Path

from mechanism_labels import robust_sleeping_beauty_gate


class KnownSleepingBeautyGateTests(unittest.TestCase):
    def test_hummers_requires_less_deep_not_strict_deep_profile(self):
        data_path = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "pilot0_openalex_hummers.json"
        )
        payload = json.loads(data_path.read_text(encoding="utf-8"))
        counts = payload["trajectory"]["counts"]

        default = robust_sleeping_beauty_gate(
            counts,
            min_total_citations=50,
        )
        strict = robust_sleeping_beauty_gate(
            counts,
            max_sleep_rate=1.0,
            min_total_citations=50,
        )

        self.assertTrue(default.robust_sb)
        self.assertTrue(default.van_raan.passed)
        self.assertEqual(default.van_raan.mode, "VARIABLE_SLEEP")
        self.assertEqual(
            default.van_raan.as_dict()["sleep_depth_class"],
            "LESS_DEEP",
        )
        self.assertGreaterEqual(default.van_raan.sleep_years, 40)

        # The stricter deep-sleep-only profile is intentionally a sensitivity
        # definition and does not capture this classic long-sleep case.
        self.assertFalse(strict.van_raan.passed)
        self.assertFalse(strict.robust_sb)


if __name__ == "__main__":
    unittest.main()
