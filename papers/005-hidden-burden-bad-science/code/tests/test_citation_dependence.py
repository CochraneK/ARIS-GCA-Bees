from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from citation_dependence import (  # noqa: E402
    is_methodological_contamination,
    is_primary_scf,
    summarize,
)


def edge(edge_id: str, semantic: str, material: str = "NO", component: str = "NO"):
    return {
        "edge_id": edge_id,
        "source_openalex_id": "W0",
        "citing_openalex_id": "W" + edge_id,
        "semantic_class": semantic,
        "component_implicated": component,
        "material_to_downstream_claim": material,
        "source_retraction_known_in_text": "UNKNOWN",
        "citation_after_retraction": "YES",
        "context_access": "FULLTEXT",
        "review_confidence": "HIGH",
    }


class CitationDependenceTests(unittest.TestCase):
    def test_background_and_critique_are_not_primary_contamination(self):
        self.assertFalse(is_primary_scf(edge("1", "BACKGROUND_MENTION")))
        self.assertFalse(is_primary_scf(edge("2", "CRITIQUE_OR_CORRECTION")))

    def test_result_dependence_requires_materiality_yes(self):
        self.assertTrue(is_primary_scf(edge("1", "RESULT_DEPENDENCE", "YES")))
        self.assertFalse(is_primary_scf(edge("2", "RESULT_DEPENDENCE", "NO")))
        self.assertFalse(is_primary_scf(edge("3", "RESULT_DEPENDENCE", "UNKNOWN")))

    def test_method_reuse_is_separate(self):
        row = edge("1", "METHOD_REUSE", "YES", "YES")
        self.assertFalse(is_primary_scf(row))
        self.assertTrue(is_methodological_contamination(row))

    def test_summary_keeps_unresolved_visible(self):
        rows = [
            edge("1", "RESULT_DEPENDENCE", "YES"),
            edge("2", "CRITIQUE_OR_CORRECTION", "NO"),
            edge("3", "INDETERMINATE", "UNKNOWN", "UNKNOWN"),
        ]
        out = summarize(rows)
        self.assertEqual(out["primary_scf_material_dependence_edges"], 1)
        self.assertEqual(out["corrective_or_critique_edges"], 1)
        self.assertEqual(out["unresolved_or_materiality_unknown_edges"], 1)

    def test_invalid_semantic_label_fails_closed(self):
        with self.assertRaises(ValueError):
            summarize([edge("1", "CONTAMINATED", "YES")])


if __name__ == "__main__":
    unittest.main()
