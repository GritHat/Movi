#!/usr/bin/env python3
"""Stampa il contesto di ogni schema nei capitoli. Uso: contesto.py CARTELLA_CAPITOLI [-n MAX] [-w AMPIEZZA] schema..."""
import re, sys, pathlib
a = sys.argv[1:]; cart = pathlib.Path(a.pop(0)); mx = 5; w = 220
while a and a[0] in ("-n", "-w"):
    k = a.pop(0); v = int(a.pop(0))
    if k == "-n": mx = v
    else: w = v
for pat in a:
    print("===", pat); n = 0
    for f in sorted(cart.glob("*.tex")):
        for i, r in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for m in re.finditer(pat, r):
                n += 1
                if n <= mx: print(f"{f.name}:{i}: …{r[max(0,m.start()-w):m.end()+w]}…")
    print(f"    [{n} occorrenze]")
