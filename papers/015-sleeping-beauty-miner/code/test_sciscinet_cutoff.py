import unittest

from sciscinet_adapter import cohort_histories, reconstruct_target_history


class SciSciNetCutoffTests(unittest.TestCase):
    def setUp(self):
        self.years = {
            "target": 2000,
            "early": 2001,
            "cutoff": 2005,
            "future": 2010,
        }
        self.edges = [
            ("early", "target"),
            ("cutoff", "target"),
            ("future", "target"),
        ]

    def test_single_target_excludes_future_edge(self):
        history = reconstruct_target_history(
            "target",
            paper_years=self.years,
            citation_edges=self.edges,
            end_year=2005,
        )
        self.assertEqual(history.counts, (0, 1, 0, 0, 0, 1))
        self.assertEqual(history.total_citations, 2)

    def test_cohort_excludes_future_edge(self):
        histories = cohort_histories(
            ["target"],
            paper_years=self.years,
            citation_edges=self.edges,
            end_year=2005,
        )
        self.assertEqual(histories["target"].total_citations, 2)


if __name__ == "__main__":
    unittest.main()
