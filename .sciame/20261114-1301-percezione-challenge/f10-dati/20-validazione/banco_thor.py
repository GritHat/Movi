#!/usr/bin/env python3
"""Misura 4 su pedoni veri (THÖR, cattura del moto): previsione durante un'occlusione creata a posteriori.

Tracce a 15 Hz; per persona, finestre non sovrapposte: RINCORSA s di misure (verità + rumore gaussiano σ per asse),
poi 3 s senza misure. Predittori: filtro del nucleo (kalman.py della catena, q), «fermo all'ultima misura»,
«velocità costante senza rumore di processo» (lo stesso filtro con q = 0). Errore contro la verità a 0,5 / 1 / 2 / 3 s,
copertura dell'ellisse al 90 % dichiarata e del cerchio al 95 % della catena. Taratura di q su exp1, prova su exp3.
Uso: <python> -I -B banco_thor.py   → uscite/banco_thor.json e una tabella."""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K                                             # noqa: E402
import numpy as np                                             # noqa: E402
from kalman import Kalman, rumore_processo, transizione        # noqa: E402

HZ, RINCORSA, BUIO = 15.0, 1.0, 3.0
ORIZZONTI = (0.5, 1.0, 2.0, 3.0)
GRIGLIA_Q = (0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0)
CHI2_90, CHI2_95 = 4.605, 5.9915


def finestre(nome):
    d = np.load(os.path.join(K.TRACCE, nome, "tracce.npz"), allow_pickle=False)
    t, xy = d["tempo_s"], d["xy_m"]
    idx = np.unique(np.rint(np.arange(0, t[-1], 1.0 / HZ) * 100).astype(int))
    idx = idx[idx < len(t)]
    t15, xy15 = t[idx], xy[idx].astype(np.float64)
    n_pre, n_buio = int(round(RINCORSA * HZ)), int(round(BUIO * HZ))
    lung = n_pre + n_buio
    fuori = []
    for p in range(xy15.shape[1]):
        ok = np.isfinite(xy15[:, p, 0]) & np.isfinite(xy15[:, p, 1])
        k = 0
        while k + lung <= len(t15):
            if ok[k:k + lung].all():
                fuori.append((p, t15[k:k + lung] - t15[k], xy15[k:k + lung, p]))
                k += lung
            else:
                k += 1
    return fuori, n_pre


def prevedi(tt, mis, n_pre, q, sigma):
    r = np.eye(2) * sigma ** 2
    kf = Kalman(mis[0, 0], mis[0, 1], r, 2.5)
    for i in range(1, n_pre):
        kf.predici(tt[i] - tt[i - 1], q)
        kf.aggiorna(mis[i], r)
    return kf.x.copy(), kf.p.copy()


def valuta(fin, n_pre, q, sigma, seme):
    rng = np.random.default_rng(seme)
    righe = []
    for p, tt, vero in fin:
        mis = vero[:n_pre] + rng.normal(0.0, sigma, (n_pre, 2))
        x, pp = prevedi(tt, mis, n_pre, q, sigma)
        x0, p0 = prevedi(tt, mis, n_pre, 0.0, sigma)
        vel = float(np.hypot(*(vero[n_pre - 1] - vero[0])) / (tt[n_pre - 1] - tt[0]))
        riga = {"persona": p, "velocita": vel}
        for h in ORIZZONTI:
            j = n_pre - 1 + int(round(h * HZ))
            tau = tt[j] - tt[n_pre - 1]
            f = transizione(tau)
            for nome, (xa, pa, qa) in (("nucleo", (x, pp, q)), ("retta", (x0, p0, 0.0))):
                m = f @ xa
                c = (f @ pa @ f.T + rumore_processo(tau, qa))[:2, :2]
                e = m[:2] - vero[j]
                riga[f"{nome}_err_{h}"] = float(np.hypot(*e))
                riga[f"{nome}_in90_{h}"] = bool(e @ np.linalg.solve(c, e) <= CHI2_90)
                riga[f"{nome}_in95c_{h}"] = bool(np.hypot(*e) <= math.sqrt(CHI2_95 * max(c[0, 0], c[1, 1])))
                riga[f"{nome}_r95_{h}"] = math.sqrt(CHI2_95 * max(c[0, 0], c[1, 1]))
            riga[f"fermo_err_{h}"] = float(np.hypot(*(mis[n_pre - 1] - vero[j])))
        righe.append(riga)
    return righe


def bootstrap(righe, chiave, rng, n=2000, f=np.mean):
    per = {}
    for r in righe:
        per.setdefault(r["persona"], []).append(float(r[chiave]))
    ids = list(per)
    v = []
    for _ in range(n):
        scelti = rng.choice(len(ids), len(ids))
        v.append(f(np.concatenate([per[ids[i]] for i in scelti])))
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def main():
    fin1, n_pre = finestre("thor_exp1_run1")
    fin3, _ = finestre("thor_exp3_run1")
    rng = np.random.default_rng(20261114)
    ris = {"finestre": {"exp1": len(fin1), "exp3": len(fin3)},
           "persone": {"exp1": len(set(f[0] for f in fin1)), "exp3": len(set(f[0] for f in fin3))}}
    print(f"finestre di {RINCORSA + BUIO:.0f} s: exp1 {len(fin1)} ({ris['persone']['exp1']} persone), exp3 {len(fin3)} "
          f"({ris['persone']['exp3']} persone)")
    print("\n== taratura di q su exp1 (σ = 2 cm): copertura dell'ellisse al 90 % a 1 / 2 / 3 s; scarto medio da 0,90 ==")
    tar = {}
    for q in GRIGLIA_Q:
        r = valuta(fin1, n_pre, q, 0.02, 1)
        cop = [float(np.mean([x[f"nucleo_in90_{h}"] for x in r])) for h in (1.0, 2.0, 3.0)]
        tar[q] = {"copertura": cop, "scarto": float(np.mean([abs(c - 0.9) for c in cop]))}
        print(f"q = {q}: {cop[0]:.3f} / {cop[1]:.3f} / {cop[2]:.3f}; scarto {tar[q]['scarto']:.3f}")
    q_scelto = min(tar, key=lambda q: tar[q]["scarto"])
    ris["taratura"] = {str(q): v for q, v in tar.items()}
    ris["q_scelto"] = q_scelto
    print(f"q scelto su exp1: {q_scelto}")
    print("\n== prova su exp3 (σ = 2 cm) ==")
    ris["prova"] = {}
    for q in sorted(set((0.01, 0.2, q_scelto))):
        for sotto in ("tutti", "in cammino"):
            r = valuta(fin3, n_pre, q, 0.02, 3)
            if sotto == "in cammino":
                r = [x for x in r if x["velocita"] > 0.3]
            riga = {"N": len(r), "persone": len(set(x["persona"] for x in r))}
            testo = [f"q = {q}, {sotto}: N = {len(r)} tratti, {riga['persone']} persone"]
            for h in ORIZZONTI:
                c90 = float(np.mean([x[f"nucleo_in90_{h}"] for x in r]))
                ic = bootstrap(r, f"nucleo_in90_{h}", rng)
                c95 = float(np.mean([x[f"nucleo_in95c_{h}"] for x in r]))
                e = [x[f"nucleo_err_{h}"] for x in r]
                riga[str(h)] = {"copertura90": c90, "ic95": ic, "copertura_cerchio95": c95,
                                "errore_mediano": float(np.median(e)), "errore_p90": float(np.percentile(e, 90)),
                                "ic_errore_mediano": bootstrap(r, f"nucleo_err_{h}", rng, f=np.median),
                                "raggio95_mediano": float(np.median([x[f"nucleo_r95_{h}"] for x in r])),
                                "fermo_mediano": float(np.median([x[f"fermo_err_{h}"] for x in r])),
                                "fermo_p90": float(np.percentile([x[f"fermo_err_{h}"] for x in r], 90)),
                                "retta_mediano": float(np.median([x[f"retta_err_{h}"] for x in r])),
                                "retta_p90": float(np.percentile([x[f"retta_err_{h}"] for x in r], 90)),
                                "retta_copertura90": float(np.mean([x[f"retta_in90_{h}"] for x in r]))}
                v = riga[str(h)]
                testo.append(f"   {h} s: copertura 90 % = {c90:.3f} (IC per persona {ic[0]:.3f}–{ic[1]:.3f}); cerchio 95 % = "
                             f"{c95:.3f}, raggio mediano {v['raggio95_mediano']:.2f} m; errore mediano {v['errore_mediano']:.2f} m "
                             f"(IC {v['ic_errore_mediano'][0]:.2f}–{v['ic_errore_mediano'][1]:.2f}), 90° perc. {v['errore_p90']:.2f}; "
                             f"fermo {v['fermo_mediano']:.2f} (90° {v['fermo_p90']:.2f}); senza rumore di processo "
                             f"{v['retta_mediano']:.2f} (90° {v['retta_p90']:.2f}), sua copertura 90 % {v['retta_copertura90']:.3f}")
            ris["prova"][f"q{q}_{sotto}"] = riga
            print("\n".join(testo))
    print("\n== sensibilità al rumore di misura (exp3, tutti, q = 0,2 e q scelto): copertura 90 % a 1 / 2 / 3 s; errore mediano ==")
    ris["sensibilita"] = {}
    for sigma in (0.005, 0.02, 0.05):
        for q in sorted(set((0.2, q_scelto))):
            r = valuta(fin3, n_pre, q, sigma, 3)
            cop = [float(np.mean([x[f"nucleo_in90_{h}"] for x in r])) for h in (1.0, 2.0, 3.0)]
            er = [float(np.median([x[f"nucleo_err_{h}"] for x in r])) for h in (1.0, 2.0, 3.0)]
            ris["sensibilita"][f"sigma{sigma}_q{q}"] = {"copertura90": cop, "errore_mediano": er}
            print(f"σ = {100 * sigma:.1f} cm, q = {q}: {cop[0]:.3f} / {cop[1]:.3f} / {cop[2]:.3f}; errore {er[0]:.2f} / {er[1]:.2f} / {er[2]:.2f} m")
    with open(os.path.join(K.USCITE, "banco_thor.json"), "w", encoding="utf-8") as f:
        json.dump(ris, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
