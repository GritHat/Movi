import json, math, sys
from collections import defaultdict
D = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f20-chiusura/05-scorta/"
def wil(k, n, z=1.959964):
    if n == 0: return (None, None)
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (round(max(0, c-h), 3), round(min(1, c+h), 3))
def leggi(f):
    out = defaultdict(list)
    for l in open(f):
        r = json.loads(l); out[(r["var"], r["cfg"])].append(r)
    return out
def misure(rr):
    inters = [r for r in rr if r["interseca_t"] is not None]
    m = {}
    m["n"] = len(rr)
    m["avviso_prima_fr"] = (sum(1 for r in inters if r["avviso_t"] is not None and r["avviso_t"] <= r["interseca_t"]), len(inters))
    m["riacq_rad_2s"] = (sum(1 for r in rr if r.get("rit_riacq_rad") is not None and r["rit_riacq_rad"] <= 2.0), len(rr))
    m["spurie_non_dich_c1"] = (sum(1 for r in rr if r.get("riacq_spurie_non_dich", 0) > 0 or r["assoc_detriti_non_dich"] > 0), len(rr))
    m["riacq_spurie_tutte"] = (sum(1 for r in rr if r.get("riacq_spurie", 0) > 0), len(rr))
    m["spuria_o_assoc_nd(def F7r)"] = (sum(1 for r in rr if r.get("riacq_spurie", 0) > 0 or r["assoc_detriti_non_dich"] > 0), len(rr))
    m["id_ok"] = (sum(1 for r in rr if r.get("id_ok")), len(rr))
    m["cont_ok"] = (sum(1 for r in rr if r["cont_ok"]), len(rr))
    m["libero>0"] = (sum(1 for r in rr if r["libero"] > 0 or r["libero_fr"] > 0), len(rr))
    m["falso_evento_o_avviso"] = (sum(1 for r in rr if r["falso_evento"] or (r["var"] == "F7c" and r["avviso_t"] is not None)), len(rr))
    m["avviso_acceso"] = (sum(1 for r in rr if r["avviso_t"] is not None), len(rr))
    m["riacq_dubbie"] = (sum(1 for r in rr if r.get("riacq_dubbie", 0) > 0), len(rr))
    mg = [r["interseca_t"] - r["avviso_t"] for r in inters if r["avviso_t"] is not None]
    m["margine_min_s"] = round(min(mg), 2) if mg else None
    m["margine_med_s"] = round(sorted(mg)[len(mg)//2], 2) if mg else None
    return m
if __name__ == "__main__":
    for f in sys.argv[1:]:
        print("==", f)
        T = leggi(f)
        for k in sorted(T):
            m = misure(T[k])
            print(k, {a: (b if not isinstance(b, tuple) else "%d/%d %s" % (b[0], b[1], wil(*b))) for a, b in m.items()})
