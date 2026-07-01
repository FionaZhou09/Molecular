import copy
import random

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import torch
from torch import nn
from xgboost import XGBRegressor


MODEL_KEYS = ("ridge", "lasso", "random_forest", "xgboost", "mlp")
FEATURE_TYPES = ("descriptors", "fingerprints", "combined")
SCALED_FEATURE_TYPES = {"descriptors", "combined"}


def _validate_feature_type(feature_type: str) -> None:
    if feature_type not in FEATURE_TYPES:
        supported = ", ".join(FEATURE_TYPES)
        raise ValueError(
            f"Unsupported feature_type: {feature_type!r}. Supported: {supported}"
        )


class MLPRegressorTorch(RegressorMixin, BaseEstimator):
    """Small sklearn-style PyTorch MLP regressor for tabular molecular features."""

    def __init__(
        self,
        hidden_layers=(128, 64),
        dropout: float = 0.1,
        batch_size: int = 32,
        epochs: int = 100,
        learning_rate: float = 0.001,
        seed: int = 42,
        patience: int = 10,
        validation_fraction: float = 0.0,
        min_delta: float = 1e-6,
        weight_decay: float = 0.0,
    ):
        self.hidden_layers = tuple(hidden_layers)
        self.dropout = dropout
        self.batch_size = batch_size
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.seed = seed
        self.patience = patience
        self.validation_fraction = validation_fraction
        self.min_delta = min_delta
        self.weight_decay = weight_decay

    def _set_seed(self) -> None:
        random.seed(self.seed)
        np.random.seed(self.seed)
        torch.manual_seed(self.seed)
        torch.set_num_threads(1)

    def _build_network(self, input_dim: int) -> nn.Sequential:
        layers = []
        current_dim = input_dim
        for hidden_dim in self.hidden_layers:
            layers.append(nn.Linear(current_dim, hidden_dim))
            layers.append(nn.ReLU())
            if self.dropout > 0:
                layers.append(nn.Dropout(self.dropout))
            current_dim = hidden_dim
        layers.append(nn.Linear(current_dim, 1))
        return nn.Sequential(*layers)

    @staticmethod
    def _as_feature_array(X) -> np.ndarray:
        X_array = np.asarray(X, dtype=np.float32)
        if X_array.ndim != 2:
            raise ValueError("X must be a 2D feature matrix")
        return X_array

    @staticmethod
    def _as_target_array(y) -> np.ndarray:
        y_array = np.asarray(y, dtype=np.float32).reshape(-1, 1)
        if y_array.ndim != 2 or y_array.shape[1] != 1:
            raise ValueError("y must be a 1D target array")
        return y_array

    def _train_validation_indices(self, n_samples: int):
        use_validation = 0 < self.validation_fraction < 1 and n_samples >= 3
        if not use_validation:
            return np.arange(n_samples), None

        validation_size = max(1, int(round(n_samples * self.validation_fraction)))
        validation_size = min(validation_size, n_samples - 1)
        rng = np.random.default_rng(self.seed)
        indices = rng.permutation(n_samples)
        return indices[validation_size:], indices[:validation_size]

    def _loss_value(self, X_tensor, y_tensor, criterion) -> float:
        self.model_.eval()
        with torch.no_grad():
            return float(criterion(self.model_(X_tensor), y_tensor).item())

    def fit(self, X_train, y_train):
        X_array = self._as_feature_array(X_train)
        y_array = self._as_target_array(y_train)
        if X_array.shape[0] != y_array.shape[0]:
            raise ValueError("X_train and y_train must contain the same number of rows")

        self._set_seed()
        self.model_ = self._build_network(X_array.shape[1])
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(
            self.model_.parameters(),
            lr=self.learning_rate,
            weight_decay=self.weight_decay,
        )

        train_indices, validation_indices = self._train_validation_indices(X_array.shape[0])
        X_tensor = torch.from_numpy(X_array)
        y_tensor = torch.from_numpy(y_array)
        train_X = X_tensor[train_indices]
        train_y = y_tensor[train_indices]
        validation_X = X_tensor[validation_indices] if validation_indices is not None else None
        validation_y = y_tensor[validation_indices] if validation_indices is not None else None

        self.initial_loss_ = self._loss_value(train_X, train_y, criterion)
        self.loss_history_ = []
        best_loss = float("inf")
        best_state = None
        epochs_without_improvement = 0
        actual_epochs = 0

        for epoch in range(self.epochs):
            self.model_.train()
            generator = torch.Generator().manual_seed(self.seed + epoch)
            permutation = torch.randperm(train_X.shape[0], generator=generator)

            for start in range(0, train_X.shape[0], self.batch_size):
                batch_indices = permutation[start : start + self.batch_size]
                batch_X = train_X[batch_indices]
                batch_y = train_y[batch_indices]

                optimizer.zero_grad()
                loss = criterion(self.model_(batch_X), batch_y)
                loss.backward()
                optimizer.step()

            train_loss = self._loss_value(train_X, train_y, criterion)
            monitor_loss = train_loss
            if validation_X is not None and validation_y is not None:
                monitor_loss = self._loss_value(validation_X, validation_y, criterion)

            self.loss_history_.append(train_loss)
            actual_epochs = epoch + 1

            if monitor_loss < best_loss - self.min_delta:
                best_loss = monitor_loss
                best_state = copy.deepcopy(self.model_.state_dict())
                epochs_without_improvement = 0
            else:
                epochs_without_improvement += 1
                if self.patience and epochs_without_improvement >= self.patience:
                    break

        if best_state is not None:
            self.model_.load_state_dict(best_state)

        self.final_loss_ = self._loss_value(train_X, train_y, criterion)
        self.training_history_ = {
            "initial_loss": self.initial_loss_,
            "final_loss": self.final_loss_,
            "epochs": actual_epochs,
        }
        return self

    def predict(self, X_test):
        if not hasattr(self, "model_"):
            raise ValueError("MLPRegressorTorch must be fitted before calling predict")

        X_array = self._as_feature_array(X_test)
        X_tensor = torch.from_numpy(X_array)
        self.model_.eval()
        with torch.no_grad():
            predictions = self.model_(X_tensor).cpu().numpy().reshape(-1)
        return predictions


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

    if model_key == "mlp":
        params = {"seed": seed}
        params.update(kwargs)
        return MLPRegressorTorch(**params)

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
