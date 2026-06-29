/**
 * O-IAxis Auth Service — JWT real (backend) con fallback demo offline
 */

const AUTH = {
  // Credenciales demo para testing (sin base de datos de usuarios aún)
  DEMO_USERS: [
    { username: "rodolfo",  password: "cto2024",   role: "CTO",   nombre: "Rodolfo" },
    { username: "admin",    password: "admin2024",  role: "Admin", nombre: "Admin" },
    { username: "demo",     password: "demo",       role: "Viewer",nombre: "Demo" },
  ],

  async login(username, password) {
    // Intentar JWT real desde backend
    try {
      const resp = await API.loginJWT(username, password);
      const session = { token: resp.access_token, user: { username, role: resp.role, nombre: resp.nombre } };
      sessionStorage.setItem("oiaxis_session", JSON.stringify(session));
      API.setToken(resp.access_token);
      return session;
    } catch (_) {
      // Fallback: demo offline si el backend no está disponible
    }

    const user = this.DEMO_USERS.find(
      u => u.username === username && u.password === password
    );
    if (!user) return null;

    const token = btoa(JSON.stringify({ sub: username, role: user.role, exp: Date.now() + 28800000 }));
    const session = { token, user: { username, role: user.role, nombre: user.nombre } };
    sessionStorage.setItem("oiaxis_session", JSON.stringify(session));
    API.setToken(token);
    return session;
  },

  logout() {
    sessionStorage.removeItem("oiaxis_session");
    API.clearToken();
  },

  getSession() {
    const raw = sessionStorage.getItem("oiaxis_session");
    if (!raw) return null;
    try { return JSON.parse(raw); } catch { return null; }
  },

  isAuthenticated() { return !!this.getSession(); },

  getRole() {
    const s = this.getSession();
    return s ? s.user.role : null;
  },

  getNombre() {
    const s = this.getSession();
    return s ? s.user.nombre : "Usuario";
  }
};

window.AUTH = AUTH;
