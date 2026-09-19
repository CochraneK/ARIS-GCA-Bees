import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import confirmatory_feasibility_frame as f


class ConfirmatoryFeasibilityFrameTests(unittest.TestCase):
    def test_development_exposure_is_excluded_and_hash_selection_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            exclusions=Path(tmp)/"exclusions.json"
            exclusions.write_text(json.dumps({
                "entries":[{"doi":"10.1/exposed"}]
            }),encoding="utf-8")

            def fake_events(update_type,year,rows):
                return [
                    {
                        "target_doi":"10.1/exposed",
                        "notice_or_source_doi":"10.9/n0",
                        "update_type":update_type,
                        "outcome_date":f"{year}-01-01",
                        "assertion_source":"publisher",
                        "relation_label":update_type,
                        "source_work_title":"notice",
                        "source_work_date":f"{year}-01-01",
                    },
                    *[
                        {
                            "target_doi":f"10.2/{year}-{update_type}-{i}",
                            "notice_or_source_doi":f"10.9/{year}-{update_type}-{i}",
                            "update_type":update_type,
                            "outcome_date":f"{year}-02-{i+1:02d}",
                            "assertion_source":"publisher",
                            "relation_label":update_type,
                            "source_work_title":"notice",
                            "source_work_date":f"{year}-02-{i+1:02d}",
                        }
                        for i in range(5)
                    ],
                ]

            def fake_resolve(doi):
                return {
                    "target_title_current":"Ordinary article",
                    "target_title_has_status_marker":False,
                    "target_published":"2020-01-01",
                    "target_year":2020,
                    "target_journal":"Journal",
                    "target_type":"journal-article",
                    "crossref_has_abstract":True,
                    "crossref_has_fulltext_link":True,
                    "crossref_has_updated_by":True,
                    "reference_count":10,
                    "is_referenced_by_count":5,
                }

            with (
                patch.object(f,"update_events_for_year",side_effect=fake_events),
                patch.object(f,"resolve_target",side_effect=fake_resolve),
                patch.object(f.time,"sleep",return_value=None),
            ):
                a=f.build(exclusions,2020,2020,2,100)
                b=f.build(exclusions,2020,2020,2,100)

        self.assertEqual(a["candidate_count"],4)
        self.assertEqual(
            [x["target_doi"] for x in a["rows"]],
            [x["target_doi"] for x in b["rows"]],
        )
        self.assertNotIn("10.1/exposed",{x["target_doi"] for x in a["rows"]})
        self.assertTrue(all(x["detector_output_visible"] is False for x in a["rows"]))
        self.assertTrue(all(x["artifact_state"]=="UNASSESSED" for x in a["rows"]))
        self.assertEqual(a["state"],"FEASIBILITY_ONLY_NOT_CONFIRMATORY")
        self.assertIn("detector performance estimation",a["forbidden_uses"])

    def test_status_marker_detection(self):
        self.assertTrue(f.STATUS_RE.search("RETRACTED: example"))
        self.assertTrue(f.STATUS_RE.search("Expression of Concern: example"))
        self.assertFalse(f.STATUS_RE.search("Ordinary research article"))


if __name__=="__main__":
    unittest.main()
