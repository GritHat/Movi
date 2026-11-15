"""concentrazione.py (sciame-avversario): peso dei singoli mezzi nella meta' di prova degli aerei; copertura senza i due voli piu' pesanti."""
import json, math, os, collections
T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "02-taratura")
def w(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return "%d/%d=%.3f [%.3f; %.3f]" % (k, n, p, max(0, c-h), min(1, c+h))
cp = json.load(open(os.path.join(T, "ris_aerei.json")))["casi_prova"]
cnt = collections.Counter(c["mezzo"] for c in cp)
print("casi per mezzo:", cnt.most_common())
print("scene per mezzo (top):", {m: len({c['scena'] for c in cp if c['mezzo'] == m}) for m, _ in cnt.most_common(3)})
top2 = {m for m, _ in cnt.most_common(2)}
for nome, sel in [("solo i 2 voli piu' pesanti", lambda c: c["mezzo"] in top2), ("gli altri 14 mezzi", lambda c: c["mezzo"] not in top2)]:
    for et in ["1-2", "3-5", "6-10", "11-20", "21-30"]:
        cs = [c for c in cp if sel(c) and c["fascia"] == et]
        if cs: print(nome, et, "dopo+iso", w(sum(c["u_new"] <= c["astar"] for c in cs), len(cs)), "prima", w(sum(c["u_old"] <= .9 for c in cs), len(cs)))
# per mezzo, tutte le fasce
for m, n in cnt.most_common():
    cs = [c for c in cp if c["mezzo"] == m]
    print("  %-22s %s" % (m, w(sum(c["u_new"] <= c["astar"] for c in cs), n)))
