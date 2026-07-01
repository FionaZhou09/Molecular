import numpy as np
import pandas as pd
import pytest

from src.featurize import (
    DESCRIPTOR_COLUMNS,
    compute_descriptors,
    compute_morgan_fingerprints,
)


def test_compute_descriptors_returns_stable_numeric_columns():
    smiles = ["CCO", "c1ccccc1", "CC(=O)O"]

    descriptors = compute_descriptors(smiles)

    assert isinstance(descriptors, pd.DataFrame)
    assert list(descriptors.columns) == DESCRIPTOR_COLUMNS
    assert descriptors.shape == (3, len(DESCRIPTOR_COLUMNS))
    assert 20 <= len(DESCRIPTOR_COLUMNS) <= 30
    assert all(np.issubdtype(dtype, np.number) for dtype in descriptors.dtypes)
    assert np.isfinite(descriptors.to_numpy()).all()


def test_compute_descriptors_includes_required_descriptor_families():
    required_columns = {
        "molecular_weight",
        "logp",
        "tpsa",
        "h_bond_donors",
        "h_bond_acceptors",
        "rotatable_bonds",
        "ring_count",
        "aromatic_ring_count",
        "formal_charge",
        "fraction_csp3",
        "molar_refractivity",
    }

    assert required_columns.issubset(DESCRIPTOR_COLUMNS)


def test_compute_descriptors_rejects_invalid_smiles():
    with pytest.raises(ValueError, match="Invalid SMILES at index 1"):
        compute_descriptors(["CCO", "not_a_smiles"])


@pytest.mark.parametrize("n_bits", [512, 1024, 2048])
def test_compute_morgan_fingerprints_shape_and_binary_values(n_bits):
    fingerprints = compute_morgan_fingerprints(
        ["CCO", "c1ccccc1", "CC(=O)O"],
        radius=2,
        n_bits=n_bits,
    )

    assert isinstance(fingerprints, np.ndarray)
    assert fingerprints.shape == (3, n_bits)
    assert set(np.unique(fingerprints)).issubset({0, 1})


def test_compute_morgan_fingerprints_rejects_unsupported_bit_count():
    with pytest.raises(ValueError, match="n_bits must be one of"):
        compute_morgan_fingerprints(["CCO"], n_bits=256)


def test_compute_morgan_fingerprints_rejects_invalid_smiles():
    with pytest.raises(ValueError, match="Invalid SMILES at index 1"):
        compute_morgan_fingerprints(["CCO", "not_a_smiles"])
