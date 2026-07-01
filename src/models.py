from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor


MODEL_KEYS = ("ridge", "lasso", "random_forest", "xgboost")
FEATURE_TYPES = ("descriptors", "fingerprints", "combined")
SCALED_FEATURE_TYPES = {"descriptors", "combined"}


def _validate_feature_type(feature_type: str) -> None:
    if feature_type not in FEATURE_TYPES:
        supported = ", ".join(FEATURE_TYPES)
        raise ValueError(
            f"Unsupported feature_type: {feature_type!r}. Supported: {supported}"
        )


def _create_estimator(model_key: str, seed: int, **kwargs):
    if model_key == "ridge":
        return Ridge(**kwargs)

    if model_key == "lasso":
        params = {"random_state": seed, "max_iter": 10000}
        params.update(kwargs)
        return Lasso(**params)

    if model_key == "random_forest":
        params = {"random_state": seed, "n_estimators": 100, "n_jobs": 1}
        params.update(kwargs)
        return RandomForestRegressor(**params)

    if model_key == "xgboost":
        params = {
            "random_state": seed,
            "objective": "reg:squarederror",
            "n_estimators": 100,
            "n_jobs": 1,
        }
        params.update(kwargs)
        return XGBRegressor(**params)

    supported = ", ".join(MODEL_KEYS)
    raise ValueError(f"Unsupported model_key: {model_key!r}. Supported: {supported}")


def create_model(model_key: str, feature_type: str, seed: int = 42, **kwargs):
    _validate_feature_type(feature_type)
    estimator = _create_estimator(model_key, seed, **kwargs)

    if feature_type in SCALED_FEATURE_TYPES:
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", estimator),
            ]
        )

    return estimator
