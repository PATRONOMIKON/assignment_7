"""Benchmark all approaches on the generated datasets and save CSV results.

Naive recursion is only attempted through length 20; a 10-second alarm protects
against unexpectedly expensive cases on supported Unix-like systems.
"""
import csv
import json
import signal
import time
from pathlib import Path
from lcs_solver import lcs_recursive, lcs_memoization, lcs_tabulation

SIZES = [10, 20, 50, 100, 200, 500, 1000]


class TimeLimit(Exception):
    pass


def _alarm_handler(signum, frame):
    raise TimeLimit("time limit exceeded")


def timed_call(function, a, b, timeout=None):
    start = time.perf_counter()
    if timeout is not None and hasattr(signal, "SIGALRM"):
        old_handler = signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(timeout)
        try:
            result = function(a, b)
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    else:
        result = function(a, b)
    return result, time.perf_counter() - start


def main():
    rows = []
    for size in SIZES:
        path = Path("sequences") / f"dna_{size}.json"
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        a, b = data["sequence1"], data["sequence2"]
        row = {"size": size, "lcs_length": "", "recursive_seconds": "", "memoization_seconds": "", "tabulation_seconds": ""}
        if size <= 20:
            try:
                result, elapsed = timed_call(lcs_recursive, a, b, timeout=10)
                row["lcs_length"] = result
                row["recursive_seconds"] = f"{elapsed:.6f}"
            except TimeLimit:
                row["recursive_seconds"] = ">10s timeout"
        for label, fn in (("memoization_seconds", lcs_memoization), ("tabulation_seconds", lcs_tabulation)):
            result, elapsed = timed_call(fn, a, b)
            if row["lcs_length"] == "":
                row["lcs_length"] = result
            elif result != row["lcs_length"]:
                raise AssertionError(f"Algorithms disagree for size {size}")
            row[label] = f"{elapsed:.6f}"
        rows.append(row)
        print(f"n={size:4}: LCS={row['lcs_length']}, recursive={row['recursive_seconds'] or 'skipped'}, "
              f"memo={row['memoization_seconds']}s, tabulation={row['tabulation_seconds']}s")
    with open("benchmark_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print("Saved benchmark_results.csv")


if __name__ == "__main__":
    main()
