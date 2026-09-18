import csv
import importlib.util
import pathlib
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "score_coder_agreement.py"
spec = importlib.util.spec_from_file_location("score_coder_agreement", MODULE_PATH)
m = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(m)


class AgreementTests(unittest.TestCase):
    def test_perfect_agreement(self):
        pairs=[("yes","yes"),("no","no"),("yes","yes")]
        self.assertEqual(m.raw_agreement(pairs), 1.0)
        self.assertEqual(m.cohen_kappa(pairs), 1.0)
        self.assertEqual(m.krippendorff_alpha_nominal(pairs), 1.0)

    def test_nonperfect_agreement(self):
        pairs=[("yes","yes"),("yes","no"),("no","no"),("no","yes")]
        self.assertAlmostEqual(m.raw_agreement(pairs), 0.5)
        self.assertAlmostEqual(m.cohen_kappa(pairs), 0.0)

    def test_incomplete_b_blocks(self):
        b={"P01":{"opposition_valid":"yes","oci_candidate":"","primary_mechanism":"feedback"}}
        c=m.completeness(b, {"P01","P02"})
        self.assertFalse(c["complete"])
        self.assertIn("P02", c["missing_records"])
        self.assertIn("oci_candidate", c["records_missing_core_fields"]["P01"])

    def test_disagreement_packet_only_nonmatching_nonblank(self):
        a={"P01":{"title":"T","opposition_valid":"yes","oci_candidate":"yes","primary_mechanism":"feedback"}}
        b={"P01":{"title":"T","opposition_valid":"no","oci_candidate":"","primary_mechanism":"feedback"}}
        rows=m.make_disagreements(a,b)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["field"],"opposition_valid")


if __name__ == "__main__":
    unittest.main()
