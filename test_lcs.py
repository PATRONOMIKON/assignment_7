"""Correctness tests for all LCS implementations; run with python -m unittest."""
import unittest
from lcs_solver import lcs_recursive, lcs_memoization, lcs_tabulation


class LCSTests(unittest.TestCase):
    def test_known_examples(self):
        for fn in (lcs_recursive, lcs_memoization, lcs_tabulation):
            self.assertEqual(fn("AGGTAB", "GXTXAYB"), 4)
            self.assertEqual(fn("ABCDGH", "AEDFHR"), 3)
            self.assertEqual(fn("ABC", "AC"), 2)

    def test_empty_and_identical(self):
        for fn in (lcs_recursive, lcs_memoization, lcs_tabulation):
            self.assertEqual(fn("", "ABC"), 0)
            self.assertEqual(fn("", ""), 0)
            self.assertEqual(fn("ACGT", "ACGT"), 4)

    def test_no_common_characters(self):
        for fn in (lcs_recursive, lcs_memoization, lcs_tabulation):
            self.assertEqual(fn("AAAA", "TTTT"), 0)

    def test_consistency_on_small_strings(self):
        cases = [("GATTACA", "GCATGCU"), ("TACG", "AGCT"), ("CCGT", "CGT")]
        for a, b in cases:
            expected = lcs_tabulation(a, b)
            self.assertEqual(lcs_recursive(a, b), expected)
            self.assertEqual(lcs_memoization(a, b), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
