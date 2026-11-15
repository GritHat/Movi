"""perdita.py - la divisione taratura/prova di 12-traiettorie separa i pezzi dello stesso mezzo? (solo lettura)"""
import os, re, sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "12-traiettorie"))
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], F, os.path.dirname(os.path.abspath(__file__))]
import prove_traiettorie as T
sc = T.scene() if hasattr(T, "scene") else None
met = T.dividi(sc)
grp = collections.defaultdict(set)
for cl, tp, d in sc:
    b = os.path.basename(d)
    k = re.sub(r"_\d+$", "", b)
    if cl == "droni" and b.startswith("alfa_"):
        k = "alfa_" + b.split("_")[1]            # stesso volo ALFA (data e ora)
    grp[(cl, k)].add(met[d])
for cl in sorted({c for c, _, _ in sc}):
    g = [v for (c, _), v in grp.items() if c == cl]
    both = sum(1 for v in g if len(v) == 2)
    print(cl, "mezzi", len(g), "con pezzi in taratura E in prova", both)
