#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "resolve"))

from build_identity100_draft import blank_row  # noqa: E402


class Identity100DraftTests(unittest.TestCase):
    def candidate(self) -> dict[str, str]:
        return {
            "person_id": "p1",
            "canonical_name": "Historical Person",
            "birth_year": "1900",
            "death_year": "1980",
        }

    def test_fragmentation_initializes_provisional_cluster(self) -> None:
        row = blank_row(
            self.candidate(),
            {
                "review_class": "possible_author_fragmentation",
                "plausible_openalex_ids": "A1;A2",
            },
        )
        self.assertEqual(row["identity_status"], "PROVISIONAL_CLUSTER")
        self.assertEqual(row["network_observable"], "false")
        self.assertEqual(row["mh_blinded_at_identity_lock"], "")

    def test_no_graph_is_protocol_derived_without_mh(self) -> None:
        row = blank_row(
            self.candidate(),
            {"review_class": "no_openalex_search_hit", "plausible_openalex_ids": ""},
        )
        self.assertEqual(row["identity_status"], "NO_GRAPH_RECORD")
        self.assertEqual(row["adjudication_status"], "protocol-derived")
        self.assertEqual(row["mh_blinded_at_identity_lock"], "true")


if __name__ == "__main__":
    unittest.main(verbosity=2)
