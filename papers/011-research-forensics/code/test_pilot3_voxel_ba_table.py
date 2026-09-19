#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("voxel",HERE/"pilot3_voxel_ba_table.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class VoxelBATests(unittest.TestCase):
    def test_preserved_original_fixture_flags_only_malformed_token(self):
        report,evaluation=m.execute(m.DEFAULT_FIXTURE)
        self.assertEqual(evaluation["status"],"PASS")
        self.assertEqual(evaluation["finding_count"],6)
        self.assertEqual(evaluation["pass_count"],5)
        self.assertEqual(evaluation["flag_count"],1)
        self.assertTrue(evaluation["checks"]["malformed_original_token_flagged"])
        self.assertFalse(evaluation["detector_visible_correction_metadata"])
        self.assertFalse(evaluation["manager_only_later_outcome"]["used_by_detector"])
        self.assertIn("malformed BA token only",evaluation["development_true_positive_scope"])
        flags=[x for x in report["findings"] if x["status"]=="FLAG"]
        self.assertEqual(len(flags),1)
        self.assertEqual(flags[0]["evidence"]["normalized_token"],"9月8日")
        self.assertFalse(flags[0]["misconduct_inference"])

if __name__=="__main__": unittest.main()
