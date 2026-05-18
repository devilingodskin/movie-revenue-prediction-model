"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.schemas import MovieInput, MoviePredictionResponse
from backend.app.services.predictor import (
    get_metrics,
    get_model_info,
    get_sample_input,
    predict_movie_success,
)


app = FastAPI(
    title="Movie Commercial Success Prediction Service",
    description=(
        "Prediction API for movie revenue and commercial success indicators. "
        "Developed by Artem Tsvetkov, Yuri Gagarin State Technical University of Saratov."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "Movie Commercial Success Prediction Service",
        "status": "running",
        "developer": "Цветков Артём Денисович",
        "organization": "СГТУ им. Гагарина Ю.А.",
    }


@app.get("/api/model/info")
def model_info() -> dict:
    return get_model_info()


@app.get("/api/model/metrics")
def model_metrics() -> dict:
    return get_metrics()


@app.get("/api/sample-input")
def sample_input() -> dict:
    return get_sample_input()


@app.post("/api/predict", response_model=MoviePredictionResponse)
def predict(movie: MovieInput) -> MoviePredictionResponse:
    try:
        return predict_movie_success(movie)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check input payload and model artifacts.",
        ) from exc
