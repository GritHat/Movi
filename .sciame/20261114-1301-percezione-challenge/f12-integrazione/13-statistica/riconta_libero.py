#!/usr/bin/env python3
# riconta_libero.py — sciame-statistico, f12. Riconta dai file grezzi banco.json e banco_semi2.json (una riga per condizione e regola).
# Uso: python -I -B riconta_libero.py <cartella 03-libero>
import sys, os, json, math, zlib, re
def wup(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c + h) / d
C = sys.argv[1]
for nome in ('banco.json', 'banco_semi2.json', 'banco_lancio1.json'):
    d = json.load(open(os.path.join(C, nome))); NF = d['NF']; R = d['righe']
    regole = sorted({r['regola'] for r in R}); cond = {(r['k'], r['scena'], r['err'], r['buchi']) for r in R}
    scene = sorted({r['scena'] for r in R}); s16 = sorted({r['scena'] for r in R if r['sedici']})
    print(f'== {nome}: NF={NF}, righe {len(R)}, regole {len(regole)}, condizioni {len(cond)}, fotogrammi {len(cond)*NF}; scene {len(scene)} (di cui nelle 16 combinazioni: {len(s16)} x 2 k)')
    print('   regola | S1 16 comb., err 0 e ±0,5: condizioni, dentro (oltre 5 cm), nascoste, qv, fotogrammi con violazione/tot, condizioni con violazione | tutte le 10 scene, err 0 e ±0,5: celle, fot. viol./tot, cond. viol./tot | ±1 grado tutte le scene: celle, fot. viol./tot | S2 mediana k=0,004 / 0,01')
    for g in regole:
        A = [r for r in R if r['regola'] == g and r['sedici'] and abs(r['err']) <= 0.5]
        B = [r for r in R if r['regola'] == g and abs(r['err']) <= 0.5]
        U = [r for r in R if r['regola'] == g and abs(r['err']) > 0.5]
        viol = lambda r: r['dentro'] + r['nascoste'] + r['qv']
        s2 = [r['mediana_m'] for k in (0.004, 0.01) for r in R if r['regola'] == g and r['scena'] == 'stanza vuota' and r['err'] == 0 and r['buchi'] == 'sparsi 5 %' and abs(r['k'] - k) < 1e-9]
        print(f"   {g:6s}| {len(A)}, {sum(r['dentro'] for r in A)} ({sum(r['profonde'] for r in A)}), {sum(r['nascoste'] for r in A)}, {sum(r['qv'] for r in A)}, {sum(r['fot_viol'] for r in A)}/{len(A)*NF}, {sum(r['fot_viol']>0 for r in A)}/{len(A)} | {sum(viol(r) for r in B)}, {sum(r['fot_viol'] for r in B)}/{len(B)*NF}, {sum(r['fot_viol']>0 for r in B)}/{len(B)} | {sum(viol(r) for r in U)}, {sum(r['fot_viol'] for r in U)}/{len(U)*NF} | {' / '.join('%.1f' % x for x in s2)}")
    if nome != 'banco_lancio1.json':
        B = [r for r in R if r['regola'] == 'PR4' and abs(r['err']) <= 0.5]
        nc = len(B); geo = len({(r['scena'], r['err']) for r in B})
        print(f"   PR4 (nuvole-1), err 0 e ±0,5: 0 violazioni? {sum(r['fot_viol'] for r in B) == 0}. Limite superiore di Wilson al 95 %: per fotogramma {wup(0, nc*NF):.5f} (n={nc*NF}, NON indipendenti); per condizione {wup(0, nc):.4f} (n={nc}); per geometria (scena x errore) {wup(0, geo):.3f} (n={geo}); per scena {wup(0, 10):.3f} (n=10)")
        for bn in ('nessuno', 'sparsi 5 %', 'sparsi 30 %', 'chiazze 5 %', 'chiazze 30 %'):
            X = [r for r in R if r['regola'] == 'PR4' and r['sedici'] and r['err'] == 0 and r['buchi'] == bn]
            print(f"      PR4 resa media 16 comb. err 0, {bn}: {sum(r['resa'] for r in X)/len(X):.1f} %  (n={len(X)})")
        for r in R:
            if r['regola'] == 'PR4' and r['scena'] == 'stanza vuota' and r['buchi'] in ('nessuno', 'sparsi 5 %') :
                print(f"      PR4 stanza vuota k={r['k']} err={r['err']:+.1f} {r['buchi']}: mediana {r['mediana_m']:.1f} m, resa {r['resa']:.1f} %, settori {r['settori']}, sconosciuto {r['sconosciuto']:.1f} %")
# semi: uno per condizione? (riga 116 di banco_libero.py: crc32 di "nome|k|e|buchi" + SEME0)
d = json.load(open(os.path.join(C, 'banco.json'))); R = d['righe']
cond = sorted({(r['scena'], r['k'], r['err'], r['buchi']) for r in R})
for suff in ('', 'semi2'):
    semi = [zlib.crc32(("%s|%g|%g|%s%s" % (n, k, e, b, suff)).encode()) for (n, k, e, b) in cond]
    print(f"semi «{suff}»: condizioni {len(cond)}, semi distinti {len(set(semi))}")
a = [zlib.crc32(("%s|%g|%g|%s%s" % (n, k, e, b, '')).encode()) for (n, k, e, b) in cond]; b2 = [zlib.crc32(("%s|%g|%g|%s%s" % (n, k, e, b, 'semi2')).encode()) for (n, k, e, b) in cond]
print('semi comuni fra i due lanci:', len(set(a) & set(b2)))
# righe identiche fra i due lanci (testo dei risultati), per tipo di buchi
A = [l for l in open(os.path.join(C, 'risultati_banco.txt'), encoding='utf-8') if l.startswith('k=')]
B = [l for l in open(os.path.join(C, 'risultati_banco_semi2.txt'), encoding='utf-8') if l.startswith('k=')]
print('righe di risultato:', len(A), len(B))
for bn in ('nessuno', 'sparsi 5 %', 'sparsi 30 %', 'chiazze 5 %', 'chiazze 30 %'):
    ia = [(x, y) for x, y in zip(A, B) if '| ' + bn in x]
    print(f"   {bn}: righe {len(ia)}, identiche fra i due lanci {sum(x == y for x, y in ia)} ({100*sum(x == y for x, y in ia)/len(ia):.1f} %)")
L1 = [l for l in open(os.path.join(C, 'risultati_banco_lancio1.txt'), encoding='utf-8') if l.startswith('k=')]
sA = set(A); print('righe del lancio 1 ritrovate identiche nel lancio 2 con gli stessi semi:', sum(l in sA for l in L1), 'su', len(L1))
