from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from innovation_delay import estimate  # noqa: E402


def make_rows():
    rows = []
    # Two matched sets. Both have flat pre-period treated-control differences.
    # Post-shock, treated topic loses 2 article arrivals/year relative to control.
    for matched_set, base in (("M1", 10), ("M2", 20)):
        for year in range(2017, 2024):
            event_year = 2020
            k = year - event_year
            control = base
            treated = base + 1
            if k >= 0:
                treated -= 2
            rows.append({
                "matched_set_id": matched_set,
                "unit_id": matched_set + "_T",
                "treated": "1",
                "event_year": str(event_year),
                "year": str(year),
                "event_time": str(k),
                "outcome_articles": str(treated),
            })
            rows.append({
                "matched_set_id": matched_set,
                "unit_id": matched_set + "_C",
                "treated": "0",
                "event_year": str(event_year),
                "year": str(year),
                "event_time": str(k),
                "outcome_articles": str(control),
            })
    return rows


class InnovationDelayTests(unittest.TestCase):
    def test_event_study_recovers_post_gap(self):
        out = estimate(
            make_rows(),
            outcome="outcome_articles",
            baseline_times=[-3, -2, -1],
            post_times=[0, 1, 2, 3],
            bootstrap_reps=100,
            seed=7,
        )
        self.assertEqual(out["matched_sets_valid"], 2)
        for k in (-3, -2, -1):
            self.assertAlmostEqual(
                out["event_study"][str(k)]["effect_mean"], 0.0
            )
        for k in (0, 1, 2, 3):
            self.assertAlmostEqual(
                out["event_study"][str(k)]["effect_mean"], -2.0
            )
        self.assertAlmostEqual(
            out["pretrend_diagnostics"]["pre_event_slope"], 0.0
        )
        self.assertGreater(
            out["output_equivalent_delay"]["mean_years"], 0
        )

    def test_incomplete_baseline_set_is_excluded(self):
        rows = make_rows()
        rows = [
            r for r in rows
            if not (
                r["matched_set_id"] == "M2"
                and r["year"] == "2017"
                and r["treated"] == "0"
            )
        ]
        out = estimate(
            rows,
            outcome="outcome_articles",
            baseline_times=[-3, -2, -1],
            post_times=[0, 1, 2, 3],
            bootstrap_reps=20,
            seed=7,
        )
        self.assertEqual(out["matched_sets_valid"], 1)
        self.assertEqual(
            out["exclusion_reasons"]["INCOMPLETE_BASELINE"], 1
        )

    def test_post_outcome_does_not_define_matching(self):
        # Estimator itself receives an already frozen matched panel and does not
        # construct matches from outcomes; this invariant ensures the API has no
        # post-treatment matching option.
        out = estimate(
            make_rows(),
            outcome="outcome_articles",
            baseline_times=[-3, -2, -1],
            post_times=[0],
            bootstrap_reps=0,
        )
        self.assertIn("Matching features must be pre-treatment.", out["warnings"])


if __name__ == "__main__":
    unittest.main()
