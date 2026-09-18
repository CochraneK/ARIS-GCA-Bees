from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from build_contamination_exposure import (  # noqa: E402
    bare_oa_id,
    edge_id,
    norm_doi,
    parse_date,
    source_seed,
)


class ContaminationExposureTests(unittest.TestCase):
    def test_doi_normalization(self):
        self.assertEqual(norm_doi("https://doi.org/10.1000/ABC"), "10.1000/abc")
        self.assertEqual(norm_doi("DOI:10.1/X"), "10.1/x")
        self.assertIsNone(norm_doi("Unavailable"))

    def test_date_parsing(self):
        self.assertEqual(parse_date("09/18/2020"), dt.date(2020, 9, 18))
        self.assertEqual(parse_date("2020-09-18"), dt.date(2020, 9, 18))
        self.assertIsNone(parse_date("unknown"))

    def test_openalex_id_normalization(self):
        self.assertEqual(bare_oa_id("https://openalex.org/W123"), "W123")
        self.assertEqual(bare_oa_id("W123"), "W123")

    def test_deterministic_edge_and_seed_ids(self):
        self.assertEqual(edge_id("W1", "W2"), edge_id("W1", "W2"))
        self.assertNotEqual(edge_id("W1", "W2"), edge_id("W1", "W3"))
        self.assertEqual(source_seed("W1", 7), source_seed("W1", 7))
        self.assertNotEqual(source_seed("W1", 7), source_seed("W1", 8))


if __name__ == "__main__":
    unittest.main()
