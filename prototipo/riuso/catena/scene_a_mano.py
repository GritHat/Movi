"""Scene minime per le prove: matrici di profondità scritte con le formule chiuse del formato comune
(03-infrastruttura/formato_sequenza.md), senza rumore. Non è un simulatore di sensore.

Suolo piano:                      Z = h / (yn·cos t + sin t)          con yn = (v - cy) / fy
Pannello verticale di fronte,     Z = z0 / (cos t - yn·sin t)         (il piano z = z0 nel riferimento del suolo),
largo da x0 a x1, alto `alto`:    colpito dove x = xn·Z sta fra x0 e x1 e la quota h - Z·(yn·cos t + sin t) fra 0 e alto.
Ogni pixel prende la superficie più vicina."""
import math

import numpy as np

META = {"larghezza": 848, "altezza": 480, "fx": 424.0, "fy": 424.0, "cx": 423.5, "cy": 239.5, "fps": 15.0,
        "sensore": "scena a mano (ideale, senza rumore)",
        "posa": {"altezza_m": 1.2, "inclinazione_gradi": 15.0},
        "origine": "f10-dati/10-catena/scene_a_mano.py", "licenza": "nessun vincolo (dati generati)"}


class Scena:
    def __init__(self, meta=META):
        self.meta = meta
        self.h, t = meta["posa"]["altezza_m"], math.radians(meta["posa"]["inclinazione_gradi"])
        u = (np.arange(meta["larghezza"]) - meta["cx"]) / meta["fx"]
        v = (np.arange(meta["altezza"]) - meta["cy"]) / meta["fy"]
        self.xn, yn = np.meshgrid(u, v)
        self.den_suolo = yn * math.cos(t) + math.sin(t)
        self.den_fronte = math.cos(t) - yn * math.sin(t)
        with np.errstate(divide="ignore"):
            self.suolo = np.where(self.den_suolo > 1e-9, self.h / self.den_suolo, np.inf)

    def fotogramma(self, pannelli=(), buco=None, suolo=True):
        """pannelli: lista di (x0, x1, z0, alto) in metri. buco: (azimut0, azimut1, distanza0, distanza1), in gradi e
        metri sul suolo: i pixel di suolo che cadono lì escono a 0. suolo=False: niente pavimento (tutto 0)."""
        z = self.suolo.copy() if suolo else np.full(self.suolo.shape, np.inf)
        if buco is not None:
            gx, gz = self.xn * z, z * self.den_fronte
            az, d = np.degrees(np.arctan2(gx, gz)), np.hypot(gx, gz)
            z[(az >= buco[0]) & (az <= buco[1]) & (d >= buco[2]) & (d <= buco[3])] = np.inf
        for x0, x1, z0, alto in pannelli:
            zp = z0 / self.den_fronte
            x, quota = self.xn * zp, self.h - zp * self.den_suolo
            colpito = (x >= x0) & (x <= x1) & (quota >= 0) & (quota <= alto) & (zp < z)
            z[colpito] = zp[colpito]
        mm = np.where(np.isfinite(z) & (z < 65.535), np.round(z * 1000.0), 0)
        return mm.astype(np.uint16)


def tempi(n, fps=15.0):
    return [k / fps for k in range(n)]
