import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.train import (
    BENCHMARK_DATASETS,
    BENCHMARK_FEATURE_TYPES,
    BENCHMARK_MODEL_KEYS,
    BENCHMARK_SEEDS,
    BENCHMARK_SPLIT_TYPES,
    build_benchmark_plan,
    run_benchmark_matrix,
)


def _parse_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _parse_seeds(value: str) -> tuple[int, ...]:
    return tuple(int(seed) for seed in _parse_csv(value))


def parse_args():
    parser = argparse.ArgumentParser(description="Run the molecular benchmark matrix.")
    parser.add_argument("--datasets", default=",".join(BENCHMARK_DATASETS))
    parser.add_argument("--feature-types", default=",".join(BENCHMARK_FEATURE_TYPES))
    parser.add_argument("--models", default=",".join(BENCHMARK_MODEL_KEYS))
    parser.add_argument("--split-types", default=",".join(BENCHMARK_SPLIT_TYPES))
    parser.add_argument(
        "--seeds",
        default=",".join(str(seed) for seed in BENCHMARK_SEEDS),
    )
    parser.add_argument(
        "--results-path",
        default="results/benchmark_results.csv",
    )
    parser.add_argument(
        "--predictions-path",
        default="results/predictions.csv",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run one cheap ESOL/Ridge/descriptors/random experiment.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the experiment plan without training models or writing outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.smoke:
        datasets = ("esol",)
        feature_types = ("descriptors",)
        model_keys = ("ridge",)
        split_types = ("random",)
        seeds = (0,)
    else:
        datasets = _parse_csv(args.datasets)
        feature_types = _parse_csv(args.feature_types)
        model_keys = _parse_csv(args.models)
        split_types = _parse_csv(args.split_types)
        seeds = _parse_seeds(args.seeds)

    if args.dry_run:
        plan = build_benchmark_plan(
            datasets=datasets,
            feature_types=feature_types,
            model_keys=model_keys,
            split_types=split_types,
            seeds=seeds,
        )
        print(plan.to_string(index=False))
        print(f"\n{len(plan)} experiments planned.")
        return

    results, predictions = run_benchmark_matrix(
        datasets=datasets,
        feature_types=feature_types,
        model_keys=model_keys,
        split_types=split_types,
        seeds=seeds,
        results_path=args.results_path,
        predictions_path=args.predictions_path,
    )
    print(f"Wrote {len(results)} result rows to {args.results_path}")
    print(f"Wrote {len(predictions)} prediction rows to {args.predictions_path}")


if __name__ == "__main__":
    main()
