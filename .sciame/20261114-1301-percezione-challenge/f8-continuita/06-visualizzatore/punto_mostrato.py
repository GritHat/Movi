#!/usr/bin/env python3
"""Quale «posizione più probabile» disegnare durante l'occlusione (sciame-visualizzatore, f8).

Modello mio, deterministico (nessun rumore, nessun seme): sensore in (0,0) che guarda lungo +y,
pannello largo 1 m a y = yp, persona sulla retta y = yd da sinistra a destra.
Filtro a velocità costante in SOLA previsione dall'ingresso in ombra: per asse
  var(t) = P0_pos + P0_vel * t^2 + q * t^3 / 3   (q = 0,2 m^2/s^3), cerchio al 95 %: r = sqrt(5,991 * var).
Candidati per il punto mostrato: (a) media del filtro; (b) media proiettata sul cuneo;
(c) baricentro della gaussiana troncata al cuneo d'ombra (celle di 5 cm).
Rifare: timeout 120 python3 punto_mostrato.py
"""
import math

Q = 0.2
P0_POS = 0.05 ** 2      # scelta mia: 5 cm sulla posizione all'ingresso
P0_VEL = 0.15 ** 2      # scelta mia: 0,15 m/s sulla velocità all'ingresso
DT = 1.0 / 15.0
CELL = 0.05
CHI2_95 = 5.991
HALF_FOV = math.radians(43.5)
SOSTA = 3.0

GEOM = {
    "T (torneo: pannello a 2 m, persona a 4 m, portata 6 m)": dict(yp=2.0, yd=4.0, R=6.0),
    "D (demo: pannello a 1,9 m, persona a 2,3 m, griglia a 3 m)": dict(yp=1.9, yd=2.3, R=3.0),
}


def in_wedge(x, y, g):
    if y <= g["yp"] or x * x + y * y > g["R"] ** 2:
        return False
    return abs(x * g["yp"] / y) <= 0.5


def seen_free(x, y, g):
    """In campo, entro la portata, non in ombra, non dietro il sensore."""
    if y <= 0 or x * x + y * y > g["R"] ** 2:
        return False
    if abs(math.atan2(x, y)) > HALF_FOV:
        return False
    return not in_wedge(x, y, g)


def wedge_cells(g):
    cells = []
    n = int(g["R"] / CELL) + 1
    for i in range(-n, n + 1):
        for j in range(0, n + 1):
            x, y = (i + 0.5) * CELL, (j + 0.5) * CELL
            if in_wedge(x, y, g):
                cells.append((x, y))
    return cells


def var(t):
    return P0_POS + P0_VEL * t * t + Q * t ** 3 / 3.0


def dist_to_side(x, y, g):
    """Distanza dal più vicino dei due raggi laterali del cuneo (il bordo oltre il quale si vede)."""
    d = []
    for sx in (-0.5, 0.5):
        nrm = math.hypot(sx, g["yp"])
        ux, uy = sx / nrm, g["yp"] / nrm
        d.append(abs(x * uy - y * ux))
    return min(d)


def truth(t, v, f, g):
    """Persona: entra in ombra a t = 0, si ferma alla frazione f della larghezza per SOSTA s, poi prosegue."""
    w = g["yd"] / g["yp"]          # larghezza dell'ombra alla distanza della persona
    x_in = -0.5 * w
    if f is None:
        return x_in + v * t, w / v
    t1 = f * w / v
    t_exit = w / v + SOSTA
    if t <= t1:
        return x_in + v * t, t_exit
    if t <= t1 + SOSTA:
        return x_in + f * w, t_exit
    return x_in + f * w + v * (t - t1 - SOSTA), t_exit


def run(gname, g, v, f, cells):
    area_w = len(cells) * CELL * CELL
    w = g["yd"] / g["yp"]
    x_in = -0.5 * w
    _, t_exit = truth(0.0, v, f, g)
    n = int(round(t_exit / DT))
    res = dict(n=n, a_free=0, b_edge=0, c_free=0, c_maxstep=0.0, c_back=0.0,
               core_shown=0, t_prev=None)
    prev_c = None
    core_alive = True
    err3 = None
    last_core_pt = (x_in, g["yd"])
    c = None
    for k in range(1, n + 1):
        t = k * DT
        xt, _ = truth(t, v, f, g)
        mx, my = x_in + v * t, g["yd"]
        s2 = var(t)
        r95sq = CHI2_95 * s2
        # (a)
        if seen_free(mx, my, g):
            res["a_free"] += 1
        # (b) e (c) e area del cerchio ritagliato
        best, bd = None, 1e9
        sw = sx = sy = 0.0
        inside = 0
        for (cx, cy) in cells:
            d2 = (cx - mx) ** 2 + (cy - my) ** 2
            if d2 < bd:
                bd, best = d2, (cx, cy)
            if d2 <= r95sq:
                inside += 1
            wgt = math.exp(-0.5 * d2 / s2)
            sw += wgt
            sx += wgt * cx
            sy += wgt * cy
        b = best
        if dist_to_side(b[0], b[1], g) < 0.10:
            res["b_edge"] += 1
        c = (sx / sw, sy / sw) if sw > 0 else b
        if seen_free(c[0], c[1], g):
            res["c_free"] += 1
        if prev_c is not None:
            step = math.hypot(c[0] - prev_c[0], c[1] - prev_c[1])
            res["c_maxstep"] = max(res["c_maxstep"], step)
            res["c_back"] = max(res["c_back"], prev_c[0] - c[0])
        prev_c = c
        # regola del nucleo: «previsto» finché il cerchio ritagliato copre meno di metà del cuneo; poi «perso» assorbente
        if core_alive and inside * CELL * CELL < 0.5 * area_w:
            res["core_shown"] += 1
            res["t_prev"] = t
            last_core_pt = (mx, my) if in_wedge(mx, my, g) else b
        else:
            core_alive = False
        if err3 is None and t >= 3.0 - 1e-9:
            err3 = dict(a=math.hypot(mx - xt, 0.0), b=math.hypot(b[0] - xt, b[1] - g["yd"]),
                        c=math.hypot(c[0] - xt, c[1] - g["yd"]), fermo=abs(x_in - xt),
                        r95=math.sqrt(r95sq))
    res["err3"] = err3
    x_out = 0.5 * w
    res["salto_nucleo"] = math.hypot(last_core_pt[0] - x_out, last_core_pt[1] - g["yd"])
    res["salto_c"] = math.hypot(c[0] - x_out, c[1] - g["yd"])
    res["sigma_fine"] = math.sqrt(var(n * DT))
    res["t_exit"] = t_exit
    res["area_w"] = area_w
    return res


def main():
    for gname, g in GEOM.items():
        cells = wedge_cells(g)
        print("=" * 100)
        print("Geometria", gname, "| area del cuneo %.2f m2 | larghezza dell'ombra alla persona %.2f m"
              % (len(cells) * CELL * CELL, g["yd"] / g["yp"]))
        print("\n-- Scena «si ferma dietro» (sosta di 3 s) --")
        print("v     f    cicli | (a) su libero % | (b) sul bordo % | (c) su libero | (c) passo max cm (2vdt) | (c) indietro max cm |"
              " nucleo: cicli con regione % (previsto fino a s) | errore a 3 s: a / b / c / fermo (m) ; r95")
        acc = dict(a=0.0, b=0.0, core=0.0, ea=0.0, eb=0.0, ec=0.0, ef=0.0, m=0)
        viol = 0
        for v in (1.0, 1.25, 1.5):
            for f in (0.25, 0.5, 0.75):
                r = run(gname, g, v, f, cells)
                n = r["n"]
                e = r["err3"]
                lim = 2 * v * DT
                bad = (r["c_free"] > 0) or (r["c_maxstep"] > lim) or (r["c_back"] > 0.05)
                viol += bad
                print("%.2f  %.2f  %3d   | %5.1f           | %5.1f           | %3d           | %5.1f (%4.1f) %s        | %5.1f               |"
                      " %5.1f (%.2f)                              | %.2f / %.2f / %.2f / %.2f ; %.2f"
                      % (v, f, n, 100.0 * r["a_free"] / n, 100.0 * r["b_edge"] / n, r["c_free"],
                         100 * r["c_maxstep"], 100 * lim, "VIOLA" if r["c_maxstep"] > lim else "ok   ",
                         100 * r["c_back"], 100.0 * r["core_shown"] / n, r["t_prev"] or 0.0,
                         e["a"], e["b"], e["c"], e["fermo"], e["r95"]))
                acc["a"] += 100.0 * r["a_free"] / n
                acc["b"] += 100.0 * r["b_edge"] / n
                acc["core"] += 100.0 * r["core_shown"] / n
                acc["ea"] += e["a"]; acc["eb"] += e["b"]; acc["ec"] += e["c"]; acc["ef"] += e["fermo"]
                acc["m"] += 1
        m = acc["m"]
        print("MEDIE dei 9 casi: (a) su libero %.1f %% | (b) sul bordo %.1f %% | nucleo: cicli con regione %.1f %% |"
              " errore a 3 s a/b/c/fermo: %.2f / %.2f / %.2f / %.2f m | casi che violano PV-1c: %d su %d"
              % (acc["a"] / m, acc["b"] / m, acc["core"] / m, acc["ea"] / m, acc["eb"] / m, acc["ec"] / m,
                 acc["ef"] / m, viol, m))
        print("\n-- Scena «prosegue» (nessuna sosta) --")
        print("v     buio s | nucleo: previsto fino a s, cicli con regione % | salto alla ricomparsa: nucleo m | (c) m | sigma per asse alla ricomparsa m | r95 m")
        for v in (1.0, 1.25, 1.5):
            r = run(gname, g, v, None, cells)
            print("%.2f  %.2f   | %.2f, %5.1f                                 | %.2f                           | %.2f  | %.2f                             | %.2f"
                  % (v, r["t_exit"], r["t_prev"] or 0.0, 100.0 * r["core_shown"] / r["n"],
                     r["salto_nucleo"], r["salto_c"], r["sigma_fine"], math.sqrt(CHI2_95) * r["sigma_fine"]))


if __name__ == "__main__":
    main()
