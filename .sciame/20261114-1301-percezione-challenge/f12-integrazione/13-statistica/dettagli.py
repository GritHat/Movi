#!/usr/bin/env python3
# dettagli.py — sciame-statistico, f12. Dove cadono V17 e V18 (per tipo di buchi), confronto con V7, Bonferroni su 5 e 15 celle in D.
import sys, json, os, math
from statistics import NormalDist
def wil(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c - h) / d, (c + h) / d
C = sys.argv[1]
for nome in ('banco.json', 'banco_semi2.json'):
    R = json.load(open(os.path.join(C, nome)))['righe']; print('==', nome)
    for g in ('V17', 'V18-1', 'V18-m', 'PR4'):
        for bn in ('nessuno', 'sparsi 5 %', 'sparsi 30 %', 'chiazze 5 %', 'chiazze 30 %'):
            A = [r for r in R if r['regola'] == g and r['sedici'] and abs(r['err']) <= 0.5 and r['buchi'] == bn]
            sv = [r for r in R if r['regola'] == g and r['scena'] == 'stanza vuota' and r['err'] == 0 and r['buchi'] == bn and abs(r['k'] - 0.004) < 1e-9][0]
            print(f"   {g:6s} {bn:13s}: 16 comb. err 0 e ±0,5: dentro {sum(r['dentro'] for r in A)} (oltre 5 cm {sum(r['profonde'] for r in A)}), nascoste {sum(r['nascoste'] for r in A)}, qv {sum(r['qv'] for r in A)}, fot. viol. {sum(r['fot_viol'] for r in A)}/{len(A)*30} | stanza vuota k 0,004: mediana {sv['mediana_m']:.1f} m, cambi {sv['cambi_s']:.2f}/s, sconosciuto {sv['sconosciuto']:.1f} %")
    for sc in sorted({r['scena'] for r in R if not r['sedici']}):
        for e in (0.0, 0.5, -0.5, 1.0, -1.0):
            A = [r for r in R if r['regola'] == 'PR4' and r['scena'] == sc and r['err'] == e]
            print(f"   PR4 [{sc}] err {e:+.1f}: celle {sum(r['dentro'] + r['nascoste'] for r in A)}, fot. viol. {sum(r['fot_viol'] for r in A)}/{len(A)*30}")
for m in (5, 15, 30):
    z = NormalDist().inv_cdf(1 - 0.025 / m)
    print(f'Bonferroni m={m} (z={z:.3f}): D primaria 1 s cella peggiore 942/1045 -> {wil(942,1045,z)[0]:.3f}; L torna 2 s primaria 1995/2112 -> {wil(1995,2112,z)[0]:.3f}; L torna 3 s primaria 1637/1774 -> {wil(1637,1774,z)[0]:.3f}; L torna 3 s secondaria 1754/1922 -> {wil(1754,1922,z)[0]:.3f}')
for k, n, e in ((2, 11701, 'scoperti pd 0,9'), (1, 5704, 'scoperti pd 0,9 esteso'), (22, 11701, 'scoperti pd 0,7'), (17, 5704, 'scoperti pd 0,7 esteso'), (24, 23402, 'scoperti tutti'), (29, 95399, 'scoperti maschera esatta')):
    print(f'{e}: {k}/{n} = {1000*k/n:.2f} per mille, Wilson {1000*wil(k,n)[0]:.2f}-{1000*wil(k,n)[1]:.2f} per mille')
