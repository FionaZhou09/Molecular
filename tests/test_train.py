import numpy as np
import pandas as pd

from src.evaluate import summarize_benchmark_results
from src.train import (
    BENCHMARK_DATASETS,
    BENCHMARK_FEATURE_TYPES,
    BENCHMARK_MODEL_KEYS,
    BENCHMARK_SEEDS,
    BENCHMARK_SPLIT_TYPES,
    build_benchmark_plan,
    run_benchmark_matrix,
    run_experiment,
)


def test_run_esol_ridge_descriptor_experiment_end_to_end():
    result, predictions = run_experiment(
        dataset_key="esol",
        feature_type="descriptors",
        model_key="ridge",
        split_type="random",
        seed=123,
    )

    required_result_keys = {
        "dataset",
        "feature_type",
        "model_key",
        "split_type",
        "seed",
        "validation_rmse",
        "validation_mae",
        "validation_r2",
        "test_rmse",
        "test_mae",
        "test_r2",
        "train_size",
        "validation_size",
        "test_size",
    }
    assert required_result_keys.issubset(result)
    assert result["dataset"] == "esol"
    assert result["feature_type"] == "descriptors"
    assert result["model_key"] == "ridge"
    assert result["split_type"] == "random"
    assert result["seed"] == 123
    assert result["train_size"] > result["validation_size"] > 0
    assert result["test_size"] > 0
    assert pd.DataFrame([result]).shape == (1, len(result))

    required_prediction_columns = [
        "dataset",
        "feature_type",
        "model_key",
        "split_type",
        "seed",
        "split",
        "smiles",
        "target",
        "prediction",
        "residual",
        "scaffold",
    ]
    assert list(predictions.columns) == required_prediction_columns
    assert set(predictions["split"]) == {"validation", "test"}
    assert len(predictions) == result["validation_size"] + result["test_size"]
    assert np.allclose(
        predictions["residual"],
        predictions["target"] - predictions["prediction"],
    )
    assert predictions["scaffold"].notna().all()


def test_run_experiment_rejects_unknown_split_type():
    try:
        run_experiment(
            dataset_key="esol",
            feature_type="descriptors",
            model_key="ridge",
            split_type="temporal",
            seed=123,
        )
    except ValueError as exc:
        assert "Unsupported split_type" in str(exc)
    else:
        raise AssertionError("Expected unknown split type to raise ValueError")


def test_benchmark_plan_defaults_cover_full_mvp_matrix():
    plan = build_benchmark_plan()

    assert len(plan) == (
        len(BENCHMARK_DATASETS)
        * len(BENCHMARK_FEATURE_TYPES)
        * len(BENCHMARK_MODEL_KEYS)
        * len(BENCHMARK_SPLIT_TYPES)
        * len(BENCHMARK_SEEDS)
    )
    assert plan.iloc[0].to_dict() == {
        "dataset": "esol",
        "feature_type": "descriptors",
        "model_key": "ridge",
        "split_type": "random",
        "seed": 0,
    }


def test_benchmark_matrix_smoke_writes_results_and_predictions(tmp_path):
    results_path = tmp_path / "benchmark_results.csv"
    predictions_path = tmp_path / "predictions.csv"

    results, predictions = run_benchmark_matrix(
        datasets=("esol",),
        feature_types=("descriptors",),
        model_keys=("ridge",),
        split_types=("random",),
        seeds=(0,),
        results_path=str(results_path),
        predictions_path=str(predictions_path),
    )

    assert results_path.exists()
    assert predictions_path.exists()
    assert len(results) == 1
    assert len(predictions) == (
        int(results.loc[0, "validation_size"]) + int(results.loc[0, "test_size"])
    )
    assert pd.read_csv(results_path).shape == results.shape
    assert pd.read_csv(predictions_path).shape == predictions.shape


def test_summary_aggregation_computes_mean_and_std_by_experiment_group():
    results = pd.DataFrame(
        [
            {
                "dataset": "esol",
                "feature_type": "descriptors",
                "model_key": "ridge",
                "split_type": "random",
                "seed": 0,
                "validation_rmse": 1.0,
                "validation_mae": 0.5,
                "validation_r2": 0.7,
                "test_rmse": 2.0,
                "test_mae": 1.0,
                "test_r2": 0.2,
            },
            {
                "dataset": "esol",
                "feature_type": "descriptors",
                "model_key": "ridge",
                "split_type": "random",
                "seed": 1,
                "validation_rmse": 3.0,
                "validation_mae": 1.5,
                "validation_r2": 0.9,
                "test_rmse": 4.0,
                "test_mae": 2.0,
                "test_r2": 0.4,
            },
        ]
    )

    summary = summarize_benchmark_results(results)

    assert list(summary.columns) == [
        "dataset",
        "feature_type",
        "model_key",
        "split_type",
        "n_seeds",
        "validation_rmse_mean",
        "validation_rmse_std",
        "validation_mae_mean",
        "validation_mae_std",
        "validation_r2_mean",
        "validation_r2_std",
        "test_rmse_mean",
        "test_rmse_std",
        "test_mae_mean",
        "test_mae_std",
        "test_r2_mean",
        "test_r2_std",
    ]
    row = summary.iloc[0]
    assert row["n_seeds"] == 2
    assert row["test_rmse_mean"] == 3.0
    assert np.isclose(row["test_rmse_std"], np.sqrt(2.0))
