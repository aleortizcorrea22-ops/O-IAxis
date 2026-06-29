/**
 * O-IAxis Dashboard — Resumen ejecutivo con KPIs, salud del sistema y quick-wins
 */

const EMPRESA_ID = 1;

async function renderDashboard() {
  const content = document.getElementById("content");
  content.innerHTML = `
    <div class="page">
      <div class="section-header">
        <div class="section-title">Dashboard Ejecutivo</div>
        <div class="section-actions">
          <span class="topbar-env">Empresa ID: ${EMPRESA_ID}</span>
          <button class="btn btn-primary" onclick="renderDashboard()">↻ Actualizar</button>
        </div>
      </div>

      <!-- KPIs -->
      <div class="kpi-grid" id="kpi-grid">
        ${kpiSkeleton(6)}
      </div>

      <!-- Charts Row -->
      <div class="grid-2">
        <div class="card">
          <div class="card-title">Flujo de Caja — Proyección ML (12 meses)</div>
          <div class="chart-wrap"><canvas id="chart-cashflow"></canvas></div>
        </div>
        <div class="card">
          <div class="card-title">Distribución de Activos (M6)</div>
          <div class="chart-wrap"><canvas id="chart-activos"></canvas></div>
        </div>
      </div>

      <!-- System Health + ML Risk -->
      <div class="grid-3">
        <div class="card">
          <div class="card-title">Salud del Sistema</div>
          <div id="sys-health"><div class="spinner"></div></div>
        </div>
        <div class="card">
          <div class="card-title">Score de Riesgo Financiero</div>
          <div class="chart-wrap" style="height:160px"><canvas id="chart-risk"></canvas></div>
        </div>
        <div class="card">
          <div class="card-title">Motores Activos</div>
          <div id="motors-status"><div class="spinner"></div></div>
        </div>
      </div>

      <!-- Alertas Fraude -->
      <div class="card">
        <div class="section-header" style="margin-bottom:12px">
          <div class="card-title" style="margin-bottom:0">Alertas M11 — Detección de Anomalías</div>
          <button class="btn btn-ghost" onclick="Pages.fraud()">Ver todas →</button>
        </div>
        <div id="fraud-alerts"><div class="spinner"></div></div>
      </div>
    </div>
  `;

  // Cargar datos en paralelo
  const [statusData, activosData, fraudData] = await Promise.allSettled([
    API.status(),
    API.activos(EMPRESA_ID),
    API.alertasFraude(EMPRESA_ID),
  ]);

  // KPIs del sistema
  const status = statusData.status === "fulfilled" ? statusData.value : null;
  renderKPIs(status, activosData, fraudData);

  // Cash Flow projection (mock data para demo)
  const cashMock = [120000, 135000, 110000, 145000, 160000, 130000, 155000, 170000, 145000, 190000, 175000, 210000];
  const months = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"];
  setTimeout(() => {
    Charts.line("chart-cashflow", months, [
      { values: cashMock, color: "#00B4D8" },
      { values: cashMock.map(v => v * 0.85), color: "#EF4444" },
    ]);
  }, 100);

  // Activos donut
  if (activosData.status === "fulfilled" && activosData.value.activos?.length) {
    const a = activosData.value;
    const segs = a.activos.slice(0, 4).map(act => ({
      label: act.tipo, value: act.valor_libro
    }));
    setTimeout(() => Charts.donut("chart-activos", segs), 100);
  } else {
    document.getElementById("chart-activos").parentElement.innerHTML =
      `<p style="color:var(--gray-400);font-size:12px;text-align:center;padding-top:80px">Sin activos registrados</p>`;
  }

  // Risk gauge
  setTimeout(() => Charts.gauge("chart-risk", 68, 100, "Riesgo Medio"), 100);

  // System health
  if (status) {
    document.getElementById("sys-health").innerHTML = `
      <div style="display:flex;flex-direction:column;gap:8px;margin-top:4px">
        ${Object.entries(status.infrastructure).map(([k, v]) => `
          <div style="display:flex;justify-content:space-between;font-size:12px">
            <span style="color:var(--gray-400)">${k.replace(/_/g," ")}</span>
            <span class="badge ${v ? 'badge-success' : 'badge-danger'}">${v ? "OK" : "N/A"}</span>
          </div>
        `).join("")}
      </div>
    `;

    document.getElementById("motors-status").innerHTML = `
      <div style="display:flex;flex-direction:column;gap:6px;margin-top:4px">
        ${Object.entries(status.active_engines).map(([k, v]) => `
          <div style="display:flex;justify-content:space-between;font-size:12px">
            <span style="color:var(--gray-400)">${k.replace(/_/g," ")}</span>
            <span class="badge badge-success">${v}</span>
          </div>
        `).join("")}
      </div>
    `;
  }

  // Fraud alerts
  if (fraudData.status === "fulfilled") {
    const fd = fraudData.value;
    if (!fd.alertas?.length) {
      document.getElementById("fraud-alerts").innerHTML =
        `<p style="color:var(--success);font-size:13px">Sin alertas activas</p>`;
    } else {
      document.getElementById("fraud-alerts").innerHTML = `
        <div class="table-wrap">
          <table>
            <thead><tr><th>ID</th><th>Tipo</th><th>Severidad</th><th>Score</th><th>Monto</th></tr></thead>
            <tbody>
              ${fd.alertas.map(a => `
                <tr>
                  <td>${a.id}</td>
                  <td>${a.tipo}</td>
                  <td><span class="badge ${a.severidad === 'critica' ? 'badge-danger' : 'badge-warning'}">${a.severidad}</span></td>
                  <td>${(a.score * 100).toFixed(0)}%</td>
                  <td>${fmtARS(a.monto || 0)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      `;
    }
  } else {
    document.getElementById("fraud-alerts").innerHTML =
      `<p style="color:var(--gray-400);font-size:12px">M11 sin datos — ingrese transacciones para detectar anomalías</p>`;
  }
}

function renderKPIs(status, activosData, fraudData) {
  const actTotal = activosData.status === "fulfilled" ? activosData.value.total_activos || 0 : 0;
  const fraudCount = fraudData.status === "fulfilled" ? fraudData.value.alertas_abiertas || 0 : 0;
  const motorsOk = status ? Object.keys(status.active_engines).length : 0;

  document.getElementById("kpi-grid").innerHTML = `
    ${kpi("Activos Totales", fmtARS(actTotal), "↑ M6 Patrimonio", "pos", "🏦")}
    ${kpi("Motores Activos", `${motorsOk}/12`, "Todos operativos", motorsOk >= 12 ? "pos" : "neutral", "⚙️")}
    ${kpi("Alertas Fraude", fraudCount, fraudCount > 0 ? "Requiere atención" : "Sin anomalías", fraudCount > 0 ? "neg" : "pos", "🔍")}
    ${kpi("Backend API", "OK", "localhost:8000", "pos", "🟢")}
    ${kpi("Quantum Engine", "PennyLane", "Simulador activo", "neutral", "⚛️")}
    ${kpi("Base de Datos", "SQLite", "25+ tablas creadas", "neutral", "🗄️")}
  `;
}

function kpi(label, value, sub, deltaClass, icon) {
  return `
    <div class="kpi-card">
      <div class="kpi-label">${label}</div>
      <span class="kpi-icon">${icon}</span>
      <div class="kpi-value">${value}</div>
      <div class="kpi-delta ${deltaClass}">${sub}</div>
    </div>
  `;
}

function kpiSkeleton(n) {
  return Array(n).fill(`<div class="kpi-card"><div class="spinner"></div></div>`).join("");
}

function fmtARS(n) {
  if (!n && n !== 0) return "—";
  if (Math.abs(n) >= 1e6) return `$ ${(n / 1e6).toFixed(2)}M`;
  if (Math.abs(n) >= 1e3) return `$ ${(n / 1e3).toFixed(1)}K`;
  return `$ ${n.toFixed(2)}`;
}

window.renderDashboard = renderDashboard;
window.fmtARS = fmtARS;
