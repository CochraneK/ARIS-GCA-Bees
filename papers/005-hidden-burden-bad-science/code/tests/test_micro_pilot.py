from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from make_micro_pilot import select_micro_pilot  # noqa: E402


class MicroPilotTests(unittest.TestCase):
    def test_balanced_groups_and_domain_coverage(self):
        groups = [
            "population_random",
            "rw_e1s_narrow",
            "rw_paper_mill",
            "rw_major_error",
            "rw_expression_of_concern",
            "rw_process_integrity",
        ]
        domains = [
            "Health Sciences",
            "Life Sciences",
            "Physical Sciences",
            "Social Sciences",
        ]
        rows = []
        i = 0
        for group in groups:
            for domain in domains:
                for _ in range(4):
                    i += 1
                    rows.append(
                        {
                            "paper_id": f"P{i}",
                            "selected_via": (
                                "population_random"
                                if group == "population_random"
                                else "rw_enrichment"
                            ),
                            "rw_enrichment_stratum": (
                                "" if group == "population_random" else group
                            ),
                            "primary_domain": domain,
                        }
                    )

        quotas = {g: 8 for g in groups}
        selected = select_micro_pilot(rows, quotas, seed=42)
        self.assertEqual(len(selected), 48)

        for group in groups:
            group_rows = [
                row
                for row in selected
                if (
                    row["selected_via"] == "population_random"
                    and group == "population_random"
                )
                or row.get("rw_enrichment_stratum") == group
            ]
            self.assertEqual(len(group_rows), 8)
            self.assertEqual(
                {row["primary_domain"] for row in group_rows},
                set(domains),
            )


if __name__ == "__main__":
    unittest.main()
