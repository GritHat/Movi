#!/usr/bin/env python3
"""v9 (montaggio finale, 2026-11-15): converte i registri VERI del prototipo (prototipo/uscite/video/*_v3, nucleo v3)
in assets/data/<ID>.js per il motore del video. Copia di registri_a_js.py con un ADATTATORE dei nomi dei campi.

Nessun valore è inventato, interpolato o corretto: si rinominano campi e si spostano dati che il registro già contiene.
Ogni trasformazione è elencata in `adattamenti` dentro il file .js. In sintesi:
  - sensori (intestazione e fotogrammi): `tipo` del prototipo -> famiglia del glifo (radar/eo/ir/lidar/cooperativo);
    il tipo vero resta in `tipo_vero`; `copertura.r_max_m` -> `portata_m`, `copertura.az_gradi` -> `campo_gradi`.
  - salute: un sensore con `affidabilita_per_sensore[].stato` diverso da «affidabile» (es. «accecato») è disegnato con
    `salute = affidabilita_persa` dallo stesso fotogramma; la causa è il `motivo` del registro.
  - eventi: `evento_contatto` -> `contatto`, `evento_avaria_o_fiammata` -> `avaria_o_fiammata` (stessi campi).
  - detriti -> volumi[0] = {forma: detriti.volume[0], forme: tutte le forme del volume, impronta: detriti.impronta[0],
    raggio_m, impronta_raggio_m} e `volumi_passati` = le forme del volume di questo stesso registro 2, 4 e 6 s prima
    (per far vedere che cresce e non si riduce).
  - meteo: dall'intestazione (lunga_portata.metriche_del_passaggio.meteo), copiato in ogni fotogramma.
  - verita.oggetti[].classe (null nel registro): dedotta dal NOME dell'oggetto (drone*, aereo*, leggero*, persona*,
    mezzo*, fr* = frammento) SOLO per scegliere la sagoma grigia; segnato `classe_da_nome`.
  - settori: tolti (nel modo lungo hanno azimut nullo: «il modo lungo non scrive visto libero fino a d»).
  - celle.rle, celle.per_sensore.*.rle, avvisi[].indici: tolti (il video non disegna le celle una per una).
Uso: python3 -I strumenti/registri_a_js_v9.py --scene scene/scene_v9.json
"""
import argparse, json, os, re, statistics, sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
OBBLIGATORI = ("tipo", "modo", "indice", "t", "dichiarazioni", "sensori", "affidabilita", "celle", "tracce", "avvisi", "eventi")
ADATTAMENTI = [
    "sensori[].tipo -> famiglia del glifo; tipo vero in tipo_vero; copertura -> portata_m, campo_gradi",
    "affidabilita_per_sensore[].stato != affidabile -> sensori[].salute = affidabilita_persa (causa = motivo)",
    "eventi: evento_contatto -> contatto; evento_avaria_o_fiammata -> avaria_o_fiammata",
    "detriti -> volumi[0] (forma, forme, impronta, raggio_m, impronta_raggio_m); volumi_passati da questo registro (-2, -4, -6 s)",
    "meteo dall'intestazione",
    "verita.oggetti[].classe dal nome (solo sagoma), classe_da_nome = true",
    "settori tolti (azimut nullo nel modo lungo)",
    "celle.rle, celle.per_sensore.*.rle, avvisi[].indici tolti",
]


def famiglia(t):
    t = (t or "").lower()
    if "radar" in t: return "radar"
    if "termica" in t or t == "ir": return "ir"
    if "camera" in t or t == "eo": return "eo"
    if "lidar" in t: return "lidar"
    if "ads" in t or "identificazione" in t or "remote" in t or "coop" in t: return "cooperativo"
    if "profondita" in t: return "profondita"
    return t


def classe_da_nome(i):
    i = str(i).lower()
    for p, c in (("drone", "multirotore"), ("aereo", "aereo"), ("leggero", "aereo_leggero"), ("persona", "persona_a_piedi"),
                 ("mezzo", "mezzo"), ("fr", "frammento")):
        if i.startswith(p): return c
    return None


def leggi(p):
    with open(p, encoding="utf-8") as f:
        L = [json.loads(x) for x in f if x.strip()]
    return L[0], [r for r in L[1:] if r.get("tipo") == "fotogramma"]


def adatta_intest(h):
    h = json.loads(json.dumps(h))
    for s in h.get("sensori", []):
        s["tipo_vero"] = s.get("tipo"); s["tipo"] = famiglia(s.get("tipo"))
        cop = s.get("copertura") or {}
        if cop.get("r_max_m"): s["portata_m"] = cop["r_max_m"]
        if cop.get("az_gradi"): s["campo_gradi"] = cop["az_gradi"]
    return h


def adatta(r, intest, storia):
    r = json.loads(json.dumps(r))
    aff = {a["sensore"]: a for a in r.get("affidabilita_per_sensore") or []}
    for s in r.get("sensori", []):
        s["tipo_vero"] = s.get("tipo"); s["tipo"] = famiglia(s.get("tipo"))
        a = aff.get(s["id"])
        if a and a.get("stato") not in (None, "affidabile") and s.get("salute") != "affidabilita_persa":
            s["salute"] = "affidabilita_persa"; s["causa"] = a.get("motivo") or a.get("stato"); s["da_affidabilita_per_sensore"] = True
    for o in (r.get("verita") or {}).get("oggetti", []):
        if not o.get("classe"):
            o["classe"] = classe_da_nome(o.get("id")); o["classe_da_nome"] = True
    for e in r.get("eventi", []):
        if e.get("tipo", "").startswith("evento_"):
            e["tipo_vero"] = e["tipo"]; e["tipo"] = e["tipo"][len("evento_"):]
    d = r.get("detriti")
    if d and d.get("volume"):
        imp = d.get("impronta")
        imp = imp[0] if isinstance(imp, list) and imp else imp
        r["volumi"] = [{"forma": d["volume"][0], "forme": d["volume"], "impronta": imp, "raggio_m": d.get("raggio_volume_m"),
                        "impronta_raggio_m": d.get("impronta_raggio_m"), "tipo": d.get("tipo"), "come_lo_so": d.get("come_lo_so")}]
        r["volumi_passati"] = [storia[x] for x in (2.0, 4.0, 6.0) if x in storia]
    met = ((intest.get("lunga_portata") or {}).get("metriche_del_passaggio") or {}).get("meteo")
    if met: r["meteo"] = met.replace("meteo_", "")
    r["settori"] = []
    c = dict(r.get("celle") or {})
    c.pop("rle", None)
    if isinstance(c.get("per_sensore"), dict):
        c["per_sensore"] = {k: {kk: vv for kk, vv in v.items() if kk != "rle"} for k, v in c["per_sensore"].items()}
    r["celle"] = c
    r["avvisi"] = [{k: v for k, v in a.items() if k != "indici"} for a in r.get("avvisi", [])]
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", default=os.path.join(RADICE, "scene", "scene_v9.json"))
    a = ap.parse_args()
    S = json.load(open(a.scene, encoding="utf-8"))
    finestre = {}
    for sc in S["scene"]:
        for g in sc.get("segmenti") or []:
            t1 = g["t_reg"] + (g["a"] - g["da"]) * g["velocita"]
            finestre.setdefault(g["registro"], []).append((g["t_reg"], t1))
        if sc.get("intest_da"):
            finestre.setdefault(sc["intest_da"], []).append((0, 0))
    problemi = 0
    for rid, wins in finestre.items():
        m = S["registri"][rid]
        p = os.path.normpath(os.path.join(RADICE, m["file"]))
        if not os.path.exists(p):
            print(f"[{rid}] MANCA {p}", file=sys.stderr); problemi += 1; continue
        if m.get("stato") == "sviluppo" or "SVILUPPO" in p:
            print(f"[{rid}] registro di sviluppo: rifiutato", file=sys.stderr); problemi += 1; continue
        intest, righe = leggi(p)
        ts = [r["t"] for r in righe]
        dt = statistics.median([b - x for x, b in zip(ts, ts[1:])]) if len(ts) > 1 else 1 / 30
        fps = round(1 / dt, 3)
        if abs(fps - round(fps)) < 0.1: fps = float(round(fps))
        lo, hi = min(w[0] for w in wins), max(w[1] for w in wins)
        tenute = [r for r in righe if lo - 1 / fps - 1e-6 <= r["t"] <= hi + 1e-6] or righe[:1]
        if hi > ts[-1] + 1e-6:
            print(f"[{rid}] il registro finisce a t={ts[-1]:.2f} s, le scene ne chiedono fino a {hi:.2f}: ultimo stato tenuto", file=sys.stderr)
        errori = sum(1 for r in tenute if any(c not in r for c in OBBLIGATORI))
        if errori:
            print(f"[{rid}] {errori} righe senza campi obbligatori", file=sys.stderr); problemi += 1
        dati = {str(r["dichiarazioni"].get("dati")) for r in tenute}
        if any("SVILUPPO" in x for x in dati):
            print(f"[{rid}] dichiarazioni.dati di sviluppo: rifiutato", file=sys.stderr); problemi += 1; continue
        vol = {r["t"]: (r.get("detriti") or {}).get("volume", [None])[0] for r in righe if (r.get("detriti") or {}).get("volume")}
        ih = adatta_intest(intest)
        out_r = []
        for r in tenute:
            storia = {k: vol[round(r["t"] - k, 4)] for k in (2.0, 4.0, 6.0) if round(r["t"] - k, 4) in vol}
            out_r.append(adatta(r, ih, storia))
        out = {"fps": fps, "t0": tenute[0]["t"], "stato": m.get("stato"), "file": m["file"], "adattamenti": ADATTAMENTI,
               "dichiarazioni_dati": sorted(dati), "intest": ih, "righe": out_r}
        q = os.path.join(RADICE, "assets", "data", f"{rid}.js")
        with open(q, "w", encoding="utf-8") as f:
            f.write("window.__REG = window.__REG || {};\nwindow.__REG[%s] = " % json.dumps(rid))
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
        print(f"[{rid}] {len(tenute)} righe, fps {fps}, t {tenute[0]['t']:.2f}–{tenute[-1]['t']:.2f}, dati={sorted(dati)} -> "
              f"{os.path.relpath(q, RADICE)} ({os.path.getsize(q) // 1024} kB)")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
