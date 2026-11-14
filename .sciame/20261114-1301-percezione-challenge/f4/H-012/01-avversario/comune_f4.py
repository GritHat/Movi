# Modulo comune delle controprove f4 (avversario). Python puro, nessun codice degli autori.
import math, random

DT = 1 / 15
SIG = 0.05
Q = 0.2
PD = 0.9
FOV = math.radians(43.5)
RMAX = 3.0
RNEAR = 1.2 / math.tan(math.radians(44))  # primo suolo visto: 1,2 m, 15 gradi in basso, 58 gradi verticali
CHI95 = 5.991
CHI99 = 9.210
THR = 5 * SIG * math.sqrt(2)  # soglia della regola "mobile": 0,354 m
SEME = 20261114


class KF1:
    """Un asse del Kalman a velocita' quasi costante (gli assi sono disaccoppiati e hanno la stessa P)."""

    def __init__(s, p, R=SIG ** 2):
        s.x = [p, 0.0]
        s.P = [[R, 0.0], [0.0, 4.0]]

    def pred(s, dt=DT):
        p, v = s.x
        s.x = [p + v * dt, v]
        a, b, c, d = s.P[0][0], s.P[0][1], s.P[1][0], s.P[1][1]
        a2 = a + dt * (b + c) + dt * dt * d
        b2 = b + dt * d
        c2 = c + dt * d
        s.P = [[a2 + Q * dt ** 3 / 3, b2 + Q * dt ** 2 / 2], [c2 + Q * dt ** 2 / 2, d + Q * dt]]

    def upd(s, z, R=SIG ** 2):
        S = s.P[0][0] + R
        k0 = s.P[0][0] / S
        k1 = s.P[1][0] / S
        y = z - s.x[0]
        s.x = [s.x[0] + k0 * y, s.x[1] + k1 * y]
        a, b, c, d = s.P[0][0], s.P[0][1], s.P[1][0], s.P[1][1]
        s.P = [[(1 - k0) * a, (1 - k0) * b], [c - k1 * a, d - k1 * b]]


def osservabile(px, pz, hs, zp, rmax=RMAX):
    """Vero se il punto al suolo e' in una cella che puo' essere 'libero osservato'."""
    r = math.hypot(px, pz)
    if pz <= 0 or r < RNEAR or r > rmax:
        return False
    b = abs(math.atan2(px, pz))
    if b > FOV:
        return False
    if b <= hs and r > zp:
        return False
    return True


def in_ombra_griglia(px, pz, hs, zp, rmax=RMAX):
    r = math.hypot(px, pz)
    return pz > 0 and zp < r <= rmax and abs(math.atan2(px, pz)) <= hs


def disco(cx, cz, rc, n=300):
    for i in range(n):
        rr = rc * math.sqrt((i + 0.5) / n)
        a = i * 2.399963229728653
        yield cx + rr * math.cos(a), cz + rr * math.sin(a)


def transito(rng, z, wp=0.5, zp=1.5, body=0.4, pd=PD, v=None, rmax=RMAX, npt=300, wmin=0.1):
    """Un attore attraversa sulla retta a profondita' z, da sinistra a destra, dietro un pannello largo wp a zp."""
    if v is None:
        v = min(1.6, max(0.8, rng.gauss(1.2, 0.15)))
    hs = math.atan((wp / 2) / zp)
    A_sh = hs * (rmax ** 2 - zp ** 2)
    x0 = -2.6
    nf = int(5.2 / v / DT) + 1
    dets, truth = [], []
    for k in range(nf):
        xc = x0 + v * k * DT
        xs = [xc - body / 2 + body * i / 20 for i in range(21)] if body > 0 else [xc]
        vis = [x for x in xs if hs < abs(math.atan2(x, z)) <= FOV]
        w = body * len(vis) / 21 if body > 0 else (1.0 if vis else 0.0)
        det = None
        if vis and w >= wmin and rng.random() < pd:
            mx = sum(vis) / len(vis) + rng.gauss(0, SIG)
            mz = z + rng.gauss(0, SIG)
            if math.hypot(mx, mz) <= rmax:
                det = (mx, mz)
        dets.append(det)
        truth.append(xc)
    k0 = next(k for k in range(nf) if truth[k] >= 0)
    out = dict(v=v, npre=0, traccia=False, conf=False, mob_c=False, mob_f=False, riemerge=False,
               buio=None, vivo1=None, vivo2=None, tend1=None, tend2=None, cont=None)
    if dets[k0] is not None:
        return out
    s = k0
    while s > 0 and dets[s - 1] is None:
        s -= 1
    e = k0
    while e < nf - 1 and dets[e + 1] is None:
        e += 1
    kx = kz = None
    hits, storia = [], []
    for k in range(s):
        d = dets[k]
        if kx is None:
            if d is None:
                continue
            kx, kz = KF1(d[0]), KF1(d[1])
            hits.append(1)
            storia.append((k, d))
            continue
        kx.pred(); kz.pred()
        hits.append(1 if d else 0)
        if d:
            kx.upd(d[0]); kz.upd(d[1])
            for (j, dj) in storia:
                if k - j <= 15 and (abs(d[0] - dj[0]) > THR or abs(d[1] - dj[1]) > THR):
                    out['mob_c'] = True
                    if k - j == 15:
                        out['mob_f'] = True
            storia.append((k, d))
        if sum(hits[-5:]) >= 3:
            out['conf'] = True
    out['npre'] = sum(1 for k in range(s) if dets[k])
    if kx is None:
        return out
    out['traccia'] = True
    t1 = t2 = None
    for k in range(s, e + 1):
        kx.pred(); kz.pred()
        rc = math.sqrt(CHI95 * kx.P[0][0])
        n1 = n2 = 0
        for (px, pz) in disco(kx.x[0], kz.x[0], rc, npt):
            if in_ombra_griglia(px, pz, hs, zp, rmax):
                n1 += 1
            if not osservabile(px, pz, hs, zp, rmax):
                n2 += 1
        area = math.pi * rc * rc
        if t1 is None and area * n1 / npt >= 0.5 * A_sh:
            t1 = (k - s + 1) * DT
        if t2 is None and area * n2 / npt >= 0.5 * A_sh:
            t2 = (k - s + 1) * DT
    out['tend1'], out['tend2'] = t1, t2
    if e + 1 < nf:
        out['riemerge'] = True
        out['buio'] = (e + 2 - s) * DT
        kx.pred(); kz.pred()
        d = dets[e + 1]
        S = kx.P[0][0] + SIG ** 2
        d2 = ((d[0] - kx.x[0]) ** 2 + (d[1] - kz.x[0]) ** 2) / S
        out['cont'] = d2 <= CHI95
        out['vivo1'] = t1 is None
        out['vivo2'] = t2 is None
    return out


def quota(xs):
    xs = list(xs)
    return 100.0 * sum(1 for x in xs if x) / len(xs) if xs else float('nan')


def mediana(xs):
    xs = sorted(x for x in xs if x is not None)
    return xs[len(xs) // 2] if xs else float('nan')
