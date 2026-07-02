import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE

from src.featurize import compute_morgan_fingerprints
from src.splits import random_split, scaffold_sets_by_split, scaffold_split


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


def _filter_predictions(
    predictions: pd.DataFrame,
    dataset: str,
    model_key: str,
    split_type: str,
    feature_type: str | None = None,
    seed: int | None = None,
    split: str | None = "test",
) -> pd.DataFrame:
    mask = (
        (predictions["dataset"] == dataset)
        & (predictions["model_key"] == model_key)
        & (predictions["split_type"] == split_type)
    )
    if feature_type is not None:
        mask &= predictions["feature_type"] == feature_type
    if seed is not None:
        mask &= predictions["seed"] == seed
    if split is not None:
        mask &= predictions["split"] == split

    filtered = predictions.loc[mask].copy()
    if filtered.empty:
        raise ValueError(
            "No prediction rows match "
            f"dataset={dataset!r}, model_key={model_key!r}, "
            f"split_type={split_type!r}, feature_type={feature_type!r}, "
            f"seed={seed!r}, split={split!r}"
        )
    return filtered


def plot_predicted_vs_actual(
    predictions: pd.DataFrame,
    dataset: str,
    model_key: str,
    split_type: str,
    feature_type: str | None = None,
    seed: int | None = None,
    split: str | None = "test",
    ax=None,
):
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 5))

    filtered = _filter_predictions(
        predictions,
        dataset=dataset,
        model_key=model_key,
        split_type=split_type,
        feature_type=feature_type,
        seed=seed,
        split=split,
    )
    ax.scatter(
        filtered["target"],
        filtered["prediction"],
        alpha=0.65,
        edgecolors="none",
    )
    min_value = min(filtered["target"].min(), filtered["prediction"].min())
    max_value = max(filtered["target"].max(), filtered["prediction"].max())
    ax.plot([min_value, max_value], [min_value, max_value], color="black", linestyle="--")
    ax.set_xlabel("Actual target")
    ax.set_ylabel("Predicted target")
    title_parts = [dataset.upper(), model_key, split_type]
    if feature_type is not None:
        title_parts.append(feature_type)
    ax.set_title("Predicted vs actual - " + " / ".join(title_parts))
    return ax


def plot_residual_distribution(
    predictions: pd.DataFrame,
    dataset: str,
    model_key: str,
    split_type: str,
    feature_type: str | None = None,
    seed: int | None = None,
    split: str | None = "test",
    ax=None,
):
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 4))

    filtered = _filter_predictions(
        predictions,
        dataset=dataset,
        model_key=model_key,
        split_type=split_type,
        feature_type=feature_type,
        seed=seed,
        split=split,
    )
    ax.hist(filtered["residual"], bins=30, color="#4C78A8", alpha=0.85)
    ax.axvline(0, color="black", linestyle="--")
    ax.set_xlabel("Residual")
    ax.set_ylabel("Count")
    title_parts = [dataset.upper(), model_key, split_type]
    if feature_type is not None:
        title_parts.append(feature_type)
    ax.set_title("Residual distribution - " + " / ".join(title_parts))
    return ax


def plot_random_vs_scaffold_summary(
    summary: pd.DataFrame,
    metric: str = "test_rmse_mean",
    feature_type: str | None = "descriptors",
    model_key: str | None = "ridge",
    ax=None,
):
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 4))

    filtered = summary.copy()
    if feature_type is not None:
        filtered = filtered.loc[filtered["feature_type"] == feature_type]
    if model_key is not None:
        filtered = filtered.loc[filtered["model_key"] == model_key]
    if filtered.empty:
        raise ValueError("No summary rows match the requested filters")

    pivot = filtered.pivot_table(
        index="dataset",
        columns="split_type",
        values=metric,
        aggfunc="mean",
    )
    pivot = pivot.loc[:, [column for column in ["random", "scaffold"] if column in pivot]]
    pivot.plot(kind="bar", ax=ax)
    ax.set_xlabel("Dataset")
    ax.set_ylabel(metric.replace("_", " "))
    ax.set_title("Random vs scaffold benchmark summary")
    ax.legend(title="Split type")
    return ax


def save_prediction_figures(
    predictions: pd.DataFrame,
    output_dir,
    combinations,
) -> dict[str, list[str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {"predicted_vs_actual": [], "residuals": []}

    for config in combinations:
        dataset = config["dataset"]
        model_key = config["model_key"]
        split_type = config["split_type"]
        feature_type = config.get("feature_type")
        seed = config.get("seed")
        split = config.get("split", "test")
        suffix = f"{dataset}_{model_key}_{split_type}"

        actual_path = output_dir / f"predicted_vs_actual_{suffix}.png"
        residual_path = output_dir / f"residuals_{suffix}.png"

        fig, ax = plt.subplots(figsize=(6, 5))
        plot_predicted_vs_actual(
            predictions,
            dataset=dataset,
            model_key=model_key,
            split_type=split_type,
            feature_type=feature_type,
            seed=seed,
            split=split,
            ax=ax,
        )
        fig.tight_layout()
        fig.savefig(actual_path, dpi=160)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(6, 4))
        plot_residual_distribution(
            predictions,
            dataset=dataset,
            model_key=model_key,
            split_type=split_type,
            feature_type=feature_type,
            seed=seed,
            split=split,
            ax=ax,
        )
        fig.tight_layout()
        fig.savefig(residual_path, dpi=160)
        plt.close(fig)

        outputs["predicted_vs_actual"].append(str(actual_path))
        outputs["residuals"].append(str(residual_path))

    return outputs


def _split_assignments(df: pd.DataFrame, split_type: str, seed: int) -> pd.Series:
    if split_type == "random":
        train_idx, val_idx, test_idx = random_split(df, seed=seed)
    elif split_type == "scaffold":
        train_idx, val_idx, test_idx = scaffold_split(df, seed=seed)
    else:
        raise ValueError(
            f"Unsupported split_type: {split_type!r}. Supported: random, scaffold"
        )

    assignments = pd.Series(index=df.index, dtype=object)
    assignments.loc[train_idx] = "train"
    assignments.loc[val_idx] = "validation"
    assignments.loc[test_idx] = "test"
    return assignments


def _bounded_perplexity(n_samples: int, requested_perplexity: int) -> int:
    if n_samples < 3:
        raise ValueError("At least three rows are required for t-SNE chemical space")
    return max(1, min(requested_perplexity, n_samples - 1))


def build_chemical_space_dataframe(
    df: pd.DataFrame,
    split_type: str,
    seed: int = 42,
    n_bits: int = 512,
    perplexity: int = 30,
) -> pd.DataFrame:
    fingerprints = compute_morgan_fingerprints(df["smiles"].tolist(), n_bits=n_bits)
    tsne = TSNE(
        n_components=2,
        random_state=seed,
        perplexity=_bounded_perplexity(len(df), perplexity),
        init="random",
        learning_rate="auto",
    )
    coordinates = tsne.fit_transform(fingerprints.astype(np.float32))
    assignments = _split_assignments(df, split_type=split_type, seed=seed)

    return pd.DataFrame(
        {
            "smiles": df["smiles"].to_numpy(),
            "target": df["target"].to_numpy(dtype=float),
            "split": assignments.to_numpy(),
            "chemical_space_x": coordinates[:, 0],
            "chemical_space_y": coordinates[:, 1],
        }
    )


def plot_chemical_space(
    chemical_space: pd.DataFrame,
    dataset: str,
    split_type: str,
    ax=None,
):
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 5))

    colors = {"train": "#4C78A8", "validation": "#F58518", "test": "#54A24B"}
    for split_name in ["train", "validation", "test"]:
        rows = chemical_space.loc[chemical_space["split"] == split_name]
        if rows.empty:
            continue
        ax.scatter(
            rows["chemical_space_x"],
            rows["chemical_space_y"],
            label=split_name,
            alpha=0.7,
            s=24,
            color=colors[split_name],
            edgecolors="none",
        )

    ax.set_xlabel("t-SNE 1")
    ax.set_ylabel("t-SNE 2")
    ax.set_title(f"Chemical space - {dataset.upper()} / {split_type}")
    ax.legend(title="Split")
    return ax


def save_chemical_space_figure(
    df: pd.DataFrame,
    dataset: str,
    split_type: str,
    output_dir,
    seed: int = 42,
    n_bits: int = 512,
    perplexity: int = 30,
) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    chemical_space = build_chemical_space_dataframe(
        df,
        split_type=split_type,
        seed=seed,
        n_bits=n_bits,
        perplexity=perplexity,
    )
    output_path = output_dir / f"chemical_space_{dataset}_{split_type}.png"

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    plot_chemical_space(
        chemical_space,
        dataset=dataset,
        split_type=split_type,
        ax=ax,
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
    return str(output_path)
