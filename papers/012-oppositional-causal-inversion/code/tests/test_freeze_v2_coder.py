import csv,importlib.util,tempfile,unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"freeze_v2_coder.py"
spec=importlib.util.spec_from_file_location("freeze_v2",P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class FreezeV2Tests(unittest.TestCase):
    def make_file(self,path,invalid=False):
        fields=["record_id","title",*m.SCORING_FIELDS,"coder_note"]
        with open(path,"w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
            for i in range(1,31):
                r={k:"" for k in fields}
                r["record_id"]=f"V2{i:02d}";r["title"]=f"T{i}"
                r["opposition_valid"]="yes" if i%2 else "no"
                r["oci_candidate"]="yes" if i%3 else "uncertain"
                for x in m.REL_FIELDS+m.IDX_FIELDS+m.MECH_FIELDS+m.EV_FIELDS:r[x]="1" if i%2 else "0"
                r["evidence_strength"]="moderate"
                r["result_direction"]="supports_reversal"
                r["normative_valence"]="mixed"
                if invalid and i==1:r["opposition_valid"]="maybe"
                w.writerow(r)

    def test_complete_controlled_file_passes(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"a.csv";self.make_file(p)
            v=m.validate(p)
            self.assertTrue(v["complete"]);self.assertEqual(v["row_count"],30)

    def test_invalid_token_fails(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"a.csv";self.make_file(p,invalid=True)
            v=m.validate(p)
            self.assertFalse(v["complete"])
            self.assertTrue(any("invalid token" in e for e in v["errors"]))

if __name__=="__main__":unittest.main()
