// Cargar datos
async function loadData() {

  const sentiment = await fetch("data/sentiment.json").then(r => r.json());
  const topics = await fetch("data/topics.json").then(r => r.json());
  const countries = await fetch("data/country_sentiment.json").then(r => r.json());

  // KPIs
  document.getElementById("positivo").innerText = sentiment.positivo + "%";
  document.getElementById("neutral").innerText = sentiment.neutral + "%";
  document.getElementById("negativo").innerText = sentiment.negativo + "%";

  // Gráfico sentimiento
  new Chart(document.getElementById("sentimentChart"), {
    type: 'doughnut',
    data: {
        labels: ["Positivo", "Neutral", "Negativo"],
        datasets: [{
        data: [sentiment.positivo, sentiment.neutral, sentiment.negativo],
        backgroundColor: [
            "#1f77b4", // azul
            "#cccccc", // gris
            "#d62728"  // rojo
        ],
        borderWidth: 0
        }]
    },
    options: {
        plugins: {
        legend: {
            position: 'bottom'
        }
        }
    }
    });

  // Gráfico tópicos
  new Chart(document.getElementById("topicsChart"), {
    type: 'bar',
    data: {
        labels: topics.map(t => t.name),
        datasets: [{
        data: topics.map(t => t.value),
        backgroundColor: "#1f77b4"
        }]
    },
    options: {
        indexAxis: 'y',
        plugins: {
        legend: { display: false }
        },
        scales: {
        x: {
            grid: { color: "#e6e6e6" }
        },
        y: {
            grid: { display: false }
        }
        }
    }
  });

  // Selector país
  const select = document.getElementById("countrySelect");

  countries.forEach(c => {
    const option = document.createElement("option");
    option.value = c.country;
    option.textContent = c.country;
    select.appendChild(option);
  });

  select.addEventListener("change", () => {
    const selected = countries.find(c => c.country === select.value);
    document.getElementById("countryResult").innerText =
      `Sentimiento: ${selected.score}`;
  });

}

loadData();