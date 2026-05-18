"""Prediction service around the exported joblib pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from backend.app.schemas import MovieInput, MoviePredictionResponse


PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
PIPELINE_PATH = ARTIFACTS_DIR / "movie_revenue_pipeline.joblib"
MODEL_INFO_PATH = ARTIFACTS_DIR / "model_info.json"
METRICS_PATH = ARTIFACTS_DIR / "metrics.json"
FEATURE_SCHEMA_PATH = ARTIFACTS_DIR / "feature_schema.json"
SAMPLE_INPUT_PATH = ARTIFACTS_DIR / "sample_input.json"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeError(f"Required artifact is missing: {path.relative_to(PROJECT_ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def _load_pipeline() -> Any:
    if not PIPELINE_PATH.exists():
        raise RuntimeError(
            f"Required model artifact is missing: {PIPELINE_PATH.relative_to(PROJECT_ROOT)}"
        )
    return joblib.load(PIPELINE_PATH)


MODEL_INFO = _load_json(MODEL_INFO_PATH)
METRICS = _load_json(METRICS_PATH)
FEATURE_SCHEMA = _load_json(FEATURE_SCHEMA_PATH)
SAMPLE_INPUT = _load_json(SAMPLE_INPUT_PATH)
PIPELINE = _load_pipeline()

RUSSIAN_VALUE_ALIASES = {
    "rating": {
        "без рейтинга": "Not Rated",
        "не указан": "Not Rated",
        "неизвестно": "Not Rated",
        "для всех": "G",
        "детский": "G",
        "с родителями": "PG",
        "13+": "PG-13",
        "16+": "PG-13",
        "18+": "R",
        "взрослый": "R",
    },
    "genre": {
        "боевик": "Action",
        "приключения": "Adventure",
        "приключенческий": "Adventure",
        "мультфильм": "Animation",
        "анимация": "Animation",
        "биография": "Biography",
        "комедия": "Comedy",
        "криминал": "Crime",
        "драма": "Drama",
        "семейный": "Family",
        "фэнтези": "Fantasy",
        "фантастика": "Sci-Fi",
        "научная фантастика": "Sci-Fi",
        "ужасы": "Horror",
        "хоррор": "Horror",
        "детектив": "Mystery",
        "романтика": "Romance",
        "мелодрама": "Romance",
        "триллер": "Thriller",
        "вестерн": "Western",
    },
    "country": {
        "сша": "United States",
        "соединенные штаты": "United States",
        "соединённые штаты": "United States",
        "америка": "United States",
        "великобритания": "United Kingdom",
        "англия": "United Kingdom",
        "россия": "Russia",
        "рф": "Russia",
        "франция": "France",
        "германия": "Germany",
        "италия": "Italy",
        "испания": "Spain",
        "канада": "Canada",
        "австралия": "Australia",
        "китай": "China",
        "япония": "Japan",
        "южная корея": "South Korea",
        "индия": "India",
        "бразилия": "Brazil",
        "мексика": "Mexico",
    },
}


def _dump_input(movie: MovieInput) -> dict[str, Any]:
    if hasattr(movie, "model_dump"):
        return movie.model_dump()
    return movie.dict()


def _normalize_for_model(column: str, value: Any) -> Any:
    if not isinstance(value, str):
        return value
    normalized_value = value.strip()
    aliases = RUSSIAN_VALUE_ALIASES.get(column, {})
    return aliases.get(normalized_value.casefold(), normalized_value)


def get_model_info() -> dict[str, Any]:
    return {
        "model_info": MODEL_INFO,
        "feature_schema": FEATURE_SCHEMA,
    }


def get_metrics() -> dict[str, Any]:
    return METRICS


def get_sample_input() -> dict[str, Any]:
    return SAMPLE_INPUT


def calculate_success_category(roi: float) -> str:
    if roi < 0:
        return "коммерчески неуспешный"
    if roi < 1:
        return "умеренно успешный"
    if roi < 3:
        return "коммерчески успешный"
    return "высокоуспешный / блокбастер"


def calculate_risk_level(roi: float) -> str:
    if roi < 0:
        return "высокий"
    if roi < 1:
        return "средний"
    if roi < 3:
        return "низкий"
    return "минимальный"


def predict_movie_success(movie: MovieInput) -> MoviePredictionResponse:
    payload = _dump_input(movie)
    model_input_columns = FEATURE_SCHEMA.get("model_input_columns", [])
    model_payload = {
        column: _normalize_for_model(column, payload.get(column))
        for column in model_input_columns
    }
    input_frame = pd.DataFrame([model_payload])

    predicted_revenue = float(PIPELINE.predict(input_frame)[0])
    predicted_revenue = max(predicted_revenue, 0.0)

    budget = float(payload["budget"])
    predicted_profit = predicted_revenue - budget
    roi = predicted_profit / budget
    payback_ratio = predicted_revenue / budget

    return MoviePredictionResponse(
        title=payload.get("title"),
        predicted_revenue=predicted_revenue,
        predicted_profit=predicted_profit,
        roi=roi,
        payback_ratio=payback_ratio,
        success_category=calculate_success_category(roi),
        risk_level=calculate_risk_level(roi),
    )
