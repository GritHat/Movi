#!/usr/bin/env python3
# confronti.py — sciame-statistico, f12. (1) D puntiforme contro esteso sugli stessi 400 semi; (2) denominatori di «tutti i lanci»;
# (3) numerosita' dal vivo per il tabellone «dentro k su n» (binomiale esatta).
import sys, os, glob, math
from math import comb
def wil(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c - h) / d, (c + h) / d
R = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.txt'))):
    for riga in open(f, encoding='utf-8', errors='replace'):
        if riga.startswith('R '):
            d = dict(t.split('=', 1) for t in riga.split()[1:] if '=' in t); d['file'] = os.path.basename(f)[:-4]; R.append(d)
I = lambda d, k: int(d[k])
print('(1) secondaria (tutti gli istanti a corpo nascosto, R90 grezza), cinque comportamenti insieme, 400 semi l\'uno, c7=1')
for g in 'DTL':
    for pd in ('0.9', '0.7'):
        for corpo in ('punto', 'esteso'):
            rr = [r for r in R if r['file'] == f'a_{g}_pd{pd}_{corpo}_c71']; out = []
            for s in '123':
                k = sum(I(r, 'inT' + s) for r in rr); n = sum(I(r, 'nT' + s) for r in rr); out.append(f'{k}/{n}={k/n:.3f} [{wil(k,n)[0]:.3f}-{wil(k,n)[1]:.3f}]')
            pegg = min((wil(I(r, 'inT2'), I(r, 'nT2'))[0], r['beh'], I(r, 'inT2'), I(r, 'nT2')) for r in rr)
            print(f'   {g} pd={pd} {corpo:6s}: 1 s {out[0]}; 2 s {out[1]}; 3 s {out[2]}; cella peggiore a 2 s {pegg[1]} {pegg[2]}/{pegg[3]} W {pegg[0]:.3f}')
print('(2) denominatori')
tutti = R; ne = [r for r in R if r['estr'] == '0']; nt = [r for r in ne if r['toglie'] == '0']
print('   tutti i lanci: validi', sum(I(r, 'validi') for r in tutti), '; validi+nonconf', sum(I(r, 'validi') + I(r, 'nonconf') for r in tutti), '; semi lanciati', sum(I(r, 'n') for r in tutti))
print('   senza estraneo: validi', sum(I(r, 'validi') for r in ne), '; senza estraneo e senza «toglie»: istanti nascosti', sum(I(r, 'hid_all') for r in nt), 'fuori R100', sum(I(r, 'f100c') for r in nt))
tr = {}
for r in R:
    tr.setdefault((r['geo'], r['beh']), 0); tr[(r['geo'], r['beh'])] = max(tr[(r['geo'], r['beh'])], I(r, 'n'))
print('   camminatori distinti (seme, comportamento, geometria) in tutti i lanci, al piu\':', sum(tr.values()), '; nei lanci (a):', 3 * 5 * 400)
for n in (6000,):
    print(f'   0 vuoti: limite superiore di Wilson al 95 % su 23402 = {wil(0,23402)[1]:.5f}; su {n} camminatori distinti = {wil(0,n)[1]:.5f}')
print('(3) tabellone «dentro k su n»: prova esatta a una coda, livello 0,05')
def coda_sup(n, c, p): return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(c, n + 1))
def soglia(n, p0, alfa=0.05):  # minimo c con P(X>=c | p0) <= alfa: «dentro almeno c su n» smentisce p <= p0
    for c in range(n + 1):
        if coda_sup(n, c, p0) <= alfa: return c
    return None
for p0, p1 in ((0.80, 0.90), (0.85, 0.90), (0.80, 0.95), (0.85, 0.95), (0.80, 0.97), (0.85, 0.97)):
    for pot in (0.80, 0.90):
        for n in range(5, 2000):
            c = soglia(n, p0)
            if c is not None and coda_sup(n, c, p1) >= pot:
                # stabilita': la potenza resta sopra anche per n+1..n+5 (la binomiale oscilla)
                if all(coda_sup(m, soglia(m, p0), p1) >= pot for m in range(n, n + 6)):
                    print(f'   escludere {p0:.2f} se il vero e\' {p1:.2f}, potenza {pot:.2f}: n = {n}, regola «dentro almeno {c} su {n}»'); break
print('   che cosa dice un tabellone di n prove (limite inferiore di Wilson al 95 % a due code):')
for n in (20, 30, 40, 60, 80, 100, 120, 150):
    out = []
    for q in (1.0, 0.95, 0.90):
        k = round(q * n); out.append(f'{k}/{n}: {wil(k,n)[0]:.3f}')
    kmin90 = next((k for k in range(n + 1) if wil(k, n)[0] >= 0.90), None); kmin85 = next((k for k in range(n + 1) if wil(k, n)[0] >= 0.85), None); kmin80 = next((k for k in range(n + 1) if wil(k, n)[0] >= 0.80), None)
    print(f'   n={n}: ' + '; '.join(out) + f' | minimo k per un limite >= 0,80: {kmin80}; >= 0,85: {kmin85}; >= 0,90: {kmin90}')
