#!/usr/bin/env python3
"""riconta5_arbitro.py - due totali della prova d'insieme: riaggancio (riga f) e passaggi scoperti con l'avviso richiesto acceso (riga e)."""
import sys, os, glob
F = sys.argv[1]; R = []
for f in sorted(glob.glob(os.path.join(F, '02-prova-insieme/ris/*.txt'))):
    for ln in open(f, encoding='utf-8'):
        if ln.startswith('R '):
            d = {}
            for tok in ln.split()[1:]:
                k, _, v = tok.partition('=')
                try: d[k] = float(v) if ('.' in v or 'nan' in v) else int(v)
                except ValueError: d[k] = v
            d['file'] = os.path.basename(f)[:-4]; R.append(d)
PERC = ('prosegue', 'rallenta', 'sosta', 'torna', 'sostalunga')
for g in 'DTL':
    for nome, sel in (('a_ (c7 0 e 1)', lambda r: r['file'].startswith(f'a_{g}_')), ('a_ + b_percorso', lambda r: r['file'].startswith(f'a_{g}_') or r['file'] == f'b_{g}_percorso'),
                      ('tutti senza estraneo, toglie=0', lambda r: r['geo'] == g and r['estr'] == 0 and r['toglie'] == 0)):
        rr = [r for r in R if sel(r) and r['beh'] in PERC]
        print(f"riaggancio {g} {nome:32s}: {sum(r['riagg'] for r in rr)}/{sum(r['ricomp'] for r in rr)}")
rr = [r for r in R if r['estr'] == 0 and r['toglie'] == 0 and r['c7'] == 1]
print('scoperti, c7=1, senza estraneo, toglie=0:', sum(r['scop_p']+r['nc_scop'] for r in rr), 'su', sum(r['n']-r['mai_nasc'] for r in rr), '(validi', sum(r['validi'] for r in rr), ')')
rr = [r for r in R if r['estr'] == 0 and r['toglie'] == 0]
print('idem con tutti i c7:', sum(r['scop_p']+r['nc_scop'] for r in rr), 'su', sum(r['n']-r['mai_nasc'] for r in rr), '| validi senza estraneo:', sum(r['validi'] for r in R if r['estr'] == 0))
