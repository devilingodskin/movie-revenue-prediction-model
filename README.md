# Прогнозирование коммерческой успешности фильма

Веб-сервис для прогнозирования кассовой выручки фильма и оценки его коммерческой успешности.

Разработано: **Цветков Артём Денисович**.  
Организация: **СГТУ им. Гагарина Ю.А.**  
Направление: **М-ПИНФ-21**.  
Тема магистерской работы: **«Разработка веб-сервиса для прогнозирования успешности продуктов киноиндустрии»**.

## Назначение проекта

Проект решает задачу прогнозирования коммерческого успеха фильма. Основная ML-задача — регрессия кассовой выручки:

```text
target = gross
```

После прогноза выручки сервис рассчитывает:

```text
predicted_profit = predicted_revenue - budget
roi = predicted_profit / budget
payback_ratio = predicted_revenue / budget
```

Категории коммерческой успешности:

```text
roi < 0        -> коммерчески неуспешный
0 <= roi < 1  -> умеренно успешный
1 <= roi < 3  -> коммерчески успешный
roi >= 3      -> высокоуспешный / блокбастер
```

## Архитектура

```text
movie-revenue-prediction/
├── artifacts/          # сохранённая production-модель и JSON-метаданные
├── backend/            # FastAPI backend для prediction API
├── data/
│   ├── raw/            # исходный датасет
│   └── processed/      # очищенный датасет для обучения
├── docs/               # документация, тестовые сценарии, русская статья
├── frontend/           # React + Vite пользовательский интерфейс
├── ml_pipeline/        # feature engineering для sklearn Pipeline
├── notebooks/          # исследовательские ноутбуки для магистерской
├── scripts/            # обучение и проверка production pipeline
└── archive/            # архивные прототипы и исторические материалы
```

Актуальные рабочие компоненты находятся в `artifacts/`, `backend/`, `frontend/`, `ml_pipeline/`, `scripts/`, `notebooks/` и `data/`. Архивные материалы вынесены в `archive/`, чтобы не смешивать старые эксперименты с production-слоем.

## Основной датасет

Рабочий датасет:

```text
data/processed/output.csv
```

Колонки:

```text
name, rating, genre, year, released, score, votes,
director, writer, star, country, budget, gross, company, runtime
```

Особенности:

- `gross` — целевая переменная;
- `budget` — ключевой бизнес-признак;
- `score` и `votes` присутствуют в обучающем датасете, но в пользовательской форме не запрашиваются напрямую;
- текущий датасет в основном описывает зарубежный рынок, поэтому для российского рынка нужен отдельный набор данных.

## Production-модель

Финальная модель:

```text
XGBoost Regressor
```

Файл:

```text
artifacts/movie_revenue_pipeline.joblib
```

Pipeline включает:

1. `MovieFeatureEngineer`;
2. `ColumnTransformer`;
3. `OneHotEncoder(handle_unknown="ignore")`;
4. `SimpleImputer`;
5. `XGBRegressor`;
6. `TransformedTargetRegressor` с `log1p` и `expm1`.

Важно: `pipeline.predict()` возвращает обычную прогнозируемую выручку `gross`, а не `log_gross`.

## Запуск backend

Из корня проекта:

```bash
uvicorn backend.app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Основной endpoint:

```text
POST http://127.0.0.1:8000/api/predict
```

## Запуск frontend

```bash
cd frontend
npm install
npm run dev
```

Открыть:

```text
http://127.0.0.1:5173/
```

Пользователь заполняет форму по шагам, проверяет введённые данные, нажимает `Рассчитать прогноз`, после чего открывается отчёт.

## Запуск через Docker

На Windows, macOS и Linux удобнее запускать проект через Docker Desktop:

```bash
docker compose up --build
```

После запуска открыть:

```text
http://127.0.0.1:5173/
```

Backend будет доступен отдельно:

```text
http://127.0.0.1:8000/docs
```

Остановка контейнеров:

```bash
docker compose down
```

Если используется старая версия Docker Compose, команда может быть такой:

```bash
docker-compose up --build
```

## Обучение production pipeline

Обучение и экспорт модели:

```bash
python3 scripts/train_final_model.py
```

Проверка сохранённой модели:

```bash
python3 scripts/test_final_model.py
```

Эти команды создают и проверяют файлы в `artifacts/`.

## Ноутбуки

Исследовательские материалы находятся в `notebooks/`. Рекомендуемый порядок:

1. `00_project_overview.ipynb`
2. `01_dataset_analysis.ipynb`
3. `02_feature_engineering_and_target.ipynb`
4. `03_model_comparison.ipynb`
5. `04_production_pipeline_demo.ipynb`
6. `05_dataset_preparation_pipeline.ipynb`
7. `06_final_model_training_walkthrough.ipynb`
8. `07_backend_api_demo.ipynb`
9. `08_e2e_testing_and_scenarios.ipynb`
10. `09_limitations_and_russian_dataset_extension.ipynb`

## Документация

Полезные материалы:

- `docs/project_structure.md` — описание структуры проекта;
- `docs/test_scenarios.md` — end-to-end сценарии проверки;
- `docs/paper_ru.md` — русская статья-описание проекта для магистерской работы.

## Проверки

Backend:

```bash
python3 -m compileall backend ml_pipeline scripts
python3 -c "from backend.app.main import app; print(app.title)"
```

Frontend:

```bash
cd frontend
npm run build
```

## Ограничения

- Текущий датасет почти не содержит российских фильмов.
- Модель обучена на исторических данных 1980–2020 годов.
- Экстремально маленькие бюджеты ограничены в API, чтобы не получать бессмысленную экстраполяцию.
- Для полноценного российского рынка рекомендуется собрать отдельный датасет российских фильмов и обучить отдельную версию модели.
