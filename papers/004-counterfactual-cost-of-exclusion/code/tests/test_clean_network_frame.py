#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "network"))

from build_clean_network_frame import choose_clean_works  # noqa: E402


class CleanNetworkFrameTests(unittest.TestCase):
    def test_explicit_work_decisions_override_plausible_window(self) -> None:
        corpus = [
            {"person_id": "p1", "openalex_work_id": "W1", "temporal_status": "plausible"},
            {"person_id": "p1", "openalex_work_id": "W2", "temporal_status": "plausible"},
        ]
        identities = [{
            "person_id": "p1",
            "canonical_name": "A",
            "network_observable": "true",
            "verified_openalex_ids": "A1",
        }]
        decisions = [
            {
                "person_id": "p1",
                "openalex_work_id": "W1",
                "work_decision": "KEEP_ORIGINAL",
                "include_in_network": "true",
            },
            {
                "person_id": "p1",
                "openalex_work_id": "W2",
                "work_decision": "EXCLUDE_NAME_COLLISION",
                "include_in_network": "false",
            },
        ]
        clean, errors = choose_clean_works(corpus, identities, decisions)
        self.assertEqual(errors, [])
        self.assertEqual([row["openalex_work_id"] for row in clean], ["W1"])
        self.assertEqual(clean[0]["clean_selection_basis"], "explicit_work_decision")

    def test_released_person_without_explicit_review_uses_plausible_only(self) -> None:
        corpus = [
            {"person_id": "p1", "openalex_work_id": "W1", "temporal_status": "plausible"},
            {"person_id": "p1", "openalex_work_id": "W2", "temporal_status": "outside_after"},
        ]
        identities = [{
            "person_id": "p1",
            "canonical_name": "A",
            "network_observable": "true",
            "verified_openalex_ids": "A1",
        }]
        clean, errors = choose_clean_works(corpus, identities, [])
        self.assertEqual(errors, [])
        self.assertEqual([row["openalex_work_id"] for row in clean], ["W1"])
        self.assertEqual(clean[0]["clean_selection_basis"], "identity_released_plausible_window")

    def test_nonobservable_person_is_not_selected(self) -> None:
        corpus = [{"person_id": "p1", "openalex_work_id": "W1", "temporal_status": "plausible"}]
        identities = [{
            "person_id": "p1",
            "canonical_name": "A",
            "network_observable": "false",
            "verified_openalex_ids": "A1",
        }]
        clean, errors = choose_clean_works(corpus, identities, [])
        self.assertEqual(clean, [])
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
