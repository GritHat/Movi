#!/usr/bin/env python3
"""Torneo dei falsificatori, parte 2 (avversario): H-010, H-012, H-013, H-018, H-019; K-003, K-004, K-007.
Python puro, semi fissati. Uso: timeout 120 python3 torneo_parte2.py A|B|C|D|E
Il filtro (Ax) e' riscritto da me: velocita' quasi costante per asse, 15 Hz, sigma 5 cm, inizializzazione
x=z, v=0, P=diag(R, 4) come negli script degli autori. I generatori g2 e g3 sono COPIE di simA.py
(tracciamento) e prova_r2.py (rovesciatore); approach()/KFc sono copie di sim.py (creativo)."""
import math
import random
import sys

DT = 1 / 15
SIG = 0.05
R = SIG * SIG
C95, C99 = 5.991, 9.21
K95 = math.sqrt(C95)


class Ax:
    __slots__ = ("x", "v", "a", "b", "c", "q", "r")

    def __init__(s, q, r=R):
        s.x = None
        s.q = q
        s.r = r

    def predict(s):
        if s.x is None:
            return
        T, q = DT, s.q
        s.x += T * s.v
        a = s.a + 2 * T * s.b + T * T * s.c + q * T ** 3 / 3
        b = s.b + T * s.c + q * T * T / 2
        s.c = s.c + q * T
        s.a, s.b = a, b

    def update(s, z):
        if s.x is None:
            s.x, s.v, s.a, s.b, s.c = z, 0.0, s.r, 0.0, 4.0
            return
        S = s.a + s.r
        k0, k1 = s.a / S, s.b / S
        y = z - s.x
        s.x += k0 * y
        s.v += k1 * y
        a, b, c = (1 - k0) * s.a, (1 - k0) * s.b, s.c - k1 * s.b
        s.a, s.b, s.c = a, b, c


def d2(ax, ay, zx, zy):
    return (zx - ax.x) ** 2 / (ax.a + ax.r) + (zy - ay.x) ** 2 / (ay.a + ay.r)


def se(p, n):
    return math.sqrt(max(p * (1 - p), 0.0) / n) if n else float("nan")


# ---------------------------------------------------------------- A: copertura incrociata
NV = 30  # 2 s visibili


def g1(rnd, D, kind=None):
    """Generatore MIO. Miscela 60/15/10/15; manovra a istante uniforme nell'occlusione; transizione in 0,5 s."""
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
    """COPIA di truth() di simA.py (tracciamento), con dt parametro e l'elenco dei passi con manovra."""
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


def reappear_d2(traj, rnd, qs):
    """Misure ai fotogrammi 0..NV-1, poi buio, poi misura all'ultimo fotogramma. d2 prima dell'aggiornamento."""
    n = len(traj)
    zs = [(p[0] + rnd.gauss(0, SIG), p[1] + rnd.gauss(0, SIG)) for p in traj]
    res = []
    for q in qs:
        ax, ay = Ax(q), Ax(q)
        for k in range(n - 1):
            ax.predict()
            ay.predict()
            if k < NV:
                ax.update(zs[k][0])
                ay.update(zs[k][1])
        ax.predict()
        ay.predict()
        res.append(d2(ax, ay, zs[-1][0], zs[-1][1]))
    return res


# --- copia di prova_r2.py (rovesciatore): geometria e traiettoria
FS3 = 15.0
T3 = 1.0 / FS3
PAN_Y, PAN_HALF, RANGE_MAX, Y_T = 2.0, 0.75, 6.0, 4.0
K3 = PAN_HALF / PAN_Y


def in_ombra(x, y):
    return y > PAN_Y and abs(x) <= K3 * y


def visibile(x, y):
    return (not in_ombra(x, y)) and math.hypot(x, y) <= RANGE_MAX


def traiettoria(rnd):
    v = min(1.8, max(0.8, rnd.gauss(1.3, 0.2)))
    x, y, vx = -4.0, Y_T, v
    u = rnd.random()
    manovra = "prosegue" if u < 0.60 else ("sosta" if u < 0.85 else "torna")
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


def binom_ge(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def testA():
    QS = (0.1, 0.2, 0.5)
    N = 4000
    print("== A. Copertura alla ricomparsa (95%% / 99%%), +- errore tipo; N=%d per cella ==" % N)
    for name in ("G1 miscela mia 60/15/10/15", "G2 truth() di simA.py (tracciamento)"):
        print("-- %s" % name)
        for D in (0.5, 1.0, 2.0, 3.0):
            rnd = random.Random(1000 + int(D * 10) + (0 if name[1] == "1" else 500))
            c95 = [0, 0, 0]
            c99 = [0, 0, 0]
            bykind = {}
            for _ in range(N):
                if name[1] == "1":
                    traj, kind = g1(rnd, D)
                else:
                    traj, ev = g2(rnd, NV + int(round(D / DT)) + 1)
                    kind = "con manovra nel buio" if any(e >= NV for e in ev) else "senza manovra nel buio"
                ds = reappear_d2(traj, rnd, QS)
                bk = bykind.setdefault(kind, [0, 0])
                bk[1] += 1
                bk[0] += ds[1] <= C95
                for i in range(3):
                    c95[i] += ds[i] <= C95
                    c99[i] += ds[i] <= C99
            s = "  D=%.1f s:" % D
            for i, q in enumerate(QS):
                p, g = c95[i] / N, c99[i] / N
                s += "  q=%.1f: 95%%=%.3f+-%.3f 99%%=%.3f" % (q, p, se(p, N), g)
            print(s)
            print("      per manovra (q=0,2, 95%):", "; ".join(
                "%s %.3f (n=%d)" % (k, a / b, b) for k, (a, b) in sorted(bykind.items())))
            if D in (1.0, 2.0):
                p = c95[1] / N
                print("      P(passare 26/30 | copertura %.3f) = %.3f" % (p, binom_ge(26, 30, p)))
    # G1 per manovra pura, q=0,2, per ricavare la quota di manovre che rompe 0,85
    print("-- G1 per manovra pura (q=0,2; 95%; N=2000)")
    for D in (1.0, 2.0):
        rnd = random.Random(77 + int(D))
        row = {}
        for kind in ("prosegue", "sosta", "torna", "svolta"):
            ok = 0
            for _ in range(2000):
                traj, _k = g1(rnd, D, kind)
                ok += reappear_d2(traj, rnd, (0.2,))[0] <= C95
            row[kind] = ok / 2000
        pm = (row["sosta"] + row["torna"] + row["svolta"]) / 3
        f = (row["prosegue"] - 0.85) / (row["prosegue"] - pm) if row["prosegue"] > pm else float("nan")
        print("  D=%.0f s: %s ; quota di manovre (in parti uguali) oltre cui la copertura < 0,85: %.0f%%" % (
            D, ", ".join("%s %.3f" % kv for kv in row.items()), 100 * f))
    # G3: ombra geometrica del rovesciatore, copertura alla riemersione per durata
    print("-- G3 traiettoria() di prova_r2.py (rovesciatore), ombra geometrica, N=4000")
    rnd = random.Random(42)
    trajs = [traiettoria(rnd) for _ in range(4000)]
    bins = ((0.2, 0.75), (0.75, 1.5), (1.5, 2.5), (2.5, 3.5), (3.5, 99))
    for q in QS:
        rn = random.Random(11)
        tab = {}
        tot = [0, 0, 0]
        for traj, man in trajs:
            ax, ay = Ax(q), Ax(q)
            tl, ent, done = None, False, False
            for (t, x, y) in traj:
                ax.predict()
                ay.predict()
                if in_ombra(x, y):
                    ent = True
                if visibile(x, y):
                    zx, zy = x + rn.gauss(0, SIG), y + rn.gauss(0, SIG)
                    if ent and not done and tl is not None:
                        done = True
                        tau = t - tl
                        dd = d2(ax, ay, zx, zy)
                        b = [i for i, (lo, hi) in enumerate(bins) if lo <= tau < hi]
                        if b:
                            e = tab.setdefault((b[0], man), [0, 0, 0])
                            e[0] += dd <= C95
                            e[1] += dd <= C99
                            e[2] += 1
                        tot[0] += dd <= C95
                        tot[1] += dd <= C99
                        tot[2] += 1
                    ax.update(zx)
                    ay.update(zy)
                    tl = t
        print("  q=%.1f: tutte le riemersioni 95%%=%.3f 99%%=%.3f (n=%d)" % (q, tot[0] / tot[2], tot[1] / tot[2], tot[2]))
        for bi, (lo, hi) in enumerate(bins):
            n = sum(v[2] for (b, m), v in tab.items() if b == bi)
            if not n:
                continue
            a = sum(v[0] for (b, m), v in tab.items() if b == bi)
            g = sum(v[1] for (b, m), v in tab.items() if b == bi)
            det = "; ".join("%s %d/%d" % (m, v[0], v[2]) for (b, m), v in sorted(tab.items()) if b == bi)
            print("     durata [%.2f,%.2f) s: 95%%=%.3f+-%.3f 99%%=%.3f n=%d  (%s)" % (lo, hi, a / n, se(a / n, n), g / n, n, det))
    # regola: q dal NIS sui tratti visibili di G2
    print("-- regola di H-012: q scelto dal NIS medio (atteso 2) sui tratti visibili di G2 (60 fotogrammi, dal 15esimo)")
    rnd = random.Random(5)
    vis = [g2(rnd, 60)[0] for _ in range(1500)]
    best = None
    for q in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0):
        rn = random.Random(6)
        s, n, inside = 0.0, 0, 0
        for traj in vis:
            ax, ay = Ax(q), Ax(q)
            for k, (x, y) in enumerate(traj):
                ax.predict()
                ay.predict()
                zx, zy = x + rn.gauss(0, SIG), y + rn.gauss(0, SIG)
                if k >= 15:
                    dd = d2(ax, ay, zx, zy)
                    s += dd
                    n += 1
                    inside += dd <= C95
                ax.update(zx)
                ay.update(zy)
        print("  q=%-5g NIS medio=%.2f  quota a un passo entro il 95%%=%.3f" % (q, s / n, inside / n))
        if best is None or abs(s / n - 2) < best[1]:
            best = (q, abs(s / n - 2))
    qn = best[0]
    for D in (1.0, 2.0):
        rnd = random.Random(900 + int(D))
        ok = 0
        for _ in range(4000):
            traj, ev = g2(rnd, NV + int(round(D / DT)) + 1)
            ok += reappear_d2(traj, rnd, (qn,))[0] <= C95
        p = ok / 4000
        print("  q del NIS = %g: copertura 95%% a %.0f s su G2 = %.3f+-%.3f ; P(26/30)=%.3f" % (qn, D, p, se(p, 4000), binom_ge(26, 30, p)))


# ---------------------------------------------------------------- B: due persone
class Person:
    def __init__(s, rnd, side, W, kind, off=0.0):
        s.v = min(1.8, max(0.8, rnd.gauss(1.3, 0.2)))
        s.dir = -side
        s.x = side * (W / 2 + 2.6 + off)
        s.kind = kind
        s.xman = rnd.uniform(-W / 2 + 0.1, W / 2 - 0.1)
        s.sd = rnd.uniform(1.0, 3.0)
        s.done = False
        s.stop_until = -1.0

    def step(s, t):
        if not s.done and (s.x - s.xman) * s.dir >= 0:
            s.done = True
            if s.kind == "sosta":
                s.stop_until = t + s.sd
            elif s.kind == "torna":
                s.dir = -s.dir
        if t >= s.stop_until:
            s.x += s.v * s.dir * DT


def best_assign(cost, nt, nd):
    """Assegnazione ottima (forza bruta, equivalente all'ungherese con porta): cost[i][j]=d2 o None fuori porta."""
    best = [1e18, None]

    def rec(j, used, tot, asg):
        if j == nd:
            if tot < best[0]:
                best[0], best[1] = tot, list(asg)
            return
        asg.append(None)
        rec(j + 1, used, tot + C99, asg)
        asg.pop()
        for i in range(nt):
            if i not in used and cost[i][j] is not None:
                used.add(i)
                asg.append(i)
                rec(j + 1, used, tot + cost[i][j], asg)
                asg.pop()
                used.discard(i)

    rec(0, set(), 0.0, [])
    return best[1]


def scene(rnd, W, kinds, variant, q=0.5):
    dy = rnd.uniform(0.3, 1.0)
    P = [Person(rnd, -1, W, kinds[0]), Person(rnd, +1, W, kinds[1], off=rnd.uniform(0, 0.8))]
    ys = [4.0, 4.0 + dy]
    tracks = []  # [id, ax, ay, miss]
    nid = 0
    last = [None, None]
    was_hidden = [False, False]
    vis_after = [0.0, 0.0]
    amb = False
    t = 0.0
    while t < 16.0:
        for tr in tracks:
            tr[1].predict()
            tr[2].predict()
            tr[3] += 1
        if variant == "persa15":
            tracks = [tr for tr in tracks if K95 * math.sqrt(tr[1].a) <= 1.5]
        else:
            tracks = [tr for tr in tracks if tr[3] * DT <= 3.0]
        dets = []
        for i, p in enumerate(P):
            if abs(p.x) > W / 2:
                dets.append((i, p.x + rnd.gauss(0, SIG), ys[i] + rnd.gauss(0, SIG)))
                if was_hidden[i]:
                    vis_after[i] += DT
            else:
                was_hidden[i] = True
                vis_after[i] = 0.0
        nt, nd = len(tracks), len(dets)
        cost = [[None] * nd for _ in range(nt)]
        for i, tr in enumerate(tracks):
            for j, (pi, zx, zy) in enumerate(dets):
                c = d2(tr[1], tr[2], zx, zy)
                if c <= C99:
                    cost[i][j] = c
        asg = best_assign(cost, nt, nd) if nd else []
        for j, (pi, zx, zy) in enumerate(dets):
            i = asg[j]
            if i is None:
                tr = [nid, Ax(q), Ax(q), 0]
                nid += 1
                tracks.append(tr)
            else:
                tr = tracks[i]
                if tr[3] >= 3:  # riaggancio dopo almeno 2 fotogrammi mancati
                    n_tr = sum(1 for ii in range(nt) if cost[ii][j] is not None)
                    n_dt = sum(1 for jj in range(nd) if cost[i][jj] is not None)
                    if n_tr >= 2 or n_dt >= 2:
                        amb = True
            tr[1].update(zx)
            tr[2].update(zy)
            tr[3] = 0
            last[pi] = tr[0]
        for p in P:
            p.step(t)
        t += DT
        if all(was_hidden) and min(vis_after) >= 1.0:
            break
    swap = last[0] == 1 or last[1] == 0
    kept = last[0] == 0 and last[1] == 1
    return swap, kept, amb


def testB():
    N = 2000
    print("== B. Due persone dietro il pannello: ungherese + porta al 99%% (q=0,5), N=%d scene per riga ==" % N)
    print("   esiti: tenuta = stesse due identita'; scambio = almeno una persona con l'identita' dell'altra;")
    print("   nuova = nessuno scambio ma almeno un'identita' nuova; muto = scambio senza alcun riaggancio ambiguo")
    for variant in ("persa15", "tetto3s"):
        for W in (1.0, 2.0):
            for label, mix in (("(i) si incrociano e proseguono", ("prosegue", "prosegue")),
                               ("(ii) tornano entrambi indietro", ("torna", "torna")),
                               ("(iv) uno sosta 1-3 s, l'altro prosegue", ("sosta", "prosegue")),
                               ("(v) uno torna, l'altro sosta", ("torna", "sosta")),
                               ("(iii) miscela 70/18/12 indipendente", None)):
                rnd = random.Random(300 + int(W * 10) + len(label) + (0 if variant == "persa15" else 50))
                sw = kp = mu = am = 0
                for _ in range(N):
                    if mix is None:
                        ks = []
                        for _i in range(2):
                            u = rnd.random()
                            ks.append("prosegue" if u < 0.70 else "sosta" if u < 0.88 else "torna")
                    else:
                        ks = mix
                    s, k, a = scene(rnd, W, ks, variant)
                    sw += s
                    kp += k
                    am += a
                    mu += s and not a
                print("  %-8s W=%.0f m %-40s tenuta %.3f  scambio %.3f+-%.3f  nuova %.3f  ambigue %.3f  scambi muti %.3f" % (
                    variant, W, label, kp / N, sw / N, se(sw / N, N), 1 - (kp + sw) / N, am / N, mu / N))


# ---------------------------------------------------------------- C: finestra del previsto
def testC():
    print("== C. Finestra del «previsto»: istante in cui il raggio al 95% supera r_max (dopo 2 s visibili, 15 Hz, 5 cm) ==")
    for q in (0.1, 0.2, 0.5, 1.0):
        ax = Ax(q)
        for k in range(NV):
            ax.predict()
            ax.update(0.0)
        sv = math.sqrt(ax.c)
        t, t10, t15, r3, g3, r1 = 0.0, None, None, None, None, None
        while t < 6.0:
            ax.predict()
            t += DT
            r = K95 * math.sqrt(ax.a)
            if t10 is None and r > 1.0:
                t10 = t
            if t15 is None and r > 1.5:
                t15 = t
            if r1 is None and t >= 1.0:
                r1 = r
            if r3 is None and t >= 3.0:
                r3, g3 = r, math.sqrt(C99 * ax.a)
        print("  q=%.1f: sigma_v a regime %.2f m/s; r95(1 s)=%.2f m; r95>1,0 m a %.2f s; r95>1,5 m a %.2f s; a 3 s: r95=%.2f m, porta 99%%=%.2f m" % (
            q, sv, r1, t10, t15, r3, g3))
    print("  transiti (s): W=1 m: 0,8 m/s -> %.2f ; 1,3 m/s -> %.2f | W=2 m: 0,8 -> %.2f ; 1,3 -> %.2f" % (1 / 0.8, 1 / 1.3, 2 / 0.8, 2 / 1.3))
    print("  senza centroide intero (W+0,45)/v: W=1: 0,8 -> %.2f ; 1,3 -> %.2f | W=2: 0,8 -> %.2f ; 1,3 -> %.2f" % (
        1.45 / 0.8, 1.45 / 1.3, 2.45 / 0.8, 2.45 / 1.3))
    print("  del tutto nascosto (W-0,45)/v: W=1: 0,8 -> %.2f ; 1,3 -> %.2f | W=2: 0,8 -> %.2f ; 1,3 -> %.2f" % (
        0.55 / 0.8, 0.55 / 1.3, 1.55 / 0.8, 1.55 / 1.3))
    # Monte Carlo: pedone lento con passo irregolare, quota di passaggi «stessa traccia»
    print("  Monte Carlo (N=2000): quota di passaggi in cui alla riemersione la traccia e' ancora «prevista» E la misura e' nella porta al 99%")
    for W in (1.0, 2.0):
        for v0 in (0.8, 1.3):
            s = "   W=%.0f m, v=%.1f m/s:" % (W, v0)
            for q, rmax in ((0.2, 1.5), (0.5, 1.5), (0.5, 1.0), (0.2, 1.0), (0.1, 1.5)):
                rnd = random.Random(int(W * 100 + v0 * 10 + q * 1000 + rmax * 7))
                ok = 0
                for _ in range(2000):
                    v = max(0.4, rnd.gauss(v0, 0.1))
                    x, j = -2.0 * v0 - W / 2, 0.0
                    ax, ay = Ax(q), Ax(q)
                    lost, was, res = False, False, None
                    for k in range(400):
                        ax.predict()
                        ay.predict()
                        hidden = abs(x) <= W / 2
                        if hidden:
                            was = True
                            if K95 * math.sqrt(ax.a) > rmax:
                                lost = True
                        else:
                            zx, zy = x + rnd.gauss(0, SIG), 4.0 + rnd.gauss(0, SIG)
                            if was:
                                res = (not lost) and d2(ax, ay, zx, zy) <= C99
                                break
                            ax.update(zx)
                            ay.update(zy)
                        j += rnd.gauss(0, 0.1) * math.sqrt(DT)
                        x += (v + j) * DT
                    ok += bool(res)
                s += "  q=%.1f,r=%.1f: %.3f" % (q, rmax, ok / 2000)
            print(s)


# ---------------------------------------------------------------- D: scommessa (copia di sim.py del creativo)
QA = 0.3
PD = 0.9
SH0, SH1 = 3.0, 5.0


class KFc:
    def __init__(self, x, v, pxx=0.01, pvv=1.0):
        self.x, self.v, self.pxx, self.pxv, self.pvv = x, v, pxx, 0.0, pvv

    def predict(self, qa=QA, dt=DT):
        self.x += self.v * dt
        pxx = self.pxx + 2 * dt * self.pxv + dt * dt * self.pvv + qa * qa * dt ** 4 / 4
        pxv = self.pxv + dt * self.pvv + qa * qa * dt ** 3 / 2
        pvv = self.pvv + qa * qa * dt * dt
        self.pxx, self.pxv, self.pvv = pxx, pxv, pvv

    def update(self, z, r=SIG * SIG):
        s = self.pxx + r
        kx, kv = self.pxx / s, self.pxv / s
        y = z - self.x
        self.x += kx * y
        self.v += kv * y
        pxx = (1 - kx) * self.pxx
        pxv = (1 - kx) * self.pxv
        pvv = self.pvv - kv * self.pxv
        self.pxx, self.pxv, self.pvv = pxx, pxv, pvv


def approach(rnd, v_true):
    x = 0.0
    kf = KFc(x + rnd.gauss(0, SIG), 1.0)
    while x < SH0:
        x += v_true * DT
        kf.predict()
        if x < SH0 and rnd.random() < PD:
            kf.update(x + rnd.gauss(0, SIG))
    return kf


def one_pass(rnd, pop, fstop=None):
    if pop == "autore":  # popolazione di sim2.py
        v = rnd.uniform(0.8, 1.6)
        pr, ps, smax = 0.3, 0.1, 3.0
    elif pop == "squadra":
        v = min(1.6, max(1.0, rnd.gauss(1.3, 0.15)))
        pr, ps, smax = 0.1, 0.0, 3.0
    else:  # giurato
        v = min(1.1, max(0.5, rnd.gauss(0.8, 0.1)))
        pr, ps, smax = (0.3, 0.2, 3.0) if fstop is None else (0.0, fstop, 3.0)
    kf = approach(rnd, v)
    tn = (SH1 - kf.x) / max(kf.v, 0.1)
    r = rnd.random()
    W = SH1 - SH0
    if r < pr:
        t = W / (v * rnd.uniform(0.6, 1.0))
    elif r < pr + ps:
        t = W / v + rnd.uniform(0.5 if pop == "giurato" else 0.0, smax)
    else:
        t = W / v
    return t / tn, tn


def testD():
    print("== D. Scommessa sulla riemersione: finestra [q05,q95] del rapporto, tarata su 100 passaggi, provata su un'altra popolazione ==")
    rnd = random.Random(2026)
    pools = {"autore": [one_pass(rnd, "autore") for _ in range(3000)],
             "squadra": [one_pass(rnd, "squadra") for _ in range(3000)]}
    tests = {"autore (stessa di sim2.py)": [one_pass(rnd, "autore") for _ in range(2000)],
             "squadra": [one_pass(rnd, "squadra") for _ in range(2000)],
             "giurato 0,8 m/s, 30% rallenta, 20% sosta": [one_pass(rnd, "giurato") for _ in range(2000)]}
    for f in (0.0, 0.1, 0.2, 0.3, 0.4):
        tests["giurato 0,8 m/s, soste %d%%, nessun rallentamento" % int(f * 100)] = [one_pass(rnd, "giurato", f) for _ in range(2000)]
    for cal in ("autore", "squadra"):
        print("-- taratura su «%s» (200 tarature da 100 passaggi)" % cal)
        acc = {k: [] for k in tests}
        wid = []
        los, his = [], []
        for _ in range(200):
            c = sorted(rnd.choice(pools[cal])[0] for _ in range(100))
            lo = c[max(int(math.floor(0.05 * 101)) - 1, 0)]
            hi = c[min(int(math.ceil(0.95 * 101)) - 1, 99)]
            los.append(lo)
            his.append(hi)
            for k, tt in tests.items():
                acc[k].append(sum(1 for ratio, tn in tt if lo <= ratio <= hi) / len(tt))
            w = sorted((hi - lo) * tn for _, tn in tests["giurato 0,8 m/s, 30% rallenta, 20% sosta"])
            wid.append(w[len(w) // 2])
        print("   q05 medio %.3f, q95 medio %.3f ; larghezza mediana della finestra sul giurato %.2f s" % (
            sum(los) / 200, sum(his) / 200, sum(wid) / 200))
        for k, a in acc.items():
            m = sum(a) / len(a)
            sd = math.sqrt(sum((x - m) ** 2 for x in a) / (len(a) - 1))
            print("   prova su %-52s copertura %.3f (dev. std fra tarature %.3f, min %.3f)" % (k, m, sd, min(a)))


# ---------------------------------------------------------------- E: regola «mobile»
def run_mobile(rnd, speed, direction, sx, sy, rx, ry, dur, q=0.2):
    """Restituisce per fotogramma (chi2 > 9,21, |v| > 0,3). direction: 'x' laterale, 'y' radiale, None fermo."""
    ax, ay = Ax(q, rx), Ax(q, ry)
    out = []
    x = y = 0.0
    for k in range(int(dur / DT)):
        ax.predict()
        ay.predict()
        ax.update(x + rnd.gauss(0, sx))
        ay.update(y + rnd.gauss(0, sy))
        chi = ax.v ** 2 / ax.c + ay.v ** 2 / ay.c
        out.append((chi > C99, math.hypot(ax.v, ay.v) > 0.3))
        if direction == "x":
            x += speed * DT
        elif direction == "y":
            y += speed * DT
    return out


def summarize(rnd, n, speed, direction, sx, sy, rx, ry):
    w1 = [0, 0]
    w2 = [0, 0]
    fr = [0, 0]
    tot = 0
    for _ in range(n):
        o = run_mobile(rnd, speed, direction, sx, sy, rx, ry, 6.0)
        for i in (0, 1):
            w1[i] += any(f[i] for f in o[:15])
            w2[i] += any(f[i] for f in o[:30])
            fr[i] += sum(f[i] for f in o[30:])
        tot += len(o) - 30
    return [w1[i] / n for i in (0, 1)], [w2[i] / n for i in (0, 1)], [fr[i] / tot for i in (0, 1)]


def testE():
    print("== E. Regola «mobile»: chi2 sulla covarianza (v'Pv^-1 v > 9,21) contro soglia fissa |v| > 0,3 m/s; stesso filtro q=0,2, 15 Hz ==")
    rnd = random.Random(31)
    print("-- (1) rumore dell'autore: isotropo 5 cm. Pedone: quota di prove con almeno un «mobile» entro 1 s / entro 2 s dalla prima misura; quota di fotogrammi a regime (2-6 s)")
    for sp in (0.0, 0.3, 0.5, 0.62, 0.8, 1.2):
        a, b, c = summarize(rnd, 1000, sp, "x" if sp else None, SIG, SIG, R, R)
        print("   v=%.2f m/s: chi2: entro 1 s %.3f, entro 2 s %.3f, fotogrammi %.3f | soglia 0,3: entro 1 s %.3f, entro 2 s %.3f, fotogrammi %.3f" % (
            sp, a[0], b[0], c[0], a[1], b[1], c[1]))
    print("-- (2) muro FERMO, rumore di profondita' 5 cm*(z/2)^2, laterale 1 cm*z/2: quota di fotogrammi «mobile» a regime")
    for z in (2.0, 3.0, 4.0, 6.0):
        sy, sx = 0.05 * (z / 2) ** 2, 0.01 * z / 2
        a1 = summarize(rnd, 500, 0.0, None, sx, sy, R, R)
        a2 = summarize(rnd, 500, 0.0, None, sx, sy, sx * sx, sy * sy)
        print("   z=%.0f m (sigma_z=%.0f cm): filtro con R=5 cm isotropo: chi2 %.3f, soglia %.3f | filtro con R(z) giusto: chi2 %.3f, soglia %.3f" % (
            z, sy * 100, a1[2][0], a1[2][1], a2[2][0], a2[2][1]))
    print("-- (3) pedone con rumore ∝ z^2 e filtro con R(z) GIUSTO: quota di prove «mobile» entro 1 s / 2 s; fotogrammi a regime")
    for z in (2.0, 4.0, 6.0):
        sy, sx = 0.05 * (z / 2) ** 2, 0.01 * z / 2
        for sp in (0.5, 1.2):
            for d in ("x", "y"):
                a, b, c = summarize(rnd, 500, sp, d, sx, sy, sx * sx, sy * sy)
                print("   z=%.0f m, v=%.1f m/s %s: chi2: 1 s %.3f, 2 s %.3f, fotogr. %.3f | soglia: 1 s %.3f, 2 s %.3f, fotogr. %.3f" % (
                    z, sp, "laterale" if d == "x" else "radiale ", a[0], b[0], c[0], a[1], b[1], c[1]))
    print("-- (4) alternativa a finestra (mia, notata dopo): spostamento su 1 s > 5*sigma*sqrt(2), rumore isotropo 5 cm")
    thr = 5 * SIG * math.sqrt(2)
    for sp in (0.0, 0.5):
        hit = 0
        for _ in range(4000):
            dx = sp * 1.0 + rnd.gauss(0, SIG) - rnd.gauss(0, SIG)
            dy = rnd.gauss(0, SIG) - rnd.gauss(0, SIG)
            hit += math.hypot(dx, dy) > thr
        print("   v=%.1f m/s: «mobile» in %.4f delle finestre di 1 s" % (sp, hit / 4000))


if __name__ == "__main__":
    {"A": testA, "B": testB, "C": testC, "D": testD, "E": testE}[sys.argv[1]]()
