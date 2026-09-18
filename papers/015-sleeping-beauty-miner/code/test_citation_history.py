import unittest

from citation_history import citation_history_from_citing_years, truncate_history


class CitationHistoryTests(unittest.TestCase):
    def test_zero_fills_missing_years(self):
        history = citation_history_from_citing_years(
            2000,
            [2000, 2003, 2003, 2005],
            end_year=2005,
        )
        self.assertEqual(history.counts, (1, 0, 0, 2, 0, 1))
        self.assertEqual(history.total_citations, 4)

    def test_invalid_prepublication_edge_is_flagged(self):
        history = citation_history_from_citing_years(
            2000,
            [1999, 2000, 2001],
        )
        self.assertEqual(history.invalid_prepublication_edges, 1)
        self.assertEqual(history.valid_edges, 2)
        self.assertEqual(history.counts, (1, 1))

    def test_strict_mode_rejects_invalid_edge(self):
        with self.assertRaises(ValueError):
            citation_history_from_citing_years(
                2000,
                [1999, 2000],
                strict=True,
            )

    def test_explicit_end_year_cannot_drop_observed_edges(self):
        with self.assertRaises(ValueError):
            citation_history_from_citing_years(
                2000,
                [2005],
                end_year=2004,
            )

    def test_truncate_history_is_cutoff_safe(self):
        full = citation_history_from_citing_years(
            2000,
            [2000, 2001, 2004, 2004],
            end_year=2005,
        )
        early = truncate_history(full, 2002)
        self.assertEqual(early.counts, (1, 1, 0))
        self.assertEqual(early.total_citations, 2)
        self.assertEqual(early.end_year, 2002)


if __name__ == "__main__":
    unittest.main()
