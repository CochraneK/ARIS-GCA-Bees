import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pilot3_comparator_discovery as d


class ComparatorDiscoveryTests(unittest.TestCase):
    def test_score_candidate_excludes_status_markers_and_registry(self):
        target_date = d.dt.date(2021, 10, 22)
        base = {
            "DOI": "10.1371/journal.pone.0999999",
            "title": ["Ordinary research article"],
            "type": "journal-article",
            "published": {"date-parts": [[2021, 10, 20]]},
            "reference-count": 10,
            "is-referenced-by-count": 5,
        }
        row = d.score_candidate(
            base,
            target_date=target_date,
            excluded=set(),
        )
        self.assertEqual(row["screen_state"], "PROVISIONAL_CROSSREF_NEGATIVE")
        self.assertEqual(row["date_distance_days"], 2)

        bad = dict(base)
        bad["title"] = ["Correction: Ordinary research article"]
        self.assertIsNone(
            d.score_candidate(
                bad,
                target_date=target_date,
                excluded=set(),
            )
        )

        self.assertIsNone(
            d.score_candidate(
                base,
                target_date=target_date,
                excluded={"10.1371/journal.pone.0999999"},
            )
        )

    def test_registry_excludes_target_and_correction_dois(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                w = csv.DictWriter(
                    handle,
                    fieldnames=["target_doi", "correction_doi"],
                )
                w.writeheader()
                w.writerow({
                    "target_doi": "https://doi.org/10.1/A",
                    "correction_doi": "10.1/B",
                })
            got = d.known_registry_dois(path)
        self.assertEqual(got, {"10.1/a", "10.1/b"})

    def test_discovery_never_matches_on_detector_outputs(self):
        fake_items = [
            {
                "DOI": f"10.1371/journal.pone.{i:07d}",
                "title": [f"Candidate {i}"],
                "type": "journal-article",
                "published": {"date-parts": [[2021, 10, 20 + i]]},
                "reference-count": i,
                "is-referenced-by-count": i * 2,
            }
            for i in range(1, 9)
        ]

        with (
            patch.object(d, "known_registry_dois", return_value=set()),
            patch.object(d, "query_window", return_value=fake_items),
        ):
            result = d.discover(per_target=1, window_days=45)

        self.assertEqual(result["candidate_count"], 4)
        self.assertIn("detector output", result["explicit_nonmatching_variables"])
        self.assertTrue(result["secondary_screen_required"])
        self.assertTrue(
            all(
                row["screen_state"] == "PROVISIONAL_CROSSREF_NEGATIVE"
                for row in result["matches"]
            )
        )


if __name__ == "__main__":
    unittest.main()
