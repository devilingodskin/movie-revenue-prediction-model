"""Feature engineering for the production movie revenue model."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class MovieFeatureEngineer(BaseEstimator, TransformerMixin):
    """Create stable numeric features from raw movie metadata.

    The transformer stores train-set thresholds in ``fit`` so single-row
    production predictions do not recalculate quantiles from the request.
    """

    categorical_features = [
        "rating",
        "genre",
        "director",
        "writer",
        "star",
        "country",
        "company",
    ]

    numeric_source_features = ["runtime", "score", "year", "votes", "budget"]

    engineered_features = [
        "log_budget",
        "budget_vote_ratio",
        "budget_runtime_ratio",
        "budget_score_ratio",
        "vote_score_ratio",
        "budget_year_ratio",
        "vote_year_ratio",
        "score_runtime_ratio",
        "budget_per_minute",
        "votes_per_year",
        "is_recent",
        "is_high_budget",
        "is_high_votes",
        "is_high_score",
    ]

    numeric_features = [
        "runtime",
        "score",
        "year",
        "votes",
        *engineered_features,
    ]

    def fit(self, X: pd.DataFrame, y: object = None) -> "MovieFeatureEngineer":
        df = self._as_dataframe(X)
        numeric = self._coerce_numeric(df, self.numeric_source_features)

        log_budget = np.log1p(numeric["budget"].clip(lower=0))
        self.min_year_ = self._safe_stat(numeric["year"], "min", default=0.0)
        self.recent_year_threshold_ = self._safe_stat(
            numeric["year"], "quantile", default=self.min_year_, quantile=0.75
        )
        self.high_budget_threshold_ = self._safe_stat(
            log_budget, "quantile", default=0.0, quantile=0.75
        )
        self.high_votes_threshold_ = self._safe_stat(
            numeric["votes"], "quantile", default=0.0, quantile=0.75
        )
        self.high_score_threshold_ = self._safe_stat(
            numeric["score"], "quantile", default=0.0, quantile=0.75
        )
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._ensure_fitted()
        df = self._as_dataframe(X).copy()

        for column in self.categorical_features:
            if column not in df.columns:
                df[column] = pd.NA

        numeric = self._coerce_numeric(df, self.numeric_source_features)
        for column in self.numeric_source_features:
            df[column] = numeric[column]

        budget = numeric["budget"]
        votes = numeric["votes"]
        runtime = numeric["runtime"]
        score = numeric["score"]
        year = numeric["year"]

        df["log_budget"] = np.log1p(budget.clip(lower=0))
        df["budget_vote_ratio"] = self._safe_divide(budget, votes + 1)
        df["budget_runtime_ratio"] = self._safe_divide(budget, runtime + 1)
        df["budget_score_ratio"] = self._safe_divide(df["log_budget"], score + 1)
        df["vote_score_ratio"] = self._safe_divide(votes, score + 1)
        df["budget_year_ratio"] = self._safe_divide(
            df["log_budget"], year - self.min_year_ + 1
        )
        df["vote_year_ratio"] = self._safe_divide(votes, year - self.min_year_ + 1)
        df["score_runtime_ratio"] = self._safe_divide(score, runtime + 1)
        df["budget_per_minute"] = self._safe_divide(budget, runtime + 1)
        df["votes_per_year"] = self._safe_divide(votes, year - self.min_year_ + 1)
        df["is_recent"] = (year >= self.recent_year_threshold_).astype(float)
        df["is_high_budget"] = (
            df["log_budget"] >= self.high_budget_threshold_
        ).astype(float)
        df["is_high_votes"] = (votes >= self.high_votes_threshold_).astype(float)
        df["is_high_score"] = (score >= self.high_score_threshold_).astype(float)

        return df[[*self.categorical_features, *self.numeric_features]]

    @staticmethod
    def _as_dataframe(X: pd.DataFrame) -> pd.DataFrame:
        if isinstance(X, pd.DataFrame):
            return X
        return pd.DataFrame(X)

    @staticmethod
    def _coerce_numeric(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
        numeric = pd.DataFrame(index=df.index)
        for column in columns:
            if column in df.columns:
                numeric[column] = pd.to_numeric(df[column], errors="coerce")
            else:
                numeric[column] = np.nan
        return numeric

    @staticmethod
    def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
        denominator = denominator.replace([np.inf, -np.inf], np.nan)
        valid_denominator = denominator.abs() > np.finfo(float).eps
        result = numerator.where(valid_denominator) / denominator.where(valid_denominator)
        return result.replace([np.inf, -np.inf], np.nan)

    @staticmethod
    def _safe_stat(
        series: pd.Series,
        method: str,
        default: float,
        quantile: float | None = None,
    ) -> float:
        clean = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
        clean = clean.dropna()
        if clean.empty:
            return default
        if method == "min":
            value = clean.min()
        elif method == "quantile" and quantile is not None:
            value = clean.quantile(quantile)
        else:
            value = default
        if pd.isna(value):
            return default
        return float(value)

    def _ensure_fitted(self) -> None:
        required_attributes = [
            "min_year_",
            "recent_year_threshold_",
            "high_budget_threshold_",
            "high_votes_threshold_",
            "high_score_threshold_",
        ]
        missing = [
            attribute
            for attribute in required_attributes
            if not hasattr(self, attribute)
        ]
        if missing:
            raise RuntimeError(
                "MovieFeatureEngineer must be fitted before transform is called."
            )
