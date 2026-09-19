import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MOD_PATH=Path(__file__).resolve().parents[1]/"materialize_v2_blind_packet.py"
spec=importlib.util.spec_from_file_location("m",MOD_PATH)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class BlindPacketTests(unittest.TestCase):
    def test_openalex_abstract_reconstruction(self):
        inv={"world":[1],"hello":[0],"again":[2]}
        self.assertEqual(m.reconstruct_openalex_abstract(inv),"hello world again")

    def test_word_cap(self):
        text=" ".join(f"w{i}" for i in range(200))
        out,truncated,n=m.cap_words(text,180)
        self.assertTrue(truncated); self.assertEqual(n,180); self.assertEqual(len(out.split()),180)

    def test_blind_keys_reject_retrieval_metadata(self):
        with self.assertRaises(AssertionError):
            m.assert_blind_record({"sample_id":"V201","title":"x","stratum":"hidden"})

    def test_blind_keys_reject_prior_labels(self):
        with self.assertRaises(AssertionError):
            m.assert_blind_record({"sample_id":"V201","title":"x","oci_candidate":"yes"})

    def test_canonical_jsonl_is_order_stable(self):
        a={"sample_id":"V202","title":"b"}
        b={"sample_id":"V201","title":"a"}
        x=m.canonical_jsonl([a,b])
        y=m.canonical_jsonl([b,a])
        self.assertEqual(x,y)
        self.assertEqual(m.sha256_bytes(x),m.sha256_bytes(y))

    def test_response_forms_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as td:
            records=[{"sample_id":"V201","title":"A"},{"sample_id":"V202","title":"B"}]
            for id_field in ("sample_id","record_id"):
                p=Path(td)/f"{id_field}.csv"
                p.write_text(f"{id_field},title,opposition_valid,coder_note\\n",encoding="utf-8")
                a=m.build_response_csv(p,records)
                b=m.build_response_csv(p,list(reversed(records)))
                self.assertEqual(a,b)
                self.assertIn(b"V201,A",a)

if __name__=="__main__":
    unittest.main()
