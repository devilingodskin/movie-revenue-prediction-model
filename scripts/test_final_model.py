"""Smoke-test the exported movie revenue prediction pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PIPELINE_PATH = PROJECT_ROOT / "artifacts" / "movie_revenue_pipeline.joblib"
SAMPLE_INPUT_PATH = PROJECT_ROOT / "artifacts" / "sample_input.json"


def success_category(roi: float) -> str:
    if roi < 0.0:
        return "коммерчески неуспешный"
    if roi < 1.0:
        return "умеренно успешный"
    if roi < 3.0:
        return "коммерчески успешный"
    return "высокоуспешный / блокбастер"


def risk_level(roi: float) -> str:
    if roi < 0.0:
        return "высокий"
    if roi < 1.0:
        return "средний"
    if roi < 3.0:
        return "низкий"
    return "минимальный"


def main() -> None:
    pipeline = joblib.load(PIPELINE_PATH)
    sample_input = json.loads(SAMPLE_INPUT_PATH.read_text(encoding="utf-8"))
    input_frame = pd.DataFrame([sample_input])

    predicted_revenue = float(pipeline.predict(input_frame)[0])
    budget = float(sample_input["budget"])
    predicted_profit = predicted_revenue - budget
    roi = predicted_profit / budget if budget > 0 else 0.0
    payback_ratio = predicted_revenue / budget if budget > 0 else 0.0

    result = {
        "title": sample_input.get("title") or sample_input.get("name"),
        "predicted_revenue": predicted_revenue,
        "predicted_profit": predicted_profit,
        "roi": roi,
        "payback_ratio": payback_ratio,
        "success_category": success_category(roi),
        "risk_level": risk_level(roi),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
