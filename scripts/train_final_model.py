"""Train and export the production movie revenue prediction pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_squared_log_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml_pipeline.feature_engineering import MovieFeatureEngineer


DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "output.csv"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
PIPELINE_PATH = ARTIFACTS_DIR / "movie_revenue_pipeline.joblib"
METRICS_PATH = ARTIFACTS_DIR / "metrics.json"
MODEL_INFO_PATH = ARTIFACTS_DIR / "model_info.json"
FEATURE_SCHEMA_PATH = ARTIFACTS_DIR / "feature_schema.json"
SAMPLE_INPUT_PATH = ARTIFACTS_DIR / "sample_input.json"

TARGET_COLUMN = "gross"
RAW_INPUT_COLUMNS = [
    "name",
    "rating",
    "genre",
    "year",
    "released",
    "score",
    "votes",
    "director",
    "writer",
    "star",
    "country",
    "budget",
    "gross",
    "company",
    "runtime",
]
CATEGORICAL_FEATURES = MovieFeatureEngineer.categorical_features
NUMERIC_FEATURES = MovieFeatureEngineer.numeric_features
ENGINEERED_FEATURES = MovieFeatureEngineer.engineered_features
UNUSED_COLUMNS = ["name", "released", TARGET_COLUMN]
MODEL_INPUT_COLUMNS = [
    "rating",
    "genre",
    "year",
    "score",
    "votes",
    "director",
    "writer",
    "star",
    "country",
    "budget",
    "company",
    "runtime",
]
OPTIONAL_METADATA_FIELDS = ["title", "name", "released"]


def make_one_hot_encoder() -> OneHotEncoder:
    """Create a version-compatible OneHotEncoder."""
    try:
        return OneHotEncoder(handle_unknown="ignore", min_frequency=5)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore")


def build_pipeline() -> Pipeline:
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", make_one_hot_encoder()),
        ]
    )
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
        ],
        remainder="drop",
    )
    regressor = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        objective="reg:squarederror",
    )
    target_regressor = TransformedTargetRegressor(
        regressor=regressor,
        func=np.log1p,
        inverse_func=np.expm1,
        check_inverse=False,
    )
    return Pipeline(
        steps=[
            ("feature_engineering", MovieFeatureEngineer()),
            ("preprocessor", preprocessor),
            ("model", target_regressor),
        ]
    )


def load_training_data() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH)
    df = df.dropna(subset=["gross", "budget"]).copy()
    df["gross"] = pd.to_numeric(df["gross"], errors="coerce")
    df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
    df = df.dropna(subset=["gross", "budget"])
    df = df[(df["gross"] > 0) & (df["budget"] > 0)].copy()
    return df


def calculate_metrics(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    clipped_predictions = np.clip(y_pred, 0, None)
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
        "msle": float(mean_squared_log_error(y_true, clipped_predictions)),
        "log_r2": float(r2_score(np.log1p(y_true), np.log1p(clipped_predictions))),
        "test_size": 0.2,
        "random_state": 42,
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    df = load_training_data()
    X = df[MODEL_INPUT_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    metrics = calculate_metrics(y_test, y_pred)
    joblib.dump(pipeline, PIPELINE_PATH)

    write_json(METRICS_PATH, metrics)
    write_json(
        MODEL_INFO_PATH,
        {
            "model_name": "XGBoost Regressor",
            "task": "movie_revenue_prediction",
            "business_task": "movie_commercial_success_prediction",
            "target": TARGET_COLUMN,
            "training_target_transform": "log1p",
            "prediction_output": "gross",
            "inverse_transform_inside_pipeline": True,
            "algorithm": "XGBRegressor",
            "dataset": "data/processed/output.csv",
            "final_model": True,
            "selection_reason": (
                "По результатам сравнительного анализа моделей наилучшее качество "
                "прогнозирования на тестовой выборке показала модель XGBoost, "
                "поэтому она была выбрана в качестве основной модели "
                "интеллектуального модуля веб-сервиса."
            ),
        },
    )
    write_json(
        FEATURE_SCHEMA_PATH,
        {
            "raw_input_columns": RAW_INPUT_COLUMNS,
            "model_input_columns": MODEL_INPUT_COLUMNS,
            "required_input_fields": MODEL_INPUT_COLUMNS,
            "optional_metadata_fields": OPTIONAL_METADATA_FIELDS,
            "categorical_features": CATEGORICAL_FEATURES,
            "numeric_features": NUMERIC_FEATURES,
            "engineered_features": ENGINEERED_FEATURES,
            "unused_columns": UNUSED_COLUMNS,
            "target_column": TARGET_COLUMN,
        },
    )
    write_json(
        SAMPLE_INPUT_PATH,
        {
            "title": "Example Action Movie",
            "rating": "PG-13",
            "genre": "Action",
            "year": 2024,
            "released": "July 15, 2024",
            "score": 7.2,
            "votes": 150000,
            "director": "Christopher Nolan",
            "writer": "Jonathan Nolan",
            "star": "Tom Hardy",
            "country": "United States",
            "budget": 50000000,
            "company": "Warner Bros.",
            "runtime": 120,
        },
    )

    print(f"Saved pipeline: {PIPELINE_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Saved metrics: {METRICS_PATH.relative_to(PROJECT_ROOT)}")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
