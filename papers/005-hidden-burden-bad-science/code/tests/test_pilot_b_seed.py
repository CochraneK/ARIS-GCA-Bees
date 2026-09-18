from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from build_pilot_b_seed import (  # noqa: E402
    inclusion_probability,
    norm_doi,
    parse_year,
    rw_stratum,
)


class PilotBSeedTests(unittest.TestCase):
    def test_normalize_doi(self):
        self.assertEqual(norm_doi("https://doi.org/10.1/ABC"), "10.1/abc")
        self.assertEqual(norm_doi("DOI:10.2/X"), "10.2/x")
        self.assertIsNone(norm_doi("Unavailable"))

    def test_parse_legacy_and_iso_years(self):
        self.assertEqual(parse_year("5/17/2018 0:00"), 2018)
        self.assertEqual(parse_year("2020-09-01"), 2020)
        self.assertEqual(parse_year("article published in 2017"), 2017)
        self.assertIsNone(parse_year("unknown"))

    def test_rw_strata_are_mutually_exclusive_by_priority(self):
        paper = {
            "e1s_narrow_auto": 1,
            "paper_mill_signal": 1,
            "e3_error_signal": 1,
            "e1p_strong_auto": 1,
            "natures": {"Expression of concern"},
        }
        self.assertEqual(rw_stratum(paper), "rw_e1s_narrow")
        paper["e1s_narrow_auto"] = 0
        self.assertEqual(rw_stratum(paper), "rw_paper_mill")
        paper["paper_mill_signal"] = 0
        self.assertEqual(rw_stratum(paper), "rw_major_error")

    def test_union_inclusion_probability(self):
        self.assertAlmostEqual(inclusion_probability(0.1, 0.2), 0.28)
        self.assertAlmostEqual(inclusion_probability(0.0, 0.2), 0.2)
        self.assertAlmostEqual(inclusion_probability(0.1, 0.0), 0.1)
        self.assertAlmostEqual(inclusion_probability(1.0, 0.2), 1.0)


if __name__ == "__main__":
    unittest.main()
