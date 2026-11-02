"""Generate reproducible random DNA sequence pairs for LCS benchmarking."""
import argparse
import json
import random
from pathlib import Path

BASES = "ACGT"
SIZES = [10, 20, 50, 100, 200, 500, 1000]


def generate_sequences(output_dir="sequences", seed=2026):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    for size in SIZES:
        data = {
            "size": size,
            "sequence1": "".join(rng.choice(BASES) for _ in range(size)),
            "sequence2": "".join(rng.choice(BASES) for _ in range(size)),
        }
        with (output_path / f"dna_{size}.json").open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
    print(f"Generated datasets for sizes: {', '.join(map(str, SIZES))} in {output_path} (seed={seed}).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="sequences")
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    generate_sequences(args.output_dir, args.seed)
