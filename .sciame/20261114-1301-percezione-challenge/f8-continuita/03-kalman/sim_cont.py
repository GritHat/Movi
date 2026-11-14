#!/usr/bin/env python3
"""sim_cont.py — sciame-kalman, f8 (continuita' visiva), corsia A.
Copertura e raggio della regione prevista per orizzonte e per comportamento. Python puro, semi fissati.
Uso:  PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 sim_cont.py main|extra|ombra [G1|G2]|dati|moto
Il filtro (velocita' quasi costante per asse, 15 Hz, sigma 5 cm, q = 0,2, inizializzazione x=z, v=0,
P=diag(R,4)) e' quello del nucleo. G0 e' il MIO generatore (non e' il modello del filtro: profili di velocita'
con ritardo del primo ordine, soste, ritorni, svolte, oscillazione del passo). g1() e g2() sono COPIE letterali
di f2/04-torneo/torneo_parte2.py (g1: avversario; g2: truth() di simA.py, tracciamento): autori diversi da me.
"""
import bisect
import math
import random
import sys
import time

DT = 1 / 15
SIG = 0.05
RR = SIG * SIG
Q0 = 0.2
NV = 30
HS = (0.5, 1.0, 2.0, 3.0, 5.0)
LV = (0.5, 0.9)
CHI = {0.5: -2 * math.log(0.5), 0.9: -2 * math.log(0.1)}
VMAX = 2.5
CAPM = 0.1
PI = math.pi


# ------------------------------------------------------------------ filtro
def kf_run(zs, q=Q0):
    x, v, a, b, c = zs[0], 0.0, RR, 0.0, 4.0
    T = DT
    for z in zs[1:]:
        x += T * v
        a, b, c = a + 2 * T * b + T * T * c + q * T ** 3 / 3, b + T * c + q * T * T / 2, c + q * T
        S = a + RR
        k0, k1 = a / S, b / S
        y = z - x
        x += k0 * y
        v += k1 * y
        a, b, c = (1 - k0) * a, (1 - k0) * b, c - k1 * b
    return x, v, a, b, c


_, _, PA, PB, PC = kf_run([0.0] * NV)  # la covarianza non dipende dalle misure


def var0(t, q):
    return PA + 2 * t * PB + t * t * PC + q * t ** 3 / 3


# ------------------------------------------------------------------ generatori
FS = 30
DTF = 1 / FS
QUOTA0 = (("prosegue", 0.40), ("rallenta", 0.10), ("ferma", 0.15), ("riparte", 0.05), ("torna", 0.10),
          ("svolta", 0.15), ("accelera", 0.05))
QUOTA_T = (("prosegue", 0.30), ("ferma", 0.20), ("torna", 0.40), ("svolta", 0.10))


def g0(rnd, quota=QUOTA0):
    u = rnd.random()
    acc = 0.0
    kind = quota[-1][0]
    for k, p in quota:
        acc += p
        if u < acc:
            kind = k
            break
    s0 = min(2.2, max(0.5, rnd.gauss(1.3, 0.3)))
    th = rnd.uniform(0, 2 * PI)
    tL = (NV - 1) * DT
    tm = tL + rnd.uniform(-0.3, 2.5)
    tau_a = rnd.uniform(0.25, 0.6)
    s_new = s0
    if kind == "rallenta":
        s_new = s0 * rnd.uniform(0.3, 0.6)
    elif kind == "accelera":
        s_new = min(VMAX, s0 * rnd.uniform(1.3, 1.8))
    pause = rnd.uniform(0.5, 2.5) if kind == "riparte" else rnd.uniform(0.0, 0.8)
    s_back = s0 * rnd.uniform(0.8, 1.1)
    dth = rnd.choice((-1, 1)) * math.radians(rnd.uniform(40, 110))
    t_turn = rnd.uniform(0.5, 1.2)
    flip = False
    turned = 0.0
    n = int(round((tL + HS[-1]) * FS)) + 2
    s, om, ds = s0, 0.0, 0.0
    x = y = 0.0
    ph = rnd.uniform(0, 2 * PI)
    fsw = 0.9 * s0 / 1.3
    out = []
    for i in range(n):
        t = i * DTF
        sw = 0.025 * math.sin(2 * PI * fsw * t + ph) * min(1.0, s / 0.5)
        out.append((x - sw * math.sin(th), y + sw * math.cos(th)))
        tgt = s0
        if t >= tm:
            if kind in ("rallenta", "accelera"):
                tgt = s_new
            elif kind == "ferma":
                tgt = 0.0
            elif kind == "riparte":
                tgt = 0.0 if t < tm + 2.5 * tau_a + pause else s0
            elif kind == "torna":
                if t < tm + 2.5 * tau_a + pause:
                    tgt = 0.0
                else:
                    if not flip:
                        th += PI + rnd.gauss(0, 0.2)
                        flip = True
                    tgt = s_back
            elif kind == "svolta":
                if abs(turned) < abs(dth):
                    st = dth / t_turn * DTF
                    th += st
                    turned += st
        om += -om * DTF + 0.12 * math.sqrt(2 * DTF) * rnd.gauss(0, 1)
        ds += -ds / 1.5 * DTF + 0.06 * math.sqrt(2 * DTF / 1.5) * rnd.gauss(0, 1)
        s += (tgt - s) / tau_a * DTF
        sp = min(VMAX, max(0.0, s + ds * min(1.0, s / 0.3)))
        if sp > 0.05:
            th += om * DTF * min(1.0, sp / 0.5)
        x += sp * math.cos(th) * DTF
        y += sp * math.sin(th) * DTF
    meas = [out[2 * k] for k in range(NV)]
    base = 2 * (NV - 1)
    truths = [out[base + int(round(h * FS))] for h in HS]
    return meas, truths, kind


def g1(rnd, D, kind=None):
    """COPIA letterale di g1() di f2/04-torneo/torneo_parte2.py (avversario)."""
    no = int(round(D / DT))
    v = min(2.0, max(0.6, rnd.gauss(1.3, 0.25)))
    th = rnd.uniform(0, 2 * math.pi)
    u = rnd.random()
    if kind is None:
        kind = "prosegue" if u < 0.60 else "sosta" if u < 0.75 else "torna" if u < 0.85 else "svolta"
    tm = NV * DT + rnd.uniform(0, D)
    vx, vy = v * math.cos(th), v * math.sin(th)
    if kind == "sosta":
        tg = (0.0, 0.0)
    elif kind == "torna":
        tg = (-vx, -vy)
    elif kind == "svolta":
        a = rnd.choice((-1, 1)) * rnd.uniform(math.pi / 4, math.pi / 2)
        tg = (vx * math.cos(a) - vy * math.sin(a), vx * math.sin(a) + vy * math.cos(a))
    else:
        tg = (vx, vy)
    sd = rnd.uniform(0.5, 3.0)
    x = y = jx = jy = 0.0
    out = []
    for k in range(NV + no + 1):
        t = k * DT
        out.append((x, y))
        if t < tm:
            cx, cy = vx, vy
        elif kind == "sosta" and t > tm + 0.5 + sd:
            f = min(1.0, (t - tm - 0.5 - sd) / 0.5)
            cx, cy = vx * f, vy * f
        else:
            f = min(1.0, (t - tm) / 0.5)
            cx, cy = vx + (tg[0] - vx) * f, vy + (tg[1] - vy) * f
        if abs(cx) + abs(cy) > 0.05:
            jx += rnd.gauss(0, 0.1) * math.sqrt(DT)
            jy += rnd.gauss(0, 0.1) * math.sqrt(DT)
            cx += jx
            cy += jy
        x += cx * DT
        y += cy * DT
    return out, kind


def g2(rnd, n, dt=DT):
    """COPIA letterale di g2() di f2/04-torneo/torneo_parte2.py (truth() di simA.py, tracciamento)."""
    sp = max(0.3, rnd.gauss(1.3, 0.3))
    th = rnd.uniform(0, 2 * math.pi)
    x = y = 0.0
    st = False
    out, ev = [], []
    for k in range(n):
        if rnd.random() < 0.1 * dt:
            st = not st
            ev.append(k)
        if rnd.random() < 0.2 * dt:
            th += rnd.uniform(-math.pi / 2, math.pi / 2)
            ev.append(k)
        if not st:
            x += sp * math.cos(th) * dt
            y += sp * math.sin(th) * dt
        out.append((x, y))
    return out, ev


def at15(out, h):
    f = (NV - 1) + h / DT
    i = int(math.floor(f + 1e-9))
    w = f - i
    if w < 1e-9:
        return out[i]
    return (out[i][0] * (1 - w) + out[i + 1][0] * w, out[i][1] * (1 - w) + out[i + 1][1] * w)


def sample(meas, truths, kind, rnd):
    zx = [p[0] + rnd.gauss(0, SIG) for p in meas]
    zy = [p[1] + rnd.gauss(0, SIG) for p in meas]
    x, vx, _, _, _ = kf_run(zx)
    y, vy, _, _, _ = kf_run(zy)
    s = math.hypot(vx, vy)
    ex, ey = (vx / s, vy / s) if s > 1e-9 else (1.0, 0.0)
    res = []
    for tx, ty in truths:
        dx, dy = tx - x, ty - y
        res.append((dx * ex + dy * ey, -dx * ey + dy * ex))
    return (s, kind, res)  # res[j] = (lungo la traccia, trasversale) rispetto all'ultima posizione stimata


def dataset(gen, seed, n, quota=QUOTA0):
    rnd = random.Random(seed)
    D = []
    for _ in range(n):
        if gen == "G0":
            meas, truths, kind = g0(rnd, quota)
        elif gen == "G1":
            out, kind = g1(rnd, HS[-1])
            meas, truths = out[:NV], [at15(out, h) for h in HS]
        else:
            out, ev = g2(rnd, NV + int(round(HS[-1] / DT)) + 2)
            meas, truths = out[:NV], [at15(out, h) for h in HS]
            kind = "con eventi" if any(k >= NV - 8 for k in ev) else "senza eventi"
        D.append(sample(meas, truths, kind, rnd))
    return D


def cq(scores, p):
    """Quantile conforme: il ceil((n+1)p)-esimo punteggio piu' piccolo."""
    s = sorted(scores)
    k = math.ceil((len(s) + 1) * p)
    return s[k - 1] if k <= len(s) else float("inf")


def lens(d, r1, r2):
    if d >= r1 + r2:
        return 0.0
    if d <= abs(r1 - r2):
        return PI * min(r1, r2) ** 2
    a1 = r1 * r1 * math.acos((d * d + r1 * r1 - r2 * r2) / (2 * d * r1))
    a2 = r2 * r2 * math.acos((d * d + r2 * r2 - r1 * r1) / (2 * d * r2))
    k = 0.5 * math.sqrt(max(0.0, (-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)))
    return a1 + a2 - k


# ------------------------------------------------------------------ predittori
class A0:
    name = "A0 attuale: CV q=0,2, cerchio chi2"
    dens = True

    def fit(s, F):
        pass

    def score(s, smp, j):
        sp, _, res = smp
        al, lt = res[j]
        return ((al - sp * HS[j]) ** 2 + lt * lt) / var0(HS[j], Q0)

    def inside(s, smp, j, p):
        return s.score(smp, j) <= CHI[p]

    def area(s, smp, j, p):
        return PI * CHI[p] * var0(HS[j], Q0)

    def nll(s, smp, j):
        v = var0(HS[j], Q0)
        return math.log(2 * PI * v) + 0.5 * s.score(smp, j)

    def centre(s, smp, j):
        return (smp[0] * HS[j], 0.0)


class A0cap(A0):
    name = "A0cap: A0 intersecato col disco v_max*t+0,1"
    dens = False

    def inside(s, smp, j, p):
        al, lt = smp[2][j]
        return A0.inside(s, smp, j, p) and al * al + lt * lt <= (VMAX * HS[j] + CAPM) ** 2

    def area(s, smp, j, p):
        return lens(smp[0] * HS[j], math.sqrt(CHI[p] * var0(HS[j], Q0)), VMAX * HS[j] + CAPM)


class A1(A0):
    name = "A1: centro CV, raggio conforme per orizzonte"
    dens = False

    def fit(s, F):
        s.r = [{p: cq([math.sqrt(A0.score(s, m, j) * var0(HS[j], Q0)) for m in F], p) for p in LV}
               for j in range(len(HS))]

    def err(s, smp, j):
        return math.sqrt(A0.score(s, smp, j) * var0(HS[j], Q0))

    def inside(s, smp, j, p):
        return s.err(smp, j) <= s.r[j][p]

    def area(s, smp, j, p):
        return PI * s.r[j][p] ** 2


class A2(A0):
    name = "A2: centro CV, raggio conforme scalato con velocita' x tempo"
    dens = False

    def sc(s, smp, j):
        h = HS[j]
        return math.sqrt(A0.score(s, smp, j) * var0(h, Q0)) / (math.sqrt(var0(h, 0.0)) + smp[0] * h)

    def fit(s, F):
        s.k = [{p: cq([s.sc(m, j) for m in F], p) for p in LV} for j in range(len(HS))]

    def inside(s, smp, j, p):
        return s.sc(smp, j) <= s.k[j][p]

    def area(s, smp, j, p):
        h = HS[j]
        return PI * (s.k[j][p] * (math.sqrt(var0(h, 0.0)) + smp[0] * h)) ** 2


def ou_g(h, tau):
    return tau * (1 - math.exp(-h / tau))


def ou_var(h, tau, q):
    if tau > 1e3:  # limite CV: evita la cancellazione numerica
        return PA + 2 * h * PB + h * h * PC + q * h ** 3 / 3
    f = math.exp(-h / tau)
    g = tau * (1 - f)
    return PA + 2 * g * PB + g * g * PC + q * tau * tau * (h - 2 * tau * (1 - f) + tau * (1 - f * f) / 2)


class B0:
    name = "B0: velocita' che decade (OU), tau e q dalla verosimiglianza, cerchio chi2"
    dens = True
    TAUS = (1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0, 1e6)
    QS = (0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2, 2.0)

    def e2(s, smp, j):
        sp, _, res = smp
        al, lt = res[j]
        return (al - sp * ou_g(HS[j], s.tau)) ** 2 + lt * lt

    def fit(s, F):
        best = None
        s.grid = []
        for tau in s.TAUS:
            for q in s.QS:
                s.tau, s.q = tau, q
                tot = 0.0
                for j, h in enumerate(HS):
                    v = ou_var(h, tau, q)
                    lg = math.log(2 * PI * v)
                    tot += sum(lg + 0.5 * s.e2(m, j) / v for m in F) / len(F)
                s.grid.append((tot / len(HS), tau, q))
                if best is None or tot < best[0]:
                    best = (tot, tau, q)
        _, s.tau, s.q = best

    def inside(s, smp, j, p):
        return s.e2(smp, j) <= CHI[p] * ou_var(HS[j], s.tau, s.q)

    def area(s, smp, j, p):
        return PI * CHI[p] * ou_var(HS[j], s.tau, s.q)

    def nll(s, smp, j):
        v = ou_var(HS[j], s.tau, s.q)
        return math.log(2 * PI * v) + 0.5 * s.e2(smp, j) / v

    def centre(s, smp, j):
        return (smp[0] * ou_g(HS[j], s.tau), 0.0)


class B1(B0):
    name = "B1: centro OU, raggio conforme per orizzonte"
    dens = False

    def __init__(s, b0):
        s.b0 = b0

    def fit(s, F):
        s.tau, s.q = s.b0.tau, s.b0.q
        s.r2 = [{p: cq([s.e2(m, j) for m in F], p) for p in LV} for j in range(len(HS))]

    def inside(s, smp, j, p):
        return s.e2(smp, j) <= s.r2[j][p]

    def area(s, smp, j, p):
        return PI * s.r2[j][p]


class C1:
    name = "C1: ellisse lungo la traccia (centro arretrato, semiassi ~ v*t), conforme"
    dens = True

    def dn(s, smp, j):
        return smp[0] * HS[j] + math.sqrt(var0(HS[j], 0.0))

    def uw(s, smp, j):
        d = s.dn(smp, j)
        return smp[2][j][0] / d, smp[2][j][1] / d

    def sc(s, smp, j):
        u, w = s.uw(smp, j)
        mu, su, sw = s.par[j]
        return ((u - mu) / su) ** 2 + (w / sw) ** 2

    def fit(s, F):
        s.par = []
        for j in range(len(HS)):
            us = [s.uw(m, j) for m in F]
            mu = sum(u for u, _ in us) / len(us)
            su = math.sqrt(sum((u - mu) ** 2 for u, _ in us) / len(us))
            sw = math.sqrt(sum(w * w for _, w in us) / len(us))
            s.par.append((mu, su, sw))
        s.k2 = [{p: cq([s.sc(m, j) for m in F], p) for p in LV} for j in range(len(HS))]

    def inside(s, smp, j, p):
        return s.sc(smp, j) <= s.k2[j][p]

    def area(s, smp, j, p):
        mu, su, sw = s.par[j]
        return PI * s.k2[j][p] * su * sw * s.dn(smp, j) ** 2

    def nll(s, smp, j):
        mu, su, sw = s.par[j]
        return math.log(2 * PI * su * sw * s.dn(smp, j) ** 2) + 0.5 * s.sc(smp, j)

    def centre(s, smp, j):
        return (s.par[j][0] * s.dn(smp, j), 0.0)


# --- miscela di gaussiane a regimi, nel riferimento della traccia
PF, PT, PS = 0.45, 0.20, 0.35  # quote a priori fra le manovre: SCELTE A MANO, non stimate
SB = 0.1  # passo delle classi di velocita'
NS = 1200  # campioni per la soglia di densita'


def comps(sp, h, lam, qc):
    Pm = 1 - math.exp(-lam * (h + 0.3))
    v = var0(h, qc)
    out = [(1 - Pm, sp * h, 0.0, v, v)]
    J = 4
    for j in range(J):
        sj = h * (j + 0.5) / J
        v0 = var0(sj, qc)
        ma = min(sp * h, sp * (sj + 0.3))
        out.append((Pm * PF / J, ma, 0.0, v0 + (sp * h / J) ** 2 / 12 + 0.01, v0 + 0.01))
        tb = max(0.0, h - sj - 0.8)
        out.append((Pm * PT / J, ma - 0.9 * sp * tb, 0.0,
                    v0 + (1.9 * sp * h / J) ** 2 / 12 + (0.2 * sp * tb) ** 2 + 0.01,
                    v0 + (0.25 * sp * tb) ** 2 + 0.01))
    for sj in (0.25 * h, 0.75 * h):
        v0 = var0(sj, qc)
        rem = h - sj
        for phi in (50.0, 90.0):
            a = math.radians(phi)
            vv = v0 + (0.35 * sp * rem) ** 2 + (sp * h / 2) ** 2 / 12 + 0.01
            for sg in (1.0, -1.0):
                out.append((Pm * PS / 8, sp * sj + sp * rem * math.cos(a), sg * sp * rem * math.sin(a), vv, vv))
    return [(w, ma, ml, va, vl, w / (2 * PI * math.sqrt(va * vl))) for (w, ma, ml, va, vl) in out]


def mixdens(cs, al, lt):
    f = 0.0
    for (_, ma, ml, va, vl, cn) in cs:
        f += cn * math.exp(-0.5 * ((al - ma) ** 2 / va + (lt - ml) ** 2 / vl))
    return f


class D0:
    name = "D0: miscela a regimi, regione a densita' piu' alta, nominale"
    dens = True
    LAMS = (0.15, 0.3, 0.5)
    QCS = (0.03, 0.08)

    def sbin(s, smp):
        return min(30, int(round(smp[0] / SB)))

    def cs(s, smp, j):
        key = (s.sbin(smp), j)
        c = s.cache.get(key)
        if c is None:
            c = s.cache[key] = comps(key[0] * SB, HS[j], s.lam, s.qc)
        return c

    def fit(s, F):
        sub = F[:2000]
        best = None
        s.grid = []
        for lam in s.LAMS:
            for qc in s.QCS:
                s.lam, s.qc, s.cache = lam, qc, {}
                tot = 0.0
                for j in range(len(HS)):
                    tot += sum(-math.log(max(1e-300, mixdens(s.cs(m, j), *m[2][j]))) for m in sub) / len(sub)
                s.grid.append((tot / len(HS), lam, qc))
                if best is None or tot < best[0]:
                    best = (tot, lam, qc)
        _, s.lam, s.qc = best
        s.cache = {}
        s.tab = {}

    def table(s, key):
        t = s.tab.get(key)
        if t is None:
            rnd = random.Random(9000 + 97 * key[0] + key[1])
            cs = comps(key[0] * SB, HS[key[1]], s.lam, s.qc)
            ws = [c[0] for c in cs]
            fs = []
            for c in rnd.choices(cs, weights=ws, k=NS):
                al = rnd.gauss(c[1], math.sqrt(c[3]))
                lt = rnd.gauss(c[2], math.sqrt(c[4]))
                fs.append(mixdens(cs, al, lt))
            fs.sort()
            desc = fs[::-1]
            cum = []
            acc = 0.0
            for f in desc:
                acc += 1.0 / f
                cum.append(acc / NS)
            t = s.tab[key] = (fs, cum)
        return t

    def pval(s, smp, j):
        """Quota della massa prevista con densita' maggiore di quella nel punto vero."""
        fs, _ = s.table((s.sbin(smp), j))
        f = mixdens(s.cs(smp, j), *smp[2][j])
        return (NS - bisect.bisect_right(fs, f)) / NS

    def lev(s, j, p):
        return p

    def inside(s, smp, j, p):
        return s.pval(smp, j) <= s.lev(j, p)

    def area(s, smp, j, p):
        _, cum = s.table((s.sbin(smp), j))
        k = min(NS, max(1, int(math.ceil(s.lev(j, p) * NS))))
        return cum[k - 1]

    def nll(s, smp, j):
        return -math.log(max(1e-300, mixdens(s.cs(smp, j), *smp[2][j])))

    def centre(s, smp, j):
        cs = s.cs(smp, j)
        return (sum(c[0] * c[1] for c in cs), 0.0)


class D1(D0):
    name = "D1: miscela a regimi, livello conforme per orizzonte"
    dens = False

    def __init__(s, d0):
        s.d0 = d0

    def fit(s, F):
        s.lam, s.qc, s.cache, s.tab = s.d0.lam, s.d0.qc, s.d0.cache, s.d0.tab
        s.lv = [{p: min(1.0, cq([s.pval(m, j) for m in F], p)) for p in LV} for j in range(len(HS))]

    def lev(s, j, p):
        return s.lv[j][p]


class E0:
    name = "E0: la miscela collassata in una gaussiana (uscita di un IMM), ellisse chi2"
    dens = True

    def __init__(s, d0):
        s.d0 = d0
        s.mom = {}

    def fit(s, F):
        pass

    def m(s, smp, j):
        key = (s.d0.sbin(smp), j)
        r = s.mom.get(key)
        if r is None:
            cs = s.d0.cs(smp, j)
            mu = sum(c[0] * c[1] for c in cs)
            va = sum(c[0] * (c[3] + (c[1] - mu) ** 2) for c in cs)
            vl = sum(c[0] * (c[4] + c[2] ** 2) for c in cs)
            r = s.mom[key] = (mu, va, vl)
        return r

    def sc(s, smp, j):
        mu, va, vl = s.m(smp, j)
        al, lt = smp[2][j]
        return (al - mu) ** 2 / va + lt * lt / vl

    def k2(s, j, p):
        return CHI[p]

    def inside(s, smp, j, p):
        return s.sc(smp, j) <= s.k2(j, p)

    def area(s, smp, j, p):
        mu, va, vl = s.m(smp, j)
        return PI * s.k2(j, p) * math.sqrt(va * vl)

    def nll(s, smp, j):
        mu, va, vl = s.m(smp, j)
        return math.log(2 * PI * math.sqrt(va * vl)) + 0.5 * s.sc(smp, j)

    def centre(s, smp, j):
        return (s.m(smp, j)[0], 0.0)


class E1(E0):
    name = "E1: ellisse dell'IMM collassato, scala conforme per orizzonte"
    dens = False

    def fit(s, F):
        s.kk = [{p: cq([s.sc(m, j) for m in F], p) for p in LV} for j in range(len(HS))]

    def k2(s, j, p):
        return s.kk[j][p]


# ------------------------------------------------------------------ misure
def evaluate(V, D, kinds=False):
    """Per orizzonte e livello: copertura, raggio equivalente; per comportamento se richiesto."""
    out = {}
    for j in range(len(HS)):
        for p in LV:
            ins = [V.inside(m, j, p) for m in D]
            ar = sum(V.area(m, j, p) for m in D) / len(D)
            out[(j, p)] = (sum(ins) / len(D), math.sqrt(ar / PI))
            if kinds:
                bk = {}
                for m, i in zip(D, ins):
                    a = bk.setdefault(m[1], [0, 0])
                    a[0] += i
                    a[1] += 1
                out[("k", j, p)] = bk
    return out


def row(lbl, vals, fmt="%6.3f"):
    return "%-10s " % lbl + " ".join(fmt % v for v in vals)


def show(V, D, title, kinds=False):
    ev = evaluate(V, D, kinds)
    print("  %s   [%s, N=%d]" % (V.name, title, len(D)))
    for p in LV:
        print("   " + row("cop %d%%" % (100 * p), [ev[(j, p)][0] for j in range(len(HS))])
              + "   | " + row("r_eq", [ev[(j, p)][1] for j in range(len(HS))], "%5.2f"))
    if kinds:
        for p in LV:
            ks = sorted(ev[("k", 0, p)])
            for k in ks:
                n = ev[("k", 0, p)][k][1]
                print("     %-12s n=%4d %d%%: " % (k, n, 100 * p)
                      + " ".join("%6.3f" % (ev[("k", j, p)][k][0] / n) for j in range(len(HS))))
    return ev


def nll_row(V, D):
    return [sum(V.nll(m, j) for m in D) / len(D) for j in range(len(HS))]


def rmse_rows(D, cents):
    print("  Errore quadratico medio del centro (m) per orizzonte %s" % (HS,))
    for name, f in cents:
        r = []
        for j in range(len(HS)):
            se = 0.0
            for m in D:
                ca, cl = f(m, j)
                se += (m[2][j][0] - ca) ** 2 + (m[2][j][1] - cl) ** 2
            r.append(math.sqrt(se / len(D)))
        print("   " + row(name[:26].ljust(26), r))


def build(F):
    a0, a0c, a1, a2, b0, c1, d0 = A0(), A0cap(), A1(), A2(), B0(), C1(), D0()
    for v in (a0, a0c, a1, a2, b0, c1, d0):
        v.fit(F)
    b1, d1, e0 = B1(b0), D1(d0), E0(d0)
    e1 = E1(d0)
    for v in (b1, d1, e0, e1):
        v.fit(F)
    return [a0, a0c, a1, a2, b0, b1, c1, d0, d1, e0, e1]


def main():
    t0 = time.time()
    print("Covarianza a regime dopo %d misure: a=%.5f b=%.5f c=%.5f  (sigma_pos %.3f m, sigma_vel %.3f m/s)"
          % (NV, PA, PB, PC, math.sqrt(PA), math.sqrt(PC)))
    print("Raggio A0 al 95%%: " + " ".join("%.2f m a %.1f s" % (math.sqrt(5.991 * var0(h, Q0)), h)
                                           for h in (0.5, 1.0, 1.6, 2.0, 3.0, 5.0)))
    F = dataset("G0", 101, 5000)
    S = dataset("G0", 202, 3000)
    T = dataset("G0", 303, 6000)
    print("Insiemi: taratura G0 seme 101 N=%d; scelta G0 seme 202 N=%d; prova G0 seme 303 N=%d  (%.1f s)"
          % (len(F), len(S), len(T), time.time() - t0))
    V = build(F)
    b0, d0 = V[4], V[7]
    print("B0: tau=%.1f s, q=%.2f (griglia: migliori tre %s)" % (
        b0.tau, b0.q, ", ".join("tau=%g q=%g nll=%.3f" % (t, q, n) for n, t, q in sorted(b0.grid)[:3])))
    print("    solo CV (tau=1e6): " + ", ".join("q=%g nll=%.3f" % (q, n) for n, t, q in b0.grid if t > 1e5))
    print("D0: lambda=%.2f /s, qc=%.2f (griglia: %s)" % (
        d0.lam, d0.qc, ", ".join("lam=%g qc=%g nll=%.3f" % (l, q, n) for n, l, q in sorted(d0.grid))))
    print("C1: per orizzonte (centro/v*t, sigma lungo, sigma trasv): "
          + " ".join("(%.2f %.2f %.2f)" % p for p in V[6].par))
    print("\n== SCELTA (insieme di scelta, seme 202): orizzonti %s ==" % (HS,))
    cand = []
    for v in V:
        ev = show(v, S, "scelta")
        ok = all(abs(ev[(j, p)][0] - p) <= 0.03 for j in range(len(HS)) for p in LV)
        mr = sum(ev[(j, 0.9)][1] for j in range(len(HS))) / len(HS)
        print("     entro +-0,03 ovunque: %s; raggio medio al 90%%: %.3f m" % ("si" if ok else "NO", mr))
        if ok and v is not V[0]:
            cand.append((mr, v))
    cand.sort(key=lambda t: t[0])
    best = [v for _, v in cand[:2]]
    print("  >> le due migliori secondo la regola scritta prima: " + " | ".join(v.name for v in best))
    print("     (%.1f s)" % (time.time() - t0))

    print("\n== PROVA su G0 (seme 303), per comportamento: orizzonti %s ==" % (HS,))
    for v in [V[0], V[1]] + best + [u for u in V[2:] if u not in best]:
        show(v, T, "prova G0", kinds=(v is V[0] or v in best or v is V[8] or v is V[2]))
    print("  NLL media (piu' bassa e' meglio) per orizzonte, prova G0:")
    for v in V:
        if v.dens:
            print("   " + row(v.name[:10], nll_row(v, T), "%7.3f"))
    cents = [("fermo all'ultima posizione", lambda m, j: (0.0, 0.0))] + [
        (v.name, v.centre) for v in (V[0], V[4], V[6], V[7])]
    rmse_rows(T, cents)
    pro = [m for m in T if m[1] == "prosegue"]
    print("  ... sul solo 'prosegue' (n=%d):" % len(pro))
    rmse_rows(pro, cents)
    print("     (%.1f s)" % (time.time() - t0))

    print("\n== ALTRA POPOLAZIONE (taratura su G0, prova su generatori di altri autori) ==")
    G1 = dataset("G1", 404, 4000)
    G2 = dataset("G2", 505, 4000)
    GT = dataset("G0", 606, 3000, QUOTA_T)
    for name, D in (("G1 avversario", G1), ("G2 tracciamento", G2), ("G0 con 40% di ritorni", GT)):
        for v in [V[0]] + best + [u for u in (V[2], V[8], V[10]) if u not in best]:
            show(v, D, name, kinds=(v is V[0] or v in best))
        rmse_rows(D, cents)
    print("     (%.1f s)" % (time.time() - t0))

    # costo: densita' della miscela su una griglia di 2600 celle
    cs = comps(1.3, 3.0, d0.lam, d0.qc)
    t1 = time.time()
    for i in range(2600):
        mixdens(cs, 0.01 * i, 0.3)
    print("\nCosto: %d componenti; densita' su 2600 celle in %.1f ms (Python puro)" % (len(cs), 1e3 * (time.time() - t1)))
    print("Tempo totale %.1f s" % (time.time() - t0))


def dati():
    """Quanti passaggi servono alla taratura conforme: dispersione della copertura di prova."""
    F = dataset("G0", 101, 5000)
    T = dataset("G0", 303, 6000)
    a = A1()
    rnd = random.Random(707)
    print("A1 al 90%%: copertura di prova (G0, N=%d) con raggio tarato su n passaggi; 300 estrazioni" % len(T))
    for j in (1, 2, 4):
        fe = [math.sqrt(A0.score(a, m, j) * var0(HS[j], Q0)) for m in F]
        te = sorted(math.sqrt(A0.score(a, m, j) * var0(HS[j], Q0)) for m in T)
        for n in (30, 100, 300, 1000):
            cov, rad = [], []
            for _ in range(300):
                r = cq(rnd.sample(fe, n), 0.9)
                rad.append(r)
                cov.append(bisect.bisect_right(te, r) / len(te))
            cov.sort()
            rad.sort()
            k = math.ceil((n + 1) * 0.9)
            bm = k / (n + 1)
            bs = math.sqrt(k * (n + 1 - k) / ((n + 1) ** 2 * (n + 2)))
            print("  h=%.0f s n=%4d: copertura media %.3f, 5%%-95%% [%.3f, %.3f] (larghezza %.3f); raggio 5%%-95%% "
                  "[%.2f, %.2f] m; Beta teorica media %.3f dev.std %.3f"
                  % (HS[j], n, sum(cov) / 300, cov[15], cov[284], cov[284] - cov[15], rad[15], rad[284], bm, bs))
    # per comportamento servono n casi DI QUEL comportamento
    print("  Nota: i passaggi sono estratti con le quote di G0; per una fascia o un comportamento conta il numero"
          " di casi in quella fascia.")


def moto():
    """Errore di posa non modellato fra la fase visibile e il buio: variazione del tasso di deriva."""
    F = dataset("G0", 101, 5000)
    T = dataset("G0", 303, 6000)
    a = A1()
    a.fit(F)
    cases = (("fermo", 0.0, 0.0, 0.0), ("giro 0,1 gradi/s; 3 m; 0,015 m/s", 3.0, 0.1, 0.015),
             ("giro 1 gradi/s; 3 m; 0,05 m/s", 3.0, 1.0, 0.05), ("giro 1 gradi/s; 10 m; 0,05 m/s", 10.0, 1.0, 0.05),
             ("giro 0,3 gradi/s; 10 m; 0,10 m/s", 10.0, 0.3, 0.10), ("giro 1 gradi/s; 30 m; 0,10 m/s", 30.0, 1.0, 0.10),
             ("giro 3 gradi/s; 10 m; 0,30 m/s", 10.0, 3.0, 0.30))
    print("A1 (tarato a sensore fermo), prova G0 N=%d; errore = (differenza dei tassi di deriva) x tempo." % len(T))
    print("Colonne: orizzonti %s. 'nudo' = regione non allargata; 'somma' = raggio^2 + chi2*sigma_posa^2." % (HS,))
    for name, r, sb, sv in cases:
        rnd = random.Random(808)
        sbr = math.radians(sb)
        for p in LV:
            nudo, somma, rr = [], [], []
            for j, h in enumerate(HS):
                sp2 = ((r * sbr) ** 2 + 2 * sv * sv) * h * h  # varianza per asse della differenza (media sugli assi)
                r0 = a.r[j][p]
                r1 = math.sqrt(r0 * r0 + CHI[p] * sp2)
                c0 = c1 = 0
                for m in T:
                    al, lt = m[2][j]
                    ea, el = al - m[0] * h, lt
                    ang = rnd.uniform(0, 2 * PI)
                    dyaw = r * rnd.gauss(0, sbr * math.sqrt(2)) * h
                    ea += dyaw * math.cos(ang) + rnd.gauss(0, sv * math.sqrt(2)) * h
                    el += dyaw * math.sin(ang) + rnd.gauss(0, sv * math.sqrt(2)) * h
                    e = math.hypot(ea, el)
                    c0 += e <= r0
                    c1 += e <= r1
                nudo.append(c0 / len(T))
                somma.append(c1 / len(T))
                rr.append(r1 / r0)
            print("  %-34s %d%% nudo  %s" % (name, 100 * p, " ".join("%.3f" % v for v in nudo)))
            print("  %-34s %d%% somma %s  (raggio x %s)" % ("", 100 * p, " ".join("%.3f" % v for v in somma),
                                                         " ".join("%.2f" % v for v in rr)))



# ------------------------------------------------------------------ seconda serie (scritta dopo 'main')
class Wmin:
    """Soglia = massimo, sui comportamenti con >= 100 casi di taratura, del quantile conforme per comportamento."""

    def __init__(s, name, score, area_at):
        s.name, s.score, s.area_at = name, score, area_at

    def fit(s, F):
        s.thr = []
        for j in range(len(HS)):
            d = {}
            for p in LV:
                bk = {}
                for m in F:
                    bk.setdefault(m[1], []).append(s.score(m, j))
                d[p] = max(cq(v, p) for v in bk.values() if len(v) >= 100)
            s.thr.append(d)

    def inside(s, smp, j, p):
        return s.score(smp, j) <= s.thr[j][p]

    def area(s, smp, j, p):
        return s.area_at(smp, j, s.thr[j][p])


def extra():
    t0 = time.time()
    F = dataset("G0", 101, 5000)
    T = dataset("G0", 303, 6000)
    V = build(F)
    a1, c1, d1, e1 = V[2], V[6], V[8], V[10]

    def d_area(m, j, lv):
        _, cum = d1.table((d1.sbin(m), j))
        return cum[min(NS, max(1, int(math.ceil(min(1.0, lv) * NS)))) - 1]

    def r_sc(m, j):
        return math.hypot(*m[2][j]) / (m[0] * HS[j] + math.sqrt(var0(HS[j], 0.0)))

    W = [Wmin("A1w: cerchio sul punto CV, soglia sul comportamento peggiore", a1.err,
              lambda m, j, t: PI * t * t),
         Wmin("E1w: ellisse dell'IMM collassato, soglia sul comportamento peggiore", e1.sc,
              lambda m, j, t: PI * t * math.sqrt(e1.m(m, j)[1] * e1.m(m, j)[2])),
         Wmin("D1w: miscela a regimi, livello sul comportamento peggiore", d1.pval, d_area),
         Wmin("R1w: disco sull'ULTIMA posizione, raggio k*(v*t+sigma), comportamento peggiore", r_sc,
              lambda m, j, t: PI * (t * (m[0] * HS[j] + math.sqrt(var0(HS[j], 0.0)))) ** 2)]
    print("== TARATURA SUL COMPORTAMENTO PEGGIORE (prova G0 seme 303): orizzonti %s ==" % (HS,))
    show(d1, T, "prova G0 (riferimento: D1 tarata in media)")
    for w in W:
        w.fit(F)
        ev = show(w, T, "prova G0", kinds=True)
        for p in LV:
            mn = [min(ev[("k", j, p)][k][0] / ev[("k", j, p)][k][1] for k in ev[("k", j, p)]) for j in range(len(HS))]
            print("     minimo per comportamento al %d%%: " % (100 * p) + " ".join("%.3f" % v for v in mn))
    print("  livelli usati da D1w al 90%%: " + " ".join("%.3f" % W[2].thr[j][0.9] for j in range(len(HS))))
    G1 = dataset("G1", 404, 4000)
    G2 = dataset("G2", 505, 4000)
    for name, D in (("G1 avversario", G1), ("G2 tracciamento", G2)):
        for w in (W[2], W[3]):
            show(w, D, name, kinds=True)
    print("\n== DIAGNOSI di C1 su G2 per velocita' stimata (notato dopo) ==")
    for lo, hi in ((0.0, 0.5), (0.5, 9.0)):
        sub = [m for m in G2 if lo <= m[0] < hi]
        print("  velocita' stimata in [%.1f, %.1f) m/s: n=%d; C1 al 90%%: %s; D1 al 90%%: %s" % (
            lo, hi, len(sub), " ".join("%.3f" % (sum(c1.inside(m, j, 0.9) for m in sub) / len(sub)) for j in range(len(HS))),
            " ".join("%.3f" % (sum(d1.inside(m, j, 0.9) for m in sub) / len(sub)) for j in range(len(HS)))))
    print("\n== CODE: rapporto fra i quantili 90%% e 50%% dell'errore del punto CV (gaussiana: 1,82) ==")
    for name, D in (("G0", T), ("G1", G1), ("G2", G2)):
        r = []
        for j in range(len(HS)):
            e = sorted(a1.err(m, j) for m in D)
            r.append(e[int(0.9 * len(e))] / e[int(0.5 * len(e))])
        print("  %s: " % name + " ".join("%.2f" % v for v in r))
    print("Tempo %.1f s" % (time.time() - t0))


def ombra():
    """Evidenza negativa: striscia d'ombra nel riferimento della traccia; chi esce e' rivisto e non conta."""
    t0 = time.time()
    F = dataset("G0", 101, 5000)
    gen = sys.argv[2] if len(sys.argv) > 2 else "G0"
    T = dataset(gen, {"G0": 303, "G1": 404, "G2": 505}[gen], 6000)
    print("Generatore di prova: %s" % gen)
    d0 = D0()
    d0.fit(F)
    a0 = A0()
    L0, L1 = -1.0, 2.0
    NSO = 1500
    for Wd in (2.0, 1.0):
        SA = Wd * (L1 - L0)
        print("== OMBRA schematica: striscia lunga %.0f m, larga %.0f m (area %.1f m2); prova N=%d; %s ==" % (
            Wd, L1 - L0, SA, len(T), HS))

        def instrip(al, lt):
            return 0.0 < al < Wd and L0 < lt < L1

        tabs = {}

        def tab(kind, key):
            t = tabs.get((kind, key))
            if t is None:
                sp, h = key[0] * SB, HS[key[1]]
                if kind == "g":
                    v = var0(h, Q0)
                    cs = [(1.0, sp * h, 0.0, v, v, 1 / (2 * PI * v))]
                else:
                    cs = comps(sp, h, d0.lam, d0.qc)
                rnd = random.Random(5000 + 97 * key[0] + key[1])
                fs = []
                for c in rnd.choices(cs, weights=[c[0] for c in cs], k=NSO):
                    al = rnd.gauss(c[1], math.sqrt(c[3]))
                    lt = rnd.gauss(c[2], math.sqrt(c[4]))
                    if instrip(al, lt):
                        fs.append(mixdens(cs, al, lt))
                fs.sort()
                cum, acc = [], 0.0
                for f in fs[::-1]:
                    acc += 1.0 / f
                    cum.append(acc / NSO)
                t = tabs[(kind, key)] = (cs, fs, cum)
            return t

        def clip_area(sp, h, p):
            r2 = CHI[p] * var0(h, Q0)
            n = 0
            for i in range(int(Wd * 10)):
                for k in range(int((L1 - L0) * 10)):
                    al, lt = 0.05 + 0.1 * i, L0 + 0.05 + 0.1 * k
                    n += (al - sp * h) ** 2 + lt * lt <= r2
            return n * 0.01

        ca = {}
        for j, h in enumerate(HS):
            hid = [m for m in T if instrip(*m[2][j])]
            if len(hid) < 30:
                print("  h=%.1f s: ancora nascosti %d: troppo pochi" % (h, len(hid)))
                continue
            kinds = {}
            for m in hid:
                kinds[m[1]] = kinds.get(m[1], 0) + 1
            line = "  h=%.1f s: ancora nascosti %d (%.3f): %s" % (h, len(hid), len(hid) / len(T), " ".join(
                "%s %d" % kv for kv in sorted(kinds.items())))
            print(line)
            for p in LV:
                c_clip = a_clip = 0.0
                res = {"g": [0, 0.0, 0, 0.0], "m": [0, 0.0, 0, 0.0]}
                for m in hid:
                    key = (d0.sbin(m), j)
                    c_clip += a0.inside(m, j, p)
                    kk = (key, p)
                    if kk not in ca:
                        ca[kk] = clip_area(key[0] * SB, h, p)
                    a_clip += ca[kk]
                    for kind in ("g", "m"):
                        cs, fs, cum = tab(kind, key)
                        r = res[kind]
                        r[3] += len(fs) / NSO
                        if len(fs) < 15:
                            r[2] += 1  # il modello da' meno dell'1 % di massa in ombra: regione vuota
                            continue
                        f = mixdens(cs, *m[2][j])
                        r[0] += (len(fs) - bisect.bisect_right(fs, f)) / len(fs) <= p
                        r[1] += cum[max(1, int(math.ceil(p * len(fs)))) - 1]
                n = len(hid)
                print("     %d%%: cerchio A0 ritagliato: cop %.3f, area %.2f m2 (%.0f%% della striscia)" % (
                    100 * p, c_clip / n, a_clip / n, 100 * a_clip / n / SA))
                for kind, nm in (("g", "gaussiana A0 troncata e rinormalizzata"), ("m", "miscela troncata e rinormalizzata")):
                    r = res[kind]
                    print("          %s: cop %.3f, area %.2f m2 (%.0f%%); regione vuota in %d casi; massa prevista"
                          " in ombra %.3f" % (nm, r[0] / n, r[1] / n, 100 * r[1] / n / SA, r[2], r[3] / n))
        # la massa prevista in ombra contro la quota vera, su TUTTI i casi
        for j, h in enumerate(HS):
            pm = pg = 0.0
            for m in T:
                key = (d0.sbin(m), j)
                pm += len(tab("m", key)[1]) / NSO
                pg += len(tab("g", key)[1]) / NSO
            print("  h=%.1f s: quota vera ancora nascosta %.3f; massa in ombra prevista: miscela %.3f, gaussiana A0 %.3f"
                  % (h, sum(instrip(*m[2][j]) for m in T) / len(T), pm / len(T), pg / len(T)))
    print("Tempo %.1f s" % (time.time() - t0))


if __name__ == "__main__":
    {"main": main, "dati": dati, "moto": moto, "extra": extra, "ombra": ombra}[sys.argv[1] if len(sys.argv) > 1 else "main"]()
