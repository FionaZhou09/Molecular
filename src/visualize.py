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
