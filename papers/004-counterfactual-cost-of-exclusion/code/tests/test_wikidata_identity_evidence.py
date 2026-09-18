#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "resolve"))

import wikidata_identity_evidence as wie  # noqa: E402


class WikidataIdentityEvidenceTests(unittest.TestCase):
    def test_fetch_entities_accepts_dict_payload(self) -> None:
        payload = {
            "entities": {
                "Q1": {"id": "Q1", "labels": {}},
                "Q2": {"id": "Q2", "labels": {}},
            }
        }
        with patch.object(wie, "request_json", return_value=payload):
            result = wie.fetch_entities(["Q1", "Q2"])
        self.assertEqual(set(result), {"Q1", "Q2"})

    def test_fetch_entities_accepts_list_payload(self) -> None:
        payload = {
            "entities": [
                {"id": "Q1", "labels": {}},
                {"id": "Q2", "labels": {}},
            ]
        }
        with patch.object(wie, "request_json", return_value=payload):
            result = wie.fetch_entities(["Q1", "Q2"])
        self.assertEqual(set(result), {"Q1", "Q2"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
