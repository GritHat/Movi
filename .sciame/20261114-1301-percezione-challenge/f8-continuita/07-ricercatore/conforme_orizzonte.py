#!/usr/bin/env python3
"""Falsificatore di ricercatore-1 (f8, continuita' visiva).

Domanda: un raggio tarato in modo conforme (split conformal) PER TEMPO SENZA OSSERVAZIONE sui residui di un
predittore a velocita' costante da' la copertura nominale in media? E per comportamento?

Python puro, semi fissati. Rifare:
  timeout 120 python3 -I conforme_orizzonte.py > risultati_conforme.txt

Indipendenza dichiarata: generatore e predittore sono dello stesso autore (ricercatore); niente in comune con il
filtro del nucleo ne' con i generatori del torneo. Vale come prova del MECCANISMO (marginale contro condizionata),
non come misura sui pedoni veri.
"""
import math
import random

DT = 1.0 / 15.0
TAUS = [0.5, 1.0, 2.0, 3.0, 5.0]
STEPS = {t: round(t / DT) for t in TAUS}
NMAX = max(STEPS.values())
SIGMA_Z = 0.03        # rumore di misura per asse, m
Q_TRUE = 0.02         # densita' del rumore di velocita' del generatore, m^2/s^3
A_MAX = 2.0           # accelerazione massima nei cambi, m/s^2
BEH = ["prosegue", "rallenta", "si_ferma", "torna", "svolta"]
MIX_CAL = [0.60, 0.10, 0.10, 0.10, 0.10]
MIX_SHIFT = [0.40, 0.10, 0.10, 0.30, 0.10]


def traiettoria(rng, beh):
    """Restituisce (stima p0, stima v, posizioni vere ai TAUS)."""
    v0 = rng.uniform(0.6, 1.8)
    # storia visibile: 1 s a 15 Hz, moto rettilineo lungo x
    ts = [-(15 - i) * DT for i in range(16)]
    zx = [v0 * t + rng.gauss(0, SIGMA_Z) for t in ts]
    zy = [rng.gauss(0, SIGMA_Z) for _ in ts]
    n = len(ts)
    mt = sum(ts) / n
    stt = sum((t - mt) ** 2 for t in ts)
    mx = sum(zx) / n
    my = sum(zy) / n
    vx = sum((t - mt) * (x - mx) for t, x in zip(ts, zx)) / stt
    vy = sum((t - mt) * (y - my) for t, y in zip(ts, zy)) / stt
    p0x = mx - vx * mt
    p0y = my - vy * mt
    # futuro nascosto
    tc = rng.uniform(0.2, 1.0)
    if beh == "prosegue":
        tgt = (v0, 0.0)
        tc = 1e9
    elif beh == "rallenta":
        k = rng.uniform(0.3, 0.7)
        tgt = (k * v0, 0.0)
    elif beh == "si_ferma":
        tgt = (0.0, 0.0)
    elif beh == "torna":
        k = rng.uniform(0.8, 1.1)
        tgt = (-k * v0, 0.0)
    else:  # svolta
        a = math.radians(rng.uniform(45, 100)) * rng.choice((-1, 1))
        tgt = (v0 * math.cos(a), v0 * math.sin(a))
    x = y = 0.0
    cx, cy = v0, 0.0            # velocita' comandata (segue il bersaglio con A_MAX)
    nx = ny = 0.0               # perturbazione a cammino casuale
    sq = math.sqrt(Q_TRUE * DT)
    out = {}
    inv = {s: t for t, s in STEPS.items()}
    for i in range(1, NMAX + 1):
        t = i * DT
        if t >= tc:
            dx, dy = tgt[0] - cx, tgt[1] - cy
            d = math.hypot(dx, dy)
            m = A_MAX * DT
            if d <= m:
                cx, cy = tgt
            else:
                cx += dx / d * m
                cy += dy / d * m
        if beh != "si_ferma" or t < tc:
            nx += rng.gauss(0, sq)
            ny += rng.gauss(0, sq)
        elif math.hypot(cx, cy) == 0.0:
            nx = ny = 0.0       # chi e' fermo resta fermo
        x += (cx + nx) * DT
        y += (cy + ny) * DT
        if i in inv:
            out[inv[i]] = (x, y)
    return (p0x, p0y), (vx, vy), out


def insieme(seed, n, mix):
    rng = random.Random(seed)
    dati = []
    for _ in range(n):
        beh = rng.choices(BEH, weights=mix)[0]
        p0, v, fut = traiettoria(rng, beh)
        r_cv = {}
        r_fermo = {}
        for t in TAUS:
            px, py = fut[t]
            r_cv[t] = math.hypot(px - (p0[0] + v[0] * t), py - (p0[1] + v[1] * t))
            r_fermo[t] = math.hypot(px - p0[0], py - p0[1])
        dati.append((beh, r_cv, r_fermo))
    return dati


def quantile_conforme(vals, alpha):
    """Quantile split-conformal: il ceil((n+1)(1-alpha))-esimo piu' piccolo."""
    s = sorted(vals)
    n = len(s)
    k = math.ceil((n + 1) * (1 - alpha))
    return s[min(k, n) - 1]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (p, c - h, c + h)


def copertura(dati, raggio, t, beh=None):
    sel = [d for d in dati if beh is None or d[0] == beh]
    k = sum(1 for d in sel if d[1][t] <= raggio)
    return wilson(k, len(sel))


def main():
    cal = insieme(20261114, 4000, MIX_CAL)
    test = insieme(8242026, 40000, MIX_CAL)
    shift = insieme(771, 40000, MIX_SHIFT)
    print("N taratura", len(cal), "N prova", len(test), "N prova con miscela spostata", len(shift))
    print("miscela taratura/prova", dict(zip(BEH, MIX_CAL)), "| spostata", dict(zip(BEH, MIX_SHIFT)))
    print()
    print("== Efficacia: errore medio (m) del predittore a velocita' costante contro 'fermo all'ultima posizione' ==")
    for t in TAUS:
        m_cv = sum(d[1][t] for d in test) / len(test)
        m_f = sum(d[2][t] for d in test) / len(test)
        riga = f"tau={t:>3} s  CV medio {m_cv:5.2f}  fermo medio {m_f:5.2f}"
        for b in BEH:
            sel = [d for d in test if d[0] == b]
            riga += f" | {b}: CV {sum(d[1][t] for d in sel)/len(sel):4.2f} fermo {sum(d[2][t] for d in sel)/len(sel):4.2f}"
        print(riga)
    for alpha in (0.10, 0.50):
        liv = 1 - alpha
        print()
        print(f"== Livello {liv:.2f} ==")
        for t in TAUS:
            q_marg = quantile_conforme([d[1][t] for d in cal], alpha)
            q_beh = {b: quantile_conforme([d[1][t] for d in cal if d[0] == b], alpha) for b in BEH}
            q_peggiore = max(q_beh.values())
            sigma_kf = math.sqrt(0.2 * t ** 3 / 3.0)
            r_kf = sigma_kf * math.sqrt(-2.0 * math.log(alpha))
            print(f"tau={t} s: raggio marginale {q_marg:.2f} m; raggio 'comportamento peggiore' {q_peggiore:.2f} m "
                  f"(x{q_peggiore/q_marg:.2f}); raggio nominale Kalman q=0,2 (solo q*tau^3/3) {r_kf:.2f} m")
            p, lo, hi = copertura(test, q_marg, t)
            print(f"   marginale, prova:            {p:.3f} [{lo:.3f}, {hi:.3f}]")
            print("   marginale, per comportamento: " + "  ".join(
                f"{b} {copertura(test, q_marg, t, b)[0]:.3f}" for b in BEH))
            p, lo, hi = copertura(test, q_peggiore, t)
            print(f"   peggiore, prova:             {p:.3f} [{lo:.3f}, {hi:.3f}]")
            print("   peggiore, per comportamento:  " + "  ".join(
                f"{b} {copertura(test, q_peggiore, t, b)[0]:.3f}" for b in BEH))
            print("   Kalman nominale, per comportamento: " + "  ".join(
                f"{b} {copertura(test, r_kf, t, b)[0]:.3f}" for b in BEH)
                + f"  | tutti {copertura(test, r_kf, t)[0]:.3f}")
            p, lo, hi = copertura(shift, q_marg, t)
            p2, lo2, hi2 = copertura(shift, q_peggiore, t)
            print(f"   miscela spostata: marginale {p:.3f} [{lo:.3f}, {hi:.3f}]; peggiore {p2:.3f} [{lo2:.3f}, {hi2:.3f}]")


if __name__ == "__main__":
    main()
