import unittest

from ranking_metrics import (
    RankedItem,
    brier_score,
    calibration_bins,
    evaluate_ranking,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)


class RankingMetricTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            RankedItem("a", 0.9, 1.0),
            RankedItem("b", 0.8, 0.0),
            RankedItem("c", 0.7, 1.0),
            RankedItem("d", 0.6, 0.0),
        ]

    def test_precision_and_recall(self):
        self.assertEqual(precision_at_k(self.items, 2), 0.5)
        self.assertEqual(recall_at_k(self.items, 2), 0.5)

    def test_perfect_ndcg_is_one(self):
        perfect = [
            RankedItem("a", 3.0, 3.0),
            RankedItem("b", 2.0, 2.0),
            RankedItem("c", 1.0, 1.0),
        ]
        self.assertAlmostEqual(ndcg_at_k(perfect, 3), 1.0)

    def test_bad_order_has_lower_ndcg(self):
        bad = [
            RankedItem("a", 3.0, 0.0),
            RankedItem("b", 2.0, 1.0),
            RankedItem("c", 1.0, 3.0),
        ]
        self.assertLess(ndcg_at_k(bad, 3), 1.0)

    def test_brier_score(self):
        self.assertAlmostEqual(
            brier_score([0, 1], [0.1, 0.9]),
            0.01,
        )

    def test_calibration_bins(self):
        bins = calibration_bins(
            [0, 0, 1, 1],
            [0.1, 0.2, 0.8, 0.9],
            n_bins=2,
        )
        self.assertEqual(len(bins), 2)
        self.assertEqual(bins[0]["event_rate"], 0.0)
        self.assertEqual(bins[1]["event_rate"], 1.0)

    def test_evaluate_ranking(self):
        result = evaluate_ranking(self.items, k=2)
        self.assertEqual(result["k"], 2)
        self.assertIn("ndcg_at_k", result)


if __name__ == "__main__":
    unittest.main()
