import unittest
from types import SimpleNamespace
from unittest.mock import patch

from pilotM_known_case_enrichment import _sample_unique_control_pool


class MultiSeedControlPoolTests(unittest.TestCase):
    def test_pool_scales_beyond_one_openalex_sample_page(self):
        calls = []

        def fake_sample_works(*, filters, sample_size, seed, api_key=None):
            calls.append((filters, sample_size, seed, api_key))
            return [
                SimpleNamespace(openalex_id=f"W{seed}_{i}")
                for i in range(sample_size)
            ]

        with patch(
            "pilotM_known_case_enrichment.sample_works",
            side_effect=fake_sample_works,
        ):
            pool, meta = _sample_unique_control_pool(
                filters="publication_year:1980,type:article",
                target_size=120,
                base_seed=7,
                api_key=None,
            )

        self.assertEqual(len(pool), 120)
        self.assertEqual(meta["unique_size"], 120)
        self.assertEqual(
            [row[1] for row in calls],
            [100, 20],
        )
        self.assertEqual(
            [row[2] for row in calls],
            [7, 104736],
        )
        self.assertTrue(all(row[1] <= 100 for row in calls))

    def test_excluded_ids_are_replaced_deterministically(self):
        calls = []

        def fake_sample_works(*, filters, sample_size, seed, api_key=None):
            calls.append((sample_size, seed))
            if len(calls) == 1:
                return [
                    SimpleNamespace(openalex_id="CASE"),
                    SimpleNamespace(openalex_id="A"),
                    SimpleNamespace(openalex_id="B"),
                ]
            return [
                SimpleNamespace(openalex_id="C"),
                SimpleNamespace(openalex_id="D"),
            ][:sample_size]

        with patch(
            "pilotM_known_case_enrichment.sample_works",
            side_effect=fake_sample_works,
        ):
            pool, meta = _sample_unique_control_pool(
                filters="publication_year:1980,type:article",
                target_size=3,
                base_seed=11,
                api_key=None,
                exclude_ids={"CASE"},
            )

        self.assertEqual(
            [work.openalex_id for work in pool],
            ["A", "B", "C"],
        )
        self.assertEqual(meta["unique_size"], 3)
        self.assertEqual(len(meta["attempts"]), 2)


if __name__ == "__main__":
    unittest.main()
