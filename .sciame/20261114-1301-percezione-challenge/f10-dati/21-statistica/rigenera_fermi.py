#!/usr/bin/env python3
"""sciame-statistico — REPLICA (non ricalcolo) del rumore del centro di una persona ferma a 2 / 3 / 4 m.

La validazione non ha conservato i valori per seme (solo mediana e massimo in uscite/mem_fermi*.json): qui si
rigenerano 20 sequenze per distanza con SEMI NUOVI (nome «stat_ferma_…», quindi un altro seme di rumore), si passano
nella catena con le soglie del nucleo (3) e con 40, e si salvano i centri per fotogramma. Il simulatore (11-simulatore)
e la catena (10-catena) sono importati in sola lettura; la misura (scarto tipo del centro del gruppo più vicino entro
0,35 m, radiale e trasversale, almeno 30 fotogrammi su 45) ha la stessa definizione della validazione, codice mio.
Uso: timeout 290 <python> -I -B rigenera_fermi.py  → tabelle/fermi_replica.json (circa 210 s)"""
import dataclasses
import json
import math
import os
import sys

for _n in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_n, "1")
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
F10 = os.path.dirname(QUI)
sys.path.insert(0, os.path.join(F10, "10-catena"))
sys.path.insert(0, os.path.join(F10, "11-simulatore"))
import numpy as np                       # noqa: E402
import catalogo as C                     # noqa: E402
import genera as G                       # noqa: E402
from catena import Catena                # noqa: E402
from parametri import Parametri          # noqa: E402

fuori = []
for d in (2.0, 3.0, 4.0):
    for seme in range(20):
        spec = C._spec("stat", "d435i", "nominale", "pavimento", f"stat_ferma_{d}__s{seme:02d}", n=45,
                       persone=[C._ferma(0.3, d)])
        tempi, quadri, extra = [], [], None
        for i, t, f, ver, extra in G.simula(spec):
            tempi.append(t)
            quadri.append(f)
        meta, _ = G.meta_e_verita(spec, extra["prof"], extra["cam"], extra["scena"], extra["tracce"], [])
        for p in (3, 40):
            cat = Catena(meta, dataclasses.replace(Parametri(), portata_m=4.5, min_punti_ostacolo=p))
            centri, muove = [], False
            for i, (t, f) in enumerate(zip(tempi, quadri)):
                r = cat.ciclo(i, t, f)
                g = min(r["gruppi"], key=lambda g_: math.hypot(g_["x"] - 0.3, g_["z"] - d), default=None)
                if g is not None and math.hypot(g["x"] - 0.3, g["z"] - d) < 0.35:
                    centri.append([g["x"], g["z"], g["celle"]])
                for tr in r["tracce"]:
                    if (tr["stato"] != "in_conferma" and tr["misura_nel_ciclo"] and tr["si_muove"] is True
                            and math.hypot(tr["ultima_misura"][0] - 0.3, tr["ultima_misura"][1] - d) < 0.35):
                        muove = True
            fuori.append({"distanza": d, "seme": seme, "p": p, "centri": centri, "si_muove": muove})
        print(d, seme, flush=True)
os.makedirs(os.path.join(QUI, "tabelle"), exist_ok=True)
with open(os.path.join(QUI, "tabelle", "fermi_replica.json"), "w", encoding="utf-8") as f:
    json.dump(fuori, f)
