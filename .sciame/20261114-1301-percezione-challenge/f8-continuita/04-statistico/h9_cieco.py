#!/usr/bin/env python3
"""Il criterio a due stadi di H9 (>= 28 su 30 regge; <= 22 smentita; 23-27: altri 30 e >= 52 su 60) con la composizione
prescritta 21 prosegue / 5 sosta / 4 torna: probabilita' esatta di «regge» in funzione della copertura per classe."""
import math
from itertools import product

def pmf(n, p):
    return [math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]

def conv(a, b):
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out

def passa(cp, cs, ct):
    d = conv(conv(pmf(21, cp), pmf(5, cs)), pmf(4, ct))  # dentro, su 30
    p1 = sum(d[28:])
    p2 = 0.0
    for a in range(23, 28):
        p2 += d[a] * sum(d[b] for b in range(31) if a + b >= 52)
    return p1, p1 + p2, sum(d[:23])

print("copertura prosegue / sosta / torna -> P(regge al primo stadio), P(regge in tutto), P(smentita al primo stadio)")
for lab, c in (("nucleo con C6 (v2_C6.txt, demo): 1,00 / 1,00 / 0,50", (1.0, 1.0, 0.50)),
               ("torneo G1 a 2 s: 1,00 / 0,955 / 0,561", (1.0, 0.955, 0.561)),
               ("chi torna MAI coperto: 1,00 / 1,00 / 0,00", (1.0, 1.0, 0.0)),
               ("chi torna mai coperto, sosta 0,93: 1,00 / 0,93 / 0,00", (1.0, 0.93, 0.0)),
               ("tutti a 0,90 (taratura giusta al 90 %)", (0.9, 0.9, 0.9)),
               ("tutti a 0,80", (0.8, 0.8, 0.8))):
    print("  %-56s %.3f  %.3f  %.3f" % ((lab,) + passa(*c)))
