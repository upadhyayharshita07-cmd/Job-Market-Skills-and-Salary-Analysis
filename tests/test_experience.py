import unittest

import pandas as pd

from app import extract_experience


class ExtractExperienceTests(unittest.TestCase):
    def summarize(self, *values):
        return extract_experience(pd.DataFrame({"Job Experience": list(values)}))

    def test_supported_ranges(self):
        cases = [
            ("3-8", 3, 8),
            ("3-8 Yrs", 3, 8),
            ("0-2 years", 0, 2),
            ("5 - 10 yr", 5, 10),
            ("  1 - 2 YeArS.  ", 1, 2),
            ("2-2 YEAR", 2, 2),
            ("4-6.", 4, 6),
        ]
        for value, low, high in cases:
            with self.subTest(value=value):
                self.assertEqual(self.summarize(value), {
                    "valid_records": 1,
                    "average_minimum": low,
                    "average_maximum": high,
                })

    def test_invalid_ranges(self):
        for value in ("8-3", "", " ", None, "three years", "3+", "3", "3.5-8", "3-8 months"):
            with self.subTest(value=value):
                self.assertEqual(self.summarize(value)["valid_records"], 0)

    def test_averages_are_calculated_separately_and_rounded(self):
        self.assertEqual(self.summarize("0-2 years", "3-8", "5-10 yr"), {
            "valid_records": 3,
            "average_minimum": 2.67,
            "average_maximum": 6.67,
        })

    def test_no_valid_ranges(self):
        empty_summary = {
            "valid_records": 0,
            "average_minimum": None,
            "average_maximum": None,
        }
        self.assertEqual(self.summarize(), empty_summary)
        self.assertEqual(self.summarize("", "8-3", "unknown"), empty_summary)

    def test_mixed_valid_and_invalid_ranges(self):
        self.assertEqual(self.summarize("0-2 years", "", "8-3", "4-6 YRS."), {
            "valid_records": 2,
            "average_minimum": 2.0,
            "average_maximum": 4.0,
        })
