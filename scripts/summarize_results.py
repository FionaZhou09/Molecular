import argparse
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import resolve_project_path
from src.evaluate import summarize_benchmark_results


def parse_args():
    parser = argparse.ArgumentParser(description="Summarize molecular benchmark results.")
    parser.add_argument(
        "--results-path",
        default="results/benchmark_results.csv",
    )
    parser.add_argument(
        "--summary-path",
        default="results/benchmark_summary.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = pd.read_csv(resolve_project_path(Path(args.results_path)))
    summary = summarize_benchmark_results(results)

    summary_path = resolve_project_path(Path(args.summary_path))
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(summary_path, index=False)
    print(f"Wrote {len(summary)} summary rows to {args.summary_path}")


if __name__ == "__main__":
    main()
