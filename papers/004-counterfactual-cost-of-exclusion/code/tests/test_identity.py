#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))

from validate_identity import validate  # noqa: E402


FIELDS = [
    "person_id",
    "canonical_name",
    "birth_year",
    "death_year",
    "identity_status",
    "verified_openalex_ids",
    "cluster_completeness",
    "network_observable",
    "strong_identifier_evidence",
    "known_work_match_n",
    "institution_match",
    "coauthor_match",
    "topic_field_match",
    "career_timing_match",
    "conflicting_orcid",
    "reviewer",
    "adjudication_status",
    "mh_blinded_at_identity_lock",
]


def write_csv(row: dict[str, str]) -> Path:
    temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".csv", delete=False)
    with temp:
        writer = csv.DictWriter(temp, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow(row)
    return Path(temp.name)


class IdentityValidatorTests(unittest.TestCase):
    def base(self) -> dict[str, str]:
        return {
            "person_id": "p1",
            "canonical_name": "Historical Scientist",
            "birth_year": "1900",
            "death_year": "1980",
            "identity_status": "VERIFIED_SINGLE",
            "verified_openalex_ids": "A123",
            "cluster_completeness": "",
            "network_observable": "true",
            "strong_identifier_evidence": "authority:example",
            "known_work_match_n": "0",
            "institution_match": "false",
            "coauthor_match": "false",
            "topic_field_match": "false",
            "career_timing_match": "false",
            "conflicting_orcid": "false",
            "reviewer": "reviewer1",
            "adjudication_status": "locked",
            "mh_blinded_at_identity_lock": "true",
        }

    def test_verified_single_with_strong_id_passes(self) -> None:
        path = write_csv(self.base())
        try:
            self.assertEqual(validate(path), [])
        finally:
            path.unlink(missing_ok=True)

    def test_verified_cluster_needs_multiple_ids(self) -> None:
        row = self.base()
        row.update({"identity_status": "VERIFIED_CLUSTER", "cluster_completeness": "high"})
        path = write_csv(row)
        try:
            errors = validate(path)
            self.assertTrue(any("at least 2 OpenAlex IDs" in error for error in errors))
        finally:
            path.unlink(missing_ok=True)

    def test_conflicting_orcid_blocks_verified_cluster(self) -> None:
        row = self.base()
        row.update(
            {
                "identity_status": "VERIFIED_CLUSTER",
                "verified_openalex_ids": "A1;A2",
                "cluster_completeness": "moderate",
                "conflicting_orcid": "true",
            }
        )
        path = write_csv(row)
        try:
            errors = validate(path)
            self.assertTrue(any("conflicting_orcid" in error for error in errors))
        finally:
            path.unlink(missing_ok=True)

    def test_provisional_cannot_be_confirmatory_network_observable(self) -> None:
        row = self.base()
        row.update(
            {
                "identity_status": "PROVISIONAL_SINGLE",
                "verified_openalex_ids": "",
                "network_observable": "true",
                "strong_identifier_evidence": "",
                "reviewer": "",
                "adjudication_status": "",
            }
        )
        path = write_csv(row)
        try:
            errors = validate(path)
            self.assertTrue(any("requires a verified identity state" in error for error in errors))
        finally:
            path.unlink(missing_ok=True)


    def test_unquoted_extra_csv_fields_fail(self) -> None:
        temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".csv", delete=False)
        path = Path(temp.name)
        try:
            with temp:
                temp.write(",".join(FIELDS) + "\n")
                values = [self.base().get(field, "") for field in FIELDS]
                temp.write(",".join(values) + ",unexpected_extra_field\n")
            errors = validate(path)
            self.assertTrue(any("unexpected extra field" in error for error in errors))
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
