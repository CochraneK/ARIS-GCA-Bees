import math
import unittest

from evidence_features import (
    canonical_pair,
    citing_community_features,
    cross_field_reference_share,
    diversity_features,
    pair_novelty_features,
    reference_field_features,
)


class EvidenceFeatureTests(unittest.TestCase):
    def test_diversity_is_zero_for_one_category(self):
        result = diversity_features(["a", "a", "a"])
        self.assertEqual(result.n_categories, 1)
        self.assertEqual(result.shannon_entropy, 0.0)
        self.assertEqual(result.normalized_entropy, 0.0)
        self.assertAlmostEqual(result.effective_categories, 1.0)

    def test_balanced_two_category_entropy_is_normalized_one(self):
        result = diversity_features(["a", "a", "b", "b"])
        self.assertAlmostEqual(result.shannon_entropy, math.log(2))
        self.assertAlmostEqual(result.normalized_entropy, 1.0)
        self.assertAlmostEqual(result.effective_categories, 2.0)

    def test_pair_novelty_uses_prior_counts_only(self):
        prior = {
            canonical_pair("a", "b"): 10,
            canonical_pair("a", "c"): 0,
        }
        result = pair_novelty_features(
            ["a", "b", "c"],
            prior_pair_counts=prior,
        )
        self.assertEqual(result.n_pairs, 3)
        self.assertEqual(result.unseen_pairs, 2)
        self.assertAlmostEqual(result.unseen_pair_share, 2 / 3)
        self.assertAlmostEqual(result.mean_prior_pair_count, 10 / 3)

    def test_cross_field_share_ignores_unknown_reference_fields(self):
        result = cross_field_reference_share(
            "physics",
            ["physics", "chemistry", None, "biology"],
        )
        self.assertAlmostEqual(result, 2 / 3)

    def test_cross_field_share_abstains_without_home_field(self):
        self.assertIsNone(
            cross_field_reference_share(None, ["physics", "chemistry"])
        )

    def test_wrappers_use_same_diversity_contract(self):
        citing = citing_community_features(["x", "y", "y"])
        refs = reference_field_features(["x", "y", "y"])
        self.assertEqual(citing.as_dict(), refs.as_dict())


if __name__ == "__main__":
    unittest.main()
