from pathlib import Path

from src.config import DATASETS, DatasetConfig


def test_mvp_datasets_are_registered():
    assert set(DATASETS) == {"esol", "freesolv"}
    assert all(isinstance(config, DatasetConfig) for config in DATASETS.values())


def test_mvp_datasets_are_regression_tasks():
    for config in DATASETS.values():
        assert config.task_type == "regression"


def test_dataset_metadata_uses_expected_raw_columns_and_paths():
    esol = DATASETS["esol"]
    freesolv = DATASETS["freesolv"]

    assert esol.display_name == "ESOL (Delaney)"
    assert esol.smiles_column == "smiles"
    assert esol.target_column == "measured log solubility in mols per litre"
    assert esol.expected_row_count == 1128
    assert esol.raw_path == Path("data/raw/esol.csv")
    assert esol.processed_path == Path("data/processed/esol.csv")
    assert esol.source

    assert freesolv.display_name == "FreeSolv"
    assert freesolv.smiles_column == "smiles"
    assert freesolv.target_column == "y"
    assert freesolv.expected_row_count == 642
    assert freesolv.raw_path == Path("data/raw/freesolv.csv")
    assert freesolv.processed_path == Path("data/processed/freesolv.csv")
    assert freesolv.source
