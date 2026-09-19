#!/usr/bin/env python3
import importlib.util,json,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m",HERE/"build_development_exclusion_registry.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class T(unittest.TestCase):
 def test_structured_dois_are_collected(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); (root/"data"/"seed").mkdir(parents=True); (root/"data"/"pilot").mkdir(); (root/"data"/"results").mkdir()
   (root/"data"/"seed"/"a.json").write_text(json.dumps({"target_doi":"https://doi.org/10.1234/ABC","note":"10.9999/not-a-field"}))
   (root/"data"/"pilot"/"b.csv").write_text("candidate_doi,x\n10.5678/DEF,1\n")
   (root/"data"/"results"/"confirmatory_feasibility_frame_v0.json").write_text(
       json.dumps({"rows":[{"target_doi":"10.7777/FEASIBILITY"}]})
   )
   rows=m.collect(root)
   self.assertEqual(set(rows),{"10.1234/abc","10.5678/def","10.7777/feasibility"})
if __name__=="__main__": unittest.main()
