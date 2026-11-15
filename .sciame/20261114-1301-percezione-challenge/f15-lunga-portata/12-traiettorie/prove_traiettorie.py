"""prove_traiettorie.py — previsione durante occlusioni VIRTUALI su traiettorie pubbliche reali (f15/12-traiettorie).

Tutto e' conto su dati pubblici con rumore di sensore SIMULATO dalle schede: niente e' provato su un sensore fisico.
Solo osservazione e avviso. Metodo e soglie: PREVISIONI.md (scritte prima).
Uso: python -I prove_traiettorie.py <radice f15> <cartella uscita>
"""
import csv, glob, json, math, os, sys, time
from multiprocessing import Pool
import numpy as np

F15, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(F15, "04-moto"))
import movi_lp as M  # noqa: E402

REG = M.carica_regole(os.path.join(F15, "04-moto", "regole_lunga_portata.json"))
SEME = 20261115
DURATE = [2, 5, 10, 20, 30]
FATTORI_Q = [0.25, 0.5, 1, 2, 4, 8]
LIVELLO = 0.90
K_ISTANTI = 10
MAPPA = {"aereo_aviazione_generale_circuito": "aereo_leggero", "aereo_avvicinamento": "aereo_linea_avvicinamento",
         "aereo_decollo": "aereo_linea_avvicinamento", "aereo_sorvolo": "aereo_linea_avvicinamento",
         "aereo_rullaggio": "aereo_rullaggio", "elicottero": "elicottero", "ala_fissa_senza_pilota": "drone_ala_fissa",
         "multirotore": "multirotore_piccolo", "auto": "auto_autostrada", "camion": "auto_autostrada",
         "moto": "auto_autostrada", "treno": "treno_alta_velocita"}
SCENARIO = {"aerei": "aeroporto_e_droni", "droni": "aeroporto_e_droni", "auto": "strada", "treni": "ferrovia"}
D2R = math.pi / 180
# sensore per classe (valori dalla scheda 02-sensori/parametri_lunga_portata.json; posizione e dove detto: IPOTESI)
SENS = {"aerei": dict(iso=7.5, periodo=1.0, dist=0.0),                       # SCANTER: sigma_posizione 7,5 m (ipotesi nella scheda)
        "droni": dict(sigma_r_m=0.6, sigma_az_rad=0.75 * D2R, sigma_el_rad=1.0 * D2R, periodo=1.0, dist=1500.0),  # IRIS
        "auto": dict(sigma_r_m=0.15, sigma_az_rad=0.3 * D2R, sigma_el_rad=0.3 * D2R, periodo=0.1, dist=100.0),    # ARS 548; sigma_az ipotesi
        "treni": dict(sigma_r_m=0.02, sigma_az_rad=0.03 * D2R, sigma_el_rad=0.03 * D2R, periodo=0.0, dist=300.0)}  # Tele-15


def leggi(scena):
    with open(os.path.join(scena, "verita.csv")) as f:
        r = list(csv.DictReader(f))
    t = np.array([float(x["tempo"]) for x in r])
    P = np.array([[float(x["x"]), float(x["y"]), float(x["z"])] for x in r])
    V = np.array([[float(x["vx"]), float(x["vy"]), float(x["vz"])] for x in r])
    ok = np.concatenate([[True], np.diff(t) > 1e-6])
    t, P, V = t[ok], P[ok], V[ok]
    ok = np.concatenate([[True], np.diff(t) > 1e-6])          # doppioni residui
    return t[ok], P[ok], V[ok]


def scene():
    out = []
    for cl in ["aerei", "droni", "auto", "treni"]:
        for d in sorted(glob.glob(os.path.join(F15, "01-dati", "traiettorie", cl, "*"))):
            s = json.load(open(os.path.join(d, "scena.json")))
            out.append((cl, s["oggetti"][0]["tipo"], d))
    return out


def dividi(sc):
    rng = np.random.default_rng(SEME)
    met = {}
    for cl in sorted({c for c, _, _ in sc}):
        idx = [i for i, x in enumerate(sc) if x[0] == cl]
        p = rng.permutation(len(idx))
        for j, k in enumerate(p):
            met[sc[idx[k]][2]] = "taratura" if j < len(idx) // 2 else "prova"
    return met


def filtra(arg):
    """Un passo del filtro per misura; salva la stima all'ultima misura (da cui partono zona e avviso) e il NIS."""
    cl, tipo, d, fq = arg
    t, P, V = leggi(d)
    s = SENS[cl]
    cfg = dict(REG["classi"][MAPPA[tipo]])
    cfg["q_cv"] *= fq
    cfg["q_manovra"] *= fq
    rng = np.random.default_rng([SEME] + list(os.path.basename(d).encode()))   # seme dichiarato, per scena
    sen = None
    if "iso" not in s:
        par = dict(sigma_r_m=s["sigma_r_m"], sigma_az_rad=s["sigma_az_rad"], sigma_el_rad=s["sigma_el_rad"])
        sen = M.Sensore("s", P[0] + np.array([s["dist"], 0.0, -10.0]), dict(par, pfa=1e-6, pd_rif=0.9, rcs_rif_m2=1, r_rif_m=1, esponente=4, r_max_m=1e9))
    sel, ult = [], -1e9
    for i in range(len(t)):
        if t[i] >= ult + s["periodo"] - 1e-6:
            sel.append(i)
            ult = t[i]
    tr, righe = None, []
    for i in sel:
        if sen is None:
            R = s["iso"] ** 2 * np.eye(3)
            z = P[i] + s["iso"] * rng.standard_normal(3)
        else:
            z, R = sen.misura(P[i], rng)
        m = M.Misura(t[i], z, R, "s", classe=MAPPA[tipo])
        if tr is None:
            tr = M.Traccia(1, m, REG, cfg)
            nis = float("nan")
        else:
            tr.prevedi(t[i])
            nis = tr.distanza(m)
            tr.aggiorna(m)
        righe.append((t[i], tr.p_ultima.copy(), tr.v_ultima.copy(), tr.sigp_ultima, tr.sigv_ultima, nis))
    return d, righe


def tipo_tratto(t, V, a, b):
    v = np.linalg.norm(V[a:b + 1], axis=1)
    v0 = v[0]
    if v0 < 1.0 or v.min() < max(1.0, 0.2 * v0):
        return "arresto"
    h = np.arctan2(V[a:b + 1, 1], V[a:b + 1, 0])
    vh = np.hypot(V[a:b + 1, 0], V[a:b + 1, 1])
    dh = np.abs((h - h[0] + np.pi) % (2 * np.pi) - np.pi)[vh > 1.0]
    if dh.size and dh.max() > 15 * D2R:
        return "virata"
    if abs(v[-1] - v0) > max(2.0, 0.15 * v0):
        return "accelerazione"
    return "rettilineo"


def casi(cl, d, righe):
    """Occlusioni virtuali: per ogni durata, K istanti a caso (seme dichiarato)."""
    t, P, V = leggi(d)
    tm = np.array([r[0] for r in righe])
    inv = M.inviluppo(REG, REG["scenari"][SCENARIO[cl]]["classi_ammesse"])
    out = []
    for D in DURATE:
        rng = np.random.default_rng([SEME + D] + list(os.path.basename(d).encode()))
        if len(tm) <= 10:
            continue
        cand = np.arange(10, len(tm))
        for k in rng.choice(cand, size=min(K_ISTANTI, len(cand)), replace=False):
            t_m, p, v, sp, sv, _ = righe[k]
            e = np.searchsorted(t, t_m + D - 1e-6)
            if e >= len(t):
                continue
            tau = t[e] - t_m
            if tau > (2 * D if D <= 5 else D + 5):
                continue
            a = np.searchsorted(t, t_m - 1e-6)
            err = float(np.linalg.norm(P[e] - (p + v * tau)))
            marg = 3.0 * (sp + sv * tau)
            v0 = min(float(np.linalg.norm(v)) + 3 * sv, inv["v_max"])
            R_avv = float(M.raggio_raggiungibile(tau, v0, inv["v_max"], inv["a_max"])) + 3 * sp + REG["ombra"]["fascia_di_guardia_m"]
            out.append(dict(D=D, tau=float(tau), err=err, marg=marg, R_avv=R_avv,
                            fuori_avv=bool(np.linalg.norm(P[e] - p) > R_avv), tipo=tipo_tratto(t, V, a, e),
                            v0=float(np.linalg.norm(V[a]))))
    return out


def tara(cs):
    r = {}
    for D in DURATE:
        sc = [c["err"] - c["marg"] for c in cs if c["D"] == D]
        r[D] = max(0.0, M.tara_regione(sc, LIVELLO)) if len(sc) >= 10 else None
    return r


def area_media(cs, r):
    a = [math.pi * (r[c["D"]] + c["marg"]) ** 2 for c in cs if r.get(c["D"]) is not None]
    return float(np.mean(np.log(a))) if a else float("inf")


def main():
    t0 = time.time()
    sc = scene()
    met = dividi(sc)
    ris = {"seme": SEME, "durate": DURATE, "livello": LIVELLO, "sensori": SENS, "mappa": MAPPA, "classi": {}}
    with Pool(8) as pool:
        for cl in ["aerei", "droni", "auto", "treni"]:
            mie = [x for x in sc if x[0] == cl]
            scelta = {}
            for fq in FATTORI_Q:
                cal = [x for x in mie if met[x[2]] == "taratura"]
                res = pool.map(filtra, [(c, tp, d, fq) for c, tp, d in cal])
                cs = [c for d, rr in res for c in casi(cl, d, rr)]
                r = tara(cs)
                scelta[fq] = (area_media(cs, r), r)
                print(cl, "q x", fq, "log-area media", round(scelta[fq][0], 3), flush=True)
            fq = min(scelta, key=lambda f: scelta[f][0])
            r = scelta[fq][1]
            prova = [x for x in mie if met[x[2]] == "prova"]
            res = pool.map(filtra, [(c, tp, d, fq) for c, tp, d in prova])
            tipo_di = {d: tp for _, tp, d in prova}
            nis = [rr[5] for _, rows in res for rr in rows[1:]]
            righe = []
            for d, rr in res:
                for c in casi(cl, d, rr):
                    c["scena"] = os.path.basename(d)
                    c["tipo_mezzo"] = tipo_di[d]
                    c["raggio"] = r[c["D"]] + c["marg"] if r[c["D"]] is not None else None
                    c["raggio"] = None if c["raggio"] is None else float(c["raggio"])
                    c["marg"] = float(c["marg"])
                    c["dentro"] = bool(c["raggio"] is not None and c["err"] <= c["raggio"])
                    c["ampio"] = bool(c["raggio"] is not None and c["raggio"] > REG["tracce"]["ampio_se_raggio_su_raggiungibile"] * c["R_avv"])
                    righe.append(c)
            ris["classi"][cl] = {"fattore_q": fq, "raggi_tarati": r, "log_area_taratura": {str(k): v[0] for k, v in scelta.items()},
                                 "tratti_taratura": len(mie) - len(prova), "tratti_prova": len(prova),
                                 "nis_media": float(np.nanmean(nis)), "nis_n": int(np.sum(np.isfinite(nis))),
                                 "nis_quota_oltre_7_81": float(np.nanmean(np.array(nis) > 7.81)), "casi": righe}
            print(cl, "fattore q scelto", fq, "casi di prova", len(righe), "NIS medio", round(ris["classi"][cl]["nis_media"], 2), flush=True)
    ris["secondi"] = time.time() - t0
    json.dump(ris, open(os.path.join(OUT, "risultati_traiettorie.json"), "w"), indent=0)
    print("secondi", round(ris["secondi"], 1))


if __name__ == "__main__":
    main()
