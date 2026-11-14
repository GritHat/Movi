#!/usr/bin/env python3
"""cerca_py.py cartella contesto espr...: ricerca per espressione regolare nei .tex, con contesto (sola lettura)."""
import re,sys,glob,os
d=sys.argv[1]; ctx=int(sys.argv[2])
for e in sys.argv[3:]:
    print('---',e); pat=re.compile(e)
    for f in sorted(glob.glob(os.path.join(d,'*.tex'))):
        if os.path.basename(f).startswith('A_') and '--conA' not in sys.argv: pass
        for i,l in enumerate(open(f,encoding='utf8'),1):
            for m in pat.finditer(l):
                print(f"{os.path.basename(f)}:{i}: …{l[max(0,m.start()-ctx):m.end()+ctx].strip()}…")
