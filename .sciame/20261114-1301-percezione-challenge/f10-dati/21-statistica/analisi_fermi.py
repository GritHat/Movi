#!/usr/bin/env python3
"""sciame-statistico — rumore del centro di una persona ferma dalla replica con semi nuovi (tabelle/fermi_replica*.json).
Unità: la sequenza (un seme). Mediana fra i semi con IC bootstrap sui semi; in più la quota di semi sopra 1 cm e
il massimo. Uso: <python> -I -B analisi_fermi.py"""
import glob
import json
import math
import os

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(5)
D = []
for f in sorted(glob.glob(os.path.join(QUI, "tabelle", "fermi_replica.json"))):
    D += json.load(open(f, encoding="utf-8"))
NOM = {2.0: 1.5, 3.0: 3.4, 4.0: 6.0}
VAL = {(2.0, 3): 0.36, (3.0, 3): 0.99, (4.0, 3): 1.25, (2.0, 40): 0.13, (3.0, 40): 0.36, (4.0, 40): 0.69}
print("distanza; soglia; semi con ≥30 centri su 45; sigma radiale cm: mediana [IC bootstrap sui semi], 90° percentile, massimo; "
      "trasversale mediana; falsi «si muove»; cifra della validazione (altri semi); curva nominale")
for p in (3, 40):
    for d in (2.0, 3.0, 4.0):
        sr, st, fm, n = [], [], 0, 0
        for r in D:
            if r["p"] != p or r["distanza"] != d:
                continue
            n += 1
            fm += r["si_muove"]
            c = np.array(r["centri"])
            if len(c) < 30:
                continue
            r0 = math.hypot(0.3, d)
            ur, ut = np.array([0.3, d]) / r0, np.array([d, -0.3]) / r0
            sr.append(100 * np.std(c[:, :2] @ ur))
            st.append(100 * np.std(c[:, :2] @ ut))
        if not sr:
            continue
        sr = np.array(sr)
        b = [np.median(sr[rng.integers(0, len(sr), len(sr))]) for _ in range(4000)]
        print(f"{d} m; {p}; {len(sr)}/{n}; {np.median(sr):.2f} [{np.percentile(b, 2.5):.2f}–{np.percentile(b, 97.5):.2f}], "
              f"{np.percentile(sr, 90):.2f}, {sr.max():.2f}; {np.median(st):.2f}; {fm}/{n}; {VAL[(d, p)]}; {NOM[d]}")
