#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m",HERE/"confirmatory_notice_evidence.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class T(unittest.TestCase):
    def test_acquire_prefers_pmc_and_never_uses_detector_output(self):
        rows=[{
            "feasibility_id":"F001","target_doi":"10.1/t",
            "notice_or_source_doi":"10.1/n","update_type":"correction",
            "outcome_date":"2020-01-01"
        }]
        with (
            patch.object(m,"crossref_notice",return_value={"title":"Correction","url":"https://doi.org/10.1/n"}),
            patch.object(m,"pubmed_ids",return_value=["123"]),
            patch.object(m,"pubmed_record",return_value={"pmid":"123","pmc_id":"PMC1"}),
            patch.object(m,"pmc_probe",return_value={"pmc_id":"PMC1","jats_available":True,"jats_sha256":"x","body_char_count":50}),
            patch.object(m.time,"sleep",return_value=None),
        ):
            x=m.acquire(rows)
        self.assertEqual(x["row_count"],1)
        self.assertEqual(x["route_counts"],{"PMC_JATS":1})
        self.assertFalse(x["detector_output_used"])
        self.assertFalse(x["full_notice_text_committed"])
        self.assertEqual(x["rows"][0]["issue_adjudication_state"],"UNASSESSED")

    def test_network_failure_is_recorded_not_dropped(self):
        rows=[{
            "feasibility_id":"F001","target_doi":"10.1/t",
            "notice_or_source_doi":"10.1/n","update_type":"retraction",
            "outcome_date":"2020-01-01"
        }]
        with (
            patch.object(m,"crossref_notice",side_effect=RuntimeError("x")),
            patch.object(m,"pubmed_ids",side_effect=RuntimeError("y")),
            patch.object(m.time,"sleep",return_value=None),
        ):
            x=m.acquire(rows)
        self.assertEqual(x["row_count"],1)
        self.assertEqual(x["rows_with_any_acquisition_error"],1)
        self.assertEqual(x["rows"][0]["manager_evidence_route"],"PUBLISHER_DOI")

if __name__=="__main__":
    unittest.main()
