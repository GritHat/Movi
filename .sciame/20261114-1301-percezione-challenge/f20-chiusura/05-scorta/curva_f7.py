"""curva_f7.py - curva della confidenza del bersaglio per F7 (sciame-tracciamento). Scrive curva_F7.json (file nuovo).

1. FORMULA (verdetto fase 3, par. 3; piano 2D): sigma^2(tau) = s0^2 + 2 s0v tau + sv^2 tau^2 + q tau^3/3,
   C(tau) = 1 - exp(-g^2 / 2 sigma^2), r_0,9(tau) = 2,146 sigma(tau). Parametri: stato stazionario del filtro del
   tracciatore F7 (velocita' costante, Q = 80 m^2/s^3, misura radar a 250 m con l'accuratezza angolare della config
   piu' l'errore d'assetto INS), calcolato qui con la Riccati. Caso: perdita TOTALE (radar e ottici) dall'istante 0.
   Insieme di presenza fuori modello: r(tau) = r0 + dv tau + a_max tau^2 / 2 (contenimento se |a| <= 10 m/s^2).
2. MISURA (simulato): dai passaggi di valutazione, la quota di cicli con il bersaglio dentro r_0,9 (3D) e dentro la
   regione dichiarata, per tempo dall'evento (l'accecamento ottico e' 0,5-3 s dall'evento).
"""
import json
import math
import os
import sys

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import scorta_f7 as S  # noqa: E402


def stazionario(cfg, D=250.0):
    rc = S.CFG[cfg]["radar"]
    T = rc["periodo"]
    sa = math.hypot(rc["s_a"], S.INS["s_att0"] * 2)
    r = (D * sa) ** 2 + (S.INS["s_p0"] * 2) ** 2           # per asse trasversale (prudente: uso il trasversale)
    F = np.array([[1, T], [0, 1]])
    Q = S.Q_TR * np.array([[T ** 3 / 3, T ** 2 / 2], [T ** 2 / 2, T]])
    P = np.eye(2) * 100
    for _ in range(2000):
        P = F @ P @ F.T + Q
        K = P[:, 0] / (P[0, 0] + r)
        P = P - np.outer(K, P[0, :])
    return math.sqrt(P[0, 0]), P[0, 1], math.sqrt(P[1, 1])


def curva(cfg):
    s0, c01, sv = stazionario(cfg)
    q, g = S.Q_TR, S.GPORTA
    righe = []
    for tau in [0, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]:
        s2 = s0 * s0 + 2 * c01 * tau + sv * sv * tau * tau + q * tau ** 3 / 3
        C = 1 - math.exp(-g * g / (2 * s2))
        r09 = 2.146 * math.sqrt(s2)
        rinv = 4.59 * s0 + 3 * sv * tau + 0.5 * S.A_MAX_INV * tau * tau
        righe.append({"tau_s": tau, "C": round(C, 4), "r09_m": round(r09, 1), "insieme_presenza_r_m": round(rinv, 1)})
    # tempo in cui C scende sotto 0,9 (bisezione)
    a, b = 0.0, 30.0
    f = lambda t: 1 - math.exp(-g * g / (2 * (s0 * s0 + 2 * c01 * t + sv * sv * t * t + q * t ** 3 / 3)))
    for _ in range(60):
        m = (a + b) / 2
        a, b = (m, b) if f(m) > 0.9 else (a, m)
    return {"parametri": {"s0_m": round(s0, 2), "s0v_m2_s": round(c01, 3), "sv_m_s": round(sv, 2), "q_m2_s3": q, "porta_g_m": g},
            "t_C_sotto_0_9_s": round(b, 2), "tabella": righe}


def misura(perc):
    out = {}
    for l in open(perc, encoding="utf-8"):
        r = json.loads(l)
        if r["var"] == "F7c":
            continue
        for (dt_ev, tau, in90, inreg) in r["curva"]:
            if dt_ev > 5.0:
                continue
            k = (r["cfg"], round(math.floor(dt_ev * 2) / 2, 1))
            a = out.setdefault(k, [0, 0, 0, 0.0])
            a[0] += in90
            a[1] += inreg
            a[2] += 1
            a[3] = max(a[3], tau)
    res = {}
    for (cfg, t0), (a90, areg, n, taumax) in sorted(out.items()):
        res.setdefault(cfg, []).append({"t_dall_evento_s": [t0, t0 + 0.5], "dentro_r09": [a90, n, round(a90 / n, 4)],
                                        "dentro_regione_dichiarata": [areg, n], "tau_max_s": taumax,
                                        "nota": "cicli correlati dentro un passaggio: la quota non ha un intervallo per ciclo"})
    return res


if __name__ == "__main__":
    perc = os.path.join(QUI, "passaggi_valutazione.jsonl")
    J = {"stato": "formula: dimostrata nel modello (verdetto fase 3, par. 3); parametri: calcolati dalla Riccati del "
                  "tracciatore F7 (ipotesi sui sensori); misura: simulata (passaggi di valutazione F7, semi 20261121)",
         "uso_nel_video": "curva 'perdita totale' = che cosa dichiara MoVi SE perdesse anche il radar; nel simulato il radar "
                          "di bordo non e' accecato dalla fiammata e la C misurata resta alta durante l'accecamento ottico",
         "formula": "sigma^2(tau) = s0^2 + 2 s0v tau + sv^2 tau^2 + q tau^3/3; C = 1 - exp(-g^2/2 sigma^2); r_0,9 = 2,146 sigma",
         "perdita_totale": {c: curva(c) for c in ("att", "sda")},
         "misura_durante_accecamento": misura(perc) if os.path.exists(perc) else None}
    with open(os.path.join(QUI, "curva_F7.json"), "x", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1)
    print(json.dumps(J["perdita_totale"], ensure_ascii=False)[:3000])
