#!/usr/bin/env python3
# applica.py MODULO : applica le sostituzioni (file, vecchio, nuovo) del modulo; ogni «vecchio» deve comparire una volta sola.
import sys, os, importlib.util
qui = os.path.dirname(os.path.abspath(__file__)); base = os.path.join(qui, '..')
spec = importlib.util.spec_from_file_location('m', sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ok = ko = 0
for i, (f, v, n) in enumerate(m.E, 1):
    p = os.path.join(base, f); t = open(p, encoding='utf-8').read(); c = t.count(v)
    if c != 1:
        ko += 1; print(f'NON APPLICATA {i} ({f}): {c} occorrenze di «{v[:70]}»'); continue
    open(p, 'w', encoding='utf-8').write(t.replace(v, n)); ok += 1
print(f'{sys.argv[1]}: applicate {ok}, non applicate {ko}')
