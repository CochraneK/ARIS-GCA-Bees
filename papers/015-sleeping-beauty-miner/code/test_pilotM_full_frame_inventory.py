import unittest
from types import SimpleNamespace
from unittest.mock import patch

import pilotM_full_frame_inventory as inventory


def _work(work_id, year, field_id):
    return SimpleNamespace(
        openalex_id=work_id,
        title=work_id,
        publication_year=year,
        doi=None,
        cited_by_count=0,
        primary_topic="Topic",
        primary_field_id=field_id,
        referenced_works_count=1,
        authorship_count=1,
    )


class FullFrameInventoryTests(unittest.TestCase):
    def test_build_inventory_uses_exact_year_field_filters(self):
        case_works = {
            "10.1021/ja01539a017": _work("H", 1958, "25"),
            "10.1103/PhysRev.47.777": _work("E", 1935, "31"),
            "10.1103/PhysRev.17.273": _work("W", 1921, "25"),
        }
        filters_seen = []

        def fake_fetch(identifier, *, api_key=None):
            for doi, work in case_works.items():
                if doi in identifier:
                    return work
            raise AssertionError(identifier)

        def fake_count(*, filters, api_key=None):
            filters_seen.append(filters)
            return 2

        def fake_iter(*, filters, api_key=None, max_records=None, **kwargs):
            year = int(filters.split("publication_year:", 1)[1].split(",", 1)[0])
            field_id = filters.split("primary_topic.field.id:", 1)[1]
            return iter([
                _work(f"{year}-A", year, field_id),
                _work(f"{year}-B", year, field_id),
            ])

        with (
            patch.object(inventory, "fetch_work", side_effect=fake_fetch),
            patch.object(inventory, "count_works", side_effect=fake_count),
            patch.object(inventory, "iter_works", side_effect=fake_iter),
        ):
            result = inventory.build_inventory()

        self.assertEqual(len(result["frames"]), 3)
        self.assertEqual(
            result["frozen_primary_case_ids"],
            ["E", "H", "W"],
        )
        self.assertTrue(all(frame["complete"] for frame in result["frames"]))
        self.assertIn(
            "publication_year:1921,type:article,primary_topic.field.id:25",
            filters_seen,
        )
        self.assertIn(
            "publication_year:1935,type:article,primary_topic.field.id:31",
            filters_seen,
        )


if __name__ == "__main__":
    unittest.main()
