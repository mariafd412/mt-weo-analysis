// === WEO RISK MONITOR — app.js ===

let allCountries = [];
let countryChartInstance = null;

async function loadData() {
  try {
    const [sentiment, topics, countries] = await Promise.all([
      fetch("data/sentiment.json").then(r => r.json()),
      fetch("data/topics.json").then(r => r.json()),
      fetch("data/country_sentiment.json").then(r => r.json())
    ]);

    allCountries = countries;
    renderKPIs(sentiment, countries);
    renderAlertZone(countries);
    renderSentimentChart(sentiment);
    renderTopicsChart(topics);
    renderRiskTable(countries);
    renderCountrySelect(countries);
  } catch (err) {
    console.error("Error cargando datos:", err);
  }
}

// === KPIs ===
function renderKPIs(sentiment, countries) {
  const fmt = v => v.toFixed(1) + "%";
  const total = sentiment.total_sentences?.toLocaleString('es') || "—";

  setEl("kpi-negativo", fmt(sentiment.negativo));
  setEl("kpi-positivo", fmt(sentiment.positivo));
  setEl("kpi-neutral", fmt(sentiment.neutral));
  setEl("kpi-total-sub", total);
  setEl("hdr-total", sentiment.total_sentences?.toLocaleString('es') || "—");
  setEl("dc-val", fmt(sentiment.negativo));

  const altosCount = countries.filter(c => c.risk === "ALTO").length;
  setEl("kpi-alto", altosCount);

  setWidth("bar-neg", sentiment.negativo);
  setWidth("bar-pos", sentiment.positivo);
  setWidth("bar-neu", sentiment.neutral);
  setWidth("bar-risk", Math.min(altosCount * 10, 100));
}

// === ALERT ZONE (países alto riesgo) ===
function renderAlertZone(countries) {
  const high = countries.filter(c => c.risk === "ALTO");
  const zone = document.getElementById("alert-zone");

  if (high.length === 0) {
    zone.style.display = "none";
    return;
  }

  zone.style.display = "block";

  let html = `
    <div class="alert-zone-title">
      ⚠ ALERTA — ${high.length} PAÍS${high.length > 1 ? 'ES' : ''} CON RIESGO ALTO DETECTADO${high.length > 1 ? 'S' : ''} EN EL WEO
    </div>
    <div class="alert-country-row">
  `;

  high.forEach(c => {
    html += `
      <div class="alert-country-chip" onclick="selectCountry('${c.country}')">
        <span class="alert-chip-name">${c.country}</span>
        <span class="alert-chip-neg">NEG ${c.negative_percent}%</span>
        <span style="font-size:11px;color:var(--text-dim);font-family:var(--font-mono)">score ${c.score}</span>
      </div>
    `;
  });

  html += `</div>`;
  zone.innerHTML = html;
}

// === DONUT SENTIMIENTO ===
function renderSentimentChart(sentiment) {
  const ctx = document.getElementById("sentimentChart").getContext("2d");

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ["Positivo", "Neutral", "Negativo"],
      datasets: [{
        data: [sentiment.positivo, sentiment.neutral, sentiment.negativo],
        backgroundColor: [
          "rgba(79,143,255,0.85)",
          "rgba(107,117,144,0.4)",
          "rgba(255,59,59,0.85)"
        ],
        borderColor: [
          "rgba(79,143,255,1)",
          "rgba(107,117,144,0.6)",
          "rgba(255,59,59,1)"
        ],
        borderWidth: 1,
        hoverOffset: 4
      }]
    },
    options: {
      cutout: "72%",
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#13161e",
          borderColor: "#2a3045",
          borderWidth: 1,
          titleColor: "#e2e6f0",
          bodyColor: "#6b7590",
          callbacks: {
            label: ctx => ` ${ctx.label}: ${ctx.parsed.toFixed(1)}%`
          }
        }
      }
    }
  });

  // Legend manual
  const legendEl = document.getElementById("sentiment-legend");
  const items = [
    { label: "Positivo", color: "rgba(79,143,255,0.85)", val: sentiment.positivo },
    { label: "Neutral", color: "rgba(107,117,144,0.6)", val: sentiment.neutral },
    { label: "Negativo", color: "rgba(255,59,59,0.85)", val: sentiment.negativo }
  ];

  legendEl.innerHTML = items.map(i =>
    `<div class="legend-item">
      <div class="legend-dot" style="background:${i.color}"></div>
      <span>${i.label} <strong style="color:var(--text);font-family:var(--font-mono)">${i.val}%</strong></span>
    </div>`
  ).join("");
}

// === TOPICS BAR ===
function renderTopicsChart(topics) {
  const ctx = document.getElementById("topicsChart").getContext("2d");

  // Colores según interpretación
  const colorMap = {
    "GEOGRAFÍA": "rgba(79,143,255,0.7)",
    "EMPLEO": "rgba(48,209,88,0.7)",
    "CRECIMIENTO": "rgba(255,159,10,0.7)",
    "POLÍTICA MONETARIA": "rgba(175,82,222,0.7)"
  };

  const borderMap = {
    "GEOGRAFÍA": "rgba(79,143,255,1)",
    "EMPLEO": "rgba(48,209,88,1)",
    "CRECIMIENTO": "rgba(255,159,10,1)",
    "POLÍTICA MONETARIA": "rgba(175,82,222,1)"
  };

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: topics.map(t => t.name),
      datasets: [{
        data: topics.map(t => t.value),
        backgroundColor: topics.map(t => colorMap[t.interpretation] || "rgba(107,117,144,0.5)"),
        borderColor: topics.map(t => borderMap[t.interpretation] || "rgba(107,117,144,0.8)"),
        borderWidth: 1,
        borderRadius: 2
      }]
    },
    options: {
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#13161e",
          borderColor: "#2a3045",
          borderWidth: 1,
          titleColor: "#e2e6f0",
          bodyColor: "#6b7590",
          callbacks: {
            label: ctx => ` Peso léxico: ${ctx.parsed.x.toFixed(1)}%`
          }
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(31,37,53,0.8)" },
          ticks: { color: "#6b7590", font: { family: "'IBM Plex Mono'", size: 10 } },
          border: { color: "#1f2535" }
        },
        y: {
          grid: { display: false },
          ticks: { color: "#e2e6f0", font: { family: "'IBM Plex Sans'", size: 12 } },
          border: { display: false }
        }
      }
    }
  });

  // Pills con palabras clave
  const pillsEl = document.getElementById("topics-pills");
  topics.slice(0, 4).forEach(t => {
    const pill = document.createElement("span");
    pill.className = "topic-pill";
    pill.innerHTML = `${t.interpretation} · <span class="topic-pill-word">${t.top_words.slice(0,3).join(", ")}</span>`;
    pillsEl.appendChild(pill);
  });
}

// === TABLA DE RIESGO ===
function renderRiskTable(countries) {
  const tbody = document.getElementById("risk-tbody");

  // Mostrar: primero los de riesgo ALTO/MEDIO, luego el resto ordenado por compound
  const sorted = [...countries].sort((a, b) => {
    const rOrder = { ALTO: 0, MEDIO: 1, BAJO: 2 };
    if (rOrder[a.risk] !== rOrder[b.risk]) return rOrder[a.risk] - rOrder[b.risk];
    return a.score - b.score;
  });

  tbody.innerHTML = sorted.map(c => {
    const neg = c.negative_percent;
    const pos = c.positive_percent;
    const neu = c.neutral_percent;

    return `
      <tr data-risk="${c.risk}" onclick="selectCountry('${c.country.replace(/'/g, "\\'")}')">
        <td style="font-weight:500;color:var(--text)">${c.country}</td>
        <td><span class="risk-badge ${c.risk}">${c.risk}</span></td>
        <td class="neg-val">${neg > 0 ? neg.toFixed(1) + "%" : "—"}</td>
        <td class="compound-val">${c.score}</td>
        <td class="mentions-val">${c.total_mentions}</td>
        <td>
          <div class="mini-bar-wrap">
            <div class="mini-bar-pos" style="width:${pos}%"></div>
            <div class="mini-bar-neu" style="width:${neu}%"></div>
            <div class="mini-bar-neg" style="width:${neg}%"></div>
          </div>
        </td>
      </tr>
    `;
  }).join("");

  // Filtros
  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const filter = btn.dataset.filter;
      document.querySelectorAll("#risk-tbody tr").forEach(row => {
        if (filter === "all" || row.dataset.risk === filter) {
          row.classList.remove("hidden");
        } else {
          row.classList.add("hidden");
        }
      });
    });
  });
}

// === SELECT PAÍS ===
function renderCountrySelect(countries) {
  const select = document.getElementById("countrySelect");
  select.innerHTML = '<option value="">— Selecciona un país —</option>';

  // Ordenar por nombre
  const sorted = [...countries].sort((a, b) => a.country.localeCompare(b.country));
  sorted.forEach(c => {
    const opt = document.createElement("option");
    opt.value = c.country;
    opt.textContent = `${c.country} [${c.risk}]`;
    if (c.risk === "ALTO") opt.style.color = "#ff3b3b";
    select.appendChild(opt);
  });

  select.addEventListener("change", () => {
    if (select.value) selectCountry(select.value);
  });
}

// === DETALLE PAÍS ===
function selectCountry(name) {
  const c = allCountries.find(x => x.country === name);
  if (!c) return;

  // Actualizar select
  document.getElementById("countrySelect").value = name;

  const detail = document.getElementById("country-detail");
  const canvas = document.getElementById("countryChart");

  const riskLabels = { ALTO: "⚠ RIESGO ALTO", MEDIO: "◉ RIESGO MEDIO", BAJO: "● RIESGO BAJO" };
  const riskDesc = {
    ALTO: "Señal de riesgo elevada en el WEO. Compound score bajo y/o alta proporción de sentimiento negativo.",
    MEDIO: "Señal de riesgo moderada. Presencia de frases negativas o compound score intermedio.",
    BAJO: "Sin señales de riesgo significativas en el WEO para este país."
  };

  detail.style.display = "block";
  canvas.style.display = "block";
  detail.className = "country-detail";
  detail.innerHTML = `
    <div class="detail-header">
      <div>
        <div class="detail-country-name">${c.country}</div>
        <div class="detail-compound">Compound score: <strong style="color:var(--accent)">${c.score}</strong></div>
      </div>
    </div>
    <div class="detail-stats">
      <div class="detail-stat">
        <div class="detail-stat-val" style="color:var(--pos-color)">${c.positive_percent.toFixed(1)}%</div>
        <div class="detail-stat-lbl">Positivo</div>
      </div>
      <div class="detail-stat">
        <div class="detail-stat-val" style="color:var(--text-dim)">${c.neutral_percent.toFixed(1)}%</div>
        <div class="detail-stat-lbl">Neutral</div>
      </div>
      <div class="detail-stat">
        <div class="detail-stat-val" style="color:var(--risk-high)">${c.negative_percent.toFixed(1)}%</div>
        <div class="detail-stat-lbl">Negativo</div>
      </div>
    </div>
    <div class="detail-mentions">${c.total_mentions} menciones en el WEO</div>
    <div class="detail-risk-banner ${c.risk}">
      ${riskLabels[c.risk]}
      <span style="font-weight:300;font-size:10px;margin-left:8px">${riskDesc[c.risk]}</span>
    </div>
  `;

  // Mini gráfico de barras
  if (countryChartInstance) countryChartInstance.destroy();
  const ctx = canvas.getContext("2d");

  countryChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["Positivo", "Neutral", "Negativo"],
      datasets: [{
        data: [c.positive_percent, c.neutral_percent, c.negative_percent],
        backgroundColor: [
          "rgba(79,143,255,0.7)",
          "rgba(107,117,144,0.4)",
          "rgba(255,59,59,0.7)"
        ],
        borderColor: [
          "rgba(79,143,255,1)",
          "rgba(107,117,144,0.6)",
          "rgba(255,59,59,1)"
        ],
        borderWidth: 1,
        borderRadius: 2
      }]
    },
    options: {
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#13161e",
          borderColor: "#2a3045",
          borderWidth: 1,
          titleColor: "#e2e6f0",
          bodyColor: "#6b7590",
          callbacks: {
            label: ctx => ` ${ctx.parsed.y.toFixed(1)}%`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: "#6b7590", font: { family: "'IBM Plex Mono'", size: 10 } },
          border: { color: "#1f2535" }
        },
        y: {
          max: 100,
          grid: { color: "rgba(31,37,53,0.8)" },
          ticks: {
            color: "#6b7590",
            font: { family: "'IBM Plex Mono'", size: 10 },
            callback: v => v + "%"
          },
          border: { color: "#1f2535" }
        }
      }
    }
  });
}

// === UTILS ===
function setEl(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function setWidth(id, pct) {
  const el = document.getElementById(id);
  if (el) el.style.width = Math.min(pct, 100) + "%";
}

// === INIT ===
loadData();
