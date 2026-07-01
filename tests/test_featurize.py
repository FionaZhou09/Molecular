import numpy as np
import pandas as pd
import pytest
import inspect

from src.featurize import (
    DESCRIPTOR_COLUMNS,
    build_feature_matrix,
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


def test_build_feature_matrix_supports_descriptor_features_without_scaling():
    df = pd.DataFrame({"smiles": ["CCO", "c1ccccc1", "CC(=O)O"]})

    features, feature_names = build_feature_matrix(df, "descriptors")
    raw_descriptors = compute_descriptors(df["smiles"].tolist()).to_numpy()

    assert isinstance(features, np.ndarray)
    assert feature_names == DESCRIPTOR_COLUMNS
    assert features.shape == (3, len(DESCRIPTOR_COLUMNS))
    np.testing.assert_allclose(features, raw_descriptors)


def test_build_feature_matrix_supports_fingerprint_features():
    df = pd.DataFrame({"smiles": ["CCO", "c1ccccc1", "CC(=O)O"]})

    features, feature_names = build_feature_matrix(df, "fingerprints")

    assert isinstance(features, np.ndarray)
    assert features.shape == (3, 2048)
    assert feature_names == [f"morgan_{index}" for index in range(2048)]
    assert set(np.unique(features)).issubset({0, 1})


def test_build_feature_matrix_supports_combined_features_in_stable_order():
    df = pd.DataFrame({"smiles": ["CCO", "c1ccccc1", "CC(=O)O"]})

    features, feature_names = build_feature_matrix(df, "combined")
    descriptor_features = compute_descriptors(df["smiles"].tolist()).to_numpy()
    fingerprint_features = compute_morgan_fingerprints(df["smiles"].tolist())

    assert features.shape == (
        3,
        descriptor_features.shape[1] + fingerprint_features.shape[1],
    )
    assert feature_names == DESCRIPTOR_COLUMNS + [
        f"morgan_{index}" for index in range(2048)
    ]
    np.testing.assert_allclose(features[:, : len(DESCRIPTOR_COLUMNS)], descriptor_features)
    np.testing.assert_array_equal(features[:, len(DESCRIPTOR_COLUMNS) :], fingerprint_features)


def test_build_feature_matrix_rejects_unknown_feature_type():
    df = pd.DataFrame({"smiles": ["CCO"]})

    with pytest.raises(ValueError, match="Unsupported feature_type"):
        build_feature_matrix(df, "scaled_descriptors")


def test_build_feature_matrix_does_not_use_standard_scaler():
    source = inspect.getsource(build_feature_matrix)

    assert "StandardScaler" not in source
    assert ".fit(" not in source
    assert ".fit_transform(" not in source
