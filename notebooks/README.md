# Ноутбуки проекта

Разработано: **Цветков Артём Денисович**, **СГТУ им. Гагарина Ю.А.**

Ноутбуки подготовлены как демонстрационный исследовательский маршрут для магистерской работы. Они не изменяют основные датасеты, backend, frontend и production-артефакты.

Рекомендуемый порядок запуска:

1. `00_project_overview.ipynb` — обзор проекта, бизнес-постановка, формулы и маршрут исследования.
2. `01_dataset_analysis.ipynb` — первичный анализ основного датасета, пропуски, распределения, страны, жанры, ROI.
3. `02_feature_engineering_and_target.ipynb` — целевая переменная `gross`, логарифмирование `log1p`, признаки и schema production-модели.
4. `03_model_comparison.ipynb` — сравнение нескольких моделей и объяснение выбора XGBoost.
5. `04_production_pipeline_demo.ipynb` — загрузка готового pipeline, прогноз, бизнес-метрики и batch-пример.
6. `05_dataset_preparation_pipeline.ipynb` — воспроизводимое объяснение подготовки `output.csv` из `movies.csv`.
7. `06_final_model_training_walkthrough.ipynb` — пошаговое обучение финальной XGBoost-модели без сохранения артефактов.
8. `07_backend_api_demo.ipynb` — проверка FastAPI backend через `TestClient`.
9. `08_e2e_testing_and_scenarios.ipynb` — end-to-end сценарии и проверка формул.
10. `09_limitations_and_russian_dataset_extension.ipynb` — ограничения текущего датасета и план расширения под российские фильмы.

Для запуска нужны зависимости из корневого `requirements.txt` и backend-зависимости из `backend/requirements.txt`.
