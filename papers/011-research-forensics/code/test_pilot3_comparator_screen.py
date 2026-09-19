import unittest
from unittest.mock import patch

import pilot3_comparator_screen as s


class ComparatorScreenTests(unittest.TestCase):
    def test_pass_requires_both_sources_negative(self):
        row = {
            "candidate_doi": "10.1371/journal.pone.0999999",
            "target_id": "t1",
            "match_rank": 1,
            "date_distance_days": 1,
        }
        with (
            patch.object(
                s,
                "crossref_updates",
                return_value={
                    "query": "x",
                    "total_results": 0,
                    "update_records": [],
                },
            ),
            patch.object(
                s,
                "pubmed_ids_for_doi",
                return_value=["123"],
            ),
            patch.object(
                s,
                "pubmed_notice_relations",
                return_value={
                    "pmid": "123",
                    "comments_corrections": [],
                    "notice_relations": [],
                    "publication_types": ["Journal Article"],
                    "notice_publication_types": [],
                },
            ),
            patch.object(s.time, "sleep"),
        ):
            out = s.screen_candidate(row)
        self.assertTrue(out["notice_negative_screen_pass"])
        self.assertEqual(
            out["screen_state"],
            "NOTICE_NEGATIVE_SCREEN_PASS_ARTIFACT_PENDING",
        )

    def test_notice_relation_blocks_candidate(self):
        row = {
            "candidate_doi": "10.1371/journal.pone.0999999",
            "target_id": "t1",
            "match_rank": 1,
            "date_distance_days": 1,
        }
        with (
            patch.object(
                s,
                "crossref_updates",
                return_value={
                    "query": "x",
                    "total_results": 0,
                    "update_records": [],
                },
            ),
            patch.object(
                s,
                "pubmed_ids_for_doi",
                return_value=["123"],
            ),
            patch.object(
                s,
                "pubmed_notice_relations",
                return_value={
                    "pmid": "123",
                    "comments_corrections": [
                        {
                            "ref_type": "ErratumIn",
                            "ref_source": "x",
                            "linked_pmid": "456",
                        }
                    ],
                    "notice_relations": [
                        {
                            "ref_type": "ErratumIn",
                            "ref_source": "x",
                            "linked_pmid": "456",
                        }
                    ],
                    "publication_types": ["Journal Article"],
                    "notice_publication_types": [],
                },
            ),
            patch.object(s.time, "sleep"),
        ):
            out = s.screen_candidate(row)
        self.assertFalse(out["notice_negative_screen_pass"])

    def test_pubmed_unresolved_is_not_negative(self):
        row = {
            "candidate_doi": "10.1371/journal.pone.0999999",
            "target_id": "t1",
            "match_rank": 1,
            "date_distance_days": 1,
        }
        with (
            patch.object(
                s,
                "crossref_updates",
                return_value={
                    "query": "x",
                    "total_results": 0,
                    "update_records": [],
                },
            ),
            patch.object(s, "pubmed_ids_for_doi", return_value=[]),
            patch.object(s.time, "sleep"),
        ):
            out = s.screen_candidate(row)
        self.assertFalse(out["notice_negative_screen_pass"])
        self.assertFalse(out["pubmed_resolved_exactly_once"])


if __name__ == "__main__":
    unittest.main()
