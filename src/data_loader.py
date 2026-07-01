import pandas as pd

from src.config import DATASETS, resolve_project_path


def load_raw_dataset(dataset_key: str) -> pd.DataFrame:
    try:
        config = DATASETS[dataset_key]
    except KeyError as exc:
        valid_keys = ", ".join(sorted(DATASETS))
        raise KeyError(f"Unknown dataset key: {dataset_key}. Valid keys: {valid_keys}") from exc

    return pd.read_csv(resolve_project_path(config.raw_path))


def normalize_dataset(
    df: pd.DataFrame,
    smiles_col: str,
    target_col: str,
) -> pd.DataFrame:
    normalized = df.loc[:, [smiles_col, target_col]].rename(
        columns={smiles_col: "smiles", target_col: "target"}
    )
    return normalized.dropna(subset=["smiles", "target"]).reset_index(drop=True)
