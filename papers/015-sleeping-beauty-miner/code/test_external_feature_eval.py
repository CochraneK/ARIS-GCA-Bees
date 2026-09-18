import unittest

from external_feature_eval import (
    build_items,
    evaluate_feature_outcome_matrix,
    evaluate_score_map,
)


class ExternalFeatureEvalTests(unittest.TestCase):
    def test_join_uses_common_ids_only(self):
        items = build_items(
            {"a": 3.0, "b": 2.0, "extra": 99.0},
            {"a": 1.0, "b": 0.0, "missing": 1.0},
        )
        self.assertEqual([item.paper_id for item in items], ["a", "b"])

    def test_binary_feature_evaluation(self):
        result = evaluate_score_map(
            {"a": 3.0, "b": 2.0, "c": 1.0},
            relevance={"a": 1.0, "b": 0.0, "c": 0.0},
            relevance_type="binary",
            k=1,
            feature_name="novelty",
        )
        self.assertEqual(result["precision_at_k"], 1.0)
        self.assertEqual(result["recall_at_k"], 1.0)
        self.assertEqual(result["feature"], "novelty")

    def test_graded_feature_evaluation_uses_ndcg_only(self):
        result = evaluate_score_map(
            {"a": 3.0, "b": 2.0, "c": 1.0},
            relevance={"a": 1.0, "b": 0.5, "c": 0.0},
            relevance_type="graded",
            k=3,
            feature_name="novelty",
        )
        self.assertAlmostEqual(result["ndcg_at_k"], 1.0)
        self.assertNotIn("precision_at_k", result)

    def test_matrix_preserves_outcomes_and_features(self):
        result = evaluate_feature_outcome_matrix(
            {
                "f1": {"a": 2.0, "b": 1.0},
                "f2": {"a": 1.0, "b": 2.0},
            },
            outcomes={
                "binary_outcome": ("binary", {"a": 1.0, "b": 0.0}),
                "graded_outcome": ("graded", {"a": 1.0, "b": 0.2}),
            },
            k=1,
        )
        self.assertEqual(
            {row["feature"] for row in result["binary_outcome"]},
            {"f1", "f2"},
        )
        self.assertEqual(
            set(result),
            {"binary_outcome", "graded_outcome"},
        )


if __name__ == "__main__":
    unittest.main()
