# Scripts

Разработано: **Цветков Артём Денисович**, **СГТУ им. Гагарина Ю.А.**

Папка содержит воспроизводимые скрипты для production-модели.

## Файлы

- `train_final_model.py` — обучает финальный XGBoost pipeline и сохраняет файлы в `artifacts/`.
- `test_final_model.py` — загружает готовый pipeline и проверяет прогноз на `artifacts/sample_input.json`.

## Запуск

Из корня проекта:

```bash
python3 scripts/train_final_model.py
python3 scripts/test_final_model.py
```

Backend не должен переобучать модель. Он использует уже готовый artifact.
