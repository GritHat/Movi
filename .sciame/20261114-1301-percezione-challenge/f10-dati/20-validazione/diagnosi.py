#!/usr/bin/env python3
"""Diagnosi di un passaggio: per fotogramma la verità, i gruppi e le tracce vicine al soggetto o al pannello.
Uso: <python> -I -B diagnosi.py <etichetta> <sequenza> [primo] [ultimo]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K
et, nome = sys.argv[1], sys.argv[2]
a = int(sys.argv[3]) if len(sys.argv) > 3 else 0
b = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
righe = K.leggi_righe(os.path.join(K.USCITE, et, nome))
ver = K.leggi_verita(os.path.join(K.SEQ_SIM, nome))
for k, r in enumerate(righe):
    if not (a <= k <= b):
        continue
    s = ver["fotogrammi"][k]["soggetti"]
    s = s[0] if s else None
    print(f"--- k={k} t={r['t']:.2f}", (f"vero x={s['x']:+.2f} z={s['z']:.2f} fraz={s['frazione_visibile']:.2f}" if s else ""),
          "celle", r["celle"], "n.gruppi", len(r["gruppi"]), "n.tracce", len(r["tracce"]))
    def vicino(x, z):
        return (s and math.hypot(x - s["x"], z - s["z"]) < 0.7) or (abs(x) < 0.8 and 1.5 < z < 2.1)
    for g in r["gruppi"]:
        if vicino(g["x"], g["z"]):
            print(f"     gruppo x={g['x']:+.2f} z={g['z']:.2f} largh={g['larghezza_m']:.2f} celle={g['celle']} punti={g['punti']} tagl={g['tagliato']}")
    for tr in r["tracce"]:
        mx, mz = tr["ultima_misura"][:2]
        if vicino(mx, mz) and tr["stato"] != "in_conferma":
            print(f"     traccia {tr['id']} {tr['stato']} mis={tr['misura_nel_ciclo']} tagl={tr['misura_tagliata']} muove={tr['si_muove']} ultima=({mx:+.2f},{mz:.2f})",
                  (f"filtro=({tr['x']:+.2f},{tr['z']:.2f}) v=({tr.get('vx',0):+.2f},{tr.get('vz',0):+.2f})" if "vx" in tr else ""))
    for e in r["eventi"]:
        if e["tipo"] not in ("nascita", "conferma", "chiusura"):
            print("     evento", e)
