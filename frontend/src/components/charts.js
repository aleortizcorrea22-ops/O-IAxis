/**
 * O-IAxis Charts — canvas-based, sin dependencias externas
 */

const Charts = {

  // ===== BARRA HORIZONTAL =====
  barH(canvasId, labels, values, color = "#00B4D8") {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const W = canvas.width = canvas.offsetWidth;
    const H = canvas.height = canvas.offsetHeight;

    ctx.clearRect(0, 0, W, H);

    const pad = 8;
    const maxVal = Math.max(...values, 1);
    const rowH = (H - pad * 2) / labels.length;

    labels.forEach((lbl, i) => {
      const y = pad + i * rowH;
      const barW = ((values[i] || 0) / maxVal) * (W * 0.55);

      // Bar
      ctx.fillStyle = color;
      ctx.globalAlpha = 0.85;
      ctx.beginPath();
      ctx.roundRect(W * 0.3, y + 4, barW, rowH - 10, 4);
      ctx.fill();
      ctx.globalAlpha = 1;

      // Label
      ctx.fillStyle = "#9FB3C8";
      ctx.font = "11px Inter, sans-serif";
      ctx.textAlign = "right";
      ctx.fillText(lbl, W * 0.27, y + rowH / 2 + 4);

      // Value
      ctx.fillStyle = "#E2EAF0";
      ctx.textAlign = "left";
      ctx.fillText(this._fmt(values[i] || 0), W * 0.3 + barW + 6, y + rowH / 2 + 4);
    });
  },

  // ===== LÍNEA =====
  line(canvasId, labels, datasets) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const W = canvas.width = canvas.offsetWidth;
    const H = canvas.height = canvas.offsetHeight;

    ctx.clearRect(0, 0, W, H);

    const padL = 50, padR = 16, padT = 16, padB = 30;
    const allVals = datasets.flatMap(d => d.values);
    const minV = Math.min(...allVals, 0);
    const maxV = Math.max(...allVals, 1);
    const range = maxV - minV || 1;

    const toX = i => padL + (i / (labels.length - 1)) * (W - padL - padR);
    const toY = v => padT + (1 - (v - minV) / range) * (H - padT - padB);

    // Grid lines
    ctx.strokeStyle = "rgba(255,255,255,.06)";
    ctx.lineWidth = 1;
    [0.25, 0.5, 0.75, 1].forEach(f => {
      const y = padT + f * (H - padT - padB);
      ctx.beginPath(); ctx.moveTo(padL, y); ctx.lineTo(W - padR, y); ctx.stroke();
      ctx.fillStyle = "#627D98";
      ctx.font = "10px Inter, sans-serif";
      ctx.textAlign = "right";
      ctx.fillText(this._fmt(maxV - f * range), padL - 4, y + 3);
    });

    // X labels
    ctx.fillStyle = "#627D98"; ctx.font = "10px Inter, sans-serif"; ctx.textAlign = "center";
    labels.forEach((lbl, i) => {
      if (i % Math.ceil(labels.length / 6) === 0)
        ctx.fillText(lbl, toX(i), H - 6);
    });

    // Dataset lines
    const colors = ["#00B4D8", "#22C55E", "#F59E0B", "#EF4444"];
    datasets.forEach((ds, di) => {
      const c = ds.color || colors[di % colors.length];
      const pts = ds.values.map((v, i) => ({ x: toX(i), y: toY(v) }));

      // Area fill
      ctx.beginPath();
      ctx.moveTo(pts[0].x, H - padB);
      pts.forEach(p => ctx.lineTo(p.x, p.y));
      ctx.lineTo(pts[pts.length - 1].x, H - padB);
      ctx.closePath();
      ctx.fillStyle = c + "22";
      ctx.fill();

      // Line
      ctx.beginPath();
      ctx.strokeStyle = c; ctx.lineWidth = 2;
      pts.forEach((p, i) => i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y));
      ctx.stroke();

      // Dots
      pts.forEach(p => {
        ctx.beginPath(); ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = c; ctx.fill();
      });
    });
  },

  // ===== DONUT =====
  donut(canvasId, segments) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const W = canvas.width = canvas.offsetWidth;
    const H = canvas.height = canvas.offsetHeight;

    ctx.clearRect(0, 0, W, H);

    const cx = W / 2, cy = H / 2, r = Math.min(W, H) * 0.38, ri = r * 0.6;
    const total = segments.reduce((s, g) => s + g.value, 0) || 1;
    const colors = ["#00B4D8", "#22C55E", "#F59E0B", "#EF4444", "#818CF8", "#FB7185"];

    let angle = -Math.PI / 2;
    segments.forEach((seg, i) => {
      const sweep = (seg.value / total) * Math.PI * 2;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, r, angle, angle + sweep);
      ctx.closePath();
      ctx.fillStyle = seg.color || colors[i % colors.length];
      ctx.fill();
      angle += sweep;
    });

    // Hole
    ctx.beginPath(); ctx.arc(cx, cy, ri, 0, Math.PI * 2);
    ctx.fillStyle = "#1B2B3E"; ctx.fill();

    // Legend
    const legY = H - 14;
    let legX = 8;
    segments.slice(0, 4).forEach((seg, i) => {
      const c = seg.color || colors[i % colors.length];
      ctx.fillStyle = c;
      ctx.fillRect(legX, legY, 10, 10);
      ctx.fillStyle = "#9FB3C8"; ctx.font = "10px Inter, sans-serif"; ctx.textAlign = "left";
      const lbl = seg.label.length > 10 ? seg.label.slice(0, 9) + "…" : seg.label;
      ctx.fillText(lbl, legX + 13, legY + 9);
      legX += ctx.measureText(lbl).width + 28;
    });
  },

  // ===== GAUGE =====
  gauge(canvasId, value, max = 100, label = "") {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const W = canvas.width = canvas.offsetWidth;
    const H = canvas.height = canvas.offsetHeight;

    ctx.clearRect(0, 0, W, H);

    const cx = W / 2, cy = H * 0.65, r = Math.min(W, H) * 0.4;
    const pct = Math.min(value / max, 1);
    const startA = Math.PI, endA = Math.PI * 2;
    const fillA = startA + pct * Math.PI;

    // Track
    ctx.beginPath(); ctx.arc(cx, cy, r, startA, endA);
    ctx.strokeStyle = "#243347"; ctx.lineWidth = 14; ctx.stroke();

    // Fill
    const color = pct > 0.7 ? "#22C55E" : pct > 0.4 ? "#F59E0B" : "#EF4444";
    ctx.beginPath(); ctx.arc(cx, cy, r, startA, fillA);
    ctx.strokeStyle = color; ctx.lineWidth = 14; ctx.stroke();

    // Value text
    ctx.fillStyle = "#FFFFFF"; ctx.font = `bold ${Math.round(W * 0.12)}px Inter, sans-serif`;
    ctx.textAlign = "center"; ctx.fillText(`${Math.round(pct * 100)}%`, cx, cy + 8);
    if (label) {
      ctx.fillStyle = "#9FB3C8"; ctx.font = `${Math.round(W * 0.07)}px Inter, sans-serif`;
      ctx.fillText(label, cx, cy + 28);
    }
  },

  // ===== HELPERS =====
  _fmt(v) {
    if (Math.abs(v) >= 1e6) return (v / 1e6).toFixed(1) + "M";
    if (Math.abs(v) >= 1e3) return (v / 1e3).toFixed(1) + "K";
    return v.toFixed(0);
  }
};

window.Charts = Charts;
