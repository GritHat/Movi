"""riconta_e1.py (sciame-avversario): riconto indipendente di E1 con integratore stabile. Uso: python -I riconta_e1.py <cartella 01-contatto>"""
import json, glob, math, sys, os
def w(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return "%d/%d [%.3f; %.3f]" % (k, n, max(0, c-h), min(1, c+h))
R = [json.loads(l) for f in sorted(glob.glob(os.path.join(sys.argv[1], "e1_stabile_0*.jsonl"))) for l in open(f)]
n = len(R); d = [r["ritardo_evento_s"] for r in R]
print("n", n, "idx unici", len({r["idx"] for r in R}))
print("0<=rit<=2", w(sum(x is not None and 0 <= x <= 2 for x in d), n))
print("rit<0", w(sum(x is not None and x < 0 for x in d), n), sorted(x for x in d if x is not None and x < 0))
print("0<=rit<=2.5", w(sum(x is not None and 0 <= x <= 2.5 for x in d), n))
print("mai", w(sum(x is None for x in d), n))
print("tutti dentro V", w(sum(r["frammenti_dentro_V"][0] == r["frammenti_dentro_V"][1] for r in R), n))
print("tipi precoci", [r["evento"]["tipo"] for r in R if r["ritardo_evento_s"] is not None and r["ritardo_evento_s"] < 0])
