#!/usr/bin/env python3
"""Genera le traiettorie per cont.c (sciame-tracciamento, f8). Python puro, semi fissati.
Uso: python3 gen_traj.py <w> <yp> <rmax> <yped> <n> <seme> > file
prosegue, sosta, torna, lontano: truth() dell'AVVERSARIO (scena_parte3.py, copiato senza modifiche).
rallenta, svolta, sostalunga: generatore MIO (dichiarato), stessa partenza e stessa velocita'.
Formato: riga 'T <ibeh> <w> <yped> <n>' poi n righe 'x y'.
"""
import math, random, sys
import scena_parte3 as sp

BEH = ['prosegue', 'sosta', 'torna', 'lontano', 'rallenta', 'svolta', 'sostalunga']
DT = sp.DT


def mia(beh, w, rng, yped):
    W = w / 2 * yped / sp.YP
    v = rng.uniform(1.0, 1.5); x, y = -3.7 * yped / 4, yped; hx, hy = 1.0, 0.0
    xs = rng.uniform(-W + 0.05, W - 0.05) if beh != 'svolta' else rng.uniform(-W + 0.3, W - 0.3)
    dwell = rng.uniform(6, 10); vlow = rng.uniform(0.2, 0.5)
    ang = rng.choice((-1, 1)) * rng.uniform(math.pi / 4, math.pi / 2)
    ph = 0; out = []; sp_now = v
    for k in range(int(14 / DT)):
        out.append((x, y))
        if ph == 0 and x >= xs:
            ph = 1
            if beh == 'svolta': hx, hy = math.cos(ang), math.sin(ang)
        if beh == 'sostalunga' and ph == 1:
            dwell -= DT
            if dwell <= 0: ph = 2
            continue
        if beh == 'rallenta' and ph == 1:
            sp_now = max(vlow, sp_now - (v - vlow) * DT / 0.5)   # rampa di 0,5 s
        if beh == 'svolta' and ph == 1:
            if math.hypot(x, y) > sp.RMAX + 0.5: continue        # uscito oltre la portata: resta li'
            if y + hy * sp_now * DT < sp.YP + 0.3: continue       # arrivato dietro il pannello: si ferma
        x += hx * sp_now * DT; y += hy * sp_now * DT
        if abs(x) > 4.3 * yped / 4: break
    return out


if __name__ == '__main__':
    w = float(sys.argv[1]); sp.YP = float(sys.argv[2]); sp.RMAX = float(sys.argv[3]); yped = float(sys.argv[4])
    n = int(sys.argv[5]); seed = int(sys.argv[6])
    for bi, beh in enumerate(BEH):
        rng = random.Random(seed + bi)
        for _ in range(n):
            tr = sp.truth(beh, w, rng, None, yped) if bi < 4 else mia(beh, w, rng, yped)
            print('T %d %.3f %.3f %d' % (bi, w, yped, len(tr)))
            for x, y in tr: print('%.4f %.4f' % (x, y))
