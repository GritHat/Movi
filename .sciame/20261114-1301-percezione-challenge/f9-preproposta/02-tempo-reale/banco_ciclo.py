#!/usr/bin/env python3
"""Stesso lavoro di banco_ciclo.c parte (a), in Python puro (senza numpy): ritaglio sulla griglia e aggiornamento dei pesi
per 10 tracce x 2 ipotesi, piu' una stima della proiezione dell'immagine (un fotogramma su 1/16 dei pixel, poi x16).

Rifare:  timeout 120 python3 banco_ciclo.py > risultati_banco_py.txt
"""
import math
import random
import time

NA, NR, NT = 88, 30, 10
rnd = random.Random(12345)

CX = [[0.0] * NR for _ in range(NA)]
CZ = [[0.0] * NR for _ in range(NA)]
AR = [[0.0] * NR for _ in range(NA)]
ST = [[0] * NR for _ in range(NA)]   # 0 libero, 2 ombra, 3 non osservato
for i in range(NA):
    for j in range(NR):
        a = math.radians(-44 + i + 0.5)
        r = (j + 0.5) * 0.1
        CX[i][j] = r * math.sin(a); CZ[i][j] = r * math.cos(a); AR[i][j] = r * 0.1 * math.radians(1)
        ST[i][j] = 2 if (26 <= i <= 73 and r > 1.2) else (3 if r < 1.24 else 0)


def ritaglio(x, z, sxx, sxz, szz, riquadro):
    det = sxx * szz - sxz * sxz
    ixx, ixz, izz = szz / det, -sxz / det, sxx / det
    a0, a1, r0, r1 = 0, NA, 0, NR
    if riquadro:
        s = 3 * math.sqrt(max(sxx, szz)); r = math.hypot(x, z); a = math.degrees(math.atan2(x, z))
        da = math.degrees(math.asin(s / r)) if r > s else 90.0
        a0 = max(0, int(math.floor(a - da + 44))); a1 = min(NA, int(math.ceil(a + da + 44)))
        r0 = max(0, int(math.floor((r - s) * 10))); r1 = min(NR, int(math.ceil((r + s) * 10)))
    tot = omb = 0.0
    exp = math.exp
    for i in range(a0, a1):
        cx, cz, ar, st = CX[i], CZ[i], AR[i], ST[i]
        for j in range(r0, r1):
            dx = cx[j] - x; dz = cz[j] - z
            w = exp(-0.5 * (dx * dx * ixx + 2 * dx * dz * ixz + dz * dz * izz)) * ar[j]
            tot += w
            if st[j]:
                omb += w
    return omb / tot if tot > 0 else 0.0


def ciclo(tr, riquadro):
    for T in tr:
        f = [ritaglio(h[0], h[1], h[2], h[3], h[4], riquadro) for h in T["h"]]
        s = T["mu"][0] * f[0] + T["mu"][1] * f[1]
        if s > 1e-9:
            T["mu"][0] = min(0.999, max(0.001, T["mu"][0] * f[0] / s)); T["mu"][1] = 1 - T["mu"][0]


def tracce(sig):
    return [{"h": [[rnd.uniform(-1, 1), rnd.uniform(1.5, 2.7), sig * sig, 0.2 * sig * sig, sig * sig] for _ in range(2)], "mu": [0.8, 0.2]} for _ in range(NT)]


def stat(nome, v):
    v = sorted(v)
    print(f"{nome:<58} mediana {v[len(v)//2]:8.2f} ms   massimo {v[-1]:8.2f} ms   (n = {len(v)})")


if __name__ == "__main__":
    print(f"# Banco del ciclo, Python {__import__('sys').version.split()[0]} puro, un filo. Griglia {NA*NR} celle; {NT} tracce x 2 ipotesi.")
    for riq in (False, True):
        for sig in (0.8, 0.3):
            ts = []
            for it in range(15):
                tr = tracce(sig)
                a = time.perf_counter(); ciclo(tr, riq); ts.append((time.perf_counter() - a) * 1e3)
            stat(f"(a) ritaglio + pesi, {'riquadro a 3 sigma' if riq else 'griglia intera     '}, sigma {sig} m", ts)
    # (b) proiezione: 1/16 dei pixel (212 x 120), stesso conto per pixel; il fotogramma intero costa circa 16 volte
    W, H = 212, 120
    fx = W / (2 * math.tan(math.radians(43.5))); fy = H / (2 * math.tan(math.radians(29)))
    rx = [(u - W / 2 + 0.5) / fx for u in range(W)]; ry = [(v - H / 2 + 0.5) / fy for v in range(H)]
    st_, ct_ = math.sin(math.radians(15)), math.cos(math.radians(15))
    prof = [[(0.0 if rnd.random() < 0.05 else min(4.0, 1.2 / max(0.02, ry[v] * ct_ + st_))) for u in range(W)] for v in range(H)]
    ts = []
    for it in range(8):
        ns = [[0] * NR for _ in range(NA)]; no = [[0] * NR for _ in range(NA)]
        a = time.perf_counter()
        for v in range(H):
            ryv = ry[v]; row = prof[v]
            for u in range(W):
                d = row[u]
                if d == 0.0:
                    continue
                xc = rx[u] * d; yc = ryv * d
                zw = d * ct_ - yc * st_; quota = 1.2 - (yc * ct_ + d * st_)
                i = int(math.degrees(math.atan2(xc, zw)) + 44); j = int(math.hypot(xc, zw) * 10)
                if 0 <= i < NA and 0 <= j < NR:
                    if 0.07 < quota < 2.0:
                        no[i][j] += 1
                    elif abs(quota) <= 0.07:
                        ns[i][j] += 1
        ts.append((time.perf_counter() - a) * 1e3)
    stat("(b) proiezione su 212x120 pixel (1/16 del fotogramma)", ts)
    print(f"    stima per 848x480 in Python puro: circa {sorted(ts)[len(ts)//2]*16:.0f} ms (x16; con numpy: non verificato, numpy non e' installato)")
