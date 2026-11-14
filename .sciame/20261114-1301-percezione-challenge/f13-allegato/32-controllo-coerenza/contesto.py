#!/usr/bin/env python3
"""Stampa il contesto di uno o più schemi nei capitoli: python3 contesto.py CARTELLA LARGHEZZA schema1 schema2 ..."""
import re, sys, pathlib
base = pathlib.Path(sys.argv[1]); w = int(sys.argv[2])
for s in sys.argv[3:]:
    print(f"##### {s}")
    for f in sorted((base/'capitoli').glob('*.tex')):
        for n, r in enumerate(f.read_text().splitlines(), 1):
            for m in re.finditer(s, r):
                a, b = max(0, m.start()-w), min(len(r), m.end()+w)
                print(f"  {f.name[:2]}:{n}: …{r[a:b]}…")
