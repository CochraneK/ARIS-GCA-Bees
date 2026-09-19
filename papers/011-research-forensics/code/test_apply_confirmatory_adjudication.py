#!/usr/bin/env python3
import importlib.util,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m",HERE/"apply_confirmatory_adjudication.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class T(unittest.TestCase):
    def rows(self):
        return [{"feasibility_id":"F001","target_doi":"10/a","issue_family_codes":"","ground_truth_tier":"","required_artifact_roles":"","content_detectability":"","adjudication_state":"UNASSESSED","adjudication_notes":""}]
    def test_only_editable_fields_change(self):
        out,a=m.merge(self.rows(),[("p",[{"feasibility_id":"F001","issue_family_codes":"other_unclear","adjudication_state":"CODED_PENDING_REVIEW"}])])
        self.assertEqual(out[0]["target_doi"],"10/a")
        self.assertEqual(out[0]["issue_family_codes"],"other_unclear")
        self.assertEqual(len(a),1)
    def test_source_edit_rejected(self):
        with self.assertRaises(ValueError):
            m.merge(self.rows(),[("p",[{"feasibility_id":"F001","target_doi":"evil"}])])

if __name__=="__main__":
    unittest.main()
