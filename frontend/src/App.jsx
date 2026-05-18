import { useEffect, useMemo, useRef, useState } from "react";
import { predictMovie } from "./api.js";
import MovieForm, { INITIAL_FORM_VALUES } from "./components/MovieForm.jsx";
import PredictionResult from "./components/PredictionResult.jsx";
import InfoPanel from "./components/InfoPanel.jsx";

const NUMERIC_FIELDS = new Set(["year", "score", "votes", "budget", "runtime"]);

function estimateVotesByBudget(budget) {
  if (budget >= 100_000_000) {
    return 150_000;
  }
  if (budget >= 50_000_000) {
    return 90_000;
  }
  if (budget >= 15_000_000) {
    return 35_000;
  }
  if (budget >= 3_000_000) {
    return 10_000;
  }
  return 2_000;
}

function normalizePayload(values) {
  const budget = Number(values.budget);
  const payload = {
    ...values,
    score: 6.5,
    votes: estimateVotesByBudget(budget),
  };

  return Object.fromEntries(
    Object.entries(payload).map(([key, value]) => [
      key,
      NUMERIC_FIELDS.has(key) ? Number(value) : value,
    ]),
  );
}

export default function App() {
  const [formValues, setFormValues] = useState(INITIAL_FORM_VALUES);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isPredictionRequested, setIsPredictionRequested] = useState(false);
  const reportRef = useRef(null);

  const backendHint = useMemo(
    () => "Сервис прогноза временно недоступен. Проверьте, что backend запущен.",
    [],
  );

  const showPredictionPanel = Boolean(isPredictionRequested || isLoading || prediction || error);
  const workspaceClassName = showPredictionPanel
    ? "workspace-grid workspace-grid--report"
    : "workspace-grid workspace-grid--centered";

  useEffect(() => {
    if (showPredictionPanel) {
      reportRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [showPredictionPanel]);

  function handleFormChange(update) {
    setFormValues(update);
    setPrediction(null);
    setError("");
    setIsPredictionRequested(false);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsPredictionRequested(true);
    setIsLoading(true);
    setError("");

    try {
      const payload = normalizePayload(formValues);
      const result = await predictMovie(payload);
      setPrediction(result);
    } catch (requestError) {
      setPrediction(null);
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="hero-section">
        <div className="hero-copy">
          <p className="institution">СГТУ им. Гагарина Ю.А. · М-ПИНФ-21</p>
          <h1>Прогнозирование коммерческой успешности фильма</h1>
          <p className="hero-text">
            Введите данные фильма по шагам, проверьте заполнение и получите
            понятную оценку выручки, прибыли, окупаемости и риска.
          </p>
          <p className="author-line">
            Разработано: Цветков Артём Денисович
          </p>
        </div>
      </section>

      <section className={workspaceClassName}>
        {!showPredictionPanel ? (
          <div className="form-stage">
            <MovieForm
              values={formValues}
              onChange={handleFormChange}
              onSubmit={handleSubmit}
              isLoading={isLoading}
            />
          </div>
        ) : null}

        {showPredictionPanel ? (
          <aside className="report-stage" ref={reportRef}>
            <PredictionResult
              result={prediction}
              error={error}
              isLoading={isLoading}
              backendHint={backendHint}
            />
            <InfoPanel />
          </aside>
        ) : null}
      </section>
    </main>
  );
}
