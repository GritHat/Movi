#!/usr/bin/env python3
"""sciame-creativo, f8: conti per il «pannello virtuale» (creativo-1). Uso: timeout 60 python3 tabellone.py
(1) P-creativo-6: potenza del tabellone, binomiale esatta. (2) P-creativo-7: miscele ripesate su esito_v1_w1.txt e, notato dopo, su esito_v2_w1_senzaC.txt."""
import math, re
def tail(n, k, p): return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c - h) / d, (c + h) / d
print('## (1) tabellone: P(almeno k su n dentro la regione al 90 %) per copertura vera p')
for n, k in ((30, 24), (20, 16), (60, 51)):
    print('n=%d soglia k=%d: ' % (n, k) + '  '.join('p=%.2f -> %.3f' % (p, tail(n, k, p)) for p in (0.90, 0.80, 0.70, 0.60)))
for k, n in ((27, 30), (18, 20), (54, 60)): print('Wilson 95 %% di %d su %d: %.2f-%.2f' % ((k, n) + wilson(k, n)))
print('passaggi in 3 minuti: corda del campo a 4 m = %.1f m; a 1,25 m/s %.1f s; con 2 s di giro: %d passaggi' % (2 * 4 * math.tan(math.radians(43.5)), 2 * 4 * math.tan(math.radians(43.5)) / 1.25, 180 // (2 * 4 * math.tan(math.radians(43.5)) / 1.25 + 2)))
def load(fn, col):
    d = {}
    for l in open(fn):
        m = re.match(r'^([a-z]+) +([0-9.]+) +(\d+) \| +(\d+) +(\d+)', l)
        if m: d[(m.group(1), float(m.group(2)))] = (int(m.group(3)), int(m.group(4 + col)))
    return d
VIRT = {'prosegue': .90, 'rallenta': .05, 'svolta': .05}; VERO = {'prosegue': .40, 'sosta': .30, 'torna': .15, 'lontano': .15}
def mix(d, w, tau):
    num = den = 0.0
    for b, pi in w.items():
        if (b, tau) in d: n, c = d[(b, tau)]; num += pi * n / 100 * c; den += pi * n / 100
    return num / den if den else float('nan')
for fn, col, lab in (('esito_v1_w1.txt', 0, 'v1, regione al 50 % (P-creativo-7, registrata)'), ('esito_v2_w1_senzaC.txt', 1, 'v2 fronte+scia, regione al 90 % (notato dopo)'),
                     ('esito_v2_w1.txt', 1, 'v2 con ventaglio, regione al 90 % (notato dopo)')):
    d = load(fn, col); print('## (2) %s: copertura fra chi e ancora nascosto, miscela in vista / miscela dietro il pannello vero / differenza' % lab)
    for tau in (1.0, 2.0, 3.0, 4.0):
        a = mix(d, VIRT, tau); b = mix(d, VERO, tau); print('  tau %.0f s: %5.1f / %5.1f / %+5.1f' % (tau, a, b, a - b))
