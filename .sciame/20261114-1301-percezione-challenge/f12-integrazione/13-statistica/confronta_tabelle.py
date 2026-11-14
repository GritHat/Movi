#!/usr/bin/env python3
# confronta_tabelle.py — sciame-statistico, f12. Confronta a macchina le celle di (b) in ris/TABELLE.txt (dell'autore) con le righe R grezze.
import sys, os, re, glob
ris = sys.argv[1]; R = {}
for f in glob.glob(os.path.join(ris, 'b_*_p*.txt')):
    for riga in open(f, encoding='utf-8'):
        if riga.startswith('R '):
            d = dict(t.split('=', 1) for t in riga.split()[1:] if '=' in t)
            for s in '123':
                R[(d['geo'], d['beh'], s)] = (int(d['inD' + s]), int(d['nD' + s]), int(d['inT' + s]), int(d['nT' + s]), int(d['shT' + s]))
n = ok = 0
for riga in open(os.path.join(ris, 'TABELLE.txt'), encoding='utf-8'):
    m = re.match(r'^([DTL]) (\S+)\s*\| (\d) \| (\d+)/(\d+)=\S+ \[\S+\] \| (\d+)/(\d+)=\S+ \[\S+\] \| (\d+)/(\d+)=', riga)
    if m:
        g, b, s = m.group(1), m.group(2), m.group(3); v = tuple(int(x) for x in m.groups()[3:])
        r = R.get((g, b, s)); n += 1
        if r and (r[0], r[1], r[2], r[3], r[4], r[3]) == v: ok += 1
        else: print('DIVERSA', g, b, s, v, r)
print(f'celle di (b) in TABELLE.txt: {n}; uguali alle righe grezze (primaria, secondaria, mostrata): {ok}')
