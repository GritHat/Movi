/* MoVi · componenti del video, VERSIONE v6 (revisione visiva: segni e testi più grandi, ingressi). Base: componenti.js.
 * (PIANO_VIDEO.md §6). Ogni componente è una funzione PURA:
 *   C.Nome(riga, intest, opz) -> stringa SVG
 * riga   = una riga «fotogramma» del registro (prototipo/movi/registro.py), già scelta dal motore con
 *          «tieni l'ultimo» (indice = floor(t_reg · fps + 1e-6)); null se l'inquadratura non ha registro.
 * intest = la riga 1 (intestazione) dello stesso registro.
 * opz    = {P: proiettore metri->px, pannello: {x,y,w,h}, T: testi della lingua, t: secondi dall'inizio della scena,
 *           stato_registro: "sviluppo"|"provvisorio"|"definitivo"|null, velocita, ...}
 * Nessun componente legge l'orologio, il caso o la rete: stesso ingresso, stesso disegno.
 * Un campo proposto (volumi, nubi, ritorni, avvisi_operatore, portata_utile_m, sistema, zone_non_verificate) che
 * manca nella riga non produce nulla. */
(function () {
  "use strict";
  const COL = {
    fondo: "#0B0F17", pannello: "#121826", bordo: "#24344A", testo: "#E8EDF2", testo2: "#AEB8C5",
    visto: "#3DD6E8", nonvisto: "#F5A524", avviso: "#C7841A", degradato: "#AEB8C5", persa: "#FF6B6B",
    nonoss: "#8A97A8", nube: "#6B7686", coop: "#A99CFF", vero: "#E8EDF2", sagoma: "#5E6A7B", segnaposto: "#FF4FD8"
  };
  const MONO = "JBMonoLocale, monospace", SANS = "InterLocale, sans-serif";

  /* ---------- utilità ---------- */
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const f1 = (x) => (Math.round(x * 10) / 10).toFixed(1);
  function fmt(s, v) { return String(s).replace(/\{(\w+)\}/g, (_, k) => (v && v[k] != null ? v[k] : "")); }
  /* testo con i segnaposto [CIFRA-…] [STATO-…] [k] [n] [DA FORNIRE] resi in magenta, ben visibili (Q24) */
  function tx(s) {
    return esc(s).replace(/\[(CIFRA[^\]]*|STATO[^\]]*|k|n|DA FORNIRE)\]/g,
      (m) => `<tspan fill="${COL.segnaposto}" font-weight="700" text-decoration="underline">${m}</tspan>`);
  }
  function testo(x, y, s, o) {
    o = o || {};
    const fam = o.mono ? MONO : SANS, size = o.size || 28, w = o.weight || (o.mono ? 700 : 600);
    const anchor = o.anchor || "start", fill = o.fill || COL.testo, op = o.opacity == null ? 1 : o.opacity;
    return `<text x="${f1(x)}" y="${f1(y)}" font-family="${fam}" font-size="${size}" font-weight="${w}" fill="${fill}" text-anchor="${anchor}" opacity="${op}"${o.ls ? ` letter-spacing="${o.ls}"` : ""}>${tx(s)}</text>`;
  }
  /* etichetta di stato su fondo scuro (leggibile sopra le trame) */
  function etichetta(x, y, s, o) {
    o = o || {};
    const size = o.size || 28, w = Math.max(10, String(s).length * size * 0.6 + 16), h = size + 12;
    let x0 = o.anchor === "end" ? x - w : (o.anchor === "middle" ? x - w / 2 : x);
    if (o.lim) { const L = o.lim; x0 = Math.max(L.x + 4, Math.min(x0, L.x + L.w - w - 4)); y = Math.max(L.y + size + 6, Math.min(y, L.y + L.h - 12)); }
    if (o.occ) {   // anti-sovrapposizione deterministica: scende finché non trova posto (al più 8 tentativi)
      const sovr = (b) => o.occ.some((q) => b.x < q.x + q.w && q.x < b.x + b.w && b.y < q.y + q.h && q.y < b.y + b.h);
      let k = 0; while (k < 8 && sovr({ x: x0, y: y - size - 2, w, h })) { y += h + 4; k++; }
      o.occ.push({ x: x0, y: y - size - 2, w, h });
    }
    return `<rect x="${f1(x0)}" y="${f1(y - size - 2)}" width="${f1(w)}" height="${h}" fill="${o.bg || COL.fondo}" opacity="${o.bgop == null ? 0.82 : o.bgop}" rx="3"/>` +
      testo(x0 + 8, y + 2, s, { mono: true, size, fill: o.fill || COL.testo });
  }
  function proiettore(bbox, r, margine) {
    const m = margine == null ? 20 : margine;
    const [x0, y0, x1, y1] = bbox, W = r.w - 2 * m, H = r.h - 2 * m;
    const s = Math.min(W / (x1 - x0), H / (y1 - y0));
    const ox = r.x + m + (W - s * (x1 - x0)) / 2, oy = r.y + m + (H - s * (y1 - y0)) / 2;
    return { s, x: (x) => ox + (x - x0) * s, y: (y) => oy + (y1 - y) * s, r: (d) => d * s, bbox, rect: r };
  }
  /* forme del registro -> path SVG (cerchio, poligono, settore_anulare con origine nel riferimento, celle polari) */
  function pathForma(F, P, intest) {
    if (!F) return "";
    if (F.tipo === "cerchio") {
      const cx = P.x(F.centro[0]), cy = P.y(F.centro[1]), r = Math.max(2, P.r(F.raggio_m));
      return `M${f1(cx - r)},${f1(cy)}a${f1(r)},${f1(r)} 0 1,0 ${f1(2 * r)},0a${f1(r)},${f1(r)} 0 1,0 ${f1(-2 * r)},0Z`;
    }
    if (F.tipo === "poligono") return "M" + F.punti.map((p) => `${f1(P.x(p[0]))},${f1(P.y(p[1]))}`).join("L") + "Z";
    if (F.tipo === "settore_anulare") return settore(P, [0, 0], F.azimut_gradi, F.distanza_m);
    if (F.tipo === "celle") return celle(F.indici, intest && intest.griglie && intest.griglie[F.griglia], P);
    return "";
  }
  function polare(P, c, az, d) {  // azimut 0 = avanti (+y), positivo a destra (+x)
    const a = az * Math.PI / 180;
    return [P.x(c[0] + d * Math.sin(a)), P.y(c[1] + d * Math.cos(a))];
  }
  function settore(P, c, az, dist) {
    const [a0, a1] = az, [d0, d1] = dist, n = Math.max(2, Math.ceil(Math.abs(a1 - a0) / 4));
    const pts = [];
    for (let i = 0; i <= n; i++) pts.push(polare(P, c, a0 + (a1 - a0) * i / n, d1));
    for (let i = n; i >= 0; i--) pts.push(polare(P, c, a0 + (a1 - a0) * i / n, Math.max(d0, 0.0001)));
    return "M" + pts.map((p) => `${f1(p[0])},${f1(p[1])}`).join("L") + "Z";
  }
  function celle(indici, g, P) {
    if (!g || !indici || g.tipo !== "polare") return "";
    const na = g.n_distanza, pa = g.passo_azimut_gradi, pd = g.passo_distanza_m, am = g.azimut_max_gradi;
    let d = "";
    for (const k of indici) {
      const ia = Math.floor(k / na), ir = k % na, a0 = -am + ia * pa, r0 = ir * pd;
      const p = [polare(P, [0, 0], a0, r0), polare(P, [0, 0], a0 + pa, r0), polare(P, [0, 0], a0 + pa, r0 + pd), polare(P, [0, 0], a0, r0 + pd)];
      d += "M" + p.map((q) => `${f1(q[0])},${f1(q[1])}`).join("L") + "Z";
    }
    return d;
  }
  function centroForma(F, P) {
    if (!F) return null;
    if (F.tipo === "cerchio") return [P.x(F.centro[0]), P.y(F.centro[1])];
    if (F.tipo === "poligono") { let x = 0, y = 0; for (const p of F.punti) { x += p[0]; y += p[1]; } return [P.x(x / F.punti.length), P.y(y / F.punti.length)]; }
    if (F.tipo === "settore_anulare") { const a = (F.azimut_gradi[0] + F.azimut_gradi[1]) / 2, d = (F.distanza_m[0] + F.distanza_m[1]) / 2; return polare(P, [0, 0], a, d); }
    return null;
  }
  function bordoAlto(F, P) {  // punto in alto della forma, per l'etichetta
    if (!F) return null;
    if (F.tipo === "cerchio") return [P.x(F.centro[0]), P.y(F.centro[1]) - P.r(F.raggio_m)];
    if (F.tipo === "poligono") { let best = null; for (const p of F.punti) { const q = [P.x(p[0]), P.y(p[1])]; if (!best || q[1] < best[1]) best = q; } return best; }
    if (F.tipo === "settore_anulare") return polare(P, [0, 0], (F.azimut_gradi[0] + F.azimut_gradi[1]) / 2, F.distanza_m[1]);
    return null;
  }
  const clip = (r) => `clip-path="url(#clip_${r})"`;

  /* trame comuni (una volta per tela) */
  function defs(pannelli) {
    let d = `<defs>
<pattern id="righeOcra" width="20" height="20" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="20" height="20" fill="none"/><rect width="7" height="20" fill="${COL.avviso}"/></pattern>
<pattern id="righeAmbra" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="18" fill="${COL.nonvisto}" opacity="0.55"/></pattern>
<pattern id="puntini" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="2.4" fill="${COL.nonoss}"/></pattern>
<pattern id="puntiniFitti" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="2.2" fill="${COL.nube}"/></pattern>
<pattern id="righeGrigie" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2" height="16" fill="${COL.degradato}" opacity="0.5"/></pattern>`;
    for (const [k, r] of Object.entries(pannelli || {})) d += `<clipPath id="clip_${k}"><rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}"/></clipPath>`;
    return d + "</defs>";
  }

  /* ---------- 1 PiantaArea ---------- */
  function PiantaArea(riga, intest, opz) {
    const P = opz.P;
    let s = `<g ${clip(opz.clip)}>`;
    for (const a of (intest.aree || [])) s += `<path d="${pathForma({ tipo: "poligono", punti: a.poligono }, P)}" fill="${COL.pannello}" stroke="${COL.bordo}" stroke-width="2"/>`;
    for (const o of (intest.ostacoli || [])) s += `<path d="${pathForma({ tipo: "poligono", punti: o.punti }, P)}" fill="#2A3446" stroke="${COL.testo2}" stroke-width="2"/>`;
    // scala grafica
    const r = opz.pannello, L = scalaTonda(200 / P.s), xs = r.x + r.w - 32 - P.r(L);
    s += `</g><g><line x1="${f1(xs)}" y1="${r.y + 40}" x2="${f1(xs + P.r(L))}" y2="${r.y + 40}" stroke="${COL.testo2}" stroke-width="3"/>` +
      testo(xs, r.y + 30, `${L >= 1000 ? L / 1000 + " km" : L + " m"}`, { mono: true, size: 24, weight: 400, fill: COL.testo2 }) + "</g>";
    return s;
  }
  function scalaTonda(x) { const p = Math.pow(10, Math.floor(Math.log10(x))); for (const m of [5, 2, 1]) if (m * p <= x) return m * p; return p; }

  /* ---------- 2 Sensori (glifi + coperture: piena, fantasma, NOT COUNTED) ---------- */
  function glifo(tipo, x, y, barrato) {
    let g;
    if (tipo === "radar") g = `<circle cx="${x}" cy="${y}" r="7" fill="${COL.testo2}"/><path d="M${x + 10},${y - 9} a13,13 0 0,1 0,18" fill="none" stroke="${COL.testo2}" stroke-width="2.5"/>`;
    else if (tipo === "eo") g = `<path d="M${x},${y - 10}L${x + 10},${y + 8}L${x - 10},${y + 8}Z" fill="none" stroke="${COL.testo2}" stroke-width="2.5"/>`;
    else if (tipo === "ir") g = `<path d="M${x},${y - 10}L${x + 10},${y + 8}L${x - 10},${y + 8}Z" fill="${COL.testo2}" fill-opacity="0.5" stroke="${COL.testo2}" stroke-width="2.5"/>`;
    else if (tipo === "lidar") g = `<path d="M${x},${y - 10}L${x + 10},${y}L${x},${y + 10}L${x - 10},${y}Z" fill="none" stroke="${COL.testo2}" stroke-width="2.5"/>`;
    else if (tipo === "cooperativo") g = `<rect x="${x - 8}" y="${y - 8}" width="16" height="16" fill="${COL.coop}"/>`;
    else g = `<rect x="${x - 9}" y="${y - 6}" width="18" height="12" fill="none" stroke="${COL.testo2}" stroke-width="2.5"/>`;
    if (barrato) g += `<line x1="${x - 13}" y1="${y + 13}" x2="${x + 13}" y2="${y - 13}" stroke="${COL.testo}" stroke-width="3"/>`;
    return `<g transform="translate(${x},${y}) scale(1.7) translate(${-x},${-y})">${g}</g>`;
  }
  function Sensori(riga, intest, opz) {
    const P = opz.P, T = opz.T.stati, nomi = opz.T.sensori, solo = opz.sensori_visibili;
    const stato = {}; for (const s of ((riga && riga.sensori) || [])) stato[s.id] = s;
    let cop = "", gl = "", et = "";
    const sens = (intest.sensori || []).filter((s, i) => solo == null || i < solo);
    let k = 0;
    for (const s of sens) {
      if (!s.pos) continue;
      const x = P.x(s.pos[0]), y = P.y(s.pos[1]), st = stato[s.id] || {}, tipo = s.tipo;
      const campo = s.campo_gradi || [-180, 180], intero = campo[1] - campo[0] >= 360;
      const portata = s.portata_m || 0;
      if (tipo !== "cooperativo" && portata) {
        const forma = (d) => intero ? pathForma({ tipo: "cerchio", centro: s.pos, raggio_m: d }, P) : settore(P, s.pos, campo, [0, d]);
        if (st.salute === "affidabilita_persa") {
          cop += `<path d="${forma(portata)}" fill="none" stroke="${COL.degradato}" stroke-width="2" stroke-dasharray="10 8"/>`;
          const c = bordoSensore(P, s, portata);
          et += etichetta(c[0], c[1], fmt(T.non_contato, { sens: nomi[tipo] || tipo }), { size: 28, fill: COL.degradato, occ: opz.occ, lim: opz.pannello });
        } else if (st.portata_utile_m) {
          const pu = Object.values(st.portata_utile_m)[0];
          cop += `<path d="${forma(portata)}" fill="none" stroke="${COL.degradato}" stroke-width="1.5" stroke-dasharray="4 10" opacity="0.7"/>`;
          cop += `<path d="${forma(pu)}" fill="${COL.degradato}" fill-opacity="0.07" stroke="${COL.degradato}" stroke-width="2.5" stroke-dasharray="14 6"/>`;
        } else {
          cop += `<path d="${forma(portata)}" fill="${COL.testo2}" fill-opacity="0.035" stroke="${COL.bordo}" stroke-width="1.5"/>`;
        }
      }
      gl += glifo(tipo, +f1(x + (k % 3 - 1) * 44), +f1(y + 44 * Math.floor(k / 3)), st.salute === "affidabilita_persa");
      k++;
    }
    return `<g ${clip(opz.clip)}>${cop}</g><g ${clip(opz.clip)}>${gl}${et}</g>`;
  }
  function bordoSensore(P, s, d) {
    const c = s.campo_gradi || [-180, 180], a = (c[1] - c[0] >= 360) ? -30 : (c[0] + c[1]) / 2;
    const p = polare(P, s.pos, a, d * 0.55), r = P.rect;
    return [Math.min(Math.max(p[0], r.x + 20), r.x + r.w - 300), Math.min(Math.max(p[1], r.y + 50), r.y + r.h - 40)];
  }

  /* ---------- 3 Traccia (disco, mezzo disco, anello, «?», etichetta) ---------- */
  function etichettaStato(tr, T) {
    if (tr.identita === "ambigua") return T.ambigua;
    if (tr.stato === "vista" && tr.sensori && tr.sensori.length === 1 && /radar|smr/.test(tr.sensori[0])) return T.vista_radar;
    if (tr.stato === "non_vista") return fmt(T.non_vista, { s: (tr.non_vista_da_s || 0).toFixed(1) });
    return T[tr.stato] || tr.stato;
  }
  function Traccia(riga, intest, opz) {
    if (!riga) return "";
    const P = opz.P, T = opz.T.stati;
    let s = "", amb = [];
    const forme = {}; for (const a of riga.avvisi || []) if (a.id_traccia != null) forme[a.id_traccia] = a.forma;
    for (const tr of riga.tracce || []) {
      let c = tr.pos ? [P.x(tr.pos[0]), P.y(tr.pos[1])] : centroForma(tr.regione || forme[tr.id], P);
      if (!c) continue;
      const [x, y] = c, id = String(tr.id).toUpperCase();
      if (tr.identita === "ambigua") amb.push([x, y]);
      // alone scuro: separa il ciano dalle trame ambra/ocra (la sottocampionatura 4:2:0 ne faceva pixel verdastri, Q11)
      s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="24" fill="${COL.fondo}"/>`;
      if (tr.stato === "vista" || tr.stato === "ricomparsa") s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="17" fill="${COL.visto}"/>`;
      else if (tr.stato === "vista_in_parte") s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="17" fill="none" stroke="${COL.visto}" stroke-width="4"/><path d="M${f1(x)},${f1(y - 17)}a17,17 0 0,0 0,34Z" fill="${COL.visto}"/>`;
      else if (tr.stato === "in_conferma") s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="17" fill="none" stroke="${COL.visto}" stroke-width="2.5"/>`;
      else s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="18" fill="none" stroke="${COL.nonvisto}" stroke-width="6"/>`;
      const col = (tr.stato === "non_vista" || tr.stato === "previsto_ampio" || tr.identita === "ambigua") ? COL.nonvisto : COL.visto;
      let lab = `${id} · ${etichettaStato(tr, T)}`;
      if (tr.stato === "ricomparsa") lab = `${id} ? · ${T.ricomparsa}`;
      if (opz.etichette !== false) s += etichetta(x + 30, y - 22, lab, { size: opz.size_etichette || 30, fill: col, occ: opz.occ, lim: opz.pannello });
    }
    if (amb.length >= 2) s = `<line x1="${f1(amb[0][0])}" y1="${f1(amb[0][1])}" x2="${f1(amb[1][0])}" y2="${f1(amb[1][1])}" stroke="${COL.nonvisto}" stroke-width="5" stroke-dasharray="12 8"/>` + s;
    return `<g ${clip(opz.clip)}>${s}</g>`;
  }

  /* ---------- 4 Regione (tratteggio al 18 %; righe per previsto_ampio; mai una sagoma dentro) ---------- */
  function Regione(riga, intest, opz) {
    if (!riga) return "";
    const P = opz.P;
    let s = "";
    for (const tr of riga.tracce || []) {
      const F = tr.regione; if (!F) continue;
      const d = pathForma(F, P, intest); if (!d) continue;
      if (tr.stato === "previsto_ampio") s += `<path d="${d}" fill="url(#righeAmbra)" stroke="${COL.nonvisto}" stroke-width="4" stroke-dasharray="14 9"/>`;
      else s += `<path d="${d}" fill="${COL.nonvisto}" fill-opacity="0.18" stroke="${COL.nonvisto}" stroke-width="4" stroke-dasharray="14 9"/>`;
    }
    return `<g ${clip(opz.clip)}>${s}</g>`;
  }

  /* ---------- 5 PossibilePresenza (contorno a righe ocra + parola; resta finché un sensore non torna a guardare) ---------- */
  function PossibilePresenza(riga, intest, opz) {
    if (!riga) return "";
    const P = opz.P, T = opz.T.stati;
    let s = "", et = "";
    for (const a of riga.avvisi || []) {
      if (a.tipo !== "possibile_presenza" || a.motivo === "possibili_detriti") continue;
      const d = pathForma(a.forma, P, intest); if (!d) continue;
      s += `<path d="${d}" fill="none" stroke="url(#righeOcra)" stroke-width="12"/>`;
      if (a.forma.tipo === "settore_anulare" && !(riga.tracce || []).some((t) => t.regione)) s += `<path d="${d}" fill="url(#righeAmbra)" opacity="0.8"/>`;
      const b = bordoAlto(a.forma, P);
      if (b) et += etichetta(b[0], b[1] - 16, T.possibile_presenza, { size: 30, fill: COL.avviso, anchor: "middle", occ: opz.occ, lim: opz.pannello });
    }
    return `<g ${clip(opz.clip)}>${s}${et}</g>`;
  }

  /* ---------- 6 VolumeDetriti (righe ocra, raggi passati, impronta; quadratini solo da ritorni[]) ---------- */
  function VolumeDetriti(riga, intest, opz) {
    if (!riga || !riga.volumi) return "";
    const P = opz.P, T = opz.T.stati;
    let s = "", et = "";
    for (const v of riga.volumi) {
      if (v.impronta) s += `<path d="${pathForma(v.impronta, P)}" fill="url(#puntini)" stroke="${COL.avviso}" stroke-width="2.5" stroke-dasharray="6 6"/>`;
      const d = pathForma(v.forma, P);
      s += `<path d="${d}" fill="url(#righeOcra)" fill-opacity="0.45" stroke="${COL.avviso}" stroke-width="3"/>`;
      if (v.forma.tipo === "cerchio") for (const r of (v.raggi_passati_m || []).slice(-3))
        s += `<circle cx="${f1(P.x(v.forma.centro[0]))}" cy="${f1(P.y(v.forma.centro[1]))}" r="${f1(P.r(r))}" fill="none" stroke="${COL.avviso}" stroke-width="1" stroke-dasharray="2 8" opacity="0.5"/>`;
      const b = bordoAlto(v.forma, P);
      if (b) et += etichetta(b[0], Math.max(b[1] - 10, P.rect.y + 70), T.volume, { size: 30, fill: COL.avviso, anchor: "middle", occ: opz.occ, lim: opz.pannello });
    }
    if (riga.ritorni && riga.ritorni.length) {
      for (const p of riga.ritorni) s += `<rect x="${f1(P.x(p[0]) - 6)}" y="${f1(P.y(p[1]) - 6)}" width="12" height="12" fill="${COL.testo2}"/>`;
      const p = riga.ritorni[0];
      et += testo(P.x(p[0]) + 12, P.y(p[1]) + 30, T.ritorni, { mono: true, size: 26, weight: 400, fill: COL.testo2 });
    }
    return `<g ${clip(opz.clip)}>${s}${et}</g>`;
  }

  /* ---------- 7 Nube (puntini fitti + contorno a trattini + parola con i sensori) ---------- */
  function Nube(riga, intest, opz) {
    if (!riga || !riga.nubi) return "";
    const P = opz.P, T = opz.T;
    let s = "";
    for (const n of riga.nubi) {
      const d = pathForma(n.forma, P);
      s += `<path d="${d}" fill="url(#puntiniFitti)" stroke="${COL.nube}" stroke-width="4" stroke-dasharray="12 8"/>`;
      const b = bordoAlto(n.forma, P), sens = (n.opaca_per || []).map((x) => T.sensori[x] || x).join(", ");
      if (b) s += etichetta(b[0], b[1] - 60, fmt(T.stati.nube, { causa: T.cause[n.tipo] || n.tipo, sens }), { size: 28, fill: COL.testo2, anchor: "middle", occ: opz.occ, lim: opz.pannello });
    }
    return `<g ${clip(opz.clip)}>${s}</g>`;
  }

  /* ---------- 8 BandaAffidabilita (bande della console; banda di sistema di 120 px) ---------- */
  function BandaAffidabilita(riga, intest, opz) {
    if (!riga) return "";
    const T = opz.T, r = opz.console, bande = [];
    for (const s of riga.sensori || []) {
      const nome = T.sensori[s.tipo] || s.tipo;
      if (s.salute === "affidabilita_persa") bande.push({ c: COL.persa, t: fmt(T.stati.affidabilita_persa, { sens: nome, causa: T.cause[s.causa] || s.causa }), scuro: true });
      else if (s.salute === "degradato" && s.portata_utile_m) bande.push({ c: "#3A4558", t: fmt(T.stati.portata_ridotta, { sens: nome }) });
    }
    for (const x of riga.sistema || []) {
      if (x === "NO_REDUNDANCY") bande.push({ c: "#3A4558", t: T.stati.no_ridondanza });
      else if (x.startsWith("WARNING_NOT_TIMELY")) { const cl = x.split(":")[1]; bande.push({ c: "#3A4558", t: fmt(T.stati.non_tempestivo, { classe: T.classi[cl] || cl }) }); }
    }
    // fonde bande uguali (EO e IR degradati -> una riga per sensore resta: sono dichiarazioni distinte)
    let s = "", y = r.y + r.h - 8;
    for (const b of bande.slice(0, 4).reverse()) {
      const pz = spezza(b.t, Math.floor((r.w - 24) / 16.8)), hb = 18 + pz.length * 34;
      s += `<rect x="${r.x}" y="${y - hb}" width="${r.w}" height="${hb}" fill="${b.c}"/>`;
      pz.forEach((p, i) => { s += testo(r.x + 12, y - hb + 38 + i * 34, p, { mono: true, size: 28, fill: b.scuro ? COL.fondo : COL.testo }); });
      y -= hb + 6;
    }
    if (riga.affidabilita === "persa" && opz.pannello_movi) {
      const m = opz.pannello_movi;
      s += `<rect x="${m.x}" y="${m.y + m.h - 120}" width="${m.w}" height="120" fill="${COL.persa}"/>` +
        testo(m.x + 32, m.y + m.h - 42, fmt(T.stati.affidabilita_persa, { sens: "SYSTEM", causa: (riga.sensori.find((x) => x.salute === "affidabilita_persa") || {}).causa ? (T.cause[(riga.sensori.find((x) => x.salute === "affidabilita_persa")).causa] || "") : "" }).replace("SYSTEM · ", ""), { mono: true, size: 48, fill: COL.fondo });
    }
    return s;
  }

  /* ---------- 9 ConsoleTracce (3 righe di stato + 1 riga d'evento + avvisi all'operatore) ---------- */
  function ConsoleTracce(riga, intest, opz) {
    const T = opz.T, r = opz.console;
    let s = `<rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}" fill="${COL.pannello}" stroke="${COL.bordo}" stroke-width="2"/>`;
    if (!riga) return s;
    let y = r.y + 54; const W = Math.floor((r.w - 32) / 16.8);
    const tracce = (riga.tracce || []).slice(0, opz.righe_console || 3);
    for (const tr of tracce) {
      const col = (tr.stato === "non_vista" || tr.stato === "previsto_ampio" || tr.identita === "ambigua") ? COL.nonvisto : COL.visto;
      const pieno = tr.stato === "vista" || tr.stato === "ricomparsa";
      s += `<circle cx="${r.x + 24}" cy="${y - 10}" r="11" fill="${pieno ? col : "none"}" stroke="${col}" stroke-width="4"/>`;
      s += testo(r.x + 46, y, String(tr.id).toUpperCase(), { mono: true, size: 28, fill: COL.testo });
      const pz = spezza(etichettaStato(tr, T.stati), W - 2);
      pz.forEach((p, i) => { s += testo(r.x + 46, y + 36 + i * 34, p, { mono: true, size: 28, fill: col }); });
      y += 52 + pz.length * 34;
    }
    const avv = (riga.avvisi || []).filter((a) => a.tipo === "possibile_presenza" && a.motivo !== "possibili_detriti");
    if (avv.length) { s += testo(r.x + 16, y, `${T.stati.possibile_presenza} · ${avv.length}`, { mono: true, size: 28, fill: COL.avviso }); y += 48; }
    // ultimo evento entro 8 s (l'evento resta scritto: è un fatto del registro)
    const ev = opz.ultimo_evento;
    if (ev && (T.eventi[ev.tipo])) {
      s += `<line x1="${r.x + 12}" y1="${y - 18}" x2="${r.x + r.w - 12}" y2="${y - 18}" stroke="${COL.bordo}" stroke-width="2"/>`;
      let yy = y + 14;
      for (const part of spezza(fmt(T.stati.evento, { tipo: T.eventi[ev.tipo], come: T.come[ev.come_lo_so] || ev.come_lo_so }), W)) { s += testo(r.x + 16, yy, part, { mono: true, size: 28, fill: COL.testo }); yy += 34; }
      if (ev.indizi) for (const part of spezza(fmt(T.stati.inferito_da, { indizi: ev.indizi.map((x) => T.indizi[x] || x).join(" + ") }), Math.floor((r.w - 32) / 13.2))) { s += testo(r.x + 16, yy, part, { mono: true, size: 22, weight: 400, fill: COL.testo2 }); yy += 28; }
      y = yy + 30;
    }
    for (const a of riga.avvisi_operatore || []) {
      const t2 = fmt(T.stati.avviso_operatore, { cosa: T.avvisi_operatore[a.codice] || a.codice });
      const pz = spezza(t2, W); pz.forEach((part, i) => { s += testo(r.x + 16, y + i * 34, part, { mono: true, size: 28, fill: COL.avviso }); });
      y += pz.length * 34 + 16;
    }
    return s;
  }
  function spezza(s, n) { const out = []; let cur = ""; for (const w of String(s).split(" ")) { if ((cur + " " + w).trim().length > n) { out.push(cur.trim()); cur = w; } else cur += " " + w; } if (cur.trim()) out.push(cur.trim()); return out; }

  /* ---------- 10 VentaglioSettori (settori a tre livelli, dal sensore) ---------- */
  function VentaglioSettori(riga, intest, opz) {
    if (!riga || !riga.settori) return "";
    const P = opz.P, g = (intest.griglie && Object.values(intest.griglie)[0]) || {}, R = g.portata_m || opz.portata_settori || 3, T = opz.T.stati;
    let s = "", vuoto = null;
    for (const z of riga.settori) {
      if (z.livello === "visto_libero_fino_a" && z.d_m) { s += `<path d="${settore(P, [0, 0], z.azimut_gradi, [0.05, z.d_m])}" fill="${COL.bordo}" opacity="0.9"/>`; vuoto = vuoto || z; }
      else if (z.livello === "attenzione") s += `<path d="${settore(P, [0, 0], z.azimut_gradi, [0.05, R])}" fill="none" stroke="${COL.avviso}" stroke-width="1.5" opacity="0.8"/>`;
      else if (z.livello === "zona_non_verificata") s += `<path d="${settore(P, [0, 0], z.azimut_gradi, [0.05, R])}" fill="url(#puntini)" opacity="0.55"/>`;
      else if (z.livello === "affidabilita_persa") s += `<path d="${settore(P, [0, 0], z.azimut_gradi, [0.05, R])}" fill="none" stroke="${COL.degradato}" stroke-dasharray="6 6"/>`;
    }
    if (vuoto && opz.mostra_vuoto) { const p = polare(P, [0, 0], (vuoto.azimut_gradi[0] + vuoto.azimut_gradi[1]) / 2, vuoto.d_m); s += etichetta(p[0], p[1], fmt(T.visto_vuoto, { d: vuoto.d_m }), { size: 18, fill: COL.testo2 }); }
    return `<g ${clip(opz.clip)}>${s}</g>`;
  }

  /* ---------- 11 ZonaNonVerificata (puntini; si toglie solo all'evento «ispezione») ---------- */
  function ZonaNonVerificata(riga, intest, opz) {
    if (!riga || !riga.zone_non_verificate) return "";
    const P = opz.P, T = opz.T.stati;
    let s = "";
    for (const z of riga.zone_non_verificate) {
      const d = pathForma(z.forma, P, intest); if (!d) continue;
      s += `<path d="${d}" fill="url(#puntini)" stroke="${COL.nonoss}" stroke-width="1.5" stroke-dasharray="3 5"/>`;
      if (opz.etichetta_zona !== false) { const c = centroForma(z.forma, P); if (c) s += etichetta(c[0], c[1] + 50, z.causa === "possibili_detriti" ? T.detriti_suolo : T.zona_non_verificata, { size: 28, fill: COL.nonoss, anchor: "middle", occ: opz.occ, lim: opz.pannello }); }
    }
    return `<g ${clip(opz.clip)}>${s}</g>`;
  }

  /* ---------- 12 Tabellone (contatore con l'origine sotto; i segnaposto restano visibili) ---------- */
  function Tabellone(riga, intest, opz) {
    let s = "", y = opz.y;
    for (const c of opz.contatori || []) {
      for (const [i, part] of spezza(c, 56).entries()) s += testo(opz.x, y + i * 34, part, { mono: true, size: 24, weight: 400, fill: COL.testo2 });
      y += 34 * spezza(c, 56).length + 18;
    }
    return s;
  }

  /* ---------- 13 CatenaBlocchi (sensori → celle → tracce → regole → uscite; classificazione tratteggiata) ---------- */
  function CatenaBlocchi(riga, intest, opz) {
    const T = opz.T, nomi = T["s7.catena"], x = opz.x, y0 = opz.y, h = 64, g = 36, w = opz.w || 330;
    let s = "";
    nomi.forEach((n, i) => {
      const y = y0 + i * (h + g), on = i < (opz.accesi == null ? 5 : opz.accesi);
      s += `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="${COL.pannello}" stroke="${on ? COL.testo2 : COL.bordo}" stroke-width="2.5"${on ? "" : ' stroke-dasharray="8 6"'}/>` +
        testo(x + w / 2, y + 42, n, { mono: true, size: 26, anchor: "middle", fill: on ? COL.testo : COL.testo2 });
      if (i < nomi.length - 1) s += `<line x1="${x + w / 2}" y1="${y + h}" x2="${x + w / 2}" y2="${y + h + g}" stroke="${COL.testo2}" stroke-width="2.5"/>`;
    });
    const yc = y0 + 2 * (h + g);
    s += `<rect x="${x + w + 50}" y="${yc - 40}" width="250" height="${h + 80}" rx="6" fill="none" stroke="${COL.testo2}" stroke-width="2" stroke-dasharray="8 6"/>`;
    spezza(T["s7.classi"], 16).forEach((p, i) => { s += testo(x + w + 175, yc - 2 + i * 30, p, { mono: true, size: 20, weight: 400, anchor: "middle", fill: COL.testo2 }); });
    s += `<line x1="${x + w}" y1="${yc + h / 2}" x2="${x + w + 50}" y2="${yc + h / 2}" stroke="${COL.testo2}" stroke-width="2" stroke-dasharray="6 6"/>`;
    return s;
  }

  /* ---------- 14 VeritaSim (sagome grigie piatte; fiammata piatta; fumo piatto; nebbia e pioggia come velo) ---------- */
  function sagoma(classe, x, y, sc) {
    const c = COL.sagoma;
    if (/aereo/.test(classe)) { const k = Math.max(0.6, sc); return `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(k)})"><path d="M-22,0 L18,-2 L22,0 L18,2 Z M-2,-1 L-8,-18 L-3,-18 L6,-1 Z M-2,1 L-8,18 L-3,18 L6,1 Z M-20,-1 L-24,-7 L-21,-7 L-15,-1 Z M-20,1 L-24,7 L-21,7 L-15,1 Z" fill="${c}"/></g>`; }
    if (/multirotore|drone/.test(classe)) return `<g transform="translate(${f1(x)},${f1(y)})"><rect x="-5" y="-5" width="10" height="10" fill="${c}"/>${[[-9, -9], [9, -9], [9, 9], [-9, 9]].map((p) => `<circle cx="${p[0]}" cy="${p[1]}" r="5" fill="none" stroke="${c}" stroke-width="2.5"/>`).join("")}</g>`;
    if (/persona/.test(classe)) return `<g transform="translate(${f1(x)},${f1(y)})"><ellipse cx="0" cy="0" rx="9" ry="6" fill="${c}"/><circle cx="0" cy="0" r="4.5" fill="#7A8698"/></g>`;
    if (/mezzo|auto|veicolo/.test(classe)) return `<rect x="${f1(x - 12)}" y="${f1(y - 6)}" width="24" height="12" fill="${c}"/>`;
    return `<rect x="${f1(x - 7)}" y="${f1(y - 7)}" width="14" height="14" fill="${c}"/>`;
  }
  function VeritaSim(riga, intest, opz) {
    const P = opz.P, r = opz.pannello, T = opz.T;
    let s = `<rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}" fill="#0E131D" stroke="${COL.bordo}" stroke-width="2"/><g ${clip(opz.clip)}>`;
    for (const a of intest.aree || []) s += `<path d="${pathForma({ tipo: "poligono", punti: a.poligono }, P)}" fill="#151C2A" stroke="${COL.bordo}" stroke-width="1.5"/>`;
    for (const o of intest.ostacoli || []) s += `<path d="${pathForma({ tipo: "poligono", punti: o.punti }, P)}" fill="#2A3446" stroke="${COL.testo2}" stroke-width="1.5"/>`;
    if (riga && riga.verita) {
      for (const o of riga.verita.oggetti || []) {
        const x = P.x(o.pos[0]), y = P.y(o.pos[1]);
        s += `<g opacity="${o.visibile === false ? 0.55 : 1}" transform="translate(${f1(x)},${f1(y)}) scale(${opz.scala_sagome || 1}) translate(${f1(-x)},${f1(-y)})">${sagoma(o.classe, x, y, 1)}</g>`;
        if (o.visibile === false && opz.mostra_fuori_vista !== false) s += testo(x + 20, y + 34, T.fuori_vista, { mono: true, size: 22, weight: 400, fill: COL.testo2 });
      }
      const F = riga.verita.fiammata;
      if (F) { const x = P.x(F.pos[0]), y = P.y(F.pos[1]); s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(Math.max(18, P.r(F.raggio_m)))}" ry="${f1(Math.max(12, P.r(F.raggio_m) * 0.7))}" fill="#F4F1EA"/>` + etichetta(x, y - 34, T["s6.flash"], { size: 24, fill: COL.testo, anchor: "middle", lim: r }); }
      for (const n of riga.nubi || []) s += `<path d="${pathForma(n.forma, P)}" fill="#6B7686" opacity="0.55"/>`;
    }
    if (riga && riga.meteo) {
      if (/nebbia/.test(riga.meteo)) s += `<rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}" fill="#AEB8C5" opacity="0.22"/>`;
      if (/pioggia/.test(riga.meteo)) { const off = ((opz.t * 40) % 16).toFixed(1); s += `<rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}" fill="url(#righeGrigie)" opacity="0.55" transform="translate(0,${off})"/>`; }
    }
    s += "</g>";
    return s;
  }

  /* ---------- 15 FasceOnesta (etichetta in alto a destra per TUTTA la scena; dominio in basso; ×N) ---------- */
  function FasceOnesta(riga, intest, opz) {
    const T = opz.T;
    let lab;
    if (!riga) lab = T["onesta.schema"];
    else if (riga.dichiarazioni && /SVILUPPO/.test(riga.dichiarazioni.dati)) lab = T["onesta.dev"];
    else if (riga.dichiarazioni && /simulat|pubblic/.test(riga.dichiarazioni.dati)) {
      lab = opz.etichetta_sensore ? `${T["onesta.sim"].split(" · ")[0]} · ${opz.etichetta_sensore}` : T["onesta.sim"];
      if (opz.stato_registro === "provvisorio") lab += " · " + T["onesta.provvisorio"];
    } else lab = T["onesta.schema"];
    let s = `<rect x="0" y="0" width="1920" height="124" fill="${COL.fondo}"/>`;
    s += testo(96, 66, opz.titolo || "", { size: 34, weight: 600 }) + testo(96, 104, opz.richiesta || "", { mono: true, size: 20, weight: 400, fill: COL.testo2 });
    const w = lab.length * 26 * 0.6 + 28;
    s += `<rect x="${f1(1824 - w)}" y="38" width="${f1(w)}" height="44" fill="none" stroke="${COL.testo}" stroke-width="2"/>` + testo(1824 - 14, 69, lab, { mono: true, size: 26, anchor: "end" });
    if (opz.dominio || opz.velocita && opz.velocita !== 1 || opz.tenuto) {
      s += `<rect x="96" y="862" width="1728" height="38" fill="${COL.fondo}"/>`;
      let d = opz.dominio || "";
      if (opz.velocita && opz.velocita !== 1) d += (d ? " · " : "") + fmt(T.compresso, { N: opz.velocita });
      if (opz.tenuto) d += (d ? " · " : "") + T.tenuto;
      s += testo(96, 890, d, { mono: true, size: 20, weight: 400, fill: COL.testo2 });
    }
    return s;
  }

  /* ---------- 16 ScenaSchema (segni grandi delle scene 2, 3, 7: disegnati dai testi e dal tempo della scena) ---------- */
  function ScenaSchema(riga, intest, opz) {
    const T = opz.T, t = opz.t, n = opz.scena;
    let s = "";
    if (n === 2) {
      const on = (a) => t >= a;
      s += testo(960, 210, T["s2.testa"], { size: 48, anchor: "middle" });
      const X = [420, 960, 1500], Y = 470;
      if (on(4)) s += `<circle cx="${X[0]}" cy="${Y}" r="46" fill="${COL.visto}"/>` + etichetta(X[0], Y + 110, T.stati.vista, { size: 32, fill: COL.visto, anchor: "middle" }) + testo(X[0], Y + 170, T["s2.a1"], { size: 32, anchor: "middle", fill: COL.testo2 });
      if (on(6.5)) s += `<ellipse cx="${X[1] + 30}" cy="${Y}" rx="150" ry="90" fill="${COL.nonvisto}" fill-opacity="0.18" stroke="${COL.nonvisto}" stroke-width="3" stroke-dasharray="12 8"/><circle cx="${X[1]}" cy="${Y}" r="46" fill="none" stroke="${COL.nonvisto}" stroke-width="5"/>` + etichetta(X[1], Y + 140, fmt(T.stati.non_vista, { s: "1.2" }), { size: 32, fill: COL.nonvisto, anchor: "middle" }) + testo(X[1], Y + 200, T["s2.a2"], { size: 32, anchor: "middle", fill: COL.testo2 });
      if (on(10)) s += `<rect x="${X[2] - 170}" y="${Y - 120}" width="340" height="240" fill="url(#righeAmbra)" stroke="${COL.nonvisto}" stroke-width="3" stroke-dasharray="12 8"/><circle cx="${X[2]}" cy="${Y}" r="40" fill="${COL.fondo}" stroke="${COL.nonvisto}" stroke-width="5"/>` + etichetta(X[2], Y + 170, T.stati.previsto_ampio, { size: 32, fill: COL.nonvisto, anchor: "middle" }) + testo(X[2], Y + 230, T["s2.a3"], { size: 32, anchor: "middle", fill: COL.testo2 });
      if (on(14)) {
        s += `<rect x="96" y="730" width="760" height="110" fill="url(#puntini)" stroke="${COL.nonoss}" stroke-width="2" stroke-dasharray="4 6"/>` + etichetta(120, 800, T.stati.zona_non_verificata, { size: 30, fill: COL.nonoss });
        if (on(15)) s += testo(620, 805, T["s2.nonvuoto"], { mono: true, size: 40, fill: COL.testo }) + (on(16) ? `<line x1="606" y1="792" x2="${606 + T["s2.nonvuoto"].length * 25 + 22}" y2="792" stroke="${COL.testo}" stroke-width="6"/>` : "");
      }
      if (on(19)) s += `<rect x="1000" y="730" width="824" height="110" fill="none" stroke="url(#righeOcra)" stroke-width="14"/>` + etichetta(1030, 800, T.stati.possibile_presenza, { size: 30, fill: COL.avviso });
    }
    if (n === 7) {
      const righe = ["s7.l1", "s7.l2", "s7.l3", "s7.l4", "s7.l5"], tempi = [1, 6, 11, 16, 20];
      righe.forEach((k, i) => { if (t >= tempi[i]) s += testo(96, 220 + i * 80, T[k], { size: 34, weight: 600, fill: i === 4 ? COL.testo : COL.testo2 }); });
      if (t >= 23) s += Tabellone(null, null, { x: 96, y: 680, contatori: [T["s7.c_v2"], T["s7.c_v1"], T["s7.c_s7"]] });
      s += CatenaBlocchi(null, null, { T, x: 1300, y: 190, w: 300, accesi: 5 });
    }
    return s;
  }

  /* ---------- 17 TitoloMarchio (titolo d'apertura; simbolo SDMs v3b animato 1,5 s; chiusura) ---------- */
  function TitoloMarchio(riga, intest, opz) {
    const M = window.__MARCHIO || {}, T = opz.T, t = opz.t;
    let s = "";
    if (opz.modo === "apertura") {
      const op = t < 2.6 ? 1 : Math.max(0, 1 - (t - 2.6) / 0.4);
      s += `<g opacity="${f1(op)}"><rect x="0" y="300" width="1920" height="430" fill="${COL.fondo}" opacity="0.88"/>` +
        `<image href="${M.wordmark || ""}" x="${960 - 144}" y="340" width="288" height="120"/>` +
        testo(960, 560, T["s1.sottotitolo"], { size: 44, anchor: "middle" }) + testo(960, 640, T["s1.riga"], { mono: true, size: 24, weight: 400, anchor: "middle", fill: COL.testo2 }) + "</g>";
    }
    if (opz.modo === "chiusura") {
      const k = Math.min(1, t / 1.5), disco = Math.min(1, t / 0.5), zona = Math.max(0, Math.min(1, (t - 0.5) / 1.0));
      s += `<g transform="translate(${960 - 204},150) scale(3)"><circle cx="32" cy="42" r="${f1(22 * disco)}" fill="${COL.visto}"/>` +
        `<ellipse cx="95" cy="42" rx="33" ry="26" fill="none" stroke="${COL.nonvisto}" stroke-width="4" stroke-dasharray="${f1(12.9 * zona)} ${f1(25.8 - 12.9 * zona)}" opacity="${f1(zona)}"/></g>`;
      if (t >= 1.5) s += `<image href="${M.wordmark || ""}" x="${960 - 120}" y="430" width="240" height="100"/>`;
      if (t >= 3) s += testo(960, 610, T["s9.tagline"], { size: 46, anchor: "middle" });
      if (t >= 6) s += testo(960, 680, T["s9.perimetro"], { mono: true, size: 28, anchor: "middle", fill: COL.testo2 });
      if (t >= 8.5) {
        s += testo(960, 770, T["s9.c1"], { size: 30, anchor: "middle" }) + testo(960, 812, T["s9.c2a"], { size: 24, weight: 400, anchor: "middle", fill: COL.testo2 }) +
          testo(960, 846, T["s9.c2b"], { size: 24, weight: 400, anchor: "middle", fill: COL.testo2 }) + testo(960, 890, T["s9.c3"], { mono: true, size: 20, weight: 400, anchor: "middle", fill: COL.testo2 });
      }
      if (opz.durata && t >= opz.durata - 0.5) s += `<rect x="0" y="0" width="1920" height="1080" fill="#000"/>`;
      void k;
    }
    return s;
  }

  /* ---------- 18 Sottotitoli (fascia bassa 940–1080; da .srt EN o IT convertito in assets/data/sottotitoli_*.js) ---------- */
  function Sottotitoli(riga, intest, opz) {
    const cues = (window.__SUB && window.__SUB[opz.lingua]) || null, T = opz.T;
    if (!cues) return "";
    const tg = opz.t_globale, c = cues.find((q) => tg >= q.a && tg < q.b);
    let s = "";
    if (c) {
      const righe = c.testo.split("\n");
      const h = righe.length * 52 + 24, y0 = 1080 - 40 - h;
      s += `<rect x="${960 - 820}" y="${y0}" width="1640" height="${h}" fill="${COL.fondo}" opacity="0.8"/>`;
      righe.forEach((r, i) => { s += testo(960, y0 + 54 + i * 52, r, { size: 40, anchor: "middle" }); });
    }
    if (window.__SUB.stimati) s += testo(1824, 1066, T.vo_guida, { mono: true, size: 14, weight: 400, anchor: "end", fill: COL.segnaposto });
    return s;
  }

  /* ================= v6: tempi d'ingresso (puri: dipendono solo da t) ================= */
  const morbido = (k) => 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, k)));
  const entra = (t, t0, d) => morbido((t - t0) / (d || 0.5));
  /* ingresso: dissolvenza + salita di 24 px */
  const sale = (t, t0, inner, d) => { const k = entra(t, t0, d || 0.5); if (k <= 0) return ""; return `<g opacity="${k.toFixed(3)}" transform="translate(0,${f1(24 * (1 - k))})">${inner}</g>`; };
  /* ingresso: scala dal centro (cx, cy) */
  const cresce = (t, t0, cx, cy, inner, d) => { const k = entra(t, t0, d || 0.45); if (k <= 0) return ""; const sc = 0.6 + 0.4 * k; return `<g opacity="${k.toFixed(3)}" transform="translate(${cx},${cy}) scale(${sc.toFixed(3)}) translate(${-cx},${-cy})">${inner}</g>`; };
  /* numeri che contano (solo cifre già scritte nel testo, che vengono da cifre.json) */
  const conta = (str, k) => k >= 1 ? str : String(str).replace(/\d+(?:[.,]\d+)?/g, (m) => { const v = parseFloat(m.replace(",", ".")); const d = (m.split(/[.,]/)[1] || "").length; return (v * morbido(k)).toFixed(d).replace(".", m.includes(",") ? "," : "."); });

  function FasceOnesta6(riga, intest, opz) {
    const T = opz.T;
    let lab;
    if (!riga) lab = T["onesta.schema"];
    else if (riga.dichiarazioni && /SVILUPPO/.test(riga.dichiarazioni.dati)) lab = T["onesta.dev"];
    else if (riga.dichiarazioni && /simulat|pubblic/.test(riga.dichiarazioni.dati)) {
      lab = opz.etichetta_sensore ? `${T["onesta.sim"].split(" · ")[0]} · ${opz.etichetta_sensore}` : T["onesta.sim"];
      if (opz.stato_registro === "provvisorio") lab += " · " + T["onesta.provvisorio"];
    } else lab = T["onesta.schema"];
    let s = `<rect x="0" y="0" width="1920" height="96" fill="${COL.fondo}"/>`;
    s += testo(32, 52, opz.titolo || "", { size: 40, weight: 700 }) + testo(32, 86, opz.richiesta || "", { mono: true, size: 22, weight: 400, fill: COL.testo2 });
    const w = lab.length * 28 * 0.6 + 32;
    s += `<rect x="${f1(1888 - w)}" y="12" width="${f1(w)}" height="48" fill="${COL.fondo}" stroke="${COL.testo}" stroke-width="2.5"/>` + testo(1888 - 16, 46, lab, { mono: true, size: 28, anchor: "end" });
    let d = opz.dominio || "";
    if (opz.velocita && opz.velocita !== 1) d += (d ? " · " : "") + fmt(T.compresso, { N: opz.velocita });
    if (opz.tenuto) d += (d ? " · " : "") + T.tenuto;
    if (d) s += testo(1888, 86, d, { mono: true, size: 22, weight: 400, anchor: "end", fill: opz.velocita && opz.velocita !== 1 ? COL.testo : COL.testo2 });
    return s;
  }

  function ScenaSchema6(riga, intest, opz) {
    const T = opz.T, t = opz.t, n = opz.scena;
    let s = "";
    if (n === 2) {
      // carrello lento (≤ 5 %/s: qui 4 % in 27 s) attorno al centro
      const z = 1 + 0.04 * Math.min(1, t / 27);
      s += `<g transform="translate(960,560) scale(${z.toFixed(4)}) translate(-960,-560)">`;
      s += sale(t, 0.2, testo(960, 210, T["s2.testa"], { size: 60, weight: 700, anchor: "middle" }));
      const X = [380, 960, 1540], Y = 450;
      s += cresce(t, 4, X[0], Y, `<circle cx="${X[0]}" cy="${Y}" r="72" fill="${COL.visto}"/>`);
      s += sale(t, 4.3, etichetta(X[0], Y + 160, T.stati.vista, { size: 40, fill: COL.visto, anchor: "middle" }) + testo(X[0], Y + 230, T["s2.a1"], { size: 44, anchor: "middle", fill: COL.testo2 }));
      s += cresce(t, 6.5, X[1], Y, `<ellipse cx="${X[1] + 40}" cy="${Y}" rx="220" ry="125" fill="${COL.nonvisto}" fill-opacity="0.18" stroke="${COL.nonvisto}" stroke-width="5" stroke-dasharray="18 12"/><circle cx="${X[1]}" cy="${Y}" r="70" fill="none" stroke="${COL.nonvisto}" stroke-width="9"/>`);
      s += sale(t, 6.8, etichetta(X[1], Y + 180, fmt(T.stati.non_vista, { s: "1.2" }), { size: 40, fill: COL.nonvisto, anchor: "middle" }) + testo(X[1], Y + 250, T["s2.a2"], { size: 44, anchor: "middle", fill: COL.testo2 }));
      s += cresce(t, 10, X[2], Y, `<rect x="${X[2] - 200}" y="${Y - 135}" width="400" height="270" fill="url(#righeAmbra)" stroke="${COL.nonvisto}" stroke-width="5" stroke-dasharray="18 12"/><circle cx="${X[2]}" cy="${Y}" r="60" fill="${COL.fondo}" stroke="${COL.nonvisto}" stroke-width="9"/>`);
      s += sale(t, 10.3, etichetta(X[2], Y + 195, T.stati.previsto_ampio, { size: 40, fill: COL.nonvisto, anchor: "middle" }) + testo(X[2], Y + 265, T["s2.a3"], { size: 44, anchor: "middle", fill: COL.testo2 }));
      s += "</g>";
      // dal secondo 14 i tre segni si fanno da parte: entra la fila «non verificato / possibile presenza»
      if (t >= 14) {
        const k = entra(t, 14, 0.8), sc = 1 - 0.42 * k;
        s = `<g transform="translate(960,${f1(120 + 40 * (1 - k))}) scale(${sc.toFixed(3)}) translate(-960,${f1(-120 - 40 * (1 - k))})">${s}</g>`;
        const zw = 860;
        s += sale(t, 14, `<rect x="96" y="600" width="${zw}" height="200" fill="url(#puntini)" stroke="${COL.nonoss}" stroke-width="3" stroke-dasharray="6 8"/>` + etichetta(130, 680, T.stati.zona_non_verificata, { size: 40, fill: COL.nonoss }), 0.6);
        if (t >= 15) {
          s += sale(t, 15, testo(560, 770, T["s2.nonvuoto"], { mono: true, size: 64, fill: COL.testo }), 0.4);
          const lw = T["s2.nonvuoto"].length * 38.4 + 30, kk = entra(t, 16, 0.5);
          if (kk > 0) s += `<line x1="545" y1="750" x2="${f1(545 + lw * kk)}" y2="750" stroke="${COL.testo}" stroke-width="9"/>`;
        }
        if (t >= 19) {
          const kk = entra(t, 19, 0.8), W = 860;
          s += `<rect x="1000" y="600" width="${f1(W * kk)}" height="200" fill="none" stroke="url(#righeOcra)" stroke-width="20"/>`;
          s += sale(t, 19.4, etichetta(1040, 720, T.stati.possibile_presenza, { size: 44, fill: COL.avviso }));
        }
      }
    }
    if (n === 7) {
      const righe = ["s7.l1", "s7.l2", "s7.l3", "s7.l4", "s7.l5"], tempi = [1, 6, 11, 16, 20];
      let y = 190;
      righe.forEach((k, i) => {
        const pz = spezza(T[k], 54);
        if (t >= tempi[i]) pz.forEach((p, j) => { s += sale(t, tempi[i], testo(96, y + j * 50, p, { size: 40, weight: i === 4 ? 700 : 600, fill: i === 4 ? COL.testo : COL.testo2 })); });
        y += pz.length * 50 + 22;
      });
      if (t >= 23) {
        let yy = y + 24;
        [T["s7.c_v2"], T["s7.c_v1"], T["s7.c_s7"]].forEach((c, i) => {
          const t0 = 23 + i * 0.8, k = (t - t0) / 1.2;
          spezza(conta(c, k), 60).forEach((p, j) => { s += sale(t, t0, testo(96, yy + j * 40, p, { mono: true, size: 30, weight: 400, fill: COL.testo2 })); yy += 0; });
          yy += spezza(c, 60).length * 40 + 14;
        });
      }
      s += CatenaBlocchi6(t, T, 1280, 170);
    }
    return s;
  }

  /* catena a blocchi che si disegna: un blocco ogni 0,6 s, i collegamenti si tracciano */
  function CatenaBlocchi6(t, T, x, y0) {
    const nomi = T["s7.catena"], h = 84, g = 46, w = 340;
    let s = "";
    nomi.forEach((n, i) => {
      const y = y0 + i * (h + g), t0 = 0.5 + i * 0.6;
      s += cresce(t, t0, x + w / 2, y + h / 2, `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="${COL.pannello}" stroke="${COL.testo2}" stroke-width="3"/>` + testo(x + w / 2, y + 56, n, { mono: true, size: 36, anchor: "middle" }));
      if (i < nomi.length - 1) { const k = entra(t, t0 + 0.35, 0.4); if (k > 0) s += `<line x1="${x + w / 2}" y1="${y + h}" x2="${x + w / 2}" y2="${f1(y + h + g * k)}" stroke="${COL.testo2}" stroke-width="3"/>`; }
    });
    const yc = y0 + 2 * (h + g), t1 = 4;
    const k = entra(t, t1, 0.5);
    if (k > 0) {
      s += `<line x1="${x + w}" y1="${yc + h / 2}" x2="${f1(x + w + 40 * k)}" y2="${yc + h / 2}" stroke="${COL.testo2}" stroke-width="3" stroke-dasharray="8 6"/>`;
      s += sale(t, t1 + 0.3, `<rect x="${x + w + 40}" y="${yc - 50}" width="230" height="${h + 100}" rx="8" fill="none" stroke="${COL.testo2}" stroke-width="3" stroke-dasharray="10 8"/>` +
        spezza(T["s7.classi"], 13).map((p, i) => testo(x + w + 155, yc - 6 + i * 34, p, { mono: true, size: 26, weight: 400, anchor: "middle", fill: COL.testo2 })).join(""));
    }
    return s;
  }

  function simbolo(t, cx, cy, sc) {   // simbolo SDMs v3b: disco ciano che cresce, zona ellittica tratteggiata che si disegna
    const disco = entra(t, 0, 0.5), zona = entra(t, 0.4, 1.0);
    return `<g transform="translate(${cx - 64 * sc},${cy - 42 * sc}) scale(${sc})"><circle cx="32" cy="42" r="${f1(22 * disco)}" fill="${COL.visto}"/>` +
      `<ellipse cx="95" cy="42" rx="33" ry="26" fill="none" stroke="${COL.nonvisto}" stroke-width="4" stroke-dasharray="${f1(12.9 * zona)} ${f1(25.8 - 12.9 * zona)}" opacity="${f1(zona)}"/></g>`;
  }

  function TitoloMarchio6(riga, intest, opz) {
    const M = window.__MARCHIO || {}, T = opz.T, t = opz.t;
    let s = "";
    if (opz.modo === "apertura") {
      const op = t < 2.6 ? 1 : Math.max(0, 1 - (t - 2.6) / 0.4);
      s += `<g opacity="${op.toFixed(3)}"><rect x="0" y="250" width="1920" height="560" fill="${COL.fondo}" opacity="0.9"/>` +
        simbolo(t / 0.6, 960, 330, 1.4) +
        sale(t, 0.35, `<image href="${M.wordmark || ""}" x="${960 - 144}" y="400" width="288" height="120"/>`, 0.5) +
        sale(t, 0.8, testo(960, 610, T["s1.sottotitolo"], { size: 52, weight: 700, anchor: "middle" }), 0.5) +
        sale(t, 1.2, testo(960, 690, T["s1.riga"], { mono: true, size: 28, weight: 400, anchor: "middle", fill: COL.testo2 }), 0.5) + "</g>";
    }
    if (opz.modo === "chiusura") {
      s += simbolo(t / 1.5 * 1.4, 960, 190, 3.2);
      s += sale(t, 1.5, `<image href="${M.wordmark || ""}" x="${960 - 180}" y="300" width="360" height="150"/>`, 0.6);
      s += sale(t, 3, testo(960, 540, T["s9.tagline"], { size: 54, weight: 700, anchor: "middle" }));
      s += sale(t, 6, testo(960, 610, T["s9.perimetro"], { mono: true, size: 34, anchor: "middle", fill: COL.testo2 }));
      if (t >= 8.5) {
        s += `<line x1="660" y1="660" x2="${f1(660 + 600 * entra(t, 8.5, 0.6))}" y2="660" stroke="${COL.bordo}" stroke-width="2"/>`;
        s += sale(t, 8.6, testo(960, 720, `${T["s9.c1"]} · ${T["v6.hack"]}`, { size: 40, weight: 700, anchor: "middle" }));
        s += sale(t, 8.9, testo(960, 776, T["s9.c2a"], { size: 34, weight: 500, anchor: "middle", fill: COL.testo2 }) + testo(960, 822, T["s9.c2b"], { size: 34, weight: 500, anchor: "middle", fill: COL.testo2 }));
        s += sale(t, 9.3, testo(960, 880, T["s9.c3"], { mono: true, size: 26, weight: 400, anchor: "middle", fill: COL.testo2 }));
      }
      if (opz.durata && t >= opz.durata - 0.8) s += `<rect x="0" y="0" width="1920" height="1080" fill="#000" opacity="${Math.min(1, (t - (opz.durata - 0.8)) / 0.4).toFixed(3)}"/>`;
    }
    return s;
  }

  /* lampo sulla vista della camera EO (SCHEMATICO): riquadro che satura a bianco in 3 fotogrammi e resta marcato */
  function LampoCamera(riga, intest, opz) {
    const T = opz.T, r = opz.riquadro, dt = opz.dal_lampo;
    if (dt == null || dt < 0) return "";
    const sat = Math.min(1, dt / 0.1);
    let s = `<rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}" fill="#0E131D" stroke="${COL.testo2}" stroke-width="3"/>`;
    s += testo(r.x + 14, r.y + 34, T["v6.camera"], { mono: true, size: 24, fill: COL.testo2 });
    // dentro: sagoma piatta dell'aereo, poi il bianco che satura (nessuna punta, nessun bagliore)
    s += `<g clip-path="url(#clip_CAM)">${sagoma("aereo", r.x + r.w / 2, r.y + r.h / 2 + 20, 1).replace("scale(1.0)", "scale(3.5)")}` +
      `<rect x="${r.x}" y="${r.y + 48}" width="${r.w}" height="${r.h - 48}" fill="#F4F1EA" opacity="${sat.toFixed(3)}"/></g>`;
    if (dt >= 0.1) s += testo(r.x + r.w / 2, r.y + r.h / 2 + 30, T["v6.saturo"], { mono: true, size: 40, anchor: "middle", fill: COL.fondo });
    if (dt >= 0.1) s += `<rect x="${r.x}" y="${r.y + r.h}" width="${r.w}" height="52" fill="${COL.persa}"/>` + testo(r.x + 14, r.y + r.h + 37, T["v6.camera_persa"], { mono: true, size: 28, fill: COL.fondo });
    return s;
  }

  window.MoViC = { COL, esc, fmt, tx, testo, etichetta, proiettore, pathForma, defs, spezza, entra, sale, cresce, morbido, LampoCamera,
    FasceOnesta6, ScenaSchema6, TitoloMarchio6, CatenaBlocchi6,
    PiantaArea, Sensori, Traccia, Regione, PossibilePresenza, VolumeDetriti, Nube, BandaAffidabilita, ConsoleTracce,
    VentaglioSettori, ZonaNonVerificata, Tabellone, CatenaBlocchi, VeritaSim, FasceOnesta, ScenaSchema, TitoloMarchio, Sottotitoli };
})();
