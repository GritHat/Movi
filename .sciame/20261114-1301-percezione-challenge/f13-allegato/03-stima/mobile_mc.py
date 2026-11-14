"""Monte Carlo della regola «mobile» (finestra crescente fino a 1 s, medie di 3 fotogrammi, soglia a 5 scarti tipo).

Riscritto da zero dalla descrizione della regola; non importa nessun modulo del progetto.
Uso: python -I -B mobile_mc.py [N]
"""
import math
import sys

import numpy as np

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
HZ = 15
DT = 1.0 / HZ
NF = 18
K = 5.0


def sigma_z(d, curva):
    if curva == "nom":
        return d * d * 0.08 / (424.0 * 0.05)
    if curva == "pes":
        return 0.04 * (d / 2.0) ** 2
    return 0.05 * (d / 2.0) ** 2


def sigma_t(d):
    return d * math.radians(1.0) / math.sqrt(12.0)


def wilson(k, n, z=1.959964):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def prova(rng, curva, d0, radiale, v, n, fattore=math.sqrt(2.0 / 3.0), credito=1.0):
    """Restituisce, per ogni traccia, il primo fotogramma k con l'etichetta (NF se mai)."""
    t = np.arange(NF) * DT
    if radiale:
        vx, vz = np.zeros(NF), d0 - v * t
    else:
        vx, vz = v * t, np.full(NF, d0)
    r = np.hypot(vx, vz)
    mx = vx + rng.normal(0, 1, (n, NF)) * sigma_t(r)
    mz = vz + rng.normal(0, 1, (n, NF)) * sigma_z(r, curva)
    dist = np.hypot(mx, mz)
    primo = np.full(n, NF)
    # medie di tre fotogrammi consecutivi, che finiscono in k
    Mx = (mx[:, 2:] + mx[:, 1:-1] + mx[:, :-2]) / 3.0          # indice k-2
    Mz = (mz[:, 2:] + mz[:, 1:-1] + mz[:, :-2]) / 3.0
    Md = np.maximum(np.maximum(dist[:, 2:], dist[:, 1:-1]), dist[:, :-2])
    for k in range(5, NF):
        j = max(2, k - HZ)                                     # finestra che cresce fino a 15 passi, medie disgiunte
        zf = np.maximum(Md[:, k - 2], Md[:, j - 2])
        su = (np.abs(Mz[:, k - 2] - Mz[:, j - 2]) > K * sigma_z(zf, curva) * credito * fattore) | \
             (np.abs(Mx[:, k - 2] - Mx[:, j - 2]) > K * sigma_t(zf) * credito * fattore)
        primo = np.where((primo == NF) & su, k, primo)
    return primo


def main():
    rng = np.random.default_rng(13032026)
    print("# regola «mobile», N = %d per cella; soglia 5*sigma*sqrt(2/3); quota con la prima etichetta entro 1 s (k <= 15)" % N)
    for curva in ("nom", "pes", "sev"):
        for d0 in (2.0, 3.0):
            riga = []
            for nome, radiale, v in (("di traverso", False, 0.5), ("avvicinamento", True, 0.5), ("fermo", True, 0.0)):
                p = prova(rng, curva, d0, radiale, v, N)
                k = int((p <= 15).sum())
                lo, hi = wilson(k, N)
                riga.append("%s %.2f %% [%.2f; %.2f]" % (nome, 100 * k / N, 100 * lo, 100 * hi))
            print(" %s da %.0f m: %s" % (curva, d0, " ; ".join(riga)))
    print("# stessa regola con la soglia letterale 5*sigma*sqrt(2) (senza il fattore 1/sqrt(3) della media)")
    for curva in ("nom", "pes", "sev"):
        for d0 in (2.0, 3.0):
            p = prova(rng, curva, d0, True, 0.5, N, fattore=math.sqrt(2.0))
            print(" %s da %.0f m, avvicinamento: %.2f %%" % (curva, d0, 100 * (p <= 15).mean()))
    print("# velocita' in avvicinamento da 2 m e da 3 m, curva pessimista: quota vista entro 1 s")
    for d0 in (2.0, 3.0):
        print(" da %.0f m: " % d0 + " ; ".join("%.1f m/s %.1f %%" % (v, 100 * (prova(rng, "pes", d0, True, v, N) <= 15).mean())
                                              for v in (0.1, 0.2, 0.3, 0.5, 0.8, 1.2)))
    print("# rumore creduto la meta' del vero (soglia dimezzata), fermo a 2 m, curva pessimista: tracce con un'etichetta falsa nel primo secondo")
    p = prova(rng, "pes", 2.0, True, 0.0, N, credito=0.5)
    print(" %.2f %%" % (100 * (p <= 15).mean()))


main()
