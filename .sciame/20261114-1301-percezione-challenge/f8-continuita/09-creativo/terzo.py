#!/usr/bin/env python3
"""sciame-creativo, f8: falsificatore del terzo generatore per «fronte + scia».
Uso: PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 terzo.py
traiettoria(): COPIA dal rovesciatore (f2/04-torneo/torneo_parte2.py), con due aggiunte mie: manovra forzata e passo = 1/15 s."""
import math, sys
import cono2
T3 = cono2.DT; PAN_Y, PAN_HALF, RANGE_MAX, Y_T = 2.0, 0.75, 6.0, 4.0; K3 = PAN_HALF / PAN_Y
def in_ombra(x, y): return y > PAN_Y and abs(x) <= K3 * y
def traiettoria(rnd, forza=None):
    v = min(1.8, max(0.8, rnd.gauss(1.3, 0.2)))
    x, y, vx = -4.0, Y_T, v
    u = rnd.random()
    manovra = "prosegue" if u < 0.60 else ("sosta" if u < 0.85 else "torna")
    if forza: manovra = forza
    x_man = rnd.uniform(-1.2, 1.2)
    sosta = rnd.uniform(2.0, 6.0)
    fatto, fermo_fino = False, -1.0
    out, t, vis_dopo = [], 0.0, 0.0
    entrato = False
    while t < 20.0:
        out.append((t, x, y))
        if in_ombra(x, y):
            entrato = True
        elif entrato:
            vis_dopo += T3
            if vis_dopo > 1.0:
                break
        if not fatto and x >= x_man:
            fatto = True
            if manovra == "sosta":
                fermo_fino = t + sosta
            elif manovra == "torna":
                vx = -v
        if t < fermo_fino:
            cur = 0.0
        else:
            vx += rnd.gauss(0, 0.1) * T3
            cur = vx
        x += cur * T3
        t += T3
    return out, manovra
cono2.truth = lambda beh, w, rng, *a, **k: [(x, y) for t, x, y in traiettoria(rng, beh)[0]]
sys.argv = ['cono2.py', '1.5', 'prosegue,sosta,torna', '100', '0.0', 'AB']
print('# terzo.py: generatore del rovesciatore, pannello 1,5 m, scenari fronte + scia')
cono2.main()
