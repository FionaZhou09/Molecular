import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold


def _validate_split_sizes(train_size: float, val_size: float, test_size: float) -> None:
    total = train_size + val_size + test_size
    if not np.isclose(total, 1.0):
        raise ValueError("train_size, val_size, and test_size must sum to 1.0")
    if min(train_size, val_size, test_size) < 0:
        raise ValueError("split sizes must be non-negative")


def _split_counts(n_rows: int, train_size: float, val_size: float) -> tuple[int, int]:
    train_count = int(round(n_rows * train_size))
    val_count = int(round(n_rows * val_size))

    if train_count + val_count > n_rows:
        overflow = train_count + val_count - n_rows
        val_count = max(0, val_count - overflow)

    return train_count, val_count


def random_split(
    df: pd.DataFrame,
    train_size: float = 0.8,
    val_size: float = 0.1,
    test_size: float = 0.1,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    _validate_split_sizes(train_size, val_size, test_size)

    indices = np.asarray(df.index)
    shuffled = indices.copy()
    rng = np.random.default_rng(seed)
    rng.shuffle(shuffled)

    train_count, val_count = _split_counts(len(shuffled), train_size, val_size)
    train_idx = shuffled[:train_count]
    val_idx = shuffled[train_count : train_count + val_count]
    test_idx = shuffled[train_count + val_count :]

    return train_idx, val_idx, test_idx


def compute_scaffold(smiles: str) -> str:
    if not isinstance(smiles, str):
        raise ValueError(f"Invalid SMILES: {smiles!r}")

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")

    return MurckoScaffold.MurckoScaffoldSmiles(mol=mol)


def scaffold_split(
    df: pd.DataFrame,
    train_size: float = 0.8,
    val_size: float = 0.1,
    test_size: float = 0.1,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    _validate_split_sizes(train_size, val_size, test_size)

    scaffold_groups: dict[str, list] = {}
    for row_index, smiles in df["smiles"].items():
        scaffold = compute_scaffold(smiles)
        scaffold_groups.setdefault(scaffold, []).append(row_index)

    rng = np.random.default_rng(seed)
    groups = list(scaffold_groups.values())
    rng.shuffle(groups)
    groups.sort(key=len, reverse=True)

    n_rows = len(df)
    train_target = n_rows * train_size
    val_target = n_rows * val_size

    train_indices = []
    val_indices = []
    test_indices = []

    for group in groups:
        train_gap = train_target - len(train_indices)
        val_gap = val_target - len(val_indices)

        if train_gap >= val_gap and train_gap > 0:
            train_indices.extend(group)
        elif val_gap > 0:
            val_indices.extend(group)
        else:
            test_indices.extend(group)

    return (
        np.asarray(train_indices, dtype=np.asarray(df.index).dtype),
        np.asarray(val_indices, dtype=np.asarray(df.index).dtype),
        np.asarray(test_indices, dtype=np.asarray(df.index).dtype),
    )
