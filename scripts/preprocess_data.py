import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATASETS  # noqa: E402
from src.data_loader import (  # noqa: E402
    load_raw_dataset,
    normalize_dataset,
    save_processed_dataset,
    validate_smiles,
)


def preprocess_dataset(dataset_key: str) -> tuple[int, int]:
    config = DATASETS[dataset_key]
    raw_df = load_raw_dataset(dataset_key)
    normalized_df = normalize_dataset(raw_df, config.smiles_column, config.target_column)
    valid_df, invalid_df = validate_smiles(normalized_df)
    save_processed_dataset(dataset_key, valid_df)
    return len(valid_df), len(invalid_df)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess raw molecular datasets.")
    parser.add_argument("--dataset", choices=sorted(DATASETS), required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    valid_count, invalid_count = preprocess_dataset(args.dataset)
    print(
        f"Processed {args.dataset}: saved {valid_count} valid rows, "
        f"found {invalid_count} invalid rows."
    )


if __name__ == "__main__":
    main()
