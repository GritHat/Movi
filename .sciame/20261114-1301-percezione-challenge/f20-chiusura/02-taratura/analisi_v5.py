"""analisi_v5.py — tabella prima/dopo sulla metà di prova: copertura al 90 % per fascia e per tipo di moto,
Wilson per caso (casi correlati dentro un mezzo: intervallo ottimista) e bootstrap a grappoli per mezzo (2000, seme fisso).
Uso: python -I analisi_v5.py <ris_classe.json> ... <uscita.json>"""
import json, math, sys
import numpy as np
FASCE = ["1-2", "3-5", "6-10", "11-20", "21-30"]


def wilson(k, n, z=1.96):
    if n == 0: return [None, None]
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(c - h, 3), round(c + h, 3)]


def coperto(c, v):
    return c["u_old"] <= 0.9 if v == "prima" else (c["u_new"] <= 0.9 if v == "dopo" else c["u_new"] <= c["astar"])


def boot(cs, v, B=2000, seme=20261115):
    g = {}
    for c in cs: g.setdefault(c["mezzo"], []).append(coperto(c, v))
    ks = list(g); rng = np.random.default_rng(seme); st = []
    if len(ks) < 2: return [None, None]
    for _ in range(B):
        s = rng.integers(0, len(ks), len(ks)); a = sum(sum(g[ks[i]]) for i in s); n = sum(len(g[ks[i]]) for i in s)
        st.append(a / n)
    return [round(float(np.quantile(st, 0.025)), 3), round(float(np.quantile(st, 0.975)), 3)]


def riga(cs, v):
    k = sum(coperto(c, v) for c in cs); n = len(cs)
    return dict(k=k, n=n, oss=round(k / n, 3) if n else None, wilson=wilson(k, n), boot_mezzi=boot(cs, v) if n else None,
                mezzi=len({c["mezzo"] for c in cs}))


out = {}
for f in sys.argv[1:-1]:
    R = json.load(open(f)); cp = R["casi_prova"]; cl = R["classe"]; o = dict(fq=R["fq_scelto"], srif=R["srif_scelto"],
          astar=R["astar"], n_prova=len(cp), mezzi_prova=len({c["mezzo"] for c in cp}), n_taratura=R["n_taratura"],
          mezzi_taratura=R["mezzi_taratura"], griglia=R["griglia_taratura"])
    for v in ("prima", "dopo", "cal"):
        o[v] = {}
        for et in FASCE:
            cs = [c for c in cp if c["fascia"] == et]
            o[v][et] = riga(cs, v)
            for tp in ("virata", "accelerazione", "rettilineo"):
                o[v][et + "|" + tp] = riga([c for c in cs if c["tipo"] == tp], v)
        for tp in ("virata", "accelerazione"):
            o[v]["tutte|" + tp] = riga([c for c in cp if c["tipo"] == tp], v)
        o[v]["scarto_medio"] = round(float(np.mean([abs(o[v][et]["oss"] - 0.9) for et in FASCE if o[v][et]["n"] >= 10])), 4)
    o["area"] = {}
    for et in FASCE:
        cs = [c for c in cp if c["fascia"] == et]
        a = {k: float(np.median([math.pi * c[k] ** 2 for c in cs])) for k in ("r90_old", "r90_new", "r90_cal")}
        o["area"][et] = dict(r90_mediano_m={k: round(math.sqrt(v / math.pi), 1) for k, v in a.items()},
                             rapporto_new=round(a["r90_new"] / a["r90_old"], 3), rapporto_cal=round(a["r90_cal"] / a["r90_old"], 3))
    out[cl] = o
json.dump(out, open(sys.argv[-1], "w"), indent=1, ensure_ascii=False)
for cl, o in out.items():
    print("==", cl, "fq", o["fq"], "srif", o["srif"], "n", o["n_prova"], "mezzi", o["mezzi_prova"])
    for v in ("prima", "dopo", "cal"):
        print(v, "scarto", o[v]["scarto_medio"], " | ".join("%s %s %s b%s" % (et, o[v][et]["oss"], o[v][et]["wilson"], o[v][et]["boot_mezzi"]) for et in FASCE))
        print("   virata", [(et, o[v][et + "|virata"]["k"], o[v][et + "|virata"]["n"]) for et in FASCE], "tutte", o[v]["tutte|virata"]["oss"], o[v]["tutte|virata"]["wilson"])
        print("   accel ", [(et, o[v][et + "|accelerazione"]["k"], o[v][et + "|accelerazione"]["n"]) for et in FASCE], "tutte", o[v]["tutte|accelerazione"]["oss"], o[v]["tutte|accelerazione"]["wilson"], o[v]["tutte|accelerazione"]["boot_mezzi"])
    print("area", o["area"])
