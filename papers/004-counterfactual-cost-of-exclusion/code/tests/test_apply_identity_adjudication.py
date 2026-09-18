#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
SCRIPT = CODE / "resolve" / "apply_identity_adjudication.py"

FIELDS = [
    "person_id","canonical_name","birth_year","death_year","identity_status",
    "verified_openalex_ids","cluster_completeness","network_observable",
    "strong_identifier_evidence","known_work_match_n","institution_match",
    "coauthor_match","topic_field_match","career_timing_match","conflicting_orcid",
    "reviewer","second_reviewer","adjudication_status","mh_blinded_at_identity_lock",
    "review_date","notes",
]
OVERRIDE_FIELDS = [
    "person_id","canonical_name","identity_status","verified_openalex_ids",
    "cluster_completeness","known_work_match_n","topic_field_match",
    "career_timing_match","conflicting_orcid","adjudication_status","notes",
]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


class ApplyIdentityAdjudicationTests(unittest.TestCase):
    def test_provisional_override_creates_zero_provisional_final(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            draft = root / "draft.csv"
            overrides = root / "overrides.csv"
            output = root / "final.csv"
            summary = root / "summary.json"
            row = {field: "" for field in FIELDS}
            row.update({
                "person_id":"p1","canonical_name":"A","birth_year":"1900","death_year":"1980",
                "identity_status":"PROVISIONAL_SINGLE","network_observable":"false",
            })
            write_csv(draft, FIELDS, [row])
            write_csv(overrides, OVERRIDE_FIELDS, [{
                "person_id":"p1","canonical_name":"A","identity_status":"VERIFIED_SINGLE",
                "verified_openalex_ids":"A1","cluster_completeness":"not_applicable",
                "known_work_match_n":"1","topic_field_match":"true","career_timing_match":"true",
                "conflicting_orcid":"false","adjudication_status":"first-review-locked",
                "notes":"MH-blind test evidence",
            }])
            subprocess.run([
                sys.executable, str(SCRIPT), "--draft", str(draft), "--overrides", str(overrides),
                "--output", str(output), "--summary-json", str(summary)
            ], check=True, capture_output=True, text=True)
            final = list(csv.DictReader(output.open(encoding="utf-8")))[0]
            self.assertEqual(final["identity_status"], "VERIFIED_SINGLE")
            self.assertEqual(final["verified_openalex_ids"], "A1")
            self.assertEqual(final["mh_blinded_at_identity_lock"], "true")
            self.assertEqual(json.loads(summary.read_text())["provisional_n"], 0)

    def test_override_refuses_nonprovisional_row(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            draft = root / "draft.csv"
            overrides = root / "overrides.csv"
            row = {field: "" for field in FIELDS}
            row.update({
                "person_id":"p1","canonical_name":"A","birth_year":"1900","death_year":"1980",
                "identity_status":"NO_GRAPH_RECORD","network_observable":"false",
            })
            write_csv(draft, FIELDS, [row])
            write_csv(overrides, OVERRIDE_FIELDS, [{
                "person_id":"p1","canonical_name":"A","identity_status":"VERIFIED_SINGLE",
                "verified_openalex_ids":"A1","cluster_completeness":"not_applicable",
                "known_work_match_n":"1","topic_field_match":"true","career_timing_match":"true",
                "conflicting_orcid":"false","adjudication_status":"x","notes":"x",
            }])
            proc = subprocess.run([
                sys.executable, str(SCRIPT), "--draft", str(draft), "--overrides", str(overrides),
                "--output", str(root/"out.csv"), "--summary-json", str(root/"s.json")
            ], capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("PROVISIONAL", proc.stderr + proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
