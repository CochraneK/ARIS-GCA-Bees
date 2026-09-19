from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from build_calibration_candidates import (  # noqa: E402
    candidate_queue,
    collapse_rows,
)
from classify_retractions import normalize_reason


def row(
    doi: str,
    reason: str,
    *,
    nature: str = "Retraction",
    e1s: int = 0,
    e3: int = 0,
    manual_scientific: int = 0,
    paper_mill: int = 0,
):
    return {
        "Record ID": "1",
        "Title": "Example",
        "Journal": "J",
        "Publisher": "P",
        "OriginalPaperDOI": doi,
        "OriginalPaperDate": "01/01/2020",
        "RetractionNature": nature,
        "Reason": reason,
        "e1s_narrow_auto": str(e1s),
        "paper_mill_signal": str(paper_mill),
        "e3_error_signal": str(e3),
        "manual_scientific_review": str(manual_scientific),
        "manual_process_review": "0",
        "context_only_reasons": "0",
    }


class CalibrationCandidateTests(unittest.TestCase):
    def test_fabrication_plus_official_finding_is_high_review_not_truth(self):
        rows = [
            row(
                "10.1/a",
                "Falsification/Fabrication of Data; "
                "Misconduct - Official Investigation(s) and/or Finding(s)",
                e1s=1,
            )
        ]
        out, summary = collapse_rows(rows)
        self.assertEqual(out[0]["candidate_queue"], "P_HIGH_REVIEW")
        self.assertEqual(out[0]["reference_binary_state"], "")
        self.assertEqual(out[0]["anchor_quality"], "")
        self.assertEqual(summary["reference_truth_labels_assigned"], 0)

    def test_fabrication_only_is_positive_review(self):
        reasons = {normalize_reason("Falsification/Fabrication of Data")}
        queue, _ = candidate_queue(
            reasons,
            {"Retraction"},
            {
                "e1s_narrow_auto": 1,
                "e3_error_signal": 0,
                "manual_scientific_review": 0,
                "paper_mill_signal": 0,
            },
        )
        self.assertEqual(queue, "P_REVIEW")

    def test_process_only_is_negative_review_candidate_not_truth(self):
        rows = [
            row(
                "10.1/b",
                "Plagiarism of Text; Investigation by Journal/Publisher",
            )
        ]
        out, _ = collapse_rows(rows)
        self.assertEqual(out[0]["candidate_queue"], "N_PROCESS_REVIEW")
        self.assertEqual(out[0]["reference_binary_state"], "")
        self.assertEqual(out[0]["requires_primary_evidence_review"], 1)

    def test_process_plus_unreliable_results_is_not_negative_candidate(self):
        rows = [
            row(
                "10.1/c",
                "Plagiarism of Text; Unreliable Results and/or Conclusions",
                manual_scientific=1,
            )
        ]
        out, _ = collapse_rows(rows)
        self.assertEqual(out[0]["candidate_queue"], "U_REVIEW")

    def test_no_doi_is_not_emitted_as_row_level_candidate(self):
        out, summary = collapse_rows(
            [row("", "Falsification/Fabrication of Data", e1s=1)]
        )
        self.assertEqual(out, [])
        self.assertEqual(summary["event_rows_without_resolvable_doi"], 1)

    def test_public_release_flag_is_false(self):
        out, summary = collapse_rows(
            [row("10.1/d", "Plagiarism of Text")]
        )
        self.assertFalse(summary["public_row_level_release_allowed"])
        self.assertEqual(out[0]["public_row_level_release_allowed"], 0)


if __name__ == "__main__":
    unittest.main()
