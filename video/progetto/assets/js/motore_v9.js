/* MoVi · motore del video, VERSIONE v9 (montaggio finale: registri veri _v3 adattati da registri_a_js_v9.py; onestà per scena;
 * testi delle scene 1, 4, 5, 6 senza sovrapposizioni; lampo dal primo fotogramma con la camera EO non affidabile).
 * Prima: VERSIONE v7 (animatic con voce: istanti dalla scena -> cue; v6 resta).
 * MoVi · motore del video, VERSIONE v6 (revisione visiva). Base: motore.js (che resta per la v5).
 * Cambi: la vista «AS MoVi DECLARES IT» occupa il 60 % dello schermo; verità e console più piccole a destra;
 * camera a fotogrammi chiave da scene_v6.json (ferma dopo l'ultima chiave); ingresso a tendina di 0,5 s fra le scene;
 * lampo schematico sulla camera EO nella scena 6. Gli stati restano quelli del registro («tieni l'ultimo»). */
(function () {
  "use strict";
  const C = window.MoViC;
  const M = { x: 24, y: 100, w: 1380, h: 900 };              // vista principale: 1 242 000 px² = 59,9 % di 1920×1080
  const K = { x: 1428, y: 100, w: 468, h: 560 };              // console
  const V = { x: 1428, y: 700, w: 468, h: 300 };              // verità (riquadro)
  const PIENO = { x: 24, y: 100, w: 1872, h: 900 }, LARGO = { x: 24, y: 100, w: 1240, h: 900 };
  const CAM = { x: M.x + 24, y: M.y + 64, w: 480, h: 250 };   // riquadro della camera EO (scena 6, schematico)
  const ultimiEventi = {};

  function riga(idReg, tReg) {
    const R = window.__REG && window.__REG[idReg];
    if (!R) return { r: null, intest: null, i: -1 };
    const i = Math.max(0, Math.min(R.righe.length - 1, Math.floor((tReg - R.t0) * R.fps + 1e-6)));
    return { r: R.righe[i], intest: R.intest, i };
  }
  function ultimoEvento(idReg, i, tReg) {
    const R = window.__REG[idReg];
    if (!ultimiEventi[idReg]) {
      const out = []; let last = null;
      for (const r of R.righe) { for (const e of r.eventi || []) if (e.tipo === "contatto" || e.tipo === "separazione" || e.tipo === "avaria_o_fiammata") last = e; out.push(last); }
      ultimiEventi[idReg] = out;
    }
    const e = ultimiEventi[idReg][i];
    return e && tReg - e.t <= 30 ? e : null;
  }
  /* primo istante (in t di registro) in cui la camera EO perde l'affidabilità: per il lampo schematico */
  const primoLampo = {};
  function tLampo(idReg) {
    if (primoLampo[idReg] !== undefined) return primoLampo[idReg];
    const R = window.__REG[idReg]; let t = null;
    for (const r of R.righe) { if ((r.sensori || []).some((q) => q.tipo === "eo" && q.salute === "affidabilita_persa")) { t = r.t; break; } }
    return (primoLampo[idReg] = t);
  }
  const interp = (a, b, k) => ({ x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, w: a.w + (b.w - a.w) * k, h: a.h + (b.h - a.h) * k });
  function vistaCamera(sc, ts) {
    const K = sc.camera; if (!K || !K.length) return sc.vista;
    if (ts <= K[0].t) return K[0].vista;
    for (let i = 0; i < K.length - 1; i++) if (ts < K[i + 1].t) {
      const k = C.morbido((ts - K[i].t) / (K[i + 1].t - K[i].t));
      return K[i].vista.map((v, j) => v + (K[i + 1].vista[j] - v) * k);
    }
    return K[K.length - 1].vista;   // camera ferma
  }
  const intestazione = (id, r, size) => `<text x="${r.x + 6}" y="${r.y - 0}" dy="-8" font-family="JBMonoLocale" font-size="${size || 22}" font-weight="700" fill="#AEB8C5">${C.esc(id)}</text>`;
  const cornice = (r) => `<rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}" fill="#0E131D" stroke="#24344A" stroke-width="2"/>`;

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
    let s = C.defs({ M, K, PIENO, LARGO, CAM }) + `<rect width="1920" height="1080" fill="#0B0F17"/>`;
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
      // scena 1: la verità parte a tutto schermo e si restringe nel riquadro (5,0–5,8 s, morbido); la vista MoVi entra
      let rv = V, kIn = 1;
      if (n === 1) { const k = C.morbido((ts - 5) / 0.8); rv = ts < 5 ? PIENO : interp(PIENO, V, k); kIn = k; }
      const vista = vistaCamera(sc, ts);
      const Pv = C.proiettore(sc.vista_verita || vista, rv, 10), Pm = C.proiettore(vista, M, 24);
      const ov = Object.assign({}, base, { P: Pv, pannello: rv, clip: "VS", scala_sagome: rv.w > 1000 ? 2.6 : 1.2 });
      const om = Object.assign({}, base, { P: Pm, pannello: M, clip: "M", console: K, pannello_movi: M, occ: [], v9: true,
        etichette_tracce: sc.etichette_tracce, console_tracce: sc.console_tracce, max_et_presenza: sc.max_et_presenza, solo_avvisi_di: sc.solo_avvisi_di });
      s = s.replace("</defs>", `<clipPath id="clip_VS"><rect x="${rv.x}" y="${rv.y}" width="${rv.w}" height="${rv.h}"/></clipPath></defs>`);
      if (kIn > 0) {
        let m = cornice(M);
        m += C.PiantaArea(r, intest, om) + C.ZonaNonVerificata(r, intest, om) + C.Sensori(r, intest, om) + C.VentaglioSettori(r, intest, om) +
          C.Nube(r, intest, om) + C.Regione(r, intest, om) + C.PossibilePresenza(r, intest, om) + C.VolumeDetriti(r, intest, om) + C.Traccia(r, intest, om);
        m += C.ConsoleTracce(r, intest, Object.assign({}, om, { ultimo_evento: ultimoEvento(segi.seg.registro, i, segi.tReg) })) + C.BandaAffidabilita(r, intest, om);
        m += intestazione(T["pannello.movi"], M) + intestazione(T["pannello.console"], K);
        m += testiScena(n, ts, r, intest, T, Pm, segi);
        // lampo schematico sulla camera EO (scena 6): dal primo fotogramma con la fiammata nel registro
        if (n === 6) { const tl = tLampo(segi.seg.registro); if (tl != null) m += C.LampoCamera(r, intest, Object.assign({}, base, { riquadro: CAM, dal_lampo: segi.tReg - tl })); }
        corpo += kIn < 1 ? `<g opacity="${kIn.toFixed(3)}">${m}</g>` : m;
      }
      corpo += C.VeritaSim(r, intest, ov) + intestazione(rv.w > 1000 ? T["pannello.verita"] : T["v6.verita_breve"] || T["pannello.verita"], rv);
    } else if (sc.tipo === "dati" && n === 8) {
      // ponte: la console si rimpicciolisce (0–1,5 s) e lascia il posto alla scena a corto raggio
      const k = C.morbido(ts / 1.5), rc = interp(K, { x: 1560, y: 760, w: 120, h: 80 }, k);
      corpo += `<rect x="${rc.x}" y="${rc.y}" width="${rc.w}" height="${rc.h}" fill="#121826" stroke="#24344A" stroke-width="2" opacity="${(1 - k).toFixed(2)}"/>`;
    } else if (sc.tipo === "schema") {
      if (n === 3) corpo += scena3(ts, T, base);
      else corpo += C.ScenaSchema6(null, null, Object.assign({}, base, { scena: n }));
    } else if (sc.tipo === "titoli") {
      corpo += C.TitoloMarchio6(null, null, Object.assign({}, base, { modo: "chiusura", durata: sc.durata }));
    }
    // ingresso a tendina (0,5 s) per le scene 2–7; la 1 apre col titolo, la 8 ha il suo ponte, la 9 i titoli
    if (n >= 2 && n <= 7 && ts < 0.5) {
      const k = C.morbido(ts / 0.5), xw = 1920 * k;
      corpo = `<clipPath id="clip_TENDINA"><rect x="0" y="0" width="${xw.toFixed(1)}" height="1080"/></clipPath><g clip-path="url(#clip_TENDINA)">${corpo}</g>` +
        `<rect x="${(xw - 6).toFixed(1)}" y="96" width="6" height="984" fill="#AEB8C5"/>`;
    }
    s += corpo;
    if (n === 1 && ts < 3) s += C.TitoloMarchio6(null, null, Object.assign({}, base, { modo: "apertura" }));
    if (sc.tipo !== "titoli") s += C.FasceOnesta6(r, intest, Object.assign({}, base, {
      titolo: T[`s${n}.titolo`], richiesta: T[`s${n}.richiesta`], dominio: sc.dominio ? T[sc.dominio] : "", onesta: sc.onesta || "schema",
      velocita: segi ? segi.seg.velocita : 1, tenuto: segi ? segi.tenuto : false, stato_registro: statoReg,
      etichetta_sensore: segi ? (meta[segi.seg.registro] || {}).etichetta_sensore : null }));
    s += C.Sottotitoli(null, null, Object.assign({}, base, { t_globale: t }));
    return s;
  }

  function testiScena(n, ts, r, intest, T, P, segi) {
    // v9: in basso a sinistra UNA riga di cifre alla volta (la più recente), sopra la fascia dei sottotitoli;
    // in alto a destra una colonna fissa per le etichette di dominio della scena (schematico, raggi dal registro)
    let s = "", y = M.y + M.h - 130, yd = M.y + 64;
    const sotto = (k, o) => { if (!T[k]) return; const pz = C.spezza(T[k], 74); for (let i = pz.length - 1; i >= 0; i--) { s += C.etichetta(M.x + 20, y, pz[i], Object.assign({ size: 28, fill: "#E8EDF2", bgop: 0.94 }, o || {})); y -= 46; } y -= 8; };
    const destra = (txt, o) => { if (!txt) return; s += C.etichetta(M.x + M.w - 24, yd, txt, Object.assign({ size: n === 6 ? 23 : 26, fill: "#E8EDF2", anchor: "end", bgop: 0.94 }, o || {})); yd += 46; };
    const tag = (k) => destra(T[k], { fill: "#0B0F17", bg: "#AEB8C5", bgop: 1 });
    const volumi = () => { for (const v of r.volumi || []) {
      destra(C.fmt(T.volume_r, { m: Math.round(v.raggio_m || 0) }), { fill: "#C7841A" });
      if (v.impronta_raggio_m) destra(C.fmt(T.impronta_r, { km: (v.impronta_raggio_m / 1000).toFixed(1) }), { fill: "#AEB8C5" }); } };
    yd += 50;   // sotto la scala grafica
    if (n === 1) {
      sotto("s1.c0", { fill: "#8A97A8", size: 24 });
      if (ts >= C.CUE(1, "conf", 4)) sotto("s1.conf");
    }
    if (n === 4) {
      // portata DICHIARATA dal nucleo (campo portata_dichiarata del registro): nominale tratteggiata, dichiarata piena
      const rad = (intest.sensori || []).find((x) => x.tipo === "radar");
      if (rad && r.portata_dichiarata) {
        const cx = P.x(rad.pos[0]), cy = P.y(rad.pos[1]);
        s += `<g clip-path="url(#clip_M)">`;
        r.portata_dichiarata.forEach((q, i) => {
          s += `<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${P.r(q.nominale_m).toFixed(1)}" fill="none" stroke="#AEB8C5" stroke-width="2" stroke-dasharray="6 8"/>`;
          s += `<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${P.r(q.dichiarata_nucleo_m).toFixed(1)}" fill="none" stroke="#E8EDF2" stroke-width="3"/>`;
          const lab = C.fmt(T["s4.cerchio"], { classe: T.classi[q.classe] || q.classe, d: Math.round(q.dichiarata_nucleo_m), nom: Math.round(q.nominale_m) });
          s += C.etichetta(cx + 16, i === 0 ? cy + P.r(q.dichiarata_nucleo_m) + 38 : cy - P.r(q.dichiarata_nucleo_m) - 14, lab, { size: 26, fill: "#E8EDF2", lim: { x: M.x, y: M.y + 150, w: M.w, h: M.h - 290 } });
        });
        s += `</g>`;
      }
      tag("s4.nebbia_tag");
      if (ts >= C.CUE(4, "portata", 4)) sotto("s4.portata");
    }
    if (n === 5) {
      if (r.volumi) { tag("s5.tag_zona"); volumi(); }
      if (ts >= C.CUE(5, "zona", 9)) sotto("s5.zona"); else if (ts >= C.CUE(5, "rit", 3)) sotto("s5.e1");
    }
    if (n === 6) {
      destra(T["s6.radar"]);
      if (r.volumi) { tag("s6.tag_zona"); volumi(); }
      if (ts >= C.CUE(6, "avviso", 15)) sotto("s6.avviso_mezzo"); else if (ts >= C.CUE(6, "camere", 4)) sotto("s6.camere");
    }
    if (n === 8) { s += `<rect x="${M.x + 2}" y="${M.y + M.h - 230}" width="${M.w - 4}" height="100" fill="#0B0F17" opacity="0.92"/>`; C.spezza(T["s8.riga"], 64).forEach((p, i) => { s += C.testo(M.x + 24, M.y + M.h - 192 + i * 44, p, { size: 36, weight: 600, fill: "#E8EDF2" }); }); }
    return s;
  }

  function scena3(ts, T, base) {
    const sc = window.__SCENE.scene.find((q) => q.n === 3);
    const R = window.__REG && window.__REG[sc.intest_da];
    let s = `<rect x="${LARGO.x}" y="${LARGO.y}" width="${LARGO.w}" height="${LARGO.h}" fill="#0E131D" stroke="#24344A" stroke-width="2"/>`;
    if (!R) return s;
    // carrello lento (≤ 5 %/s): 6 % in 16 s, verso i sensori
    const z = 1 + 0.06 * Math.min(1, ts / 16);
    const v = sc.vista, cx = 0, cy = 20, vz = [cx + (v[0] - cx) / z, cy + (v[1] - cy) / z, cx + (v[2] - cx) / z, cy + (v[3] - cy) / z];
    const P = C.proiettore(vz, LARGO, 30);
    const o = Object.assign({}, base, { P, pannello: LARGO, clip: "LARGO", sensori_visibili: Math.min(R.intest.sensori.length, ts < C.CUE(3, "sensori_da", 0) ? 0 : 1 + Math.floor((ts - C.CUE(3, "sensori_da", 0)) / C.CUE(3, "sensori_passo", 1.6))) });
    s += C.PiantaArea(null, R.intest, o) + C.Sensori(null, R.intest, o);
    const rad = R.intest.sensori.find((x) => x.tipo === "radar"), cxp = P.x(rad.pos[0]), cyp = P.y(rad.pos[1]);
    const tA = C.CUE(3, "archi", 9);
    if (ts >= tA) {
      // archi, non cerchi interi (Q33); si disegnano in 0,8 s
      const k = C.entra(ts, tA, 0.8);
      const arco = (rr) => { const a0 = -20 * Math.PI / 180, a1 = (-20 - 60 * k) * Math.PI / 180; return `M${(cxp + rr * Math.cos(a0)).toFixed(1)},${(cyp + rr * Math.sin(a0)).toFixed(1)} A${rr},${rr} 0 0,0 ${(cxp + rr * Math.cos(a1)).toFixed(1)},${(cyp + rr * Math.sin(a1)).toFixed(1)}`; };
      s += `<g clip-path="url(#clip_LARGO)"><path d="${arco(640)}" fill="none" stroke="#AEB8C5" stroke-width="4" stroke-dasharray="16 10"/><path d="${arco(200)}" fill="none" stroke="#AEB8C5" stroke-width="4"/></g>`;
      s += C.sale(ts, tA + 0.6, C.etichetta(cxp + 150, cyp - 210, T["s3.drone"], { size: 28, fill: "#AEB8C5" }) + C.etichetta(cxp + 420, cyp - 560, T["s3.aereo"], { size: 28, fill: "#AEB8C5" }));
      const dx = cxp + 330, dy = cyp - 330;
      s += C.cresce(ts, tA + 0.8, dx, dy, `<g><rect x="${dx - 9}" y="${dy - 9}" width="18" height="18" fill="#5E6A7B"/>${[[-16, -16], [16, -16], [16, 16], [-16, 16]].map((p) => `<circle cx="${dx + p[0]}" cy="${dy + p[1]}" r="9" fill="none" stroke="#5E6A7B" stroke-width="4"/>`).join("")}</g>`);
      s += C.testo(LARGO.x + 24, LARGO.y + LARGO.h - 30, T["s3.scala"], { mono: true, size: 22, weight: 400, fill: "#AEB8C5" });
    }
    const X = 1300;
    s += C.sale(ts, C.CUE(3, "terra", 0.6), C.spezza(T["s3.terra"], 26).map((p, i) => C.testo(X, 200 + i * 46, p, { size: 38, weight: 700, fill: "#E8EDF2" })).join(""));
    if (ts >= tA) s += C.sale(ts, tA, C.spezza(T["s3.portata"], 28).map((p, i) => C.testo(X, 340 + i * 44, p, { size: 36, fill: "#AEB8C5" })).join(""));
    if (ts >= tA + 1 && T["s3.riga1"]) s += C.sale(ts, tA + 1, C.spezza(T["s3.riga1"], 36).map((p, i) => C.testo(X, 500 + i * 34, p, { mono: true, size: 26, weight: 400, fill: "#AEB8C5" })).join(""));
    if (ts >= C.CUE(3, "riga2", 13)) s += C.sale(ts, C.CUE(3, "riga2", 13), C.spezza(T["s3.riga2"], 26).map((p, i) => C.testo(X, 740 + i * 48, p, { size: 40, weight: 700, fill: "#E8EDF2" })).join(""));
    return s;
  }

  window.MoViMotore = { disegna };
})();
