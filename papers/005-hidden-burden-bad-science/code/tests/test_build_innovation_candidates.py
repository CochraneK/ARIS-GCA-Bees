from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from build_innovation_candidates import (  # noqa: E402
    day_before,
    reconstruct_abstract,
    semantic_query_text,
    source_field_id,
)


class InnovationCandidateTests(unittest.TestCase):
    def test_reconstruct_abstract(self):
        inv = {"world": [1], "hello": [0], "again": [2]}
        self.assertEqual(reconstruct_abstract(inv), "hello world again")

    def test_semantic_query_uses_title_and_abstract(self):
        work = {
            "display_name": "Title",
            "abstract_inverted_index": {"Abstract": [0], "text": [1]},
        }
        q = semantic_query_text(work)
        self.assertTrue(q.startswith("Title"))
        self.assertIn("Abstract text", q)

    def test_day_before_event(self):
        self.assertEqual(day_before("2020-03-01"), "2020-02-29")

    def test_source_field_id(self):
        work = {
            "primary_topic": {
                "field": {"id": "https://openalex.org/fields/27"}
            }
        }
        self.assertEqual(source_field_id(work), "27")


if __name__ == "__main__":
    unittest.main()
