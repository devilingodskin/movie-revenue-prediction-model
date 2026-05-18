export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function requestJson(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const message =
      data?.detail ||
      `Ошибка запроса к backend: ${response.status} ${response.statusText}`;
    throw new Error(message);
  }

  return data;
}

export async function predictMovie(payload) {
  return requestJson("/api/predict", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getModelInfo() {
  return requestJson("/api/model/info");
}

export async function getModelMetrics() {
  return requestJson("/api/model/metrics");
}

export async function getSampleInput() {
  return requestJson("/api/sample-input");
}
