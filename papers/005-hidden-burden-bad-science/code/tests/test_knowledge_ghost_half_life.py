from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from knowledge_ghost_half_life import kaplan_meier_median, source_half_life  # noqa: E402


class GhostHalfLifeTests(unittest.TestCase):
    def test_event_requires_consecutive_confirmation(self):
        counts = {2016: 10, 2017: 10, 2018: 10, 2020: 8, 2021: 4, 2022: 4, 2023: 3}
        out = source_half_life(
            counts, dt.date(2019, 6, 1), baseline_years=3, confirm_years=2, last_complete_year=2023
        )
        self.assertTrue(out["event_observed"])
        self.assertEqual(out["half_life_years"], 2)
        self.assertEqual(out["event_year"], 2021)

    def test_transient_dip_does_not_trigger(self):
        counts = {2016: 10, 2017: 10, 2018: 10, 2020: 4, 2021: 8, 2022: 4, 2023: 4}
        out = source_half_life(
            counts, dt.date(2019, 6, 1), baseline_years=3, confirm_years=2, last_complete_year=2023
        )
        self.assertEqual(out["event_year"], 2022)

    def test_right_censoring_is_preserved(self):
        counts = {2017: 10, 2018: 10, 2020: 8, 2021: 7, 2022: 6}
        out = source_half_life(
            counts, dt.date(2019, 1, 1), baseline_years=2, confirm_years=2, last_complete_year=2022
        )
        self.assertFalse(out["event_observed"])
        self.assertTrue(out["right_censored"])
        self.assertEqual(out["censor_time_years"], 3)

    def test_km_median_handles_censoring(self):
        records = [
            {"estimable": True, "event_observed": True, "half_life_years": 1},
            {"estimable": True, "event_observed": True, "half_life_years": 2},
            {"estimable": True, "event_observed": False, "right_censored": True, "censor_time_years": 3},
        ]
        out = kaplan_meier_median(records)
        self.assertTrue(out["median_reached"])
        self.assertEqual(out["median_years"], 2)


if __name__ == "__main__":
    unittest.main()
