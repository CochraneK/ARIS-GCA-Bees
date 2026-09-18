import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "retrieve_pilot0.py"
spec = importlib.util.spec_from_file_location("retrieve_pilot0", MODULE_PATH)
m = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(m)


class RetrievalTests(unittest.TestCase):
    def test_normalize_doi(self):
        self.assertEqual(m.normalize_doi("https://doi.org/10.1234/ABC.1 "), "10.1234/abc.1")

    def test_title_key_fallback(self):
        a = {"doi": "", "title": "A Paradox: Test!", "year": 2020}
        b = {"doi": None, "title": "A paradox test", "year": "2020"}
        self.assertEqual(m.dedupe_key(a), m.dedupe_key(b))

    def test_interleave_deduplicates(self):
        a = [
            {"doi":"10.1/x","title":"X","year":2020},
            {"doi":"10.1/y","title":"Y","year":2021},
        ]
        b = [
            {"doi":"10.1/x","title":"Different metadata","year":2020},
            {"doi":"10.1/z","title":"Z","year":2022},
        ]
        got = m.interleave_unique([a,b], 10)
        self.assertEqual([m.normalize_doi(x["doi"]) for x in got], ["10.1/x","10.1/y","10.1/z"])

    def test_limit(self):
        groups=[[{"doi":f"10.1/{i}","title":str(i),"year":2020} for i in range(5)]]
        self.assertEqual(len(m.interleave_unique(groups, 3)), 3)


if __name__ == "__main__":
    unittest.main()
