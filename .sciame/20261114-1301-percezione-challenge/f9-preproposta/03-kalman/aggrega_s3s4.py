#!/usr/bin/env python3
# sciame-kalman f9: rilegge le righe DATI di ris_s3s4_*.txt e stampa le tabelle.  Uso: python3 aggrega_s3s4.py
import glob, math
Q = {'prosegue': 0.5, 'sosta': 0.2, 'ritorno': 0.1, 'lontano': 0.1, 'passo': 0.1}
D = {}
for f in sorted(glob.glob('ris_s3s4_*.txt')):
    for line in open(f):
        if not line.startswith('DATI'):
            continue
        p = line.split()
        beh, e, lett, q, nv, k = p[1], p[2], p[3], float(p[4]), int(p[5]), int(p[6])
        D[(lett, e, q, beh, k)] = (nv, {a.split('=')[0]: float(a.split('=')[1]) for a in p[7:]})
T = {8: '0,5', 15: '1', 30: '2', 45: '3'}
ORD = ['prosegue', 'sosta', 'ritorno', 'lontano', 'passo', 'TUTTI']


def get(lett, e, q, beh, k):
    if beh != 'TUTTI':
        nv, d = D[(lett, e, q, beh, k)]
        return d
    out = {}
    for b, s in Q.items():
        nv, d = D[(lett, e, q, b, k)]
        for kk, v in d.items():
            out[kk] = out.get(kk, 0.0) + s * v / nv * 2000
    return out


def r(a, b):
    return f"{a / b:5.3f}" if b > 0 else "  -  "


for (lett, e, q) in sorted({(a, b, c) for (a, b, c, _, _) in D}):
    print(f"\n=== lettura {lett}, errore della maschera {e} m, q in occlusione {q} ===")
    print("comport.  tau   n     | K cop  r95  | A: 1s    2,45s  reg95  area  sig   mu1  >0,8  zero | B: 1s   2,45s  reg95  area  mu1   >0,8 | C reg95 area | C2: in_portata cop  area  p_fuori dich.  vero")
    for beh in ORD:
        for k in (8, 15, 30, 45):
            d = get(lett, e, q, beh, k)
            n = d['n']
            if n <= 0:
                continue
            nA = max(1e-9, n - d['Avuota'])
            print(f"{beh:9s} {T[k]:>3s} {n:7.0f} | {r(d['Kc'], n)} {d['Kr'] / n:4.2f} | {r(d['A1'], n)} {r(d['A245'], n)} {r(d['Ah'], n)} {d['Aa'] / nA:5.2f} {d['Ase'] / nA:4.2f} {d['Amu'] / nA:5.2f} {r(d['A08'], n)} {r(d['Az'], n)} | "
                  f"{r(d['B1'], n)} {r(d['B245'], n)} {r(d['Bh'], n)} {d['Ba'] / n:5.2f} {d['Bmu'] / n:5.2f} {r(d['B08'], n)} | {r(d['Ch'], n)} {d['Ca'] / n:4.2f} | "
                  f"n_in={d['Cnin']:6.0f} {r(d['Chin'], d['Cnin'])} {(d['Cain'] / d['Cnin']) if d['Cnin'] > 0 else 0:4.2f}  {d['Cpo'] / n:5.3f} {r(d['Cto'], n)}")
