import csv
import tempfile
import unittest
from pathlib import Path

from scan_local_corpus import scan


class LocalScanTests(unittest.TestCase):
    def test_scan_excludes_future_citation_and_keeps_state_conservative(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            papers = tmp / "papers.csv"
            citations = tmp / "citations.csv"

            with papers.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["paper_id", "publication_year"],
                )
                writer.writeheader()
                writer.writerows(
                    [
                        {"paper_id": "a", "publication_year": 2000},
                        {"paper_id": "b", "publication_year": 2000},
                        {"paper_id": "c1", "publication_year": 2001},
                        {"paper_id": "c2", "publication_year": 2010},
                    ]
                )

            with citations.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["citing_paper_id", "cited_paper_id"],
                )
                writer.writeheader()
                writer.writerows(
                    [
                        {"citing_paper_id": "c1", "cited_paper_id": "a"},
                        {"citing_paper_id": "c2", "cited_paper_id": "a"},
                    ]
                )

            result = scan(
                paper_table=papers,
                citation_table=citations,
                cutoff_year=2005,
                cohort_start=2000,
                cohort_end=2000,
                strategy="current_citations",
                top_k=2,
            )

            self.assertEqual(result["n_targets"], 2)
            cards = {card["paper_id"]: card for card in result["cards"]}
            self.assertEqual(
                cards["a"]["citation_trajectory"]["total_citations"],
                1,
            )
            self.assertEqual(cards["a"]["state"], "INSUFFICIENT_DATA")
            self.assertEqual(cards["b"]["state"], "INSUFFICIENT_DATA")


if __name__ == "__main__":
    unittest.main()
