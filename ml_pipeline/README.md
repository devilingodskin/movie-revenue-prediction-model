# ML Pipeline

Разработано: **Цветков Артём Денисович**, **СГТУ им. Гагарина Ю.А.**

Папка содержит код production-слоя машинного обучения.

## Файлы

- `feature_engineering.py` — sklearn-compatible transformer `MovieFeatureEngineer`.
- `__init__.py` — делает папку Python-пакетом.

`MovieFeatureEngineer` используется внутри сохранённого `artifacts/movie_revenue_pipeline.joblib`. Поэтому при запуске backend корень проекта должен быть доступен для импорта.
