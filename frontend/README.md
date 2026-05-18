# React Frontend

Разработано: **Цветков Артём Денисович**, **СГТУ им. Гагарина Ю.А.**

React + Vite интерфейс для демонстрации веб-сервиса прогнозирования коммерческой успешности фильма.

## Запуск backend

Из корня проекта:

```bash
uvicorn backend.app.main:app --reload
```

Backend должен быть доступен по адресу:

```text
http://127.0.0.1:8000
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

## Сборка

```bash
npm run build
```

## Пользовательский сценарий

1. Пользователь заполняет параметры фильма по шагам.
2. На финальном шаге проверяет введённые данные.
3. Нажимает `Рассчитать прогноз`.
4. Форма скрывается, открывается отчёт с прогнозом и бизнес-показателями.

## API

Frontend отправляет запрос:

```text
POST http://127.0.0.1:8000/api/predict
```

## Формулы

```text
predicted_profit = predicted_revenue - budget
roi = predicted_profit / budget
payback_ratio = predicted_revenue / budget
```
