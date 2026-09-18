from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from make_adjudication_packet import make_packets  # noqa: E402


class AdjudicationPacketTests(unittest.TestCase):
    def test_reviewer_packet_hides_design_metadata_manager_preserves_all(self):
        rows = [
            {
                "paper_id": "P1",
                "doi": "10.1/a",
                "openalex_id": "W1",
                "publication_year": "2019",
                "work_type": "article",
                "primary_domain": "Life Sciences",
                "primary_field": "Medicine",
                "primary_subfield": "X",
                "audit_stratum": "2015_2019",
                "stratum_population_N": "31791658",
                "stratum_sample_n": "1925",
                "selected_via": "rw_enrichment",
                "rw_enrichment_stratum": "rw_e1s_narrow",
                "det_formal_retraction": "1",
                "det_e1s_narrow_reason": "1",
                "aris_inclusion_probability": "0.1",
                "aris_design_weight": "10",
            },
            {
                "paper_id": "P2",
                "doi": "",
                "openalex_id": "W2",
                "publication_year": "2020",
                "work_type": "review",
                "primary_domain": "Social Sciences",
                "primary_field": "Psychology",
                "primary_subfield": "Y",
                "audit_stratum": "2020_2024",
                "stratum_population_N": "30282727",
                "stratum_sample_n": "1881",
                "selected_via": "population_random",
                "rw_enrichment_stratum": "",
                "det_formal_retraction": "0",
                "det_e1s_narrow_reason": "0",
                "aris_inclusion_probability": "0.01",
                "aris_design_weight": "100",
            },
        ]
        reviewer, manager = make_packets(
            rows, reviewers=["R1", "R2"], double_fraction=1.0, seed=7
        )
        self.assertEqual(len(reviewer), 4)
        self.assertEqual(len(manager), 4)

        for row in reviewer:
            self.assertNotIn("selected_via", row)
            self.assertNotIn("rw_enrichment_stratum", row)
            self.assertNotIn("det_formal_retraction", row)
            self.assertNotIn("aris_design_weight", row)
            self.assertNotIn("audit_stratum", row)
            self.assertNotIn("stratum_population_N", row)
            self.assertNotIn("stratum_sample_n", row)
            self.assertIn("scientific_state", row)

        for row in manager:
            self.assertIn("selected_via", row)
            self.assertIn("rw_enrichment_stratum", row)
            self.assertIn("det_formal_retraction", row)
            self.assertIn("aris_design_weight", row)
            self.assertIn("audit_stratum", row)
            self.assertIn("stratum_population_N", row)
            self.assertIn("stratum_sample_n", row)
            self.assertEqual(row["stratum_population_N"] in {"31791658", "30282727"}, True)

    def test_duplicate_paper_id_fails_closed(self):
        rows = [
            {"paper_id": "P1"},
            {"paper_id": "P1"},
        ]
        with self.assertRaises(ValueError):
            make_packets(rows, reviewers=["R1", "R2"], double_fraction=0, seed=1)


if __name__ == "__main__":
    unittest.main()
