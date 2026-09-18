import unittest

from aggregate_feature_ablation import aggregate_feature_results


class FeatureAblationAggregateTests(unittest.TestCase):
    def _result(self, seed, a, b):
        return {
            "ablation": "historical title lexical novelty",
            "target_cohort": {
                "filters": "publication_year:1980",
                "seed": seed,
                "n": 20,
            },
            "prior_corpus": {
                "n_titles": 100,
                "provenance": {
                    "filters": "to_publication_date:1979-12-31",
                    "seed": seed + 100,
                },
            },
            "coverage": {"known_token_share": 0.75},
            "feature_outcome_matrix": {
                "consensus": [
                    {
                        "feature": "distance",
                        "relevance_type": "binary",
                        "precision_at_k": 0.2,
                        "recall_at_k": 0.5,
                        "ndcg_at_k": a,
                    },
                    {
                        "feature": "oov",
                        "relevance_type": "binary",
                        "precision_at_k": 0.4,
                        "recall_at_k": 1.0,
                        "ndcg_at_k": b,
                    },
                ]
            },
        }

    def test_macro_aggregation_and_winners(self):
        result = aggregate_feature_results(
            [
                self._result(1, 0.8, 0.4),
                self._result(2, 0.6, 0.9),
            ]
        )
        self.assertEqual(result["n_strata"], 2)
        self.assertAlmostEqual(
            result["metrics"]["consensus"]["distance"]["ndcg_at_k"][
                "mean"
            ],
            0.7,
        )
        self.assertEqual(
            result["ndcg_winner_counts"]["consensus"]["distance"],
            1,
        )
        self.assertEqual(
            result["ndcg_winner_counts"]["consensus"]["oov"],
            1,
        )


if __name__ == "__main__":
    unittest.main()
