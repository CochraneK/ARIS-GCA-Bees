import urllib.error
import unittest
from unittest.mock import patch

import openalex_adapter


class OpenAlexAdapterTests(unittest.TestCase):
    def test_count_works_reads_meta_count(self):
        def fake_request(path, *, params=None, api_key=None, **kwargs):
            self.assertEqual(path, "/works")
            self.assertEqual(params["filter"], "publication_year:1921")
            return {"results": [], "meta": {"count": 321}}

        with patch.object(openalex_adapter, "_request_json", fake_request):
            count = openalex_adapter.count_works(
                filters="publication_year:1921"
            )

        self.assertEqual(count, 321)

    def test_iter_works_uses_cursor_pagination(self):
        calls = []

        def fake_request(path, *, params=None, api_key=None, **kwargs):
            calls.append((path, dict(params or {})))
            cursor = params["cursor"]
            if cursor == "*":
                return {
                    "results": [
                        {
                            "id": "https://openalex.org/W1",
                            "display_name": "One",
                            "publication_year": 1921,
                            "primary_topic": {
                                "field": {
                                    "id": "https://openalex.org/fields/25"
                                }
                            },
                            "authorships": [{}],
                            "referenced_works_count": 1,
                        }
                    ],
                    "meta": {"next_cursor": "NEXT"},
                }
            return {
                "results": [
                    {
                        "id": "https://openalex.org/W2",
                        "display_name": "Two",
                        "publication_year": 1921,
                        "primary_topic": {
                            "field": {
                                "id": "https://openalex.org/fields/25"
                            }
                        },
                        "authorships": [{}, {}],
                        "referenced_works_count": 2,
                    }
                ],
                "meta": {"next_cursor": None},
            }

        with (
            patch.object(openalex_adapter, "_request_json", fake_request),
            patch.object(openalex_adapter.time, "sleep"),
        ):
            works = list(
                openalex_adapter.iter_works(
                    filters=(
                        "publication_year:1921,type:article,"
                        "primary_topic.field.id:25"
                    )
                )
            )

        self.assertEqual([w.openalex_id for w in works], ["W1", "W2"])
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][1]["cursor"], "*")
        self.assertEqual(calls[1][1]["cursor"], "NEXT")
        self.assertIn("referenced_works_count", calls[0][1]["select"])

    def test_historical_filter_is_sent_to_api(self):
        calls = []

        def fake_request(path, *, params=None, api_key=None, **kwargs):
            calls.append((path, params))
            return {
                "results": [
                    {
                        "id": "https://openalex.org/W1",
                        "publication_year": 2010,
                        "display_name": "Citing work",
                        "doi": None,
                    }
                ],
                "meta": {"next_cursor": None},
            }

        with (
            patch.object(openalex_adapter, "_request_json", fake_request),
            patch.object(openalex_adapter.time, "sleep"),
        ):
            rows = list(
                openalex_adapter.iter_citing_works(
                    "W123",
                    to_publication_year=2011,
                )
            )

        self.assertEqual(len(rows), 1)
        self.assertEqual(calls[0][0], "/works")
        self.assertIn("cites:W123", calls[0][1]["filter"])
        self.assertIn(
            "to_publication_date:2011-12-31",
            calls[0][1]["filter"],
        )

    def test_work_payload_extracts_primary_field_id(self):
        work = openalex_adapter.OpenAlexWork.from_payload(
            {
                "id": "https://openalex.org/W1",
                "display_name": "Target",
                "publication_year": 1980,
                "primary_topic": {
                    "display_name": "Topic",
                    "field": {
                        "id": "https://openalex.org/fields/31",
                        "display_name": "Physics and Astronomy",
                    },
                },
                "authorships": [{}, {}],
                "referenced_works_count": 12,
            }
        )
        self.assertEqual(work.primary_field_id, "31")
        self.assertEqual(work.authorship_count, 2)
        self.assertEqual(work.referenced_works_count, 12)

    def test_short_id_accepts_full_openalex_url(self):
        self.assertEqual(
            openalex_adapter._short_id("https://openalex.org/W123"),
            "W123",
        )

    def test_retry_delay_respects_reasonable_retry_after(self):
        error = urllib.error.HTTPError(
            "https://api.openalex.org/works",
            429,
            "Too Many Requests",
            {"Retry-After": "7"},
            None,
        )
        self.assertEqual(
            openalex_adapter._retry_delay(error, attempt=3),
            7.0,
        )

    def test_retry_delay_bounds_large_retry_after(self):
        error = urllib.error.HTTPError(
            "https://api.openalex.org/works",
            429,
            "Too Many Requests",
            {"Retry-After": "9999"},
            None,
        )
        self.assertEqual(
            openalex_adapter._retry_delay(error, attempt=2),
            4.0,
        )

    def test_known_work_history_does_not_refetch_target_metadata(self):
        work = openalex_adapter.OpenAlexWork(
            openalex_id="W123",
            title="Target",
            publication_year=2000,
            doi=None,
            cited_by_count=None,
            primary_topic=None,
        )

        citing_rows = [
            {"publication_year": 2001},
            {"publication_year": 2003},
        ]

        with (
            patch.object(
                openalex_adapter,
                "iter_citing_works",
                return_value=iter(citing_rows),
            ),
            patch.object(
                openalex_adapter,
                "fetch_work",
                side_effect=AssertionError("must not refetch target"),
            ),
        ):
            history = openalex_adapter.reconstruct_history_for_known_work(
                work,
                end_year=2003,
            )

        self.assertEqual(history.counts, (0, 1, 0, 1))
        self.assertEqual(history.total_citations, 2)


if __name__ == "__main__":
    unittest.main()
