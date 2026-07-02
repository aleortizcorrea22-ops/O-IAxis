/**
 * O-IAxis Pages — Tesorería, Fiscal, ML, Quantum, Fraud
 */

const Pages = {

  // ===== M6 PATRIMONIO =====
  async patrimonio() {
    setPage("M6 — Patrimonio", `
      <div class="page">
        <div class="section-header">
          <div class="section-title">Motor M6 — Patrimonio y Activos</div>
        </div>
        <div class="card" style="margin-bottom:16px">
          <div class="card-title">Agregar Activo</div>
          <div class="grid-2" style="margin-bottom:12px">
            <div class="form-group">
              <label>Tipo</label>
              <select id="pat-tipo" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
                <option value="inmueble">Inmueble</option>
                <option value="vehiculo">Vehículo</option>
                <option value="maquinaria">Maquinaria</option>
                <option value="equipo">Equipo Informático</option>
                <option value="otros">Otros</option>
              </select>
            </div>
            <div class="form-group">
              <label>Descripción</label>
              <input id="pat-desc" type="text" placeholder="Oficina central" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
            <div class="form-group">
              <label>Valor en Libros ($)</label>
              <input id="pat-vlibro" type="number" placeholder="5000000" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
            <div class="form-group">
              <label>Valor de Mercado ($)</label>
              <input id="pat-vmercado" type="number" placeholder="7000000" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
          </div>
          <button class="btn btn-primary" onclick="agregarActivo()">+ Agregar Activo</button>
          <div id="pat-result" style="margin-top:12px"></div>
        </div>
        <div id="patrimonio-content"><div class="spinner"></div></div>
      </div>
    `);

    const activos = await API.activos(EMPRESA_ID).catch(() => ({ total_activos: 0, activos: [] }));

    let html = "";
    if (activos.total_activos) {
      html += `
        <div class="kpi-grid" style="margin-bottom:16px">
          ${kpi("Total Activos", fmtARS(activos.total_activos), "Balance patrimonial", "pos", "🏦")}
        </div>
      `;
    }

    html += `<div class="card">
      <div class="card-title">Inventario de Activos</div>`;
    if (activos.activos?.length) {
      html += `<div class="table-wrap"><table>
        <thead><tr><th>Tipo</th><th>Descripción</th><th>Valor Libro</th><th>Valor Mercado</th><th>Diferencia</th><th>Acción</th></tr></thead>
        <tbody>
          ${activos.activos.map(a => {
            const diff = (a.valor_mercado || a.valor_libro) - a.valor_libro;
            return `
              <tr>
                <td><span class="badge badge-info">${a.tipo}</span></td>
                <td>${a.descripcion}</td>
                <td>${fmtARS(a.valor_libro)}</td>
                <td>${fmtARS(a.valor_mercado || a.valor_libro)}</td>
                <td style="color:${diff >= 0 ? 'var(--success)' : 'var(--danger)'}">${diff >= 0 ? '+' : ''}${fmtARS(diff)}</td>
                <td style="display:flex;gap:6px"><button onclick="editarActivo(${a.id}, '${a.tipo}', '${a.descripcion}', ${a.valor_libro}, ${a.valor_mercado})" title="Editar" style="background:var(--teal);color:white;border:none;padding:6px;border-radius:4px;cursor:pointer;font-size:14px;width:32px;height:32px;display:flex;align-items:center;justify-content:center">✏️</button><button onclick="borrarActivo(${a.id})" title="Borrar" style="background:var(--danger);color:white;border:none;padding:6px;border-radius:4px;cursor:pointer;font-size:14px;width:32px;height:32px;display:flex;align-items:center;justify-content:center">🗑️</button></td>
              </tr>
            `;
          }).join("")}
        </tbody>
      </table></div>`;
    } else {
      html += `<p style="color:var(--gray-400);font-size:12px">Sin activos registrados.</p>`;
    }
    html += "</div>";

    document.getElementById("patrimonio-content").innerHTML = html;
  },

  // ===== M2 TESORERÍA =====
  async tesoreria() {
    setPage("M2 — Tesorería", `
      <div class="page">
        <div class="section-header">
          <div class="section-title">Motor M2 — Tesorería y Flujo de Caja</div>
        </div>
        <div class="card" style="margin-bottom:16px">
          <div class="card-title">Agregar Transacción</div>
          <div class="grid-2" style="margin-bottom:12px">
            <div class="form-group">
              <label>Tipo</label>
              <select id="teso-tipo" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
                <option value="ingresos">Ingresos</option>
                <option value="egresos">Egresos</option>
                <option value="transferencias">Transferencias</option>
              </select>
            </div>
            <div class="form-group">
              <label>Monto ($)</label>
              <input id="teso-monto" type="number" placeholder="500000" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
            <div class="form-group">
              <label>Descripción</label>
              <input id="teso-desc" type="text" placeholder="Cobranza cliente ABC" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
            <div class="form-group">
              <label>Fecha</label>
              <input id="teso-fecha" type="date" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
            <div class="form-group">
              <label>Referencia</label>
              <input id="teso-ref" type="text" placeholder="REF-001" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
          </div>
          <button class="btn btn-primary" onclick="agregarTransaccion()">+ Agregar Transacción</button>
          <div id="teso-result" style="margin-top:12px"></div>
        </div>
        <div id="tesoreria-content"><div class="spinner"></div></div>
      </div>
    `);

    const [resumen, txs] = await Promise.allSettled([
      API.tesoreriaResumen(EMPRESA_ID),
      API.tesoreriaTransactions(EMPRESA_ID),
    ]);

    let html = "";

    if (resumen.status === "fulfilled") {
      const r = resumen.value;
      html += `
        <div class="kpi-grid" style="margin-bottom:16px">
          ${kpi("Saldo Actual", fmtARS(r.saldo_actual), "Posición de caja", "pos", "💰")}
          ${kpi("Ingresos del Mes", fmtARS(r.ingresos_mes), "Este mes", "pos", "📈")}
          ${kpi("Egresos del Mes", fmtARS(r.egresos_mes), "Este mes", "neg", "📉")}
          ${kpi("Flujo Neto", fmtARS(r.flujo_neto), r.flujo_neto >= 0 ? "Positivo" : "Negativo", r.flujo_neto >= 0 ? "pos" : "neg", "⚖️")}
          ${kpi("Tx Pendientes", r.transacciones_pendientes, "Sin ejecutar", "neutral", "⏳")}
        </div>
      `;
    } else {
      html += `<div class="card" style="margin-bottom:16px"><p style="color:var(--gray-400)">Sin datos de tesorería registrados. Cree transacciones vía API: <code>POST /api/v1/motors/m2/transactions</code></p></div>`;
    }

    // Transacciones
    html += `
      <div class="card">
        <div class="section-header" style="margin-bottom:12px">
          <div class="card-title" style="margin-bottom:0">Últimas Transacciones</div>
        </div>
    `;
    if (txs.status === "fulfilled" && txs.value.length) {
      html += `<div class="table-wrap"><table>
        <thead><tr><th>ID</th><th>Fecha</th><th>Tipo</th><th>Monto</th><th>Referencia</th><th>Estado</th><th>Acción</th></tr></thead>
        <tbody>
          ${txs.value.map(t => `
            <tr>
              <td>${t.id}</td>
              <td>${t.fecha_transaccion}</td>
              <td><span class="badge ${t.tipo === 'ingresos' ? 'badge-success' : 'badge-danger'}">${t.tipo}</span></td>
              <td>${fmtARS(t.monto)}</td>
              <td style="color:var(--gray-400)">${t.referencia}</td>
              <td><span class="badge badge-info">${t.status}</span></td>
              <td style="display:flex;gap:6px"><button onclick="editarTransaccion(${t.id}, '${t.tipo}', ${t.monto}, '${(t.referencia||'').replace(/'/g,'')}', '${t.fecha_transaccion||''}')" title="Editar" style="background:var(--teal);color:white;border:none;padding:6px;border-radius:4px;cursor:pointer;font-size:14px;width:32px;height:32px;display:flex;align-items:center;justify-content:center">✏️</button><button onclick="borrarTransaccion(${t.id})" title="Borrar" style="background:var(--danger);color:white;border:none;padding:6px;border-radius:4px;cursor:pointer;font-size:14px;width:32px;height:32px;display:flex;align-items:center;justify-content:center">🗑️</button></td>
            </tr>
          `).join("")}
        </tbody>
      </table></div>`;
    } else {
      html += `<p style="color:var(--gray-400);font-size:12px">No hay transacciones registradas.</p>`;
    }
    html += "</div>";

    document.getElementById("tesoreria-content").innerHTML = html;
  },

  // ===== M5 FISCAL =====
  async fiscal() {
    setPage("M5 — Fiscal", `
      <div class="page">
        <div class="section-header">
          <div class="section-title">Motor M5 — Gestión Fiscal e Impositiva</div>
        </div>
        <div class="card" style="margin-bottom:16px">
          <div class="card-title">Registrar Impuesto</div>
          <div class="grid-2" style="margin-bottom:12px">
            <div class="form-group">
              <label>Tipo de Impuesto</label>
              <select id="fisc-tipo" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
                <option value="iva">IVA</option>
                <option value="ingresos_brutos">Ingresos Brutos</option>
                <option value="ganancias">Ganancias</option>
                <option value="afip">AFIP General</option>
              </select>
            </div>
            <div class="form-group">
              <label>Período (AAAA-MM)</label>
              <input id="fisc-periodo" type="text" placeholder="2026-06" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
            <div class="form-group">
              <label>Base Imponible ($)</label>
              <input id="fisc-base" type="number" placeholder="500000" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
            <div class="form-group">
              <label>Alícuota (%)</label>
              <input id="fisc-alicuota" type="number" placeholder="21" step="0.01" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
            </div>
          </div>
          <button class="btn btn-primary" onclick="agregarImpuesto()">+ Registrar Impuesto</button>
          <div id="fisc-result" style="margin-top:12px"></div>
        </div>
        <div id="fiscal-content"><div class="spinner"></div></div>
      </div>
    `);

    const [impuestos, obligaciones] = await Promise.allSettled([
      API.impuestos(EMPRESA_ID),
      API.obligaciones(EMPRESA_ID),
    ]);

    let html = "";

    // Impuestos
    html += `<div class="card" style="margin-bottom:16px">
      <div class="card-title">Impuestos Registrados</div>`;
    if (impuestos.status === "fulfilled" && impuestos.value.length) {
      html += `<div class="table-wrap"><table>
        <thead><tr><th>ID</th><th>Tipo</th><th>Período</th><th>Base Imponible</th><th>Alícuota</th><th>Monto</th><th>Estado</th><th>Acción</th></tr></thead>
        <tbody>
          ${impuestos.value.map(i => `
            <tr>
              <td>${i.id}</td>
              <td><span class="badge badge-info">${i.tipo_impuesto}</span></td>
              <td>${i.periodo}</td>
              <td>${fmtARS(i.base_imponible)}</td>
              <td>${i.alicuota}%</td>
              <td>${fmtARS(i.monto_impuesto)}</td>
              <td><span class="badge ${i.estado === 'pagado' ? 'badge-success' : i.estado === 'vencido' ? 'badge-danger' : 'badge-warning'}">${i.estado}</span></td>
              <td style="display:flex;gap:6px"><button onclick="editarImpuesto(${i.id}, '${i.tipo_impuesto}', '${i.periodo}', ${i.base_imponible}, ${i.alicuota})" title="Editar" style="background:var(--teal);color:white;border:none;padding:6px;border-radius:4px;cursor:pointer;font-size:14px;width:32px;height:32px;display:flex;align-items:center;justify-content:center">✏️</button><button onclick="borrarImpuesto(${i.id})" title="Borrar" style="background:var(--danger);color:white;border:none;padding:6px;border-radius:4px;cursor:pointer;font-size:14px;width:32px;height:32px;display:flex;align-items:center;justify-content:center">🗑️</button></td>
            </tr>
          `).join("")}
        </tbody>
      </table></div>`;
    } else {
      html += `<p style="color:var(--gray-400);font-size:12px">Sin impuestos registrados. Usar <code>POST /api/v1/motors/m5/impuestos</code></p>`;
    }
    html += "</div>";

    // Obligaciones
    html += `<div class="card">
      <div class="card-title">Calendario de Obligaciones</div>`;
    if (obligaciones.status === "fulfilled" && obligaciones.value.length) {
      html += `<div class="table-wrap"><table>
        <thead><tr><th>Tipo</th><th>Descripción</th><th>Vencimiento</th><th>Estado</th></tr></thead>
        <tbody>
          ${obligaciones.value.map(o => `
            <tr>
              <td><span class="badge badge-info">${o.tipo}</span></td>
              <td>${o.descripcion}</td>
              <td>${o.fecha_vencimiento}</td>
              <td><span class="badge ${o.estatus === 'cumplido' ? 'badge-success' : 'badge-warning'}">${o.estatus}</span></td>
            </tr>
          `).join("")}
        </tbody>
      </table></div>`;
    } else {
      html += `<p style="color:var(--gray-400);font-size:12px">Sin obligaciones registradas.</p>`;
    }
    html += "</div>";

    document.getElementById("fiscal-content").innerHTML = html;
  },

  // ===== ML ENGINE =====
  async ml() {
    setPage("ML Engine", `
      <div class="page">
        <div class="section-header">
          <div class="section-title">Machine Learning — Motores Predictivos</div>
        </div>
        <div id="ml-content"><div class="spinner"></div></div>
      </div>
    `);

    const [models, risk] = await Promise.allSettled([
      API.mlModels(),
      API.financialRisk(1.5, 2.0, 3.5),
    ]);

    let html = "";

    if (risk.status === "fulfilled") {
      const r = risk.value;
      html += `
        <div class="grid-2" style="margin-bottom:0">
          <div class="card">
            <div class="card-title">Evaluación de Riesgo Financiero (Demo)</div>
            <div style="margin-top:12px">
              <div style="font-size:32px;font-weight:700;color:${r.risk_level === 'LOW' ? 'var(--success)' : r.risk_level === 'MEDIUM' ? 'var(--warning)' : 'var(--danger)'}">
                ${r.risk_level}
              </div>
              <div style="font-size:13px;color:var(--gray-400);margin:8px 0">Score: ${r.risk_score} / 100</div>
              <div class="progress-bar" style="margin:8px 0">
                <div class="progress-fill" style="width:${r.risk_score}%;background:${r.risk_level === 'LOW' ? 'var(--success)' : r.risk_level === 'MEDIUM' ? 'var(--warning)' : 'var(--danger)'}"></div>
              </div>
              ${r.risk_factors.length ? `
                <div style="margin-top:12px;font-size:12px;color:var(--gray-400)">Factores:</div>
                <ul style="margin-top:6px;padding-left:16px;font-size:12px;color:var(--danger);line-height:1.8">
                  ${r.risk_factors.map(f => `<li>${f}</li>`).join("")}
                </ul>
              ` : `<p style="color:var(--success);font-size:12px;margin-top:8px">Sin factores de riesgo detectados</p>`}
              <p style="font-size:11px;color:var(--gray-600);margin-top:12px">${r.recommendation}</p>
            </div>
          </div>
          <div class="card">
            <div class="card-title">Proyección Flujo de Caja (demo)</div>
            <div class="chart-wrap" style="margin-top:8px"><canvas id="chart-ml-cashflow"></canvas></div>
          </div>
        </div>
      `;
    }

    // Models list
    if (models.status === "fulfilled") {
      html += `
        <div class="card" style="margin-top:16px">
          <div class="card-title">Modelos Disponibles</div>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Modelo</th><th>Tipo</th><th>Accuracy</th><th>Endpoint</th></tr></thead>
              <tbody>
                ${models.value.models.map(m => `
                  <tr>
                    <td style="font-weight:600">${m.name}</td>
                    <td><span class="badge badge-info">${m.type}</span></td>
                    <td>
                      <div style="display:flex;align-items:center;gap:8px">
                        <div class="progress-bar" style="width:80px"><div class="progress-fill" style="width:${m.accuracy*100}%"></div></div>
                        <span style="font-size:12px">${(m.accuracy*100).toFixed(0)}%</span>
                      </div>
                    </td>
                    <td style="color:var(--teal);font-size:11px;font-family:monospace">/api/v1/ml${m.endpoint}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      `;
    }

    document.getElementById("ml-content").innerHTML = html;
    setTimeout(() => {
      const mock = [120,135,110,145,160,130,155,170,145,190,175,210];
      Charts.line("chart-ml-cashflow",
        ["E","F","M","A","M","J","J","A","S","O","N","D"],
        [{ values: mock, color: "#00B4D8" }]
      );
    }, 100);
  },

  // ===== QUANTUM =====
  async quantum() {
    setPage("Quantum Engine", `
      <div class="page">
        <div class="section-header">
          <div class="section-title">⚛️ Motor Cuántico — Optimización QAOA</div>
        </div>
        <div id="quantum-content"><div class="spinner"></div></div>
      </div>
    `);

    const qStatus = await API.quantumStatus().catch(() => null);

    let html = `
      <div class="card" style="margin-bottom:16px">
        <div class="card-title">Estado del Motor Cuántico</div>
        ${qStatus ? `
          <div style="display:flex;gap:24px;margin-top:12px;flex-wrap:wrap">
            <div><span style="color:var(--gray-400);font-size:12px">Disponible:</span>
              <span class="badge ${qStatus.quantum_available ? 'badge-success' : 'badge-warning'}" style="margin-left:6px">${qStatus.quantum_available ? "Sí" : "No"}</span>
            </div>
            <div><span style="color:var(--gray-400);font-size:12px">Backend:</span>
              <span style="color:var(--teal);font-size:12px;margin-left:6px">${qStatus.backend}</span>
            </div>
            <div><span style="color:var(--gray-400);font-size:12px">Regla de Oro:</span>
              <span style="color:var(--white);font-size:12px;margin-left:6px">${qStatus.rule}</span>
            </div>
          </div>
        ` : `<p style="color:var(--danger);font-size:12px">No se pudo conectar al motor cuántico</p>`}
      </div>

      <!-- Demo Optimizer -->
      <div class="grid-2">
        <div class="card">
          <div class="card-title">Optimización de Portafolio (QAOA Demo)</div>
          <p style="color:var(--gray-400);font-size:12px;margin-bottom:12px">5 activos, presupuesto 3, aversión al riesgo 0.4</p>
          <button class="btn btn-primary" onclick="runPortfolioDemo()">
            ⚛️ Ejecutar QAOA
          </button>
          <div id="portfolio-result" style="margin-top:12px"></div>
        </div>
        <div class="card">
          <div class="card-title">Scheduling de Pagos (Quantum Demo)</div>
          <p style="color:var(--gray-400);font-size:12px;margin-bottom:12px">4 pagos pendientes, caja disponible $ 500K</p>
          <button class="btn btn-primary" onclick="runPaymentsDemo()">
            ⚛️ Optimizar Pagos
          </button>
          <div id="payments-result" style="margin-top:12px"></div>
        </div>
      </div>

      <div class="card" style="margin-top:0">
        <div class="card-title">Asignación de Recursos (Quantum Demo)</div>
        <p style="color:var(--gray-400);font-size:12px;margin-bottom:12px">3 proyectos disponibles, presupuesto $ 800K</p>
        <button class="btn btn-primary" onclick="runResourcesDemo()">
          ⚛️ Asignar Recursos
        </button>
        <div id="resources-result" style="margin-top:12px"></div>
      </div>
    `;

    document.getElementById("quantum-content").innerHTML = html;
  },

  // ===== FRAUD / M11 =====
  async fraud() {
    setPage("M11 — Detección de Fraude", `
      <div class="page">
        <div class="section-header">
          <div class="section-title">Motor M11 — Detección de Fraude y Anomalías</div>
        </div>
        <div id="fraud-content"><div class="spinner"></div></div>
      </div>
    `);

    const alertas = await API.alertasFraude(EMPRESA_ID).catch(() => ({ alertas: [], alertas_abiertas: 0 }));

    let html = `
      <div class="kpi-grid" style="margin-bottom:16px">
        ${kpi("Alertas Abiertas", alertas.alertas_abiertas || 0, "Requieren revisión", (alertas.alertas_abiertas || 0) > 0 ? "neg" : "pos", "🚨")}
      </div>
      <div class="card">
        <div class="card-title">Simulador de Detección</div>
        <p style="color:var(--gray-400);font-size:12px;margin-bottom:12px">Ingrese una serie de montos de transacciones para detectar anomalías con ML</p>
        <div style="display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap">
          <div class="form-group" style="margin-bottom:0;flex:1;min-width:200px">
            <label>Serie de montos (separados por coma)</label>
            <input id="fraud-input" type="text" value="1000,1200,950,1100,15000,1050,980,1150" placeholder="1000,1200,950,...">
          </div>
          <button class="btn btn-primary" onclick="runFraudDetection()">Detectar Anomalías</button>
        </div>
        <div id="fraud-sim-result" style="margin-top:16px"></div>
      </div>
    `;

    if (alertas.alertas?.length) {
      html += `
        <div class="card" style="margin-top:16px">
          <div class="card-title">Historial de Alertas</div>
          <div class="table-wrap"><table>
            <thead><tr><th>ID</th><th>Tipo</th><th>Severidad</th><th>Score</th><th>Monto</th></tr></thead>
            <tbody>
              ${alertas.alertas.map(a => `
                <tr>
                  <td>${a.id}</td>
                  <td>${a.tipo}</td>
                  <td><span class="badge ${a.severidad === 'critica' ? 'badge-danger' : 'badge-warning'}">${a.severidad}</span></td>
                  <td>${(a.score * 100).toFixed(0)}%</td>
                  <td>${fmtARS(a.monto || 0)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table></div>
        </div>
      `;
    }

    document.getElementById("fraud-content").innerHTML = html;
  },
};

// ===== QUANTUM DEMO RUNNERS =====
async function runPortfolioDemo() {
  const el = document.getElementById("portfolio-result");
  el.innerHTML = `<div class="spinner"></div>`;
  try {
    const result = await API.quantumPortfolio({
      returns: [0.12, 0.08, 0.15, 0.10, 0.20],
      risks:   [0.05, 0.03, 0.08, 0.04, 0.12],
      budget: 3,
      risk_aversion: 0.4
    });
    el.innerHTML = `
      <div style="font-size:12px;color:var(--gray-400);margin-bottom:6px">${result.algorithm}</div>
      <div style="font-size:12px">Activos seleccionados: <strong style="color:var(--teal)">[${result.selected_assets.join(", ")}]</strong></div>
      <div style="font-size:12px">Retorno esperado: <strong style="color:var(--success)">${(result.expected_return * 100).toFixed(2)}%</strong></div>
      <div style="font-size:12px">Sharpe estimado: <strong>${result.sharpe_estimate?.toFixed(3)}</strong></div>
    `;
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger);font-size:12px">${e.message}</p>`;
  }
}

async function runPaymentsDemo() {
  const el = document.getElementById("payments-result");
  el.innerHTML = `<div class="spinner"></div>`;
  try {
    const result = await API.quantumPayments({
      payments: [
        { monto: 150000, penalizacion: 5000, prioridad: 1 },
        { monto: 200000, penalizacion: 8000, prioridad: 2 },
        { monto: 100000, penalizacion: 2000, prioridad: 1 },
        { monto: 250000, penalizacion: 12000, prioridad: 3 },
      ],
      available_cash: 500000
    });
    el.innerHTML = `
      <div style="font-size:12px;color:var(--gray-400);margin-bottom:6px">${result.algorithm}</div>
      <div style="font-size:12px">Pagar ahora: <strong style="color:var(--teal)">[${result.pay_immediately.join(", ")}]</strong></div>
      <div style="font-size:12px">Efectivo requerido: <strong>${fmtARS(result.cash_required)}</strong></div>
      <div style="font-size:12px">Penalizaciones evitadas: <strong style="color:var(--success)">${fmtARS(result.penalties_avoided)}</strong></div>
      <div style="font-size:12px">Factible: <span class="badge ${result.feasible ? 'badge-success' : 'badge-danger'}">${result.feasible ? "Sí" : "No"}</span></div>
    `;
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger);font-size:12px">${e.message}</p>`;
  }
}

async function runResourcesDemo() {
  const el = document.getElementById("resources-result");
  el.innerHTML = `<div class="spinner"></div>`;
  try {
    const result = await API.quantumResources({
      projects: [
        { nombre: "CRM Digital", roi: 0.25, costo: 300000 },
        { nombre: "Planta Automatización", roi: 0.35, costo: 500000 },
        { nombre: "Capacitación RRHH", roi: 0.15, costo: 100000 },
      ],
      total_resources: 800000
    });
    el.innerHTML = `
      <div style="font-size:12px;color:var(--gray-400);margin-bottom:6px">${result.algorithm}</div>
      <div style="font-size:12px">Proyectos financiados: <strong style="color:var(--teal)">${result.funded_projects.map(p => p.nombre).join(", ")}</strong></div>
      <div style="font-size:12px">Costo total: <strong>${fmtARS(result.total_cost)}</strong></div>
      <div style="font-size:12px">ROI total esperado: <strong style="color:var(--success)">${(result.expected_total_roi * 100).toFixed(1)}%</strong></div>
      <div style="font-size:12px">Recursos restantes: <strong>${fmtARS(result.resources_remaining)}</strong></div>
    `;
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger);font-size:12px">${e.message}</p>`;
  }
}

async function runFraudDetection() {
  const el = document.getElementById("fraud-sim-result");
  const raw = document.getElementById("fraud-input").value;
  const series = raw.split(",").map(v => parseFloat(v.trim())).filter(v => !isNaN(v));

  if (series.length < 3) {
    el.innerHTML = `<p style="color:var(--warning);font-size:12px">Ingrese al menos 3 valores.</p>`;
    return;
  }

  el.innerHTML = `<div class="spinner"></div>`;
  try {
    const params = series.map(v => `transacciones=${v}`).join("&");
    const result = await API.get(`/api/v1/motors/m11/detectar-fraude?empresa_id=${EMPRESA_ID}&${params}`);
    el.innerHTML = `
      <div style="font-size:13px;font-weight:600;margin-bottom:8px;color:${result.total_anomalias > 0 ? 'var(--danger)' : 'var(--success)'}">
        ${result.total_anomalias > 0 ? `⚠ ${result.total_anomalias} anomalía(s) detectadas` : "✓ Sin anomalías detectadas"}
      </div>
      ${result.detalle.length ? `
        <div class="table-wrap"><table>
          <thead><tr><th>Índice</th><th>Valor</th><th>Z-Score</th><th>Severidad</th></tr></thead>
          <tbody>
            ${result.detalle.map(a => `
              <tr>
                <td>${a.index}</td>
                <td>${fmtARS(a.value)}</td>
                <td>${a.z_score.toFixed(2)}</td>
                <td><span class="badge ${a.severity === 'high' ? 'badge-danger' : 'badge-warning'}">${a.severity}</span></td>
              </tr>
            `).join("")}
          </tbody>
        </table></div>
      ` : ""}
    `;
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger);font-size:12px">${e.message}</p>`;
  }
}

// ===== FORM HANDLERS =====
async function agregarTransaccion() {
  const el = document.getElementById("teso-result");
  const tipo = document.getElementById("teso-tipo").value;
  const monto = parseFloat(document.getElementById("teso-monto").value);
  const desc = document.getElementById("teso-desc").value;
  const fecha = document.getElementById("teso-fecha").value;
  const referencia = document.getElementById("teso-ref").value || "REF-001";

  if (!monto || !desc || !fecha) {
    el.innerHTML = `<p style="color:var(--warning)">Completa todos los campos</p>`;
    return;
  }

  el.innerHTML = `<div class="spinner"></div>`;
  try {
    await API.post("/api/v1/motors/m2/transactions", {
      empresa_id: EMPRESA_ID,
      tipo,
      monto,
      descripcion: desc,
      fecha_transaccion: fecha,
      referencia
    });
    el.innerHTML = `<p style="color:var(--success)">✓ Transacción agregada</p>`;
    document.getElementById("teso-monto").value = "";
    document.getElementById("teso-desc").value = "";
    document.getElementById("teso-fecha").value = "";
    document.getElementById("teso-ref").value = "";
    setTimeout(() => Pages.tesoreria(), 1500);
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger)">${e.message}</p>`;
  }
}

async function agregarImpuesto() {
  const el = document.getElementById("fisc-result");
  const tipo = document.getElementById("fisc-tipo").value;
  const periodo = document.getElementById("fisc-periodo").value;
  const base = parseFloat(document.getElementById("fisc-base").value);
  const alicuota = parseFloat(document.getElementById("fisc-alicuota").value) / 100;

  if (!periodo || !base || !alicuota) {
    el.innerHTML = `<p style="color:var(--warning)">Completa todos los campos</p>`;
    return;
  }

  el.innerHTML = `<div class="spinner"></div>`;
  try {
    await API.post("/api/v1/motors/m5/impuestos", {
      empresa_id: EMPRESA_ID,
      tipo_impuesto: tipo,
      periodo,
      base_imponible: base,
      alicuota
    });
    el.innerHTML = `<p style="color:var(--success)">✓ Impuesto registrado</p>`;
    document.getElementById("fisc-base").value = "";
    document.getElementById("fisc-periodo").value = "";
    document.getElementById("fisc-alicuota").value = "";
    setTimeout(() => Pages.fiscal(), 1500);
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger)">${e.message}</p>`;
  }
}

async function agregarActivo() {
  const el = document.getElementById("pat-result");
  const tipo = document.getElementById("pat-tipo").value;
  const desc = document.getElementById("pat-desc").value;
  const vlibro = parseFloat(document.getElementById("pat-vlibro").value);
  const vmercado = parseFloat(document.getElementById("pat-vmercado").value);

  if (!desc || !vlibro || !vmercado) {
    el.innerHTML = `<p style="color:var(--warning)">Completa todos los campos</p>`;
    return;
  }

  el.innerHTML = `<div class="spinner"></div>`;
  try {
    await API.post("/api/v1/motors/m6/activos", {
      empresa_id: EMPRESA_ID,
      tipo,
      descripcion: desc,
      valor_libro: vlibro,
      valor_mercado: vmercado
    });
    el.innerHTML = `<p style="color:var(--success)">✓ Activo agregado</p>`;
    document.getElementById("pat-desc").value = "";
    document.getElementById("pat-vlibro").value = "";
    document.getElementById("pat-vmercado").value = "";
    setTimeout(() => Pages.patrimonio(), 1500);
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger)">${e.message}</p>`;
  }
}

// Funciones para borrar datos
async function borrarTransaccion(id) {
  if (!confirm("🗑️ ¿Confirma eliminar esta transacción?")) return;
  try {
    await API.request(`/api/v1/motors/m2/transactions/${id}`, { method: "DELETE" });
    showToast("🗑️ Transacción eliminada");
    Pages.tesoreria();
  } catch (e) {
    showToast("❌ Error al eliminar: " + e.message, "error");
  }
}

async function borrarImpuesto(id) {
  if (!confirm("🗑️ ¿Confirma eliminar este impuesto?")) return;
  try {
    await API.request(`/api/v1/motors/m5/impuestos/${id}`, { method: "DELETE" });
    showToast("🗑️ Impuesto eliminado");
    Pages.fiscal();
  } catch (e) {
    showToast("❌ Error al eliminar: " + e.message, "error");
  }
}

async function borrarActivo(id) {
  if (!confirm("🗑️ ¿Confirma eliminar este activo?")) return;
  try {
    await API.request(`/api/v1/motors/m6/activos/${id}`, { method: "DELETE" });
    showToast("🗑️ Activo eliminado");
    Pages.patrimonio();
  } catch (e) {
    showToast("❌ Error al eliminar: " + e.message, "error");
  }
}

// ===== MODAL DE EDICIÓN =====
function abrirModal(html) {
  document.getElementById("modal-overlay").style.display = "flex";
  document.getElementById("modal-box").style.display = "block";
  document.getElementById("modal-box").innerHTML = html;
}
function cerrarModal() {
  document.getElementById("modal-overlay").style.display = "none";
  document.getElementById("modal-box").style.display = "none";
}

// Editar fila completa M2 — Transacción
function editarTransaccion(id, tipo, monto, referencia, fecha) {
  abrirModal(`
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <div style="font-size:15px;font-weight:700;color:var(--white)">✏️ Editar Transacción #${id}</div>
      <button onclick="cerrarModal()" style="background:none;border:none;color:var(--gray-400);font-size:20px;cursor:pointer;line-height:1">×</button>
    </div>
    <div class="grid-2" style="margin-bottom:16px">
      <div class="form-group">
        <label>Tipo</label>
        <select id="ed-tipo" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
          <option value="ingresos" ${tipo==='ingresos'?'selected':''}>Ingresos</option>
          <option value="egresos" ${tipo==='egresos'?'selected':''}>Egresos</option>
          <option value="transferencias" ${tipo==='transferencias'?'selected':''}>Transferencias</option>
        </select>
      </div>
      <div class="form-group">
        <label>Monto ($)</label>
        <input id="ed-monto" type="number" value="${monto}" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
      </div>
      <div class="form-group">
        <label>Referencia / Descripción</label>
        <input id="ed-ref" type="text" value="${referencia}" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
      </div>
      <div class="form-group">
        <label>Fecha</label>
        <input id="ed-fecha" type="date" value="${fecha || new Date().toISOString().split('T')[0]}" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
      </div>
    </div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      <button onclick="cerrarModal()" class="btn" style="background:var(--navy-3);color:var(--gray-400)">Cancelar</button>
      <button onclick="guardarTransaccion(${id})" class="btn btn-primary">Guardar Cambios</button>
    </div>
    <div id="ed-result" style="margin-top:10px"></div>
  `);
}

async function guardarTransaccion(id) {
  const tipo = document.getElementById("ed-tipo").value;
  const monto = parseFloat(document.getElementById("ed-monto").value);
  const referencia = document.getElementById("ed-ref").value;
  const fecha = document.getElementById("ed-fecha").value;
  const el = document.getElementById("ed-result");
  if (!monto || !referencia || !fecha) { el.innerHTML = `<p style="color:var(--warning);font-size:12px">Completa todos los campos</p>`; return; }
  el.innerHTML = `<div class="spinner"></div>`;
  try {
    await API.request(`/api/v1/motors/m2/transactions/${id}`, {
      method: "PUT",
      body: JSON.stringify({ tipo, monto, referencia, empresa_id: EMPRESA_ID, fecha_transaccion: fecha })
    });
    cerrarModal();
    showToast("✏️ Transacción actualizada");
    Pages.tesoreria();
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger);font-size:12px">❌ ${e.message}</p>`;
  }
}

// Editar fila completa M5 — Impuesto
function editarImpuesto(id, tipo, periodo, base, alicuota) {
  abrirModal(`
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <div style="font-size:15px;font-weight:700;color:var(--white)">✏️ Editar Impuesto #${id}</div>
      <button onclick="cerrarModal()" style="background:none;border:none;color:var(--gray-400);font-size:20px;cursor:pointer;line-height:1">×</button>
    </div>
    <div class="grid-2" style="margin-bottom:16px">
      <div class="form-group">
        <label>Tipo de Impuesto</label>
        <select id="ed-tipo" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
          <option value="iva" ${tipo==='iva'?'selected':''}>IVA</option>
          <option value="ingresos_brutos" ${tipo==='ingresos_brutos'?'selected':''}>Ingresos Brutos</option>
          <option value="ganancias" ${tipo==='ganancias'?'selected':''}>Ganancias</option>
          <option value="afip" ${tipo==='afip'?'selected':''}>AFIP General</option>
        </select>
      </div>
      <div class="form-group">
        <label>Período (AAAA-MM)</label>
        <input id="ed-periodo" type="text" value="${periodo}" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
      </div>
      <div class="form-group">
        <label>Base Imponible ($)</label>
        <input id="ed-base" type="number" value="${base}" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
      </div>
      <div class="form-group">
        <label>Alícuota (%)</label>
        <input id="ed-alicuota" type="number" value="${(alicuota * 100).toFixed(2)}" step="0.01" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
      </div>
    </div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      <button onclick="cerrarModal()" class="btn" style="background:var(--navy-3);color:var(--gray-400)">Cancelar</button>
      <button onclick="guardarImpuesto(${id})" class="btn btn-primary">Guardar Cambios</button>
    </div>
    <div id="ed-result" style="margin-top:10px"></div>
  `);
}

async function guardarImpuesto(id) {
  const tipo = document.getElementById("ed-tipo").value;
  const periodo = document.getElementById("ed-periodo").value;
  const base = parseFloat(document.getElementById("ed-base").value);
  const alicuota = parseFloat(document.getElementById("ed-alicuota").value) / 100;
  const el = document.getElementById("ed-result");
  if (!periodo || !base || !alicuota) { el.innerHTML = `<p style="color:var(--warning);font-size:12px">Completa todos los campos</p>`; return; }
  el.innerHTML = `<div class="spinner"></div>`;
  try {
    await API.request(`/api/v1/motors/m5/impuestos/${id}`, {
      method: "PUT",
      body: JSON.stringify({ tipo_impuesto: tipo, periodo, base_imponible: base, alicuota, empresa_id: EMPRESA_ID, fecha_vencimiento: new Date().toISOString().split('T')[0] })
    });
    cerrarModal();
    showToast("✏️ Impuesto actualizado");
    Pages.fiscal();
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger);font-size:12px">❌ ${e.message}</p>`;
  }
}

// Editar fila completa M6 — Activo
function editarActivo(id, tipo, desc, vlibro, vmercado) {
  abrirModal(`
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <div style="font-size:15px;font-weight:700;color:var(--white)">✏️ Editar Activo #${id}</div>
      <button onclick="cerrarModal()" style="background:none;border:none;color:var(--gray-400);font-size:20px;cursor:pointer;line-height:1">×</button>
    </div>
    <div class="grid-2" style="margin-bottom:16px">
      <div class="form-group">
        <label>Tipo</label>
        <select id="ed-tipo" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
          <option value="inmueble" ${tipo==='inmueble'?'selected':''}>Inmueble</option>
          <option value="vehiculo" ${tipo==='vehiculo'?'selected':''}>Vehículo</option>
          <option value="maquinaria" ${tipo==='maquinaria'?'selected':''}>Maquinaria</option>
          <option value="equipo" ${tipo==='equipo'?'selected':''}>Equipo Informático</option>
          <option value="otros" ${tipo==='otros'?'selected':''}>Otros</option>
        </select>
      </div>
      <div class="form-group">
        <label>Descripción</label>
        <input id="ed-desc" type="text" value="${desc}" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
      </div>
      <div class="form-group">
        <label>Valor en Libros ($)</label>
        <input id="ed-vlibro" type="number" value="${vlibro}" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
      </div>
      <div class="form-group">
        <label>Valor de Mercado ($)</label>
        <input id="ed-vmercado" type="number" value="${vmercado}" style="width:100%;background:var(--navy);border:1px solid var(--navy-3);border-radius:8px;padding:9px 12px;color:var(--white)">
      </div>
    </div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      <button onclick="cerrarModal()" class="btn" style="background:var(--navy-3);color:var(--gray-400)">Cancelar</button>
      <button onclick="guardarActivo(${id})" class="btn btn-primary">Guardar Cambios</button>
    </div>
    <div id="ed-result" style="margin-top:10px"></div>
  `);
}

async function guardarActivo(id) {
  const tipo = document.getElementById("ed-tipo").value;
  const desc = document.getElementById("ed-desc").value;
  const vlibro = parseFloat(document.getElementById("ed-vlibro").value);
  const vmercado = parseFloat(document.getElementById("ed-vmercado").value);
  const el = document.getElementById("ed-result");
  if (!desc || !vlibro || !vmercado) { el.innerHTML = `<p style="color:var(--warning);font-size:12px">Completa todos los campos</p>`; return; }
  el.innerHTML = `<div class="spinner"></div>`;
  try {
    await API.request(`/api/v1/motors/m6/activos/${id}`, {
      method: "PUT",
      body: JSON.stringify({ tipo_activo: tipo, descripcion: desc, valor_libro: vlibro, valor_mercado: vmercado, empresa_id: EMPRESA_ID })
    });
    cerrarModal();
    showToast("✏️ Activo actualizado");
    Pages.patrimonio();
  } catch (e) {
    el.innerHTML = `<p style="color:var(--danger);font-size:12px">❌ ${e.message}</p>`;
  }
}

// ===== HELPERS =====
function setPage(title, html) {
  document.getElementById("topbar-title").textContent = title;
  document.getElementById("content").innerHTML = html;
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

window.Pages = Pages;
window.runPortfolioDemo = runPortfolioDemo;
window.runPaymentsDemo = runPaymentsDemo;
window.runResourcesDemo = runResourcesDemo;
window.runFraudDetection = runFraudDetection;
window.agregarTransaccion = agregarTransaccion;
window.agregarImpuesto = agregarImpuesto;
window.agregarActivo = agregarActivo;
window.borrarTransaccion = borrarTransaccion;
window.borrarImpuesto = borrarImpuesto;
window.borrarActivo = borrarActivo;
window.editarTransaccion = editarTransaccion;
window.editarImpuesto = editarImpuesto;
window.editarActivo = editarActivo;
window.guardarTransaccion = guardarTransaccion;
window.guardarImpuesto = guardarImpuesto;
window.guardarActivo = guardarActivo;
window.abrirModal = abrirModal;
window.cerrarModal = cerrarModal;
