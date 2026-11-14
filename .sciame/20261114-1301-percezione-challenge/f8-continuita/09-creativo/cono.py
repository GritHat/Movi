#!/usr/bin/env python3
"""sciame-creativo, f8: «cono degli analoghi sfoltito alle bocche» contro il nucleo e due linee di base.
Python puro, semi fissati. Uso:
  PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 cono.py <w> <comportamenti separati da virgola> [N=100] [eps=0.05] [dw=0.0] [nm=400]
Scena, traiettorie di prova e filtro: COPIE di vis(), truth(), KF di f2/04-torneo/scena_parte3.py (avversario).
Libreria degli analoghi: COPIA di g1() di f2/04-torneo/torneo_parte2.py (avversario).
Miei: truth_mio() (rallenta, svolta), la classe Cono, le misure.
"""
import bisect, heapq, math, random, sys, time

DT = 1 / 15.; SIG = 0.05; R = SIG * SIG; PD = 0.9; FOV = math.radians(43.5); RMAX = 6.0; YP = 2.0
Q = 0.2; CHI95 = 5.991; VMAX = 2.5
GX0, GY0, GNX, GNY, CELL = -8.0, -2.0, 160, 100, 0.1      # griglia fine (maschere)
C2 = 0.25; NX2 = 64; NY2 = 40                              # griglia delle regioni
GUARD = 0.2; PDM = 0.9
TAUS = {8: 0.5, 15: 1.0, 30: 2.0, 45: 3.0, 60: 4.0, 75: 5.0}
CAP = 82


# ------------------------------------------------------------------ COPIE (scena_parte3.py)
def vis(x, y, w):
    """0 = non osservato (fuori campo o portata), 1 = visto (libero), 2 = in ombra del pannello."""
    if y <= 0.05: return 0
    if x * x + y * y > RMAX * RMAX or abs(math.atan2(x, y)) > FOV: return 0
    if w > 0 and y > YP and abs(x * YP / y) <= w / 2: return 2
    return 1


class KF:
    def __init__(s, z1, z2, dk):
        s.x, s.y = z2; s.vx = (z2[0] - z1[0]) / (DT * dk); s.vy = (z2[1] - z1[1]) / (DT * dk)
        s.a = R; s.b = R / (DT * dk); s.c = 2 * R / (DT * dk) ** 2
    def predict(s):
        s.x += s.vx * DT; s.y += s.vy * DT; a, b, c = s.a, s.b, s.c
        s.a = a + 2 * b * DT + c * DT * DT + Q * DT ** 3 / 3; s.b = b + c * DT + Q * DT * DT / 2; s.c = c + Q * DT
    def update(s, z):
        S = s.a + R; k1 = s.a / S; k2 = s.b / S; ex = z[0] - s.x; ey = z[1] - s.y
        s.x += k1 * ex; s.y += k1 * ey; s.vx += k2 * ex; s.vy += k2 * ey
        a, b, c = s.a, s.b, s.c; s.a = (1 - k1) * a; s.b = (1 - k1) * b; s.c = c - k2 * b
    def rad(s): return math.sqrt(CHI95 * s.a)


def truth(beh, w, rng, v=None, yped=4.0, sign=1):
    W = w / 2 * yped / YP; v = v or rng.uniform(1.0, 1.5); x, y = -3.7 * yped / 4, yped; hx, hy = 1.0, 0.0; xs = None; dwell = 0
    if beh == 'sosta': xs = rng.uniform(-W + 0.05, W - 0.05); dwell = rng.uniform(2, 4)
    elif beh in ('torna', 'lontano'): xs = rng.uniform(-W + 0.3, W - 0.3)
    ph = 0; out = []
    for k in range(int(14 / DT)):
        out.append((sign * x, y))
        if ph == 0 and xs is not None and x >= xs:
            if beh == 'sosta': ph = 1
            elif beh == 'torna': hx = -1.0; ph = 2
            else: r = math.hypot(x, y); hx, hy = x / r, y / r; ph = 2
        if ph == 1:
            dwell -= DT
            if dwell <= 0: ph = 2
            continue
        if beh == 'lontano' and ph == 2 and math.hypot(x, y) > RMAX + 0.5: continue
        x += hx * v * DT; y += hy * v * DT
        if abs(x) > 4.3: break
    return out


# ------------------------------------------------------------------ COPIA (torneo_parte2.py)
NV = 30
def g1(rnd, D, kind=None):
    """Generatore dell'avversario. Miscela 60/15/10/15; manovra a istante uniforme nell'occlusione; transizione in 0,5 s."""
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


# ------------------------------------------------------------------ MIO
def truth_mio(beh, w, rng, yped=4.0):
    """rallenta (x0,3-0,5) e svolta (45-90 gradi) dentro l'ombra: aggiunte mie, stessa forma di truth()."""
    W = w / 2 * yped / YP; v = rng.uniform(1.0, 1.5); x, y = -3.7 * yped / 4, yped; hx, hy = 1.0, 0.0
    xs = rng.uniform(-W + 0.3, W - 0.3); f = rng.uniform(0.3, 0.5)
    a = rng.choice((-1, 1)) * rng.uniform(math.pi / 4, math.pi / 2); ph = 0; out = []
    for k in range(int(14 / DT)):
        out.append((x, y))
        if ph == 0 and x >= xs:
            ph = 2
            if beh == 'rallenta': v *= f
            else: hx, hy = math.cos(a), math.sin(a)
        nx, ny = x + hx * v * DT, y + hy * v * DT
        if math.hypot(nx, ny) > RMAX + 0.5: continue                 # fuori portata: resta li'
        if ny < YP + 0.3 and abs(nx) < w / 2 + 0.3: continue           # arrivato dietro il pannello: si ferma
        x, y = nx, ny
        if abs(x) > 4.3 or y < 0.3: break
    return out


def make_lib(n, seed):
    """n membri: spostamenti canonici (direzione iniziale lungo +x) dall'istante d'ingresso, per 6 s."""
    rnd = random.Random(seed); lib = []
    while len(lib) < n:
        tr, kind = g1(rnd, 6.0)
        x0, y0 = tr[NV]; xa, ya = tr[NV - 3]
        sp = math.hypot(x0 - xa, y0 - ya) / (3 * DT)
        if sp < 0.2: continue
        c, s = (x0 - xa) / (sp * 3 * DT), (y0 - ya) / (sp * 3 * DT)
        dx = [((p[0] - x0) * c + (p[1] - y0) * s) for p in tr[NV:]]
        dy = [(-(p[0] - x0) * s + (p[1] - y0) * c) for p in tr[NV:]]
        lib.append((sp, dx, dy, kind))
    return lib


_M = {}
def masks(w, west):
    """griglie fini: verita' (vis) e 'libero oltre la fascia' con l'ombra stimata; griglia 0,25 m non libera."""
    k = (round(w, 3), round(west, 3))
    if k in _M: return _M[k]
    g = GUARD; d = g * 0.7071
    offs = ((0, 0), (g, 0), (-g, 0), (0, g), (0, -g), (d, d), (d, -d), (-d, d), (-d, -d))
    fg = bytearray(GNX * GNY); nsh = 0
    for j in range(GNY):
        y = GY0 + (j + .5) * CELL
        for i in range(GNX):
            x = GX0 + (i + .5) * CELL
            if vis(x, y, w) == 2: nsh += 1
            if all(vis(x + ox, y + oy, west) == 1 for ox, oy in offs): fg[j * GNX + i] = 1
    nf2 = bytearray(NX2 * NY2)   # 1 = cella 0,25 m NON libera (centro)
    for j in range(NY2):
        for i in range(NX2):
            x = GX0 + (i + .5) * C2; y = GY0 + (j + .5) * C2
            if not fg[int((y - GY0) / CELL) * GNX + int((x - GX0) / CELL)]: nf2[j * NX2 + i] = 1
    _M[k] = (fg, nf2, nsh * CELL * CELL)
    return _M[k]


def flood(nf2, px, py):
    """distanza geodetica dal punto d'ingresso passando solo per celle non libere (Dijkstra, 8 vicini)."""
    INF = 1e9; dist = [INF] * (NX2 * NY2); h = []
    for rad in (0.4, 0.8, 1.6):
        for j in range(NY2):
            y = GY0 + (j + .5) * C2
            if abs(y - py) > rad: continue
            for i in range(NX2):
                x = GX0 + (i + .5) * C2; d = math.hypot(x - px, y - py)
                if d <= rad and nf2[j * NX2 + i]: dist[j * NX2 + i] = d; h.append((d, j * NX2 + i))
        if h: break
    heapq.heapify(h)
    while h:
        d, c = heapq.heappop(h)
        if d > dist[c]: continue
        j, i = divmod(c, NX2)
        for dj, di, st in ((0, 1, C2), (0, -1, C2), (1, 0, C2), (-1, 0, C2), (1, 1, C2 * 1.4142), (1, -1, C2 * 1.4142), (-1, 1, C2 * 1.4142), (-1, -1, C2 * 1.4142)):
            jj = j + dj; ii = i + di
            if 0 <= jj < NY2 and 0 <= ii < NX2 and nf2[jj * NX2 + ii]:
                nd = d + st; cc = jj * NX2 + ii
                if nd < dist[cc]: dist[cc] = nd; heapq.heappush(h, (nd, cc))
    return dist, sorted(d for d in dist if d < INF)


class Cono:
    def __init__(s, kf, lib, rng, fg, nf2, eps):
        sa = math.sqrt(kf.a); sc = math.sqrt(kf.c); g = rng.gauss; s.fg = fg; s.eps = eps; s.n = len(lib)
        s.m = []
        for sp, dx, dy, kind in lib:
            vx = kf.vx + g(0, sc); vy = kf.vy + g(0, sc); v = math.hypot(vx, vy); f = v / sp
            s.m.append([1.0, kf.x + g(0, sa), kf.y + g(0, sa), f * vx / v, f * vy / v, dx, dy, 0.0, 0.0])
        s.dist, s.sd = flood(nf2, kf.x, kf.y)
        s.gx, s.gy = kf.x, kf.y; s.j = 0
    def step(s):
        """un ciclo: muove i membri, sfoltisce, calcola regioni e fantasma. Restituisce il dizionario delle uscite."""
        s.j += 1; j = min(s.j, 90); fg = s.fg; W = 0.0; cm = {}; al = []
        for m in s.m:
            w = m[0]
            if w < 1e-4: continue
            dx = m[5][j]; dy = m[6][j]
            x = m[1] + m[3] * dx - m[4] * dy; y = m[2] + m[4] * dx + m[3] * dy
            i = int((x - GX0) * 10); jj = int((y - GY0) * 10)
            if 0 <= i < GNX and 0 <= jj < GNY and x >= GX0 and y >= GY0 and fg[jj * GNX + i]:
                w *= (1 - PDM); m[0] = w
                if w < 1e-4: continue
            m[7] = x; m[8] = y; W += w; al.append(m)
            c = (int((y - GY0) * 4) << 8) | int((x - GX0) * 4)
            cm[c] = cm.get(c, 0.0) + w
        S = W / s.n; beta = s.eps / (s.eps + (1 - s.eps) * S) if s.eps > 0 else 0.0
        rad = VMAX * s.j * DT + 0.3; nF = max(1, bisect.bisect_right(s.sd, rad)); bgc = beta / nF; dist = s.dist
        items = []
        for c, mw in cm.items():
            jj, i = c >> 8, c & 255
            inF = 0 <= jj < NY2 and 0 <= i < NX2 and dist[jj * NX2 + i] <= rad
            items.append(((1 - beta) * mw / W + (bgc if inF else 0.0), c, inF))
        items.sort(reverse=True)
        out = {'S': S, 'beta': beta, 'rad': rad, 'nF': nF, 'bgc': bgc, 'dens': {c: v for v, c, f in items}}
        cum = 0.0; n50 = n90 = None; nout = 0
        for k, (v, c, inF) in enumerate(items):
            cum += v
            if not inF: nout += 1
            if n50 is None and cum >= 0.5: n50 = k + 1
            if n90 is None and cum >= 0.9: n90 = k + 1; break
        out['r50'] = set(c for v, c, f in items[:n50]) if n50 else None     # None = diffuso: tutto lo sfondo + celle dei membri
        out['r90'] = set(c for v, c, f in items[:n90]) if n90 else None
        nall = nF + sum(1 for v, c, f in items if not f)
        out['a50'] = (n50 if n50 else nall) * C2 * C2; out['a90'] = (n90 if n90 else nall) * C2 * C2
        out['all'] = set(c for v, c, f in items)
        # fantasma: membro piu' vicino alla mediana pesata, passo limitato
        if S >= 0.02 and al:
            def wmed(idx):
                acc = 0.0; h = W / 2
                for m in sorted(al, key=lambda m: m[idx]):
                    acc += m[0]
                    if acc >= h: return m[idx]
            mx = wmed(7); my = wmed(8); best = None; bd = 1e9
            for m in al:
                d = (m[7] - mx) ** 2 + (m[8] - my) ** 2
                if d < bd and m[0] > 0.5: bd = d; best = m
            if best is None: best = min(al, key=lambda m: (m[7] - mx) ** 2 + (m[8] - my) ** 2)
            tx, ty = best[7], best[8]; out['gdiff'] = False
        else:
            tx, ty = s.gx, s.gy; out['gdiff'] = True
        ex = 0.5 * (tx - s.gx); ey = 0.5 * (ty - s.gy); e = math.hypot(ex, ey); mxs = VMAX * DT
        if e > mxs: ex *= mxs / e; ey *= mxs / e
        s.gx += ex; s.gy += ey; out['ghost'] = (s.gx, s.gy); out['target'] = (tx, ty)
        return out
    def contains(s, o, key, x, y):
        c = (int((y - GY0) * 4) << 8) | int((x - GX0) * 4)
        r = o[key]
        if r is not None: return c in r
        if c in o['all']: return True
        jj, i = c >> 8, c & 255
        return 0 <= jj < NY2 and 0 <= i < NX2 and y >= GY0 and x >= GX0 and s.dist[jj * NX2 + i] <= o['rad']
    def density(s, o, x, y):
        c = (int((y - GY0) * 4) << 8) | int((x - GX0) * 4)
        if c in o['dens']: return o['dens'][c] / (C2 * C2)
        jj, i = c >> 8, c & 255
        if 0 <= jj < NY2 and 0 <= i < NX2 and y >= GY0 and x >= GX0 and s.dist[jj * NX2 + i] <= o['rad']: return max(o['bgc'], 1e-6) / (C2 * C2)
        return 1e-6 / (C2 * C2)


def nucleo_frac(kf, w):
    """quota dell'ombra (celle 0,25 m con centro in ombra vera) coperta dal cerchio al 95 %."""
    rho = kf.rad(); r2 = rho * rho; n = 0; tot = 0
    for j in range(NY2):
        y = GY0 + (j + .5) * C2
        for i in range(NX2):
            x = GX0 + (i + .5) * C2
            if vis(x, y, w) == 2:
                tot += 1
                if (x - kf.x) ** 2 + (y - kf.y) ** 2 <= r2: n += 1
    return n / max(tot, 1)


def run_trial(beh, w, dw, rng, lib, eps, st, tms):
    tr = truth(beh, w, rng) if beh in ('prosegue', 'sosta', 'torna', 'lontano') else truth_mio(beh, w, rng)
    west = w + dw; fg, nf2, ASH = masks(w, west)
    kf = None; zp = None; kp = None; k0 = None; co = None; o = None; fro = None; nuc_on = True; hdg = None; last_hidden = None
    for k, (x, y) in enumerate(tr):
        vt = vis(x, y, w)
        det = vt == 1 and rng.random() < PD
        z = (x + rng.gauss(0, SIG), y + rng.gauss(0, SIG)) if det else None
        if kf is None:
            if det:
                if zp is None: zp, kp = z, k
                else: kf = KF(zp, z, k - kp)
            continue
        kf.predict()
        if k0 is None:
            if vt == 1:
                if det: kf.update(z)
                continue
            k0 = k; fro = (kf.x, kf.y); v = math.hypot(kf.vx, kf.vy); hdg = (kf.vx / v, kf.vy / v)
            co = Cono(kf, lib, rng, fg, nf2, eps); j = 0
        if det:   # ricomparsa: salto fra la stima dell'ultimo ciclo e la prima misura
            if o is not None:
                g = o['ghost']; jg = math.hypot(g[0] - z[0], g[1] - z[1])
                near = 1e9
                cells = o['r90'] if o['r90'] is not None else o['all']
                for c in cells:
                    cx = GX0 + ((c & 255) + .5) * C2; cy = GY0 + ((c >> 8) + .5) * C2
                    d = math.hypot(cx - z[0], cy - z[1])
                    if d < near: near = d
                if o['r90'] is None:   # diffuso: conta anche lo sfondo
                    zc = (int((z[1] - GY0) * 4)) * NX2 + int((z[0] - GX0) * 4)
                    for dj in (-1, 0, 1):
                        for di in (-1, 0, 1):
                            cc = zc + dj * NX2 + di
                            if 0 <= cc < NX2 * NY2 and co.dist[cc] <= o['rad']: near = min(near, 0.3)
                st['re'].append((beh, jg, math.hypot(kf.x - z[0], kf.y - z[1]), math.hypot(fro[0] - z[0], fro[1] - z[1]), near <= 0.45,
                                 last_hidden, (k - k0) * DT))
            break
        t0 = time.perf_counter(); pg = (co.gx, co.gy); o = co.step(); tms.append(time.perf_counter() - t0); j = k - k0 + 1
        g = o['ghost']; stp = (g[0] - pg[0]) * hdg[0] + (g[1] - pg[1]) * hdg[1]
        st['step'].append((beh, math.hypot(g[0] - pg[0], g[1] - pg[1]), stp))
        if nuc_on and nucleo_frac(kf, w) >= 0.5: nuc_on = False
        if vt == 1: continue                       # visibile ma non rilevato: non si misura
        diff90 = o['r90'] is None
        info = (not diff90) and o['a90'] < 0.5 * ASH
        c90 = co.contains(o, 'r90', x, y); c50 = co.contains(o, 'r50', x, y); last_hidden = (c50, c90)
        st['cyc'].append((beh, info, nuc_on, diff90, o['r50'] is None))
        tau = TAUS.get(k - k0)
        if tau is not None:
            eg = math.hypot(g[0] - x, g[1] - y); ecv = math.hypot(kf.x - x, kf.y - y); efr = math.hypot(fro[0] - x, fro[1] - y)
            kcont = ecv <= kf.rad() and vis(x, y, west) != 1
            nll_e = -math.log(co.density(o, x, y)); nll_k = math.log(2 * math.pi * kf.a) + ecv * ecv / (2 * kf.a)
            st['ev'].append((beh, tau, c50, c90, o['a50'] / ASH, o['a90'] / ASH, diff90, eg, ecv, efr, kcont, nuc_on, nll_e, nll_k, o['S'], o['beta']))
        if k - k0 >= CAP: break


def mean(v): return sum(v) / len(v) if v else float('nan')
def med(v):
    v = sorted(v); return v[len(v) // 2] if v else float('nan')
def pct(v, q):
    v = sorted(v); return v[min(len(v) - 1, int(q * len(v)))] if v else float('nan')


def main():
    w = float(sys.argv[1]); behs = sys.argv[2].split(','); N = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    eps = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05; dw = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    nm = int(sys.argv[6]) if len(sys.argv) > 6 else 400
    lib = make_lib(nm, 777)
    kinds = {}
    for m in lib: kinds[m[3]] = kinds.get(m[3], 0) + 1
    _, _, ASH = masks(w, w + dw)
    print('# cono.py  w=%.1f  N=%d  eps=%.3f  dw=%+.2f  membri=%d  fascia=%.2f  ombra in portata=%.2f m2  libreria=%s' % (w, N, eps, dw, nm, GUARD, ASH, kinds))
    st = {'ev': [], 'cyc': [], 'step': [], 're': []}; tms = []
    for bi, beh in enumerate(behs):
        seeds = {'prosegue': 1, 'sosta': 2, 'torna': 3, 'lontano': 4, 'rallenta': 5, 'svolta': 6}
        rng = random.Random(20261114 + 1000 * seeds[beh] + int(w * 10))
        for t in range(N): run_trial(beh, w, dw, rng, lib, eps, st, tms)
    print('\n## per comportamento e tempo senza osservazione (solo cicli a soggetto non visibile)')
    print('beh       tau   n | c50%  c90% | a50%  a90% diff% | err: fant.  vel.cost  fermo (mediana, m) | nucleo: mostrato% cerchio contiene% | NLL cono  NLL kalman | S     beta')
    for beh in behs:
        for tau in sorted(TAUS.values()):
            e = [r for r in st['ev'] if r[0] == beh and r[1] == tau]
            if not e: continue
            print('%-9s %3.1f %3d | %4.0f  %4.0f | %4.0f  %4.0f  %4.0f | %9.2f %9.2f %6.2f              | %16.0f %17.0f | %8.2f %10.2f | %.2f  %.2f' % (
                beh, tau, len(e), 100 * mean([r[2] for r in e]), 100 * mean([r[3] for r in e]), 100 * mean([r[4] for r in e]), 100 * mean([r[5] for r in e]),
                100 * mean([r[6] for r in e]), med([r[7] for r in e]), med([r[8] for r in e]), med([r[9] for r in e]),
                100 * mean([r[11] for r in e]), 100 * mean([r[10] for r in e]), mean([r[12] for r in e]), mean([r[13] for r in e]), mean([r[14] for r in e]), mean([r[15] for r in e])))
    print('\n## continuita: quota dei cicli nascosti con stima emessa')
    print('beh        cicli | cono emesso% (costruzione) cono informativo% (r90 non diffusa e < meta ombra) r90 diffusa% r50 diffusa% | nucleo mostrato%')
    for beh in behs:
        c = [r for r in st['cyc'] if r[0] == beh]
        print('%-9s %6d | 100  %5.1f  %5.1f  %5.1f | %5.1f' % (beh, len(c), 100 * mean([r[1] for r in c]), 100 * mean([r[3] for r in c]), 100 * mean([r[4] for r in c]), 100 * mean([r[2] for r in c])))
    print('\n## regolarita del fantasma (tutti i cicli dopo l ingresso)')
    print('beh        cicli | passo max m | passi indietro > 2 cm % | passo indietro max m')
    for beh in behs:
        s = [r for r in st['step'] if r[0] == beh]
        print('%-9s %6d | %.3f | %5.1f | %.3f' % (beh, len(s), max(r[1] for r in s), 100 * mean([r[2] < -0.02 for r in s]), -min(r[2] for r in s)))
    print('\n## ricomparsa: salto fra stima e prima misura (m), e prima misura entro 0,45 m dalla regione al 90 %')
    print('beh         n | fantasma med p90 | vel.cost med p90 | fermo med p90 | entro r90 % | ultimo ciclo nascosto: c50% c90% | buio medio s')
    for beh in behs:
        r = [x for x in st['re'] if x[0] == beh]
        if not r: print('%-9s   0' % beh); continue
        lh = [x[5] for x in r if x[5] is not None]
        print('%-9s %3d | %.2f %.2f | %.2f %.2f | %.2f %.2f | %5.1f | %4.0f %4.0f | %.2f' % (beh, len(r), med([x[1] for x in r]), pct([x[1] for x in r], .9), med([x[2] for x in r]), pct([x[2] for x in r], .9),
              med([x[3] for x in r]), pct([x[3] for x in r], .9), 100 * mean([x[4] for x in r]), 100 * mean([a for a, b in lh]), 100 * mean([b for a, b in lh]), mean([x[6] for x in r])))
    tm = sorted(tms)
    print('\n## costo del passo del cono (Python puro): cicli %d  mediana %.2f ms  p95 %.2f ms  max %.2f ms' % (len(tm), 1000 * tm[len(tm) // 2], 1000 * tm[int(.95 * len(tm))], 1000 * tm[-1]))


if __name__ == '__main__':
    main()
