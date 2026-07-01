import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.splits import scaffold_sets_by_split


def plot_scaffold_counts(
    df: pd.DataFrame,
    train_idx,
    val_idx,
    test_idx,
    ax=None,
):
    if ax is None:
        _, ax = plt.subplots()

    scaffold_sets = scaffold_sets_by_split(df, train_idx, val_idx, test_idx)
    split_names = ["train", "validation", "test"]
    counts = [len(scaffold_sets[split_name]) for split_name in split_names]

    ax.bar(split_names, counts)
    ax.set_xlabel("Split")
    ax.set_ylabel("Unique scaffolds")
    ax.set_title("Scaffold counts by split")
    return ax
