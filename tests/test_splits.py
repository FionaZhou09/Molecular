import numpy as np
import pandas as pd
import pytest

from src.splits import compute_scaffold, random_split, scaffold_split


def _assert_complete_non_overlapping_split(split_indices, expected_indices):
    train_idx, val_idx, test_idx = split_indices
    split_sets = [set(train_idx), set(val_idx), set(test_idx)]

    assert split_sets[0].isdisjoint(split_sets[1])
    assert split_sets[0].isdisjoint(split_sets[2])
    assert split_sets[1].isdisjoint(split_sets[2])
    assert set().union(*split_sets) == set(expected_indices)


def test_random_split_is_deterministic_for_same_seed():
    df = pd.DataFrame({"smiles": [f"C{i}" for i in range(20)]})

    first = random_split(df, train_size=0.6, val_size=0.2, test_size=0.2, seed=123)
    second = random_split(df, train_size=0.6, val_size=0.2, test_size=0.2, seed=123)

    for first_split, second_split in zip(first, second):
        np.testing.assert_array_equal(first_split, second_split)


def test_random_split_covers_all_rows_once_and_preserves_index_values():
    df = pd.DataFrame(
        {"smiles": [f"C{i}" for i in range(10)]},
        index=[100 + i for i in range(10)],
    )

    train_idx, val_idx, test_idx = random_split(
        df,
        train_size=0.6,
        val_size=0.2,
        test_size=0.2,
        seed=42,
    )

    assert len(train_idx) == 6
    assert len(val_idx) == 2
    assert len(test_idx) == 2
    _assert_complete_non_overlapping_split((train_idx, val_idx, test_idx), df.index)


def test_random_split_rejects_invalid_ratios():
    df = pd.DataFrame({"smiles": ["CCO", "CCN"]})

    with pytest.raises(ValueError, match="must sum to 1.0"):
        random_split(df, train_size=0.8, val_size=0.2, test_size=0.2)


def test_compute_scaffold_groups_same_bemis_murcko_core():
    assert compute_scaffold("c1ccccc1") == compute_scaffold("Cc1ccccc1")
    assert compute_scaffold("c1ccccc1") == compute_scaffold("Oc1ccccc1")
    assert compute_scaffold("C1CCCCC1") != compute_scaffold("c1ccccc1")


def test_compute_scaffold_rejects_invalid_smiles():
    with pytest.raises(ValueError, match="Invalid SMILES"):
        compute_scaffold("not_a_smiles")


def test_scaffold_split_covers_rows_and_keeps_scaffolds_together():
    df = pd.DataFrame(
        {
            "smiles": [
                "c1ccccc1",
                "Cc1ccccc1",
                "Oc1ccccc1",
                "C1CCCCC1",
                "CC1CCCCC1",
                "C1CCNCC1",
                "CCO",
                "CCN",
                "CCCl",
                "CCCBr",
            ]
        },
        index=[10 + i for i in range(10)],
    )

    train_idx, val_idx, test_idx = scaffold_split(
        df,
        train_size=0.6,
        val_size=0.2,
        test_size=0.2,
        seed=7,
    )

    _assert_complete_non_overlapping_split((train_idx, val_idx, test_idx), df.index)

    scaffold_to_split = {}
    for split_name, indices in {
        "train": train_idx,
        "val": val_idx,
        "test": test_idx,
    }.items():
        for index in indices:
            scaffold = compute_scaffold(df.loc[index, "smiles"])
            previous_split = scaffold_to_split.setdefault(scaffold, split_name)
            assert previous_split == split_name


def test_scaffold_split_is_deterministic_for_same_seed():
    df = pd.DataFrame(
        {
            "smiles": [
                "c1ccccc1",
                "Cc1ccccc1",
                "C1CCCCC1",
                "CC1CCCCC1",
                "C1CCNCC1",
                "CCO",
                "CCN",
                "CCCl",
            ]
        }
    )

    first = scaffold_split(df, train_size=0.5, val_size=0.25, test_size=0.25, seed=99)
    second = scaffold_split(df, train_size=0.5, val_size=0.25, test_size=0.25, seed=99)

    for first_split, second_split in zip(first, second):
        np.testing.assert_array_equal(first_split, second_split)
