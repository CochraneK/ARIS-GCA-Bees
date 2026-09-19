from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from make_calibration_reference_packets import build_packets  # noqa: E402
from merge_calibration_reference_reviews import (  # noqa: E402
    merge_reference_reviews,
)


def candidate(queue="P_REVIEW"):
    return {
        "candidate_id": "CALC_abc",
        "paper_id": "P1",
        "doi": "10.1/x",
        "title": "Title",
        "publication_year": "2020",
        "journal": "J",
        "publisher": "P",
        "candidate_queue": queue,
        "reasons": "SECRET_REASON",
        "candidate_basis": "SECRET_BASIS",
        "reference_binary_state": "",
    }


def review(
    reviewer,
    *,
    state="SEVERE_SUPPORTED",
    quality="A",
    materiality="MATERIAL",
):
    return {
        "candidate_id": "CALC_abc",
        "paper_id": "P1",
        "doi": "10.1/x",
        "reference_reviewer_id": reviewer,
        "model_name": "RefModel",
        "model_version_or_snapshot": "v1",
        "prompt_version": "CAL-REF-V1",
        "run_id": "run1",
        "reference_state": state,
        "anchor_quality": quality,
        "materiality_assessment": materiality,
        "evidence_type": "FORMAL_FINDING",
        "evidence_source": f"https://example.org/{reviewer}",
        "evidence_locator": "finding paragraph 1",
        "evidence_access": "FULL_PRIMARY",
        "brief_evidence_rationale": "Primary evidence supports classification.",
        "abstain_reason": "",
    }


class CalibrationReferenceTests(unittest.TestCase):
    def test_packets_strip_candidate_queue_and_reasons(self):
        packets = build_packets([candidate()])
        self.assertEqual(set(packets), {"REF_A", "REF_B"})
        for reviewer, rows in packets.items():
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertNotIn("candidate_queue", row)
            self.assertNotIn("reasons", row)
            self.assertNotIn("candidate_basis", row)
            self.assertNotIn("reference_binary_state", row)
            self.assertEqual(row["reference_reviewer_id"], reviewer)
            self.assertEqual(row["prompt_version"], "CAL-REF-V1")

    def test_unresolved_queue_is_not_packetized(self):
        packets = build_packets([candidate(queue="U_REVIEW")])
        self.assertEqual(packets["REF_A"], [])
        self.assertEqual(packets["REF_B"], [])

    def test_positive_A_consensus_becomes_primary_anchor(self):
        anchors, summary = merge_reference_reviews(
            [review("REF_A")],
            [review("REF_B")],
        )
        self.assertEqual(len(anchors), 1)
        self.assertEqual(anchors[0]["anchor_family"], "P+")
        self.assertEqual(anchors[0]["reference_binary_state"], 1)
        self.assertEqual(anchors[0]["anchor_quality"], "A")
        self.assertEqual(summary["primary_calibration_A_only"], 1)

    def test_negative_consensus_requires_scientifically_unaffected(self):
        a = review(
            "REF_A",
            state="NON_SEVERE_SUPPORTED",
            materiality="SCIENTIFICALLY_UNAFFECTED",
        )
        b = review(
            "REF_B",
            state="NON_SEVERE_SUPPORTED",
            materiality="SCIENTIFICALLY_UNAFFECTED",
        )
        anchors, _ = merge_reference_reviews([a], [b])
        self.assertEqual(len(anchors), 1)
        self.assertEqual(anchors[0]["anchor_family"], "N+")
        self.assertEqual(anchors[0]["reference_binary_state"], 0)

    def test_state_disagreement_is_excluded(self):
        a = review("REF_A")
        b = review(
            "REF_B",
            state="NON_SEVERE_SUPPORTED",
            materiality="SCIENTIFICALLY_UNAFFECTED",
        )
        anchors, summary = merge_reference_reviews([a], [b])
        self.assertEqual(anchors, [])
        self.assertEqual(summary["status_counts"]["STATE_DISAGREEMENT"], 1)

    def test_C_quality_consensus_is_descriptive_only(self):
        a = review("REF_A", quality="C")
        b = review("REF_B", quality="C")
        anchors, summary = merge_reference_reviews([a], [b])
        self.assertEqual(anchors, [])
        self.assertEqual(
            summary["status_counts"]["CONSENSUS_C_DESCRIPTIVE_ONLY"], 1
        )

    def test_same_reference_reviewer_id_fails(self):
        with self.assertRaises(ValueError):
            merge_reference_reviews(
                [review("REF_A")],
                [review("REF_A")],
            )

    def test_article_adjudicator_cannot_be_reference_reviewer(self):
        with self.assertRaises(ValueError):
            merge_reference_reviews(
                [review("AI_A")],
                [review("REF_B")],
            )


if __name__ == "__main__":
    unittest.main()
