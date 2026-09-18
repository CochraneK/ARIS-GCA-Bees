import unittest

from outcome_labels import (
    awakening_within_horizon_outcome,
    build_outcome_record,
    delayed_recognition_consensus_outcome,
    outcome_bundle,
    percentile_ranks,
    top_fraction_binary,
)


class OutcomeLabelTests(unittest.TestCase):
    def test_build_record_separates_cutoff_and_future(self):
        row = build_outcome_record(
            paper_id="p",
            publication_year=2000,
            counts=[0, 1, 1, 2, 10, 20],
            cutoff_year=2003,
        )
        self.assertEqual(row.pre_cutoff_citations, 4)
        self.assertEqual(row.future_citations, 30)
        self.assertEqual(row.observation_end_year, 2005)

    def test_percentile_ranks_handle_ties(self):
        result = percentile_ranks({"a": 1.0, "b": 1.0, "c": 3.0})
        self.assertAlmostEqual(result["a"], 0.25)
        self.assertAlmostEqual(result["b"], 0.25)
        self.assertAlmostEqual(result["c"], 1.0)

    def test_top_fraction_has_fixed_reproducible_size(self):
        result = top_fraction_binary(
            {"b": 1.0, "a": 1.0, "c": 0.0, "d": 0.0},
            fraction=0.25,
        )
        self.assertEqual(sum(result.values()), 1.0)
        self.assertEqual(result["a"], 1.0)

    def test_awakening_must_be_post_cutoff(self):
        rows = [
            build_outcome_record(
                paper_id="late",
                publication_year=2000,
                counts=[0, 0, 0, 0, 1, 10, 30],
                cutoff_year=2002,
            ),
            build_outcome_record(
                paper_id="early",
                publication_year=2000,
                counts=[0, 10, 20, 20, 20, 20, 20],
                cutoff_year=2002,
            ),
        ]
        outcome = awakening_within_horizon_outcome(
            rows,
            horizon_years=10,
        )
        self.assertEqual(outcome["early"], 0.0)

    def test_consensus_requires_multiple_components(self):
        rows = [
            build_outcome_record(
                paper_id="a",
                publication_year=2000,
                counts=[0, 0, 0, 0, 1, 10, 30],
                cutoff_year=2002,
            ),
            build_outcome_record(
                paper_id="b",
                publication_year=2000,
                counts=[0, 2, 2, 2, 2, 2, 2],
                cutoff_year=2002,
            ),
            build_outcome_record(
                paper_id="c",
                publication_year=2000,
                counts=[0, 1, 1, 1, 1, 1, 1],
                cutoff_year=2002,
            ),
        ]
        result = delayed_recognition_consensus_outcome(
            rows,
            beauty_fraction=1 / 3,
            acceleration_fraction=1 / 3,
            horizon_years=10,
            min_components=2,
        )
        self.assertEqual(set(result), {"a", "b", "c"})
        self.assertTrue(all(value in {0.0, 1.0} for value in result.values()))

    def test_bundle_contains_prespecified_outcomes(self):
        rows = [
            build_outcome_record(
                paper_id="a",
                publication_year=2000,
                counts=[0, 0, 1, 2, 5],
                cutoff_year=2002,
            ),
            build_outcome_record(
                paper_id="b",
                publication_year=2000,
                counts=[0, 1, 1, 1, 1],
                cutoff_year=2002,
            ),
        ]
        bundle = outcome_bundle(rows, horizon_years=5)
        self.assertEqual(
            set(bundle),
            {
                "beauty_percentile",
                "beauty_top_fraction",
                "future_acceleration_percentile",
                "awakening_within_horizon",
                "delayed_recognition_consensus",
            },
        )


if __name__ == "__main__":
    unittest.main()
