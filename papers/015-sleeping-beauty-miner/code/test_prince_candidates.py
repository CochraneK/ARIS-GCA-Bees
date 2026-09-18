import unittest

from prince_candidates import (
    CitingWork,
    extract_prince_candidates,
    prince_evidence_coverage,
)


class PrinceCandidateTests(unittest.TestCase):
    def test_window_and_ordering(self):
        rows = [
            CitingWork("early", 1990, later_cocitation_count=100),
            CitingWork("near-before", 1994, later_cocitation_count=10),
            CitingWork("exact", 1995, later_cocitation_count=5),
            CitingWork("near-after", 1996, later_cocitation_count=20),
            CitingWork("late", 2005, later_cocitation_count=500),
        ]
        result = extract_prince_candidates(
            rows,
            awakening_year=1995,
            years_before=3,
            years_after=2,
        )
        self.assertEqual(
            [row.paper_id for row in result],
            ["exact", "near-before", "near-after"],
        )

    def test_tied_temporal_distance_prefers_pre_awake(self):
        result = extract_prince_candidates(
            [
                CitingWork("after", 1996),
                CitingWork("before", 1994),
            ],
            awakening_year=1995,
            years_before=2,
            years_after=2,
        )
        self.assertEqual(result[0].paper_id, "before")

    def test_no_causal_claim_in_serialized_output(self):
        row = extract_prince_candidates(
            [CitingWork("p", 2000)],
            awakening_year=2000,
        )[0]
        self.assertFalse(row.as_dict()["causal_claim"])

    def test_coverage(self):
        rows = extract_prince_candidates(
            [
                CitingWork(
                    "a",
                    2000,
                    later_cocitation_count=3,
                    community_spread=2,
                    semantic_similarity=0.8,
                ),
                CitingWork("b", 2001),
            ],
            awakening_year=2000,
        )
        coverage = prince_evidence_coverage(rows)
        self.assertEqual(coverage["n_candidates"], 2)
        self.assertEqual(coverage["cocitation_coverage"], 0.5)
        self.assertEqual(coverage["community_coverage"], 0.5)
        self.assertEqual(coverage["semantic_coverage"], 0.5)

    def test_invalid_similarity_rejected(self):
        with self.assertRaises(ValueError):
            extract_prince_candidates(
                [CitingWork("p", 2000, semantic_similarity=1.5)],
                awakening_year=2000,
            )


if __name__ == "__main__":
    unittest.main()
