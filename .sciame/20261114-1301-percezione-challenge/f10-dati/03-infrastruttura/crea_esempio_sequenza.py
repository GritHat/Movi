#!/usr/bin/env python3
"""Scrive una piccola sequenza d'esempio nel formato comune (vedi formato_sequenza.md).

    f10-dati/ambiente/venv/bin/python -I crea_esempio_sequenza.py <cartella_nuova>

È un esempio DEL FORMATO, non un modello di sensore: geometria ideale, niente rumore, niente buchi.
Scena: suolo piano; un ostacolo (pannello verticale largo 0,6 m e alto 2 m, a z = 1,5 m); un soggetto
(pannello verticale largo 0,5 m e alto 1,7 m) che a z = 2,5 m va da x = -1 m a x = +1 m in 2 s e passa
dietro l'ostacolo. Camera a 1,2 m da terra, inclinata di 15° verso il basso, 160x120 pixel, 15 fps.
"""
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True  # niente __pycache__ accanto agli script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from controlla_sequenza import scrivi_sequenza  # noqa: E402

L, A, FPS, N = 160, 120, 15.0, 31
FX = FY = (L / 2) / math.tan(math.radians(87.0 / 2))  # campo orizzontale di 87°, scelto solo per l'esempio
CX, CY = (L - 1) / 2, (A - 1) / 2
H, INCL = 1.2, 15.0
PORTATA_MM = 10000
OSTACOLO = {"x": 0.0, "z": 1.5, "larghezza": 0.6, "altezza": 2.0}
SOGGETTO = {"z": 2.5, "larghezza": 0.5, "altezza": 1.7}

t = math.radians(INCL)
u, v = np.meshgrid((np.arange(L) - CX) / FX, (np.arange(A) - CY) / FY)  # direzione del raggio: (u, v, 1)
giu = v * math.cos(t) + math.sin(t)       # componente verso il basso del raggio
avanti = math.cos(t) - v * math.sin(t)    # componente orizzontale in avanti
suolo = np.where(giu > 1e-9, H / np.maximum(giu, 1e-9), np.inf)  # profondità lungo l'asse ottico, in metri


def pannello(x, z, larghezza, altezza):
    """Profondità (m) di un pannello verticale di fronte alla camera, a distanza orizzontale z; inf dove manca."""
    p = np.where(avanti > 1e-9, z / np.maximum(avanti, 1e-9), np.inf)
    quota = H - p * giu
    dentro = (np.abs(p * u - x) <= larghezza / 2) & (quota >= 0) & (quota <= altezza)
    return np.where(dentro, p, np.inf)


def in_millimetri(prof):
    mm = np.where(np.isfinite(prof), np.rint(prof * 1000.0), 0)
    return np.where(mm > PORTATA_MM, 0, mm).astype(np.uint16)  # oltre la portata dell'esempio: nessun dato


ostacolo = pannello(OSTACOLO["x"], OSTACOLO["z"], OSTACOLO["larghezza"], OSTACOLO["altezza"])
fotogrammi, tempi, verita_fot = [], [], []
for i in range(N):
    x = -1.0 + 2.0 * i / (N - 1)
    sogg = pannello(x, SOGGETTO["z"], SOGGETTO["larghezza"], SOGGETTO["altezza"])
    scena = np.minimum(np.minimum(suolo, ostacolo), sogg)
    suoi = np.isfinite(sogg)  # i pixel che il soggetto occuperebbe da solo
    visti = suoi & (sogg <= scena)
    frazione = float(visti.sum() / max(1, suoi.sum()))
    fotogrammi.append(in_millimetri(scena))
    tempi.append(i / FPS)
    verita_fot.append({"indice": i, "soggetti": [{"id": "s1", "x": round(x, 4), "z": SOGGETTO["z"],
                                                    "visibile": frazione > 0, "frazione_visibile": round(frazione, 4)}]})

meta = {"larghezza": L, "altezza": A, "fx": FX, "fy": FY, "cx": CX, "cy": CY, "fps": FPS,
        "sensore": "esempio ideale del formato (non è un modello di sensore)",
        "posa": {"altezza_m": H, "inclinazione_gradi": INCL},
        "origine": "f10-dati/03-infrastruttura/crea_esempio_sequenza.py", "licenza": "nessun vincolo (dati generati)"}
m = OSTACOLO["larghezza"] / 2
verita = {"fotogrammi": verita_fot,
          "ostacoli": [{"id": "o1", "tipo": "poligono", "altezza_m": OSTACOLO["altezza"],
                        "vertici": [[-m, 1.49], [m, 1.49], [m, 1.51], [-m, 1.51]]}]}

if len(sys.argv) != 2:
    print(__doc__, file=sys.stderr)
    sys.exit(2)
scrivi_sequenza(sys.argv[1], meta, tempi, fotogrammi, verita)
print(f"scritta {sys.argv[1]}: {N} fotogrammi {L}x{A}; soggetto nascosto in "
      f"{sum(not f['soggetti'][0]['visibile'] for f in verita_fot)} fotogrammi")
