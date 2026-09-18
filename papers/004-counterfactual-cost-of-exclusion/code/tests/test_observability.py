#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "analysis"))

from summarize_observability import summarize  # noqa: E402


class ObservabilitySummaryTests(unittest.TestCase):
    def test_summary_rates(self) -> None:
        candidates = [
            {"person_id": "p1", "pilot_stratum": "1900_1924|v_q1", "region": "Europe", "gender": "Male", "level2_main_occ": "Academia", "level3_main_occ": "Math"},
            {"person_id": "p2", "pilot_stratum": "1900_1924|v_q1", "region": "Europe", "gender": "Female", "level2_main_occ": "Academia", "level3_main_occ": "Biology"},
        ]
        decisions = [
            {"person_id": "p1", "identity_status": "VERIFIED_SINGLE", "network_observable": "true"},
            {"person_id": "p2", "identity_status": "NO_GRAPH_RECORD", "network_observable": "false"},
        ]
        rows, overall = summarize(candidates, decisions)
        self.assertEqual(overall["candidate_n"], 2)
        self.assertEqual(overall["verified_n"], 1)
        self.assertEqual(overall["network_observable_n"], 1)
        europe = next(row for row in rows if row["group_variable"] == "region" and row["group_value"] == "Europe")
        self.assertEqual(europe["candidate_n"], 2)
        self.assertAlmostEqual(europe["verified_rate"], 0.5)
        self.assertAlmostEqual(europe["no_graph_rate"], 0.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
