#!/usr/bin/env python3
"""Riassunto compatto dei file ris/*.txt del torneo. Uso: python3 riassunto.py ris/base_T.txt [colonna=c90|c50|area|noreg]"""
import sys, math
CN = ['C004', 'C001', 'C005W', 'C005P', 'ESTA', 'ESTB']
def leggi(p):
    d = {}; sez = 0
    for r in open(p):
        if r.startswith('## '): sez = int(r[3:].split('.')[0]); continue
        if sez != 1 or '|' not in r or r.startswith('comport'): continue
        parti = r.split('|'); a = parti[0].split(); beh, tau, n = a[0], float(a[1]), int(a[2])
        cand = [tuple(float(x) for x in parti[1 + i].split()) for i in range(6)]
        d[(beh, tau)] = (n, cand, tuple(float(x) for x in parti[7].split()))
    return d
def wilson(p, n, z=1.96):
    if n == 0: return (float('nan'),) * 2
    den = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return ((c - h) / den, (c + h) / den)
if __name__ == '__main__':
    d = leggi(sys.argv[1]); col = {'c90': 0, 'c50': 1, 'area': 2, 'noreg': 3}[sys.argv[2] if len(sys.argv) > 2 else 'c90']
    behs = []; [behs.append(b) for (b, t) in d if b not in behs]; taus = sorted({t for (b, t) in d})
    print('# %s  colonna=%s  (n fra parentesi; * = n<30)' % (sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'c90'))
    for ci, cn in enumerate(CN):
        print(cn)
        for b in behs:
            riga = '  %-11s' % b
            for t in taus:
                if (b, t) in d:
                    n, cand, _ = d[(b, t)]; riga += ' %4.1fs %5.3f(%3d)%s' % (t, cand[ci][col], n, '*' if n < 30 else ' ')
            print(riga)
    print('limiti esterni: REACH S1 S1congelato (minimo sui tau)')
    for b in behs:
        v = [d[(b, t)][2] for t in taus if (b, t) in d]; print('  %-11s %.3f %.3f %.3f' % (b, min(x[0] for x in v), min(x[1] for x in v), min(x[2] for x in v)))
