#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "network"))

from build_verified_work_corpus import (  # noqa: E402
    deduplicate_person_works,
    plausible_career_window,
    temporal_status,
    work_dedup_key,
)


class VerifiedWorkCorpusTests(unittest.TestCase):
    def test_same_doi_across_fragments_deduplicates(self) -> None:
        records = [
            {
                "dedup_key": "doi:10.1/example",
                "source_author_id": "A1",
                "openalex_work_id": "W1",
                "doi": "10.1/example",
                "title": "Same Work",
                "publication_year": 1950,
                "cited_by_count": 2,
            },
            {
                "dedup_key": "doi:10.1/example",
                "source_author_id": "A2",
                "openalex_work_id": "W2",
                "doi": "10.1/example",
                "title": "Same Work",
                "publication_year": 1950,
                "cited_by_count": 10,
            },
        ]
        out = deduplicate_person_works(records)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["duplicate_records_n"], 2)
        self.assertEqual(out[0]["source_author_ids"], ["A1", "A2"])
        self.assertEqual(out[0]["cited_by_count"], 10)

    def test_title_year_is_fallback_dedup_key(self) -> None:
        work = {
            "id": "https://openalex.org/W1",
            "doi": None,
            "display_name": "A Distinctive Historical Work",
            "publication_year": 1938,
        }
        self.assertEqual(
            work_dedup_key(work),
            "titleyear:a distinctive historical work|1938",
        )

    def test_candidate_lifetime_window_is_explicit(self) -> None:
        lo, hi = plausible_career_window(1902, 1980)
        self.assertEqual((lo, hi), (1917, 1985))
        self.assertEqual(temporal_status(1938, lo, hi), "plausible")
        self.assertEqual(temporal_status(1892, lo, hi), "outside_before")
        self.assertEqual(temporal_status(2003, lo, hi), "outside_after")
        self.assertEqual(temporal_status(None, lo, hi), "undated")


if __name__ == "__main__":
    unittest.main(verbosity=2)
