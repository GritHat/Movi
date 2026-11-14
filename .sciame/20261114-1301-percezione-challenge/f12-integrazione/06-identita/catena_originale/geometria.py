"""Dalla profondità ai punti sul piano del suolo.

Riferimento della camera: x a destra, y in basso, z lungo l'asse ottico. Riferimento del suolo (quello di
verita.json): origine sotto il centro ottico, x a destra, z in avanti, quota verso l'alto. Con la posa (h, t):
    x = Xc,   z = Zc cos t - Yc sin t,   quota = h - Yc cos t - Zc sin t        (formato_sequenza.md)
Qui la posa è tenuta come tre versori (destra, su, avanti) nel riferimento della camera più l'altezza, così la
posa nota e quella stimata dal piano del suolo (che può avere anche un rollio) usano lo stesso codice."""
import math
from dataclasses import dataclass

import numpy as np


@dataclass
class Posa:
    altezza_m: float
    destra: np.ndarray
    su: np.ndarray
    avanti: np.ndarray
    stimata: bool = False
    nota: str = ""

    @property
    def inclinazione_gradi(self):
        return math.degrees(math.atan2(-self.su[2], -self.su[1]))

    @property
    def rollio_gradi(self):
        return math.degrees(math.asin(max(-1.0, min(1.0, float(self.su[0])))))


def posa_da_normale(altezza, su, stimata=False, nota=""):
    """Costruisce la posa dal versore «su» (normale al suolo, verso la camera) scritto nel riferimento della camera."""
    su = np.asarray(su, dtype=np.float64)
    su = su / np.linalg.norm(su)
    asse = np.array([0.0, 0.0, 1.0])
    avanti = asse - su * float(asse @ su)            # proiezione orizzontale dell'asse ottico
    n = np.linalg.norm(avanti)
    if n < 1e-6:
        raise ValueError("la camera guarda lungo la verticale: «avanti» non è definito")
    avanti = avanti / n
    destra = np.cross(avanti, su)
    return Posa(float(altezza), destra, su, avanti, stimata, nota)


def posa_da_meta(meta):
    """La posa di meta.json (rollio nullo), oppure None se manca."""
    p = meta.get("posa")
    if p is None:
        return None
    t = math.radians(p["inclinazione_gradi"])
    return posa_da_normale(p["altezza_m"], [0.0, -math.cos(t), -math.sin(t)], nota="da meta.json")


def punti_camera(prof, meta):
    """Punti 3D (N, 3) in metri dei pixel validi (profondità > 0)."""
    v, u = np.nonzero(prof)
    z = prof[v, u].astype(np.float64) * 0.001
    return np.stack([(u - meta["cx"]) * z / meta["fx"], (v - meta["cy"]) * z / meta["fy"], z], axis=1)


def stima_suolo(fotogrammi, meta, seme=0, n_prove=400, tolleranza_m=0.03, max_punti=20000,
                inclinazione_max_gradi=60.0, altezza_min_m=0.2, altezza_max_m=3.0):
    """Stima robusta del piano del suolo quando la posa non è nota (RANSAC, poi minimi quadrati sui punti concordi).

    Sceglie il piano con più punti concordi fra quelli la cui normale sta entro `inclinazione_max_gradi` dal «su»
    della camera e che passano fra `altezza_min_m` e `altezza_max_m` sotto il centro ottico. Limite dichiarato: un
    grande piano orizzontale che non è il suolo (un tavolo) può vincere. Restituisce (posa, frazione_concorde)."""
    gen = np.random.default_rng(seme)
    p = np.concatenate([punti_camera(f, meta) for f in fotogrammi])
    if len(p) < 100:
        raise ValueError("troppo pochi punti validi per stimare il suolo")
    if len(p) > max_punti:
        p = p[gen.choice(len(p), max_punti, replace=False)]
    cos_max = math.cos(math.radians(inclinazione_max_gradi))
    migliore, n_migliore = None, 0
    for _ in range(n_prove):
        a, b, c = p[gen.choice(len(p), 3, replace=False)]
        n = np.cross(b - a, c - a)
        lung = np.linalg.norm(n)
        if lung < 1e-9:
            continue
        n = n / lung
        d = -float(n @ a)                              # piano: n·p + d = 0
        if d < 0:
            n, d = -n, -d                              # la normale guarda la camera: d = altezza
        if -n[1] < cos_max or not (altezza_min_m <= d <= altezza_max_m):
            continue
        concordi = np.abs(p @ n + d) <= tolleranza_m
        k = int(concordi.sum())
        if k > n_migliore:
            migliore, n_migliore = concordi, k
    if migliore is None:
        raise ValueError("nessun piano del suolo plausibile trovato")
    q = p[migliore]
    centro = q.mean(axis=0)
    n = np.linalg.svd(q - centro, full_matrices=False)[2][-1]     # direzione di minima varianza
    d = -float(n @ centro)
    if d < 0:
        n, d = -n, -d
    frazione = n_migliore / len(p)
    posa = posa_da_normale(d, n, stimata=True,
                           nota=f"stimata dal piano del suolo (RANSAC, {frazione:.0%} dei punti entro {tolleranza_m} m)")
    return posa, frazione


class Proiezione:
    """Coefficienti per pixel, calcolati una volta: con Z la profondità in metri,
        x = Z·ax,  z = Z·az,  distanza sul suolo = Z·ar,  quota = h - Z·aq,
    e l'azimut atan2(x, z) non dipende da Z: l'indice di azimut di ogni pixel è fisso."""

    def __init__(self, meta, posa, par):
        self.posa, self.h = posa, np.float32(posa.altezza_m)
        u = (np.arange(meta["larghezza"], dtype=np.float64) - meta["cx"]) / meta["fx"]
        v = (np.arange(meta["altezza"], dtype=np.float64) - meta["cy"]) / meta["fy"]
        xn, yn = np.meshgrid(u, v)
        raggi = np.stack([xn, yn, np.ones_like(xn)], axis=-1)
        ax, az, aq = raggi @ posa.destra, raggi @ posa.avanti, -(raggi @ posa.su)
        azimut = np.degrees(np.arctan2(ax, az))
        ia = np.floor((azimut + par.azimut_max_gradi) / par.passo_azimut_gradi).astype(np.int64)
        self.in_azimut = ((az > 0) & (ia >= 0) & (ia < par.n_azimut)).ravel()
        self.ia = np.clip(ia, 0, par.n_azimut - 1).ravel().astype(np.int32)
        self.ax, self.az = ax.ravel().astype(np.float32), az.ravel().astype(np.float32)
        self.aq, self.ar = aq.ravel().astype(np.float32), np.hypot(ax, az).ravel().astype(np.float32)
