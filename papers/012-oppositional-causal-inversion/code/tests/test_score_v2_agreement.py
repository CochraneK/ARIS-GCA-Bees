import csv,hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/"score_v2_agreement.py"
sys.path.insert(0,str(SCRIPT.parent))
import score_v2_agreement as m

class ScoreV2Tests(unittest.TestCase):
    def make_response(self,path,flip=False):
        fields=["record_id","title",*m.FIELDS,"coder_note"]
        with open(path,"w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
            for i in range(1,31):
                r={k:"" for k in fields};r["record_id"]=f"V2{i:02d}";r["title"]=f"T{i}"
                base="yes" if i%2 else "no"
                r["opposition_valid"]=("no" if base=="yes" else "yes") if flip else base
                r["oci_candidate"]="yes" if i%2 else "no"
                for x in m.REL_FIELDS+m.IDX_FIELDS+m.MECH_FIELDS+m.EV_FIELDS:r[x]="1" if i%2 else "0"
                r["evidence_strength"]="strong" if i%2 else "moderate"
                r["result_direction"]="supports_reversal" if i%2 else "null"
                r["normative_valence"]="beneficial" if i%2 else "harmful"
                w.writerow(r)

    def freeze(self,path,coder,bundle):
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        return {"classification":"V2_COMPLETED_CODER_FREEZE","coder":coder,"labels_frozen":True,
                "completed_response_sha256":sha,"input_bundle_sha256":bundle}

    def run_score(self,flip_b=False):
        td=tempfile.TemporaryDirectory();root=Path(td.name)
        a=root/"a.csv";b=root/"b.csv";self.make_response(a);self.make_response(b,flip=flip_b)
        bundle="abc123"
        af=root/"af.json";bf=root/"bf.json"
        af.write_text(json.dumps(self.freeze(a,"A2",bundle)),encoding="utf-8")
        bf.write_text(json.dumps(self.freeze(b,"B2",bundle)),encoding="utf-8")
        summary=root/"summary.json";dis=root/"d.csv"
        cp=subprocess.run([sys.executable,str(SCRIPT),"--a2",str(a),"--b2",str(b),
          "--a2-freeze",str(af),"--b2-freeze",str(bf),"--summary",str(summary),"--disagreements",str(dis)],
          capture_output=True,text=True)
        self.assertEqual(cp.returncode,0,cp.stderr)
        data=json.loads(summary.read_text(encoding="utf-8"))
        td.cleanup();return data

    def test_perfect_independent_files_pass(self):
        d=self.run_score(False)
        self.assertEqual(d["status"],"PASS_V2_RELIABILITY")
        self.assertTrue(d["full_165_screening_unlocked"])

    def test_primary_gate_failure_locks_full_screen(self):
        d=self.run_score(True)
        self.assertEqual(d["status"],"REVISE_V2_INSTRUMENT")
        self.assertFalse(d["gate"]["primary_pass"])
        self.assertFalse(d["full_165_screening_unlocked"])

if __name__=="__main__":unittest.main()
