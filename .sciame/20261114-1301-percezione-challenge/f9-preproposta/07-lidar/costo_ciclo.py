#!/usr/bin/env python3
"""Costo per ciclo, lato PC, del canale laterale: 3 sensori x 64 zone -> un avviso per sensore.
Comando: timeout 60 python3 -I costo_ciclo.py   (seme fisso; Python puro; tempi indicativi)"""
import random, time
random.seed(20261114)
N = 20000
quadri = [[(random.randint(20, 2500), random.choice((5, 5, 5, 9, 10, 255, 4)), random.randint(0, 400))
           for _ in range(64)] for _ in range(3)]

def ciclo(q, soglia_mm=500, amb_max=300):
    out = []
    for sens in q:
        vicino = 0; amb = 0
        for d, st, a in sens:
            amb += a
            if st in (5, 9) and d < soglia_mm:
                vicino += 1
        out.append(("non disponibile" if amb / 64 > amb_max else ("presenza" if vicino >= 2 else "nessun ritorno")))
    return out

t0 = time.perf_counter()
for _ in range(N):
    ciclo(quadri)
dt = (time.perf_counter() - t0) / N
print(f"{dt*1e6:.1f} microsecondi per ciclo (3 x 64 zone), N = {N}; a 15 Hz: {dt*15*100:.4f} % di un core")
