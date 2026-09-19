#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "freeze", HERE / "pilot3_comparator_artifact_freeze.py"
)
freeze = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(freeze)


PUBMED = b"""<PubmedArticleSet><PubmedArticle><PubmedData><ArticleIdList>
<ArticleId IdType="doi">10.1371/journal.pone.0000001</ArticleId>
<ArticleId IdType="pmc">PMC12345</ArticleId>
</ArticleIdList></PubmedData></PubmedArticle></PubmedArticleSet>"""

PMC_OK = b"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
<front><article-meta>
<article-id pub-id-type="doi">10.1371/journal.pone.0000001</article-id>
<title-group><article-title>Ordinary research article</article-title></title-group>
</article-meta></front><body><sec><p>Substantive body text.</p></sec></body>
</article>"""

PMC_NOTICE = b"""<article>
<front><article-meta>
<article-id pub-id-type="doi">10.1371/journal.pone.0000001</article-id>
<title-group><article-title>Ordinary research article</article-title></title-group>
<related-article related-article-type="corrected-article"/>
</article-meta></front><body><p>Body.</p></body></article>"""


class FreezeTests(unittest.TestCase):
    def payload(self):
        return {
            "selected_development_comparators": [
                {
                    "target_id": "t1",
                    "target_doi": "10.1371/journal.pone.9999999",
                    "target_published": "2021-01-01",
                    "candidate_doi": "10.1371/journal.pone.0000001",
                    "candidate_title": "Ordinary research article",
                    "candidate_published": "2021-01-01",
                    "date_distance_days": 0,
                    "notice_negative_screen_pass": True,
                    "pubmed_notice_screen": {"pmid": "123"},
                }
            ]
        }

    def test_success_records_hash_without_full_text(self):
        def fake(url):
            return PUBMED if "db=pubmed" in url else PMC_OK

        out = freeze.qualify_selected(
            self.payload(),
            fetcher=fake,
            retrieved_at_utc="2026-09-19T12:00:00Z",
        )
        self.assertTrue(out["all_selected_frozen"])
        self.assertFalse(out["full_text_committed"])
        self.assertEqual(out["frozen_pass_count"], 1)
        row = out["frozen_comparators"][0]
        self.assertEqual(row["pmc_id"], "PMC12345")
        self.assertEqual(
            row["qualification_state"], "FROZEN_NOTICE_NEGATIVE_FULLTEXT"
        )
        self.assertEqual(len(row["fulltext_sha256"]), 64)
        self.assertNotIn("full_text", row)

    def test_explicit_correction_relation_fails(self):
        def fake(url):
            return PUBMED if "db=pubmed" in url else PMC_NOTICE

        out = freeze.qualify_selected(
            self.payload(),
            fetcher=fake,
            retrieved_at_utc="2026-09-19T12:00:00Z",
        )
        self.assertFalse(out["all_selected_frozen"])
        self.assertEqual(
            out["frozen_comparators"][0]["qualification_state"],
            "FULLTEXT_FREEZE_REVIEW_REQUIRED",
        )

    def test_pubmed_identity_mismatch_raises(self):
        bad = PUBMED.replace(
            b"10.1371/journal.pone.0000001",
            b"10.1371/journal.pone.1234567",
        )
        with self.assertRaises(ValueError):
            freeze.pubmed_to_pmcid(
                bad,
                expected_doi="10.1371/journal.pone.0000001",
            )


if __name__ == "__main__":
    unittest.main()
