#!/usr/bin/env python3
"""A5 — il banco THÖR della validazione rifatto nelle condizioni della catena: rumore del solo dato vero (6 cm),
ultime misure tolte (gruppo «tagliato»), rincorsa corta. Stesse finestre e stesso kalman.py; il resto è mio.
Uso: <python> -I -B a5_thor.py"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import av_comune as A                                          # noqa: E402
sys.path.insert(0, A.VAL)
import numpy as np                                             # noqa: E402
import banco_thor as B                                         # noqa: E402  (sola lettura: uso finestre())
from kalman import Kalman, rumore_processo, transizione        # noqa: E402

HZ = 15.0


def valuta(fin, n_pre, q, sigma, tolte, rincorsa, seme=3, orizzonti=(0.5, 1.0, 2.0, 3.0)):
    rng = np.random.default_rng(seme)
    out = {h: {"err": [], "in90": [], "in95c": [], "r95": []} for h in orizzonti}
    for p, tt, vero in fin:
        mis = vero[:n_pre] + rng.normal(0.0, sigma, (n_pre, 2))
        ultimo = n_pre - 1 - tolte                 # indice dell'ultima misura che aggiorna il filtro
        primo = max(0, ultimo - rincorsa + 1)
        r = np.eye(2) * sigma ** 2
        kf = Kalman(mis[primo, 0], mis[primo, 1], r, 2.5)
        for i in range(primo + 1, ultimo + 1):
            kf.predici(tt[i] - tt[i - 1], q)
            kf.aggiorna(mis[i], r)
        for h in orizzonti:
            j = n_pre - 1 + int(round(h * HZ))     # come la validazione: h dal fotogramma n_pre-1
            tau = tt[j] - tt[ultimo]
            f = transizione(tau)
            m = f @ kf.x
            c = (f @ kf.p @ f.T + rumore_processo(tau, q))[:2, :2]
            e = m[:2] - vero[j]
            out[h]["err"].append(float(np.hypot(*e)))
            out[h]["in90"].append(bool(e @ np.linalg.solve(c, e) <= B.CHI2_90))
            r95 = math.sqrt(B.CHI2_95 * max(c[0, 0], c[1, 1]))
            out[h]["in95c"].append(bool(np.hypot(*e) <= r95))
            out[h]["r95"].append(r95)
    return out


def riga(nome, o):
    t = [nome]
    for h in (1.0, 2.0, 3.0):
        t.append(f"{h:.0f} s: err med {np.median(o[h]['err']):.2f} (p90 {np.percentile(o[h]['err'], 90):.2f}) m, ell90 {np.mean(o[h]['in90']):.3f}, "
                 f"cerchio95 {np.mean(o[h]['in95c']):.3f}, r95 {np.median(o[h]['r95']):.2f} m")
    print(" | ".join(t))


def main():
    for nome in ("thor_exp3_run1", "thor_exp1_run1"):
        fin, n_pre = B.finestre(nome)
        print(f"== {nome}: {len(fin)} finestre, {len(set(f[0] for f in fin))} persone, rincorsa {n_pre} misure ==")
        vel_pre = np.array([np.hypot(*(v[n_pre - 1] - v[0])) / (tt[n_pre - 1] - tt[0]) for _, tt, v in fin])
        vel_buio = np.array([np.hypot(*(v[-1] - v[n_pre - 1])) / (tt[-1] - tt[n_pre - 1]) for _, tt, v in fin])
        cammino = np.array([np.sum(np.hypot(*np.diff(v[n_pre - 1:], axis=0).T)) for _, tt, v in fin])
        lenti = (vel_pre < 0.3)
        si_ferma = (vel_pre > 0.6) & (vel_buio < 0.3)          # cammina e poi (spostamento netto in 3 s) si ferma o torna
        print(f"A5d: finestre con velocità di rincorsa < 0,3 m/s: {int(lenti.sum())} su {len(fin)} ({100 * lenti.mean():.1f} %); "
              f"«cammina (> 0,6) e poi spostamento netto < 0,9 m in 3 s»: {int(si_ferma.sum())} ({100 * si_ferma.mean():.1f} %); "
              f"mediana velocità rincorsa {np.median(vel_pre):.2f} m/s, cammino mediano nel buio {np.median(cammino):.2f} m")
        per = {}
        for p, tt, v in fin:
            per[p] = per.get(p, 0) + 1
        print("     finestre per persona:", dict(sorted(per.items())))
        for q in (0.2, 0.1, 0.05):
            print(f"-- q = {q}")
            riga("  validazione (σ 2 cm, rincorsa 15, 0 tolte)      ", valuta(fin, n_pre, q, 0.02, 0, 15))
            riga("  σ 6 cm, rincorsa 15, 0 tolte                    ", valuta(fin, n_pre, q, 0.06, 0, 15))
            riga("  A5a: σ 6 cm, rincorsa 10, ultime 5 tolte        ", valuta(fin, n_pre, q, 0.06, 5, 10))
            riga("  σ 2 cm, rincorsa 10, ultime 5 tolte             ", valuta(fin, n_pre, q, 0.02, 5, 10))
            riga("  A5b: σ 6 cm, rincorsa 4, 0 tolte                ", valuta(fin, n_pre, q, 0.06, 0, 4))
            riga("  σ 2 cm, rincorsa 4, 0 tolte                     ", valuta(fin, n_pre, q, 0.02, 0, 4))
        # solo chi si ferma: errore del filtro del nucleo
        if si_ferma.sum() >= 3:
            fs = [f for f, s in zip(fin, si_ferma) if s]
            riga(f"-- q = 0,2, solo le {len(fs)} finestre «cammina e poi si ferma» (σ 2 cm)", valuta(fs, n_pre, 0.2, 0.02, 0, 15))


if __name__ == "__main__":
    main()
