#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "analysis"))

from map_ford_domains import classify  # noqa: E402


class FordDomainMappingTests(unittest.TestCase):
    def test_direct_mapping_examples(self) -> None:
        self.assertEqual(classify("mathematician")[0], "1 Natural sciences")
        self.assertEqual(classify("engineer")[0], "2 Engineering and technology")
        self.assertEqual(classify("physician")[0], "3 Medical and health sciences")
        self.assertEqual(classify("psychologist")[0], "5 Social sciences")
        self.assertEqual(classify("historian")[0], "6 Humanities and the arts")

    def test_generic_occupation_stays_unclassified(self) -> None:
        broad, second, basis = classify("academic")
        self.assertEqual(broad, "unclassified")
        self.assertEqual(second, "unclassified")
        self.assertIn("generic", basis)

    def test_unknown_label_is_not_guessed(self) -> None:
        broad, _, basis = classify("future_unknown_field")
        self.assertEqual(broad, "unclassified")
        self.assertEqual(basis, "unmapped_source_occupation")


if __name__ == "__main__":
    unittest.main(verbosity=2)
