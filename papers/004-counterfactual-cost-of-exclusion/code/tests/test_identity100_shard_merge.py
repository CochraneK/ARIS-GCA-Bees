#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "resolve"))

from merge_identity100_shards import nested_openalex_id, wrapper_key  # noqa: E402


class Identity100ShardMergeTests(unittest.TestCase):
    def test_nested_author_id(self) -> None:
        row = {
            "person_id": "p1",
            "author": {"id": "https://openalex.org/A123"},
        }
        self.assertEqual(nested_openalex_id(row, "author"), "A123")
        self.assertEqual(wrapper_key(row, "author"), ("p1", "A123"))

    def test_nested_work_id(self) -> None:
        row = {
            "person_id": "p1",
            "author_id": "A123",
            "work": {"id": "https://openalex.org/W456"},
        }
        self.assertEqual(nested_openalex_id(row, "work"), "W456")
        self.assertEqual(wrapper_key(row, "work"), ("p1", "W456"))

    def test_same_work_id_for_two_people_remains_distinct_provenance(self) -> None:
        a = {"person_id": "p1", "work": {"id": "https://openalex.org/W1"}}
        b = {"person_id": "p2", "work": {"id": "https://openalex.org/W1"}}
        self.assertNotEqual(wrapper_key(a, "work"), wrapper_key(b, "work"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
