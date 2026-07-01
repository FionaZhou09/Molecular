import pandas as pd
import pytest

from src.config import DATASETS, DatasetConfig
from src.data_loader import (
    load_raw_dataset,
    normalize_dataset,
    save_processed_dataset,
    validate_smiles,
)


def test_load_raw_dataset_reads_esol_and_freesolv():
    esol = load_raw_dataset("esol")
    freesolv = load_raw_dataset("freesolv")

    assert len(esol) == 1128
    assert "smiles" in esol.columns
    assert "measured log solubility in mols per litre" in esol.columns

    assert len(freesolv) == 642
    assert list(freesolv.columns) == ["smiles", "y"]


def test_load_raw_dataset_rejects_unknown_key():
    with pytest.raises(KeyError, match="Unknown dataset key"):
        load_raw_dataset("lipophilicity")


def test_normalize_dataset_returns_smiles_and_target_columns_only():
    raw = pd.DataFrame(
        {
            "compound_smiles": ["CCO", "c1ccccc1"],
            "measurement": [-0.1, -2.3],
            "extra": ["ignored", "ignored"],
        }
    )

    normalized = normalize_dataset(raw, "compound_smiles", "measurement")

    assert list(normalized.columns) == ["smiles", "target"]
    assert normalized.to_dict("records") == [
        {"smiles": "CCO", "target": -0.1},
        {"smiles": "c1ccccc1", "target": -2.3},
    ]


def test_normalize_dataset_drops_missing_smiles_or_target_deterministically():
    raw = pd.DataFrame(
        {
            "smiles": ["CCO", None, "CCN", "CCC"],
            "y": [1.0, 2.0, None, 4.0],
        },
        index=[10, 20, 30, 40],
    )

    normalized = normalize_dataset(raw, "smiles", "y")

    assert list(normalized.columns) == ["smiles", "target"]
    assert normalized.to_dict("records") == [
        {"smiles": "CCO", "target": 1.0},
        {"smiles": "CCC", "target": 4.0},
    ]
    assert list(normalized.index) == [0, 1]


def test_validate_smiles_returns_valid_and_invalid_rows_separately():
    normalized = pd.DataFrame(
        {
            "smiles": ["CCO", "not_a_smiles", "c1ccccc1"],
            "target": [1.0, 2.0, 3.0],
        }
    )

    valid_rows, invalid_rows = validate_smiles(normalized)

    assert valid_rows.to_dict("records") == [
        {"smiles": "CCO", "target": 1.0},
        {"smiles": "c1ccccc1", "target": 3.0},
    ]
    assert invalid_rows.to_dict("records") == [
        {"smiles": "not_a_smiles", "target": 2.0},
    ]


def test_save_processed_dataset_writes_only_smiles_and_target(tmp_path, monkeypatch):
    processed_path = tmp_path / "processed" / "tiny.csv"
    monkeypatch.setitem(
        DATASETS,
        "tiny",
        DatasetConfig(
            display_name="Tiny",
            raw_path=tmp_path / "raw.csv",
            processed_path=processed_path,
            source="test fixture",
            expected_row_count=1,
            smiles_column="smiles",
            target_column="y",
            task_type="regression",
        ),
    )
    df = pd.DataFrame(
        {
            "smiles": ["CCO"],
            "target": [1.0],
            "extra": ["do not save"],
        }
    )

    save_processed_dataset("tiny", df)

    saved = pd.read_csv(processed_path)
    assert list(saved.columns) == ["smiles", "target"]
    assert saved.to_dict("records") == [{"smiles": "CCO", "target": 1.0}]
