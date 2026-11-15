/* MoVi · motore del video: dato il tempo globale t (s), sceglie la scena, il tratto di registro e la riga
 * («tieni l'ultimo», nessuna interpolazione degli stati) e compone i componenti in una stringa SVG.
 * Dati attesi (file JS locali, nessun fetch):
 *   window.__SCENE  da tempi/scene_tempi.js (monta.py)       window.__REG[id] da assets/data/<id>.js (registri_a_js.py)
 *   window.__TESTI, window.__LINGUA da testi/testi.js        window.__MARCHIO da assets/marchio/marchio.js
 *   window.__SUB (facoltativo) da assets/data/sottotitoli.js */
(function () {
  "use strict";
  const C = window.MoViC;
  const V = { x: 96, y: 160, w: 480, h: 690 }, M = { x: 600, y: 160, w: 784, h: 690 }, K = { x: 1408, y: 160, w: 416, h: 690 };
  const PIENO = { x: 96, y: 160, w: 1728, h: 690 }, LARGO = { x: 96, y: 160, w: 1100, h: 690 };
  const ultimiEventi = {};

  function riga(idReg, tReg) {
    const R = window.__REG && window.__REG[idReg];
    if (!R) return { r: null, intest: null, i: -1 };
    const i = Math.max(0, Math.min(R.righe.length - 1, Math.floor((tReg - R.t0) * R.fps + 1e-6)));
    return { r: R.righe[i], intest: R.intest, i };
  }
  function ultimoEvento(idReg, i, tReg) {
    const R = window.__REG[idReg];
    if (!ultimiEventi[idReg]) {   // precalcolo deterministico: per ogni riga l'ultimo evento di tipo noto
      const out = []; let last = null;
      for (const r of R.righe) { for (const e of r.eventi || []) if (e.tipo === "contatto" || e.tipo === "separazione") last = e; out.push(last); }
      ultimiEventi[idReg] = out;
    }
    const e = ultimiEventi[idReg][i];
    return e && tReg - e.t <= 30 ? e : null;
  }
  function interp(a, b, k) { return { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, w: a.w + (b.w - a.w) * k, h: a.h + (b.h - a.h) * k }; }
  function intestazione(id, r) { return `<text x="${r.x + 4}" y="${r.y - 10}" font-family="JBMonoLocale" font-size="18" font-weight="700" fill="#AEB8C5">${C.esc(id)}</text>`; }

  function scenaCorrente(t) {
    const S = window.__SCENE.scene;
    for (const s of S) if (t >= s.inizio && t < s.inizio + s.durata) return s;
    return S[S.length - 1];
  }
  function segmento(sc, ts) {
    if (!sc.segmenti) return null;
    let seg = null;
    for (const g of sc.segmenti) if (ts >= g.da) seg = g;
    if (!seg) seg = sc.segmenti[0];
    const dentro = ts < seg.a;
    const tReg = seg.t_reg + (Math.min(ts, seg.a) - seg.da) * seg.velocita;
    return { seg, tReg, tenuto: !dentro && ts >= seg.a && sc.tieni_ultimo_fino_a != null };
  }

  function disegna(t) {
    const T = window.__TESTI[window.__LINGUA], sc = scenaCorrente(t), ts = t - sc.inizio, n = sc.n;
    const meta = window.__SCENE.registri || {};
    let s = C.defs({ V, M, K, PIENO, LARGO }) + `<rect width="1920" height="1080" fill="#0B0F17"/>`;
    let r = null, intest = null, segi = null, i = -1;
    if (sc.tipo === "dati") {
      segi = segmento(sc, ts);
      const q = riga(segi.seg.registro, segi.tReg); r = q.r; intest = q.intest; i = q.i;
      if (n === 8 && ts < segi.seg.da) { r = null; }
    }
    const statoReg = segi ? (meta[segi.seg.registro] || {}).stato : null;
    const base = { T, t: ts, lingua: window.__LINGUA, scena: n };
    let corpo = "";

    if (sc.tipo === "dati" && intest && r) {
      // pannelli: nella scena 1 la verità parte a tutto schermo e si restringe a 5–5,5 s (lineare)
      let rv = V;
      if (n === 1) rv = ts < 5 ? PIENO : (ts < 5.5 ? interp(PIENO, V, (ts - 5) / 0.5) : V);
      const Pv = C.proiettore(sc.vista, rv, 16), Pm = C.proiettore(sc.vista, M, 24);
      const ov = Object.assign({}, base, { P: Pv, pannello: rv, clip: "VS" });
      const om = Object.assign({}, base, { P: Pm, pannello: M, clip: "M", console: K, pannello_movi: M, occ: [] });
      s = s.replace("</defs>", `<clipPath id="clip_VS"><rect x="${rv.x}" y="${rv.y}" width="${rv.w}" height="${rv.h}"/></clipPath></defs>`);
      const mostraTre = !(n === 1 && ts < 5.5);
      if (mostraTre) {
        corpo += `<rect x="${M.x}" y="${M.y}" width="${M.w}" height="${M.h}" fill="#0E131D" stroke="#24344A" stroke-width="2"/>`;
        corpo += C.PiantaArea(r, intest, om) + C.ZonaNonVerificata(r, intest, om) + C.Sensori(r, intest, om) + C.VentaglioSettori(r, intest, om) +
          C.Nube(r, intest, om) + C.VolumeDetriti(r, intest, om) + C.Regione(r, intest, om) + C.PossibilePresenza(r, intest, om) + C.Traccia(r, intest, om);
        corpo += C.ConsoleTracce(r, intest, Object.assign({}, om, { ultimo_evento: ultimoEvento(segi.seg.registro, i, segi.tReg) })) + C.BandaAffidabilita(r, intest, om);
        corpo += intestazione(T["pannello.movi"], M) + intestazione(T["pannello.console"], K);
      }
      corpo += C.VeritaSim(r, intest, ov) + intestazione(T["pannello.verita"], rv);
      corpo += testiScena(n, ts, r, intest, T, Pm, segi);
    } else if (sc.tipo === "dati" && n === 8) {
      // ponte: la console della scena 6 si rimpicciolisce (0–1,5 s) e lascia il posto alla scena a corto raggio
      const k = Math.min(1, ts / 1.5), rc = interp(K, { x: 1560, y: 760, w: 120, h: 80 }, k);
      corpo += `<rect x="${rc.x}" y="${rc.y}" width="${rc.w}" height="${rc.h}" fill="#121826" stroke="#24344A" stroke-width="2" opacity="${(1 - k).toFixed(2)}"/>`;
    } else if (sc.tipo === "schema") {
      if (n === 3) corpo += scena3(ts, T, base);
      else corpo += C.ScenaSchema(null, null, Object.assign({}, base, { scena: n }));
    } else if (sc.tipo === "titoli") {
      corpo += C.TitoloMarchio(null, null, Object.assign({}, base, { modo: "chiusura", durata: sc.durata }));
    }
    s += corpo;
    if (n === 1 && ts < 3) s += C.TitoloMarchio(null, null, Object.assign({}, base, { modo: "apertura" }));
    if (sc.tipo !== "titoli") s += C.FasceOnesta(r, intest, Object.assign({}, base, {
      titolo: T[`s${n}.titolo`], richiesta: T[`s${n}.richiesta`], dominio: sc.dominio ? T[sc.dominio] : "",
      velocita: segi ? segi.seg.velocita : 1, tenuto: segi ? segi.tenuto : false, stato_registro: statoReg,
      etichetta_sensore: segi ? (meta[segi.seg.registro] || {}).etichetta_sensore : null }));
    s += C.Sottotitoli(null, null, Object.assign({}, base, { t_globale: t }));
    return s;
  }

  function testiScena(n, ts, r, intest, T, P, segi) {
    let s = "";
    const riga = (y, k) => C.etichetta(M.x + 16, y, T[k], { size: 19, fill: "#AEB8C5", bgop: 0.92 });
    if (n === 4) {
      const eo = (intest.sensori || []).find((x) => x.tipo === "eo");
      const x = eo ? P.x(eo.pos[0]) + 30 : M.x + 30, y = eo ? P.y(eo.pos[1]) + 60 : M.y + 80;
      if (ts < 7) s += C.etichetta(Math.min(x, M.x + M.w - 560), y, T["s4.nebbia"], { size: 22, fill: "#E8EDF2" });
      else if (ts < 11) s += C.etichetta(Math.min(x, M.x + M.w - 400), y, T["s4.pioggia"], { size: 22, fill: "#E8EDF2" });
      const la = (r.tracce || []).find((q) => q.id === "leggero1");
      if (la) { const c = la.pos ? [P.x(la.pos[0]), P.y(la.pos[1])] : null; if (c) s += C.etichetta(c[0] + 18, c[1] + 50, T["s4.noncoop"], { size: 20, fill: "#AEB8C5" }); }
    }
    if (n === 5) {
      if (r.volumi) s += riga(M.y + M.h - 58, "s5.mai");
      s += riga(M.y + M.h - 22, "s5.v3");
      if (ts >= 19) s += C.etichetta(M.x + 24, M.y + 60, T["s5.fine"], { size: 22, fill: "#8A97A8" });
      if (r.volumi) s += C.etichetta(V.x + 8, V.y + V.h - 14, T["s5.nocontatto"], { size: 16, fill: "#AEB8C5" });
    }
    if (n === 6) s += C.etichetta(M.x + 24, M.y + 60, T["s6.radar"], { size: 22, fill: "#E8EDF2" });
    if (n === 8) { s += `<rect x="${M.x + 2}" y="${M.y + M.h - 96}" width="${M.w - 4}" height="94" fill="#0B0F17" opacity="0.92"/>`; C.spezza(T["s8.riga"], 60).forEach((p, i) => { s += C.testo(M.x + 24, M.y + M.h - 58 + i * 34, p, { size: 24, weight: 600, fill: "#E8EDF2" }); }); }
    return s;
  }

  function scena3(ts, T, base) {
    const R = window.__REG && window.__REG[window.__SCENE.scene.find((q) => q.n === 3).intest_da];
    let s = `<rect x="${LARGO.x}" y="${LARGO.y}" width="${LARGO.w}" height="${LARGO.h}" fill="#0E131D" stroke="#24344A" stroke-width="2"/>`;
    if (!R) return s;
    const sc = window.__SCENE.scene.find((q) => q.n === 3), P = C.proiettore(sc.vista, LARGO, 30);
    const o = Object.assign({}, base, { P, pannello: LARGO, clip: "LARGO", sensori_visibili: Math.min(R.intest.sensori.length, 1 + Math.floor(ts / 2)) });
    s += C.PiantaArea(null, R.intest, o) + C.Sensori(null, R.intest, o);
    // schema delle portate per classe (NON in scala): cerchio grande «aircraft», piccolo «small drone»
    const rad = R.intest.sensori.find((x) => x.tipo === "radar"), cx = P.x(rad.pos[0]), cy = P.y(rad.pos[1]);
    if (ts >= 9) {
      // archi, non cerchi interi: due cerchi concentrici si leggerebbero come un bersaglio (Q33)
      const arco = (r) => { const a0 = -20 * Math.PI / 180, a1 = -80 * Math.PI / 180; return `M${(cx + r * Math.cos(a0)).toFixed(1)},${(cy + r * Math.sin(a0)).toFixed(1)} A${r},${r} 0 0,0 ${(cx + r * Math.cos(a1)).toFixed(1)},${(cy + r * Math.sin(a1)).toFixed(1)}`; };
      s += `<g clip-path="url(#clip_LARGO)"><path d="${arco(520)}" fill="none" stroke="#AEB8C5" stroke-width="2.5" stroke-dasharray="12 8"/><path d="${arco(150)}" fill="none" stroke="#AEB8C5" stroke-width="2.5"/></g>`;
      s += C.etichetta(cx + 120, cy - 160, T["s3.drone"], { size: 20, fill: "#AEB8C5" }) + C.etichetta(cx + 360, cy - 440, T["s3.aereo"], { size: 20, fill: "#AEB8C5" });
      // il multirotore piccolo fuori dalla portata per la sua classe
      const dx = cx + 260, dy = cy - 260;
      s += `<g><rect x="${dx - 5}" y="${dy - 5}" width="10" height="10" fill="#5E6A7B"/>${[[-9, -9], [9, -9], [9, 9], [-9, 9]].map((p) => `<circle cx="${dx + p[0]}" cy="${dy + p[1]}" r="5" fill="none" stroke="#5E6A7B" stroke-width="2.5"/>`).join("")}</g>`;
      s += C.testo(LARGO.x + 24, LARGO.y + LARGO.h - 60, T["s3.scala"], { mono: true, size: 18, weight: 400, fill: "#AEB8C5" });
    }
    const X = 1240;
    s += C.testo(X, 240, T["s3.terra"], { mono: true, size: 24, fill: "#E8EDF2" });
    if (ts >= 9) C.spezza(T["s3.portata"], 30).forEach((p, i) => { s += C.testo(X, 320 + i * 34, p, { mono: true, size: 24, fill: "#AEB8C5" }); });
    if (ts >= 10) C.spezza(T["s3.riga1"], 34).forEach((p, i) => { s += C.testo(X, 460 + i * 34, p, { mono: true, size: 22, weight: 400, fill: "#AEB8C5" }); });
    if (ts >= 13) s += C.testo(X, 700, T["s3.riga2"], { size: 30, fill: "#E8EDF2" });
    return s;
  }

  window.MoViMotore = { disegna };
})();
