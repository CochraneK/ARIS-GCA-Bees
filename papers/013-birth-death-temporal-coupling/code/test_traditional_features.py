import json
import unittest
from datetime import date
from pathlib import Path

import pseudo_calendars as pseudo
import traditional_features as tf


class TraditionalFeatureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).parents[1] / "process" / "TRADITIONAL_REFERENCE_VECTORS.json"
        cls.vectors = json.loads(path.read_text(encoding="utf-8"))

    def test_pinned_library(self):
        self.assertEqual(tf.INSTALLED_LUNAR_PYTHON, "1.4.8")
        self.assertEqual(tf.PINNED_LUNAR_PYTHON, "1.4.8")

    def test_reference_vectors(self):
        for vector in self.vectors["vectors"]:
            with self.subTest(vector=vector["id"]):
                y,m,d = map(int, vector["date"].split("-"))
                got = tf.date_only_features(date(y,m,d))
                exp = vector["expected"]

                if "official_year_ganzhi" in exp:
                    self.assertEqual(
                        got["official_chinese_calendar"]["year"]["ganzhi"],
                        exp["official_year_ganzhi"],
                    )
                if "bazi_year_ganzhi" in exp:
                    value = got["bazi_style_date_only"]["year"]
                    actual = None if value is None else value["ganzhi"]
                    self.assertEqual(actual, exp["bazi_year_ganzhi"])
                if "li_chun_ambiguous" in exp:
                    self.assertEqual(
                        got["bazi_style_date_only"][
                            "year_ambiguous_without_birth_time"
                        ],
                        exp["li_chun_ambiguous"],
                    )
                if "solar_term_on_date" in exp:
                    self.assertIn(
                        exp["solar_term_on_date"],
                        got["boundary_flags"]["solar_terms_on_date"],
                    )
                if "bazi_month_branch" in exp:
                    self.assertEqual(
                        got["bazi_style_date_only"]["month"]["branch"],
                        exp["bazi_month_branch"],
                    )
                if "civil_day_ganzhi" in exp:
                    self.assertEqual(
                        got["civil_date_sexagenary_day"]["ganzhi"],
                        exp["civil_day_ganzhi"],
                    )

    def test_li_chun_date_never_guesses_year(self):
        got = tf.date_only_features(date(2018,2,4))
        self.assertTrue(
            got["bazi_style_date_only"][
                "year_ambiguous_without_birth_time"
            ]
        )
        self.assertIsNone(got["bazi_style_date_only"]["year"])

    def test_pseudo_element_map_is_balanced_and_deterministic(self):
        a = pseudo.balanced_stem_element_map(13001)
        b = pseudo.balanced_stem_element_map(13001)
        self.assertEqual(a,b)
        counts = {}
        for value in a.values():
            counts[value] = counts.get(value,0) + 1
        self.assertEqual(set(counts.values()), {2})
        self.assertNotEqual(a, tf.STEM_ELEMENT)

    def test_pseudo_polarity_map_is_balanced(self):
        m = pseudo.balanced_stem_polarity_map(13002)
        self.assertEqual(
            sorted(m.values()).count("Yang"),
            5,
        )
        self.assertEqual(
            sorted(m.values()).count("Yin"),
            5,
        )

    def test_solar_boundary_shift_is_nontrivial(self):
        shifts = {pseudo.solar_boundary_shift_days(s) for s in range(13001,13020)}
        self.assertTrue(all(abs(x) >= 3 for x in shifts))
        self.assertTrue(all(abs(x) <= 30 for x in shifts))
        self.assertGreater(len(shifts), 3)


if __name__ == "__main__":
    unittest.main()
