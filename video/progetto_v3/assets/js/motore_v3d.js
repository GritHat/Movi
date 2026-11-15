/* v3d (copia di motore_v3c.js, che resta): QA_V3C D4, REVISIONE_V3C C3, C4, C5; zoom F7 a 560 m.
 * MoVi video v3c (copia di motore_v3b.js, che resta): F7 dal registro F7r c1 cella totale (avviso non localizzato, sfera prudente),
 * giurato 8 (legenda delle regioni piene), 9 (etichette dentro il pannello), etichetta «0.9» non piu' toccata dalla riga d'evento. */
/* MoVi video v3b (correzioni QA_V3 e GIURATO_V3, copia di motore_finale.js che resta) · MoVi video v3 FINALE (volo ad alta velocita' + F7 «scorta»): motore, funzioni pure del tempo.
 * Derivato da motore_volo_v3.js (che resta). VistaPianta/VistaQuota/Scorta disegnano SOLO dai registri veri
 * (window.__VOLO, simulati); la curva della confidenza viene da window.__CURVA (curva_video.json, calcolata) e i punti
 * dalla banda osservata (traiettorie pubbliche, sensore simulato); le cifre a schermo SOLO da window.__CIFRE
 * (cifre_finale.json = blocco del verdetto finale). Lampo e fumo di F7 sono ILLUSTRATIVI e lo schermo lo dice.
 * Palette senza tinte fra 90 e 160 gradi (niente verde). Nessun orologio, nessun caso, nessuna rete. */
(function () {
  "use strict";
  const COL = { fondo: "#0B0F17", pannello: "#121826", bordo: "#24344A", testo: "#E8EDF2", testo2: "#AEB8C5",
    visto: "#3DD6E8", nonvisto: "#F5A524", avviso: "#C7841A", persa: "#FF6B6B", nonoss: "#8A97A8", vero: "#E8EDF2",
    coop: "#A99CFF", lampo: "#FFF4D6", fumo: "#6B7686" };
  const MONO = "JBMonoLocale, monospace", SANS = "InterLocale, sans-serif";
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const f1 = (x) => (Math.round(x * 10) / 10).toFixed(1);
  const cl = (x, a, b) => Math.max(a, Math.min(b, x));
  const ease = (x) => { x = cl(x, 0, 1); return x * x * (3 - 2 * x); };
  function T(x, y, s, o) {
    if (s == null || s === "") return ""; o = o || {};
    const fam = o.mono ? MONO : SANS, size = o.size || 28, w = o.weight || (o.mono ? 700 : 600);
    return `<text x="${f1(x)}" y="${f1(y)}" font-family="${fam}" font-size="${size}" font-weight="${w}" fill="${o.fill || COL.testo}" text-anchor="${o.anchor || "start"}" opacity="${o.op == null ? 1 : o.op}">${esc(s)}</text>`;
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
  function scala(P, r, metri, lab) {
    const w = P.r(metri), x = r.x + r.w - w - 130, y = r.y + 30;
    return L(x, y, x + w, y, { stroke: COL.testo2, sw: 3 }) + L(x, y - 7, x, y + 7, { stroke: COL.testo2 }) + L(x + w, y - 7, x + w, y + 7, { stroke: COL.testo2 }) + T(x + w + 10, y + 8, lab, { mono: true, size: 20, fill: COL.testo2 });
  }
  const vel_txt = (v) => (v > 1.05 ? `playback ×${v.toFixed(1)} (accelerated)` : v < 0.95 ? `playback ×${v.toFixed(2)} (slowed)` : "playback ×1");

  /* ---------- registro: fotogramma con «tieni l'ultimo» ---------- */
  function fotogramma(sc, treg) {
    const F = window.__VOLO[sc].fotogrammi; let lo = 0, hi = F.length - 1;
    if (treg <= F[0].t) return { f: F[0], i: 0, F };
    while (lo < hi) { const m = (lo + hi + 1) >> 1; if (F[m].t <= treg + 1e-6) lo = m; else hi = m - 1; }
    return { f: F[lo], i: lo, F };
  }

  /* ---------- VistaPianta / VistaQuota (F1, F3, F4, F5) ---------- */
  function vista(sc, treg, r, bb, asse, opz) {
    const { f, i, F } = fotogramma(sc, treg), P = proiettore(bb, r, 20), id = "cp" + sc + asse;
    const X = (p) => P.x(p[0]), Y = (p) => P.y(asse === "xy" ? p[1] : p[2]);
    let s = R(r.x, r.y, r.w, r.h) + clipDef(id, r) + `<g clip-path="url(#${id})">`;
    if (asse === "xz") s += L(r.x, P.y(0), r.x + r.w, P.y(0), { stroke: COL.nonoss, sw: 2 });
    if (f.ev && f.ev.c) {
      const cx = P.x(f.ev.c[0]);
      if (asse === "xy") {
        s += C(cx, P.y(f.ev.c[1]), P.r(f.ev.R), { stroke: COL.avviso, sw: 3, dash: "14 10" });
        s += C(cx, P.y(f.ev.c[1]), P.r(f.ev.rV), { stroke: COL.avviso, sw: 3, fill: COL.avviso, op: 0.15 });
      } else {
        s += R(cx - P.r(f.ev.rV), P.y(f.ev.zmax), 2 * P.r(f.ev.rV), P.r(f.ev.zmax - f.ev.zmin), { fill: COL.avviso, stroke: COL.avviso, op: 0.15, rx: 0 });
        s += L(cx - P.r(f.ev.R), P.y(0) - 4, cx + P.r(f.ev.R), P.y(0) - 4, { stroke: COL.avviso, sw: 8, dash: "14 10" });
      }
    }
    for (const k in f.v) { const p = f.v[k], x = X(p), y = Y(p); s += L(x - 9, y, x + 9, y, { stroke: COL.vero, sw: 2, op: 0.7 }) + L(x, y - 9, x, y + 9, { stroke: COL.vero, sw: 2, op: 0.7 }); }
    const ordine = f.tr.filter((u) => !u[5]).concat(f.tr.filter((u) => u[5]));
    for (const k of ordine) {
      const [tid, x, y, z, nv, vista, rP] = k, p = [x, y, z], px = X(p), py = Y(p);
      if (vista) {
        let pts = [];
        for (let j = i; j >= 0 && F[i].t - F[j].t <= 3.0; j -= 2) { const q = F[j].tr.find((u) => u[0] === tid && u[5]); if (q) pts.push(q); }
        for (let j = 1; j < pts.length; j++) { const a = pts[j - 1], b = pts[j]; s += L(X(a.slice(1)), Y(a.slice(1)), X(b.slice(1)), Y(b.slice(1)), { stroke: COL.visto, sw: 4, op: 0.8 * (1 - j / pts.length) }); }
        s += C(px, py, 9, { fill: COL.visto });
      } else {
        // difetto c1 della bozza: le regioni enormi delle tracce perse da molto velavano il pannello.
        // Ora: contorno sempre (dato vero), velo solo se la regione e' piccola; tracce perse da > 10 s in grigio.
        const rr = Math.max(12, P.r(rP)), vecchia = nv > 10, col = vecchia ? COL.nonoss : COL.nonvisto;
        s += C(px, py, rr, { stroke: col, sw: vecchia ? 2 : 3, dash: "10 8", op: vecchia ? 0.6 : 0.9 });
        if (rr < 260 && !vecchia) s += `<circle cx="${f1(px)}" cy="${f1(py)}" r="${f1(rr)}" fill="${COL.nonvisto}" opacity="0.07"/>`;
        s += C(px, py, 6, { stroke: col, sw: 3 });
      }
    }
    s += "</g>";
    if (asse === "xy" && opz && opz.etichette) {
      let n = 0; const occ = [];
      const ord = f.tr.slice().sort((a, b) => (b[5] - a[5]) || (a[4] - b[4]));
      for (const k of ord) {
        if (n >= 4) break; const [tid, x, y, z, nv, vista, rP] = k;
        const lab = vista ? "SEEN" : `NOT SEEN · ${nv.toFixed(1)} s · region ${rP >= 1000 ? (rP / 1000).toFixed(1) + " km" : Math.round(rP) + " m"}`, lw = lab.length * 13.2 + 16;
        let px = cl(P.x(x), r.x + 4, r.x + r.w - lw - 30), py = cl(P.y(y) - 22, r.y + 100, r.y + r.h - 90);
        while (occ.some((q) => Math.abs(q - py) < 36)) py += 36; if (py > r.y + r.h - 60) continue; occ.push(py);
        s += R(px + 14, py - 24, lw, 34, { fill: COL.fondo, stroke: "none", op: 0.85, rx: 3 }) + T(px + 22, py, lab, { mono: true, size: 22, fill: vista ? COL.visto : (nv > 10 ? COL.nonoss : COL.nonvisto) }); n++;
      }
    }
    if (opz && opz.scala) s += scala(P, r, opz.scala[0], opz.scala[1]);
    s += T(r.x + 14, r.y + 32, asse === "xy" ? `PLAN VIEW · ${vel_txt(opz && opz.vel || 1)}` : "ALTITUDE VIEW (distance–height)", { mono: true, size: 20, fill: COL.testo2 });
    return s;
  }

  function console_(sc, treg, r, extra) {
    const { f } = fotogramma(sc, treg); let s = R(r.x, r.y, r.w, r.h), y = r.y + 40;
    s += T(r.x + 18, y, `t = ${f.t.toFixed(1)} s · simulated run, log readout`, { mono: true, size: 22, fill: COL.testo2 }); y += 40;
    const nomi = { radar_sorveglianza_droni: "RADAR", camera_eo_ottica_lunga: "EO CAMERA", camera_termica_ottica_lunga: "THERMAL CAMERA" };
    for (const k in f.af) { const ok = f.af[k]; s += T(r.x + 18, y, `${nomi[k] || k}: ${ok ? "reliable" : "RELIABILITY LOST"}`, { mono: true, size: 24, fill: ok ? COL.testo2 : COL.persa }); y += 34; }
    if (f.ap && f.t >= f.ap[0]) { s += T(r.x + 18, y + 6, "PROXIMITY WARNING", { mono: true, size: 24, fill: COL.nonvisto }); y += 32; s += T(r.x + 18, y + 6, "predicted close pass between two tracks", { mono: true, size: 20, fill: COL.nonvisto }); y += 40; }
    if (f.ev) { s += T(r.x + 18, y + 6, "EVENT: FAILURE OR FLASH · INFERRED", { mono: true, size: 24, fill: COL.avviso }); y += 34; s += T(r.x + 18, y + 6, "debris volume and footprint declared", { mono: true, size: 22, fill: COL.avviso }); y += 30; s += T(r.x + 18, y + 6, "not verified: possible presence", { mono: true, size: 22, fill: COL.avviso }); y += 40; }
    if (extra) for (const e of extra) if (treg >= (e.da || -1e9)) { s += T(r.x + 18, y + 6, e.s, { mono: true, size: e.size || 22, fill: e.c || COL.testo }); y += 32; }
    return s;
  }

  /* ---------- grafici ---------- */
  function grafico(r, xmax, ymin, ymax, opz) {
    const px = (x) => r.x + 80 + (x / xmax) * (r.w - 110), py = (y) => r.y + r.h - 40 - ((y - ymin) / (ymax - ymin)) * (r.h - 84);
    let s = R(r.x, r.y, r.w, r.h) + L(px(0), py(ymin), px(xmax), py(ymin), { stroke: COL.testo2 }) + L(px(0), py(ymin), px(0), py(ymax), { stroke: COL.testo2 });
    for (const xt of opz.xt) s += T(px(xt), py(ymin) + 26, String(xt), { mono: true, size: 18, fill: COL.testo2, anchor: "middle" });
    for (const yt of opz.yt) s += T(px(0) - 10, py(yt) + 6, String(yt), { mono: true, size: 18, fill: COL.testo2, anchor: "end" });
    s += T(r.x + 16, r.y + 28, opz.titolo, { size: 21, fill: COL.testo });
    s += T(px(xmax), py(ymin) - 8, "τ (s)", { mono: true, size: 16, fill: COL.testo2, anchor: "end" });
    return { s, px, py };
  }
  function interp(xs, ys, x) { if (x <= xs[0]) return ys[0]; for (let i = 1; i < xs.length; i++) if (x <= xs[i]) { const u = (x - xs[i - 1]) / (xs[i] - xs[i - 1]); return ys[i - 1] + u * (ys[i] - ys[i - 1]); } return ys[ys.length - 1]; }
  function poli(xs, ys, g, tau, col) { // la curva calcolata, campionata a 0,5 s (densa: nessun tratto lineare lungo)
    let d = ""; for (let i = 0; i < xs.length; i++) { if (xs[i] > tau + 1e-9 && i > 0) { d += ` L${f1(g.px(tau))},${f1(g.py(interp(xs, ys, tau)))}`; break; } d += (i ? " L" : "M") + `${f1(g.px(xs[i]))},${f1(g.py(ys[i]))}`; }
    return `<path d="${d}" fill="none" stroke="${col}" stroke-width="4"/>` + C(g.px(Math.min(tau, xs[xs.length - 1])), g.py(interp(xs, ys, tau)), 7, { fill: col });
  }

  /* ---------- s7 confidenza (curva tarata) ---------- */
  function curva(t, D, cf) {
    const K = window.__CURVA; let s = ""; const tau = 30 * ease((t - 1.0) / Math.max(1, D - 5));
    // sinistra: schema della regione che segue la previsione e cresce; la zona fissa al punto di perdita resta indietro
    const r0 = { x: 40, y: 100, w: 1060, h: 700 }; s += R(r0.x, r0.y, r0.w, r0.h);
    s += T(r0.x + 14, r0.y + 32, "PLAN VIEW · schematic: motion compressed, radii from the computed curve", { mono: true, size: 20, fill: COL.testo2 });
    const cx = 260, cy = 470, sc = 0.9, xp = cx + 17 * tau; // 17 px per s di previsione (schema dichiarato)
    const rz = interp(K.tempi_s, K.raggio_0_9_m, tau);
    s += L(70, cy, cx, cy, { stroke: COL.visto, sw: 4, op: 0.6 }) + L(cx, cy, 1080, cy, { stroke: COL.nonvisto, sw: 2, dash: "4 8", op: 0.6 });
    s += C(cx, cy, 9, { fill: COL.visto, op: tau < 0.2 ? 1 : 0.35 }) + T(cx, cy + 40, "last seen", { mono: true, size: 18, fill: COL.testo2, anchor: "middle" });
    s += C(cx, cy, 150 * sc, { stroke: COL.nonoss, sw: 3, dash: "6 6" }) + T(r0.x + 20, cy - 150 * sc - 14, "fixed zone at last sighting · 150 m (for comparison)", { mono: true, size: 20, fill: COL.nonoss });
    s += `<circle cx="${f1(xp)}" cy="${cy}" r="${f1(rz * sc)}" fill="${COL.nonvisto}" opacity="0.08"/>` + C(xp, cy, rz * sc, { stroke: COL.nonvisto, sw: 3, dash: "12 8" }) + C(xp, cy, 6, { stroke: COL.nonvisto, sw: 3 });
    s += T(cl(xp, 330, 820), cy + rz * sc + 34, `NOT SEEN · ${tau.toFixed(1)} s · region r0.9 = ${Math.round(rz)} m`, { mono: true, size: 24, fill: COL.nonvisto, anchor: "middle" });
    s += T(r0.x + 20, r0.y + r0.h - 84, "aircraft at 210 m/s, straight line: the most favourable case;", { mono: true, size: 19, fill: COL.testo2 });
    s += T(r0.x + 20, r0.y + r0.h - 58, "on real tracks the region is much larger (see points on the right)", { mono: true, size: 19, fill: COL.testo2 });
    s += T(r0.x + 20, r0.y + r0.h - 22, "σ²(τ) = σ0² + 2σ0v·τ + σv²·τ² + q·τ³/3 + σ_ref²   ·   C(τ) = 1 − exp(−r²/2σ²(τ))", { mono: true, size: 21, fill: COL.testo });
    const g1 = grafico({ x: 1120, y: 100, w: 760, h: 215 }, 30, 0.5, 1, { xt: [0, 10, 20, 30], yt: [0.5, 1], titolo: "C(τ): chance it is within 150 m of the prediction · computed" });
    s += g1.s + poli(K.tempi_s, K.C, g1, tau, COL.testo2);
    const g2 = grafico({ x: 1120, y: 327, w: 760, h: 215 }, 30, 0, 200, { xt: [0, 10, 20, 30], yt: [0, 100, 200], titolo: "radius kept at 0.9, r0.9(τ) in m · computed in the model" });
    s += g2.s + poli(K.tempi_s, K.raggio_0_9_m, g2, tau, COL.nonvisto);
    const g3 = grafico({ x: 1120, y: 554, w: 760, h: 246 }, 30, 0.6, 1, { xt: [0, 10, 20, 30], yt: [0.6, 0.8, 1], titolo: "coverage of the 0.9 region · public flight tracks, simulated sensor" });
    s += g3.s + L(g3.px(0), g3.py(0.9), g3.px(30), g3.py(0.9), { stroke: COL.testo2, dash: "8 6" }) + T(g3.px(30) - 4, g3.py(0.9) - 8, "0.9", { mono: true, size: 16, fill: COL.testo2, anchor: "end" });
    const B = K.banda_osservata_copertura_0_9;
    for (const k of Object.keys(B)) {
      const [a, b] = k.split("-").map(Number), xm = (a + b) / 2; if (tau < a) continue; const v = B[k], x = g3.px(xm);
      s += L(x, g3.py(v.wilson_per_caso[0]), x, g3.py(v.wilson_per_caso[1]), { stroke: COL.visto, sw: 3 }) + C(x, g3.py(v.osservata), 7, { stroke: COL.visto, sw: 3, fill: COL.fondo });
      s += T(x, g3.py(v.wilson_per_caso[0]) + 22, (Math.round(v.osservata * 1000 + 1e-6) / 1000 >= 0 ? (Math.round(Math.round(v.osservata * 1000) / 10) / 100).toFixed(2) : ""), { mono: true, size: 17, fill: COL.visto, anchor: "middle" });
    }
    if (tau > 20) { const x = g3.px(27.5), op = ease((tau - 20) / 3); // virata: tutte le fasce insieme, limite (C-TAR-VIRATA)
      s += `<g opacity="${f1(op)}">` + L(x + 26, g3.py(0.67), x + 26, g3.py(0.78), { stroke: COL.persa, sw: 3 }) + C(x + 26, g3.py(0.73), 7, { stroke: COL.persa, sw: 3, fill: COL.fondo }) + T(x - 4, g3.py(0.73) + 6, "turns 0.73 · limit", { mono: true, size: 17, fill: COL.persa, anchor: "end" }) + "</g>"; }
    const bd = cf["C-TAR-BANDA"].testo_schermo.split(" · ");
    s += T(1124, 826, cf["C-TAR-1-2"].testo_schermo, { mono: true, size: 18, fill: COL.testo });
    s += T(1124, 849, bd[0] + " · " + bd[1], { mono: true, size: 18, fill: COL.testo });
    s += T(1124, 872, bd[2] + " · 95 % intervals per case", { mono: true, size: 18, fill: COL.testo });
    return s;
  }

  /* ---------- s8 F7 «scorta»: MoVi a bordo di un drone in moto (registro F7r davanti) ---------- */
  let F7C = null;
  function puntoUrto() { // ultimo istante con droneA e droneB nella verita' del registro: punto medio (mondo)
    if (F7C) return F7C; const F = window.__VOLO.F7.fotogrammi; let k = null;
    for (const f of F) if (f.v.droneA && f.v.droneB) k = f;
    F7C = { t: k.t + 0.1, p: [0, 1, 2].map((j) => (k.v.droneA[j] + k.v.droneB[j]) / 2) }; return F7C;
  }
  function evAttivo(f) { return f.ev && (f.ev.tipo !== "evento_vicino_non_localizzato" || f.ev.t0 == null || f.t - f.ev.t0 <= 8.0 + 1e-6); }
  const NL = (f) => f.ev && f.ev.tipo === "evento_vicino_non_localizzato";
  function mappa(M, t) { for (let i = 1; i < M.length; i++) if (t <= M[i][0]) { const u = (t - M[i - 1][0]) / (M[i][0] - M[i - 1][0]); return { tr: M[i - 1][1] + u * (M[i][1] - M[i - 1][1]), v: (M[i][1] - M[i - 1][1]) / (M[i][0] - M[i - 1][0]) }; } const n = M.length - 1; return { tr: M[n][1], v: 1 }; }
  const NOMI_STATO = { affidabile: "reliable", non_affidabile_saturazione: "UNRELIABLE · saturated", degradata_possibile_fumo: "degraded · possible smoke", ripristinata_dichiarata: "restored (declared)", ripristinato_dichiarato: "restored (declared)" };
  function scorta(S, t, cf) {
    const m = mappa(S.cfg.mappa, t), treg = m.tr, { f, i, F } = fotogramma("F7", treg), U = puntoUrto();
    const rel = (p) => [p[0] - f.pz[0], p[1] - f.pz[1], p[2]];
    let s = "";
    const viste = [["xy", { x: 40, y: 100, w: 1100, h: 700 }, [-140, -215, 560, 215]], ["xz", { x: 1160, y: 100, w: 720, h: 290 }, [-140, 0, 560, 200]]];
    for (const [asse, r, bb] of viste) {
      const P = proiettore(bb, r, 20), id = "cpF7" + asse, X = (p) => P.x(p[0]), Y = (p) => P.y(asse === "xy" ? p[1] : p[2]);
      s += R(r.x, r.y, r.w, r.h) + clipDef(id, r) + `<g clip-path="url(#${id})">`;
      if (asse === "xz") s += L(r.x, P.y(0), r.x + r.w, P.y(0), { stroke: COL.nonoss, sw: 2 });
      if (f.ev && evAttivo(f)) { const a = rel(f.ev.a); s += C(X(a), Y(a), P.r(f.ev.r), { stroke: COL.avviso, sw: 3, dash: "14 10", fill: COL.avviso, op: 0.08 }) + C(X(a), Y(a), P.r(f.ev.r), { stroke: COL.avviso, sw: 3, dash: "14 10" }); }
      // ILLUSTRATIVO: fumo e lampo nel punto d'urto (dal registro: posizione e istante; forma e colore disegnati)
      const dt = treg - U.t, pu = rel(U.p);
      if (dt > 0) for (let k = 0; k < 5; k++) { const rr = P.r(12 + 9 * dt + 6 * k), ox = P.r(4 * dt * (k - 2)), oy = P.r(3 * dt * ((k % 2) ? 1 : -1));
        s += C(X(pu) + ox, Y(pu) + oy, rr, { fill: COL.fumo, op: cl(0.30 - 0.025 * dt, 0.10, 0.30) }); }
      if (dt > -0.05 && dt < 0.7) { const u = cl(dt / 0.7, 0, 1); s += C(X(pu), Y(pu), P.r(8 + 70 * u), { fill: COL.lampo, op: 0.95 * (1 - u) }) + C(X(pu), Y(pu), P.r(4 + 25 * u), { fill: "#FFFFFF", op: 1 - u }); }
      for (const k in f.v) { if (k === "portatore") continue; const p = rel(f.v[k]), x = X(p), y = Y(p); s += L(x - 9, y, x + 9, y, { stroke: COL.vero, sw: 2, op: 0.7 }) + L(x, y - 9, x, y + 9, { stroke: COL.vero, sw: 2, op: 0.7 }); }
      // portatore (MoVi a bordo) nell'origine: posa stimata
      const c0 = [0, 0, f.pz[2]]; s += `<path d="M${f1(X(c0) + 16)},${f1(Y(c0))} L${f1(X(c0) - 12)},${f1(Y(c0) - 11)} L${f1(X(c0) - 6)},${f1(Y(c0))} L${f1(X(c0) - 12)},${f1(Y(c0) + 11)} Z" fill="${COL.coop}"/>`;
      const ord = f.tr.filter((u) => !u[6]).concat(f.tr.filter((u) => u[6]));
      for (const k of ord) {
        const [tid, ruolo, x, y, z, nv, vista, rP] = k, p = rel([x, y, z]), px = X(p), py = Y(p);
        if (ruolo === "f") { s += vista ? C(px, py, 4, { fill: COL.avviso }) : C(px, py, Math.max(6, P.r(rP)), { stroke: COL.avviso, sw: 1.5, dash: "4 4", op: 0.7 }); continue; }
        if (vista) {
          if (ruolo === "b") { let pts = []; for (let j = i; j >= 0 && F[i].t - F[j].t <= 2.0; j -= 2) { const q = F[j].tr.find((u) => u[0] === tid && u[6]); if (q) pts.push(rel([q[2] - F[j].pz[0] + f.pz[0], q[3] - F[j].pz[1] + f.pz[1], q[4]])); }
            for (let j = 1; j < pts.length; j++) s += L(X(pts[j - 1]), Y(pts[j - 1]), X(pts[j]), Y(pts[j]), { stroke: COL.visto, sw: 4, op: 0.8 * (1 - j / pts.length) }); }
          s += C(px, py, ruolo === "b" ? 10 : 7, { fill: COL.visto });
        } else {
          s += `<circle cx="${f1(px)}" cy="${f1(py)}" r="${f1(Math.max(12, P.r(rP)))}" fill="${COL.nonvisto}" opacity="0.10"/>` + C(px, py, Math.max(12, P.r(rP)), { stroke: COL.nonvisto, sw: 3, dash: "10 8" }) + C(px, py, 6, { stroke: COL.nonvisto, sw: 3 });
        }
      }
      s += "</g>";
      if (asse === "xy") {
        const b = f.tr.find((u) => u[1] === "b");
        if (b) { const p = rel([b[2], b[3], b[4]]), lab = b[6] ? `TRACKED DRONE · SEEN · identity ${b[8] === "confermata" ? "confirmed" : b[8] === "presunta_dubbia" ? "presumed, doubtful" : "presumed"}` : `TRACKED DRONE · NOT SEEN ${b[5].toFixed(1)} s · region ${Math.round(b[7])} m`;
          const lw = lab.length * 12.2 + 18, lx = cl(X(p) - 200, r.x + 10, r.x + r.w - lw - 12); let ly = cl(Y(p) - 70, r.y + 124, r.y + r.h - 60);
          // QA_V3C D4: l'etichetta del drone seguito non copre «CARRIER · MoVi on board» (box del portatore: x0-10..x0+250, y0+24..y0+50)
          const qx = X([0, 0]) - 10, qy = Y([0, 0]) + 44; if (lx < qx + 260 && lx + lw > qx && ly + 9 > qy - 20 && ly - 25 < qy + 8) ly = (Y(p) < qy ? qy - 34 : qy + 44);
          s += R(lx, ly - 25, lab.length * 12.2 + 18, 34, { fill: COL.fondo, stroke: "none", op: 0.85, rx: 3 }) + T(lx + 9, ly, lab, { mono: true, size: 20, fill: b[6] ? COL.visto : COL.nonvisto }); }
        s += T(X([0, 0]) - 10, Y([0, 0]) + 44, "CARRIER · MoVi on board", { mono: true, size: 18, fill: COL.coop });
        if (f.ev && evAttivo(f)) s += R(r.x + 8, r.y + r.h - 42, 560, 32, { fill: COL.fondo, stroke: "none", op: 0.85, rx: 3 }) + T(r.x + 16, r.y + r.h - 18, NL(f) ? "CONSERVATIVE SPHERE · never clear inside" : "DEBRIS VOLUME declared · never clear inside", { mono: true, size: 20, fill: COL.avviso });
        if (dt > 0) s += T(r.x + r.w - 16, r.y + r.h - 18, "flash and smoke: drawn for illustration", { mono: true, size: 18, fill: COL.testo2, anchor: "end" });
        s += R(r.x + 8, r.y + 44, 1000, 26, { fill: COL.fondo, stroke: "none", op: 0.85, rx: 3 }) + T(r.x + 14, r.y + 62, "+ truth (simulation only, MoVi does not see it)   ● seen   ◌ not seen: region where it can be", { mono: true, size: 18, fill: COL.testo2 });
        s += R(r.x + 8, r.y + 74, 640, 24, { fill: COL.fondo, stroke: "none", op: 0.85, rx: 3 }) + R(r.x + 14, r.y + 80, 22, 13, { fill: COL.avviso, stroke: COL.avviso, op: 0.35, rx: 2 }) + T(r.x + 46, r.y + 93, "filled: where it can be after an event · no probability", { mono: true, size: 18, fill: COL.testo2 });
        s += T(r.x + 14, r.y + 32, `VIEW FROM THE CARRIER · plan, carrier frame (estimated pose) · ${vel_txt(m.v)}`, { mono: true, size: 20, fill: COL.testo2 });
      } else s += T(r.x + 14, r.y + 32, "ALTITUDE VIEW (distance–height)", { mono: true, size: 20, fill: COL.testo2 });
    }
    // console
    const r = { x: 1160, y: 405, w: 720, h: 395 }; let y = r.y + 36; s += R(r.x, r.y, r.w, r.h);
    s += T(r.x + 18, y, `t = ${f.t.toFixed(1)} s · simulated run, log readout`, { mono: true, size: 20, fill: COL.testo2 }); y += 36;
    for (const [k, n] of [["radar_bordo#0", "RADAR 360°"], ["camera#1", "CAMERA"]]) { const v = f.af[k] || ""; s += T(r.x + 18, y, `${n}: ${NOMI_STATO[v] || v}`, { mono: true, size: 22, fill: v === "affidabile" ? COL.testo2 : v.indexOf("non_affidabile") === 0 ? COL.persa : COL.nonvisto }); y += 32; }
    const b = f.tr.find((u) => u[1] === "b");
    if (b) { const Cc = b[9] == null ? 1 : b[9]; y += 6;
      s += T(r.x + 18, y, "position confidence, tracked drone (computed in the model)", { mono: true, size: 18, fill: COL.testo2 }); y += 12;
      const gx = r.x + 18, gw = r.w - 40; s += R(gx, y, gw, 18, { fill: COL.fondo, stroke: COL.bordo, rx: 3 }) + R(gx, y, gw * Cc, 18, { fill: Cc >= 0.9 ? COL.visto : COL.nonvisto, stroke: "none", rx: 3 }) + L(gx + gw * 0.9, y - 4, gx + gw * 0.9, y + 22, { stroke: COL.testo, sw: 2 });
      s += T(gx + gw * 0.9, y + 40, "0.9", { mono: true, size: 16, fill: COL.testo2, anchor: "middle" });
      // REVISIONE_V3C C3: la barra e' la confidenza sulla posizione, non sull'identita'; l'identita' si scrive accanto (dal registro)
      if (b[8]) s += T(gx, y + 40, `identity: ${b[8] === "confermata" ? "confirmed" : b[8] === "presunta_dubbia" ? "presumed, doubtful" : "presumed"}`, { mono: true, size: 16, fill: b[8] === "confermata" ? COL.testo2 : COL.nonvisto });
      y += 72; }
    if (f.ev && NL(f)) { s += T(r.x + 18, y, "EVENT: nearby event · position unknown", { mono: true, size: 22, fill: COL.avviso }); y += 28;
      s += T(r.x + 18, y, evAttivo(f) ? `conservative sphere r ${Math.round(f.ev.r)} m · never clear inside` : "sphere expired (8 s) · event kept in the log", { mono: true, size: 20, fill: COL.avviso }); y += 34; }
    else if (f.ev) { s += T(r.x + 18, y, "EVENT: nearby collision · inferred", { mono: true, size: 22, fill: COL.avviso }); y += 28; s += T(r.x + 18, y, "debris volume declared, never clear inside", { mono: true, size: 20, fill: COL.avviso }); y += 34; }
    if (f.ap) { s += T(r.x + 18, y, NL(f) ? "WARNING to carrier: nearby event · position unknown" : "warning: path enters debris volume", { mono: true, size: 20, fill: COL.nonvisto }); y += 26; s += T(r.x + 18, y, "conservative, not localised, not selective", { mono: true, size: 18, fill: COL.nonvisto }); y += 28; }
    s += T(r.x + 18, r.y + r.h - 40, "radar blinded up to 2 s · pessimistic model · fix under test", { mono: true, size: 18, fill: COL.nonvisto });
    s += T(r.x + 18, r.y + r.h - 14, "flash trigger optimistic · identity presumed, doubtful", { mono: true, size: 18, fill: COL.testo2 });
    return s;
  }

  /* ---------- scene ---------- */
  function etichetta_onesta(o) {
    if (o === "sim") return T(1880, 44, "SIMULATION", { mono: true, size: 26, fill: COL.nonvisto, anchor: "end" }) + T(1880, 74, "Simulated · state-of-the-art sensor parameters assumed · no physical sensor", { mono: true, size: 20, fill: COL.testo2, anchor: "end" });
    if (o && o.indexOf("|") > 0) { const [a, b] = o.split("|"); return T(1880, 44, a, { mono: true, size: 26, fill: COL.nonvisto, anchor: "end" }) + T(1880, 74, b, { mono: true, size: 20, fill: COL.testo2, anchor: "end" }); }
    return T(1880, 44, "SCHEMATIC", { mono: true, size: 26, fill: COL.testo2, anchor: "end" }) + (o && o !== "schema" ? T(1880, 74, o, { mono: true, size: 20, fill: COL.testo2, anchor: "end" }) : "");
  }
  function contatore(righe, t) {
    let s = "", y = 838; for (const r of righe) { if (t < (r.da || 0) || t > (r.a || 1e9)) continue; const op = Math.min(ease((t - (r.da || 0)) / 0.6), ease(((r.a || 1e9) - t) / 0.4));
      s += T(60, y, r.s, { mono: true, size: r.size || 22, fill: r.c || COL.testo, op }); y += (r.size || 22) + 10; }
    return s;
  }
  function scenaDati(sc, cfg, t) {
    const treg = cfg.t0 + t * cfg.vel;
    let s = vista(sc, treg, { x: 40, y: 100, w: 1100, h: 700 }, cfg.bbxy, "xy", { etichette: true, scala: cfg.scala, vel: cfg.vel });
    s += vista(sc, treg, { x: 1160, y: 100, w: 720, h: 330 }, cfg.bbxz, "xz", {});
    s += console_(sc, treg, { x: 1160, y: 445, w: 720, h: 355 }, cfg.extra ? cfg.extra.map((e) => ({ ...e, da: e.treg })) : null);
    s += R(52, 746, 700, 24, { fill: COL.fondo, stroke: "none", op: 0.85, rx: 3 }) + R(60, 752, 22, 13, { fill: COL.avviso, stroke: COL.avviso, op: 0.35, rx: 2 }) + T(92, 765, "filled: where it can be after an event · no probability", { mono: true, size: 18, fill: COL.testo2 });
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
    const K = [
      { titolo: "Site: drone behind a building", righe: ["drone at 15–21 m/s, hidden", "by a building, announced:", cf["LP-1"].testo_schermo.split(" · ")[0], "", "never 'clear' on the drone,", "with the declared map"], etichetta: "simulation" },
      { titolo: "Site: taxiing aircraft", righe: ["three fused sensors:", cf["LP-4"].testo_schermo.split(": ")[1].split(" · ")[0], "", "limit: for aircraft in flight", "the site warning is late"], etichetta: "simulation" },
      { titolo: "Short range, other uses", righe: ["people behind obstacles,", "cars, trains (simulation)", "", "for a blind person: a warning", "aid, never a replacement for", "the cane or the guide dog"], etichetta: "schematic · no figures" } ];
    let s = "";
    K.forEach((k, j) => { const op = ease((t - 0.6 - j * 1.6) / 0.8), x = 60 + j * 610;
      s += `<g opacity="${op}">` + R(x, 160, 580, 560) + T(x + 24, 214, k.titolo, { size: 30 });
      k.righe.forEach((r, i) => { s += T(x + 24, 290 + i * 46, r, { mono: true, size: 23, fill: i === 2 && j < 2 ? COL.visto : COL.testo2 }); });
      s += T(x + 24, 690, k.etichetta, { mono: true, size: 20, fill: COL.nonvisto }) + "</g>"; });
    return s;
  }
  function chiusura(t, D, cf) {
    let s = ""; const lim = cf["LIMITI"].valore, sc = cf["SCALA"].valore, fine = D - 6.0;
    if (t < fine) {
      s += T(60, 160, "LIMITS", { mono: true, size: 30, fill: COL.persa });
      lim.forEach((l, i) => { s += T(60, 222 + i * 50, "· " + l, { size: 26, op: ease((t - 0.5 - i * 0.6) / 0.5) }); });
      s += T(1000, 160, "FROM PROTOTYPE TO DEPLOYED SYSTEM", { mono: true, size: 30, fill: COL.visto });
      sc.forEach((g, i) => { const op = ease((t - 4 - i * 1.4) / 0.6), y = 720 - i * 170, x = 1000 + i * 40;
        const sotto = g[1] === "HW-CALC" ? ["dedicated processing estimated 0.08–1.2 ms:", "estimate by analogy, not a measurement;", "the sensor revisit dominates"] : [g[1]];
        s += `<g opacity="${op}">` + R(x, y - 70, 860 - i * 40, 140) + T(x + 20, y - 30, g[0], { size: 28 });
        sotto.forEach((q, j) => { s += T(x + 20, y + 6 + j * 26, q, { mono: true, size: 19, fill: g[1] === "HW-CALC" ? COL.nonvisto : COL.testo2 }); });
        s += "</g>"; });
    } else {
      const u = ease((t - fine) / 1.0), M = window.__MARCHIO || {};
      if (M.wordmark) s += `<image href="${M.wordmark}" x="${960 - 300}" y="230" width="600" height="250" opacity="${u}"/>`;
      s += T(960, 560, "Seen, not seen, unknown: declared for every track.", { size: 36, anchor: "middle", op: u });
      s += T(960, 616, "Observes and warns · no output is a command", { mono: true, size: 24, fill: COL.testo2, anchor: "middle", op: u });
      s += T(960, 700, "By SDMs · Ignazio Crocchiolo · Federico Dellini · Danilo Amalfitano · Emanuele Ciotola · Pierfrancesco Amendola", { size: 22, fill: COL.testo2, anchor: "middle", op: u });
      s += T(960, 738, "The Big Hack 2026 · prototype built in one day · everything simulated, no physical sensor", { size: 22, fill: COL.testo2, anchor: "middle", op: u });
      s += T(960, 776, "Synthetic voice (Kokoro-82M, Apache-2.0) · synthetic music made for this video · fonts Inter, JetBrains Mono (OFL) · animation GSAP 3.15 (standard license)", { size: 18, fill: COL.testo2, anchor: "middle", op: u });
    }
    return s;
  }
  function sottotitolo(tg) {
    const S = window.__SOTTO || []; const q = S.find((x) => tg >= x.a && tg < x.b); if (!q) return "";
    let righe = [q.s];
    if (q.s.length > 80) { const p = q.s.split(" "); let a = "", k = 0; while (k < p.length && (a + " " + p[k]).length < q.s.length / 2) { a = (a ? a + " " : "") + p[k]; k++; } righe = [a, p.slice(k).join(" ")]; }
    const w = Math.min(1840, Math.max(...righe.map((x) => x.length)) * 16 + 40), h = 46 * righe.length + 12, y0 = 1066 - h;
    let s = R(960 - w / 2, y0, w, h, { fill: "#000", stroke: "none", op: 0.72, rx: 4 });
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
    else if (S.tipo === "scorta") s += scorta(S, t, cf);
    else if (S.tipo === "tre") s += tre(t);
    else if (S.tipo === "curva") s += curva(t, D, cf);
    else if (S.tipo === "schede") s += schede(t, cf);
    else if (S.tipo === "chiusura") s += chiusura(t, D, cf);
    const titoli = !(S.tipo === "chiusura" && t >= D - 6.0);
    if (S.titolo && titoli) s += T(40, 56, S.titolo, { size: 34 });
    if (S.contatore) s += contatore(S.contatore, t);
    if (S.titolone && t < S.titolone) { const u = Math.min(1, (S.titolone - t) / 0.5);
      s += `<rect x="0" y="0" width="1920" height="1080" fill="${COL.fondo}" opacity="${f1(0.85 * u)}"/>`;
      const M = window.__MARCHIO || {}; if (M.wordmark) s += `<image href="${M.wordmark}" x="${960 - 240}" y="330" width="480" height="200" opacity="${u}"/>`;
      s += T(960, 620, "Fast flight: when continuity is lost", { size: 44, anchor: "middle", op: u }); }
    s += "</g>";
    // etichetta d'onesta' SEMPRE visibile, a piena opacita', anche sul titolo d'apertura e sui titoli di coda
    s += etichetta_onesta(titoli ? S.onesta : "schema");
    s += sottotitolo(tg);
    return s;
  }
  window.MoViMotore = { disegna };
})();
