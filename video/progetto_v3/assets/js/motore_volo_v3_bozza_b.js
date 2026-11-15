/* MoVi video v3 (volo ad alta velocita'): motore e componenti nuovi, funzioni pure del tempo.
 * VistaPianta + VistaQuota + ScieVeloci disegnano SOLO dai registri veri (window.__VOLO, simulati);
 * CurvaConfidenza e BarreLatenza sono SCHEMATIC, con le cifre di window.__CIFRE (cifre.json).
 * Palette di componenti_v10.js (nessuna tinta fra 90 e 160 gradi). Nessun orologio, nessun caso, nessuna rete. */
(function () {
  "use strict";
  const COL = { fondo: "#0B0F17", pannello: "#121826", bordo: "#24344A", testo: "#E8EDF2", testo2: "#AEB8C5",
    visto: "#3DD6E8", nonvisto: "#F5A524", avviso: "#C7841A", persa: "#FF6B6B", nonoss: "#8A97A8", vero: "#E8EDF2",
    segnaposto: "#FF4FD8", coop: "#A99CFF" };
  const MONO = "JBMonoLocale, monospace", SANS = "InterLocale, sans-serif";
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const f1 = (x) => (Math.round(x * 10) / 10).toFixed(1);
  const cl = (x, a, b) => Math.max(a, Math.min(b, x));
  const ease = (x) => { x = cl(x, 0, 1); return x * x * (3 - 2 * x); };
  function T(x, y, s, o) {
    if (s == null || s === "") return ""; o = o || {};
    const fam = o.mono ? MONO : SANS, size = o.size || 28, w = o.weight || (o.mono ? 700 : 600);
    const txt = esc(s).replace(/\[(PENDING[^\]]*)\]/g, (m) => `<tspan fill="${COL.segnaposto}">${m}</tspan>`);
    return `<text x="${f1(x)}" y="${f1(y)}" font-family="${fam}" font-size="${size}" font-weight="${w}" fill="${o.fill || COL.testo}" text-anchor="${o.anchor || "start"}" opacity="${o.op == null ? 1 : o.op}">${txt}</text>`;
  }
  const R = (x, y, w, h, o) => { o = o || {}; return `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" fill="${o.fill || COL.pannello}" stroke="${o.stroke || COL.bordo}" stroke-width="${o.sw || 2}" rx="${o.rx == null ? 6 : o.rx}" opacity="${o.op == null ? 1 : o.op}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ""}/>`; };
  const C = (x, y, r, o) => { o = o || {}; return `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(Math.max(0.5, r))}" fill="${o.fill || "none"}" stroke="${o.stroke || "none"}" stroke-width="${o.sw || 2}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ""} opacity="${o.op == null ? 1 : o.op}"/>`; };
  const L = (x1, y1, x2, y2, o) => { o = o || {}; return `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${o.stroke || COL.bordo}" stroke-width="${o.sw || 2}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ""} opacity="${o.op == null ? 1 : o.op}"/>`; };
  function proiettore(bb, r, m) {
    m = m == null ? 24 : m; const [x0, y0, x1, y1] = bb, W = r.w - 2 * m, H = r.h - 2 * m;
    const s = Math.min(W / (x1 - x0), H / (y1 - y0));
    const ox = r.x + m + (W - s * (x1 - x0)) / 2, oy = r.y + m + (H - s * (y1 - y0)) / 2;
    return { s, x: (x) => ox + (x - x0) * s, y: (y) => oy + (y1 - y) * s, r: (d) => d * s };
  }
  function clipDef(id, r) { return `<defs><clipPath id="${id}"><rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}"/></clipPath></defs>`; }
  function scala(P, r, metri, lab) { // tacca grafica della scala
    const w = P.r(metri), x = r.x + r.w - w - 130, y = r.y + 30;
    return L(x, y, x + w, y, { stroke: COL.testo2, sw: 3 }) + L(x, y - 7, x, y + 7, { stroke: COL.testo2 }) + L(x + w, y - 7, x + w, y + 7, { stroke: COL.testo2 }) + T(x + w + 10, y + 8, lab, { mono: true, size: 20, fill: COL.testo2 });
  }

  /* ---------- registro: fotogramma con «tieni l'ultimo» ---------- */
  function fotogramma(sc, treg) {
    const F = window.__VOLO[sc].fotogrammi; let lo = 0, hi = F.length - 1;
    if (treg <= F[0].t) return { f: F[0], i: 0, F };
    while (lo < hi) { const m = (lo + hi + 1) >> 1; if (F[m].t <= treg + 1e-6) lo = m; else hi = m - 1; }
    return { f: F[lo], i: lo, F };
  }

  /* ---------- VistaPianta / VistaQuota con ScieVeloci ---------- */
  function vista(sc, treg, r, bb, asse, opz) {
    // asse: "xy" = pianta, "xz" = quota (distanza-altezza)
    const { f, i, F } = fotogramma(sc, treg), P = proiettore(bb, r, 20), id = "cp" + sc + asse;
    const X = (p) => P.x(p[0]), Y = (p) => P.y(asse === "xy" ? p[1] : p[2]);
    let s = R(r.x, r.y, r.w, r.h) + clipDef(id, r) + `<g clip-path="url(#${id})">`;
    if (asse === "xz") s += L(r.x, P.y(0), r.x + r.w, P.y(0), { stroke: COL.nonoss, sw: 2 }); // suolo
    // evento: volume V e impronta (solo se il registro li porta)
    if (f.ev && f.ev.c) {
      const cx = P.x(f.ev.c[0]);
      if (asse === "xy") {
        s += C(cx, P.y(f.ev.c[1]), P.r(f.ev.R), { stroke: COL.avviso, sw: 3, dash: "14 10" });
        s += C(cx, P.y(f.ev.c[1]), P.r(f.ev.rV), { stroke: COL.avviso, sw: 3, fill: COL.avviso, op: 0.3 });
      } else {
        s += R(cx - P.r(f.ev.rV), P.y(f.ev.zmax), 2 * P.r(f.ev.rV), P.r(f.ev.zmax - f.ev.zmin), { fill: COL.avviso, stroke: COL.avviso, op: 0.3, rx: 0 });
        s += L(cx - P.r(f.ev.R), P.y(0) - 4, cx + P.r(f.ev.R), P.y(0) - 4, { stroke: COL.avviso, sw: 8, dash: "14 10" });
      }
    }
    // verita' (solo montaggio)
    for (const k in f.v) { const p = f.v[k], x = X(p), y = Y(p); s += L(x - 9, y, x + 9, y, { stroke: COL.vero, sw: 2, op: 0.7 }) + L(x, y - 9, x, y + 9, { stroke: COL.vero, sw: 2, op: 0.7 }); }
    // tracce
    const occ = [];
    for (const k of f.tr) {
      const [tid, x, y, z, nv, vista, rP] = k, p = [x, y, z], px = X(p), py = Y(p);
      if (vista) {
        // ScieVeloci: 3 s di passato visto della stessa traccia, mai il futuro
        let pts = [];
        for (let j = i; j >= 0 && F[i].t - F[j].t <= 3.0; j -= 2) { const q = F[j].tr.find((u) => u[0] === tid && u[5]); if (q) pts.push(q); }
        for (let j = 1; j < pts.length; j++) { const a = pts[j - 1], b = pts[j]; s += L(X(a.slice(1)), Y(a.slice(1)), X(b.slice(1)), Y(b.slice(1)), { stroke: COL.visto, sw: 4, op: 0.8 * (1 - j / pts.length) }); }
        s += C(px, py, 9, { fill: COL.visto });
      } else {
        s += C(px, py, Math.max(12, P.r(rP)), { stroke: COL.nonvisto, sw: 3, dash: "10 8", op: 0.9 });
        s += `<circle cx="${f1(px)}" cy="${f1(py)}" r="${f1(Math.max(12, P.r(rP)))}" fill="${COL.nonvisto}" opacity="0.07"/>`;
        s += C(px, py, 6, { stroke: COL.nonvisto, sw: 3 });
      }
    }
    s += "</g>";
    // etichette sopra (solo pianta), al piu' 4, senza sovrapposizioni grossolane
    if (asse === "xy" && opz && opz.etichette) {
      let n = 0;
      const ord = f.tr.slice().sort((a, b) => (b[5] - a[5]) || (a[4] - b[4]));
      for (const k of ord) {
        if (n >= 4) break; const [tid, x, y, z, nv, vista, rP] = k; let px = cl(P.x(x), r.x + 10, r.x + r.w - 330), py = cl(P.y(y) - 22, r.y + 60, r.y + r.h - 90);
        while (occ.some((q) => Math.abs(q - py) < 34)) py += 34; if (py > r.y + r.h - 60) continue; occ.push(py);
        const lab = vista ? "SEEN" : `NOT SEEN · ${nv.toFixed(1)} s · region ${Math.round(rP)} m`;
        s += R(px + 14, py - 24, lab.length * 13.2 + 16, 34, { fill: COL.fondo, stroke: "none", op: 0.85, rx: 3 }) + T(px + 22, py, lab, { mono: true, size: 22, fill: vista ? COL.visto : COL.nonvisto }); n++;
      }
    }
    if (opz && opz.scala) s += scala(P, r, opz.scala[0], opz.scala[1]);
    s += T(r.x + 14, r.y + 32, asse === "xy" ? "PLAN VIEW" : "ALTITUDE VIEW (distance–height)", { mono: true, size: 20, fill: COL.testo2 });
    return s;
  }

  /* ---------- console: sensori, avviso, evento ---------- */
  function console_(sc, treg, r, extra) {
    const { f } = fotogramma(sc, treg); let s = R(r.x, r.y, r.w, r.h), y = r.y + 40;
    s += T(r.x + 18, y, `t = ${f.t.toFixed(1)} s (simulated)`, { mono: true, size: 22, fill: COL.testo2 }); y += 40;
    const nomi = { radar_sorveglianza_droni: "RADAR", camera_eo_ottica_lunga: "EO CAMERA", camera_termica_ottica_lunga: "THERMAL CAMERA" };
    for (const k in f.af) { const ok = f.af[k]; s += T(r.x + 18, y, `${nomi[k] || k}: ${ok ? "reliable" : "RELIABILITY LOST"}`, { mono: true, size: 24, fill: ok ? COL.testo2 : COL.persa }); y += 34; }
    if (f.ap && f.t >= f.ap[0]) { s += T(r.x + 18, y + 6, `PROXIMITY WARNING at ${f.ap[0].toFixed(1)} s`, { mono: true, size: 24, fill: COL.nonvisto }); y += 32; s += T(r.x + 18, y + 6, `predicted min. distance ${Math.round(f.ap[2])} m, ${Math.round(f.ap[1])} s ahead`, { mono: true, size: 22, fill: COL.nonvisto }); y += 40; }
    if (f.ev) { s += T(r.x + 18, y + 6, `EVENT: ${String(f.ev.tipo).replace("avaria o fiammata (dedotto)", "FAILURE OR FLASH · INFERRED")} at ${f.ev.t} s`, { mono: true, size: 24, fill: COL.avviso }); y += 34; s += T(r.x + 18, y + 6, `debris volume r ${Math.round(f.ev.rV)} m · footprint R ${(f.ev.R / 1000).toFixed(1)} km`, { mono: true, size: 22, fill: COL.avviso }); y += 30; s += T(r.x + 18, y + 6, "not verified: possible presence", { mono: true, size: 22, fill: COL.avviso }); y += 40; }
    if (extra) for (const e of extra) if (treg >= (e.da || -1e9)) { s += T(r.x + 18, y + 6, e.s, { mono: true, size: 22, fill: e.c || COL.testo }); y += 32; }
    return s;
  }

  /* ---------- CurvaConfidenza (SCHEMATIC, scena chiave) ---------- */
  function grafico(r, xs, ys, xmax, ymax, opz) {
    const px = (x) => r.x + 70 + (x / xmax) * (r.w - 100), py = (y) => r.y + r.h - 40 - (y / ymax) * (r.h - 80);
    let s = R(r.x, r.y, r.w, r.h) + L(px(0), py(0), px(xmax), py(0), { stroke: COL.testo2 }) + L(px(0), py(0), px(0), py(ymax), { stroke: COL.testo2 });
    for (const xt of opz.xt) s += T(px(xt), py(0) + 28, String(xt), { mono: true, size: 18, fill: COL.testo2, anchor: "middle" });
    for (const yt of opz.yt) s += T(px(0) - 10, py(yt) + 6, String(yt), { mono: true, size: 18, fill: COL.testo2, anchor: "end" });
    s += T(r.x + 16, r.y + 28, opz.titolo, { size: 22, fill: COL.testo });
    s += T(px(xmax), py(0) + 28, "τ (s)", { mono: true, size: 18, fill: COL.testo2, anchor: "end" });
    return { s, px, py };
  }
  function curva(t, D, cf) {
    let s = ""; const tau = 30 * ease((t - 1.5) / (D - 6)); // tau mostrato 0 -> 30 s
    const esC = cf["CONF-ESEMPIO"].valore;
    // sinistra: zona che cresce (schema, raggi calcolati dall'esempio IMM)
    const r0 = { x: 40, y: 100, w: 1060, h: 700 }; s += R(r0.x, r0.y, r0.w, r0.h);
    s += T(r0.x + 14, r0.y + 32, "PLAN VIEW · schematic, radii computed in the model", { mono: true, size: 20, fill: COL.testo2 });
    const cx = 420, cy = 450, sc = 0.30; // px per metro
    s += L(60, cy, cx, cy, { stroke: COL.visto, sw: 4, op: 0.6 }) + C(cx, cy, 9, { fill: COL.visto, op: tau < 0.2 ? 1 : 0.35 });
    const rz = interp(esC.tau_s, esC.r09_m, tau), xp = cx + 9 * tau; // previsione lungo la rotta (schema)
    s += C(cx, cy, 300 * sc, { stroke: COL.nonoss, sw: 3, dash: "6 6" }) + T(cx, cy + 300 * sc + 30, "zone declared at loss · 300 m", { mono: true, size: 20, fill: COL.nonoss, anchor: "middle" });
    s += `<circle cx="${f1(xp)}" cy="${cy}" r="${f1(Math.max(8, rz * sc))}" fill="${COL.nonvisto}" opacity="0.08"/>` + C(xp, cy, Math.max(8, rz * sc), { stroke: COL.nonvisto, sw: 3, dash: "12 8" });
    s += T(cl(xp, 200, 900), cl(cy - rz * sc - 18, 150, 760), `NOT SEEN · ${tau.toFixed(1)} s · r0.9 = ${Math.round(rz)} m`, { mono: true, size: 24, fill: COL.nonvisto, anchor: "middle" });
    s += T(r0.x + 20, r0.y + r0.h - 56, "aircraft at 80 m/s turning · radar σ 7.5 m (worked example)", { mono: true, size: 20, fill: COL.testo2 });
    s += T(r0.x + 20, r0.y + r0.h - 24, "σ²(τ) = σ0² + 2σ0v·τ + σv²·τ² + q·τ³/3     C(τ) = 1 − exp(−r²/2σ²(τ))", { mono: true, size: 22, fill: COL.testo });
    // destra in alto: C della zona fissa
    const g1 = grafico({ x: 1130, y: 100, w: 750, h: 220 }, null, null, 30, 1, { xt: [0, 5, 10, 20, 30], yt: [0, 0.5, 1], titolo: "Confidence in the fixed zone, C(τ) · computed" });
    s += g1.s + poli(esC.tau_s, esC.C, g1, tau, COL.testo2);
    // destra al centro: raggio r0.9
    const g2 = grafico({ x: 1130, y: 335, w: 750, h: 220 }, null, null, 30, 1100, { xt: [0, 5, 10, 20, 30], yt: [0, 500, 1000], titolo: "Region kept at 0.9: radius r0.9(τ) in m · computed" });
    s += g2.s + poli(esC.tau_s, esC.r09_m, g2, tau, COL.nonvisto);
    // destra in basso: verifica su 16 aerei reali
    const g3 = grafico({ x: 1130, y: 570, w: 750, h: 230 }, null, null, 30, 0.5, { xt: [0, 5, 10, 20, 30], yt: [], titolo: "Contained on 16 real aircraft (ADS-B, simulated sensor)" });
    const py3 = g3.py; g3.py = (y) => py3(y - 0.5);
    for (const yt of [0.5, 0.75, 1]) s += T(g3.px(0) - 10, g3.py(yt) + 6, String(yt), { mono: true, size: 18, fill: COL.testo2, anchor: "end" });
    s += g3.s + L(g3.px(0), g3.py(0.9), g3.px(30), g3.py(0.9), { stroke: COL.testo2, dash: "8 6" }) + T(g3.px(30), g3.py(0.9) - 8, "level 0.9", { mono: true, size: 16, fill: COL.testo2, anchor: "end" });
    const pv = cf["CONF-REALI"].valore;
    for (const b of pv) {
      const xm = (b.da + b.a) / 2; if (tau < b.da) continue;
      const x = g3.px(xm), c = b.classe === "L" ? COL.persa : COL.visto;
      s += L(x, g3.py(b.w[0]), x, g3.py(b.w[1]), { stroke: c, sw: 3 }) + C(x, g3.py(b.p), 7, { stroke: c, sw: 3, fill: COL.fondo });
      s += T(x, g3.py(b.p) - 16 - (b.classe === "L" ? 0 : 0), b.p.toFixed(2) + (b.classe === "L" ? " limit" : ""), { mono: true, size: 18, fill: c, anchor: "middle" });
    }
    s += T(1140, 830, "Wilson 95 %, cases correlated per aircraft (optimistic) · limits: 0.71 at 1–2 s, 0.78 in turns at 6–10 s", { mono: true, size: 18, fill: COL.testo2 });
    s += T(1140, 852, "[PENDING: calibrated curve, f20-chiusura/02-taratura/curva_video.json]", { mono: true, size: 18 });
    return s;
  }
  function interp(xs, ys, x) { if (x <= xs[0]) return ys[0]; for (let i = 1; i < xs.length; i++) if (x <= xs[i]) { const u = (x - xs[i - 1]) / (xs[i] - xs[i - 1]); return ys[i - 1] + u * (ys[i] - ys[i - 1]); } return ys[ys.length - 1]; }
  function poli(xs, ys, g, tau, col) {
    let d = "", s = ""; for (let i = 0; i < xs.length; i++) { if (xs[i] > tau + 1e-9 && i > 0) { const y = interp(xs, ys, tau); d += ` L${f1(g.px(tau))},${f1(g.py(y))}`; break; } d += (i ? " L" : "M") + `${f1(g.px(xs[i]))},${f1(g.py(ys[i]))}`; }
    s += `<path d="${d}" fill="none" stroke="${col}" stroke-width="4"/>`;
    for (let i = 0; i < xs.length; i++) if (xs[i] <= tau) s += C(g.px(xs[i]), g.py(ys[i]), 5, { fill: col });
    s += L(g.px(tau), g.py(0), g.px(tau), g.py(g.py ? 1e9 : 0) , { op: 0 });
    return s;
  }

  /* ---------- BarreLatenza (SCHEMATIC) ---------- */
  function barre(t, cf) {
    const B = cf["LAT-BARRE"].valore, max = 750, x0 = 520, W = 1300; let s = "", y = 190;
    const pal = [COL.nonoss, COL.testo2, COL.coop, COL.visto, COL.nonvisto, "#5E6A7B"];
    s += T(80, 150, "First warning to a machine, worst case (ms) · ESTIMATES BY ANALOGY, NO MEASUREMENT", { mono: true, size: 24, fill: COL.testo2 });
    B.righe.forEach((riga, k) => {
      const u = ease((t - 1 - k * 1.2) / 2.5); let x = x0;
      s += T(80, y + 44, riga.nome, { size: 26 });
      riga.seg.forEach((g, j) => { const w = (g[1] / max) * W * u; if (w > 0.3) s += R(x, y + 10, w, 50, { fill: pal[j % pal.length], stroke: COL.fondo, sw: 1, rx: 0, op: 0.9 }); x += w; });
      s += T(x + 12, y + 46, u > 0.98 ? `≈ ${riga.tot} ms` : "", { mono: true, size: 24 }); y += 120;
    });
    let lx = 80; B.legenda.forEach((n, j) => { s += R(lx, y + 4, 22, 22, { fill: pal[j], stroke: "none", rx: 2 }) + T(lx + 30, y + 22, n, { mono: true, size: 20, fill: COL.testo2 }); lx += n.length * 12.5 + 70; });
    // riquadro d'ingrandimento sul calcolo
    const z = { x: 80, y: y + 60, w: 1760, h: 190 }; s += R(z.x, z.y, z.w, z.h, { dash: "8 6" });
    s += T(z.x + 20, z.y + 40, "ZOOM · processing only (signal + plots + tracking)", { mono: true, size: 22, fill: COL.testo2 });
    s += T(z.x + 20, z.y + 90, cf["LAT-CPU"].testo_schermo, { mono: true, size: 26 });
    s += T(z.x + 20, z.y + 130, cf["LAT-DED"].testo_schermo, { mono: true, size: 26, fill: COL.nonvisto });
    s += T(z.x + 20, z.y + 170, cf["LAT-ANALOGIA"].testo_schermo, { mono: true, size: 20, fill: COL.testo2 });
    return s;
  }

  /* ---------- scene ---------- */
  function etichetta_onesta(o) {
    if (o === "sim") return T(1880, 44, "SIMULATION", { mono: true, size: 26, fill: COL.nonvisto, anchor: "end" }) + T(1880, 74, "Simulated · state-of-the-art sensor parameters assumed · no physical sensor", { mono: true, size: 20, fill: COL.testo2, anchor: "end" });
    return T(1880, 44, "SCHEMATIC", { mono: true, size: 26, fill: COL.testo2, anchor: "end" }) + (o && o !== "schema" ? T(1880, 74, o, { mono: true, size: 20, fill: COL.testo2, anchor: "end" }) : "");
  }
  function contatore(righe, t) {
    let s = "", y = 850; for (const r of righe) { if (t < (r.da || 0)) continue; const op = ease((t - (r.da || 0)) / 0.6);
      s += T(60, y, r.s, { mono: true, size: r.size || 26, fill: r.c || COL.testo, op }); y += (r.size || 26) + 12; }
    return s;
  }
  function scenaDati(sc, cfg, t) {
    const treg = cfg.t0 + t * cfg.vel;
    let s = vista(sc, treg, { x: 40, y: 100, w: 1100, h: 700 }, cfg.bbxy, "xy", { etichette: true, scala: cfg.scala });
    s += vista(sc, treg, { x: 1160, y: 100, w: 720, h: 330 }, cfg.bbxz, "xz", {});
    s += console_(sc, treg, { x: 1160, y: 445, w: 720, h: 355 }, cfg.extra ? cfg.extra.map((e) => ({ ...e, da: e.treg })) : null);
    s += T(60, 790, "+ truth (simulation only, MoVi does not see it)   ● seen   ◌ not seen: region where it can be", { mono: true, size: 18, fill: COL.testo2 });
    return s;
  }
  function tre(t) {
    let s = ""; const it = [["I SEE IT", "seen", COL.visto], ["I DON'T SEE IT · HERE IS WHERE IT CAN BE", "not seen", COL.nonvisto], ["I DON'T KNOW", "unknown", COL.nonoss]];
    it.forEach((v, k) => { const op = ease((t - 1.5 - k * 2.2) / 0.8), y = 300 + k * 190, x = 360;
      if (k === 0) s += C(x, y, 22, { fill: v[2], op }); else if (k === 1) s += C(x, y, 60, { stroke: v[2], sw: 4, dash: "12 8", op }) + C(x, y, 7, { stroke: v[2], sw: 3, op }); else s += R(x - 60, y - 50, 120, 100, { fill: "none", stroke: v[2], dash: "4 6", op }) + T(x, y + 14, "?", { size: 48, fill: v[2], anchor: "middle", op });
      s += T(480, y + 12, v[0], { mono: true, size: 40, fill: v[2], op }); });
    s += T(480, 860, "not observed ≠ clear", { mono: true, size: 34, fill: COL.testo, op: ease((t - 9) / 0.8) });
    return s;
  }
  function schede(t, cf) {
    const K = cf["SITO-SCHEDE"].valore; let s = "";
    K.forEach((k, j) => { const op = ease((t - 0.8 - j * 2.5) / 0.8), x = 60 + j * 610;
      s += `<g opacity="${op}">` + R(x, 160, 580, 560) + T(x + 24, 210, k.titolo, { size: 30 });
      k.righe.forEach((r, i) => { s += T(x + 24, 280 + i * 44, r, { mono: true, size: 22, fill: i === 0 ? COL.testo : COL.testo2 }); });
      s += T(x + 24, 690, k.etichetta, { mono: true, size: 20, fill: COL.nonvisto }) + "</g>"; });
    return s;
  }
  function chiusura(t, D, cf) {
    let s = ""; const lim = cf["LIMITI"].valore, sc = cf["SCALA"].valore, fine = D - 6.5;
    if (t < fine) {
      s += T(60, 160, "LIMITS", { mono: true, size: 30, fill: COL.persa });
      lim.forEach((l, i) => { s += T(60, 220 + i * 48, "· " + l, { size: 26, op: ease((t - 0.5 - i * 0.8) / 0.5) }); });
      s += T(1060, 160, "FROM PROTOTYPE TO DEPLOYED SYSTEM", { mono: true, size: 30, fill: COL.visto });
      sc.forEach((g, i) => { const op = ease((t - 4 - i * 1.5) / 0.6), y = 700 - i * 150, x = 1060 + i * 60;
        s += `<g opacity="${op}">` + R(x, y - 60, 760 - i * 60, 120) + T(x + 20, y - 18, g[0], { size: 28 }) + T(x + 20, y + 24, g[1], { mono: true, size: 20, fill: COL.testo2 }) + "</g>"; });
    } else {
      const u = ease((t - fine) / 1.0), M = window.__MARCHIO || {};
      if (M.wordmark) s += `<image href="${M.wordmark}" x="${960 - 300}" y="260" width="600" height="250" opacity="${u}"/>`;
      s += T(960, 600, "Seen, not seen, unknown: declared for every track.", { size: 36, anchor: "middle", op: u });
      s += T(960, 660, "Observes and warns · no output is a command", { mono: true, size: 24, fill: COL.testo2, anchor: "middle", op: u });
      s += T(960, 760, "By SDMs · Ignazio Crocchiolo · Federico Dellini · Danilo Amalfitano · Emanuele Ciotola · Pierfrancesco Amendola", { size: 22, fill: COL.testo2, anchor: "middle", op: u });
      s += T(960, 800, "The Big Hack 2026 · prototype built in one day · everything simulated", { size: 22, fill: COL.testo2, anchor: "middle", op: u });
    }
    return s;
  }
  function sottotitolo(tg) {
    const S = window.__SOTTO || []; const q = S.find((x) => tg >= x.a && tg < x.b); if (!q) return "";
    let righe = [q.s];
    if (q.s.length > 80) { const p = q.s.split(" "); let a = "", k = 0; while (k < p.length && (a + " " + p[k]).length < q.s.length / 2) { a = (a ? a + " " : "") + p[k]; k++; } righe = [a, p.slice(k).join(" ")]; }
    const w = Math.min(1840, Math.max(...righe.map((x) => x.length)) * 16 + 40), h = 46 * righe.length + 12, y0 = 1062 - h;
    let s = R(960 - w / 2, y0, w, h, { fill: "#000", stroke: "none", op: 0.7, rx: 4 });
    righe.forEach((x, i) => { s += T(960, y0 + 40 + i * 46, x, { size: 30, anchor: "middle" }); });
    return s;
  }

  function disegna(tg) {
    const SC = window.__SCENE_V3, cf = window.__CIFRE;
    let k = SC.length - 1; for (let i = 0; i < SC.length; i++) if (tg < SC[i].inizio + SC[i].durata) { k = i; break; }
    const S = SC[k], t = tg - S.inizio, D = S.durata;
    let s = `<rect x="0" y="0" width="1920" height="1080" fill="${COL.fondo}"/>`;
    const fin = Math.min(ease(t / 0.4), ease((D - t) / 0.3));
    s += `<g opacity="${f1(Math.max(0.05, fin))}">`;
    if (S.tipo === "dati") s += scenaDati(S.registro, S.cfg, t);
    else if (S.tipo === "tre") s += tre(t);
    else if (S.tipo === "curva") s += curva(t, D, cf);
    else if (S.tipo === "barre") s += barre(t, cf);
    else if (S.tipo === "schede") s += schede(t, cf);
    else if (S.tipo === "chiusura") s += chiusura(t, D, cf);
    if (S.titolo && !(S.tipo === "chiusura" && t >= D - 6.5)) s += T(40, 56, S.titolo, { size: 34 });
    if (!(S.tipo === "chiusura" && t >= D - 6.5)) s += etichetta_onesta(S.onesta);
    if (S.contatore) s += contatore(S.contatore, t);
    if (S.titolone && t < S.titolone) { const u = Math.min(1, (S.titolone - t) / 0.5);
      s += `<rect x="0" y="0" width="1920" height="1080" fill="${COL.fondo}" opacity="${f1(0.85 * u)}"/>`;
      const M = window.__MARCHIO || {}; if (M.wordmark) s += `<image href="${M.wordmark}" x="${960 - 240}" y="330" width="480" height="200" opacity="${u}"/>`;
      s += T(960, 620, "Fast flight: when continuity is lost", { size: 44, anchor: "middle", op: u }); }
    s += "</g>" + sottotitolo(tg);
    return s;
  }
  window.MoViMotore = { disegna };
})();
