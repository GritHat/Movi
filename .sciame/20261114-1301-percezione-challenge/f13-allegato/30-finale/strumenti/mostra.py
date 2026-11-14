#!/usr/bin/env python3
# mostra.py FILE(prefisso) AMPIEZZA SCHEMA... : stampa il contesto di ogni schema (regex) nei capitoli
import re, sys, glob, os
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'capitoli')
pref, amp = sys.argv[1], int(sys.argv[2])
for f in sorted(glob.glob(os.path.join(d, pref + '*.tex'))):
    t = open(f, encoding='utf-8').read()
    for s in sys.argv[3:]:
        for m in re.finditer(s, t):
            a, b = max(0, m.start() - amp), min(len(t), m.end() + amp)
            r = t.count('\n', 0, m.start()) + 1
            print(f'== {os.path.basename(f)}:{r} [{s}]\n{t[a:b]}\n')
