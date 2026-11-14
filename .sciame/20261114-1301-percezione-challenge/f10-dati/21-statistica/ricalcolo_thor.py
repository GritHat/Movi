#!/usr/bin/env python3
"""sciame-statistico — ricalcolo indipendente del banco THÖR (previsione a velocità quasi costante su pedoni veri).

Legge solo 12-dati-veri/tracce/<nome>/tracce.npz (allow_pickle=False). Filtro scritto qui (per asse, 2 stati:
gli assi sono disaccoppiati perché R è isotropa), non quello della catena. Stesso protocollo scritto dalla validazione
alle 17:14: 15 Hz, finestre non sovrapposte di 4 s per persona (1 s di rincorsa con rumore σ = 2 cm, 3 s al buio),
velocità iniziale con scarto 2,5 m/s, ellisse al 90 % (χ² = 4,605). Unità statistica: la PERSONA (ricampionamento
per persona, 4000 repliche); in più copertura per persona e «togline una».
Uso: <python> -I -B ricalcolo_thor.py → tabelle/thor.json e una tabella."""
import json
import os
import sys

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
TR = os.path.join(os.path.dirname(QUI), "12-dati-veri", "tracce")
HZ, NPRE, NBUIO = 15, 15, 45
ORIZ = (1.0, 2.0, 3.0)
GRIGLIA = (0.01, 0.05, 0.1, 0.2, 0.5)
CHI2 = 4.605


def finestre(nome, sfasamento=0):
    d = np.load(os.path.join(TR, nome, "tracce.npz"), allow_pickle=False)
    t, xy = d["tempo_s"], d["xy_m"].astype(np.float64)
    idx = np.unique(np.rint(np.arange(0, t[-1], 1.0 / HZ) * 100).astype(int))
    idx = idx[idx < len(t)]
    xy = xy[idx]
    L = NPRE + NBUIO
    out = []
    for p in range(xy.shape[1]):
        ok = np.isfinite(xy[:, p]).all(axis=1)
        k = sfasamento
        while k + L <= len(xy):
            if ok[k:k + L].all():
                out.append((p, xy[k:k + L, p]))
                k += L
            else:
                k += 1
    return out


def filtro_asse(m, q, sigma, v0=2.5, dt=1.0 / HZ):
    """Kalman a 2 stati (posizione, velocità) su una sola coordinata; restituisce stato e covarianza finali."""
    x = np.array([m[0], 0.0])
    P = np.array([[sigma ** 2, 0.0], [0.0, v0 ** 2]])
    F = np.array([[1.0, dt], [0.0, 1.0]])
    Q = q * np.array([[dt ** 3 / 3, dt ** 2 / 2], [dt ** 2 / 2, dt]])
    for z in m[1:]:
        x = F @ x
        P = F @ P @ F.T + Q
        s = P[0, 0] + sigma ** 2
        K = P[:, 0] / s
        x = x + K * (z - x[0])
        P = P - np.outer(K, P[0, :])
    return x, P


def valuta(fin, q, sigma, seme):
    rng = np.random.default_rng(seme)
    R = []
    for p, vero in fin:
        mis = vero[:NPRE] + rng.normal(0, sigma, (NPRE, 2))
        st = [filtro_asse(mis[:, a], q, sigma) for a in (0, 1)]
        vel = float(np.hypot(*(vero[NPRE - 1] - vero[0])) / ((NPRE - 1) / HZ))
        r = {"p": p, "vel": vel}
        for h in ORIZ:
            j = NPRE - 1 + int(round(h * HZ))
            m2, e2 = 0.0, 0.0
            for a in (0, 1):
                x, P = st[a]
                pred = x[0] + x[1] * h
                var = P[0, 0] + 2 * h * P[0, 1] + h * h * P[1, 1] + q * h ** 3 / 3
                e = pred - vero[j, a]
                m2 += e * e / var
                e2 += e * e
            r[f"in{h}"] = m2 <= CHI2
            r[f"err{h}"] = float(np.sqrt(e2))
            r[f"fermo{h}"] = float(np.hypot(*(mis[NPRE - 1] - vero[j])))
        R.append(r)
    return R


def per_persona(R, chiave):
    d = {}
    for r in R:
        d.setdefault(r["p"], []).append(float(r[chiave]))
    return d


def ic_persona(R, chiave, f=np.mean, n=4000, seme=7):
    rng = np.random.default_rng(seme)
    d = per_persona(R, chiave)
    ids = list(d)
    v = [f(np.concatenate([d[ids[i]] for i in rng.integers(0, len(ids), len(ids))])) for _ in range(n)]
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def main():
    ris = {}
    F = {"exp1": finestre("thor_exp1_run1"), "exp3": finestre("thor_exp3_run1")}
    for k, v in F.items():
        per = {}
        for p, _ in v:
            per[p] = per.get(p, 0) + 1
        print(f"{k}: {len(v)} tratti, {len(per)} persone; tratti per persona {sorted(per.values())}")
        ris[k] = {"tratti": len(v), "per_persona": per}
    print("\n== copertura dell'ellisse al 90 % a 1 / 2 / 3 s (σ = 2 cm); IC 95 % ricampionando le PERSONE ==")
    tab = {}
    for exp in ("exp1", "exp3"):
        for q in GRIGLIA:
            R = valuta(F[exp], q, 0.02, 11 if exp == "exp1" else 33)
            riga = {}
            for h in ORIZ:
                c = float(np.mean([r[f"in{h}"] for r in R]))
                lo, hi = ic_persona(R, f"in{h}")
                pp = [float(np.mean(v)) for v in per_persona(R, f"in{h}").values()]
                loo = []
                d = per_persona(R, f"in{h}")
                for esclusa in d:
                    loo.append(float(np.mean(np.concatenate([v for k_, v in d.items() if k_ != esclusa]))))
                em = float(np.median([r[f"err{h}"] for r in R]))
                elo, ehi = ic_persona(R, f"err{h}", f=np.median)
                riga[str(h)] = {"copertura": c, "ic": [lo, hi], "per_persona_min_max": [min(pp), max(pp)],
                                "togline_una_min_max": [min(loo), max(loo)], "errore_mediano": em, "ic_errore": [elo, ehi],
                                "errore_p90": float(np.percentile([r[f"err{h}"] for r in R], 90)),
                                "fermo_mediano": float(np.median([r[f"fermo{h}"] for r in R]))}
            scarto = float(np.mean([abs(riga[str(h)]["copertura"] - 0.9) for h in ORIZ]))
            tab[f"{exp}_q{q}"] = dict(riga, scarto=scarto, N=len(R))
            print(f"{exp} q={q}: " + " / ".join(
                f"{riga[str(h)]['copertura']:.3f} [{riga[str(h)]['ic'][0]:.2f}–{riga[str(h)]['ic'][1]:.2f}; persone "
                f"{riga[str(h)]['per_persona_min_max'][0]:.2f}–{riga[str(h)]['per_persona_min_max'][1]:.2f}]" for h in ORIZ)
                + f"; scarto da 0,90: {scarto:.3f}; errore mediano " + " / ".join(
                f"{riga[str(h)]['errore_mediano']:.2f} [{riga[str(h)]['ic_errore'][0]:.2f}–{riga[str(h)]['ic_errore'][1]:.2f}]" for h in ORIZ)
                + "; fermo " + " / ".join(f"{riga[str(h)]['fermo_mediano']:.2f}" for h in ORIZ))
    for exp in ("exp1", "exp3"):
        scelto = min(GRIGLIA, key=lambda q: tab[f"{exp}_q{q}"]["scarto"])
        print(f"q scelto su {exp} con la regola scritta: {scelto}")
        ris[f"q_scelto_{exp}"] = scelto
    # sensibilità: seme del rumore e sfasamento delle finestre (exp3, q = 0,05 e 0,2)
    print("\n== sensibilità (exp3): 20 semi del rumore; sfasamento delle finestre di 0, 1, 2, 3 s ==")
    for q in (0.05, 0.1, 0.2):
        cs = np.array([[np.mean([r[f"in{h}"] for r in valuta(F["exp3"], q, 0.02, s)]) for h in ORIZ] for s in range(100, 120)])
        sf = []
        for off in (0, 15, 30, 45):
            Fo = finestre("thor_exp3_run1", off)
            R = valuta(Fo, q, 0.02, 33)
            sf.append([len(Fo)] + [round(float(np.mean([r[f"in{h}"] for r in R])), 3) for h in ORIZ])
        print(f"q={q}: fra i semi min–max " + " / ".join(f"{cs[:, i].min():.3f}–{cs[:, i].max():.3f}" for i in range(3))
              + f"; sfasamenti [N, 1 s, 2 s, 3 s]: {sf}")
        ris[f"sens_q{q}"] = {"semi_min": cs.min(0).tolist(), "semi_max": cs.max(0).tolist(), "sfasamenti": sf}
    # effetto del raggruppamento: IC ingenuo (Wilson sui tratti) contro IC per persona, q = 0,05 a 2 s
    R = valuta(F["exp3"], 0.05, 0.02, 33)
    k = sum(r["in2.0"] for r in R)
    n = len(R)
    p = k / n
    z = 1.96
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    hh = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    lo, hi = ic_persona(R, "in2.0")
    print(f"\nexp3 q=0,05 a 2 s: Wilson sui tratti {c - hh:.3f}–{c + hh:.3f} (larghezza {2 * hh:.3f}); per persona {lo:.3f}–{hi:.3f} "
          f"(larghezza {hi - lo:.3f}); rapporto delle larghezze {(hi - lo) / (2 * hh):.2f}")
    ris["tabella"] = tab
    with open(os.path.join(QUI, "tabelle", "thor.json"), "w", encoding="utf-8") as f:
        json.dump(ris, f, indent=1)


if __name__ == "__main__":
    main()
