"""prove_v5b.py — VARIANTE: IMM4 con pesi che evolvono (catena di Markov) invece dei pesi fissati.  — taratura (σ_rif, fattore di q, ricalibrazione isotonica) SOLO sulla metà di taratura, verifica sulla
metà di prova. Stessi dati, divisione per mezzo, seme, sensore simulato e istanti di f19-volo/03-confidenza/prove_reali.py
(funzioni copiate qui, l'originale resta intatto). Uso: python -I prove_v5.py <classe> <uscita.json>"""
import csv, glob, json, math, os, re, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stima_v5 as S5
S4 = S5.S4
F15 = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f15-lunga-portata"
SEME = 20261115; DURATE = [1, 2, 5, 10, 20, 30]; K = 8; D2R = math.pi / 180
FATTORI = [0.25, 1.0, 4.0]; SRIF = [0.0, 10.0, 20.0, 40.0, 80.0]
FASCE = [(0, 2.5, "1-2"), (2.5, 5.5, "3-5"), (5.5, 10.5, "6-10"), (10.5, 20.5, "11-20"), (20.5, 40, "21-30")]


def mezzo(sc):
    for pat, f in [(r"atl_([0-9a-f]{6})$", lambda m: "icao:" + m.group(1)),
                   (r"lhrzrh_TRAIN_\d{4}-\d\d-\d\d_(\w+?)_(avv|dec)$", lambda m: "nvolo:" + m.group(1)),
                   (r"trajair_\d+_(\d+)_\d+$", lambda m: "icao:%06x" % int(m.group(1))),
                   (r"(cmu_m100_volo\d+)$", lambda m: m.group(1)),
                   (r"alfa_(\d{14})", lambda m: "T28:" + m.group(1))]:
        m = re.match(pat, sc)
        if m: return f(m)
    return sc


def leggi(d):
    r = list(csv.DictReader(open(os.path.join(d, "verita.csv"))))
    t = np.array([float(x["tempo"]) for x in r])
    P = np.array([[float(x["x"]), float(x["y"]), float(x["z"])] for x in r])
    V = np.array([[float(x["vx"]), float(x["vy"]), float(x["vz"])] for x in r])
    for _ in range(2):
        ok = np.concatenate([[True], np.diff(t) > 1e-6]); t, P, V = t[ok], P[ok], V[ok]
    return t, P, V


def scene():
    out = []
    for d in sorted(glob.glob(os.path.join(F15, "01-dati", "traiettorie", "aerei", "*"))):
        t, P, V = leggi(d)
        if np.median(np.linalg.norm(V, axis=1)) > 60: out.append(("aerei_veloci", d))
    for d in sorted(glob.glob(os.path.join(F15, "01-dati", "traiettorie", "droni", "*"))):
        out.append(("droni_ala_fissa" if os.path.basename(d).startswith("alfa") else "multirotori", d))
    return out


def dividi(sc):
    rng = np.random.default_rng(SEME); met = {}
    for cl in sorted({c for c, _ in sc}):
        g = sorted({mezzo(os.path.basename(d)) for c, d in sc if c == cl}); p = rng.permutation(len(g))
        lato = {g[k]: ("taratura" if j < len(g) // 2 else "prova") for j, k in enumerate(p)}
        for c, d in sc:
            if c == cl: met[d] = lato[mezzo(os.path.basename(d))]
    return met


def misura(cl, p, rng):
    if cl == "aerei_veloci":
        R = 7.5 ** 2 * np.eye(3); return p + 7.5 * rng.standard_normal(3), R
    s = np.array([1500.0, 0.0, -10.0]); d = p - s; r = np.linalg.norm(d); rh = np.hypot(d[0], d[1])
    ur = d / r; uaz = np.array([-d[1], d[0], 0]) / max(rh, 1e-6); uel = np.cross(ur, uaz)
    J = np.stack([ur, uaz * rh, uel * r], 1)
    R = J @ np.diag([0.6 ** 2, (0.75 * D2R) ** 2, (1.0 * D2R) ** 2]) @ J.T
    return p + np.linalg.cholesky(R) @ rng.standard_normal(3), R


def tipo_tratto(V, a, b):
    v = np.linalg.norm(V[a:b + 1], axis=1); h = np.arctan2(V[a:b + 1, 1], V[a:b + 1, 0])
    dh = np.abs((h - h[0] + np.pi) % (2 * np.pi) - np.pi)[np.hypot(V[a:b + 1, 0], V[a:b + 1, 1]) > 1.0]
    if dh.size and dh.max() > 15 * D2R: return "virata"
    if abs(v[-1] - v[0]) > max(2.0, 0.15 * v[0]): return "accelerazione"
    return "rettilineo"


def fascia(tau):
    for lo, hi, et in FASCE:
        if lo <= tau < hi: return et


def u_di(mix, ro):
    return S4.confidenza(mix, dict(dims=[0, 1, 2], A=max(ro, 1e-6) ** 2 * np.eye(3), c=None), n=40)


def lavora(arg):
    cl, d, fq, fq_old, completo, tab = arg        # tab: {"srif":, "astar": {fascia|modo: a*}} per la prova
    t, P, V = leggi(d)
    p_old = S4.scala_parametri(S4.PARAMETRI_BASE[cl], fq_old); p = S5.parametri(cl, fq)
    rng = np.random.default_rng([SEME] + list(os.path.basename(d).encode()))
    sel, ult = [], -1e9
    for i in range(len(t)):
        if t[i] >= ult + 1.0 - 1e-6: sel.append(i); ult = t[i]
    if len(sel) < 15: return []
    stati, fo, fn = [], None, None
    for i in sel:
        z, R = misura(cl, P[i], rng)
        if fo is None: fo = S4.IMM(z, R, t[i], p_old); fn = S5.IMM4(z, R, t[i], p)
        else:
            for f in (fo, fn): f.prevedi(t[i]); f.aggiorna(z, R)
        stati.append((i, fo.copia(), fn.copia()))
    out = []
    for D in DURATE:
        r2 = np.random.default_rng([SEME + D] + list(os.path.basename(d).encode()))
        cand = np.arange(10, len(stati))
        for k in r2.choice(cand, size=min(K, len(cand)), replace=False):
            i0, fi, f4 = stati[k]
            e = np.searchsorted(t, t[i0] + D - 1e-6)
            if e >= len(t): continue
            tau = t[e] - t[i0]
            if tau > D + max(1.5, 0.2 * D): continue
            modo = S5.NOMI4[int(np.argmax(f4.mu))]
            c = dict(scena=os.path.basename(d), mezzo=mezzo(os.path.basename(d)), D=D, tau=float(tau),
                     fascia=fascia(tau), tipo=tipo_tratto(V, i0, e), modo=modo)
            # prima: IMM v4 (pesi che evolvono), stesso fattore tarato in f19
            (_, mu, xs, Ps), = S4.predizione_senza_misure(fi, [tau]); mo = (mu, xs, Ps)
            mo_c = sum(mu[j] * xs[j][:3] for j in range(3)); ro_o = float(np.linalg.norm(P[e] - mo_c))
            c["u_old"] = u_di(mo, ro_o)
            # dopo: IMM4 a pesi fissati + σ_rif
            (_, mu4, xs4, Ps4), = S4.predizione_senza_misure(f4, [tau]); m4 = (mu4, xs4, Ps4)
            mc = sum(mu4[j] * xs4[j][:3] for j in range(4)); ro = float(np.linalg.norm(P[e] - mc))
            if not completo:
                c["u_new"] = {str(s): u_di(S5.con_rif(m4, s), ro) for s in SRIF}
            else:
                mr = S5.con_rif(m4, tab["srif"]); c["u_new"] = u_di(mr, ro)
                c["r90_old"] = S4.raggio_per_livello(mo, 0.9, (0, 1, 2), n=28, iter_=24)
                c["r90_new"] = S4.raggio_per_livello(mr, 0.9, (0, 1, 2), n=28, iter_=24)
                a = tab["astar"].get(c["fascia"] + "|" + modo, tab["astar"].get(c["fascia"], 0.9))
                c["astar"] = a
                c["r90_cal"] = S4.raggio_per_livello(mr, min(a, 0.9995), (0, 1, 2), n=28, iter_=24)
            out.append(c)
    return out


def wilson(k, n, z=1.96):
    if n == 0: return [None, None]
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(c - h, 4), round(c + h, 4)]


def scarto(casi, key, srif=None, lev=0.9):
    s = []
    for _, _, et in FASCE:
        cs = [c for c in casi if c["fascia"] == et]
        if len(cs) >= 10:
            u = [c[key][srif] if srif is not None else c[key] for c in cs]
            s.append(abs(sum(x <= lev for x in u) / len(cs) - lev))
    return float(np.mean(s)) if s else 9.9


if __name__ == "__main__":
    cl, OUT = sys.argv[1], sys.argv[2]
    FQ_OLD = {"aerei_veloci": 4.0, "droni_ala_fissa": 4.0, "multirotori": 0.25}[cl]   # scelta di f19 (prove_reali.log)
    t0 = time.time(); sc = scene(); met = dividi(sc)
    tar = [d for c, d in sc if c == cl and met[d] == "taratura"]; prv = [d for c, d in sc if c == cl and met[d] == "prova"]
    log = open(OUT.replace(".json", ".log"), "w")
    with Pool(8) as pool:
        griglia, casi_tar = {}, {}
        for fq in FATTORI:
            cs = [c for o in pool.map(lavora, [(cl, d, fq, FQ_OLD, False, None) for d in tar]) for c in o]
            casi_tar[fq] = cs
            for s in SRIF:
                griglia["%g|%g" % (fq, s)] = scarto(cs, "u_new", str(s))
                print(cl, "fq", fq, "srif", s, "n", len(cs), "scarto", round(griglia["%g|%g" % (fq, s)], 4), file=log, flush=True)
        best = min(griglia, key=griglia.get); fq, srif = map(float, best.split("|"))
        ct = casi_tar[fq]
        # ricalibrazione isotonica: a*(α=0,9) = quantile 0,9 empirico del PIT sulla taratura (ECDF, monotona per costruzione)
        astar = {}
        for _, _, et in FASCE:
            u = sorted(c["u_new"][str(srif)] for c in ct if c["fascia"] == et)
            if len(u) >= 20: astar[et] = float(np.quantile(u, 0.9))
            for m in S5.NOMI4:
                um = sorted(c["u_new"][str(srif)] for c in ct if c["fascia"] == et and c["modo"] == m)
                if len(um) >= 40: astar[et + "|" + m] = float(np.quantile(um, 0.9))
        print("scelta", fq, srif, astar, round(time.time() - t0, 1), file=log, flush=True)
        tab = dict(srif=srif, astar=astar)
        cp = [c for o in pool.map(lavora, [(cl, d, fq, FQ_OLD, True, tab) for d in prv]) for c in o]
    json.dump(dict(classe=cl, fq_scelto=fq, srif_scelto=srif, griglia_taratura=griglia, astar=astar,
                   n_taratura=len(ct), mezzi_taratura=len({c["mezzo"] for c in ct}),
                   casi_prova=cp, secondi=round(time.time() - t0, 1)), open(OUT, "w"))
    print("fine", round(time.time() - t0, 1), file=log, flush=True)
