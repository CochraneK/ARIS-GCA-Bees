import unittest

from historical_backtest import (
    PaperHistory,
    evaluate_baseline,
    score_at_cutoff,
)


class HistoricalBacktestTests(unittest.TestCase):
    def test_future_citations_do_not_change_cutoff_score(self):
        early = PaperHistory("p", 2000, (0, 1, 0, 2, 0, 0))
        future_spike = PaperHistory("p", 2000, (0, 1, 0, 2, 100, 200))

        a = score_at_cutoff(
            early,
            cutoff_year=2003,
            strategy="current_citations",
        )
        b = score_at_cutoff(
            future_spike,
            cutoff_year=2003,
            strategy="current_citations",
        )
        self.assertEqual(a, b)

    def test_future_relevance_affects_evaluation_not_score(self):
        histories = [
            PaperHistory("a", 2000, (0, 5, 5, 5)),
            PaperHistory("b", 2000, (0, 1, 1, 1)),
        ]
        result = evaluate_baseline(
            histories,
            cutoff_year=2003,
            strategy="current_citations",
            future_relevance={"a": 0.0, "b": 1.0},
            k=1,
        )
        self.assertEqual(result["precision_at_k"], 0.0)
        self.assertEqual(result["recall_at_k"], 0.0)

    def test_missing_future_label_is_excluded(self):
        histories = [
            PaperHistory("a", 2000, (0, 5)),
            PaperHistory("b", 2000, (0, 1)),
        ]
        result = evaluate_baseline(
            histories,
            cutoff_year=2001,
            strategy="current_citations",
            future_relevance={"a": 1.0},
            k=5,
        )
        self.assertEqual(result["n"], 1)
        self.assertEqual(result["k"], 1)


if __name__ == "__main__":
    unittest.main()
