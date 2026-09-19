import unittest

from pilotM_merge_shards import merge_shards


class PilotMMergeShardTests(unittest.TestCase):
    def _paper(self, paper_id, counts):
        return {
            "paper_id": paper_id,
            "publication_year": 1980,
            "field": "OPENALEX_PRIMARY_FIELD_31",
            "annual_citation_counts": counts,
            "reference_count": 20,
            "author_count": 2,
        }

    def test_deduplicates_before_classification(self):
        base = [1] * 20
        shard1 = {
            "provenance": {"seed": 1},
            "papers": [
                self._paper(f"a{i}", base) for i in range(20)
            ],
        }
        shard2 = {
            "provenance": {"seed": 2},
            "papers": [
                self._paper("a0", base),
                *[
                    self._paper(f"b{i}", base)
                    for i in range(19)
                ],
            ],
        }
        result = merge_shards([shard1, shard2])
        provenance = result["input_provenance"]
        self.assertEqual(provenance["n_shards"], 2)
        self.assertEqual(provenance["n_unique_papers"], 39)
        self.assertEqual(provenance["n_duplicate_rows_removed"], 1)
        self.assertIn("a0", provenance["duplicate_paper_ids"])
        self.assertEqual(result["n_input_papers"], 39)


if __name__ == "__main__":
    unittest.main()
