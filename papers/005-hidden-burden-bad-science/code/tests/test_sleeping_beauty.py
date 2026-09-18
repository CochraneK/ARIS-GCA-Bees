from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from sleeping_beauty import (  # noqa: E402
    analyze,
    annual_series,
    awakening_age,
    beauty_coefficient,
    peak_age,
)


class SleepingBeautyTests(unittest.TestCase):
    def test_linear_growth_has_zero_beauty(self):
        citations = [0, 1, 2, 3, 4]
        self.assertEqual(peak_age(citations), 4)
        self.assertAlmostEqual(beauty_coefficient(citations), 0.0)

    def test_dormant_then_spike_has_positive_beauty(self):
        citations = [0, 0, 0, 0, 10]
        self.assertGreater(beauty_coefficient(citations), 0)
        self.assertLess(awakening_age(citations), peak_age(citations))

    def test_peak_at_publication_is_zero(self):
        citations = [10, 5, 3, 1]
        self.assertEqual(peak_age(citations), 0)
        self.assertEqual(beauty_coefficient(citations), 0.0)
        self.assertEqual(awakening_age(citations), 0)

    def test_missing_calendar_years_fill_zero(self):
        series = annual_series(
            2000,
            {2000: 1, 2002: 3},
            observation_end_year=2003,
        )
        self.assertEqual(series, [1, 0, 3, 0])

    def test_peak_tie_uses_earliest_peak(self):
        self.assertEqual(peak_age([0, 5, 1, 5]), 1)

    def test_sample_flag_is_explicitly_relative(self):
        rows = [
            {"paper_id": "A", "openalex_id": "W1", "publication_year": "2000", "citation_year": "2000", "citations": "0"},
            {"paper_id": "A", "openalex_id": "W1", "publication_year": "2000", "citation_year": "2004", "citations": "10"},
            {"paper_id": "B", "openalex_id": "W2", "publication_year": "2000", "citation_year": "2000", "citations": "1"},
            {"paper_id": "B", "openalex_id": "W2", "publication_year": "2000", "citation_year": "2001", "citations": "2"},
        ]
        out = analyze(rows, top_fraction=0.5)
        self.assertTrue(out["beauty_coefficient"]["continuous_primary_measure"])
        self.assertIn("not a natural/universal", out["sample_relative_flag"]["warning"])


if __name__ == "__main__":
    unittest.main()
