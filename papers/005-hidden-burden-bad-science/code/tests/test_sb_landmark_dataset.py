from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from build_sb_landmark_dataset import (  # noqa: E402
    build_landmark_row,
    build_dataset,
)


class SBLandmarkTests(unittest.TestCase):
    def test_post_landmark_changes_do_not_change_features(self):
        base = {
            2000: 0,
            2001: 1,
            2002: 0,
            2003: 1,
            2004: 0,
            2005: 1,
            2006: 0,
            2007: 0,
            2008: 10,
            2009: 15,
            2010: 5,
        }
        changed = copy.deepcopy(base)
        changed[2008] = 100
        changed[2009] = 200

        a = build_landmark_row(
            "P1", 2000, base,
            landmark_age=5,
            horizon_years=5,
            observation_end_year=2010,
        )
        b = build_landmark_row(
            "P1", 2000, changed,
            landmark_age=5,
            horizon_years=5,
            observation_end_year=2010,
        )

        feature_keys = [k for k in a if k.startswith("feature_")]
        self.assertTrue(feature_keys)
        for key in feature_keys:
            self.assertEqual(a[key], b[key], key)

        self.assertNotEqual(
            a["outcome_full_history_beauty_coefficient"],
            b["outcome_full_history_beauty_coefficient"],
        )

    def test_censoring_leaves_binary_outcomes_blank(self):
        row = build_landmark_row(
            "P1",
            2000,
            {2000: 0, 2001: 1, 2002: 0, 2003: 2},
            landmark_age=3,
            horizon_years=10,
            observation_end_year=2008,
        )
        self.assertEqual(row["eligible_for_horizon"], 0)
        self.assertEqual(
            row["outcome_awakening_within_horizon_after_landmark"], ""
        )
        self.assertEqual(
            row["outcome_peak_within_horizon_after_landmark"], ""
        )

    def test_dataset_summary_counts_only_mature_rows(self):
        rows = []
        for year, count in [
            (2000, 0), (2001, 0), (2002, 1), (2003, 0),
            (2004, 0), (2005, 1), (2006, 5), (2007, 10),
        ]:
            rows.append({
                "paper_id": "A",
                "openalex_id": "W1",
                "publication_year": "2000",
                "citation_year": str(year),
                "citations": str(count),
            })

        out, summary = build_dataset(
            rows,
            landmark_age=2,
            horizon_years=4,
            observation_end_year=2007,
        )
        self.assertEqual(len(out), 1)
        self.assertEqual(summary["papers_eligible_for_horizon"], 1)
        self.assertIn("feature_boundary", summary)

    def test_landmark_feature_window_is_inclusive(self):
        row = build_landmark_row(
            "P1",
            2000,
            {2000: 1, 2001: 2, 2002: 3, 2003: 100},
            landmark_age=2,
            horizon_years=1,
            observation_end_year=2003,
        )
        self.assertEqual(row["feature_citations_cumulative"], 6)
        self.assertEqual(row["feature_citations_last_year"], 3)


if __name__ == "__main__":
    unittest.main()
