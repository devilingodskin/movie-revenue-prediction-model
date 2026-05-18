# FastAPI Backend

Разработано: **Цветков Артём Денисович**, **СГТУ им. Гагарина Ю.А.**

Backend API для веб-сервиса прогнозирования коммерческой успешности фильма.

Backend не обучает модель. Он загружает готовый production pipeline:

```text
artifacts/movie_revenue_pipeline.joblib
```

Pipeline уже содержит обратное преобразование target, поэтому `predict()` возвращает обычную прогнозируемую кассовую выручку `gross`, а не `log_gross`.

## Установка зависимостей

Из корня проекта:

```bash
python3 -m pip install -r backend/requirements.txt
```

Корень проекта должен оставаться доступным для импорта, потому что joblib pipeline ссылается на:

```text
ml_pipeline.feature_engineering.MovieFeatureEngineer
```

## Запуск

Из корня проекта:

```bash
uvicorn backend.app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Endpoint'ы

- `GET /` — статус сервиса.
- `GET /api/model/info` — metadata модели и feature schema.
- `GET /api/model/metrics` — метрики модели.
- `GET /api/sample-input` — пример входного JSON.
- `POST /api/predict` — прогноз выручки и коммерческой успешности.

## Формулы

```text
predicted_profit = predicted_revenue - budget
roi = predicted_profit / budget
payback_ratio = predicted_revenue / budget
```

## Категории успешности

```text
roi < 0        -> коммерчески неуспешный
0 <= roi < 1  -> умеренно успешный
1 <= roi < 3  -> коммерчески успешный
roi >= 3      -> высокоуспешный / блокбастер
```

## Уровень риска

```text
roi < 0        -> высокий
0 <= roi < 1  -> средний
1 <= roi < 3  -> низкий
roi >= 3      -> минимальный
```

## Проверка импорта

```bash
python3 -c "from backend.app.main import app; print(app.title)"
```
