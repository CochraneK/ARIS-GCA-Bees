import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pilotM_full_frame_histories as histories


class FullFrameHistoryTests(unittest.TestCase):
    def test_resume_skips_completed_ids_and_appends_new_rows(self):
        inventory = {
            "frames": [
                {
                    "case_id": "caseA",
                    "publication_year": 1921,
                    "primary_field_id": "25",
                    "works": [
                        {
                            "openalex_id": "W1",
                            "title": "One",
                            "publication_year": 1921,
                            "primary_field_id": "25",
                            "reference_count": 1,
                            "author_count": 1,
                        },
                        {
                            "openalex_id": "W2",
                            "title": "Two",
                            "publication_year": 1921,
                            "primary_field_id": "25",
                            "reference_count": 2,
                            "author_count": 2,
                        },
                    ],
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            checkpoint = Path(tmp) / "checkpoint.jsonl"
            checkpoint.write_text(
                json.dumps({
                    "paper_id": "W1",
                    "annual_citation_counts": [0, 1],
                }) + "\n",
                encoding="utf-8",
            )

            fake_history = SimpleNamespace(
                counts=(0, 0, 3),
                total_citations=3,
                valid_edges=3,
            )
            with patch.object(
                histories,
                "reconstruct_history_for_known_work",
                return_value=fake_history,
            ) as mocked:
                result = histories.reconstruct_inventory(
                    inventory,
                    checkpoint_path=checkpoint,
                    observation_end_year=1923,
                )

            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["new_records"], 1)
            self.assertEqual(result["skipped_completed"], 1)
            self.assertEqual(mocked.call_count, 1)
            rows = [
                json.loads(line)
                for line in checkpoint.read_text(
                    encoding="utf-8"
                ).splitlines()
            ]
            self.assertEqual(
                [row["paper_id"] for row in rows],
                ["W1", "W2"],
            )
            self.assertEqual(
                rows[1]["annual_citation_counts"],
                [0, 0, 3],
            )

    def test_bounded_batch_stops_after_requested_new_records(self):
        inventory = {
            "frames": [
                {
                    "case_id": "caseA",
                    "publication_year": 1935,
                    "primary_field_id": "31",
                    "works": [
                        {
                            "openalex_id": f"W{i}",
                            "publication_year": 1935,
                            "primary_field_id": "31",
                        }
                        for i in range(3)
                    ],
                }
            ]
        }
        fake_history = SimpleNamespace(
            counts=(0,),
            total_citations=0,
            valid_edges=0,
        )

        with tempfile.TemporaryDirectory() as tmp:
            checkpoint = Path(tmp) / "checkpoint.jsonl"
            with patch.object(
                histories,
                "reconstruct_history_for_known_work",
                return_value=fake_history,
            ) as mocked:
                result = histories.reconstruct_inventory(
                    inventory,
                    checkpoint_path=checkpoint,
                    max_new_records=2,
                )

            self.assertEqual(result["status"], "bounded_batch_complete")
            self.assertEqual(result["new_records"], 2)
            self.assertEqual(mocked.call_count, 2)


if __name__ == "__main__":
    unittest.main()
