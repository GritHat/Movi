"""Cose comuni ai programmi di misura di 20-validazione: percorsi, importazione della catena (sola lettura),
predittore che registra lo stato d'ingresso, lettura della verità del simulatore, intervalli."""
import json
import math
import os
import sys

for _n in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_n, "1")
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
F10 = os.path.dirname(QUI)
CATENA = os.path.join(F10, "10-catena")
SIM = os.path.join(F10, "11-simulatore")
SEQ_SIM = os.path.join(SIM, "sequenze")
SEQ_VERE = os.path.join(F10, "12-dati-veri", "sequenze")
TRACCE = os.path.join(F10, "12-dati-veri", "tracce")
USCITE = os.path.join(QUI, "uscite")
sys.path.insert(0, CATENA)

import numpy as np                                             # noqa: E402

from catena import esegui                                      # noqa: E402
from mappa import InvarianteViolato                            # noqa: E402
from parametri import IN_OMBRA, LIBERO, NON_OSSERVATO, OCCUPATO, Parametri   # noqa: E402
from presenza import PredittoreVelocitaCostante                # noqa: E402
from sorgente import SorgenteCartella, SorgenteMemoria         # noqa: E402

INGRESSI = []          # riempito dal predittore che registra; chi corre lo svuota a ogni sequenza


class PredittoreCheRegistra(PredittoreVelocitaCostante):
    """Il predittore del nucleo, identico; in più annota lo stato d'ingresso (serve alle linee di base)."""

    def __init__(self, ingresso, par):
        super().__init__(ingresso, par)
        INGRESSI.append({"id": int(ingresso.id_traccia), "t": float(ingresso.t),
                         "x": [float(v) for v in ingresso.x], "p": [[float(v) for v in r] for r in ingresso.p],
                         "ultima_misura": [float(v) for v in ingresso.ultima_misura],
                         "larghezza_m": float(ingresso.larghezza_m), "celle_nucleo": int(ingresso.nucleo.sum())})


def corri(sorgente, uscita, par=None, posa=None, griglie=True):
    """Passa la sorgente nella catena. Restituisce (riassunto o None, errore o None, ingressi)."""
    INGRESSI.clear()
    try:
        r = esegui(sorgente, uscita, par or Parametri(), posa, griglie, fabbrica_predittore=PredittoreCheRegistra)
        err = None
    except InvarianteViolato as e:
        r, err = None, f"INVARIANTE: {e}"
    except Exception as e:                                     # la catena che fallisce è un risultato
        r, err = None, f"{type(e).__name__}: {e}"
    ing = list(INGRESSI)
    if uscita is not None:
        os.makedirs(uscita, exist_ok=True)
        with open(os.path.join(uscita, "ingressi.json"), "w", encoding="utf-8") as f:
            json.dump({"ingressi": ing, "errore": err}, f)
    return r, err, ing


def leggi_righe(uscita):
    with open(os.path.join(uscita, "fotogrammi.jsonl"), encoding="utf-8") as f:
        return [json.loads(r) for r in f if r.strip()]


def leggi_griglie(uscita):
    return np.load(os.path.join(uscita, "griglie.npz"), allow_pickle=False)


def leggi_verita(cartella):
    with open(os.path.join(cartella, "verita.json"), encoding="utf-8") as f:
        return json.load(f)


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def quota(k, n):
    a, b = wilson(k, n)
    return f"{k} su {n} ({100 * k / n:.1f} %; IC 95 % {100 * a:.1f}–{100 * b:.1f})" if n else "0 su 0"


def classi_polari(verita, na=180, nr=30, sotto=5):
    """Dalla maschera CARTESIANA della verità (2,5 cm) la classe di ogni cella polare della catena.

    Restituisce (centro, tutta_ombra, parte_ombra, moda): `centro` è la classe del campione più vicino al centro
    della cella; `tutta_ombra` vero se tutti i sotto-campioni della cella (sotto × sotto) cadono in classe 1 o 3;
    `parte_ombra` se almeno uno. Via diversa dalla maschera polare della verità (che ha la stessa origine)."""
    c = verita["ombra_suolo"]["cartesiana"]
    m = np.array([[int(ch) for ch in riga] for riga in c["celle"]], dtype=np.uint8)      # [z, x]
    x0, z0, passo = c["x_m_centro_prima"], c["z_m_centro_prima"], c["passo_m"]
    fa = (np.arange(sotto) + 0.5) / sotto
    az = np.radians(-90.0 + (np.arange(na)[:, None, None, None] + fa[None, None, :, None]) * 1.0)
    rr = (np.arange(nr)[None, :, None, None] + fa[None, None, None, :]) * 0.1
    x, z = np.sin(az) * rr, np.cos(az) * rr
    ix = np.rint((x - x0) / passo).astype(int)
    iz = np.rint((z - z0) / passo).astype(int)
    dentro = (ix >= 0) & (ix < m.shape[1]) & (iz >= 0) & (iz < m.shape[0])
    cl = np.where(dentro, m[np.clip(iz, 0, m.shape[0] - 1), np.clip(ix, 0, m.shape[1] - 1)], 2)
    cl = cl.reshape(na, nr, sotto * sotto)
    ombra = (cl == 1) | (cl == 3)
    centro = cl[:, :, (sotto * sotto) // 2]
    return centro, ombra.all(axis=2), ombra.any(axis=2), cl


def cella(x, z, na=180, nr=30):
    ia = math.floor(math.degrees(math.atan2(x, z)) + 90.0)
    ir = math.floor(math.hypot(x, z) / 0.1)
    return (ia, ir) if 0 <= ia < na and 0 <= ir < nr else None
