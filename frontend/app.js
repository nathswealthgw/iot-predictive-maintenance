const metrics = [
  { label: "Devices monitored", value: "120,000+" },
  { label: "Predicted failures", value: "3,420 / month" },
  { label: "Downtime reduction", value: "900+ hours" },
  { label: "Model latency", value: "<120 ms" }
];

const alerts = [
  {
    id: "device-1042",
    status: "High risk",
    signal: "Vibration spike",
    eta: "36 hours"
  },
  {
    id: "device-5581",
    status: "Medium risk",
    signal: "Thermal drift",
    eta: "5 days"
  },
  {
    id: "device-9021",
    status: "Monitor",
    signal: "Pressure variance",
    eta: "7 days"
  }
];

const metricsContainer = document.getElementById("metrics");
const alertsContainer = document.getElementById("alerts");
const waveGrid = document.getElementById("wave-grid");
const pulseLog = document.getElementById("pulse-log");
const uptimeValue = document.getElementById("uptime-value");
const throughputValue = document.getElementById("throughput-value");
const riskValue = document.getElementById("risk-value");

metrics.forEach((metric) => {
  const card = document.createElement("div");
  card.className = "metric-card";
  card.innerHTML = `
    <div class="metric-card__value">${metric.value}</div>
    <div class="metric-card__label">${metric.label}</div>
  `;
  metricsContainer.appendChild(card);
});

alerts.forEach((alert) => {
  const item = document.createElement("li");
  item.className = "alert-item";
  item.innerHTML = `
    <div>
      <div class="alert-item__id">${alert.id}</div>
      <div class="alert-item__signal">${alert.signal}</div>
    </div>
    <div class="alert-item__meta">
      <span>${alert.status}</span>
      <span>${alert.eta}</span>
    </div>
  `;
  alertsContainer.appendChild(item);
});

const waveBars = Array.from({ length: 18 }, (_, index) => {
  const bar = document.createElement("div");
  bar.className = "wave-bar";
  bar.style.animationDelay = `${index * 0.18}s`;
  waveGrid.appendChild(bar);
  return bar;
});

const pulseTemplates = [
  "Motor vibration spike normalized",
  "Thermal anomaly resolved",
  "Pressure surge contained",
  "Voltage drift stabilized",
  "Bearing wear detected"
];

const pulseEntries = [];

const updatePulseLog = () => {
  pulseLog.innerHTML = "";
  pulseEntries.slice(0, 4).forEach((entry) => {
    const item = document.createElement("li");
    item.innerHTML = `
      <span>${entry.message}</span>
      <span>${entry.time}</span>
    `;
    pulseLog.appendChild(item);
  });
};

const formatTime = (date) =>
  date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });

const updateLiveDemo = () => {
  const uptime = 99.88 + Math.random() * 0.1;
  const throughput = 41820 + Math.floor(Math.random() * 900);
  const risk = 0.24 + Math.random() * 0.2;

  uptimeValue.textContent = `${uptime.toFixed(2)}%`;
  throughputValue.textContent = throughput.toLocaleString();
  riskValue.textContent = risk.toFixed(2);

  waveBars.forEach((bar) => {
    const height = 30 + Math.random() * 70;
    bar.style.height = `${height}%`;
  });

  if (Math.random() > 0.4) {
    pulseEntries.unshift({
      message: pulseTemplates[Math.floor(Math.random() * pulseTemplates.length)],
      time: formatTime(new Date())
    });
    pulseEntries.splice(4);
    updatePulseLog();
  }
};

updateLiveDemo();
setInterval(updateLiveDemo, 1800);
