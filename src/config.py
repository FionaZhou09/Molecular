from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DatasetConfig:
    display_name: str
    raw_path: Path
    processed_path: Path
    source: str
    expected_row_count: int
    smiles_column: str
    target_column: str
    task_type: str


DATASETS = {
    "esol": DatasetConfig(
        display_name="ESOL (Delaney)",
        raw_path=Path("data/raw/esol.csv"),
        processed_path=Path("data/processed/esol.csv"),
        source="DeepChem MoleculeNet Delaney/ESOL raw CSV: https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/delaney-processed.csv",
        expected_row_count=1128,
        smiles_column="smiles",
        target_column="measured log solubility in mols per litre",
        task_type="regression",
    ),
    "freesolv": DatasetConfig(
        display_name="FreeSolv",
        raw_path=Path("data/raw/freesolv.csv"),
        processed_path=Path("data/processed/freesolv.csv"),
        source="DeepChem MoleculeNet FreeSolv raw CSV gzip fallback: https://deepchemdata.s3.us-west-1.amazonaws.com/datasets/freesolv.csv.gz",
        expected_row_count=642,
        smiles_column="smiles",
        target_column="y",
        task_type="regression",
    ),
}


def resolve_project_path(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path
