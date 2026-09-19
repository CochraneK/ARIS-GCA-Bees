from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from sb1_baseline import (  # noqa: E402
    FEATURES,
    auc,
    evaluate,
    year_block_folds,
)


def make_rows(n_years=10, per_year=6):
    rows = []
    paper = 0
    for y in range(1990, 1990 + n_years):
        for j in range(per_year):
            paper += 1
            # Simple deterministic pattern with both classes in most years.
            cumulative = (j + (y - 1990)) % 8
            target = 1 if ((j + 2 * (y - 1990)) % 5 == 0) else 0
            rows.append({
                "paper_id": f"P{paper}",
                "publication_year": str(y),
                "eligible_for_horizon": "1",
                "feature_citations_cumulative": str(cumulative),
                "feature_citations_last_year": str(cumulative % 3),
                "feature_citations_max_annual": str(max(1, cumulative // 2)),
                "feature_citations_mean_annual": str(cumulative / 6),
                "feature_zero_citation_years": str(6 - min(6, cumulative)),
                "feature_positive_citation_years": str(min(6, cumulative)),
                "feature_citation_slope": str((cumulative - 2) / 10),
                "outcome_awakening_within_horizon_after_landmark": str(target),
                "outcome_full_history_beauty_coefficient": str(1000 + paper),
            })
    return rows


class SB1BaselineTests(unittest.TestCase):
    def test_auc_perfect(self):
        self.assertAlmostEqual(auc([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9]), 1.0)

    def test_year_folds_keep_same_year_together(self):
        rows = [
            {"publication_year": 1990},
            {"publication_year": 1990},
            {"publication_year": 1991},
            {"publication_year": 1992},
        ]
        mapping = year_block_folds(rows, 2)
        self.assertIn(1990, mapping)
        self.assertEqual(mapping[1990], mapping[1990])

    def test_future_outcome_column_cannot_leak_into_features(self):
        rows = make_rows()
        _, a = evaluate(rows, folds=5)

        changed = copy.deepcopy(rows)
        for row in changed:
            row["outcome_full_history_beauty_coefficient"] = "999999999"
            row["future_magic_predictor"] = row[
                "outcome_awakening_within_horizon_after_landmark"
            ]

        pred_a, _ = evaluate(rows, folds=5)
        pred_b, b = evaluate(changed, folds=5)

        pa = [x["predicted_probability"] for x in pred_a]
        pb = [x["predicted_probability"] for x in pred_b]
        self.assertEqual(pa, pb)
        self.assertEqual(a["feature_columns"], FEATURES)
        self.assertEqual(b["feature_columns"], FEATURES)
        self.assertNotIn("future_magic_predictor", FEATURES)

    def test_all_eligible_rows_receive_oof_predictions(self):
        rows = make_rows()
        predictions, summary = evaluate(rows, folds=5)
        self.assertEqual(len(predictions), len(rows))
        self.assertEqual(summary["rows_eligible"], len(rows))
        self.assertEqual(summary["folds_realized"], 5)
        self.assertIsNotNone(summary["metrics"]["brier"])

    def test_ineligible_rows_are_excluded(self):
        rows = make_rows()
        rows[0]["eligible_for_horizon"] = "0"
        rows[0]["outcome_awakening_within_horizon_after_landmark"] = ""
        predictions, summary = evaluate(rows, folds=5)
        self.assertEqual(len(predictions), len(rows) - 1)
        self.assertEqual(summary["rows_eligible"], len(rows) - 1)


if __name__ == "__main__":
    unittest.main()
