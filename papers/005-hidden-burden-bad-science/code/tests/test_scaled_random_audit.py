from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from build_scaled_random_audit import allocate, filter_expr  # noqa: E402


class ScaledAuditTests(unittest.TestCase):
    def test_allocation_hits_total_and_minimum(self):
        counts = {"a": 10000, "b": 20000, "c": 30000}
        out = allocate(counts, total_n=6000, minimum_per_stratum=1000)
        self.assertEqual(sum(out.values()), 6000)
        self.assertTrue(all(v >= 1000 for v in out.values()))
        self.assertGreater(out["c"], out["a"])

    def test_small_total_rejected(self):
        with self.assertRaises(ValueError):
            allocate({"a": 10, "b": 10}, total_n=5, minimum_per_stratum=3)

    def test_filter_freezes_types(self):
        f = filter_expr(2000, 2004)
        self.assertIn("publication_year:2000-2004", f)
        self.assertIn("type:article|review", f)


if __name__ == "__main__":
    unittest.main()
