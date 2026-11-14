#!/usr/bin/env python3
# potenza.py — sciame-statistico, f12. Regole del tabellone «dentro k su n»: livello e potenza, binomiale esatta.
from math import comb, sqrt
def cs(n, c, p): return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(c, n + 1))
def wl(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n; return (p + z * z / (2 * n) - z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
def soglia(n, p0, a=0.05): return next(c for c in range(n + 2) if cs(n, c, p0) <= a)
print('A. regola «dentro almeno c su n» per escludere 0,80 (una coda, livello <= 0,05)')
for n in (30, 40, 60, 90, 94, 100, 120):
    c = soglia(n, 0.80); print(f'   n={n}: c={c}; P(passa) se il vero e\' 0,80: {cs(n,c,.8):.3f}; 0,85: {cs(n,c,.85):.2f}; 0,90: {cs(n,c,.9):.2f}; 0,95: {cs(n,c,.95):.2f}')
print('B. regola per escludere 0,85')
for n in (60, 100, 120, 296, 401):
    c = soglia(n, 0.85); print(f'   n={n}: c={c}; P(passa) se il vero e\' 0,85: {cs(n,c,.85):.3f}; 0,90: {cs(n,c,.9):.2f}; 0,95: {cs(n,c,.95):.2f}')
print('C. per scrivere «almeno 9 su 10» (limite inferiore di Wilson al 95 % >= 0,90)')
for n in (30, 40, 60, 80, 100, 120, 150):
    c = next((k for k in range(n + 1) if wl(k, n) >= 0.90), None)
    if c is None: print(f'   n={n}: impossibile anche con {n} su {n} (limite {wl(n,n):.3f})'); continue
    print(f'   n={n}: servono {c} su {n}; P(riuscirci) se il vero e\' 0,90: {cs(n,c,.9):.3f}; 0,95: {cs(n,c,.95):.2f}; 0,97: {cs(n,c,.97):.2f}; 0,99: {cs(n,c,.99):.2f}')
print('D. VD: regione che contiene la verita\' 83 passaggi su 90: limite di Wilson', round(wl(83, 90), 3), '; identita\' 41 su 45:', round(wl(41, 45), 3), '; V8 scoperti 130/1581 e 9/2800: quote', round(130/1581, 4), round(9/2800, 4))
