#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(CODE / "simulate"))
sys.path.insert(0, str(CODE / "acquire"))

from counterfactual_core import TemporalGraph, Work, simulate  # noqa: E402
from build_candidate_frame import eligible_rows  # noqa: E402
from openalex_pilot import (  # noqa: E402
    author_name_score,
    career_plausibility,
    name_similarity,
    normalize_name,
    normalize_openalex_id,
    normalize_orcid,
)
from validate_exposure import validate  # noqa: E402


class CounterfactualCoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = TemporalGraph(
            works=[
                Work("f1", 1900, "focal", 1.0),
                Work("alt", 1900, "other", 1.0),
                Work("d1", 1910, "other", 5.0),
                Work("d2", 1920, "other", 2.0),
            ],
            edges=[("f1", "d1"), ("alt", "d1"), ("d1", "d2")],
        )

    def test_zero_attenuation_is_zero_cpe(self) -> None:
        result = simulate(self.graph, "focal", 1900, 0.0, "M2", seed=1)
        self.assertEqual(result.cpe, 0.0)
        self.assertEqual(result.directly_removed, [])

    def test_pre_intervention_work_is_preserved(self) -> None:
        result = simulate(self.graph, "focal", 1901, 1.0, "M0", seed=1)
        self.assertEqual(result.cpe, 0.0)
        self.assertEqual(result.directly_removed, [])

    def test_m0_removes_descendants(self) -> None:
        result = simulate(self.graph, "focal", 1900, 1.0, "M0", seed=1)
        self.assertEqual(set(result.directly_removed), {"f1"})
        self.assertEqual(set(result.dependency_lost), {"d1", "d2"})
        self.assertAlmostEqual(result.cpe, 8.0)

    def test_m1_respects_alternative_precursor(self) -> None:
        result = simulate(self.graph, "focal", 1900, 1.0, "M1", seed=1)
        self.assertEqual(set(result.directly_removed), {"f1"})
        self.assertEqual(result.dependency_lost, [])
        self.assertAlmostEqual(result.cpe, 1.0)

    def test_same_year_chain_uses_true_topological_order(self) -> None:
        graph = TemporalGraph(
            works=[
                Work("z_source", 1900, "focal", 1.0),
                Work("m_mid", 1900, "other", 1.0),
                Work("a_target", 1900, "other", 1.0),
            ],
            edges=[("z_source", "m_mid"), ("m_mid", "a_target")],
        )
        result = simulate(graph, "focal", 1900, 1.0, "M1", seed=1)
        self.assertEqual(set(result.dependency_lost), {"m_mid", "a_target"})
        self.assertAlmostEqual(result.cpe, 3.0)

    def test_m2_can_be_sign_negative(self) -> None:
        graph = TemporalGraph(
            works=[Work("f1", 1900, "focal", 1.0), Work("d1", 1910, "other", 5.0)],
            edges=[("f1", "d1")],
        )
        result = simulate(
            graph,
            "focal",
            1900,
            1.0,
            "M2",
            seed=1,
            replacement_probability=1.0,
            recovery_value_multiplier=2.0,
        )
        self.assertLess(result.cpe, 0.0)
        self.assertEqual(result.adaptively_recovered, ["d1"])

    def test_future_to_past_edge_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TemporalGraph(
                [Work("later", 1910, "a"), Work("earlier", 1900, "b")],
                [("later", "earlier")],
            )


class CandidateFrameTests(unittest.TestCase):
    def test_candidate_filter_has_no_mental_health_dependency(self) -> None:
        rows = [
            {
                "wikidata_code": "Q1",
                "name": "Scientist_One",
                "birth": "1900",
                "death": "1980",
                "level1_main_occ": "Discovery/Science",
                "mh_label_that_must_be_ignored": "anything",
            },
            {
                "wikidata_code": "Q2",
                "name": "Artist_Two",
                "birth": "1900",
                "death": "1980",
                "level1_main_occ": "Culture",
                "mh_label_that_must_be_ignored": "anything",
            },
        ]
        selected = eligible_rows(rows, 1850, 1975, 1900, 2026)
        self.assertEqual([row["wikidata_code"] for row in selected], ["Q1"])


class OpenAlexHelperTests(unittest.TestCase):
    def test_identifier_normalization(self) -> None:
        self.assertEqual(normalize_openalex_id("https://openalex.org/A1234"), "A1234")
        self.assertEqual(normalize_openalex_id("A1234"), "A1234")
        self.assertEqual(normalize_orcid("https://orcid.org/0000-0001-2345-6789"), "0000-0001-2345-6789")

    def test_name_normalization_handles_diacritics_and_punctuation(self) -> None:
        self.assertEqual(normalize_name("José-María O'Neill"), "jose maria o neill")

    def test_exact_and_alias_names_score_high(self) -> None:
        author = {
            "display_name": "John Nash",
            "display_name_alternatives": ["John Forbes Nash Jr."],
        }
        self.assertEqual(author_name_score("John Nash", author), 1.0)
        self.assertGreater(author_name_score("John Forbes Nash Jr", author), 0.95)
        self.assertLess(name_similarity("John Nash", "Alice Smith"), 0.5)

    def test_career_plausibility_prefers_lifetime_overlap(self) -> None:
        author = {
            "counts_by_year": [
                {"year": 1950, "works_count": 2},
                {"year": 1960, "works_count": 4},
                {"year": 1970, "works_count": 1},
            ]
        }
        self.assertGreater(career_plausibility(author, 1920, 2015), 0.9)
        self.assertEqual(career_plausibility(author, 1800, 1850), 0.0)


class ExposureValidatorTests(unittest.TestCase):
    FIELDS = [
        "person_id",
        "canonical_name",
        "birth_year",
        "death_year",
        "domain",
        "mh_evidence_class",
        "source_class_best",
        "source_primary_identifier",
        "search_status",
        "outcome_blinded_at_lock",
        "historical_term_normalized",
        "modern_mapping_family",
        "first_evidence_year",
        "last_evidence_year",
    ]

    def write_csv(self, row: dict[str, str]) -> Path:
        temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".csv", delete=False)
        with temp:
            writer = csv.DictWriter(temp, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerow(row)
        return Path(temp.name)

    def test_valid_a1_passes(self) -> None:
        path = self.write_csv(
            {
                "person_id": "p1",
                "canonical_name": "Historical Person",
                "birth_year": "1900",
                "death_year": "1980",
                "domain": "science",
                "mh_evidence_class": "A1",
                "source_class_best": "primary_clinical",
                "source_primary_identifier": "archive:123",
                "search_status": "expanded",
                "outcome_blinded_at_lock": "true",
                "historical_term_normalized": "historical clinical term",
                "modern_mapping_family": "",
                "first_evidence_year": "1930",
                "last_evidence_year": "1940",
            }
        )
        try:
            self.assertEqual(validate(path), [])
        finally:
            path.unlink(missing_ok=True)

    def test_a1_without_clinical_provenance_fails(self) -> None:
        path = self.write_csv(
            {
                "person_id": "p1",
                "canonical_name": "Historical Person",
                "birth_year": "1900",
                "death_year": "1980",
                "domain": "science",
                "mh_evidence_class": "A1",
                "source_class_best": "general_secondary",
                "source_primary_identifier": "website",
                "search_status": "basic",
                "outcome_blinded_at_lock": "true",
                "historical_term_normalized": "term",
                "modern_mapping_family": "",
                "first_evidence_year": "1930",
                "last_evidence_year": "1940",
            }
        )
        try:
            errors = validate(path)
            self.assertTrue(any("requires source_class_best=primary_clinical" in error for error in errors))
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
