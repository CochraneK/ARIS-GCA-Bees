#!/usr/bin/env python3
import importlib.util,unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m",HERE/"confirmatory_notice_excerpt.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class T(unittest.TestCase):
 def test_cap(self):
  x,tr,total=m.cap(" ".join(str(i) for i in range(100)))
  self.assertEqual(len(x.split()),80); self.assertTrue(tr); self.assertEqual(total,100)
 def test_build_never_track_a(self):
  e={"rows":[{"feasibility_id":"F1","target_doi":"10/t","notice_or_source_doi":"10/n","update_type":"correction","manager_evidence_route":"PMC_JATS","pmc":{"pmc_id":"PMC1"}}]}
  with patch.object(m,"pmc_body",return_value="concrete correction text"),patch.object(m.time,"sleep",return_value=None):
   x=m.build(e)
  self.assertEqual(x["rows_with_nonempty_excerpt"],1)
  self.assertTrue(x["rows"][0]["manager_only"])
  self.assertFalse(x["rows"][0]["track_a_input_allowed"])

if __name__=="__main__": unittest.main()
