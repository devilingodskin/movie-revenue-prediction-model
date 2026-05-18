# Тестовые сценарии веб-сервиса прогнозирования коммерческой успешности фильма

Документ фиксирует результаты end-to-end проверки связки React frontend и FastAPI backend.

Проверяемый backend endpoint:

```text
POST http://127.0.0.1:8000/api/predict
```

Проверяемый frontend:

```text
http://127.0.0.1:5173/
```

Данные сценариев являются условными и используются только для проверки работы веб-сервиса. Они не должны трактоваться как реальные прогнозы для настоящих фильмов.

## Проверяемые поля ответа

Во всех сценариях проверяется наличие следующих полей:

- `predicted_revenue`
- `predicted_profit`
- `roi`
- `payback_ratio`
- `success_category`
- `risk_level`

## Сценарий 1 — высокобюджетный коммерческий фильм

### Цель проверки

Проверить работу сервиса на условном высокобюджетном коммерческом фильме с высоким ожидаемым интересом аудитории.

### Входной JSON

```json
{
  "title": "Scenario 1 High Budget Commercial Film",
  "rating": "PG-13",
  "genre": "Action",
  "year": 2024,
  "score": 7.2,
  "votes": 150000,
  "director": "Christopher Nolan",
  "writer": "Jonathan Nolan",
  "star": "Tom Hardy",
  "country": "United States",
  "budget": 50000000,
  "company": "Warner Bros.",
  "runtime": 120,
  "released": "July 15, 2024"
}
```

### Ожидаемые поля ответа

Ожидается, что API вернет прогнозируемую выручку, прибыль, ROI, коэффициент окупаемости, категорию коммерческой успешности и уровень риска.

### Фактический ответ API

```json
{
  "title": "Scenario 1 High Budget Commercial Film",
  "predicted_revenue": 203410624.0,
  "predicted_profit": 153410624.0,
  "roi": 3.06821248,
  "payback_ratio": 4.06821248,
  "success_category": "высокоуспешный / блокбастер",
  "risk_level": "минимальный"
}
```

### Вывод

Сервис вернул все ожидаемые поля. Для данного условного примера модель отнесла фильм к категории высокоуспешных / блокбастеров с минимальным уровнем риска.

## Сценарий 2 — среднебюджетный фильм

### Цель проверки

Проверить работу сервиса на условном среднебюджетном фильме с умеренными ожидаемыми показателями аудитории.

### Входной JSON

```json
{
  "title": "Scenario 2 Mid Budget Film",
  "rating": "R",
  "genre": "Drama",
  "year": 2022,
  "score": 6.6,
  "votes": 35000,
  "director": "Denis Villeneuve",
  "writer": "Eric Roth",
  "star": "Amy Adams",
  "country": "United States",
  "budget": 18000000,
  "company": "A24",
  "runtime": 105,
  "released": "October 10, 2022"
}
```

### Ожидаемые поля ответа

Ожидается, что API вернет прогнозируемую выручку, прибыль, ROI, коэффициент окупаемости, категорию коммерческой успешности и уровень риска.

### Фактический ответ API

```json
{
  "title": "Scenario 2 Mid Budget Film",
  "predicted_revenue": 29573484.0,
  "predicted_profit": 11573484.0,
  "roi": 0.6429713333333333,
  "payback_ratio": 1.6429713333333333,
  "success_category": "умеренно успешный",
  "risk_level": "средний"
}
```

### Вывод

Сервис вернул все ожидаемые поля. Для данного условного примера прогноз показывает окупаемость бюджета и умеренную коммерческую успешность.

## Сценарий 3 — рискованный фильм с низким потенциалом окупаемости

### Цель проверки

Проверить работу сервиса на условном фильме с высоким бюджетом, низкой ожидаемой оценкой и низким ожидаемым уровнем интереса аудитории.

### Входной JSON

```json
{
  "title": "Scenario 3 Risky Low Potential Film",
  "rating": "Not Rated",
  "genre": "Drama",
  "year": 2024,
  "score": 3.8,
  "votes": 300,
  "director": "Unknown Director",
  "writer": "Unknown Writer",
  "star": "Unknown Actor",
  "country": "United States",
  "budget": 80000000,
  "company": "Independent",
  "runtime": 95,
  "released": "January 20, 2024"
}
```

### Ожидаемые поля ответа

Ожидается, что API вернет прогнозируемую выручку, прибыль, ROI, коэффициент окупаемости, категорию коммерческой успешности и уровень риска.

### Фактический ответ API

```json
{
  "title": "Scenario 3 Risky Low Potential Film",
  "predicted_revenue": 16228347.0,
  "predicted_profit": -63771653.0,
  "roi": -0.7971456625,
  "payback_ratio": 0.2028543375,
  "success_category": "коммерчески неуспешный",
  "risk_level": "высокий"
}
```

### Вывод

Сервис вернул все ожидаемые поля. Для данного условного примера прогнозируемая выручка ниже бюджета, поэтому фильм классифицирован как коммерчески неуспешный с высоким уровнем риска.

## Проверка формул

В API используются следующие формулы:

```text
predicted_profit = predicted_revenue - budget
roi = predicted_profit / budget
payback_ratio = predicted_revenue / budget
```

Также проверяется соотношение:

```text
payback_ratio = roi + 1
```

### Результаты проверки

| Сценарий | Проверка прибыли | Проверка ROI | Проверка payback_ratio | Проверка payback_ratio = roi + 1 |
|---|---:|---:|---:|---:|
| Сценарий 1 | 0.0 | 0.0 | 0.0 | 0.0 |
| Сценарий 2 | 0.0 | 0.0 | 0.0 | 0.0 |
| Сценарий 3 | 0.0 | 0.0 | 0.0 | -2.7755575615628914e-17 |

Значения в таблице показывают разницу между фактическим значением поля и значением, пересчитанным по формуле. В сценарии 3 расхождение для `payback_ratio = roi + 1` находится на уровне машинной погрешности floating-point вычислений и не является логической ошибкой.

## Дополнительные проверки запуска

Проверка backend:

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Проверка frontend:

```bash
cd frontend
npm run dev
```

Проверка сборки frontend:

```bash
cd frontend
npm run build
```

Проверка импорта backend:

```bash
python3 -c "from backend.app.main import app; print(app.title)"
```
