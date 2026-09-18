#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))

from validate_work_decisions import validate  # noqa: E402

WORK_FIELDS = [
    "person_id",
    "canonical_name",
    "openalex_work_id",
    "work_decision",
    "include_in_network",
    "canonical_work_id",
    "decision_evidence",
    "reviewer",
    "second_reviewer",
    "adjudication_status",
    "mh_blinded_at_work_lock",
    "review_date",
]
IDENTITY_FIELDS = [
    "person_id",
    "canonical_name",
    "identity_status",
]


def write_csv(fields: list[str], rows: list[dict[str, str]]) -> Path:
    tmp = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".csv", delete=False)
    with tmp:
        writer = csv.DictWriter(tmp, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return Path(tmp.name)


class WorkDecisionValidatorTests(unittest.TestCase):
    def base(self) -> dict[str, str]:
        return {
            "person_id": "p1",
            "canonical_name": "Historical Scientist",
            "openalex_work_id": "W1",
            "work_decision": "KEEP_ORIGINAL",
            "include_in_network": "true",
            "canonical_work_id": "W1",
            "decision_evidence": "known work",
            "reviewer": "r1",
            "second_reviewer": "",
            "adjudication_status": "first-review-locked",
            "mh_blinded_at_work_lock": "true",
            "review_date": "2026-09-18",
        }

    def test_keep_row_passes_with_verified_identity(self) -> None:
        work = write_csv(WORK_FIELDS, [self.base()])
        identity = write_csv(
            IDENTITY_FIELDS,
            [{"person_id": "p1", "canonical_name": "Historical Scientist", "identity_status": "VERIFIED_SINGLE"}],
        )
        try:
            self.assertEqual(validate(work, identity_path=identity), [])
        finally:
            work.unlink(missing_ok=True)
            identity.unlink(missing_ok=True)

    def test_excluded_work_cannot_be_in_network(self) -> None:
        row = self.base()
        row.update({"work_decision": "EXCLUDE_NAME_COLLISION", "include_in_network": "true", "canonical_work_id": ""})
        work = write_csv(WORK_FIELDS, [row])
        try:
            errors = validate(work)
            self.assertTrue(any("include_in_network" in error for error in errors))
        finally:
            work.unlink(missing_ok=True)

    def test_nonverified_identity_blocks_work_review(self) -> None:
        work = write_csv(WORK_FIELDS, [self.base()])
        identity = write_csv(
            IDENTITY_FIELDS,
            [{"person_id": "p1", "canonical_name": "Historical Scientist", "identity_status": "AMBIGUOUS_COLLISION"}],
        )
        try:
            errors = validate(work, identity_path=identity)
            self.assertTrue(any("VERIFIED identities" in error for error in errors))
        finally:
            work.unlink(missing_ok=True)
            identity.unlink(missing_ok=True)

    def test_complete_queue_detects_missing_decision(self) -> None:
        work = write_csv(WORK_FIELDS, [self.base()])
        queue_fields = ["person_id", "canonical_name", "openalex_work_id"]
        queue = write_csv(
            queue_fields,
            [
                {"person_id": "p1", "canonical_name": "Historical Scientist", "openalex_work_id": "W1"},
                {"person_id": "p1", "canonical_name": "Historical Scientist", "openalex_work_id": "W2"},
            ],
        )
        try:
            errors = validate(work, review_queue_path=queue, require_complete_queue=True)
            self.assertTrue(any("missing decision" in error for error in errors))
        finally:
            work.unlink(missing_ok=True)
            queue.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
