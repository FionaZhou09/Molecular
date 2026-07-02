from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.visualize import (
    build_chemical_space_dataframe,
    plot_predicted_vs_actual,
    plot_random_vs_scaffold_summary,
    plot_residual_distribution,
    plot_chemical_space,
    save_chemical_space_figure,
    save_prediction_figures,
)


def _sample_predictions():
    return pd.DataFrame(
        {
            "dataset": ["esol", "esol", "esol"],
            "feature_type": ["descriptors", "descriptors", "descriptors"],
            "model_key": ["ridge", "ridge", "ridge"],
            "split_type": ["random", "random", "random"],
            "seed": [0, 0, 0],
            "split": ["test", "test", "test"],
            "smiles": ["CCO", "CC", "CCC"],
            "target": [1.0, 2.0, 3.0],
            "prediction": [1.1, 1.8, 3.2],
            "residual": [-0.1, 0.2, -0.2],
            "scaffold": ["", "", ""],
        }
    )


def test_prediction_plot_helpers_return_labeled_axes():
    predictions = _sample_predictions()

    actual_ax = plot_predicted_vs_actual(
        predictions,
        dataset="esol",
        model_key="ridge",
        split_type="random",
    )
    residual_ax = plot_residual_distribution(
        predictions,
        dataset="esol",
        model_key="ridge",
        split_type="random",
    )

    assert actual_ax.get_xlabel() == "Actual target"
    assert actual_ax.get_ylabel() == "Predicted target"
    assert "ESOL" in actual_ax.get_title()
    assert residual_ax.get_xlabel() == "Residual"
    assert residual_ax.get_ylabel() == "Count"
    plt.close("all")


def test_random_vs_scaffold_summary_plot_returns_axes():
    summary = pd.DataFrame(
        {
            "dataset": ["esol", "esol"],
            "feature_type": ["descriptors", "descriptors"],
            "model_key": ["ridge", "ridge"],
            "split_type": ["random", "scaffold"],
            "test_rmse_mean": [0.9, 1.2],
            "test_rmse_std": [0.1, 0.2],
        }
    )

    ax = plot_random_vs_scaffold_summary(summary)

    assert ax.get_xlabel() == "Dataset"
    assert "Random vs scaffold" in ax.get_title()
    plt.close("all")


def test_save_prediction_figures_writes_non_empty_files(tmp_path):
    outputs = save_prediction_figures(
        _sample_predictions(),
        output_dir=tmp_path,
        combinations=[
            {
                "dataset": "esol",
                "feature_type": "descriptors",
                "model_key": "ridge",
                "split_type": "random",
                "seed": 0,
                "split": "test",
            }
        ],
    )

    assert set(outputs) == {"predicted_vs_actual", "residuals"}
    assert Path(outputs["predicted_vs_actual"][0]).stat().st_size > 0
    assert Path(outputs["residuals"][0]).stat().st_size > 0


def test_chemical_space_dataframe_contains_coordinates_and_split_labels():
    df = pd.DataFrame(
        {
            "smiles": ["CCO", "CCN", "CCC", "CCCl", "c1ccccc1", "CC(=O)O"],
            "target": [0.0, 0.2, 0.4, 0.8, 1.2, 1.4],
        }
    )

    chemical_space = build_chemical_space_dataframe(
        df,
        split_type="random",
        seed=7,
        n_bits=512,
        perplexity=2,
    )

    assert list(chemical_space.columns) == [
        "smiles",
        "target",
        "split",
        "chemical_space_x",
        "chemical_space_y",
    ]
    assert len(chemical_space) == len(df)
    assert set(chemical_space["split"]) <= {"train", "validation", "test"}
    assert chemical_space[["chemical_space_x", "chemical_space_y"]].notna().all().all()


def test_chemical_space_plot_and_save_helpers_write_non_empty_file(tmp_path):
    chemical_space = pd.DataFrame(
        {
            "smiles": ["CCO", "CCN", "CCC"],
            "target": [0.0, 0.2, 0.4],
            "split": ["train", "validation", "test"],
            "chemical_space_x": [0.0, 1.0, 2.0],
            "chemical_space_y": [2.0, 1.0, 0.0],
        }
    )

    ax = plot_chemical_space(chemical_space, dataset="esol", split_type="random")
    assert ax.get_xlabel() == "t-SNE 1"
    assert "ESOL" in ax.get_title()
    plt.close("all")

    df = pd.DataFrame(
        {
            "smiles": ["CCO", "CCN", "CCC", "CCCl", "c1ccccc1", "CC(=O)O"],
            "target": [0.0, 0.2, 0.4, 0.8, 1.2, 1.4],
        }
    )
    output_path = save_chemical_space_figure(
        df,
        dataset="esol",
        split_type="random",
        output_dir=tmp_path,
        seed=7,
        n_bits=512,
        perplexity=2,
    )

    assert Path(output_path).stat().st_size > 0
