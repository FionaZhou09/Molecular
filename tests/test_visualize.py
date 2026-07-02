from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.visualize import (
    plot_predicted_vs_actual,
    plot_random_vs_scaffold_summary,
    plot_residual_distribution,
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
