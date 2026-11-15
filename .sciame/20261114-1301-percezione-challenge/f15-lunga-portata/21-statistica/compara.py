"""Confronta la divisione per scena (12-traiettorie) e per mezzo (21-statistica/ridivisione), per classe e D.
Intervalli: Wilson sui casi; Wilson con n = mezzi distinti di prova; bootstrap a grappoli per mezzo (2000).
Uso: python -I compara.py <f15> <cartella 21-statistica>"""
import json, os, sys, re, collections
import numpy as np
F15, S = sys.argv[1], sys.argv[2]
Z = 1.959963984540054
def wilson(k, n):
    p = k / n; den = 1 + Z * Z / n; c = (p + Z * Z / (2 * n)) / den
    h = Z * np.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den
    return max(0., c - h), min(1., c + h)
def mezzo(sc):   # unita' indipendente: aereo (ICAO o numero di volo), volo per i droni (2 soli esemplari), veicolo, treno
    for pat, f in [(r"atl_([0-9a-f]{6})$", lambda m: "icao:" + m.group(1)),
                   (r"lhrzrh_TRAIN_\d{4}-\d\d-\d\d_(\w+?)_(avv|dec)$", lambda m: "nvolo:" + m.group(1)),
                   (r"trajair_\d+_(\d+)_\d+$", lambda m: "icao:%06x" % int(m.group(1))),
                   (r"(cmu_m100_volo\d+)$", lambda m: m.group(1)),
                   (r"alfa_(\d{14})", lambda m: "T28:" + m.group(1)),
                   (r"ngsim_us101_v(\d+)_\d+$", lambda m: "veicolo:" + m.group(1)),
                   (r"fi_treno(\d+)_\d+$", lambda m: "treno:" + m.group(1))]:
        m = re.match(pat, sc)
        if m: return f(m)
    return sc
rng = np.random.default_rng(1)
res = {}
A = json.load(open(os.path.join(F15, "12-traiettorie", "risultati_traiettorie.json")))
B = json.load(open(os.path.join(S, "ridivisione", "risultati_traiettorie.json")))
def riga(cc, chiave="dentro"):
    n = len(cc); k = sum(c[chiave] for c in cc)
    g = collections.defaultdict(list)
    for c in cc: g[mezzo(c["scena"])].append(c[chiave])
    arr = [np.array(v, float) for v in g.values()]; G = len(arr)
    pm = np.mean([a.mean() for a in arr])
    bs = []
    for _ in range(2000):
        s = rng.integers(0, G, G); bs.append(sum(arr[i].sum() for i in s) / sum(len(arr[i]) for i in s))
    return {"k": k, "n": n, "p": k / n, "wilson": wilson(k, n), "mezzi": G, "wilson_mezzi": wilson(pm * G, G),
            "boot": (float(np.quantile(bs, .025)), float(np.quantile(bs, .975))),
            "mezzi_con_almeno_un_caso": sum(1 for a in arr if a.any())}
for cl in A["classi"]:
    res[cl] = {}
    for D in A["durate"]:
        a = [c for c in A["classi"][cl]["casi"] if c["D"] == D]
        b = [c for c in B["classi"][cl]["casi"] if c["D"] == D]
        ra, rb = riga(a), riga(b); fa = riga(b, "fuori_avv")
        res[cl][D] = {"scena": ra, "mezzo": rb, "fuori_avv_mezzo": fa}
        print("%-6s D=%2d  scena %.3f [%.3f;%.3f] n=%d | mezzo %.3f [%.3f;%.3f] n=%d mezzi=%d Wm[%.3f;%.3f] boot[%.3f;%.3f] | fuori %d/%d=%.3f, mezzi con fuori %d/%d  diff %+.3f" % (
            cl, D, ra["p"], *ra["wilson"], ra["n"], rb["p"], *rb["wilson"], rb["n"], rb["mezzi"], *rb["wilson_mezzi"], *rb["boot"],
            fa["k"], fa["n"], fa["p"], fa["mezzi_con_almeno_un_caso"], fa["mezzi"], rb["p"] - ra["p"]))
    # sottotipi droni
    if cl == "droni":
        for tm in ["multirotore", "ala_fissa_senza_pilota"]:
            for D in (5, 10):
                b = [c for c in B["classi"][cl]["casi"] if c["D"] == D and c["tipo_mezzo"] == tm]
                r = riga(b); res[cl]["%s_%d" % (tm, D)] = r
                print("   %s D=%d %.3f n=%d voli=%d Wvoli[%.3f;%.3f] boot[%.3f;%.3f]" % (tm, D, r["p"], r["n"], r["mezzi"], *r["wilson_mezzi"], *r["boot"]))
json.dump(res, open(os.path.join(S, "compara.json"), "w"), indent=1, default=float)
