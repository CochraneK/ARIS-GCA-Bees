import unittest

from mechanism_cohort_cli import run_payload


class MechanismCohortCliTests(unittest.TestCase):
    def test_payload_preserves_provenance_and_blocks_no_sb(self):
        papers = [
            {
                "paper_id": f"p{i}",
                "publication_year": 1980,
                "field": "physics",
                "annual_citation_counts": [1] * 20,
                "reference_count": 20,
                "author_count": 2,
            }
            for i in range(20)
        ]
        result = run_payload(
            {
                "papers": papers,
                "provenance": {
                    "source": "synthetic",
                    "snapshot": "fixture-v1",
                },
            }
        )
        self.assertFalse(result["mechanism_ready"])
        self.assertFalse(result["mechanism_analysis_ready"])
        self.assertEqual(
            result["input_provenance"]["snapshot"],
            "fixture-v1",
        )
        self.assertEqual(
            result["cli_parameters"]["max_abs_smd"],
            0.10,
        )

    def test_missing_history_is_rejected(self):
        with self.assertRaises(KeyError):
            run_payload(
                [
                    {
                        "paper_id": "p",
                        "publication_year": 1980,
                        "field": "physics",
                    }
                ]
            )


if __name__ == "__main__":
    unittest.main()
