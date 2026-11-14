#!/usr/bin/env python3
"""riconta2_arbitro.py - controlli in piu' dell'arbitro: dettagli dell'identita', completezza per ricerca testuale (C-A), frasi (C-G)."""
import sys, os, glob, json, re, collections
S = sys.argv[1]; F = os.path.join(S, 'f12-integrazione')
def leggi(p): return [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
print('A. Identita\': dove sta il centro nascosto (tutte_p, tutti i profili e livelli)')
for nome in ('06-identita/risultati/nuovi424.jsonl', '06-identita/risultati/nuovi848.jsonl',
             '07-controprova-identita/risultati/ultimi424_replica.jsonl', '07-controprova-identita/risultati/ultimi848_replica.jsonl'):
    for conf in ('prima', 'tutte_p'):
        rr = [r for r in leggi(os.path.join(F, nome)) if r.get('conf') == conf and 'cella_centro_nascosto' in r]
        c = collections.Counter()
        for r in rr:
            for k, v in r['cella_centro_nascosto'].items(): c[k] += v
        print(f"   {nome.split('/')[-1]:28s} {conf:8s} passaggi {len(rr)}: {dict(c)}; riagganci a nascosto {sum(r.get('riagganci_a_soggetto_nascosto',0) for r in rr)}; pannello mobile {sum(1 for r in rr if r.get('pannello_si_muove'))}")
rr = [r for r in leggi(os.path.join(F, '07-controprova-identita/risultati/att_rotto.jsonl')) if r.get('gruppo') == 'B4_rimozione']
for conf in sorted({r['conf'] for r in rr}):
    x = [r['rimozione'] for r in rr if r['conf'] == conf]
    print('B. rimozione del pannello,', conf, 'n =', len(x), '| chiavi:', sorted(x[0].keys()))
    for k in sorted(x[0].keys()):
        print('     ', k, collections.Counter(json.dumps(v[k])[:30] for v in x).most_common(4))
for lar in (424, 848):
    rr = [r for r in leggi(os.path.join(F, '07-controprova-identita/risultati/att_estraneo.jsonl')) if r.get('gruppo') == f'E_estraneo_{lar}']
    for conf in sorted({r['conf'] for r in rr}):
        x = [r['estraneo'] for r in rr if r['conf'] == conf]
        if lar == 424 and conf == 'tutte_p': print('C. estraneo, chiavi:', sorted(x[0].keys()))
        same = sum(1 for e in x if e.get('idA') is not None and e.get('idA') == e.get('idB'))
        fu = sum(e.get('A_fuori_avviso', e.get('fuori_avviso', 0)) or 0 for e in x); na = sum(e.get('A_nascosta', 0) or 0 for e in x)
        print(f'   estraneo {lar} {conf}: identita\' di A data a B {same}/{len(x)}; A nascosta {na} fotogrammi; fuori avviso {fu}')
print('D. Completezza per ricerca testuale (occorrenze in V3 finale | tabella finale | blocco f14 | piano finale | schermo finale)')
docs = {'V3': '20-finale/SOLUZIONE_V3.md', 'TAB': '20-finale/TABELLA_CORREZIONI.md', 'PIA': '21-piano-finale/PIANO_14_4.md', 'SCH': '22-schermo-finale/SCHERMO_E_DEMO.md'}
T = {k: open(os.path.join(F, v), encoding='utf-8').read() for k, v in docs.items()}
T['BLO'] = open(os.path.join(S, 'f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md'), encoding='utf-8').read()
ordine = ['V3', 'TAB', 'BLO', 'PIA', 'SCH']
voci = [f'F-4{n:02d}' for n in range(1, 14)] + [f'K-40{n}' for n in range(1, 8)] + ['K-014', 'K-015', 'K-016', 'K-017', 'K-018', 'K-003', 'K-007',
        'K-216', 'K-305', 'K-404', 'K-406', 'K-107', 'K-108', 'K-109', 'K-110', 'K-111', 'K-202', 'K-214', 'K-215', 'K-218', 'K-219', 'K-220', 'K-221',
        'K-301', 'K-302', 'K-303', 'K-304', 'K-306', 'K-307', 'K-308', 'ingaggio', 'puntamento', 'R1', 'R8', 'M1', 'M8', 'c1', 'c8', 'C1', 'C8', '1,8 m', '0,5°',
        'classific', 'etichett', 'non è realizzato', 'a mano', 'CL1', 'SCENARIO', 'facoltativa']
for v in voci:
    pat = re.compile(r'(?<![A-Za-z0-9-])' + re.escape(v) + r'(?![0-9])')
    print(f"   {v:18s}", ' | '.join(f"{k} {len(pat.findall(T[k])):3d}" for k in ordine))
manc = [v for v in voci[:20] if not re.search(re.escape(v) + r'(?![0-9])', T['V3'] + T['TAB'])]
print('   F-401..F-413 e K-401..K-407 assenti sia da V3 sia dalla tabella:', manc)
print('E. Frasi da non dire fuori dagli elenchi di divieto (schermo finale, copione §7; piano finale)')
cop = T['SCH'].split('## 7.')[1] if '## 7.' in T['SCH'] else ''
vietate = ['validat', 'garantit', 'certificat', 'via libera', 'nessun ostacolo', 'bassa latenza', '15 Hz', 'drone', 'UAV', 'in volo', '100 %', 'riconosce', 'classifica', 'tarato',
           'identità mantenuta', 'dal vivo', 'mappa 3D', '360', 'perso', 'sosta', 'ispezione', 'Intelligenza Artificiale', '2,7 m', '9 su 10']
for v in vietate:
    n = len(re.findall(re.escape(v), cop, flags=re.I))
    if n: print(f"   copione: «{v}» {n} volta/e:", [m.group(0) for m in re.finditer('.{40}' + re.escape(v) + '.{40}', cop, flags=re.I)][:2])
print('   parole del copione:', len(cop.split()))
