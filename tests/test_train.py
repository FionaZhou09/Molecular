import numpy as np
import pandas as pd

from src.train import run_experiment


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
