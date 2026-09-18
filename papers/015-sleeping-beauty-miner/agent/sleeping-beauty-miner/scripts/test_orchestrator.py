import unittest

from orchestrator import run


class OrchestratorTests(unittest.TestCase):
    def test_prospective_cutoff_hides_future_citations(self):
        card = run(
            {
                "paper_id": "p1",
                "publication_year": 2000,
                "mode": "PROSPECTIVE",
                "cutoff_year": 2003,
                "citation_history": [0, 0, 1, 0, 20, 50],
                "baseline_strategy": "momentum_3y",
                "provenance": ["synthetic"],
            }
        )
        self.assertEqual(
            card["citation_trajectory"]["counts"],
            [0, 0, 1, 0],
        )
        self.assertEqual(card["analysis_cutoff"], 2003)
        self.assertEqual(card["state"], "INSUFFICIENT_DATA")

    def test_retrospective_emits_metrics(self):
        card = run(
            {
                "paper_id": "p2",
                "publication_year": 2000,
                "mode": "RETROSPECTIVE",
                "citation_history": [0, 0, 0, 1, 10, 20],
                "provenance": ["synthetic"],
            }
        )
        metrics = card["retrospective_metrics"]
        self.assertAlmostEqual(metrics["beauty_coefficient"], 23.6)
        self.assertEqual(metrics["awakening_time"], 3)

    def test_future_integrity_flag_is_hidden(self):
        card = run(
            {
                "paper_id": "p3",
                "publication_year": 2000,
                "mode": "PROSPECTIVE",
                "cutoff_year": 2005,
                "citation_history": [0, 0, 0, 1, 2, 3],
                "integrity_findings": [
                    {
                        "finding_id": "later",
                        "detector_id": "retraction-check",
                        "applicable": True,
                        "status": "FLAG",
                        "evidence_class": "E2",
                        "available_year": 2015
                    }
                ],
                "provenance": ["synthetic"],
            }
        )
        gate = card["integrity_gate"]
        self.assertEqual(gate["state"], "ABSTAIN")
        self.assertEqual(
            gate["excluded_future_finding_ids"],
            ["later"],
        )

    def test_cutoff_safe_quarantine_overrides_state(self):
        card = run(
            {
                "paper_id": "p4",
                "publication_year": 2000,
                "mode": "PROSPECTIVE",
                "cutoff_year": 2005,
                "citation_history": [0, 0, 0, 1, 2, 3],
                "candidate_state": "DORMANT_CANDIDATE",
                "integrity_findings": [
                    {
                        "finding_id": "deterministic",
                        "detector_id": "d1",
                        "applicable": True,
                        "status": "FLAG",
                        "evidence_class": "E0",
                        "reproducible": "yes",
                        "available_year": 2004
                    }
                ],
                "provenance": ["synthetic"],
            }
        )
        self.assertEqual(card["state"], "INTEGRITY_QUARANTINED")


if __name__ == "__main__":
    unittest.main()
