# AV10 — proposta avversario-4: «quota verificata per cella». Rifare: timeout 120 python3 -I av10.py > risultati_av10.txt
import random, math, sys, os, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim import *

QS = (0.2, 0.6, 1.0, 1.4, 1.8)


def cella_av4(Ds, occ, r0, a, r, k):
    if occ[a][r] >= 3 or r > r0[a]:
        return None
    qv = None
    for q in QS:
        if stato(Ds, centro_cella(a, r, q), k) != LIBERO:
            break
        qv = q
    return qv


def prova(nome, boxes, room, zmax, k, seme, ostacoli):
    """ostacoli: lista di (x0,x1,y0,y1,zbasso) = pianta e quota inferiore dell'ostacolo vero."""
    clean, ID = render(boxes, 15.0, zmax, room)
    rng = random.Random(seme)
    fr = [rumoroso(clean, ID, k, rng) for _ in range(12)]
    falsi = tot = lib = 0
    qv2, qv3 = [], []
    for t in range(2, 12):
        Ds = [fr[t], fr[t - 1], fr[t - 2]]
        occ, suo, r0 = griglia_pixel(fr[t])
        for a in range(NA):
            for r in range(13, NR):
                if stato(Ds, centro_cella(a, r, 0.2), k) == FUORI:
                    continue
                x, y, _ = centro_cella(a, r, 0)
                sotto = [o for o in ostacoli if o[0] <= x <= o[1] and o[2] <= y <= o[3]]
                if not sotto:
                    tot += 1
                qv = cella_av4(Ds, occ, r0, a, r, k)
                if qv is None:
                    continue
                if not sotto:
                    lib += 1
                    if abs(x) < 0.3 and 1.9 <= y <= 2.1:
                        qv2.append(qv)
                    if abs(x) < 0.3 and 2.8 <= y <= 3.0:
                        qv3.append(qv)
                elif any(qv >= o[4] for o in sotto):
                    falsi += 1
    print("%-34s k=%.4f | celle libere con un ostacolo nella colonna sotto la quota verificata: %d in 10 fot. | resa del libero %.1f %% | q_v mediana a 2 m %s, a 3 m %s" % (
        nome, k, falsi, 100.0 * lib / tot, statistics.median(qv2) if qv2 else "-", statistics.median(qv3) if qv3 else "-"))


for k in (0.004, 0.0100):
    prova("stanza vuota", [], True, 6.0, k, 1, [])
    prova("barra 1,40-1,50 a 2,0-2,1 m", [(-0.6, 0.6, 2.0, 2.1, 1.40, 1.50)], True, 6.0, k, 2, [(-0.6, 0.6, 2.0, 2.1, 1.40)])
    prova("barra sottile 1,15-1,25", [(-0.6, 0.6, 2.0, 2.1, 1.15, 1.25)], True, 6.0, k, 3, [(-0.6, 0.6, 2.0, 2.1, 1.15)])
    prova("tubo 3 cm a 1,20 m di quota", [(-0.6, 0.6, 2.0, 2.03, 1.20, 1.23)], True, 6.0, k, 4, [(-0.6, 0.6, 2.0, 2.03, 1.20)])
    prova("scatola 0,25 m", [(-0.2, 0.2, 2.0, 2.3, 0.0, 0.25)], True, 6.0, k, 5, [(-0.2, 0.2, 2.0, 2.3, 0.0)])
    prova("scatola 0,10 m", [(-0.2, 0.2, 2.0, 2.3, 0.0, 0.10)], True, 6.0, k, 6, [(-0.2, 0.2, 2.0, 2.3, 0.0)])
    prova("senza fondale, portata 6 m", [], False, 6.0, k, 7, [])
    prova("senza fondale, portata 10 m", [], False, 10.0, k, 8, [])
