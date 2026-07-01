import numpy as np
import pytest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.models import MODEL_KEYS, MLPRegressorTorch, create_model


def _tiny_regression_data():
    X = np.array(
        [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [2.0, 1.0, 0.0],
            [3.0, 0.0, 1.0],
            [4.0, 1.0, 0.0],
            [5.0, 0.0, 1.0],
        ],
        dtype=float,
    )
    y = np.array([0.1, 1.2, 1.9, 3.1, 4.2, 4.9], dtype=float)
    return X, y


def _model_kwargs(model_key):
    if model_key == "mlp":
        return {
            "hidden_layers": (8,),
            "dropout": 0.0,
            "batch_size": 3,
            "epochs": 120,
            "learning_rate": 0.05,
            "patience": 30,
        }
    if model_key == "xgboost":
        return {"n_estimators": 5, "max_depth": 2, "verbosity": 0}
    if model_key == "random_forest":
        return {"n_estimators": 5, "max_depth": 3}
    if model_key == "lasso":
        return {"alpha": 0.01, "max_iter": 5000}
    if model_key == "ridge":
        return {"alpha": 1.0}
    return {}


def test_model_registry_keys_are_stable():
    assert MODEL_KEYS == ("ridge", "lasso", "random_forest", "xgboost", "mlp")


@pytest.mark.parametrize("model_key", MODEL_KEYS)
def test_create_model_returns_fit_predict_model(model_key):
    X, y = _tiny_regression_data()
    model = create_model(
        model_key,
        feature_type="fingerprints",
        seed=123,
        **_model_kwargs(model_key),
    )

    model.fit(X, y)
    predictions = model.predict(X)

    assert hasattr(model, "fit")
    assert hasattr(model, "predict")
    assert predictions.shape == (len(y),)
    assert np.isfinite(predictions).all()


@pytest.mark.parametrize("feature_type", ["descriptors", "combined"])
def test_descriptor_like_features_use_train_time_standard_scaling(feature_type):
    model = create_model("ridge", feature_type=feature_type, seed=123)

    assert isinstance(model, Pipeline)
    assert isinstance(model.named_steps["scaler"], StandardScaler)
    assert "model" in model.named_steps


def test_fingerprint_features_do_not_use_standard_scaling():
    model = create_model("ridge", feature_type="fingerprints", seed=123)

    assert not isinstance(model, Pipeline)
    assert not isinstance(model, StandardScaler)


def test_random_state_is_applied_to_seeded_models():
    rf = create_model("random_forest", feature_type="fingerprints", seed=123)
    xgb = create_model(
        "xgboost",
        feature_type="fingerprints",
        seed=123,
        n_estimators=5,
        verbosity=0,
    )

    assert rf.random_state == 123
    assert xgb.random_state == 123


def test_mlp_training_reduces_loss_on_tiny_dataset():
    X, y = _tiny_regression_data()
    model = MLPRegressorTorch(
        hidden_layers=(16,),
        dropout=0.0,
        batch_size=3,
        epochs=150,
        learning_rate=0.05,
        seed=123,
        patience=40,
    )

    model.fit(X, y)
    predictions = model.predict(X)

    assert predictions.shape == (len(y),)
    assert np.isfinite(predictions).all()
    assert model.training_history_["final_loss"] < model.training_history_["initial_loss"]


def test_mlp_seed_is_stored_for_reproducible_training():
    model = create_model(
        "mlp",
        feature_type="fingerprints",
        seed=123,
        hidden_layers=(8,),
        epochs=5,
    )

    assert model.seed == 123


def test_mlp_descriptor_pipeline_fits_and_predicts():
    X, y = _tiny_regression_data()
    model = create_model(
        "mlp",
        feature_type="descriptors",
        seed=123,
        hidden_layers=(8,),
        dropout=0.0,
        batch_size=3,
        epochs=80,
        learning_rate=0.05,
        patience=20,
    )

    model.fit(X, y)
    predictions = model.predict(X)

    assert predictions.shape == (len(y),)
    assert np.isfinite(predictions).all()


def test_create_model_rejects_unknown_model_key():
    with pytest.raises(ValueError, match="Unsupported model_key"):
        create_model("svm", feature_type="fingerprints", seed=123)


def test_create_model_rejects_unknown_feature_type():
    with pytest.raises(ValueError, match="Unsupported feature_type"):
        create_model("ridge", feature_type="graphs", seed=123)
