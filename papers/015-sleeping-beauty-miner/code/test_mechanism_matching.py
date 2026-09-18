import unittest

from mechanism_matching import (
    MechanismPaper,
    build_priority_contrasts,
    match_balance_diagnostics,
    nearest_controls,
    standardized_mean_difference,
)


class MechanismMatchingTests(unittest.TestCase):
    def setUp(self):
        self.sb = MechanismPaper(
            paper_id="sb",
            state="SLEEPING_BEAUTY",
            publication_year=1980,
            field="physics",
            early_citation_percentile=0.10,
            reference_count=20,
            author_count=2,
            early_citation_count=1,
        )
        self.forgotten_close = MechanismPaper(
            paper_id="f_close",
            state="FORGOTTEN",
            publication_year=1980,
            field="physics",
            early_citation_percentile=0.11,
            reference_count=21,
            author_count=2,
            early_citation_count=1,
        )
        self.forgotten_far = MechanismPaper(
            paper_id="f_far",
            state="FORGOTTEN",
            publication_year=1980,
            field="physics",
            early_citation_percentile=0.24,
            reference_count=50,
            author_count=6,
            early_citation_count=4,
        )
        self.hit = MechanismPaper(
            paper_id="hit",
            state="IMMEDIATE_HIT",
            publication_year=1980,
            field="physics",
            early_citation_percentile=0.90,
            reference_count=22,
            author_count=2,
            early_citation_count=30,
        )

    def test_nearest_forgotten_control_is_selected(self):
        matches, unmatched = nearest_controls(
            [self.sb],
            [self.forgotten_far, self.forgotten_close],
            control_state="FORGOTTEN",
            early_percentile_caliper=0.15,
        )
        self.assertFalse(unmatched)
        self.assertEqual(matches[0].control_id, "f_close")

    def test_field_mismatch_is_not_matched(self):
        other = MechanismPaper(
            paper_id="other",
            state="FORGOTTEN",
            publication_year=1980,
            field="medicine",
            early_citation_percentile=0.10,
        )
        matches, unmatched = nearest_controls(
            [self.sb],
            [other],
            control_state="FORGOTTEN",
        )
        self.assertFalse(matches)
        self.assertEqual(unmatched, ["sb"])

    def test_no_replacement_by_default(self):
        sb2 = MechanismPaper(
            paper_id="sb2",
            state="SLEEPING_BEAUTY",
            publication_year=1980,
            field="physics",
            early_citation_percentile=0.12,
        )
        matches, unmatched = nearest_controls(
            [self.sb, sb2],
            [self.forgotten_close],
            control_state="FORGOTTEN",
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(len(unmatched), 1)

    def test_standardized_mean_difference_detects_balance(self):
        self.assertAlmostEqual(
            standardized_mean_difference([1, 2, 3], [1, 2, 3]),
            0.0,
        )
        self.assertGreater(
            standardized_mean_difference([1, 2, 3], [3, 4, 5]),
            0.1,
        )

    def test_balance_requires_multiple_pairs(self):
        match, _ = nearest_controls(
            [self.sb],
            [self.forgotten_close],
            control_state="FORGOTTEN",
        )
        diagnostics = match_balance_diagnostics(
            match,
            [self.sb, self.forgotten_close],
            include_early_attention=True,
        )
        self.assertFalse(diagnostics["balance_assessable"])
        self.assertIsNone(diagnostics["balance_pass"])

    def test_priority_contrasts_build_two_questions(self):
        result = build_priority_contrasts(
            [
                self.sb,
                self.forgotten_close,
                self.forgotten_far,
                self.hit,
            ]
        )
        self.assertIn("SB_vs_FORGOTTEN", result)
        self.assertIn("SB_vs_IMMEDIATE_HIT", result)
        self.assertEqual(
            result["SB_vs_FORGOTTEN"]["matches"][0]["control_id"],
            "f_close",
        )
        self.assertEqual(
            result["SB_vs_IMMEDIATE_HIT"]["matches"][0]["control_id"],
            "hit",
        )
        self.assertFalse(
            result["matching_rule"]["post_outcome_variables_used"]
        )


if __name__ == "__main__":
    unittest.main()
