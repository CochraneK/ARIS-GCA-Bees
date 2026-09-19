import unittest

from mechanism_cohort import (
    CorpusPaper,
    build_mechanism_cohort,
    prefilter_sciscinet_rows,
)


def make_history(early, middle, late):
    return tuple(early + middle + late)


class MechanismCohortTests(unittest.TestCase):
    def test_no_sb_blocks_mechanism_claim(self):
        papers = []
        for i in range(20):
            papers.append(
                CorpusPaper(
                    paper_id=f"p{i}",
                    publication_year=1980,
                    field="physics",
                    annual_citation_counts=tuple([1] * 20),
                )
            )
        result = build_mechanism_cohort(
            papers,
            min_stratum_size=20,
        )
        self.assertFalse(result["mechanism_ready"])
        self.assertEqual(result["n_robust_sleeping_beauties"], 0)
        self.assertIsNotNone(result["mechanism_block_reason"])

    def test_robust_sb_and_controls_are_created(self):
        papers = []

        # One true delayed-recognition case:
        papers.append(
            CorpusPaper(
                paper_id="sb",
                publication_year=1980,
                field="physics",
                annual_citation_counts=tuple(
                    [0] * 10 + [6, 8, 10, 12] + [20, 25, 30, 35, 40, 45]
                ),
                reference_count=20,
                author_count=2,
            )
        )

        # Low-early / low-late forgotten controls.
        for i in range(1, 8):
            papers.append(
                CorpusPaper(
                    paper_id=f"forgotten{i}",
                    publication_year=1980,
                    field="physics",
                    annual_citation_counts=tuple(
                        [0] * 10 + [0] * 10
                    ),
                    reference_count=20 + i,
                    author_count=2,
                )
            )

        # Immediate hits.
        for i in range(1, 7):
            papers.append(
                CorpusPaper(
                    paper_id=f"hit{i}",
                    publication_year=1980,
                    field="physics",
                    annual_citation_counts=tuple(
                        [30] * 10 + [30] * 10
                    ),
                    reference_count=20 + i,
                    author_count=2,
                )
            )

        # Fading papers.
        for i in range(1, 7):
            papers.append(
                CorpusPaper(
                    paper_id=f"fade{i}",
                    publication_year=1980,
                    field="physics",
                    annual_citation_counts=tuple(
                        [12] * 10 + [0] * 10
                    ),
                    reference_count=20 + i,
                    author_count=2,
                )
            )

        result = build_mechanism_cohort(
            papers,
            min_stratum_size=20,
            sb_min_total_citations=50,
            matching_early_percentile_caliper=0.25,
        )
        self.assertTrue(result["mechanism_ready"])
        # One synthetic SB is enough to prove cases exist, but not enough to
        # assess matched-group SMD balance.
        self.assertFalse(result["mechanism_analysis_ready"])
        self.assertIn(
            "SB-vs-at-risk-dormant balance not assessable",
            result["mechanism_analysis_block_reasons"],
        )
        self.assertGreaterEqual(
            result["state_counts"].get("SLEEPING_BEAUTY", 0),
            1,
        )
        self.assertTrue(
            result["contrasts"]["SB_vs_AT_RISK_DORMANT"]["matches"]
        )
        self.assertTrue(
            result["contrasts"]["SB_vs_FORGOTTEN"]["matches"]
        )
        self.assertTrue(
            result["contrasts"]["SB_vs_IMMEDIATE_HIT"]["matches"]
        )

    def test_multiple_balanced_pairs_can_pass_analysis_readiness(self):
        papers = []
        for sb_index in range(2):
            papers.append(
                CorpusPaper(
                    paper_id=f"sb{sb_index}",
                    publication_year=1980,
                    field="physics",
                    annual_citation_counts=tuple(
                        [0] * 10
                        + [6 + sb_index, 8, 10, 12]
                        + [20, 25, 30, 35, 40, 45]
                    ),
                    reference_count=20 + sb_index,
                    author_count=2,
                )
            )
        for i in range(8):
            papers.append(
                CorpusPaper(
                    paper_id=f"forgotten{i}",
                    publication_year=1980,
                    field="physics",
                    annual_citation_counts=tuple([0] * 20),
                    reference_count=20 + (i % 2),
                    author_count=2,
                )
            )
        for i in range(6):
            papers.append(
                CorpusPaper(
                    paper_id=f"hit{i}",
                    publication_year=1980,
                    field="physics",
                    annual_citation_counts=tuple([30] * 20),
                    reference_count=20 + (i % 2),
                    author_count=2,
                )
            )
        for i in range(6):
            papers.append(
                CorpusPaper(
                    paper_id=f"fade{i}",
                    publication_year=1980,
                    field="physics",
                    annual_citation_counts=tuple([12] * 10 + [0] * 10),
                    reference_count=20 + (i % 2),
                    author_count=2,
                )
            )

        result = build_mechanism_cohort(
            papers,
            min_stratum_size=20,
            sb_min_total_citations=50,
            matching_early_percentile_caliper=0.30,
            min_primary_match_rate=0.50,
        )
        self.assertTrue(result["mechanism_ready"])
        self.assertTrue(
            result["contrasts"]["SB_vs_AT_RISK_DORMANT"]["balance"][
                "balance_assessable"
            ]
        )

    def test_small_stratum_abstains(self):
        papers = [
            CorpusPaper(
                paper_id="p1",
                publication_year=1980,
                field="physics",
                annual_citation_counts=tuple([0] * 20),
            )
        ]
        result = build_mechanism_cohort(
            papers,
            min_stratum_size=20,
        )
        self.assertEqual(
            result["state_counts"]["ABSTAIN_STRATUM_TOO_SMALL"],
            1,
        )

    def test_sciscinet_prefilter_is_only_a_prefilter(self):
        rows = [
            {"paperid": "a", "SB_B": 40, "cited_by_count": 60},
            {"paperid": "b", "SB_B": 20, "cited_by_count": 100},
            {"paperid": "c", "SB_B": 100, "cited_by_count": 10},
        ]
        selected = prefilter_sciscinet_rows(rows)
        self.assertEqual([row["paperid"] for row in selected], ["a"])


if __name__ == "__main__":
    unittest.main()
