#!/usr/bin/env python3
"""Arbitro f8-f5: riconteggio della cifra portante sulla precisione (semi riparati, 15-statistica/ris/semi_*.tsv).
Rifare: PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 riconta_semi.py > riconta_semi.txt"""
import glob, os, math, re
F8 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERC = ["prosegue", "rallenta", "sosta", "torna", "sostalunga"]
FUORI = ["svolta", "lontano"]
def wilson(k, n, z=1.959964):
    if n == 0: return (float('nan'),) * 2
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d
def somma(geo, pred):
    acc = {}; vuoti = npass = 0; nfile = 0
    for p in sorted(glob.glob(f"{F8}/15-statistica/ris/semi_{geo}_*x400.tsv")):
        nfile += 1
        for r in open(p, encoding="utf-8"):
            c = r.rstrip("\n").split("\t")
            if c[0] == "H" and c[3] == pred:
                kv = dict(x.split("=", 1) for x in c[5:] if "=" in x)
                a = acc.setdefault((c[2], float(c[4])), [0, 0, 0, 0, 0.0, 0.0])
                a[0] += int(kv["in90"]); a[1] += int(kv["n"]); a[2] += int(kv["fuori_griglia"]); a[3] += int(kv["in100"])
                a[4] += float(kv["area90"]) * int(kv["n"]); a[5] += float(kv["ombra"]) * int(kv["n"])
            if c[0] == "P" and c[3] == pred:
                kv = dict(x.split("=", 1) for x in c[4:] if "=" in x and not x.startswith("pass="))
                vuoti += int(kv["pass_vuoto"]); npass += int(kv["npass"])
    return acc, vuoti, npass, nfile
for pred in ("sd-1", "sd-0"):
    print("=" * 90); print(pred)
    for den in ("tutti", "griglia"):
        celle2 = ok2 = celle3 = ok3_85 = ok3_90 = 0; peggio_inf = 1.0; peggio = None; nonris = []
        for geo in "DTL":
            acc, vuoti, npass, nfile = somma(geo, pred)
            for b in PERC:
                for tau in (0.5, 1.0, 2.0, 3.0):
                    k, n, fg, i100, _, _ = acc[(b, tau)]
                    nn = n - fg if den == "griglia" else n
                    lo, hi = wilson(k, nn)
                    if tau <= 2.0:
                        celle2 += 1; ok2 += lo > 0.90
                        if lo < peggio_inf: peggio_inf = lo; peggio = (geo, b, tau, k, nn, round(k / nn, 3), round(lo, 3))
                    celle3 += 1; ok3_85 += lo > 0.85
                    if tau == 3.0:
                        ok3_90 += lo > 0.90
                        if not lo > 0.90: nonris.append((geo, b, k, nn, round(k / nn, 3), round(lo, 3), round(hi, 3)))
        print(f"  denominatore «{den}»: fino a 2 s, celle con il limite inferiore di Wilson > 0,90: {ok2} su {celle2}; peggior limite inferiore {peggio}")
        print(f"     fino a 3 s, celle con il limite inferiore > 0,85: {ok3_85} su {celle3}; a 3 s, celle con il limite inferiore > 0,90: {ok3_90} su 15; le altre: {nonris}")
    for geo in "DTL":
        acc, vuoti, npass, nfile = somma(geo, pred)
        fuori100 = sum(a[1] - a[3] for a in acc.values()); camp = sum(a[1] for a in acc.values())
        print(f"  {geo}: file {nfile}; passaggi con un vuoto {vuoti} su {npass}; campioni H {camp}, fuori da R100 {fuori100}")
        for b in PERC + FUORI:
            print(f"     {b:11s} " + "  ".join(f"{t:g}s {acc[(b,t)][0]}/{acc[(b,t)][1]}={acc[(b,t)][0]/acc[(b,t)][1]:.3f}" for t in (1.0, 2.0, 3.0, 5.0)))
        print("     area R90/ombra (media pesata, «prosegue»): " + "  ".join(f"{t:g}s {acc[('prosegue',t)][4]/acc[('prosegue',t)][5]:.2f}" for t in (1.0, 2.0, 3.0, 5.0)))
