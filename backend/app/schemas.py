"""Pydantic schemas for the movie prediction API."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class MovieInput(BaseModel):
    """Input payload for movie revenue prediction."""

    title: Optional[str] = Field(default=None, description="Movie title metadata.")
    rating: str
    genre: str
    year: int
    score: float
    votes: int
    director: str
    writer: str
    star: str
    country: str
    budget: float = Field(
        ge=300_000,
        description="Movie budget in USD. Values below 300,000 are outside the reliable range of the current model.",
    )
    company: str
    runtime: float = Field(gt=0)
    released: Optional[str] = Field(
        default=None,
        description="Release date metadata; not used by the production model.",
    )


class MoviePredictionResponse(BaseModel):
    """Prediction output with commercial success indicators."""

    title: Optional[str]
    predicted_revenue: float
    predicted_profit: float
    roi: float
    payback_ratio: float
    success_category: str
    risk_level: str


ModelInfoResponse = dict[str, Any]
