#!/usr/bin/env python3
import csv,importlib.util,json,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m",HERE/"confirmatory_preflight.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def contract():
 return {
  "protocol_version":"x","state":"PRE_FREEZE",
  "freeze_gates":{"a":True},
  "confirmatory_scoring_allowed":True,
  "claim_boundary":"x",
  "split_contract":{"required_columns":["target_doi","split"],"cluster_fields":["known_cluster_id","text_cluster_id","image_cluster_id"]},
  "temporal_contract":{"development_cutoff":"2025-01-01","temporal_test_label":"temporal_test","outcome_date_field":"outcome_date"},
  "track_a_leakage_contract":{"manifest_allowlist":["paper_id","target_title_safe","split"],"forbidden_field_fragments":["notice","reason","label"],"forbidden_value_tokens":["RETRACTED"]},
 }

class T(unittest.TestCase):
 def write(self,path,rows):
  fields=list(rows[0]); f=path.open("w",newline=""); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows); f.close()
 def test_clean_grouped_temporal_manifest_can_pass(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"m.csv"; self.write(p,[
    {"target_doi":"10.1/a","split":"test","known_cluster_id":"k1","text_cluster_id":"","image_cluster_id":"","outcome_date":"2024-01-01"},
    {"target_doi":"10.1/b","split":"temporal_test","known_cluster_id":"k2","text_cluster_id":"","image_cluster_id":"","outcome_date":"2025-02-01"}])
   out=m.inspect(contract(),{"entries":[{"doi":"10.1/dev"}]},p,None)
   self.assertTrue(out["ready_for_confirmatory_scoring"]); self.assertEqual(out["blockers"],[])
 def test_dev_reuse_and_cluster_crossing_are_blocked(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"m.csv"; self.write(p,[
    {"target_doi":"10.1/dev","split":"test","known_cluster_id":"same","text_cluster_id":"","image_cluster_id":"","outcome_date":"2024-01-01"},
    {"target_doi":"10.1/x","split":"validation","known_cluster_id":"same","text_cluster_id":"","image_cluster_id":"","outcome_date":"2024-01-01"}])
   out=m.inspect(contract(),{"entries":[{"doi":"10.1/dev"}]},p,None)
   self.assertTrue(any(x.startswith("development_doi_reused:") for x in out["blockers"]))
   self.assertTrue(any(x.startswith("cluster_crosses_splits:") for x in out["blockers"]))
 def test_track_a_label_field_and_value_are_blocked(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); p=root/"m.csv"; self.write(p,[{"target_doi":"10.1/x","split":"test","known_cluster_id":"","text_cluster_id":"","image_cluster_id":"","outcome_date":"2024-01-01"}])
   ta=root/"ta.csv"; self.write(ta,[{"paper_id":"p","target_title_safe":"RETRACTED paper","split":"test","notice_type":"x"}])
   out=m.inspect(contract(),{"entries":[]},p,ta)
   self.assertTrue(any(x.startswith("track_a_fields_not_allowlisted:") for x in out["blockers"]))
   self.assertTrue(any(x.startswith("track_a_forbidden_value:") for x in out["blockers"]))
if __name__=="__main__": unittest.main()
