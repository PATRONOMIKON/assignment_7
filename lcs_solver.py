"""Longest Common Subsequence (LCS) implementations for DNA strings.

The three functions return the length of the LCS, not the subsequence itself.
They accept arbitrary strings, although the supplied datasets use A/C/G/T.
"""
from functools import lru_cache
import sys


def lcs_recursive(seq1: str, seq2: str) -> int:
    """Naive exponential-time recursion, included for comparison."""
    def solve(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0
        if seq1[i - 1] == seq2[j - 1]:
            return 1 + solve(i - 1, j - 1)
        return max(solve(i - 1, j), solve(i, j - 1))
    return solve(len(seq1), len(seq2))


def lcs_memoization(seq1: str, seq2: str) -> int:
    """Top-down dynamic programming; cache each pair of prefix lengths."""
    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0
        if seq1[i - 1] == seq2[j - 1]:
            return 1 + solve(i - 1, j - 1)
        return max(solve(i - 1, j), solve(i, j - 1))
    # The longest dependency chain can approach len(seq1) + len(seq2).
    # Raise the interpreter limit for this call, then restore the prior setting.
    old_limit = sys.getrecursionlimit()
    needed_limit = len(seq1) + len(seq2) + 100
    try:
        if needed_limit > old_limit:
            sys.setrecursionlimit(needed_limit)
        return solve(len(seq1), len(seq2))
    finally:
        if sys.getrecursionlimit() != old_limit:
            sys.setrecursionlimit(old_limit)


def lcs_tabulation(seq1: str, seq2: str) -> int:
    """Bottom-up dynamic programming using O(len(seq1)*len(seq2)) time.

    Only two rows are stored, reducing auxiliary space to O(min(n, m)).
    """
    # Keep the shorter sequence on the columns to minimize memory.
    if len(seq2) > len(seq1):
        seq1, seq2 = seq2, seq1
    m = len(seq2)
    previous = [0] * (m + 1)
    for char1 in seq1:
        current = [0] * (m + 1)
        for j, char2 in enumerate(seq2, start=1):
            if char1 == char2:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[m]
