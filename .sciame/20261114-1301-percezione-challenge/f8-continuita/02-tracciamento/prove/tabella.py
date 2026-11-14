#!/usr/bin/env python3
"""tabella.py <file risultati> <metodo> <colonna: err|p90|c50|c90|a50|a90|punt|lib> : matrice comportamento x tau (con n)."""
import sys, re
f, met, col = sys.argv[1], sys.argv[2], sys.argv[3]
ci = {'err': 0, 'p90': 1, 'c50': 2, 'c90': 3, 'a50': 4, 'a90': 5, 'punt': 6, 'lib': 7}[col]
beh = None; out = {}
for l in open(f):
    if l.startswith('== '): beh = l.split()[1]; continue
    if '|' not in l or met not in l or beh is None or l.startswith(' ') is False: continue
    p = l.split('|'); h = p[0].split(); nums = re.findall(r'-?\d+\.\d+|nan', '|'.join(p[1:]).replace(met, ''))
    out.setdefault(beh, {})[h[0]] = (int(h[1]), nums[ci])
print('%s  %s  %s' % (f, met, col))
for b, d in out.items():
    print('  %-10s' % b + ' '.join('%s:%s(%d)' % (t, v, n) for t, (n, v) in d.items()))
