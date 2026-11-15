"""prove_reali.py — confidenza prevista contro frequenza osservata su traiettorie PUBBLICHE reali (ADS-B aerei veloci,
droni ALFA ad ala fissa, multirotori CMU), con occlusioni virtuali di 1-30 s e rumore di sensore SIMULATO dalle schede
(stesse ipotesi di f15/12-traiettorie). Taratura e prova divise per MEZZO (stessa funzione mezzo() di f15/21-statistica).
Uso: python -I prove_reali.py <radice f15> <cartella uscita>"""
import csv, glob, json, math, os, re, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stima_v4 as S

F15, OUT = sys.argv[1], sys.argv[2]
SEME = 20261115
DURATE = [1, 2, 5, 10, 20, 30]
K = 8
LIV = [0.5, 0.68, 0.9, 0.95, 0.99]
FATTORI = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0.25, 1.0, 4.0, 16.0]
D2R = math.pi / 180


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
    rng = np.random.default_rng(SEME)
    met = {}
    for cl in sorted({c for c, _ in sc}):
        g = sorted({mezzo(os.path.basename(d)) for c, d in sc if c == cl})
        p = rng.permutation(len(g))
        lato = {g[k]: ("taratura" if j < len(g) // 2 else "prova") for j, k in enumerate(p)}
        for c, d in sc:
            if c == cl: met[d] = lato[mezzo(os.path.basename(d))]
    return met


def misura(cl, p, rng):
    if cl == "aerei_veloci":                                  # radar di superficie/terminale: sigma 7,5 m isotropa (ipotesi f15)
        R = 7.5 ** 2 * np.eye(3)
        return p + 7.5 * rng.standard_normal(3), R
    s = np.array([1500.0, 0.0, -10.0])                        # radar per droni a 1,5 km (scheda IRIS f15; posizione ipotesi)
    d = p - s; r = np.linalg.norm(d); rh = np.hypot(d[0], d[1])
    ur = d / r; uaz = np.array([-d[1], d[0], 0]) / max(rh, 1e-6)
    uel = np.cross(ur, uaz)
    J = np.stack([ur, uaz * rh, uel * r], 1)
    R = J @ np.diag([0.6 ** 2, (0.75 * D2R) ** 2, (1.0 * D2R) ** 2]) @ J.T
    return p + np.linalg.cholesky(R) @ rng.standard_normal(3), R


def tipo_tratto(V, a, b):
    v = np.linalg.norm(V[a:b + 1], axis=1)
    h = np.arctan2(V[a:b + 1, 1], V[a:b + 1, 0])
    dh = np.abs((h - h[0] + np.pi) % (2 * np.pi) - np.pi)[np.hypot(V[a:b + 1, 0], V[a:b + 1, 1]) > 1.0]
    if dh.size and dh.max() > 15 * D2R: return "virata"
    if abs(v[-1] - v[0]) > max(2.0, 0.15 * v[0]): return "accelerazione"
    return "rettilineo"


def lavora(arg):
    cl, d, fq, completo = arg
    t, P, V = leggi(d)
    p = S.scala_parametri(S.PARAMETRI_BASE[cl], fq)
    rng = np.random.default_rng([SEME] + list(os.path.basename(d).encode()))
    sel, ult = [], -1e9
    for i in range(len(t)):
        if t[i] >= ult + 1.0 - 1e-6: sel.append(i); ult = t[i]
    if len(sel) < 15: return d, []
    stati = []
    f_cv = f_imm = None
    for i in sel:
        z, R = misura(cl, P[i], rng)
        if f_cv is None:
            f_cv = S.FiltroCV(z, R, t[i], p); f_imm = S.IMM(z, R, t[i], p)
        else:
            for f in (f_cv, f_imm): f.prevedi(t[i]); f.aggiorna(z, R)
        stati.append((i, S.copia_cv(f_cv), f_imm.copia()))
    out = []
    for D in DURATE:
        r2 = np.random.default_rng([SEME + D] + list(os.path.basename(d).encode()))
        cand = np.arange(10, len(stati))
        for k in r2.choice(cand, size=min(K, len(cand)), replace=False):
            i0, fc, fi = stati[k]
            e = np.searchsorted(t, t[i0] + D - 1e-6)
            if e >= len(t): continue
            tau = t[e] - t[i0]
            if tau > D + max(1.5, 0.2 * D): continue
            caso = dict(D=D, tau=float(tau), tipo=tipo_tratto(V, i0, e), v0=float(np.linalg.norm(V[i0])))
            for nome, f in (("cv", fc), ("imm", fi)):
                (_, mu, xs, Ps), = S.predizione_senza_misure(f, [tau])
                mix = (mu, xs, Ps)
                m = sum(mu[j] * xs[j][:3] for j in range(len(mu)))
                ro = float(np.linalg.norm(P[e] - m))
                # PIT: confidenza prevista della sfera centrata sulla previsione con raggio = distanza osservata
                u = S.confidenza(mix, dict(dims=[0, 1, 2], A=max(ro, 1e-6) ** 2 * np.eye(3), c=None), n=48)
                caso[nome] = dict(err=ro, u=u)
                if completo:
                    caso[nome]["r90"] = S.raggio_per_livello(mix, 0.9, (0, 1, 2), n=32, iter_=28)
                    if nome == "cv":                     # NEES esatto (chi-quadro 3) per il filtro lineare
                        dd = P[e] - xs[0][:3]
                        nees = float(dd @ np.linalg.solve(Ps[0][:3, :3], dd))
                        caso[nome]["u_nees"] = float(S.C_sfera_centrata(math.sqrt(nees), 1.0))
            out.append(caso)
    return d, out


def wilson(k, n, z=1.96):
    if n == 0: return [None, None]
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(c - h, 4), round(c + h, 4)]


FASCE = [(0, 2.5, "1-2"), (2.5, 5.5, "3-5"), (5.5, 10.5, "6-10"), (10.5, 20.5, "11-20"), (20.5, 40, "21-30")]


def affidabilita(casi, nome, chiave="u"):
    res = {}
    for lo, hi, et in FASCE:
        cs = [c for c in casi if lo <= c["tau"] < hi and chiave in c[nome]]
        res[et] = {str(a): dict(n=len(cs), k=sum(c[nome][chiave] <= a for c in cs),
                                oss=round(sum(c[nome][chiave] <= a for c in cs) / max(len(cs), 1), 4),
                                wilson=wilson(sum(c[nome][chiave] <= a for c in cs), len(cs))) for a in LIV}
    return res


def scarto90(casi, nome):
    s = []
    for lo, hi, _ in FASCE:
        cs = [c for c in casi if lo <= c["tau"] < hi]
        if len(cs) >= 10: s.append(abs(sum(c[nome]["u"] <= 0.9 for c in cs) / len(cs) - 0.9))
    return float(np.mean(s)) if s else 9.9


if __name__ == "__main__":
    t0 = time.time()
    sc = scene(); met = dividi(sc)
    os.makedirs(OUT, exist_ok=True)
    log = open(os.path.join(OUT, "prove_reali.log"), "w")
    ris = {"conteggi": {}, "taratura": {}, "prova": {}}
    with Pool(8) as pool:
        for cl in ["aerei_veloci", "droni_ala_fissa", "multirotori"]:
            tar = [d for c, d in sc if c == cl and met[d] == "taratura"]
            prv = [d for c, d in sc if c == cl and met[d] == "prova"]
            ris["conteggi"][cl] = dict(scene_taratura=len(tar), scene_prova=len(prv),
                                       mezzi_taratura=len({mezzo(os.path.basename(d)) for d in tar}),
                                       mezzi_prova=len({mezzo(os.path.basename(d)) for d in prv}))
            scelta, best = {}, {}
            for fq in FATTORI:
                cs = [c for _, o in pool.map(lavora, [(cl, d, fq, False) for d in tar]) for c in o]
                for nome in ("cv", "imm"):
                    s = scarto90(cs, nome)
                    print(cl, nome, "fattore", fq, "casi", len(cs), "scarto90 medio", round(s, 4), file=log, flush=True)
                    if nome not in best or s < best[nome][1]: best[nome] = (fq, s)
            scelta = {k: v[0] for k, v in best.items()}
            ris["taratura"][cl] = scelta
            prova = {}
            for nome in ("cv", "imm"):
                cs = [c for _, o in pool.map(lavora, [(cl, d, scelta[nome], True) for d in prv]) for c in o]
                prova[nome] = cs
            # confronto: stessi casi? i casi dipendono solo da seme e scena, non dal fattore: stessi istanti
            rr = {"n_casi": {k: len(v) for k, v in prova.items()}}
            for nome in ("cv", "imm"):
                cs = prova[nome]
                rr["affidabilita_" + nome] = affidabilita(cs, nome)
                if nome == "cv": rr["affidabilita_nees_cv"] = affidabilita(cs, "cv", "u_nees")
                tab = {}
                for lo, hi, et in FASCE:
                    sub = [c for c in cs if lo <= c["tau"] < hi]
                    if not sub: continue
                    k90 = sum(c[nome]["u"] <= 0.9 for c in sub)
                    tab[et] = dict(n=len(sub), err_mediano_m=round(float(np.median([c[nome]["err"] for c in sub])), 2),
                                   err_p95_m=round(float(np.percentile([c[nome]["err"] for c in sub], 95)), 2),
                                   r90_mediano_m=round(float(np.median([c[nome]["r90"] for c in sub])), 2),
                                   area90_mediana_m2=round(float(np.median([math.pi * c[nome]["r90"] ** 2 for c in sub])), 1),
                                   copertura90=round(k90 / len(sub), 4), wilson90=wilson(k90, len(sub)))
                    for tp in ("rettilineo", "virata", "accelerazione"):
                        s2 = [c for c in sub if c["tipo"] == tp]
                        k2 = sum(c[nome]["u"] <= 0.9 for c in s2)
                        tab[et]["copertura90_" + tp] = dict(n=len(s2), oss=round(k2 / max(len(s2), 1), 4), wilson=wilson(k2, len(s2)))
                rr["tabella_" + nome] = tab
            ris["prova"][cl] = rr
            json.dump(prova, open(os.path.join(OUT, "casi_prova_%s.json" % cl), "w"))
            print(cl, "fatto", round(time.time() - t0, 1), "s", file=log, flush=True)
    ris["secondi"] = round(time.time() - t0, 1)
    json.dump(ris, open(os.path.join(OUT, "risultati_reali.json"), "w"), indent=1, ensure_ascii=False)
    print("fine", ris["secondi"], file=log)
