#!/usr/bin/env python3
"""Converte i registri (.jsonl, formato di prototipo/movi/registro.py) in assets/data/<ID>.js per il video.

Legge scene/scene.json (o --scene): per ogni registro elencato tiene solo le righe che le scene usano (finestre dei
segmenti, con «tieni l'ultimo»), toglie ciò che il video non disegna (rle delle celle, indici degli avvisi) e scrive
  window.__REG["ID"] = {fps, t0, stato, file, intest, righe}
Nessuna interpolazione, nessuna modifica dei valori: le righe passano come sono (salvo i campi tolti, elencati in
`tolti`). Controlla con una versione locale di valida_riga i campi obbligatori e lo segnala (non corregge).

Uso:  python3 -I strumenti/registri_a_js.py [--scene scene/scene.json] [--tempi tempi/scene_tempi.json]
"""
import argparse, json, os, statistics, sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
OBBLIGATORI = ("tipo", "modo", "indice", "t", "dichiarazioni", "sensori", "affidabilita", "celle", "settori", "tracce",
               "avvisi", "eventi")
TOLTI = ["celle.rle", "celle.per_sensore.*.rle", "avvisi[].indici"]


def leggi(p):
    with open(p, encoding="utf-8") as f:
        L = [json.loads(x) for x in f if x.strip()]
    return L[0], [r for r in L[1:] if r.get("tipo") == "fotogramma"]


def snellisci(r):
    r = dict(r)
    c = dict(r.get("celle") or {})
    c.pop("rle", None)
    if isinstance(c.get("per_sensore"), dict):
        c["per_sensore"] = {k: {kk: vv for kk, vv in v.items() if kk != "rle"} for k, v in c["per_sensore"].items()}
    r["celle"] = c
    r["avvisi"] = [{k: v for k, v in a.items() if k != "indici"} for a in r.get("avvisi", [])]
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", default=os.path.join(RADICE, "scene", "scene.json"))
    ap.add_argument("--tempi", default=os.path.join(RADICE, "tempi", "scene_tempi.json"))
    a = ap.parse_args()
    S = json.load(open(a.scene, encoding="utf-8"))
    durate = {}
    if os.path.exists(a.tempi):
        durate = {s["id"]: s for s in json.load(open(a.tempi, encoding="utf-8"))["scene"]}
    finestre = {}
    for sc in S["scene"]:
        segs = (durate.get(sc["id"]) or sc).get("segmenti") or sc.get("segmenti") or []
        for g in segs:
            t1 = g["t_reg"] + (g["a"] - g["da"]) * g["velocita"]
            finestre.setdefault(g["registro"], []).append((g["t_reg"], t1))
        if sc.get("intest_da"):
            finestre.setdefault(sc["intest_da"], []).append((0, 0))
    problemi = 0
    for rid, wins in finestre.items():
        m = S["registri"][rid]
        p = os.path.normpath(os.path.join(RADICE, m["file"]))
        if not os.path.exists(p):
            print(f"[{rid}] MANCA {p}: la scena resterà SCHEMATIC senza dati", file=sys.stderr)
            problemi += 1
            continue
        intest, righe = leggi(p)
        ts = [r["t"] for r in righe]
        dt = statistics.median([b - x for x, b in zip(ts, ts[1:])]) if len(ts) > 1 else 1 / 30
        fps = round(1 / dt, 3)
        if abs(fps - round(fps)) < 0.1:      # i tempi del registro sono arrotondati a 4 decimali
            fps = float(round(fps))
        lo, hi = min(w[0] for w in wins), max(w[1] for w in wins)
        tenute = [r for r in righe if lo - 1 / fps - 1e-6 <= r["t"] <= hi + 1e-6] or righe[:1]
        if hi > ts[-1] + 1e-6:
            print(f"[{rid}] il registro finisce a t={ts[-1]:.2f} s, le scene ne chiedono fino a {hi:.2f}: ultimo stato tenuto",
                  file=sys.stderr)
        errori = sum(1 for r in tenute if any(c not in r for c in OBBLIGATORI))
        if errori:
            print(f"[{rid}] {errori} righe senza campi obbligatori", file=sys.stderr)
            problemi += 1
        dati = {r["dichiarazioni"].get("dati") for r in tenute}
        out = {"fps": fps, "t0": tenute[0]["t"], "stato": m.get("stato"), "file": m["file"], "tolti": TOLTI,
               "dichiarazioni_dati": sorted(str(x) for x in dati), "intest": intest,
               "righe": [snellisci(r) for r in tenute]}
        q = os.path.join(RADICE, "assets", "data", f"{rid}.js")
        with open(q, "w", encoding="utf-8") as f:
            f.write("window.__REG = window.__REG || {};\nwindow.__REG[%s] = " % json.dumps(rid))
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
        print(f"[{rid}] {len(tenute)} righe, fps {fps}, t {tenute[0]['t']:.2f}–{tenute[-1]['t']:.2f}, dati={sorted(map(str, dati))}, "
              f"stato={m.get('stato')} -> {os.path.relpath(q, RADICE)} ({os.path.getsize(q) // 1024} kB)")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
