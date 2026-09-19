import unittest

from mechanism_matching import MechanismPaper
from risk_set_matching import (
    build_awakening_risk_set_contrast,
    first_burst_age,
    is_at_risk_dormant_control,
    match_awakening_risk_sets,
)


class RiskSetMatchingTests(unittest.TestCase):
    def setUp(self):
        self.case = MechanismPaper(
            paper_id="sb",
            state="SLEEPING_BEAUTY",
            publication_year=1980,
            field="physics",
            early_citation_percentile=0.8,
            reference_count=20,
            author_count=2,
            annual_citation_counts=tuple(
                [1] * 10 + [8, 8, 8, 8] + [20] * 6
            ),
            robust_sleep_years=10,
            robust_sleep_rate=1.0,
        )
        self.dormant = MechanismPaper(
            paper_id="dormant",
            state="AMBIGUOUS",
            publication_year=1980,
            field="physics",
            early_citation_percentile=0.7,
            reference_count=21,
            author_count=2,
            annual_citation_counts=tuple(
                [1] * 10 + [1] * 10
            ),
        )
        self.future_case = MechanismPaper(
            paper_id="future",
            state="SLEEPING_BEAUTY",
            publication_year=1980,
            field="physics",
            early_citation_percentile=0.9,
            reference_count=19,
            author_count=2,
            annual_citation_counts=tuple(
                [1] * 14 + [8, 8, 8, 8] + [20, 20]
            ),
            robust_sleep_years=14,
            robust_sleep_rate=1.0,
        )
        self.early_hit = MechanismPaper(
            paper_id="hit",
            state="IMMEDIATE_HIT",
            publication_year=1980,
            field="physics",
            early_citation_percentile=1.0,
            annual_citation_counts=tuple([20] * 20),
        )

    def test_first_burst_age(self):
        self.assertEqual(
            first_burst_age(
                tuple([0] * 10 + [8, 8, 8, 8]),
                wake_years=4,
                min_wake_rate=5.0,
            ),
            9,
        )

    def test_future_case_can_be_control_before_it_awakens(self):
        eligible, rate, burst = is_at_risk_dormant_control(
            self.case,
            self.future_case,
        )
        self.assertTrue(eligible)
        self.assertAlmostEqual(rate, 1.0)
        self.assertGreater(burst, self.case.robust_sleep_years)

    def test_early_hit_is_not_at_risk_dormant(self):
        eligible, _, _ = is_at_risk_dormant_control(
            self.case,
            self.early_hit,
        )
        self.assertFalse(eligible)

    def test_matching_prefers_similar_sleep_depth(self):
        matches, unmatched = match_awakening_risk_sets(
            [self.case, self.dormant, self.future_case, self.early_hit],
            controls_per_case=1,
        )
        self.assertFalse(
            self.case.paper_id in unmatched
        )
        case_match = next(
            match for match in matches if match.case_id == "sb"
        )
        self.assertIn(
            case_match.control_id,
            {"dormant", "future"},
        )
        self.assertAlmostEqual(case_match.control_rate_to_event, 1.0)

    def test_contrast_exposes_risk_set_semantics(self):
        result = build_awakening_risk_set_contrast(
            [self.case, self.dormant, self.future_case, self.early_hit]
        )
        self.assertEqual(result["design"], "event-time risk-set matching")
        self.assertTrue(
            result["rules"]["control_may_awaken_later"]
        )
        self.assertFalse(
            result["rules"]["post_event_control_outcomes_used_for_matching"]
        )


if __name__ == "__main__":
    unittest.main()
