import io
import unittest

import numpy as np

import pilot1_numident_raw as mod


class RawNumidentLayoutTest(unittest.TestCase):
    def _line(self, values):
        chars = [" "] * 186
        for name, value in values.items():
            start, end = mod.FIELD_SPECS[name]
            text = str(value)
            self.assertLessEqual(len(text), end - start)
            text = text.rjust(end - start)
            chars[start:end] = list(text)
        return "".join(chars) + "\n"

    def test_fixed_width_positions(self):
        line = self._line(
            {
                "bmonth": "12",
                "bday": "25",
                "byear": "1950",
                "sex": "2",
                "proof_death": "P",
                "dob_exception": "A",
                "special_exception": "B",
                "mbr_dob_exception": "C",
                "death_source": "42",
                "verified_edr": "Y",
                "dmonth": "07",
                "dday": "04",
                "dyear": "1994",
            }
        )
        df = next(mod.read_member_chunks(io.StringIO(line), 10))
        row = df.iloc[0]
        self.assertEqual(row["bmonth"].strip(), "12")
        self.assertEqual(row["bday"].strip(), "25")
        self.assertEqual(row["byear"].strip(), "1950")
        self.assertEqual(row["dmonth"].strip(), "07")
        self.assertEqual(row["dday"].strip(), "04")
        self.assertEqual(row["dyear"].strip(), "1994")
        self.assertEqual(row["death_source"].strip(), "42")
        self.assertEqual(row["verified_edr"].strip(), "Y")

    def test_calendar_validation(self):
        y = np.array([2000, 2001, 2001])
        m = np.array([2, 2, 4])
        d = np.array([29, 29, 31])
        self.assertEqual(
            mod.valid_gregorian(y, m, d).tolist(),
            [True, False, False],
        )

    def test_phase_safe_year_gap(self):
        by = np.array([1970, 1970, 1970, 1970])
        dy = np.array([1988, 1989, 2080, 2081])
        self.assertEqual(
            mod.phase_safe_year_gap(by, dy).tolist(),
            [False, True, True, False],
        )

    def test_primary_strata_use_exact_birth_year(self):
        acc = mod.PhaseAccumulator()
        acc.add(
            np.array([0, 10], dtype=np.int16),
            np.array([1, 11], dtype=np.int16),
            np.array([1900, 1901], dtype=np.int32),
            np.array([1988, 1988], dtype=np.int32),
            np.array([1, 1], dtype=np.int16),
        )
        self.assertIn((1900, 1988, 1), acc.strata)
        self.assertIn((1901, 1988, 1), acc.strata)
        summary = acc.summarize()
        self.assertEqual(summary["null_model"], "exact birth year × death year × sex")
        self.assertAlmostEqual(float(acc.expected().sum()), 2.0, places=9)


if __name__ == "__main__":
    unittest.main()
