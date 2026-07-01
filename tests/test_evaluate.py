import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.evaluate import evaluate_regression


def test_evaluate_regression_matches_sklearn_definitions():
    y_true = np.array([1.0, 2.0, 3.0, 5.0])
    y_pred = np.array([0.5, 2.5, 2.0, 5.5])

    metrics = evaluate_regression(y_true, y_pred)

    assert metrics == {
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
        "mae": mean_absolute_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
    }


def test_evaluate_regression_returns_plain_float_values():
    metrics = evaluate_regression([1.0, 2.0, 3.0], [1.0, 2.5, 2.0])

    assert set(metrics) == {"rmse", "mae", "r2"}
    assert all(isinstance(value, float) for value in metrics.values())
