/**
 * O-IAxis API Service — cliente HTTP para el backend FastAPI
 */

const BASE_URL = "http://localhost:8000";

const API = {
  // ===== AUTH TOKEN =====
  _token: null,

  setToken(t) { this._token = t; sessionStorage.setItem("oiaxis_token", t); },
  getToken()  { return this._token || sessionStorage.getItem("oiaxis_token"); },
  clearToken(){ this._token = null; sessionStorage.removeItem("oiaxis_token"); },

  // ===== HTTP =====
  async request(path, opts = {}) {
    const headers = { "Content-Type": "application/json", ...opts.headers };
    const token = this.getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${BASE_URL}${path}`, { ...opts, headers });

    if (!res.ok) {
      const detail = await res.text().catch(() => "Error");
      throw new Error(`${res.status}: ${detail}`);
    }
    return res.json();
  },

  get(path) { return this.request(path, { method: "GET" }); },

  post(path, body) {
    return this.request(path, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  // Form-encoded POST for OAuth2 login
  async postForm(path, body) {
    const params = new URLSearchParams(body);
    const res = await fetch(`${BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params.toString(),
    });
    if (!res.ok) {
      const detail = await res.json().catch(() => ({}));
      throw new Error(detail.detail || "Login fallido");
    }
    return res.json();
  },

  // ===== ENDPOINTS =====

  // Auth
  loginJWT(username, password) {
    return this.postForm("/api/v1/auth/token", { username, password });
  },

  // Health & Status
  health()  { return this.get("/health"); },
  status()  { return this.get("/api/v1/status"); },

  // M2 - Tesorería
  tesoreriaResumen(empresaId) { return this.get(`/api/v1/motors/m2/resumen/${empresaId}`); },
  tesoreriaTransactions(empresaId) { return this.get(`/api/v1/motors/m2/transactions?empresa_id=${empresaId}&limit=20`); },
  cajaDiaria(empresaId, fi, ff) { return this.get(`/api/v1/motors/m2/caja-diaria?empresa_id=${empresaId}&fecha_inicio=${fi}&fecha_fin=${ff}`); },

  // M5 - Fiscal
  fiscalResumen(empresaId) { return this.get(`/api/v1/motors/m5/resumen/${empresaId}`); },
  impuestos(empresaId) { return this.get(`/api/v1/motors/m5/impuestos?empresa_id=${empresaId}`); },
  obligaciones(empresaId) { return this.get(`/api/v1/motors/m5/obligaciones?empresa_id=${empresaId}`); },

  // M6 - Patrimonio
  activos(empresaId) { return this.get(`/api/v1/motors/m6/activos/${empresaId}`); },
  balance(empresaId) { return this.get(`/api/v1/motors/m6/balance/${empresaId}`); },

  // M7 - Crédito
  creditScore(empresaId, ingresos, deuda, historial) {
    return this.get(`/api/v1/motors/m7/credit-score?empresa_id=${empresaId}&ingresos_anuales=${ingresos}&deuda_total=${deuda}&historial_pago=${historial}`);
  },

  // M10 - Inversiones
  inversiones(empresaId) { return this.get(`/api/v1/motors/m10/inversiones/${empresaId}`); },

  // M11 - Fraude
  alertasFraude(empresaId) { return this.get(`/api/v1/motors/m11/alertas/${empresaId}`); },

  // ML
  predictCashFlow(data, periods = 12) {
    const params = data.map(v => `historical_data=${v}`).join("&");
    return this.post(`/api/v1/ml/predict/cash-flow?${params}&periods=${periods}`, {});
  },
  financialRisk(dte, cr, ic) {
    return this.post(`/api/v1/ml/assess/financial-risk?debt_to_equity=${dte}&current_ratio=${cr}&interest_coverage=${ic}`, {});
  },
  mlModels() { return this.get("/api/v1/ml/models/info"); },

  // Quantum
  quantumStatus() { return this.get("/api/v1/quantum/status"); },
  quantumPortfolio(body) { return this.post("/api/v1/quantum/optimize/portfolio", body); },
  quantumPayments(body) { return this.post("/api/v1/quantum/optimize/payments", body); },
  quantumResources(body) { return this.post("/api/v1/quantum/optimize/resources", body); },
};

window.API = API;
