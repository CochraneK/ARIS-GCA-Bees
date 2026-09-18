import unittest

from aggregate_pilot1 import aggregate_results


class Pilot1AggregateTests(unittest.TestCase):
    def _result(self, seed, ndcg_a, ndcg_b):
        return {
            "sampling": {
                "filters": (
                    "publication_year:1980,type:article,"
                    "primary_topic.field.id:31"
                ),
                "sample_size_analyzed": 20,
                "seed": seed,
            },
            "temporal_design": {
                "feature_cutoff_year": 1995,
                "outcome_observation_end_year": 2011,
            },
            "outcome_summary": {
                "beauty_top_fraction": {
                    "relevance_type": "binary",
                    "n": 20,
                    "n_positive": 4,
                    "positive_rate": 0.2,
                }
            },
            "outcome_baseline_matrix": {
                "beauty_top_fraction": [
                    {
                        "strategy": "a",
                        "precision_at_k": 0.4,
                        "recall_at_k": 0.5,
                        "ndcg_at_k": ndcg_a,
                    },
                    {
                        "strategy": "b",
                        "precision_at_k": 0.2,
                        "recall_at_k": 0.25,
                        "ndcg_at_k": ndcg_b,
                    },
                ]
            },
        }

    def test_macro_average_and_winner_counts(self):
        result = aggregate_results(
            [
                self._result(1, 0.8, 0.4),
                self._result(2, 0.6, 0.7),
            ]
        )
        self.assertEqual(result["n_strata"], 2)
        self.assertEqual(result["total_papers_analyzed"], 40)
        metric = result["metrics"]["beauty_top_fraction"]["a"][
            "ndcg_at_k"
        ]
        self.assertAlmostEqual(metric["mean"], 0.7)
        self.assertEqual(
            result["ndcg_winner_counts"]["beauty_top_fraction"]["a"],
            1,
        )
        self.assertEqual(
            result["ndcg_winner_counts"]["beauty_top_fraction"]["b"],
            1,
        )

    def test_field_id_is_parsed(self):
        result = aggregate_results([self._result(1, 0.8, 0.4)])
        self.assertEqual(result["strata"][0]["field_id"], "31")


if __name__ == "__main__":
    unittest.main()
