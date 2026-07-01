import pandas as pd

from src.config import resolve_project_path
from src.data_loader import get_dataset_config
from src.evaluate import evaluate_regression
from src.featurize import build_feature_matrix
from src.models import create_model
from src.splits import compute_scaffold, random_split, scaffold_split


PREDICTION_COLUMNS = [
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


def _load_processed_dataset(dataset_key: str) -> pd.DataFrame:
    config = get_dataset_config(dataset_key)
    return pd.read_csv(resolve_project_path(config.processed_path))


def _create_split(df: pd.DataFrame, split_type: str, seed: int):
    if split_type == "random":
        return random_split(df, seed=seed)
    if split_type == "scaffold":
        return scaffold_split(df, seed=seed)

    raise ValueError(
        "Unsupported split_type: "
        f"{split_type!r}. Supported: random, scaffold"
    )


def _prefixed_metrics(prefix: str, y_true, y_pred) -> dict[str, float]:
    metrics = evaluate_regression(y_true, y_pred)
    return {f"{prefix}_{metric_name}": value for metric_name, value in metrics.items()}


def _prediction_rows(
    df: pd.DataFrame,
    indices,
    predictions,
    split_name: str,
    dataset_key: str,
    feature_type: str,
    model_key: str,
    split_type: str,
    seed: int,
) -> pd.DataFrame:
    rows = []
    for row_index, prediction in zip(indices, predictions):
        target = float(df.loc[row_index, "target"])
        rows.append(
            {
                "dataset": dataset_key,
                "feature_type": feature_type,
                "model_key": model_key,
                "split_type": split_type,
                "seed": seed,
                "split": split_name,
                "smiles": df.loc[row_index, "smiles"],
                "target": target,
                "prediction": float(prediction),
                "residual": target - float(prediction),
                "scaffold": compute_scaffold(df.loc[row_index, "smiles"]),
            }
        )

    return pd.DataFrame(rows, columns=PREDICTION_COLUMNS)


def run_experiment(
    dataset_key: str,
    feature_type: str,
    model_key: str,
    split_type: str,
    seed: int,
) -> tuple[dict, pd.DataFrame]:
    df = _load_processed_dataset(dataset_key)
    train_idx, validation_idx, test_idx = _create_split(df, split_type, seed)
    features, _ = build_feature_matrix(df, feature_type)
    target = df["target"].to_numpy(dtype=float)

    model = create_model(model_key, feature_type=feature_type, seed=seed)
    model.fit(features[train_idx], target[train_idx])

    validation_predictions = model.predict(features[validation_idx])
    test_predictions = model.predict(features[test_idx])

    result = {
        "dataset": dataset_key,
        "feature_type": feature_type,
        "model_key": model_key,
        "split_type": split_type,
        "seed": seed,
        "train_size": len(train_idx),
        "validation_size": len(validation_idx),
        "test_size": len(test_idx),
    }
    result.update(
        _prefixed_metrics(
            "validation",
            target[validation_idx],
            validation_predictions,
        )
    )
    result.update(_prefixed_metrics("test", target[test_idx], test_predictions))

    predictions = pd.concat(
        [
            _prediction_rows(
                df,
                validation_idx,
                validation_predictions,
                "validation",
                dataset_key,
                feature_type,
                model_key,
                split_type,
                seed,
            ),
            _prediction_rows(
                df,
                test_idx,
                test_predictions,
                "test",
                dataset_key,
                feature_type,
                model_key,
                split_type,
                seed,
            ),
        ],
        ignore_index=True,
    )

    return result, predictions
