# Data

Разработано: **Цветков Артём Денисович**, **СГТУ им. Гагарина Ю.А.**

Папка содержит основной рабочий датасет проекта.

## Файлы

- `raw/movies.csv` — исходный датасет Movie Industry до финальной очистки.
- `processed/output.csv` — очищенный датасет, используемый для production-обучения.

## Схема `output.csv`

```text
name, rating, genre, year, released, score, votes,
director, writer, star, country, budget, gross, company, runtime
```

## Назначение колонок

- `gross` — целевая переменная, кассовая выручка фильма.
- `budget` — бюджет фильма.
- `score`, `votes` — признаки из исторических данных.
- `name`, `released` — в production-модели не используются как основные ML-признаки.

## Важно

`output.csv` не нужно изменять вручную при обычном запуске проекта. Обучение production-модели выполняется скриптом:

```bash
python3 scripts/train_final_model.py
```
