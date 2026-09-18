from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from make_citation_ai_packet import make_packets  # noqa: E402


class CitationAIPacketTests(unittest.TestCase):
    def test_two_assignments_per_edge_and_no_semantic_label_leak(self):
        rows = [{
            "edge_id": "E1",
            "source_openalex_id": "W1",
            "source_doi": "10.1/a",
            "source_retraction_date": "2020-01-01",
            "citing_openalex_id": "W2",
            "citing_doi": "10.2/b",
            "citing_title": "X",
            "citing_publication_date": "2021-01-01",
            "citing_work_type": "article",
            "citing_domain": "Health Sciences",
            "citing_field": "Medicine",
            "citing_subfield": "X",
            "citing_has_fulltext": "1",
            "citing_is_oa": "1",
            "citation_after_retraction": "YES",
            "semantic_class": "RESULT_DEPENDENCE",
        }]
        reviewer, linkage, summary = make_packets(rows, ["A", "B"])
        self.assertEqual(len(reviewer), 2)
        self.assertEqual(len(linkage), 2)
        self.assertEqual(summary["assignments_total"], 2)
        for r in reviewer:
            self.assertEqual(r["semantic_class"], "")
            self.assertEqual(r["prompt_version"], "CIT-EDGE-V1")
        for r in linkage:
            self.assertEqual(r["semantic_class"], "RESULT_DEPENDENCE")

    def test_duplicate_edge_fails_closed(self):
        rows = [{"edge_id": "E1"}, {"edge_id": "E1"}]
        with self.assertRaises(ValueError):
            make_packets(rows, ["A", "B"])


if __name__ == "__main__":
    unittest.main()
