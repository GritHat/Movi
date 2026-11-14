#!/usr/bin/env python3
"""Quanto può dire il tabellone dal vivo (sciame-visualizzatore, f8). Conto binomiale esatto, nessun seme.
Rifare: timeout 120 python3 tabellone.py
"""
from math import comb


def pmf(k, n, p):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


def cdf(k, n, p):
    return sum(pmf(i, n, p) for i in range(0, k + 1))


def cp(k, n, alpha=0.05):
    """Intervallo esatto di Clopper-Pearson per bisezione."""
    def solve(f, lo, hi):
        for _ in range(60):
            mid = (lo + hi) / 2
            if f(mid):
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    low = 0.0 if k == 0 else solve(lambda p: 1 - cdf(k - 1, n, p) < alpha / 2, 0.0, 1.0)
    high = 1.0 if k == n else solve(lambda p: cdf(k, n, p) > alpha / 2, 0.0, 1.0)
    return low, high


print("PV-2a. Intervallo esatto al 95 % per k dentro su n (livello dichiarato 90 %)")
for n, k in ((10, 9), (10, 10), (20, 18), (30, 27), (60, 54), (100, 90), (200, 180), (400, 360)):
    lo, hi = cp(k, n)
    print("  %3d su %3d: %.1f %% - %.1f %%  (largo %.1f punti)%s"
          % (k, n, 100 * lo, 100 * hi, 100 * (hi - lo), "   <- contiene anche l'80 %" if lo <= 0.80 else ""))

print("\nPV-2b. Probabilità di vedere almeno 9 su 10 dentro, per copertura vera")
for p in (0.95, 0.90, 0.80, 0.70, 0.60, 0.50):
    print("  copertura vera %.2f: %.1f %%" % (p, 100 * (1 - cdf(8, 10, p))))

print("\nPV-2c. Minimo n con una soglia c tale che P(k >= c | 0,90) >= 0,90 e P(k >= c | p1) <= 0,10")
for p1 in (0.80, 0.70):
    found = None
    for n in range(5, 400):
        for c in range(0, n + 1):
            if 1 - cdf(c - 1, n, 0.90) >= 0.90 and (1 - cdf(c - 1, n, p1)) <= 0.10:
                found = (n, c)
                break
        if found:
            break
    print("  contro copertura vera %.2f: n = %d, soglia %d dentro" % (p1, found[0], found[1]))

print("\n[dopo] Regione troppo larga: anche una regione al «90 %» che copre il 99 % va segnalata.")
for n in (10, 30, 60, 100):
    print("  n = %3d: P(tutti dentro | copertura vera 0,90) = %.1f %%; P(tutti dentro | 0,99) = %.1f %%"
          % (n, 100 * 0.9 ** n, 100 * 0.99 ** n))
