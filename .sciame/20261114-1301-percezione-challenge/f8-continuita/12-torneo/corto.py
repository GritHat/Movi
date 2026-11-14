#!/usr/bin/env python3
"""Una riga per comportamento: c90 di C004, C001, C005W, ESTA ai tau 1, 2, 3 s; fuori REACH/S1; ciclo di vita. Uso: python3 corto.py ris/a*.txt"""
import sys, re
from riassunto import leggi
for p in sys.argv[1:]:
    d = leggi(p); righe = open(p).read().split('\n'); print('==', p.split('/')[-1])
    behs = []; [behs.append(b) for (b, t) in d if b not in behs]
    for b in behs:
        s = '  %-11s' % b
        for ci, cn in ((0, 'C004'), (1, 'C001'), (2, 'C005W'), (4, 'ESTA')):
            s += ' %s' % cn + ''.join(' %.2f' % d[(b, t)][1][ci][0] if (b, t) in d else '  -- ' for t in (1.0, 2.0, 3.0))
        s += ' | n ' + '/'.join(str(d[(b, t)][0]) if (b, t) in d else '-' for t in (1.0, 2.0, 3.0))
        print(s)
    for r in righe:
        if 'fuori REACH' in r: print('   ', re.sub(r'passaggi (\d+), con occlusione (\d+), cicli nascosti (\d+)', r'pass \1 occl \2 cicli \3', r)[:170])
    sez = 0
    for r in righe:
        if r.startswith('## '): sez = int(r[3:].split('.')[0]); continue
        if sez == 5 and r.strip(): print('    vita:', r)
        if sez == 3 and r.strip(): print('    visibile non rilevato:', r)
