export default function InfoPanel() {
  return (
    <section className="info-panel">
      <div className="info-section">
        <h2>Как читать результат</h2>
        <p className="info-text">
          Чем выше ROI и коэффициент окупаемости, тем выше предполагаемый
          коммерческий потенциал фильма. Отрицательный ROI означает, что прогноз
          выручки ниже бюджета.
        </p>
      </div>

      <div className="info-section">
        <h2>Категории</h2>
        <ul className="rule-list">
          <li>ROI &lt; 0 — коммерчески неуспешный</li>
          <li>0 &lt;= ROI &lt; 1 — умеренно успешный</li>
          <li>1 &lt;= ROI &lt; 3 — коммерчески успешный</li>
          <li>ROI &gt;= 3 — высокоуспешный / блокбастер</li>
        </ul>
      </div>
    </section>
  );
}
