import { useMemo, useState } from "react";

export const INITIAL_FORM_VALUES = {
  title: "",
  rating: "",
  genre: "",
  year: "",
  director: "",
  writer: "",
  star: "",
  country: "",
  budget: "",
  company: "",
  runtime: "",
  released: "",
};

const FORM_FIELDS = [
  {
    group: "Фильм",
    name: "title",
    label: "Как называется фильм?",
    shortLabel: "Название",
    type: "text",
    optional: true,
    hint: "Можно написать на русском. Название нужно только для результата.",
  },
  {
    group: "Фильм",
    name: "rating",
    label: "Какой возрастной рейтинг у фильма?",
    shortLabel: "Рейтинг",
    type: "select",
  },
  {
    group: "Фильм",
    name: "genre",
    label: "Какой основной жанр?",
    shortLabel: "Жанр",
    type: "text",
    hint: "Например: Боевик, Драма, Комедия, Фантастика.",
  },
  {
    group: "Фильм",
    name: "year",
    label: "В каком году выходит фильм?",
    shortLabel: "Год",
    type: "number",
    min: 1900,
    max: 2100,
    hint: "Укажите год выхода или планируемого релиза.",
  },
  {
    group: "Фильм",
    name: "released",
    label: "Когда планируется релиз?",
    shortLabel: "Дата релиза",
    type: "text",
    optional: true,
    hint: "Можно оставить пустым. Например: 15 июля 2024.",
  },
  {
    group: "Проект",
    name: "budget",
    label: "Какой бюджет фильма?",
    shortLabel: "Бюджет",
    type: "number",
    min: 300000,
    minMessage: "Для текущей модели укажите бюджет не ниже $300 000.",
    hint: "Введите бюджет в долларах США. Минимум для расчёта: $300 000.",
  },
  {
    group: "Проект",
    name: "runtime",
    label: "Какая длительность фильма?",
    shortLabel: "Длительность",
    type: "number",
    min: 1,
    hint: "Укажите длительность в минутах.",
  },
  {
    group: "Команда",
    name: "director",
    label: "Кто режиссёр?",
    shortLabel: "Режиссёр",
    type: "text",
    hint: "Можно написать на русском.",
  },
  {
    group: "Команда",
    name: "writer",
    label: "Кто сценарист?",
    shortLabel: "Сценарист",
    type: "text",
    hint: "Укажите основного сценариста.",
  },
  {
    group: "Команда",
    name: "star",
    label: "Кто ведущий актёр?",
    shortLabel: "Ведущий актёр",
    type: "text",
    hint: "Укажите ключевого актёра или актрису.",
  },
  {
    group: "Производство",
    name: "country",
    label: "Какая страна производства?",
    shortLabel: "Страна",
    type: "text",
    hint: "Например: США, Россия, Великобритания.",
  },
  {
    group: "Производство",
    name: "company",
    label: "Какая производственная компания?",
    shortLabel: "Компания",
    type: "text",
    hint: "Укажите студию или компанию-производителя.",
  },
];

const RATING_OPTIONS = [
  "G",
  "PG",
  "PG-13",
  "R",
  "NC-17",
  "Not Rated",
  "18+",
  "16+",
  "13+",
  "Без рейтинга",
];

function validateField(field, value) {
  if (field.optional && String(value ?? "").trim() === "") {
    return "";
  }

  if (!field.optional && String(value ?? "").trim() === "") {
    return "Заполните это поле, чтобы продолжить.";
  }

  if (field.type === "number") {
    const numberValue = Number(value);
    if (!Number.isFinite(numberValue)) {
      return "Введите число.";
    }
    if (field.min !== undefined && numberValue < field.min) {
      return field.minMessage || `Минимальное значение: ${field.min}.`;
    }
    if (field.max !== undefined && numberValue > field.max) {
      return `Максимальное значение: ${field.max}.`;
    }
  }

  return "";
}

function formatReviewValue(field, value) {
  if (value === "" || value === null || value === undefined) {
    return "Не указано";
  }
  if (field.name === "budget") {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(Number(value));
  }
  if (field.name === "runtime") {
    return `${value} мин.`;
  }
  return String(value);
}

function ActiveField({ field, value, error, onFieldChange }) {
  const inputId = `movie-${field.name}`;
  const commonProps = {
    id: inputId,
    name: field.name,
    value,
    autoFocus: true,
    required: !field.optional,
    onChange: (event) => onFieldChange(field.name, event.target.value),
  };

  return (
    <label className="single-field" htmlFor={inputId}>
      <span>
        {field.label}
        {field.optional ? <em>необязательно</em> : null}
      </span>
      {field.type === "select" ? (
        <select {...commonProps}>
          <option value="" disabled>
            Выберите рейтинг
          </option>
          {RATING_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      ) : (
        <input
          {...commonProps}
          type={field.type}
          min={field.min}
          max={field.max}
          step={field.step}
        />
      )}
      {field.hint ? <small>{field.hint}</small> : null}
      {error ? <strong className="field-error">{error}</strong> : null}
    </label>
  );
}

export default function MovieForm({
  values,
  onChange,
  onSubmit,
  isLoading,
}) {
  const [activeIndex, setActiveIndex] = useState(0);
  const [fieldError, setFieldError] = useState("");
  const reviewIndex = FORM_FIELDS.length;
  const isReviewStep = activeIndex === reviewIndex;
  const currentField = FORM_FIELDS[activeIndex];
  const progress = Math.round(((activeIndex + 1) / (reviewIndex + 1)) * 100);

  const currentGroup = useMemo(() => {
    if (isReviewStep) {
      return "Проверка";
    }
    return currentField.group;
  }, [currentField, isReviewStep]);

  function handleFieldChange(name, value) {
    setFieldError("");
    onChange((currentValues) => ({
      ...currentValues,
      [name]: value,
    }));
  }

  function validateCurrentField() {
    if (isReviewStep) {
      return true;
    }
    const error = validateField(currentField, values[currentField.name]);
    setFieldError(error);
    return !error;
  }

  function findFirstInvalidField() {
    return FORM_FIELDS.findIndex((field) =>
      Boolean(validateField(field, values[field.name])),
    );
  }

  function goToPreviousStep() {
    setFieldError("");
    setActiveIndex((step) => Math.max(step - 1, 0));
  }

  function goToNextStep() {
    if (!validateCurrentField()) {
      return;
    }
    setActiveIndex((step) => Math.min(step + 1, reviewIndex));
  }

  function goToField(index) {
    setFieldError("");
    setActiveIndex(index);
  }

  function handleFormSubmit(event) {
    event.preventDefault();
    if (!isReviewStep) {
      goToNextStep();
      return;
    }

    const invalidIndex = findFirstInvalidField();
    if (invalidIndex >= 0) {
      setActiveIndex(invalidIndex);
      setFieldError(
        validateField(FORM_FIELDS[invalidIndex], values[FORM_FIELDS[invalidIndex].name]),
      );
      return;
    }

    onSubmit(event);
  }

  return (
    <form className="form-panel form-panel--wizard" onSubmit={handleFormSubmit}>
      <div className="wizard-top">
        <div>
          <span className="wizard-kicker">{currentGroup}</span>
          <h2>{isReviewStep ? "Проверьте данные" : "Заполните по одному полю"}</h2>
        </div>
        <div className="progress-badge">{progress}%</div>
      </div>

      <div className="progress-track" aria-hidden="true">
        <div style={{ width: `${progress}%` }} />
      </div>

      {!isReviewStep ? (
        <div className="question-card" key={currentField.name}>
          <div className="question-counter">
            Вопрос {activeIndex + 1} из {FORM_FIELDS.length}
          </div>
          <ActiveField
            field={currentField}
            value={values[currentField.name]}
            error={fieldError}
            onFieldChange={handleFieldChange}
          />
        </div>
      ) : (
        <div className="review-card">
          <p className="review-note">
            Проверьте значения перед расчётом. При необходимости вернитесь к
            нужному пункту.
          </p>
          <div className="review-grid">
            {FORM_FIELDS.map((field, index) => (
              <button
                className="review-item"
                key={field.name}
                type="button"
                onClick={() => goToField(index)}
              >
                <span>{field.shortLabel}</span>
                <strong>{formatReviewValue(field, values[field.name])}</strong>
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="form-actions wizard-actions">
        {activeIndex > 0 ? (
          <button className="secondary-button" type="button" onClick={goToPreviousStep}>
            Назад
          </button>
        ) : null}
        {!isReviewStep ? (
          <button className="primary-button" type="button" onClick={goToNextStep}>
            Далее
          </button>
        ) : (
          <button className="primary-button" type="submit" disabled={isLoading}>
            {isLoading ? "Считаем прогноз..." : "Рассчитать прогноз"}
          </button>
        )}
      </div>
    </form>
  );
}
