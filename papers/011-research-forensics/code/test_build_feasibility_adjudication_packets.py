import unittest
import build_feasibility_adjudication_packets as b


class PacketBuilderTests(unittest.TestCase):
    def test_manager_only_separation(self):
        frame={
            "state":"FEASIBILITY_ONLY_NOT_CONFIRMATORY",
            "rows":[{
                "feasibility_id":"F001",
                "target_doi":"10.1/a",
                "notice_or_source_doi":"10.1/n",
                "update_type":"correction",
                "outcome_date":"2025-01-02",
                "assertion_source":"publisher",
                "relation_label":"correction",
                "source_work_title":"Correction notice",
                "target_title_current":"Article",
                "target_title_has_status_marker":False,
                "target_published":"2024-01-01",
                "crossref_has_fulltext_link":True,
            }]
        }
        manager,acq,summary=b.build(frame)
        self.assertEqual(len(manager),1)
        self.assertEqual(manager[0]["issue_family"],"UNADJUDICATED")
        self.assertEqual(manager[0]["required_artifact_role"],"UNADJUDICATED")
        self.assertFalse(manager[0]["detector_visible"])
        self.assertTrue(manager[0]["manager_only"])
        self.assertEqual(acq[0]["artifact_state"],"UNASSESSED")
        self.assertEqual(acq[0]["pre_outcome_cutoff_exclusive"],"2025-01-02")
        self.assertFalse(acq[0]["detector_visible"])
        self.assertEqual(summary["detector_visible_records"],0)

    def test_unassessed_is_not_negative(self):
        frame={
            "state":"FEASIBILITY_ONLY_NOT_CONFIRMATORY",
            "rows":[{
                "feasibility_id":"F001",
                "target_doi":"10.1/a",
                "update_type":"retraction",
                "outcome_date":"2025-01-02",
                "target_title_has_status_marker":True,
                "crossref_has_fulltext_link":False,
            }]
        }
        manager,acq,summary=b.build(frame)
        self.assertEqual(manager[0]["content_detectability"],"UNADJUDICATED")
        self.assertEqual(acq[0]["artifact_state"],"UNASSESSED")
        self.assertEqual(summary["artifact_state_assessed"],0)

    def test_duplicate_ids_fail_closed(self):
        row={
            "feasibility_id":"F001",
            "target_doi":"10.1/a",
            "update_type":"correction",
        }
        with self.assertRaises(ValueError):
            b.build({"state":"FEASIBILITY_ONLY_NOT_CONFIRMATORY","rows":[row,row]})


if __name__=="__main__":
    unittest.main()
