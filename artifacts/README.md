# Artifacts

Разработано: **Цветков Артём Денисович**, **СГТУ им. Гагарина Ю.А.**

Папка содержит production-артефакты финальной модели прогнозирования кассовой выручки фильма.

## Файлы

- `movie_revenue_pipeline.joblib` — единый sklearn Pipeline с feature engineering, preprocessing, XGBoost и обратным преобразованием `expm1`.
- `model_info.json` — описание задачи, алгоритма, target и используемого датасета.
- `metrics.json` — метрики качества модели на тестовой выборке.
- `feature_schema.json` — схема входных, категориальных, числовых и неиспользуемых полей.
- `sample_input.json` — пример входного JSON для проверки backend и pipeline.

Backend только загружает эти файлы. Переобучение модели выполняется отдельно через `scripts/train_final_model.py`.
