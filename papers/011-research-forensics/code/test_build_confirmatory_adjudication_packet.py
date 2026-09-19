#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m",HERE/"build_confirmatory_adjudication_packet.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class T(unittest.TestCase):
    def frame(self):
        base={
            "state":"FEASIBILITY_ONLY_NOT_CONFIRMATORY",
            "candidate_count":2,
            "rows":[],
        }
        for i in (1,2):
            base["rows"].append({
                "feasibility_id":f"F{i:03d}",
                "calendar_stratum":2020,
                "target_doi":f"10.1/{i}",
                "notice_or_source_doi":f"10.2/{i}",
                "update_type":"correction",
                "outcome_date":"2020-01-01",
                "assertion_source":"publisher",
                "relation_label":"Correction",
                "source_work_title":"Correction",
                "source_work_date":"2020-01-01",
                "target_title_current":"Paper",
                "target_title_has_status_marker":False,
                "target_published":"2019-01-01",
                "target_year":2019,
                "target_journal":"J",
                "target_type":"journal-article",
                "detector_output_visible":False,
                "review_priority":"HIGH",
                "artifact_state":"UNASSESSED",
            })
        return base

    def test_projection_excludes_scoring_fields(self):
        rows,meta=m.build(self.frame())
        self.assertEqual(len(rows),2)
        self.assertEqual(meta["state"],"MANAGER_ONLY_UNADJUDICATED")
        self.assertFalse(meta["selection_used_detector_output"])
        self.assertTrue(all(r["adjudication_state"]=="UNASSESSED" for r in rows))
        for forbidden in m.FORBIDDEN_SOURCE_FIELDS:
            self.assertNotIn(forbidden,rows[0])
        self.assertNotIn("detector_output_visible",rows[0])

    def test_non_blind_input_fails(self):
        f=self.frame()
        f["rows"][0]["detector_output_visible"]=True
        with self.assertRaises(ValueError):
            m.build(f)

if __name__=="__main__":
    unittest.main()
