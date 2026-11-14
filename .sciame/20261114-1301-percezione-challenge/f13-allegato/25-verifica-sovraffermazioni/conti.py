#!/usr/bin/env python3
"""Riconto degli intervalli di Wilson al 95 % delle frequenze toccate dalle correzioni, e dei due conti in forma chiusa."""
from math import sqrt
def wilson(k, n, z=1.959964):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return max(0, c-h), min(1, c+h)
for nome, k, n in [("identità 424 px", 176, 180), ("identità 848 px", 174, 180), ("estraneo", 19, 20),
                   ("pannello mobile, partenza", 79, 90), ("pannello mobile fuori dominio", 7, 10),
                   ("avviso acceso dopo rimozione", 10, 10), ("copertura pannello 1 m a 1 s", 942, 1045),
                   ("vuoti su camminatori distinti", 0, 6000), ("secondo soggetto, ideale", 2400, 2400),
                   ("secondo soggetto a", 3027, 3041), ("secondo soggetto b", 3493, 3616), ("secondo soggetto c", 3239, 3546),
                   ("posa +0,5°", 6, 10), ("bambino", 2, 10), ("premessa mancante", 24, 23402)]:
    a, b = wilson(k, n); print(f"{nome:36s} {k:>6d}/{n:<6d} = {k/n:.4f}  Wilson 95 % [{a:.4f}; {b:.4f}]")
print("fascia: 0,40/0,355 =", round(0.40/0.355, 3), " (0,40-0,20)/0,355 =", round(0.20/0.355, 3))
print("latenza: 16,7+95+22+21,3 =", 16.7+95+22+21.3, " con 71 ms:", 16.7+71+22+21.3)
print("avviso: (3-0,95)/(0,267+0,155+1,0) =", round((3-0.95)/(0.267+0.155+1.0), 3))
