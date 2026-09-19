#!/usr/bin/env python3
import importlib.util,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m",HERE/"validate_confirmatory_adjudication.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

PROTOCOL={
 "issue_family_vocab":{"statistical_reporting":"x","other_unclear":"x"},
 "ground_truth_tiers":{"GT-A":"x","GT-B":"x"},
 "artifact_role_vocab":{"table":"x","none_content_detectable":"x"},
 "content_detectability":{"CONTENT_ASSESSABLE":"x","PROCESS_ONLY":"x","MIXED":"x","UNCLEAR":"x"},
 "first_pass_states":["UNASSESSED","CODED_PENDING_REVIEW","NEEDS_SOURCE","EXCLUDE_DUPLICATE_EVENT"],
}

class T(unittest.TestCase):
 def base(self):
  return {"feasibility_id":"F001","issue_family_codes":"statistical_reporting","ground_truth_tier":"GT-B","required_artifact_roles":"table","content_detectability":"CONTENT_ASSESSABLE","adjudication_state":"CODED_PENDING_REVIEW"}
 def test_valid_coded_row(self):
  x=m.validate([self.base()],PROTOCOL)
  self.assertTrue(x["structure_valid"]); self.assertEqual(x["error_count"],0)
 def test_process_only_requires_none_role(self):
  r=self.base(); r["content_detectability"]="PROCESS_ONLY"
  x=m.validate([r],PROTOCOL)
  self.assertTrue(any(e.startswith("process_only_role_mismatch") for e in x["errors"]))
 def test_unassessed_allowed_until_complete_gate(self):
  r=self.base(); r.update({"issue_family_codes":"","ground_truth_tier":"","required_artifact_roles":"","content_detectability":"","adjudication_state":"UNASSESSED"})
  self.assertEqual(m.validate([r],PROTOCOL)["error_count"],0)
  self.assertGreater(m.validate([r],PROTOCOL,True)["error_count"],0)

if __name__=="__main__": unittest.main()
