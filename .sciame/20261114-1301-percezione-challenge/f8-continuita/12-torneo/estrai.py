#!/usr/bin/env python3
"""Estrae dalle sezioni 2, 5 e 8 dei risultati: 'piccola e sbagliata', punto su libero, vita, errore del punto. Uso: python3 estrai.py ris/base_T.txt ..."""
import sys, re
for p in sys.argv[1:]:
    sez = 0; beh = ''; print('==', p.split('/')[-1]); tot = [0, 0, 0]; out2 = {}; out8 = []
    for r in open(p):
        if r.startswith('## '): sez = int(r[3:].split('.')[0]); continue
        if sez == 2:
            m = re.match(r'(\S+)\s+passaggi (\d+), con occlusione (\d+), cicli nascosti (\d+)', r)
            if m: beh = m.group(1); continue
            m = re.match(r'\s+(\S+)\s+senza\s+([\d.]+) \((\d+)\).*suFG\s+([\d.]+) \((\d+)\).*piccolaSbagliata\s+([\d.]+) \((\d+)\) \| puntoFG\s+([\d.]+)', r)
            if m: out2.setdefault(beh, []).append('%s senza %s%% (%s) cw %s%% (%s) puntoFG %s%%' % (m.group(1), m.group(2), m.group(3), m.group(6), m.group(7), m.group(8)))
        if sez == 5:
            a = r.split('|')
            if len(a) >= 4 and a[0].split() and a[0].split()[0] != '##':
                tot[0] += int(a[0].split()[1]); tot[1] += int(a[1].split()[0]); tot[2] += int(a[1].split()[1].strip('()'))
        if sez == 8 and '|' in r: out8.append(r.rstrip())
    for b, v in out2.items(): print('  %-11s' % b, ' | '.join(x for x in v if not x.startswith(('C005P', 'ESTB'))))
    print('  vita: passaggi %d, con cicli nascosti senza traccia pendente %d (%.1f %%), cicli %d' % (tot[0], tot[1], 100.0 * tot[1] / max(1, tot[0]), tot[2]))
    print('  errore mediano del punto: C004 | C001 media | vel.cost | EST-A | fermo')
    for r in out8:
        if r.split()[0] in ('prosegue', 'sosta', 'torna') and r.split()[1] in ('1.0', '2.0', '3.0', '5.0'): print('   ', r)
