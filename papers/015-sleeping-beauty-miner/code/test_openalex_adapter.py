import unittest
from unittest.mock import patch

import openalex_adapter


class OpenAlexAdapterTests(unittest.TestCase):
    def test_historical_filter_is_sent_to_api(self):
        calls = []

        def fake_request(path, *, params=None, api_key=None, timeout=30):
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

        with patch.object(openalex_adapter, "_request_json", fake_request):
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

    def test_short_id_accepts_full_openalex_url(self):
        self.assertEqual(
            openalex_adapter._short_id("https://openalex.org/W123"),
            "W123",
        )


if __name__ == "__main__":
    unittest.main()
