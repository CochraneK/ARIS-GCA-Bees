import csv
import tempfile
import unittest
from pathlib import Path

from baselines import cutoff_features, rank_histories
from candidate_card import DISCLAIMER, build_candidate_card, evidence_item
from integrity_adapter import adapt_011_findings
from sciscinet_adapter import (
    iter_citation_edges,
    load_paper_years,
    reconstruct_target_history,
)


class BaselineTests(unittest.TestCase):
    def test_cutoff_features_use_only_supplied_history(self):
        features = cutoff_features([0, 0, 1, 0, 2, 4])
        self.assertEqual(features.total_citations, 7)
        self.assertEqual(features.recent_3y, 6)
        self.assertEqual(features.previous_3y, 1)

    def test_rank_histories_is_deterministic(self):
        rows = [
            ("b", [0, 1, 1]),
            ("a", [0, 1, 1]),
            ("c", [0, 0, 5]),
        ]
        ranked = rank_histories(rows, strategy="momentum_3y")
        self.assertEqual(ranked[0][0], "c")
        self.assertEqual([x[0] for x in ranked[1:]], ["a", "b"])


class IntegrityAdapterTests(unittest.TestCase):
    def test_future_findings_are_not_leaked(self):
        findings = [
            {
                "finding_id": "old",
                "detector_id": "d1",
                "applicable": True,
                "status": "PASS",
                "evidence_class": "E1",
                "available_year": 2010,
            },
            {
                "finding_id": "future",
                "detector_id": "d2",
                "applicable": True,
                "status": "FLAG",
                "evidence_class": "E2",
                "available_year": 2020,
            },
        ]
        gate = adapt_011_findings(findings, cutoff_year=2015)
        self.assertEqual(gate.state, "CLEAR")
        self.assertEqual(gate.excluded_future_finding_ids, ("future",))

    def test_unknown_timestamp_abstains_in_prospective_mode(self):
        gate = adapt_011_findings(
            [
                {
                    "finding_id": "x",
                    "detector_id": "d1",
                    "applicable": True,
                    "status": "FLAG",
                    "evidence_class": "E1",
                }
            ],
            cutoff_year=2015,
        )
        self.assertEqual(gate.state, "ABSTAIN")
        self.assertFalse(gate.cutoff_safe)

    def test_single_e0_flag_is_caution_not_quarantine(self):
        gate = adapt_011_findings(
            [
                {
                    "finding_id": "meta",
                    "detector_id": "metadata-check",
                    "applicable": True,
                    "status": "FLAG",
                    "evidence_class": "E0",
                    "available_year": 2010,
                }
            ],
            cutoff_year=2015,
        )
        self.assertEqual(gate.state, "CAUTION")

    def test_independent_strong_flags_quarantine(self):
        findings = [
            {
                "finding_id": "a",
                "detector_id": "d1",
                "dependency_group": "g1",
                "applicable": True,
                "status": "FLAG",
                "evidence_class": "E1",
                "available_year": 2010,
            },
            {
                "finding_id": "b",
                "detector_id": "d2",
                "dependency_group": "g2",
                "applicable": True,
                "status": "FLAG",
                "evidence_class": "E2",
                "available_year": 2010,
            },
        ]
        gate = adapt_011_findings(findings, cutoff_year=2015)
        self.assertEqual(gate.state, "QUARANTINE")


class CandidateCardTests(unittest.TestCase):
    def test_quarantine_overrides_candidate_state(self):
        gate = adapt_011_findings(
            [
                {
                    "finding_id": "a",
                    "detector_id": "d1",
                    "dependency_group": "g1",
                    "applicable": True,
                    "status": "FLAG",
                    "evidence_class": "E1",
                    "available_year": 2010,
                },
                {
                    "finding_id": "b",
                    "detector_id": "d2",
                    "dependency_group": "g2",
                    "applicable": True,
                    "status": "FLAG",
                    "evidence_class": "E3",
                    "available_year": 2010,
                },
            ],
            cutoff_year=2015,
        )
        card = build_candidate_card(
            paper_id="p1",
            mode="PROSPECTIVE",
            analysis_cutoff=2015,
            state="DORMANT_CANDIDATE",
            evidence_families=[
                evidence_item(
                    name="citation_momentum",
                    applicable=True,
                    cutoff_safe=True,
                    status="SUPPORTIVE",
                    value=2.0,
                    provenance=["fixture"],
                )
            ],
            integrity_gate=gate,
            provenance=["fixture"],
        )
        self.assertEqual(card["state"], "INTEGRITY_QUARANTINED")
        self.assertEqual(card["disclaimer"], DISCLAIMER)


class SciSciNetAdapterTests(unittest.TestCase):
    def test_csv_slice_reconstructs_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            papers = tmp / "papers.csv"
            cites = tmp / "citations.csv"

            with papers.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["paper_id", "publication_year"],
                )
                writer.writeheader()
                writer.writerows(
                    [
                        {"paper_id": "target", "publication_year": 2000},
                        {"paper_id": "c1", "publication_year": 2001},
                        {"paper_id": "c2", "publication_year": 2004},
                        {"paper_id": "c3", "publication_year": 2004},
                    ]
                )

            with cites.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["citing_paper_id", "cited_paper_id"],
                )
                writer.writeheader()
                writer.writerows(
                    [
                        {"citing_paper_id": "c1", "cited_paper_id": "target"},
                        {"citing_paper_id": "c2", "cited_paper_id": "target"},
                        {"citing_paper_id": "c3", "cited_paper_id": "target"},
                    ]
                )

            years = load_paper_years(papers)
            edges = list(iter_citation_edges(cites))
            history = reconstruct_target_history(
                "target",
                paper_years=years,
                citation_edges=edges,
                end_year=2004,
            )
            self.assertEqual(history.counts, (0, 1, 0, 0, 2))


if __name__ == "__main__":
    unittest.main()
