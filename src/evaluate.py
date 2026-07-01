import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


SUMMARY_GROUP_COLUMNS = ["dataset", "feature_type", "model_key", "split_type"]
SUMMARY_METRIC_COLUMNS = [
    "validation_rmse",
    "validation_mae",
    "validation_r2",
    "test_rmse",
    "test_mae",
    "test_r2",
]


def evaluate_regression(y_true, y_pred) -> dict[str, float]:
    y_true_array = np.asarray(y_true, dtype=float)
    y_pred_array = np.asarray(y_pred, dtype=float)

    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true_array, y_pred_array))),
        "mae": float(mean_absolute_error(y_true_array, y_pred_array)),
        "r2": float(r2_score(y_true_array, y_pred_array)),
    }


def summarize_benchmark_results(results: pd.DataFrame) -> pd.DataFrame:
    grouped = results.groupby(SUMMARY_GROUP_COLUMNS, as_index=False)
    summary = grouped.agg(
        n_seeds=("seed", "nunique"),
        **{
            f"{metric}_mean": (metric, "mean")
            for metric in SUMMARY_METRIC_COLUMNS
        },
        **{
            f"{metric}_std": (metric, "std")
            for metric in SUMMARY_METRIC_COLUMNS
        },
    )

    ordered_columns = SUMMARY_GROUP_COLUMNS + ["n_seeds"]
    for metric in SUMMARY_METRIC_COLUMNS:
        ordered_columns.extend([f"{metric}_mean", f"{metric}_std"])

    return summary.loc[:, ordered_columns]
