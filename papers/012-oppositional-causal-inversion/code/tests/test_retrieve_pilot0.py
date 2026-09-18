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

    def test_anchor_groups_require_one_from_each_group(self):
        ok, missing = m.title_passes_anchor_groups(
            "Over-optimization of academic publishing metrics: observing Goodhart's Law in action",
            [["goodhart", "campbell"], ["metric", "target", "proxy"]],
        )
        self.assertTrue(ok)
        self.assertEqual(missing, [])

        ok, missing = m.title_passes_anchor_groups(
            "Goodhart, Sir Ernest Frederic, barrister-at-law",
            [["goodhart", "campbell"], ["metric", "target", "proxy"]],
        )
        self.assertFalse(ok)
        self.assertEqual(len(missing), 1)

    def test_filter_rejects_wrong_type_and_wrong_topic(self):
        query = {"anchor_groups":[["autonomy"],["dependence","delegation"]]}
        records = [
            {"title":"Autonomy and dependence in organizations","type":"article"},
            {"title":"Cardiovascular autonomic neuropathy in diabetes","type":"article"},
            {"title":"Autonomy and dependence questionnaire","type":"dataset"},
        ]
        accepted, rejected = m.filter_records(records, query, ["article"])
        self.assertEqual(len(accepted), 1)
        self.assertEqual(len(rejected), 2)
        reasons = [r["rejection_reasons"] for r in rejected]
        self.assertTrue(any("missing_anchor_group" in x for x in reasons))
        self.assertTrue(any("type_not_allowed" in x for x in reasons))


if __name__ == "__main__":
    unittest.main()
