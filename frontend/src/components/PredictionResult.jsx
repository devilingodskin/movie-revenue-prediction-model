const usdFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

function Metric({ label, value, accent }) {
  return (
    <div className={`metric${accent ? " metric--accent" : ""}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ReportRow({ label, value }) {
  return (
    <div className="report-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default function PredictionResult({ result, error, isLoading, backendHint }) {
  return (
    <section className="result-panel report-panel" aria-live="polite">
      <div className="panel-header report-header">
        <div>
          <h2>{result ? "Отчёт по прогнозу" : "Подготовка отчёта"}</h2>
          <p>
            {result?.title
              ? result.title
              : "Итоговая оценка коммерческого потенциала фильма"}
          </p>
        </div>
      </div>

      {isLoading ? <div className="status-message">Формируем отчёт...</div> : null}

      {error ? (
        <div className="error-message">
          <strong>Не удалось получить прогноз.</strong>
          <span>{error}</span>
          <small>{backendHint}</small>
        </div>
      ) : null}

      {result ? (
        <div className="report-content">
          <div className="report-summary">
            <Metric
              label="Прогнозируемая кассовая выручка"
              value={usdFormatter.format(result.predicted_revenue)}
              accent
            />
            <Metric
              label="Прогнозируемая прибыль"
              value={usdFormatter.format(result.predicted_profit)}
            />
            <Metric label="ROI" value={result.roi.toFixed(2)} />
            <Metric
              label="Коэффициент окупаемости"
              value={result.payback_ratio.toFixed(2)}
            />
          </div>

          <div className="report-outcome">
            <ReportRow
              label="Категория коммерческой успешности"
              value={result.success_category}
            />
            <ReportRow label="Уровень риска" value={result.risk_level} />
          </div>

          <div className="report-note">
            <strong>Вывод</strong>
            <p>
              Прогноз показывает ожидаемый коммерческий результат проекта при
              указанных параметрах. Чем выше ROI и коэффициент окупаемости, тем
              выше запас относительно бюджета фильма.
            </p>
          </div>
        </div>
      ) : null}
    </section>
  );
}
