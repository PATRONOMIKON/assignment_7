# Assignment 6 — Longest Common Subsequence (LCS)

This project implements and compares three algorithms that return the **length** of the longest common subsequence shared by two strings. The included datasets are DNA strings using `A`, `C`, `G`, and `T`.

## Files

- `lcs_solver.py` — naive recursion, top-down memoization, and bottom-up tabulation.
- `sequence_generator.py` — generates reproducible pairs of sizes 10, 20, 50, 100, 200, 500, and 1000.
- `sequences/` — generated JSON input datasets.
- `test_lcs.py` — correctness tests, including the assignment example.
- `benchmark.py` — times the algorithms and writes `benchmark_results.csv`.
- `benchmark_results.csv` — measured timings from the included datasets (timings vary by machine).
- `LCS_Analysis.docx` — written analysis submitted with the project.

## Run

Use Python 3.9 or newer. No third-party packages are required.

```bash
python -m unittest -v
python sequence_generator.py
python benchmark.py
```

The generator defaults to seed `2026`, so the same input strings are generated on each run. To use another seed:

```bash
python sequence_generator.py --seed 123
```

The naive recursive implementation is intentionally exponential and is benchmarked only for sizes up to 20. The benchmark has a 10-second guard for recursive runs on Unix-like systems. Memoization and tabulation are run for all supplied sizes. Tabulation stores only two rows, using `O(min(n, m))` auxiliary space.

## Algorithm summary

For prefixes ending at positions `i` and `j`, an empty prefix has LCS length 0. If the final characters match, add one to the LCS of the two shorter prefixes. Otherwise, take the maximum after removing one final character from either sequence. Memoization caches each index pair; tabulation computes the same recurrence iteratively.
