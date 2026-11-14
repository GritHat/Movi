#!/usr/bin/env python3
"""Che cosa succede allo strato «possibile presenza» se la griglia cambia risoluzione.

Griglia fine: polare 1 grado x 0,1 m, 88 x 30 celle (campo 88 gradi, 0-3 m).
Strato 1: cuneo d'ombra di un pannello largo 1 m a 1,15 m, dilatato di 0,40 m (SOLUZIONE_V2, B5).
Tre modi di passare alla griglia grossa (fattore f) e tornare:
  - «al centro»: la cella grossa prende lo stato di UNA figlia (come a[::f, ::f]);
  - «a maggioranza»: presenza se lo sono piu' di meta' delle figlie;
  - «conservativo»: presenza se lo e' ALMENO una figlia.
Il ritorno alla griglia fine replica la cella grossa sulle figlie.

Rifare:  timeout 120 python3 sim_griglia.py > risultati_griglia.txt
"""
import math

NA, NR = 88, 30
DA, DR = 1.0, 0.1
A0 = -44.0


def centro(i, j):
    a = math.radians(A0 + (i + 0.5) * DA)
    r = (j + 0.5) * DR
    return r * math.sin(a), r * math.cos(a), r


def area(j):
    return (j + 0.5) * DR * DR * math.radians(DA)


def dist_seg(px, pz, ax, az, bx, bz):
    vx, vz = bx - ax, bz - az
    t = ((px - ax) * vx + (pz - az) * vz) / (vx * vx + vz * vz)
    t = max(0.0, min(1.0, t))
    return math.hypot(px - ax - t * vx, pz - az - t * vz)


def strato1(x0, x1, zp, fascia=0.40, portata=3.0):
    """Cuneo d'ombra del pannello [x0,x1] a distanza zp, dilatato di `fascia` (distanza dal cuneo)."""
    a0, a1 = math.atan2(x0, zp), math.atan2(x1, zp)
    m = [[False] * NR for _ in range(NA)]
    # bordi del cuneo: i due raggi dai bordi del pannello fino alla portata, e il pannello
    e0 = (x0, zp, portata * math.sin(a0), portata * math.cos(a0))
    e1 = (x1, zp, portata * math.sin(a1), portata * math.cos(a1))
    for i in range(NA):
        for j in range(NR):
            x, z, r = centro(i, j)
            a = math.atan2(x, z)
            dentro = a0 <= a <= a1 and z >= zp and r <= portata
            if dentro:
                m[i][j] = True
                continue
            d = min(dist_seg(x, z, *e0), dist_seg(x, z, *e1), dist_seg(x, z, x0, zp, x1, zp))
            if d <= fascia and r <= portata:
                m[i][j] = True
    return m


def giu(m, f, modo, oi=0, oj=0):
    """Fine -> grossa (fattore f, origine spostata di oi, oj celle fini)."""
    na = (NA + oi + f - 1) // f
    nr = (NR + oj + f - 1) // f
    g = [[False] * nr for _ in range(na)]
    for I in range(na):
        for J in range(nr):
            figlie = []
            for di in range(f):
                for dj in range(f):
                    i, j = I * f + di - oi, J * f + dj - oj
                    if 0 <= i < NA and 0 <= j < NR:
                        figlie.append(m[i][j])
            if not figlie:
                continue
            if modo == "centro":
                i, j = I * f - oi, J * f - oj          # la figlia d'angolo, come a[::f, ::f]
                g[I][J] = m[i][j] if (0 <= i < NA and 0 <= j < NR) else figlie[0]
            elif modo == "maggioranza":
                g[I][J] = sum(figlie) * 2 > len(figlie)
            else:
                g[I][J] = any(figlie)
    return g


def su(g, f, oi=0, oj=0):
    m = [[False] * NR for _ in range(NA)]
    for i in range(NA):
        for j in range(NR):
            m[i][j] = g[(i + oi) // f][(j + oj) // f]
    return m


def conta(m):
    return sum(m[i][j] for i in range(NA) for j in range(NR)), sum(area(j) for i in range(NA) for j in range(NR) if m[i][j])


def confronta(a, b):
    """Celle e area di presenza in a che mancano in b (perse), e aggiunte."""
    pn = pa = an = aa = 0
    larg = 0.0
    for i in range(NA):
        for j in range(NR):
            if a[i][j] and not b[i][j]:
                pn += 1; pa += area(j)
            if b[i][j] and not a[i][j]:
                an += 1; aa += area(j)
    return pn, pa, an, aa


if __name__ == "__main__":
    # pannello largo 1 m a 1,15 m, non centrato (da -0,37 a +0,63 m), come nella geometria della demo
    base = strato1(-0.37, 0.63, 1.15)
    n0, ar0 = conta(base)
    print(f"# Strato 1 sulla griglia fine: {n0} celle, {ar0:.3f} m2 (pannello 1 m a 1,15 m, fascia 0,40 m)")
    print(f"{'fattore':>7} {'modo':<13}{'perse (celle)':>14}{'perse (m2)':>11}{'aggiunte (m2)':>14}{'area dopo/prima':>16}{'dopo 10 giri':>13}")
    for f in (2, 4):
        for modo in ("centro", "maggioranza", "conservativo"):
            m1 = su(giu(base, f, modo), f)
            pn, pa, an, aa = confronta(base, m1)
            m = m1
            for _ in range(9):
                m = su(giu(m, f, modo), f)
            print(f"{f:>7} {modo:<13}{pn:>14}{pa:>11.3f}{aa:>14.3f}{conta(m1)[1]/ar0:>16.3f}{conta(m)[1]/ar0:>13.3f}")
    # conservativo ma con l'origine della griglia grossa che cambia a ogni giro (griglia ricostruita non allineata)
    print("\n# Conservativo, fattore 2, origine della griglia grossa spostata di una cella fine a giri alterni")
    m = base
    for g in range(1, 11):
        o = g % 2
        m = su(giu(m, 2, "conservativo", o, o), 2, o, o)
        if g in (1, 2, 5, 10):
            print(f"giro {g:>2}: area/iniziale = {conta(m)[1]/ar0:.3f}; perse = {confronta(base, m)[0]}")
    # azzeramento alla riallocazione
    print("\n# Griglia riallocata e azzerata al cambio: celle di presenza perse =", n0, f"({ar0:.3f} m2, 100 %)")
