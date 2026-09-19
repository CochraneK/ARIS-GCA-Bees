from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from collect_ai_batch_outputs import (  # noqa: E402
    checksum_rows,
    collect,
)


def write_csv(path: Path, rows):
    fields = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def article_row(aid: str, paper: str, person: str):
    return {
        "assignment_id": aid,
        "paper_id": paper,
        "adjudicator_id": person,
        "model_name": "Model",
        "model_version_or_snapshot": "v1",
        "prompt_version": "AI-ADJ-V1",
        "run_id": "run1",
        "scientific_state": "NO_MATERIAL_PROBLEM_FOUND",
        "materiality": "IMMATERIAL",
        "misconduct_evidence": "NO_EVIDENCE_OF_MISCONDUCT",
        "publication_process_state": "",
        "review_confidence": "HIGH",
        "fulltext_seen": "YES",
        "notice_seen": "NO",
        "formal_finding_seen": "NO",
        "evidence_locator": "abstract",
        "brief_evidence_rationale": "No material problem established.",
        "abstain_reason": "",
    }


def citation_row(aid: str, edge: str, person: str):
    return {
        "assignment_id": aid,
        "edge_id": edge,
        "adjudicator_id": person,
        "model_name": "Model",
        "model_version_or_snapshot": "v1",
        "prompt_version": "CIT-EDGE-V1",
        "run_id": "run1",
        "semantic_class": "BACKGROUND_MENTION",
        "component_implicated": "UNKNOWN",
        "material_to_downstream_claim": "NO",
        "source_retraction_known_in_text": "NO",
        "context_access": "FULLTEXT",
        "review_confidence": "HIGH",
        "evidence_locator": "Introduction",
        "brief_evidence_rationale": "Background-only citation.",
        "abstain_reason": "",
    }


class CollectAIBatchOutputsTests(unittest.TestCase):
    def test_article_batches_collect_and_validate_checksum(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rows = [
                article_row("A2", "P2", "AI_A"),
                article_row("A1", "P1", "AI_A"),
            ]
            write_csv(root / "AI_A_batch_001_output.csv", rows)
            manifest = {
                "classification": "AI_ADJUDICATION_BATCH_MANIFEST_NO_LABELS",
                "assignments_total": 2,
                "reviewers": {"AI_A": 2},
                "batches": [{
                    "reviewer_id": "AI_A",
                    "batch_number": 1,
                    "filename": "AI_A_batch_001.csv",
                    "assignments": 2,
                    "assignment_checksum_sha256": checksum_rows(
                        rows, ("assignment_id", "paper_id")
                    ),
                }],
            }
            collected, summary = collect(
                manifest, root, mode="article"
            )
            self.assertEqual(len(collected["AI_A"]), 2)
            self.assertEqual(summary["validated_batches"], 1)
            self.assertEqual(summary["validated_unique_assignments"], 2)

    def test_citation_batches_collect(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rows = [
                citation_row("C1", "E1", "CIT_AI_A"),
                citation_row("C2", "E2", "CIT_AI_A"),
            ]
            write_csv(root / "CIT_AI_A_batch_001_output.csv", rows)
            manifest = {
                "classification": "CITATION_EDGE_AI_BATCH_MANIFEST_NO_LABELS",
                "assignments_total": 2,
                "adjudicators": {"CIT_AI_A": 2},
                "batches": [{
                    "adjudicator_id": "CIT_AI_A",
                    "batch_number": 1,
                    "filename": "CIT_AI_A_batch_001.csv",
                    "assignments": 2,
                    "assignment_checksum_sha256": checksum_rows(
                        rows, ("assignment_id", "edge_id")
                    ),
                }],
            }
            collected, summary = collect(
                manifest, root, mode="citation"
            )
            self.assertEqual(len(collected["CIT_AI_A"]), 2)
            self.assertEqual(summary["mode"], "citation")

    def test_missing_batch_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            manifest = {
                "classification": "AI_ADJUDICATION_BATCH_MANIFEST_NO_LABELS",
                "assignments_total": 1,
                "reviewers": {"AI_A": 1},
                "batches": [{
                    "reviewer_id": "AI_A",
                    "batch_number": 1,
                    "filename": "AI_A_batch_001.csv",
                    "assignments": 1,
                    "assignment_checksum_sha256": "x",
                }],
            }
            with self.assertRaises(FileNotFoundError):
                collect(manifest, Path(td), mode="article")

    def test_checksum_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rows = [article_row("A1", "WRONG", "AI_A")]
            write_csv(root / "AI_A_batch_001_output.csv", rows)
            manifest = {
                "classification": "AI_ADJUDICATION_BATCH_MANIFEST_NO_LABELS",
                "assignments_total": 1,
                "reviewers": {"AI_A": 1},
                "batches": [{
                    "reviewer_id": "AI_A",
                    "batch_number": 1,
                    "filename": "AI_A_batch_001.csv",
                    "assignments": 1,
                    "assignment_checksum_sha256": checksum_rows(
                        [article_row("A1", "P1", "AI_A")],
                        ("assignment_id", "paper_id"),
                    ),
                }],
            }
            with self.assertRaises(ValueError):
                collect(manifest, root, mode="article")

    def test_wrong_adjudicator_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rows = [article_row("A1", "P1", "AI_B")]
            write_csv(root / "AI_A_batch_001_output.csv", rows)
            manifest = {
                "classification": "AI_ADJUDICATION_BATCH_MANIFEST_NO_LABELS",
                "assignments_total": 1,
                "reviewers": {"AI_A": 1},
                "batches": [{
                    "reviewer_id": "AI_A",
                    "batch_number": 1,
                    "filename": "AI_A_batch_001.csv",
                    "assignments": 1,
                    "assignment_checksum_sha256": checksum_rows(
                        rows, ("assignment_id", "paper_id")
                    ),
                }],
            }
            with self.assertRaises(ValueError):
                collect(manifest, root, mode="article")

    def test_indeterminate_requires_abstain_reason(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            row = article_row("A1", "P1", "AI_A")
            row["scientific_state"] = "INDETERMINATE"
            row["abstain_reason"] = ""
            write_csv(root / "AI_A_batch_001_output.csv", [row])
            manifest = {
                "classification": "AI_ADJUDICATION_BATCH_MANIFEST_NO_LABELS",
                "assignments_total": 1,
                "reviewers": {"AI_A": 1},
                "batches": [{
                    "reviewer_id": "AI_A",
                    "batch_number": 1,
                    "filename": "AI_A_batch_001.csv",
                    "assignments": 1,
                    "assignment_checksum_sha256": checksum_rows(
                        [row], ("assignment_id", "paper_id")
                    ),
                }],
            }
            with self.assertRaises(ValueError):
                collect(manifest, root, mode="article")


if __name__ == "__main__":
    unittest.main()
