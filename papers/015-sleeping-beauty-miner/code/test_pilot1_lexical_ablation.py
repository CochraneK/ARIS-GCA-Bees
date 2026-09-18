import unittest

from pilot1_lexical_ablation import evaluate_lexical_ablation


class Pilot1LexicalAblationTests(unittest.TestCase):
    def _cohort(self):
        return {
            "sampling": {
                "filters": (
                    "publication_year:1980,type:article,"
                    "primary_topic.field.id:31"
                ),
                "seed": 1,
                "sample_id_sha256": "abc",
            },
            "temporal_design": {
                "feature_cutoff_year": 1995,
                "outcome_observation_end_year": 2011,
            },
            "review_budget_k": 1,
            "cases": [
                {
                    "paper_id": "novel",
                    "title": "zebra mangrove fermentation",
                    "outcomes": {
                        "beauty_percentile": 1.0,
                        "beauty_top_fraction": 1.0,
                        "future_acceleration_percentile": 1.0,
                        "future_uptake_percentile": 0.5,
                        "awakening_within_horizon": 1.0,
                        "delayed_recognition_consensus": 1.0,
                        "delayed_recognition_with_uptake_floor": 1.0,
                    },
                },
                {
                    "paper_id": "familiar",
                    "title": "quantum spin dynamics",
                    "outcomes": {
                        "beauty_percentile": 0.0,
                        "beauty_top_fraction": 0.0,
                        "future_acceleration_percentile": 0.0,
                        "future_uptake_percentile": 0.0,
                        "awakening_within_horizon": 0.0,
                        "delayed_recognition_consensus": 0.0,
                        "delayed_recognition_with_uptake_floor": 0.0,
                    },
                },
            ],
        }

    def test_lexical_distance_can_be_evaluated_on_same_outcomes(self):
        result = evaluate_lexical_ablation(
            self._cohort(),
            prior_titles=[
                "quantum spin dynamics",
                "galaxy rotation curves",
                "protein folding kinetics",
            ],
            prior_ids=["p1", "p2", "p3"],
            prior_provenance={"source": "fixture"},
        )
        matrix = result["feature_outcome_matrix"]
        rows = {
            row["feature"]: row
            for row in matrix["delayed_recognition_consensus"]
        }
        self.assertEqual(
            rows["lexical_nearest1_distance"]["precision_at_k"],
            1.0,
        )
        self.assertEqual(result["prior_corpus"]["n_titles"], 3)
        self.assertEqual(len(result["prior_corpus"]["sample_id_sha256"]), 64)

    def test_no_weighted_composite_is_emitted(self):
        result = evaluate_lexical_ablation(
            self._cohort(),
            prior_titles=["quantum spin dynamics", "galaxy rotation"],
        )
        self.assertEqual(
            set(result["feature_direction"]),
            {
                "lexical_nearest1_distance",
                "lexical_nearest3_distance",
                "lexical_oov_share",
            },
        )
        self.assertNotIn("lexical_novelty_score", result["feature_direction"])


if __name__ == "__main__":
    unittest.main()
