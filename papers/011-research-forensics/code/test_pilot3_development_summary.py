#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("summary",HERE/"pilot3_development_summary.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class T(unittest.TestCase):
    def test_summary_boundaries(self):
        x=m.build()
        self.assertEqual(x["true_positive_evaluations"]["count"],6)
        self.assertEqual(x["true_positive_evaluations"]["unique_target_papers"],5)
        self.assertEqual(x["true_positive_evaluations"]["family_counts"],{"F5":1,"F3":3,"F8":1,"F1":1})
        self.assertEqual(len(x["abstention_example"]["abstained_checks"]),5)
        self.assertEqual(x["negative_side_development_comparators"]["count"],4)
        self.assertEqual(x["conservative_non_escalation"]["flag_count"],0)
        self.assertFalse(x["confirmatory_performance_estimate"])
        self.assertFalse(x["misconduct_inference"])
    def test_markdown_boundary(self):
        t=m.markdown(m.build())
        self.assertIn("No precision, specificity, or false-positive-rate estimate.",t)
        self.assertIn("They are not clean controls",t)
        self.assertIn("No author-level intent, guilt, or misconduct inference.",t)
if __name__=="__main__": unittest.main()
