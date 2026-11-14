# sim.py — banco dell'avversario (f7, fase f4). Python puro, nessuna riga presa da 11-torneo/torneo.c.
# Modello: camera a foro a 1,2 m, inclinata in giu', 87 x 58 gradi, 320 x 240; profondita' lungo l'asse ottico;
# rumore k*z^2; margine m(z)=0,03+3*k*z^2. `leggi` e `stato` sono lo pseudocodice del par. 1.3 di DECISIONE.md.
import math, random

W, H = 320, 240
CAMH = 1.2
THX = math.tan(math.radians(43.5))
THY = math.tan(math.radians(29.0))
TX = [((i + 0.5) - W / 2) / (W / 2) * THX for i in range(W)]
TY = [(H / 2 - (j + 0.5)) / (H / 2) * THY for j in range(H)]
INF = float("inf")
NA, NR = 87, 30
LIBERO, OCCUPATO, IN_OMBRA, NON_VALIDO, FUORI = "L", "O", "S", "N", "F"


def render(boxes, pitch=15.0, zmax=6.0, room=True):
    """boxes: lista di (x0,x1,y0,y1,z0,z1). Ritorna (D pulita, ID): 0 = non valido; ID -2 suolo, -3 pareti, -1 niente."""
    s, c = math.sin(math.radians(pitch)), math.cos(math.radians(pitch))
    D = [0.0] * (W * H)
    ID = [-1] * (W * H)
    for j in range(H):
        ty = TY[j]
        dy = c + ty * s
        dz = -s + ty * c
        bt, bi = INF, -1
        if dz < -1e-12:
            bt, bi = CAMH / (-dz), -2
        if room:
            if dy > 1e-12 and 4.0 / dy < bt:
                bt, bi = 4.0 / dy, -3
            if dz > 1e-12 and (3.0 - CAMH) / dz < bt:
                bt, bi = (3.0 - CAMH) / dz, -3
        pre = []
        for b, (x0, x1, y0, y1, z0, z1) in enumerate(boxes):
            if abs(dy) < 1e-12:
                continue
            ta, tb = y0 / dy, y1 / dy
            if ta > tb:
                ta, tb = tb, ta
            if abs(dz) < 1e-12:
                if not (z0 <= CAMH <= z1):
                    continue
                tc, td = -INF, INF
            else:
                tc, td = (z0 - CAMH) / dz, (z1 - CAMH) / dz
                if tc > td:
                    tc, td = td, tc
            t0, t1 = max(ta, tc), min(tb, td)
            if t0 <= t1 and t1 > 0:
                pre.append((b, t0, t1, x0, x1))
        row = j * W
        for i in range(W):
            tx = TX[i]
            best, bid = bt, bi
            if room:
                t = 3.0 / abs(tx) if abs(tx) > 1e-12 else INF
                if t < best:
                    best, bid = t, -3
            for (b, t0, t1, x0, x1) in pre:
                if tx > 1e-12:
                    a, e = x0 / tx, x1 / tx
                elif tx < -1e-12:
                    a, e = x1 / tx, x0 / tx
                else:
                    if not (x0 <= 0 <= x1):
                        continue
                    a, e = -INF, INF
                lo = t0 if t0 > a else a
                hi = t1 if t1 < e else e
                if lo <= hi and lo > 1e-9 and lo < best:
                    best, bid = lo, b
            if bid != -1 and 0.05 < best <= zmax:
                D[row + i] = best
            ID[row + i] = bid
    return D, ID


def rumoroso(D, ID, k, rng, nulli=()):
    out = [0.0] * len(D)
    g = rng.gauss
    for n, t in enumerate(D):
        if t == 0.0 or ID[n] in nulli:
            continue
        v = t + k * t * t * g(0, 1) if k > 0 else t
        out[n] = v if v > 0.02 else 0.02
    return out


def assi(pitch):
    s, c = math.sin(math.radians(pitch)), math.cos(math.radians(pitch))
    return (0.0, c, -s), (1.0, 0.0, 0.0), (0.0, s, c)


def proietta(p, pitch=15.0):
    f, r, u = assi(pitch)
    v = (p[0], p[1], p[2] - CAMH)
    z = v[0] * f[0] + v[1] * f[1] + v[2] * f[2]
    if z < 0.05:
        return None
    x = v[0]
    y = v[1] * u[1] + v[2] * u[2]
    fu = (x / z) / THX * (W / 2) + W / 2
    fv = H / 2 - (y / z) / THY * (H / 2)
    if not (0 <= fu < W and 0 <= fv < H):
        return None
    return int(fu), int(fv), z


def punto(i, j, d, pitch=15.0):
    """Punto 3D ricostruito dal pixel con la posa creduta."""
    f, r, u = assi(pitch)
    tx, ty = TX[i], TY[j]
    return (d * tx, d * (f[1] + ty * u[1]), CAMH + d * (f[2] + ty * u[2]))


def marg(z, k):
    return 0.03 + 3 * k * z * z


def leggi(D, p, k, pitch=15.0):
    q = proietta(p, pitch)
    if q is None:
        return FUORI
    i, j, z = q
    if i < 1 or j < 1 or i >= W - 1 or j >= H - 1:
        return FUORI
    dmin, dmax = INF, 0.0
    for b in (-1, 0, 1):
        base = (j + b) * W + i
        for a in (-1, 0, 1):
            d = D[base + a]
            if d == 0.0:
                return NON_VALIDO
            if d < dmin:
                dmin = d
            if d > dmax:
                dmax = d
    m = marg(z, k)
    if z < dmin - m:
        return LIBERO
    if z > dmax + m:
        return IN_OMBRA
    return OCCUPATO


def stato(Ds, p, k, pitch=15.0):
    """Ds = [D[t], D[t-1], D[t-2]] della stessa epoca (quelli che esistono)."""
    s = leggi(Ds[0], p, k, pitch)
    if s == LIBERO:
        return LIBERO
    if not any(leggi(Dp, p, k, pitch) == LIBERO for Dp in Ds[1:3]):
        return s
    q = proietta(p, pitch)
    i, j, z = q
    D = Ds[0]
    if D[j * W + i] == 0.0:
        return s
    m = marg(z, k)
    for b in (-1, 0, 1):
        base = (j + b) * W + i
        for a in (-1, 0, 1):
            d = D[base + a]
            if d != 0.0 and d < z + m:
                return s
    return LIBERO


def cella_di(x, y):
    r = math.hypot(x, y)
    az = math.degrees(math.atan2(x, y)) + 43.5
    if r >= 3.0 or az < 0 or az >= NA or y <= 0:
        return None
    return int(az), int(r / 0.1)


def centro_cella(a, r, quota):
    az = math.radians(a + 0.5 - 43.5)
    rr = (r + 0.5) * 0.1
    return (rr * math.sin(az), rr * math.cos(az), quota)


def griglia_pixel(D, pitch=15.0):
    """Conteggi per cella dai pixel: occ (quota 0,07-2,0), suolo (-0,15..0,07). Ritorna anche r0[az] (primo ritorno, >=3 pixel)."""
    occ = [[0] * NR for _ in range(NA)]
    suo = [[0] * NR for _ in range(NA)]
    f, r_, u = assi(pitch)
    for j in range(H):
        ty = TY[j]
        ky = f[1] + ty * u[1]
        kz = f[2] + ty * u[2]
        row = j * W
        for i in range(W):
            d = D[row + i]
            if d == 0.0:
                continue
            x, y, z = d * TX[i], d * ky, CAMH + d * kz
            if y <= 0:
                continue
            rr = math.hypot(x, y)
            if rr >= 3.0:
                continue
            az = math.degrees(math.atan2(x, y)) + 43.5
            if az < 0 or az >= NA:
                continue
            if 0.07 <= z <= 2.0:
                occ[int(az)][int(rr / 0.1)] += 1
            elif -0.15 < z < 0.07:
                suo[int(az)][int(rr / 0.1)] += 1
    r0 = [NR] * NA
    for a in range(NA):
        for r in range(NR):
            if occ[a][r] >= 3:
                r0[a] = r
                break
    return occ, suo, r0
