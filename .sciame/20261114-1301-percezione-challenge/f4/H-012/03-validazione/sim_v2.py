#!/usr/bin/env python3
"""Prove A e B di H-012 (f4), sciame-validazione. Python puro, scritto da capo.
Progetto congelato in f3/H-012/02-validazione/VERIFICA.md, par. 4. Seme base 5101.
Uso:  sim_h012.py A <T|D> <w> <N>     | sim_h012.py SWEEP <N> | sim_h012.py A2
      sim_h012.py WALL <nwin>         | sim_h012.py PED <N>   | sim_h012.py V1 <N>
"""
import sys, math, random

DT = 1.0 / 15.0
Q = 0.2
CHI95 = 5.991
CHI99 = 9.21
G = 0.40
VMAX = 2.5
TG = 10.0
HALF = math.radians(43.5)
SEED = 5101
SQ2 = math.sqrt(2.0)
ACC = 1.0
DEG1 = math.radians(1.0)


def sig_r(z, curve):
    if curve == 'nom':
        return z * z * 0.08 / (424.0 * 0.05)
    if curve == 'lim':
        return 0.04 * (z / 2.0) ** 2
    return 0.05 * (z / 2.0) ** 2          # 'tor'


def sig_t(z):
    return z * DEG1 / math.sqrt(12.0)


class KF1:
    __slots__ = ('p', 'v', 'a', 'b', 'c')

    def __init__(s, z1, z2, dt, R):
        s.p = z2; s.v = (z2 - z1) / dt
        s.a = R; s.b = R / dt; s.c = 2 * R / (dt * dt)

    def predict(s):
        s.p += s.v * DT
        a, b, c = s.a, s.b, s.c
        s.a = a + 2 * DT * b + DT * DT * c + Q * DT ** 3 / 3
        s.b = b + DT * c + Q * DT * DT / 2
        s.c = c + Q * DT

    def update(s, z, R):
        S = s.a + R; k1 = s.a / S; k2 = s.b / S; y = z - s.p
        s.p += k1 * y; s.v += k2 * y
        a, b, c = s.a, s.b, s.c
        s.a = a - k1 * a; s.b = b - k1 * b; s.c = c - k2 * b


class Geo:
    def __init__(s, yp, w, yped, rmax, e):
        s.yp = yp; s.w = w; s.yped = yped; s.rmax = rmax; s.e = e
        s.tA = (w / 2.0) / yp                       # ombra vera
        s.Ap = math.atan(s.tA)
        s.xs = s.tA * yped                          # mezza larghezza vera alla linea del pedone
        s.xse = s.xs + e                            # stimata
        s.has = s.xse > 1e-9
        if s.has:
            s.tAe = s.xse / yped
            s.Ae = math.atan(s.tAe)
            s.he = yp * s.tAe
            s.sA = math.sin(s.Ae); s.cA = math.cos(s.Ae)
            s.area = s.Ae * rmax * rmax - s.he * yp
        else:
            s.area = 0.0

    def in_true(s, x, y):
        return y >= s.yp and abs(x) <= y * s.tA

    def in_est(s, x, y):
        return s.has and y >= s.yp and abs(x) <= y * s.tAe

    def d_est(s, x, y):
        if not s.has:
            return 1e9
        ax = abs(x)
        if y >= s.yp and ax <= y * s.tAe:
            return 0.0
        dx = ax - s.he; dy = y - s.yp
        d1 = (s.yp - y) if (ax <= s.he) else math.hypot(dx, dy)
        t = dx * s.sA + dy * s.cA
        d2 = math.hypot(dx, dy) if t <= 0 else abs(dx * s.cA - dy * s.sA)
        return d1 if d1 < d2 else d2

    def d_true(s, x, y):
        ax = abs(x)
        if y >= s.yp and ax <= y * s.tA:
            return 0.0
        h = s.yp * s.tA; sA = math.sin(s.Ap); cA = math.cos(s.Ap)
        dx = ax - h; dy = y - s.yp
        d1 = (s.yp - y) if (ax <= h) else math.hypot(dx, dy)
        t = dx * sA + dy * cA
        d2 = math.hypot(dx, dy) if t <= 0 else abs(dx * cA - dy * sA)
        return d1 if d1 < d2 else d2

    def cell(s, x, y):
        """centro della cella polare (1 grado x 0,1 m) che contiene il punto; e se sta nella griglia"""
        th = math.degrees(math.atan2(x, y)); r = math.hypot(x, y)
        thc = math.radians(math.floor(th) + 0.5); rc = (math.floor(r / 0.1) + 0.5) * 0.1
        ing = rc <= s.rmax and abs(thc) <= HALF + 1e-9
        return rc * math.sin(thc), rc * math.cos(thc), ing

    def layer1(s, x, y):
        """(lettura i: sola ombra dilatata ; lettura ii: + non osservate contigue, cioe' fuori griglia)"""
        xc, yc, ing = s.cell(x, y)
        if not ing:
            return False, True
        v = s.d_est(xc, yc) <= G
        return v, v

    def est_unobs(s, x, y):
        xc, yc, ing = s.cell(x, y)
        return (not ing) or s.in_est(xc, yc)


def observe(geo, x, y, rho, rnd, curve):
    """-> (larghezza visibile [rad], misura (zx,zy,Rx,Ry) o None)"""
    r = math.hypot(x, y); th = math.atan2(x, y)
    if r > geo.rmax or r <= rho:
        return 0.0, None
    al = math.asin(rho / r)
    lo = max(th - al, -HALF); hi = min(th + al, HALF)
    if hi <= lo:
        return 0.0, None
    if y > geo.yp:
        l1 = lo; h1 = min(hi, -geo.Ap); w1 = max(0.0, h1 - l1)
        l2 = max(lo, geo.Ap); h2 = hi; w2 = max(0.0, h2 - l2)
    else:
        l1 = lo; h1 = hi; w1 = hi - lo; w2 = 0.0; l2 = h2 = 0.0
    if w1 >= w2:
        wv = w1; tm = 0.5 * (l1 + h1)
    else:
        wv = w2; tm = 0.5 * (l2 + h2)
    if wv < 3 * DEG1:
        return wv, None
    sr = sig_r(r, curve); st = sig_t(r)
    zr = r + rnd.gauss(0, sr); xi = rnd.gauss(0, st)
    sn = math.sin(tm); cs = math.cos(tm)
    zx = zr * sn + xi * cs; zy = zr * cs - xi * sn
    Rx = st * st * cs * cs + sr * sr * sn * sn; Ry = sr * sr * cs * cs + st * st * sn * sn
    return wv, (zx, zy, Rx, Ry, sr)


def run_pass(rnd, geo, beh, curve, rho, pd=1.0):
    yped = geo.yped; xs = geo.xs
    xvis = min(yped * math.tan(HALF), math.sqrt(max(geo.rmax ** 2 - yped ** 2, 0.0)))
    x0 = -min(xs + 2.0, xvis - 0.25); xend = -x0
    v = rnd.uniform(0.8, 1.4)
    xstop = rnd.uniform(-xs + 0.2, xs - 0.2) if xs > 0.2 else 0.0
    x, y, vx, vy = x0, yped, v, 0.0
    phase = 0; timer = 0.0; t4 = None
    kx = ky = None; first = None
    pending = False; kpend = -1; klast = -1; zlast = None
    lost1 = lost2 = False; prev = None           # prev = (cx, cy, r95, shown1, shown2)
    nomeas = 0; freeb = 0
    alert = False                                 # avviso legato alla traccia attivo (lettura R-a)
    R = dict(n1=0, n1_out_i=0, n1_out_ii=0, n1_nolayer=0, n1_afterTG=0, n2=0, n2_fail=0,
             openmiss=0, reem=None, relb=None, tg=False, dur=None, track=False, hidk=None)
    k = 0
    while k < 600:
        if k > 0:
            if phase == 0:
                tx, ty = v, 0.0
                if beh != 'prosegue' and x >= xstop - v * v / (2 * ACC):
                    phase = 1
            if phase == 1:
                tx, ty = 0.0, 0.0
                if math.hypot(vx, vy) < 0.02:
                    vx = vy = 0.0
                    if beh == 'sosta':
                        phase = 2; timer = rnd.uniform(2.0, 4.0)
                    elif beh == 'torna':
                        phase = 3
                    else:
                        phase = 4; t4 = k
            if phase == 2:
                tx, ty = 0.0, 0.0
                timer -= DT
                if timer <= 0:
                    phase = 5
            elif phase == 3:
                tx, ty = -v, 0.0
            elif phase == 4:
                rr = math.hypot(x, y); tx, ty = v * x / rr, v * y / rr
            elif phase == 5:
                tx, ty = v, 0.0
            dvx = tx - vx; dvy = ty - vy; n = math.hypot(dvx, dvy)
            if n <= ACC * DT:
                vx, vy = tx, ty
            else:
                vx += dvx / n * ACC * DT; vy += dvy / n * ACC * DT
            x += vx * DT; y += vy * DT
            if beh in ('prosegue', 'sosta') and x >= xend:
                break
            if beh == 'torna' and phase == 3 and x <= x0:
                break
            if beh == 'lontano' and t4 is not None and (k - t4) * DT >= 12.5:
                break
        wv, z = observe(geo, x, y, rho, rnd, curve)
        if z is not None and pd < 1.0 and rnd.random() > pd:
            z = None
        hidden = geo.in_true(x, y)
        ingrid = math.hypot(x, y) <= geo.rmax and abs(math.atan2(x, y)) <= HALF
        got = False
        if kx is None:
            if z is not None:
                if first is None:
                    first = (z, k)
                else:
                    (z1, k1) = first; dt = (k - k1) * DT
                    kx = KF1(z1[0], z[0], dt, z[2]); ky = KF1(z1[1], z[1], dt, z[3])
                    klast = k; zlast = z; R['track'] = True
                got = True
        else:
            kx.predict(); ky.predict()
            if z is not None:
                dx = z[0] - kx.p; dy = z[1] - ky.p
                d2 = dx * dx / (kx.a + z[2]) + dy * dy / (ky.a + z[3])
                if pending:
                    tau = (k - klast) * DT
                    disc = math.hypot(z[0] - zlast[0], z[1] - zlast[1]) <= VMAX * tau + 3 * z[4] * SQ2
                    if R['reem'] is None:
                        near40 = near20 = False
                        if prev is not None:
                            cx, cy, r95 = prev[0], prev[1], prev[2]
                            i = -8
                            while i <= 8 and not near20:
                                qx = z[0] + i * 0.05; j = -8
                                while j <= 8:
                                    qy = z[1] + j * 0.05
                                    dq = math.hypot(i * 0.05, j * 0.05)
                                    if dq <= 0.40 and math.hypot(qx - cx, qy - cy) <= r95 and geo.est_unobs(qx, qy):
                                        near40 = True
                                        if dq <= 0.20:
                                            near20 = True; break
                                    j += 1
                                i += 1
                        R['reem'] = dict(tau=tau, in95=d2 <= CHI95, in99=d2 <= CHI99, disc=disc,
                                         s1=(prev[3] if prev else True), s2=(prev[4] if prev else True),
                                         n40=near40, n20=near20, afterTG=(k - kpend) * DT >= TG, tf=k * DT)
                    if disc:
                        if R['dur'] is None:
                            R['dur'] = (k - kpend) * DT
                        pending = False; alert = False
                        if d2 <= CHI99:
                            kx.update(z[0], z[2]); ky.update(z[1], z[3])
                        else:
                            kx.p = z[0]; kx.v = 0.0; kx.a = z[2]; kx.b = 0.0; kx.c = 1.0
                            ky.p = z[1]; ky.v = 0.0; ky.a = z[3]; ky.b = 0.0; ky.c = 1.0
                        klast = k; zlast = z; got = True
                else:
                    kx.update(z[0], z[2]); ky.update(z[1], z[3])
                    klast = k; zlast = z; got = True
            if not got:
                px, py = kx.p, ky.p
                if not pending:
                    l1 = geo.layer1(px, py)
                    if geo.est_unobs(px, py) or l1[1]:
                        pending = True; alert = True; kpend = k; lost1 = lost2 = False; freeb = 0
                        if R['hidk'] is None:
                            R['hidk'] = k; R['tl'] = klast * DT
                    else:
                        R['openmiss'] += 1
                if pending:
                    r95 = math.sqrt(CHI95 * max(kx.a, ky.a))
                    if not lost1 and geo.has and math.pi * r95 * r95 >= 0.5 * geo.area:
                        cnt = 0; n = int(r95 / 0.2) + 1; i = -n
                        while i <= n:
                            qx = px + i * 0.2; j = -n
                            while j <= n:
                                qy = py + j * 0.2
                                if (i * i + j * j) * 0.04 <= r95 * r95 and geo.in_est(qx, qy) and math.hypot(qx, qy) <= geo.rmax:
                                    cnt += 1
                                j += 1
                            i += 1
                        if cnt * 0.04 >= 0.5 * geo.area:
                            lost1 = True
                    if not lost2 and geo.has:
                        dy = py - geo.yped
                        if abs(dy) < r95:
                            hf = math.sqrt(r95 * r95 - dy * dy)
                            ov = min(px + hf, geo.xse) - max(px - hf, -geo.xse)
                            if ov >= geo.xse:
                                lost2 = True
                    prev = (px, py, r95, not lost1, not lost2)
                    if alert and (k - kpend) * DT >= TG:
                        alert = False; R['tg'] = True
                        if R['dur'] is None:
                            R['dur'] = TG
                    # lettura R-b: prova del raggio sulla posizione prevista
                    if R['relb'] is None:
                        xc, yc, ing = geo.cell(px, py)
                        if ing and geo.d_est(xc, yc) > G:
                            freeb += 1
                            if freeb >= 3:
                                R['relb'] = dict(t=(k - kpend) * DT, hidden=hidden, unseen=(z is None))
                        else:
                            freeb = 0
        nomeas = 0 if got else nomeas + 1
        # controlli contro la verita'
        if hidden and not got:
            R['n1'] += 1
            if not alert:
                if R['tg']:
                    R['n1_afterTG'] += 1
                else:
                    R['n1_nolayer'] += 1
            else:
                l1 = geo.layer1(x, y)
                if not l1[0]:
                    R['n1_out_i'] += 1
                if not l1[1]:
                    R['n1_out_ii'] += 1
        if ingrid and nomeas >= 3 and R['track']:
            R['n2'] += 1
            if wv < DEG1:
                inl = alert and geo.layer1(x, y)[1]
                if not inl and not R['tg']:
                    R['n2_fail'] += 1
        k += 1
    return R


BEH = ('prosegue', 'sosta', 'torna', 'lontano')


def agg_cell(geo, beh, curve, rho, N, seed, pd=1.0):
    rnd = random.Random(seed)
    A = dict(N=N, n1=0, out_i=0, out_ii=0, nolayer=0, afterTG=0, p_out_i=0, p_out_ii=0, p_nolayer=0, p_any=0,
             n2=0, n2f=0, p_n2f=0, openmiss=0, reem=0, c_s1=0, c_p1=0, c_s2=0, c_p2=0, c20_s1=0, c20_s2=0,
             in95=0, sh1=0, sh2=0, disc=0, c20=0, c40=0, relb=0, relb_h=0, tg=0, dmax=0.0, dsum=0.0, dn=0, notrack=0, over=0)
    for _ in range(N):
        R = run_pass(rnd, geo, beh, curve, rho, pd)
        A['n1'] += R['n1']; A['out_i'] += R['n1_out_i']; A['out_ii'] += R['n1_out_ii']
        A['nolayer'] += R['n1_nolayer']; A['afterTG'] += R['n1_afterTG']
        A['p_out_i'] += R['n1_out_i'] > 0; A['p_out_ii'] += R['n1_out_ii'] > 0; A['p_nolayer'] += R['n1_nolayer'] > 0; A['p_any'] += (R['n1_out_ii'] > 0 or R['n1_nolayer'] > 0)
        A['n2'] += R['n2']; A['n2f'] += R['n2_fail']; A['p_n2f'] += R['n2_fail'] > 0
        A['openmiss'] += R['openmiss']; A['notrack'] += not R['track']
        e = R['reem']
        if e is not None and not e['afterTG']:
            A['reem'] += 1; A['in95'] += e['in95']; A['sh1'] += e['s1']; A['sh2'] += e['s2']; A['disc'] += e['disc']
            c40 = e['in95'] and e['n40']; c20 = e['in95'] and e['n20']
            A['c_s1'] += c40 and e['s1']; A['c_p1'] += c40 and not e['s1']
            A['c_s2'] += c40 and e['s2']; A['c_p2'] += c40 and not e['s2']
            A['c20_s1'] += c20 and e['s1']; A['c20_s2'] += c20 and e['s2']; A['c20'] += c20; A['c40'] += c40
        b = R['relb']
        if b is not None:
            A['relb'] += 1; A['relb_h'] += b['hidden']
        A['tg'] += R['tg']
        if R['dur'] is not None:
            A['dn'] += 1; A['dsum'] += R['dur']; A['dmax'] = max(A['dmax'], R['dur'])
            A['over'] += R['dur'] > TG + 3 * DT + 1e-9
    return A


def pc(a, b):
    return 100.0 * a / b if b else float('nan')


def cmd_A(gname, w, N, curve='nom', pd=1.0):
    print("# prova A, geometria %s, pannello %.1f m, N=%d per cella, curva %s, Pd=%.2f, seme base %d" % (gname, w, N, curve, pd, SEED))
    yp, yped, rmax = (2.0, 4.0, 6.0) if gname == 'T' else (1.5, 2.5, 3.0)
    ci = 0
    for e in (-0.2, 0.0, 0.2):
        geo = Geo(yp, w, yped, rmax, e)
        print("== errore d'ombra %+.1f m; ombra vera %.2f m alla linea del pedone; area ombra stimata %.2f m2" % (e, 2 * geo.xs, geo.area))
        for beh in BEH:
            ci += 1
            A = agg_cell(geo, beh, curve, 0.20, N, SEED + (1 if gname == 'T' else 2) * 100000 + int(w * 10) * 1000 + ci, pd)
            print(" %-8s A1: N1=%d fotogr.; fuori(i)=%d [%d pass.] fuori(ii)=%d [%d pass.] senza strato=%d [%d pass.] dopoTg=%d | N2=%d fallimenti=%d [%d pass.] | mancati in campo aperto=%d senza traccia=%d"
                  % (beh, A['n1'], A['out_i'], A['p_out_i'], A['out_ii'], A['p_out_ii'], A['nolayer'], A['p_nolayer'], A['afterTG'],
                     A['n2'], A['n2f'], A['p_n2f'], A['openmiss'], A['notrack']))
            n = A['reem']
            print("          A3: riem=%d in95=%.1f%% | d1: cont+mostrato=%.1f%% cont+perso=%.1f%% | d2: cont+mostrato=%.1f%% cont+perso=%.1f%% | contenuta (resp., tol 0,40) %.1f%% ; tol 0,20 %.1f%% | A4 mostrato: d1 %.1f%% d2 %.1f%% | A5 disco=%.1f%%"
                  % (n, pc(A['in95'], n), pc(A['c_s1'], n), pc(A['c_p1'], n), pc(A['c_s2'], n), pc(A['c_p2'], n),
                     pc(A['c40'], n), pc(A['c20'], n), pc(A['sh1'], n), pc(A['sh2'], n), pc(A['disc'], n)))
            print("          A7: R-a durata media %.2f s max %.2f s (n=%d, oltre Tg+3f: %d, a Tg: %d) | R-b rilasci=%d di cui a soggetto nascosto=%d (%.1f%% dei passaggi)"
                  % (A['dsum'] / A['dn'] if A['dn'] else float('nan'), A['dmax'], A['dn'], A['over'], A['tg'], A['relb'], A['relb_h'], pc(A['relb_h'], N)))
            sys.stdout.flush()


def cmd_SWEEP(N):
    print("# sensibilita' di A1 all'errore d'ombra, geometria T, pannello 1 m, curva nom, N=%d per cella" % N)
    print("# errore corpo | passaggi con N1 fuori dallo strato 1 (lettura ii) o senza strato | passaggi con fallimento N2 ; su 3 comportamenti (prosegue, sosta, torna)")
    ci = 0
    for rho in (0.20, 0.30):
        for ie in range(-5, 6):
            e = ie * 0.1; geo = Geo(2.0, 1.0, 4.0, 6.0, e)
            f1 = f2 = tot = fr = n1 = 0
            for beh in ('prosegue', 'sosta', 'torna'):
                ci += 1
                A = agg_cell(geo, beh, 'nom', rho, N, SEED + 900000 + ci)
                f1 += A['p_any']; f2 += A['p_n2f']; tot += N
                fr += A['out_ii'] + A['nolayer']; n1 += A['n1']
            print(" e=%+.1f corpo=%.1f : N1 fuori %d/%d passaggi (%.2f%%), fotogrammi %d/%d (contenuti %.2f%%) ; N2 %d/%d"
                  % (e, 2 * rho, f1, tot, pc(f1, tot), fr, n1, 100 - pc(fr, n1), f2, tot))
            sys.stdout.flush()


def cmd_A2():
    print("# A2: area dello strato 1 (ombra stimata dilatata di g) su suolo davvero visibile; griglia 1 grado x 0,1 m")
    for (gname, yp, yped, rmax, ws) in (('T', 2.0, 4.0, 6.0, (1.0, 2.0)), ('D', 1.5, 2.5, 3.0, (0.5, 1.0))):
        for w in ws:
            for e in (-0.2, 0.0, 0.2):
                geo = Geo(yp, w, yped, rmax, e)
                al1 = avis = a60 = a40 = 0.0; dmax = 0.0; hidfree = 0.0
                for ti in range(-44, 44):
                    thc = math.radians(ti + 0.5)
                    if abs(thc) > HALF + 1e-9:
                        continue
                    for ri in range(5, int(round(rmax / 0.1))):
                        rc = (ri + 0.5) * 0.1; xc = rc * math.sin(thc); yc = rc * math.cos(thc)
                        ar = rc * DEG1 * 0.1
                        tr = geo.in_true(xc, yc)
                        if geo.d_est(xc, yc) <= G:
                            al1 += ar
                            if not tr:
                                avis += ar; dt = geo.d_true(xc, yc)
                                dmax = max(dmax, dt)
                                if dt > 0.60: a60 += ar
                                if dt > 0.40: a40 += ar
                        elif tr:
                            hidfree += ar
                print(" %s w=%.1f e=%+.1f: strato1 %.2f m2; su suolo visibile %.2f m2 (%.1f%%); oltre 0,40 m dal bordo vero %.2f m2 (%.1f%%); oltre 0,60 m %.3f m2; distanza max %.2f m; celle NASCOSTE fuori dallo strato 1 %.3f m2"
                      % (gname, w, e, al1, avis, pc(avis, al1), a40, pc(a40, al1), a60, dmax, hidfree))


# ----------------------------------------------------------------------------- prova B
def meas_noise(rnd, s, outl):
    if outl > 0 and rnd.random() < outl:
        return rnd.uniform(-0.5, 0.5)
    return rnd.gauss(0, s)


def cmd_WALL(nwin):
    print("# B1: muro fermo, %d finestre da 1 s per riga. falsi «mobile»: spost. (una valutazione per finestra | almeno una su 15 scorrevoli) ; chi2 (fotogrammi | finestre con almeno uno) ; v1a v1b (una valutazione per finestra)" % nwin)
    ci = 0
    for curve in ('nom', 'lim', 'tor'):
        for z in (2.0, 3.0, 4.0):
            for (mism, outl) in ((1.0, 0.0), (0.5, 0.0), (1 / 3.0, 0.0), (1.0, 0.02)):
                ci += 1; rnd = random.Random(SEED + 500000 + ci)
                sr = sig_r(z, curve); st = sig_t(z); srb = sr * mism; stb = st * mism
                thr = 5 * srb * SQ2; tht = 5 * stb * SQ2; k3 = math.sqrt(1 / 3.0)
                n = nwin * 15 + 18
                xs = [meas_noise(rnd, st, outl) for _ in range(n)]
                ys = [z + meas_noise(rnd, sr, outl) for _ in range(n)]
                kx = KF1(xs[0], xs[1], DT, stb * stb); ky = KF1(ys[0], ys[1], DT, srb * srb)
                d_one = d_any = c_fr = c_win = a_one = b_one = 0; anyd = anyc = False
                Rx = stb * stb; Ry = srb * srb
                for k in range(2, n):
                    kx.predict(); ky.predict(); kx.update(xs[k], Rx); ky.update(ys[k], Ry)
                    if k < 18:
                        continue
                    fc = kx.v * kx.v / kx.c + ky.v * ky.v / ky.c > CHI99
                    fd = abs(ys[k] - ys[k - 15]) > thr or abs(xs[k] - xs[k - 15]) > tht
                    c_fr += fc; anyd = anyd or fd; anyc = anyc or fc
                    if (k - 18) % 15 == 14:
                        d_one += fd; d_any += anyd; c_win += anyc; anyd = anyc = False
                        ma = (ys[k] + ys[k - 1] + ys[k - 2]) / 3; mb = (ys[k - 13] + ys[k - 14] + ys[k - 15]) / 3; mc = (ys[k - 15] + ys[k - 16] + ys[k - 17]) / 3
                        na = (xs[k] + xs[k - 1] + xs[k - 2]) / 3; nb = (xs[k - 13] + xs[k - 14] + xs[k - 15]) / 3; nc = (xs[k - 15] + xs[k - 16] + xs[k - 17]) / 3
                        a_one += abs(ma - mb) > thr * k3 or abs(na - nb) > tht * k3
                        b_one += abs(ma - mc) > thr * k3 or abs(na - nc) > tht * k3
                print(" %s z=%.0f m sigma_r=%.1f cm creduto x%.2f anomale %.0f%%: spost %.3f%% | %.3f%% ; chi2 %.3f%% | %.3f%% ; v1a %.3f%% v1b %.3f%%"
                      % (curve, z, sr * 100, mism, outl * 100, pc(d_one, nwin), pc(d_any, nwin), pc(c_fr, n - 18), pc(c_win, nwin), pc(a_one, nwin), pc(b_one, nwin)))
                sys.stdout.flush()


def ped_pass(rnd, curve, z0, radial, v, mism, outl, nfr=31):
    """-> (k primo «mobile» spostamento, chi2, v1a, v1b) ; None se mai"""
    xs = []; ys = []; zz = []
    kd = kc = ka = kb = None; kx = ky = None; k3 = math.sqrt(1 / 3.0)
    for k in range(nfr):
        t = k * DT
        tx, ty = (0.0, z0 - v * t) if radial else (v * t, z0)
        r = math.hypot(tx, ty); sr = sig_r(r, curve); st = sig_t(r)
        mx = tx + meas_noise(rnd, st, outl); my = ty + meas_noise(rnd, sr, outl)
        xs.append(mx); ys.append(my); rm = math.hypot(mx, my); zz.append(rm)
        Rx = (sig_t(rm) * mism) ** 2; Ry = (sig_r(rm, curve) * mism) ** 2
        if k == 1:
            kx = KF1(xs[0], mx, DT, Rx); ky = KF1(ys[0], my, DT, Ry)
        elif k >= 2:
            kx.predict(); ky.predict(); kx.update(mx, Rx); ky.update(my, Ry)
            if kc is None and kx.v * kx.v / kx.c + ky.v * ky.v / ky.c > CHI99:
                kc = k
        if k >= 15:
            zf = max(zz[k], zz[k - 15]); thr = 5 * sig_r(zf, curve) * mism * SQ2; tht = 5 * sig_t(zf) * mism * SQ2
            if kd is None and (abs(my - ys[k - 15]) > thr or abs(mx - xs[k - 15]) > tht):
                kd = k
            if ka is None:
                ma = (ys[k] + ys[k - 1] + ys[k - 2]) / 3 - (ys[k - 13] + ys[k - 14] + ys[k - 15]) / 3
                na = (xs[k] + xs[k - 1] + xs[k - 2]) / 3 - (xs[k - 13] + xs[k - 14] + xs[k - 15]) / 3
                if abs(ma) > thr * k3 or abs(na) > tht * k3:
                    ka = k
        if k >= 17 and kb is None:
            zf = max(zz[k], zz[k - 17]); thr = 5 * sig_r(zf, curve) * mism * SQ2; tht = 5 * sig_t(zf) * mism * SQ2
            mb = (ys[k] + ys[k - 1] + ys[k - 2]) / 3 - (ys[k - 15] + ys[k - 16] + ys[k - 17]) / 3
            nb = (xs[k] + xs[k - 1] + xs[k - 2]) / 3 - (xs[k - 15] + xs[k - 16] + xs[k - 17]) / 3
            if abs(mb) > thr * k3 or abs(nb) > tht * k3:
                kb = k
    return kd, kc, ka, kb


def frac(lst, lim):
    return 100.0 * sum(1 for q in lst if q is not None and q <= lim) / len(lst)


def cmd_PED(N):
    print("# B2-B4: pedone a 0,5 m/s, N=%d per riga; quota con prima etichetta «mobile» entro 1 s + 1 fotogramma (k<=16) [entro 1,5 s, k<=22]; stessi semi per le due regole" % N)
    ci = 0
    for curve in ('nom', 'lim', 'tor'):
        for z0 in (2.0, 3.0, 4.0):
            for radial in (False, True):
                for (mism, outl) in ((1.0, 0.0), (0.5, 0.0), (1 / 3.0, 0.0), (1.0, 0.02)):
                    ci += 1; rnd = random.Random(SEED + 700000 + ci)
                    res = [ped_pass(rnd, curve, z0, radial, 0.5, mism, outl) for _ in range(N)]
                    d = [r[0] for r in res]; c = [r[1] for r in res]; a = [r[2] for r in res]; b = [r[3] for r in res]
                    print(" %s da %.0f m %-12s creduto x%.2f anomale %.0f%%: spost %.1f%% [%.1f%%] ; chi2 %.1f%% [%.1f%%] ; v1a %.1f%% ; v1b (k<=18) %.1f%%"
                          % (curve, z0, 'avvicinam.' if radial else 'di traverso', mism, outl * 100,
                             frac(d, 16), frac(d, 22), frac(c, 16), frac(c, 22), frac(a, 16), frac(b, 18)))
        sys.stdout.flush()


def cmd_V1(N):
    print("# validazione-1: velocita' minima vista in avvicinamento da 2 m (quota entro il limite), N=%d per velocita'" % N)
    for curve in ('tor', 'lim', 'nom'):
        rows = []
        for iv in range(1, 15):
            v = iv * 0.05; rnd = random.Random(SEED + 800000 + iv)
            res = [ped_pass(rnd, curve, 2.0, True, v, 1.0, 0.0) for _ in range(N)]
            rows.append((v, frac([r[0] for r in res], 16), frac([r[2] for r in res], 16), frac([r[3] for r in res], 18)))
        def v90(col):
            for i in range(1, len(rows)):
                if rows[i][col] >= 90.0 > rows[i - 1][col]:
                    a, b = rows[i - 1], rows[i]
                    return a[0] + (90.0 - a[col]) * (b[0] - a[0]) / (b[col] - a[col])
            return float('nan') if rows[0][col] < 90 else rows[0][0]
        print(" curva %s: " % curve + " ".join("v=%.2f:%.0f/%.0f/%.0f" % r for r in rows))
        b, a1, b1 = v90(1), v90(2), v90(3)
        print("   v al 90%%: base %.3f m/s ; v1a %.3f (guadagno %.2f) ; v1b %.3f (guadagno %.2f)" % (b, a1, b / a1, b1, b / b1))


def cmd_A6(N):
    print("# A6: due bersagli da lati opposti (il secondo specchiato), sfasamento U(-1.5,1.5) s, geometria T, e=0, N=%d coppie per riga" % N)
    print("# regola della soluzione: se pendono due tracce nella stessa ombra -> «identita' ambigua» (non consuma le pendenti); una sola -> riaggancio")
    for w in (1.0, 2.0):
        geo = Geo(2.0, w, 4.0, 6.0, 0.0)
        for (b1, b2) in (('prosegue', 'prosegue'), ('torna', 'torna'), ('prosegue', 'sosta'), ('sosta', 'torna')):
            rnd = random.Random(SEED + 600000 + int(w) * 100 + BEH.index(b1) * 10 + BEH.index(b2))
            ev = amb = muti = both = 0
            for _ in range(N):
                Ra = run_pass(rnd, geo, b1, 'nom', 0.20); Rb = run_pass(rnd, geo, b2, 'nom', 0.20)
                if Ra['reem'] is None or Rb['reem'] is None or 'tl' not in Ra or 'tl' not in Rb:
                    continue
                off = rnd.uniform(-1.5, 1.5)
                a = (Ra['tl'], Ra['reem']['tf']); b = (Rb['tl'] + off, Rb['reem']['tf'] + off)
                both += 1
                for (me, ot) in ((a, b), (b, a)):
                    ev += 1
                    pend_other = ot[0] < me[1] and not (ot[1] < me[0])
                    if pend_other:
                        amb += 1
                    # con una sola pendente la traccia pendente e' la propria: nessuno scambio possibile
            print(" w=%.0f m %s+%s: coppie %d, riemersioni %d, «ambigua» dichiarata %.1f%%, scambi muti %d" % (w, b1, b2, both, ev, pc(amb, ev), muti))


# ====================================================================== versione 2
def observe2(geo, x, y, rho, rnd, curve, det):
    """-> (larghezza visibile rad, tagliato, colonna del centro visibile, misura o None)"""
    r = math.hypot(x, y); th = math.atan2(x, y)
    if r > geo.rmax or r <= rho:
        return 0.0, False, False, None
    al = math.asin(rho / r)
    lo = max(th - al, -HALF); hi = min(th + al, HALF)
    if hi <= lo:
        return 0.0, False, False, None
    cut = False
    if y > geo.yp:
        w1 = max(0.0, min(hi, -geo.Ap) - lo); l2 = max(lo, geo.Ap); w2 = max(0.0, hi - l2)
        cut = hi > -geo.Ap and lo < geo.Ap
        if w1 >= w2:
            wv = w1; tm = lo + 0.5 * w1
        else:
            wv = w2; tm = l2 + 0.5 * w2
        cvis = geo.Ap < abs(th) <= HALF
    else:
        wv = hi - lo; tm = 0.5 * (lo + hi); cvis = abs(th) <= HALF
    ok = (wv >= 3 * DEG1) if det == 'col' else (wv * r >= 0.15)
    if not ok:
        return wv, cut, cvis and wv >= DEG1, None
    sr = sig_r(r, curve); st = sig_t(r)
    zr = r + rnd.gauss(0, sr); xi = rnd.gauss(0, st)
    sn = math.sin(tm); cs = math.cos(tm)
    return wv, cut, cvis, (zr * sn + xi * cs, zr * cs - xi * sn,
                           st * st * cs * cs + sr * sr * sn * sn, sr * sr * cs * cs + st * st * sn * sn, sr)


def traj(rnd, geo, beh):
    yped = geo.yped; xs = geo.xs
    xvis = min(yped * math.tan(HALF), math.sqrt(max(geo.rmax ** 2 - yped ** 2, 0.0)))
    x0 = -min(xs + 2.0, xvis - 0.25); xend = -x0
    v = rnd.uniform(0.8, 1.4)
    xstop = rnd.uniform(-xs + 0.2, xs - 0.2) if xs > 0.2 else 0.0
    x, y, vx, vy = x0, yped, v, 0.0
    phase = 0; timer = 0.0; t4 = None; out = [(x, y)]; k = 0
    while k < 600:
        k += 1
        if phase == 0:
            tx, ty = v, 0.0
            if beh != 'prosegue' and x >= xstop - v * v / (2 * ACC):
                phase = 1
        if phase == 1:
            tx, ty = 0.0, 0.0
            if math.hypot(vx, vy) < 0.02:
                vx = vy = 0.0
                if beh == 'sosta':
                    phase = 2; timer = rnd.uniform(2.0, 4.0)
                elif beh == 'torna':
                    phase = 3
                else:
                    phase = 4; t4 = k
        if phase == 2:
            tx, ty = 0.0, 0.0; timer -= DT
            if timer <= 0:
                phase = 5
        elif phase == 3:
            tx, ty = -v, 0.0
        elif phase == 4:
            rr = math.hypot(x, y); tx, ty = v * x / rr, v * y / rr
        elif phase == 5:
            tx, ty = v, 0.0
        dvx = tx - vx; dvy = ty - vy; n = math.hypot(dvx, dvy)
        if n <= ACC * DT:
            vx, vy = tx, ty
        else:
            vx += dvx / n * ACC * DT; vy += dvy / n * ACC * DT
        x += vx * DT; y += vy * DT
        if beh in ('prosegue', 'sosta') and x >= xend:
            break
        if beh == 'torna' and phase == 3 and x <= x0:
            break
        if beh == 'lontano' and t4 is not None and (k - t4) * DT >= 12.5:
            break
        out.append((x, y))
    return out


def c1_ok(geo, zx, zy, band):
    r = math.hypot(zx, zy); th = abs(math.atan2(zx, zy))
    return geo.d_est(zx, zy) <= band and geo.rmax - r > 0.40 and r * math.sin(max(HALF - th, 0.0)) > 0.40


def pass_v2(rnd, geo, beh, curve, band, det, c6, pd=1.0, rho=0.20, cutentry=False):
    P = traj(rnd, geo, beh)
    kx = ky = None; first = None
    pending = False; alert = False; closed = False; lost = False; newtrack = False
    unconf = 0; lastdet = None; lastcut = False; kpend = -1; klost = -1; kuse = -1
    R = dict(fail=0, closed=False, entered=False, reem=False, reatt=False, shown=False, durprev=None,
             tperso=None, in95=None, tdark=None, track=False)
    waitin95 = False
    for k, (x, y) in enumerate(P):
        wv, cut, cvis, z = observe2(geo, x, y, rho, rnd, curve, det)
        if z is not None and pd < 1.0 and rnd.random() > pd:
            z = None
        got = z is not None
        use = got and not (c6 and cut)
        if kx is None:
            if use:
                if first is None:
                    first = (z, k)
                else:
                    (z1, k1) = first; dt = (k - k1) * DT
                    kx = KF1(z1[0], z[0], dt, z[2]); ky = KF1(z1[1], z[1], dt, z[3]); kuse = k; R['track'] = True
            if got:
                lastdet = (z[0], z[1], k); lastcut = cut
        else:
            kx.predict(); ky.predict()
            if got:
                if pending and not newtrack:
                    ok = c1_ok(geo, z[0], z[1], band)
                    if not R['reem']:
                        R['reem'] = True; R['reatt'] = ok; R['shown'] = not lost
                        R['tdark'] = (k - lastdet[2]) * DT
                        R['durprev'] = ((klost if lost else k) - kpend) * DT
                        R['tperso'] = (k - klost) * DT if lost else 0.0
                        waitin95 = True
                    if ok:
                        pending = False; alert = False
                    else:
                        newtrack = True                    # «identita' ambigua»: lo strato 1 resta
                if use and not closed and not newtrack:
                    dx = z[0] - kx.p; dy = z[1] - ky.p
                    d2 = dx * dx / (kx.a + z[2]) + dy * dy / (ky.a + z[3])
                    if waitin95:
                        R['in95'] = d2 <= CHI95; waitin95 = False
                    if d2 <= CHI99:
                        kx.update(z[0], z[2]); ky.update(z[1], z[3])
                    else:
                        kx.p = z[0]; kx.v = 0.0; kx.a = z[2]; kx.b = 0.0; kx.c = 1.0
                        ky.p = z[1]; ky.v = 0.0; ky.a = z[3]; ky.b = 0.0; ky.c = 1.0
                    kuse = k
                lastdet = (z[0], z[1], k); lastcut = cut; unconf = 0
            else:
                if not pending and not closed and lastdet is not None:
                    if geo.d_est(lastdet[0], lastdet[1]) <= band or (cutentry and lastcut):
                        pending = True; alert = True; kpend = k; lost = False; R['entered'] = True
                    else:
                        unconf += 1
                        if unconf > 3:
                            closed = True; R['closed'] = True
                if pending and not lost and geo.has:
                    r95 = math.sqrt(CHI95 * max(kx.a, ky.a))
                    if math.pi * r95 * r95 >= 0.5 * geo.area:
                        px, py = kx.p, ky.p; cnt = 0; n = int(r95 / 0.1) + 1; i = -n; r2 = r95 * r95
                        while i <= n:
                            qx = px + i * 0.1; j = -n
                            while j <= n:
                                if (i * i + j * j) * 0.01 <= r2:
                                    qy = py + j * 0.1
                                    if geo.in_est(qx, qy) and math.hypot(qx, qy) <= geo.rmax:
                                        cnt += 1
                                j += 1
                            i += 1
                        if cnt * 0.01 >= 0.5 * geo.area:
                            lost = True; klost = k
        if not got:
            xc, yc, ing = geo.cell(x, y)
            if ing and not geo.in_est(xc, yc) and not (cvis and wv >= DEG1):
                if not (alert and geo.d_est(xc, yc) <= band):
                    R['fail'] += 1
    return R


def med(v):
    v = sorted(v)
    return v[len(v) // 2] if v else float('nan')


GEOS = {'DC': (1.9, 1.0, 2.3, 3.0), 'T1': (2.0, 1.0, 4.0, 6.0), 'T2': (2.0, 2.0, 4.0, 6.0),
        'D05': (1.5, 0.5, 2.5, 3.0), 'D1': (1.5, 1.0, 2.5, 3.0)}


def cmd_R8(N, pd=1.0, cutentry=False):
    print("# R8 regola nuova (cuneo tagliato alla griglia + fascia; nessun tetto; ingresso dall'ultima misura; C1; C6; w_min 0,15 m), N=%d per cella, Pd=%.2f, ingresso anche da gruppo tagliato=%s" % (N, pd, cutentry))
    ci = 0
    for gname in ('DC', 'T1', 'T2'):
        yp, w, yped, rmax = GEOS[gname]
        for (band, e, lab) in ((0.40, -0.2, 'principale'), (0.40, 0.0, 'principale'), (0.40, 0.2, 'principale'),
                               (0.0, -0.2, 'BRACCIO'), (0.20, -0.2, 'BRACCIO'), (0.40, -0.4, 'BRACCIO')):
            geo = Geo(yp, w, yped, rmax, e)
            for beh in BEH:
                ci += 1; rnd = random.Random(SEED + 2000000 + ci)
                f = cl = en = re = ra = sh = 0; dp = []; tp = []; td = []
                for _ in range(N):
                    R = pass_v2(rnd, geo, beh, 'nom', band, 'wmin', True, pd, 0.20, cutentry)
                    f += R['fail'] > 0; cl += R['closed']; en += R['entered']
                    if R['reem']:
                        re += 1; ra += R['reatt']; sh += R['shown']; dp.append(R['durprev']); tp.append(R['tperso']); td.append(R['tdark'])
                print(" %s %-10s fascia %.2f errore %+.1f %-8s: falliti %d/%d ; traccia chiusa in campo aperto %d ; entrata in ombra %d ; riemersioni %d riagganciate %.1f%% ; previsto mostrato alla riem. %.1f%% ; mediane: buio %.2f s, previsto %.2f s, perso %.2f s"
                      % (gname, lab, band, e, beh, f, N, cl, en, re, pc(ra, re), pc(sh, re), med(td), med(dp), med(tp)))
            sys.stdout.flush()


def cmd_C6(N):
    print("# «contiene alla riemersione» = prima misura usata dal filtro dopo il buio dentro il cerchio al 95%%; con e senza C6; N=%d; errore 0; curva nom" % N)
    ci = 0
    for gname in ('D05', 'D1', 'DC', 'T1'):
        yp, w, yped, rmax = GEOS[gname]; geo = Geo(yp, w, yped, rmax, 0.0)
        for det in ('col', 'wmin'):
            for beh in ('prosegue', 'sosta', 'torna'):
                n = N if beh == 'prosegue' else N // 5
                row = []
                for c6 in (False, True):
                    ci += 1; rnd = random.Random(SEED + 3000000 + ci // 2 * 2)
                    ok = tot = sh = 0; td = []
                    for _ in range(n):
                        R = pass_v2(rnd, geo, beh, 'nom', 0.40, det, c6)
                        if R['in95'] is not None:
                            tot += 1; ok += R['in95']; sh += R['shown']; td.append(R['tdark'])
                    row.append("%s: %.1f%% (n=%d; mostrato %.1f%%; buio %.2f s)" % ('con C6' if c6 else 'senza C6', pc(ok, tot), tot, pc(sh, tot), med(td)))
                print(" %s rilevatore %-4s %-8s %s | %s" % (gname, det, beh, row[0], row[1]))
        sys.stdout.flush()


def cmd_SECOND(N):
    print("# secondo soggetto mai tracciato, con una traccia pendente nell'ombra: riaggancio (sbagliato) secondo C1 su una delle sue prime 3 rilevazioni; N=%d" % N)
    ci = 0
    for gname in ('DC', 'T1'):
        yp, w, yped, rmax = GEOS[gname]
        for e in (-0.2, 0.0, 0.2):
            geo = Geo(yp, w, yped, rmax, e); res = []
            for kind in ('campo', 'portata', 'ombra'):
                ci += 1; rnd = random.Random(SEED + 4000000 + ci); wrong = seen = 0
                for _ in range(N):
                    v = rnd.uniform(0.8, 1.4)
                    if kind == 'campo':
                        x, y, vx, vy = -(yped * math.tan(HALF) + 0.6), yped, v, 0.0
                    elif kind == 'portata':
                        while True:
                            th = rnd.uniform(-HALF + 2 * DEG1, HALF - 2 * DEG1)
                            if abs(th) > geo.Ap + 0.1:
                                break
                        x, y = (rmax + 1.0) * math.sin(th), (rmax + 1.0) * math.cos(th); vx, vy = -v * math.sin(th), -v * math.cos(th)
                    else:
                        x, y, vx, vy = rnd.uniform(-geo.xs + 0.2, geo.xs - 0.2), yped, v, 0.0
                    nd = 0; bad = False
                    for k in range(200):
                        x += vx * DT; y += vy * DT
                        wv, cut, cvis, z = observe2(geo, x, y, 0.20, rnd, 'nom', 'wmin')
                        if z is not None:
                            nd += 1
                            if c1_ok(geo, z[0], z[1], 0.40):
                                bad = True
                            if nd >= 3:
                                break
                    seen += nd > 0; wrong += bad
                res.append("%s %d/%d" % (kind, wrong, seen))
            print(" %s errore %+.1f: riagganci sbagliati: %s" % (gname, e, " ; ".join(res)))


def mob_final(xs, ys, zz, valid, curve, mism=1.0):
    """primo k con etichetta «mobile»: finestra che cresce (<= 1 s), medie di 3 fotogrammi validi consecutivi"""
    k3 = math.sqrt(1 / 3.0); M = {}
    for k in range(2, len(xs)):
        if valid[k] and valid[k - 1] and valid[k - 2]:
            M[k] = ((xs[k] + xs[k - 1] + xs[k - 2]) / 3, (ys[k] + ys[k - 1] + ys[k - 2]) / 3, max(zz[k], zz[k - 1], zz[k - 2]))
            for j in range(max(2, k - 15), k - 2):
                if j in M:
                    zf = max(M[k][2], M[j][2])
                    if abs(M[k][1] - M[j][1]) > 5 * sig_r(zf, curve) * mism * SQ2 * k3 or abs(M[k][0] - M[j][0]) > 5 * sig_t(zf) * mism * SQ2 * k3:
                        return k
                    break
    return None


def cmd_MOB(N):
    print("# regola «mobile» finale (finestra che cresce, media di 3): quota vista entro 1,0 s (k<=15) [entro 1 s + 1 fotogramma], 0,5 m/s, N=%d; fermo: etichette false entro 1 s, N=%d" % (N, 2 * N))
    ci = 0
    for curve in ('nom', 'lim', 'tor'):
        for z0 in (2.0, 3.0):
            out = []
            for (lab, radial, v, n) in (('di traverso', False, 0.5, N), ('avvicinam.', True, 0.5, N), ('FERMO', True, 0.0, 2 * N)):
                ci += 1; rnd = random.Random(SEED + 5000000 + ci); ks = []
                for _ in range(n):
                    xs = []; ys = []; zz = []
                    for k in range(18):
                        t = k * DT; tx, ty = (0.0, z0 - v * t) if radial else (v * t, z0)
                        r = math.hypot(tx, ty)
                        mx = tx + rnd.gauss(0, sig_t(r)); my = ty + rnd.gauss(0, sig_r(r, curve))
                        xs.append(mx); ys.append(my); zz.append(math.hypot(mx, my))
                    ks.append(mob_final(xs, ys, zz, [True] * 18, curve))
                out.append("%s %.2f%% [%.2f%%]" % (lab, frac(ks, 15), frac(ks, 16)))
            print(" %s da %.0f m: %s" % (curve, z0, " ; ".join(out)))


def cmd_WALLP(N):
    print("# muro fermo (largo 1,2 m a 2,8 m) con una persona (40 cm) che passa a 1,6 m: passaggi con almeno un'etichetta «mobile» falsa sul muro; N=%d" % N)
    ci = 0; yw = 2.8; hw = 0.6; yq = 1.6
    for curve in ('nom', 'lim', 'tor'):
        ci += 1; res = {}
        for c6 in (False, True):
            rnd = random.Random(SEED + 6000000 + ci); bad = 0; nopers = 0
            for _ in range(N):
                v = rnd.uniform(0.8, 1.4); xp = -2.6
                a1 = math.atan2(-hw, yw); a2 = math.atan2(hw, yw)
                xs = []; ys = []; zz = []; valid = []
                while xp < 2.6:
                    xp += v * DT
                    rp = math.hypot(xp, yq); tp = math.atan2(xp, yq); al = math.asin(0.2 / rp)
                    lo, hi = tp - al, tp + al
                    cutw = hi > a1 and lo < a2
                    w1 = max(0.0, min(a2, lo) - a1); l2 = max(a1, hi); w2 = max(0.0, a2 - l2)
                    if not cutw:
                        tm = 0.0
                    elif w1 >= w2:
                        tm = a1 + 0.5 * w1
                    else:
                        tm = l2 + 0.5 * w2
                    if max(w1, w2) < 3 * DEG1 and cutw:
                        xs.append(0.0); ys.append(yw); zz.append(yw); valid.append(False); continue
                    mx = yw * math.tan(tm) + rnd.gauss(0, sig_t(yw)); my = yw + rnd.gauss(0, sig_r(yw, curve))
                    xs.append(mx); ys.append(my); zz.append(math.hypot(mx, my)); valid.append(not (c6 and cutw))
                bad += mob_final(xs, ys, zz, valid, curve) is not None
            res[c6] = bad
        print(" curva %s: senza C6 %d/%d (%.1f%%) ; con C6 %d/%d (%.1f%%)" % (curve, res[False], N, pc(res[False], N), res[True], N, pc(res[True], N)))


def cmd_PD(N):
    print("# Pd 0,9, attraversamento di 4 s (60 fotogrammi) in campo aperto, N=%d: tracce vere chiuse dalla regola «non confermato»" % N)
    rnd = random.Random(SEED + 7000000); c4 = c3 = 0
    for _ in range(N):
        run = mx = 0
        for k in range(60):
            if rnd.random() > 0.9:
                run += 1; mx = max(mx, run)
            else:
                run = 0
        c4 += mx >= 4; c3 += mx >= 3
    print(" chiuse al quarto mancato di fila: %d/%d (%.2f%%) ; se si chiude al terzo: %d/%d (%.2f%%)" % (c4, N, pc(c4, N), c3, N, pc(c3, N)))


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'R8':
        cmd_R8(int(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 1.0, len(sys.argv) > 4 and sys.argv[4] == 'cut')
    elif c == 'C6':
        cmd_C6(int(sys.argv[2]))
    elif c == 'SECOND':
        cmd_SECOND(int(sys.argv[2]))
    elif c == 'MOB':
        cmd_MOB(int(sys.argv[2]))
    elif c == 'WALLP':
        cmd_WALLP(int(sys.argv[2]))
    elif c == 'PD':
        cmd_PD(int(sys.argv[2]))
