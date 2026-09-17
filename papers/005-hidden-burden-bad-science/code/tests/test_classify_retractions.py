from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from classify_retractions import classify, split_reasons  # noqa: E402


class RetractionClassifierTests(unittest.TestCase):
    def test_split_semicolon_reasons(self):
        self.assertEqual(
            split_reasons("Falsification/Fabrication of Data; Paper Mill"),
            ["Falsification/Fabrication of Data", "Paper Mill"],
        )

    def test_fabrication_is_narrow_scientific_integrity_failure(self):
        flags = classify(["Falsification/Fabrication of Data"])
        self.assertEqual(flags["e1s_narrow_auto"], 1)
        self.assertEqual(flags["e1m_strong_auto"], 1)
        self.assertEqual(flags["e3_error_signal"], 0)

    def test_plagiarism_is_misconduct_not_automatically_false_science(self):
        flags = classify(["Plagiarism of Text"])
        self.assertEqual(flags["e1m_strong_auto"], 1)
        self.assertEqual(flags["e1s_narrow_auto"], 0)

    def test_honest_error_is_not_misconduct(self):
        flags = classify(["Error in Analyses"])
        self.assertEqual(flags["e3_error_signal"], 1)
        self.assertEqual(flags["e1s_narrow_auto"], 0)
        self.assertEqual(flags["e1m_strong_auto"], 0)

    def test_ambiguous_unreliable_data_requires_manual_review(self):
        flags = classify(["Unreliable Data"])
        self.assertEqual(flags["manual_scientific_review"], 1)
        self.assertEqual(flags["manual_review_required"], 1)
        self.assertEqual(flags["e1s_narrow_auto"], 0)

    def test_investigation_only_does_not_become_misconduct(self):
        flags = classify(["Investigation by ORI"])
        self.assertEqual(flags["context_only_reasons"], 1)
        self.assertEqual(flags["e1m_strong_auto"], 0)
        self.assertEqual(flags["manual_review_required"], 1)

    def test_paper_mill_is_process_signal_but_not_auto_e1s(self):
        flags = classify(["Paper Mill"])
        self.assertEqual(flags["paper_mill_signal"], 1)
        self.assertEqual(flags["e1p_strong_auto"], 1)
        self.assertEqual(flags["e1s_narrow_auto"], 0)
        self.assertEqual(flags["manual_review_required"], 1)


if __name__ == "__main__":
    unittest.main()
