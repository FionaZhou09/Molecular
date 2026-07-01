import pandas as pd
from rdkit import Chem

from src.config import DATASETS, resolve_project_path


def get_dataset_config(dataset_key: str):
    try:
        return DATASETS[dataset_key]
    except KeyError as exc:
        valid_keys = ", ".join(sorted(DATASETS))
        raise KeyError(f"Unknown dataset key: {dataset_key}. Valid keys: {valid_keys}") from exc


def load_raw_dataset(dataset_key: str) -> pd.DataFrame:
    config = get_dataset_config(dataset_key)
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


def validate_smiles(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    is_valid = df["smiles"].apply(
        lambda smiles: isinstance(smiles, str) and Chem.MolFromSmiles(smiles) is not None
    )
    valid_rows = df.loc[is_valid].reset_index(drop=True)
    invalid_rows = df.loc[~is_valid].reset_index(drop=True)
    return valid_rows, invalid_rows


def save_processed_dataset(dataset_key: str, df: pd.DataFrame) -> None:
    config = get_dataset_config(dataset_key)
    processed_path = resolve_project_path(config.processed_path)
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df.loc[:, ["smiles", "target"]].to_csv(processed_path, index=False)
