import unittest

from lexical_novelty import (
    batch_title_novelty,
    cosine_similarity,
    fit_idf,
    tfidf_vector,
    title_novelty_features,
    tokenize,
)


class LexicalNoveltyTests(unittest.TestCase):
    def test_tokenize_is_deterministic_and_removes_common_words(self):
        self.assertEqual(
            tokenize("The Quantum Effect of Cats in Boxes"),
            ["quantum", "cats", "boxes"],
        )

    def test_identical_title_has_small_nearest_distance(self):
        prior = [
            "quantum spin dynamics",
            "galaxy rotation curves",
            "protein folding kinetics",
        ]
        result = title_novelty_features(
            "quantum spin dynamics",
            prior_titles=prior,
        )
        self.assertAlmostEqual(result.nearest1_distance, 0.0)

    def test_unseen_vocabulary_has_high_oov_share(self):
        prior = [
            "quantum spin dynamics",
            "galaxy rotation curves",
        ]
        result = title_novelty_features(
            "zebra mangrove fermentation",
            prior_titles=prior,
        )
        self.assertEqual(result.oov_token_share, 1.0)
        self.assertEqual(result.max_prior_similarity, 0.0)
        self.assertEqual(result.nearest1_distance, 1.0)

    def test_partial_overlap_is_between_extremes(self):
        prior = [
            "quantum spin dynamics",
            "galaxy rotation curves",
        ]
        result = title_novelty_features(
            "quantum galaxy scattering",
            prior_titles=prior,
        )
        self.assertGreater(result.max_prior_similarity, 0.0)
        self.assertLess(result.max_prior_similarity, 1.0)

    def test_batch_matches_single_contract(self):
        prior = ["alpha beta gamma", "delta epsilon zeta"]
        batch = batch_title_novelty(
            {"a": "alpha beta gamma", "b": "novel theta words"},
            prior_titles=prior,
        )
        single = title_novelty_features(
            "alpha beta gamma",
            prior_titles=prior,
        )
        self.assertEqual(batch["a"].as_dict(), single.as_dict())
        self.assertGreater(
            batch["b"].nearest1_distance,
            batch["a"].nearest1_distance,
        )

    def test_cosine_empty_vector_is_zero(self):
        self.assertEqual(cosine_similarity({}, {"x": 1.0}), 0.0)

    def test_tfidf_is_l2_normalized(self):
        idf, _ = fit_idf(["alpha beta", "beta gamma"])
        vector = tfidf_vector(["alpha", "beta"], idf)
        norm = sum(value * value for value in vector.values()) ** 0.5
        self.assertAlmostEqual(norm, 1.0)


if __name__ == "__main__":
    unittest.main()
