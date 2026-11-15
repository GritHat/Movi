"""riconta_taratura.py (sciame-avversario): fuga fra le meta' e riconto della copertura per fascia, dai json di 02-taratura."""
import json, math, os, sys, collections
import numpy as np
T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "02-taratura")
sys.path.insert(0, T)
import prove_v5 as PV
def w(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return "%d/%d=%.3f [%.3f; %.3f]" % (k, n, p, max(0, c-h), min(1, c+h))
sc = PV.scene(); met = PV.dividi(sc)
cl_of = {d: c for c, d in sc}
for cl in sorted(set(cl_of.values())):
    tar = {PV.mezzo(os.path.basename(d)) for d, l in met.items() if l == "taratura" and cl_of[d] == cl}
    prv = {PV.mezzo(os.path.basename(d)) for d, l in met.items() if l == "prova" and cl_of[d] == cl}
    print(cl, "mezzi tar", len(tar), "prova", len(prv), "intersezione", len(tar & prv))
    # attacco: chiave del mezzo per volo lhrzrh (numero di volo, non aereo): stesse scene con basename diverso?
    nv = [m for m in tar | prv if m.startswith("nvolo:")]
    print("  chiavi per numero di volo:", len(nv))
for f, cl in [("ris_aerei.json", "aerei_veloci"), ("ris_droni_ala_fissa.json", "droni_ala_fissa"), ("ris_multirotori.json", "multirotori"), ("ris_b_aerei.json", "aerei_veloci b")]:
    R = json.load(open(os.path.join(T, f)))
    cp = R["casi_prova"]
    mz = {c["mezzo"] for c in cp}
    sc_prova = {c["scena"] for c in cp}
    fuga = [s for s in sc_prova if met.get(next((d for d in met if os.path.basename(d) == s), ""), "") != "prova"]
    print("\n", f, "n prova", len(cp), "mezzi", len(mz), "scene prova non in meta' prova:", len(fuga), "astar", R["astar"])
    rng = np.random.default_rng(777)
    M = sorted(mz)
    for _, _, et in PV.FASCE + [(0, 0, "tutte")]:
        cs = [c for c in cp if et == "tutte" or c["fascia"] == et]
        k_old = sum(c["u_old"] <= 0.9 for c in cs); k_new = sum(c["u_new"] <= 0.9 for c in cs)
        k_cal = sum(c["u_new"] <= c["astar"] for c in cs)
        # bootstrap a grappoli per mezzo (mio, seme 777, 1000)
        by = collections.defaultdict(list)
        for c in cs: by[c["mezzo"]].append(c["u_new"] <= c["astar"])
        ks = list(by); bs = []
        for _ in range(1000):
            pick = rng.choice(len(ks), len(ks)); v = [x for i in pick for x in by[ks[i]]]; bs.append(np.mean(v))
        print("  %-6s prima %s | dopo %s | dopo+iso %s {boot %.3f; %.3f}" % (et, w(k_old, len(cs)), w(k_new, len(cs)), w(k_cal, len(cs)), np.quantile(bs, .025), np.quantile(bs, .975)))
    for tipo in sorted({c["tipo"] for c in cp}):
        cs = [c for c in cp if c["tipo"] == tipo]
        print("  tipo %-14s prima %s dopo+iso %s dopo %s" % (tipo, w(sum(c["u_old"] <= .9 for c in cs), len(cs)), w(sum(c["u_new"] <= c["astar"] for c in cs), len(cs)), w(sum(c["u_new"] <= .9 for c in cs), len(cs))))
    # mezzo con piu' peso
    cnt = collections.Counter(c["mezzo"] for c in cp); print("  mezzo piu' pesante:", cnt.most_common(2), "su", len(cp))
