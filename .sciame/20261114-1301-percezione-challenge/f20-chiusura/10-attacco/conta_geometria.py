"""conta_geometria.py (sciame-avversario): conteggi per variante di geometria, Wilson per passaggio."""
import json, math, sys, collections
def w(k, n, z=1.96):
    if n == 0: return "0/0"
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return "%d/%d [%.3f; %.3f]" % (k, n, max(0, c-h), min(1, c+h))
R = [json.loads(l) for l in open(sys.argv[1])]
err = [r for r in R if "errore" in r]
print("errori", len(err), err[:1])
G = collections.defaultdict(list)
for r in R:
    if "errore" not in r: G[(r["var"], r["cfg"])].append(r)
for (v, c), L in sorted(G.items()):
    n = len(L); dl = [r["ritardo"] for r in L]
    dm = sorted(r["dmin_vero_m_t"][0] for r in L if r["dmin_vero_m_t"])
    s = "%-14s %s n=%d  " % (v, c, n)
    if v.startswith("F3"):
        s += "entro2 %s | entro3 %s | prima %s | mai %s | inneschi %s" % (
            w(sum(x is not None and 0 <= x <= 2 for x in dl), n), w(sum(x is not None and 0 <= x <= 3 for x in dl), n),
            w(sum(x is not None and x < 0 for x in dl), n), w(sum(x is None for x in dl), n),
            dict(collections.Counter((r["innesco"] or {}).get("perche") for r in L)))
    else:
        s += "falsi %s | dmin vero mediano %.0f m" % (w(sum(r["evento"] for r in L), n), dm[len(dm)//2])
    s += " | libero sul vero %s" % w(sum(r["libero_vero"] > 0 for r in L), n)
    print(s)
