#!/usr/bin/env python3
# verifica_strati.py -- sciame-matematico, f7, corsia A.  Python puro, semi fissati.
# Rifare:  PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 verifica_strati.py > risultati.txt
# Sezione piana (2D).  Le previsioni sono in PREVISIONI.md (scritte prima).
import math, random, sys, time

A = 0.1                      # lato della cella (m)
NX, NY = 32, 48              # x in [0,3.2), y in [-2.4,2.4)
Y0 = -2.4
FOV_H = math.radians(43.5)   # semiampiezza del campo
BIN = math.radians(0.5)
NB = 174
R_MIN, R_MAX = 0.4, 3.0
B_NOISE = 0.03               # rumore limitato e margine radiale (m)
DT = 1.0 / 15.0
SUB = 4                      # sottopassi per fotogramma
LAT_SUB = 9                  # latenza = 9 sottopassi = 0,150 s
H_SUB = 13                   # orizzonte = 13 sottopassi = 0,2167 s
L_HIT, L_MISS, L_LO, L_HI = 0.847, -0.405, -2.0, 3.5
L_FREE_THR = math.log(0.3 / 0.7)
INF = 99.0
FULL = (1 << NY) - 1


def build_cells():
    """Per cella: (ix, iy, b0, b1, rmax) per le celle interamente nel campo."""
    cells = []
    for ix in range(NX):
        for iy in range(NY):
            x0, x1 = ix * A, (ix + 1) * A
            y0, y1 = Y0 + iy * A, Y0 + (iy + 1) * A
            cx = min(max(0.0, x0), x1)
            cy = min(max(0.0, y0), y1)
            rmin = math.hypot(cx, cy)
            rmax = max(math.hypot(x, y) for x in (x0, x1) for y in (y0, y1))
            if rmin < R_MIN or rmax > R_MAX:
                continue
            angs = [math.atan2(y, x) for x in (x0, x1) for y in (y0, y1)]
            tmin, tmax = min(angs), max(angs)
            if tmin < -FOV_H or tmax > FOV_H:
                continue
            b0 = int(math.floor((tmin + FOV_H) / BIN))
            b1 = min(NB - 1, int(math.floor((tmax + FOV_H) / BIN)))
            cells.append((ix, iy, b0, b1 + 1, rmax + B_NOISE))
    return cells


CELLS = build_cells()


def ray_rect(ox, oy, dx, dy, r):
    """Distanza lungo il raggio fino al rettangolo r=(x0,y0,x1,y1), INF se manca."""
    x0, y0, x1, y1 = r
    tn, tf = 0.0, INF
    for o, d, lo, hi in ((ox, dx, x0, x1), (oy, dy, y0, y1)):
        if abs(d) < 1e-12:
            if o < lo or o > hi:
                return INF
        else:
            t1, t2 = (lo - o) / d, (hi - o) / d
            if t1 > t2:
                t1, t2 = t2, t1
            tn, tf = max(tn, t1), min(tf, t2)
            if tn > tf:
                return INF
    return tn


def static_depth(rects, ox=0.0, oy=0.0, rot=0.0):
    """Profondita' minima per passo angolare sui rettangoli fermi (9 raggi per passo + spigoli)."""
    dep = [INF] * NB
    for k in range(NB):
        lo = -FOV_H + k * BIN
        m = INF
        for s in range(9):
            th = lo + BIN * s / 8.0 + rot
            dx, dy = math.cos(th), math.sin(th)
            for r in rects:
                t = ray_rect(ox, oy, dx, dy, r)
                if t < m:
                    m = t
        dep[k] = m
    for r in rects:
        for (px, py) in ((r[0], r[1]), (r[0], r[3]), (r[2], r[1]), (r[2], r[3])):
            th = math.atan2(py - oy, px - ox) - rot
            k = int(math.floor((th + FOV_H) / BIN))
            if 0 <= k < NB:
                d = math.hypot(px - ox, py - oy)
                # lo spigolo conta solo se non e' nascosto da un altro rettangolo
                if d < dep[k]:
                    dep[k] = d
    return dep


def add_disc(dep, cx, cy, rho, ox=0.0, oy=0.0, rot=0.0):
    """Minimo esatto, per passo angolare, della distanza raggio-disco."""
    ex, ey = cx - ox, cy - oy
    d = math.hypot(ex, ey)
    if d <= rho:
        for k in range(NB):
            dep[k] = 0.0
        return
    phi = math.atan2(ey, ex) - rot
    al = math.asin(rho / d)
    k0 = max(0, int(math.floor((phi - al + FOV_H) / BIN)))
    k1 = min(NB - 1, int(math.floor((phi + al + FOV_H) / BIN)))
    for k in range(k0, k1 + 1):
        lo = -FOV_H + k * BIN
        th = min(max(phi, lo), lo + BIN)
        off = th - phi
        s = d * math.sin(off)
        q = rho * rho - s * s
        if q < 0.0:
            q = 0.0
        t = d * math.cos(off) - math.sqrt(q)
        if t < dep[k]:
            dep[k] = t


def dilate(rows, n, border):
    """Dilatazione quadrata (L-infinito) di n celle su righe-bitmask; fuori griglia = 1."""
    out = []
    for m in rows:
        v = m
        for k in range(1, n + 1):
            v |= (m << k) | (m >> k)
        out.append(v & FULL)
    res = []
    for i in range(NX):
        v = 0
        for j in range(max(0, i - n), min(NX, i + n + 1)):
            v |= out[j]
        res.append(v | border[i])
    return res


def border_mask(n):
    b = []
    edge = ((1 << n) - 1) | (((1 << n) - 1) << (NY - n)) if n > 0 else 0
    for i in range(NX):
        b.append(FULL if (i < n or i >= NX - n) else edge)
    return b


def popcount_rows(rows):
    return sum(r.bit_count() for r in rows)


def disc_cells(cx, cy, rho, occ):
    ix0 = max(0, int(math.floor((cx - rho) / A)))
    ix1 = min(NX - 1, int(math.floor((cx + rho) / A)))
    iy0 = max(0, int(math.floor((cy - rho - Y0) / A)))
    iy1 = min(NY - 1, int(math.floor((cy + rho - Y0) / A)))
    r2 = rho * rho
    for ix in range(ix0, ix1 + 1):
        x0 = ix * A
        nx = min(max(cx, x0), x0 + A)
        for iy in range(iy0, iy1 + 1):
            y0 = Y0 + iy * A
            ny = min(max(cy, y0), y0 + A)
            if (nx - cx) ** 2 + (ny - cy) ** 2 <= r2:
                occ[ix] |= (1 << iy)


WALLS = [(3.3, -3.0, 3.4, 3.0), (-1.0, 2.5, 3.4, 2.6), (-1.0, -2.6, 3.4, -2.5)]


def make_world(rng, vmax, kind='dinamica'):
    rects = list(WALLS)
    for _ in range(rng.randint(1, 2) if kind != 'vuota' else 0):
        px = rng.uniform(1.2, 2.0)
        w = rng.uniform(0.5, 1.0)
        py = rng.uniform(-1.2, 1.2 - w)
        rects.append((px, py, px + 0.1, py + w))
    movers = []
    for _ in range(rng.randint(2, 4) if kind == 'dinamica' else 0):
        movers.append({
            'p': [rng.uniform(-0.8, 3.1), rng.uniform(-2.3, 2.3)],
            'rho': rng.uniform(0.15, 0.25),
            'w': [rng.uniform(-0.8, 3.1), rng.uniform(-2.3, 2.3)],
            'v': vmax if rng.random() < 0.3 else rng.uniform(0.2, vmax),
            'pause': 0})
    return rects, movers


def step_movers(rng, movers, vmax, dt):
    for m in movers:
        if m['pause'] > 0:
            m['pause'] -= 1
            continue
        px, py = m['p']
        wx, wy = m['w']
        dist = math.hypot(wx - px, wy - py)
        s = m['v'] * dt
        if dist <= s:
            m['p'] = [wx, wy]
            m['w'] = [rng.uniform(-0.8, 3.1), rng.uniform(-2.3, 2.3)]
            m['v'] = vmax if rng.random() < 0.3 else rng.uniform(0.2, vmax)
            if rng.random() < 0.3:
                m['pause'] = rng.randint(8, 120)
        else:
            m['p'] = [px + (wx - px) * s / dist, py + (wy - py) * s / dist]


RULES = ('PI', 'PI_eta', 'cono1', 'nucleo', 'bayes', 'bayes2')


def run(seed, vmax, pdrop, frames=300, cover=None, kind='dinamica', cellhole=0.0, vfac=1.0):
    rng = random.Random(seed)
    rects, movers = make_world(rng, vmax * vfac, kind)
    sdep = static_depth(rects)
    nsub = frames * SUB + H_SUB + 1
    traj = []
    dt = DT / SUB
    for _ in range(nsub):
        traj.append([(m['p'][0], m['p'][1], m['rho']) for m in movers])
        step_movers(rng, movers, vmax * vfac, dt)
    occ = []
    for s in range(nsub):
        o = [0] * NX
        for (cx, cy, rho) in traj[s]:
            disc_cells(cx, cy, rho, o)
        occ.append(o)
    n_d = math.ceil(vmax * DT / A - 1e-9)
    n_h = math.ceil(vmax * (H_SUB * dt) / A - 1e-9)
    bd, bh, b0 = border_mask(n_d), border_mask(n_h), border_mask(0)
    PI = [FULL] * NX
    L = [[0.0] * NY for _ in range(NX)]
    lastF = [[-99] * NY for _ in range(NX)]
    nrng = random.Random(seed * 7919 + 13)
    st = {r: {'dich': 0, 'ff_fin': 0, 'ff_0': 0} for r in RULES}
    st['F'] = 0
    st['occ_fuori_PI'] = 0
    st['cov'] = {r: [] for r in RULES}
    for t in range(frames):
        covered = cover is not None and cover[0] <= t < cover[1]
        dep = list(sdep)
        for (cx, cy, rho) in traj[t * SUB]:
            add_disc(dep, cx, cy, rho)
        dv = [0.0] * NB   # non valido -> -1 (blocca)
        di = [0.0] * NB   # non valido -> INF (ignorato)
        for k in range(NB):
            if covered or nrng.random() < pdrop:
                dv[k], di[k] = -1.0, INF
            else:
                z = dep[k] + nrng.uniform(-B_NOISE, B_NOISE)
                dv[k], di[k] = z, z
        HIT = [0] * NX
        for k in range(NB):
            z = dv[k]
            if 0.0 < z <= R_MAX:
                th = -FOV_H + (k + 0.5) * BIN
                ix = int(math.floor(z * math.cos(th) / A))
                iy = int(math.floor((z * math.sin(th) - Y0) / A))
                if 0 <= ix < NX and 0 <= iy < NY:
                    HIT[ix] |= (1 << iy)
        F = [0] * NX
        NUC = [0] * NX
        REC = [0] * NX
        BAY = [0] * NX
        for (ix, iy, k0, k1, rm) in CELLS:
            bit = 1 << iy
            Lr = L[ix]
            if min(dv[k0:k1]) > rm and not (cellhole > 0.0 and nrng.random() < cellhole):
                F[ix] |= bit
                NUC[ix] |= bit
                REC[ix] |= bit
                lastF[ix][iy] = t
                v = Lr[iy] + L_MISS
                Lr[iy] = v if v > L_LO else L_LO
            elif lastF[ix][iy] >= t - 2:
                REC[ix] |= bit
                # senza dato ora (solo passi non validi bloccano) e visto libero da poco
                if covered or min(di[k0:k1]) > rm:
                    NUC[ix] |= bit
            if HIT[ix] & bit:
                v = Lr[iy] + L_HIT
                Lr[iy] = v if v < L_HI else L_HI
            if Lr[iy] < L_FREE_THR:
                BAY[ix] |= bit
        # --- strato PI (possibile presenza, appartenenza insiemistica)
        d = dilate(PI, n_d, bd)
        PI = [d[i] & ~F[i] & FULL for i in range(NX)]
        dh = dilate(PI, n_h, bh)
        DL = [~dh[i] & FULL for i in range(NX)]
        # --- cono a un fotogramma
        nf = [~F[i] & FULL for i in range(NX)]
        dc = dilate(nf, n_h, bh)
        D1 = [~dc[i] & FULL for i in range(NX)]
        sets = {'PI': DL,
                'PI_eta': [DL[i] & REC[i] for i in range(NX)],
                'cono1': D1,
                'nucleo': NUC,
                'bayes': BAY,
                'bayes2': [BAY[i] & ~HIT[i] for i in range(NX)]}
        onow = occ[t * SUB]
        owin = [0] * NX
        for s in range(t * SUB + LAT_SUB, t * SUB + H_SUB + 1):
            o = occ[s]
            for i in range(NX):
                owin[i] |= o[i]
        st['F'] += popcount_rows(F)
        st['occ_fuori_PI'] += sum((onow[i] & ~PI[i]).bit_count() for i in range(NX))
        for r in RULES:
            S = sets[r]
            st[r]['dich'] += popcount_rows(S)
            st[r]['ff_fin'] += sum((S[i] & owin[i]).bit_count() for i in range(NX))
            st[r]['ff_0'] += sum((S[i] & onow[i]).bit_count() for i in range(NX))
            if cover is not None and cover[0] <= t < cover[1]:
                st['cov'][r].append(popcount_rows(S))
    return st


def sim_A(nworld=24):
    print('== A. Strati: falsi liberi, costo, valore della storia ==')
    print('celle nel campo (interamente):', len(CELLS), 'su', NX * NY)
    summary = {}
    for vmax in (2.5, 1.4):
        for pdrop in (0.0, 0.05):
            tot = {r: {'dich': 0, 'ff_fin': 0, 'ff_0': 0, 'w_fin': 0, 'w_0': 0} for r in RULES}
            Fsum = 0
            occout = 0
            nfr = 0
            for w in range(nworld):
                st = run(1000 + w, vmax, pdrop)
                nfr += 300
                Fsum += st['F']
                occout += st['occ_fuori_PI']
                for r in RULES:
                    for k in ('dich', 'ff_fin', 'ff_0'):
                        tot[r][k] += st[r][k]
                    tot[r]['w_fin'] += 1 if st[r]['ff_fin'] > 0 else 0
                    tot[r]['w_0'] += 1 if st[r]['ff_0'] > 0 else 0
            print('\nv_max = %.1f m/s, buchi = %.0f %%, corse = %d, fotogrammi = %d; celle viste libere per fotogramma = %.1f; celle occupate fuori da PI = %d'
                  % (vmax, 100 * pdrop, nworld, nfr, Fsum / nfr, occout))
            print('  regola    dich/fot  dich/F   falsi_fin  corse_fin  falsi_0   corse_0')
            for r in RULES:
                x = tot[r]
                print('  %-8s %8.1f  %5.1f%%  %9d  %5d/%d  %8d  %5d/%d'
                      % (r, x['dich'] / nfr, 100.0 * x['dich'] / Fsum, x['ff_fin'], x['w_fin'], nworld,
                         x['ff_0'], x['w_0'], nworld))
            summary[(vmax, pdrop)] = {r: tot[r]['dich'] / nfr for r in RULES}
    for vmax in (2.5, 1.4):
        a, b = summary[(vmax, 0.0)], summary[(vmax, 0.05)]
        print('\nvalore della storia, v_max = %.1f: PI con buchi / senza = %.1f %%; cono1 con buchi / senza = %.1f %%'
              % (vmax, 100 * b['PI'] / a['PI'], 100 * b['cono1'] / a['cono1'] if a['cono1'] > 0 else float('nan')))
    print('\n-- sensore coperto: fotogrammi 150-179 (2 s) tutti non validi, v_max 2.5 e 1.4, buchi 0 %, 12 corse ciascuno')
    for vmax in (2.5, 1.4):
        worst = {r: 0 for r in RULES}
        minb = {r: 10 ** 9 for r in RULES}
        ffcov = {r: 0 for r in RULES}
        for w in range(12):
            st = run(2000 + w, vmax, 0.0, cover=(150, 180))
            for r in RULES:
                c = st['cov'][r]
                nz = max([i + 1 for i, v in enumerate(c) if v > 0] or [0])
                worst[r] = max(worst[r], nz)
                minb[r] = min(minb[r], min(c))
                ffcov[r] += st[r]['ff_fin']
        for r in RULES:
            print('  v_max %.1f  %-8s ultimo fotogramma coperto con celle dichiarate: %2d (%.2f s); minimo dichiarate nella copertura: %d; falsi_fin nelle corse: %d'
                  % (vmax, r, worst[r], worst[r] * DT, minb[r], ffcov[r]))


def sim_F():
    print('== F. Seconda tornata (previsioni D1-D5): costo della regola PI per v_max e scena; buchi per cella ==')
    ff = 0
    oo = 0
    nrun = 0
    print('  quota dichiarata dalla regola PI sul visto libero (dich/F), senza buchi, 12 mondi x 300 fotogrammi (scena vuota: 2 mondi)')
    print('  v_max  margine_celle   vuota    pannelli   dinamica   | celle dichiarate per fotogramma (dinamica)')
    for vmax in (0.4, 0.9, 1.4, 2.5):
        row = []
        dyn = 0.0
        for kind, nw in (('vuota', 2), ('pannelli', 12), ('dinamica', 12)):
            d = f = 0
            for w in range(nw):
                st = run(3000 + w, vmax, 0.0, kind=kind)
                d += st['PI']['dich']
                f += st['F']
                ff += st['PI']['ff_fin'] + st['PI']['ff_0']
                oo += st['occ_fuori_PI']
                nrun += 1
            row.append(100.0 * d / f)
            if kind == 'dinamica':
                dyn = d / (nw * 300.0)
        nh = math.ceil(vmax * (H_SUB * DT / SUB) / A - 1e-9)
        print('  %.1f    %d             %5.1f%%   %5.1f%%    %5.1f%%    | %.1f' % (vmax, nh, row[0], row[1], row[2], dyn))
    print('  buchi per cella (5 %, indipendenti), scena dinamica, 24 mondi x 300 fotogrammi')
    for vmax in (0.9, 1.4):
        res = {}
        for ch in (0.0, 0.05):
            d = {'PI': 0, 'cono1': 0, 'PI_eta': 0}
            for w in range(24):
                st = run(1000 + w, vmax, 0.0, cellhole=ch)
                for r in d:
                    d[r] += st[r]['dich']
                ff += st['PI']['ff_fin'] + st['PI']['ff_0']
                oo += st['occ_fuori_PI']
                nrun += 1
            res[ch] = d
        print('  v_max %.1f: PI senza buchi %.1f celle/fot, con buchi %.1f (%.1f %%); cono1 senza %.1f, con %.1f (%.1f %%); PI_eta con buchi %.1f'
              % (vmax, res[0.0]['PI'] / 7200.0, res[0.05]['PI'] / 7200.0, 100.0 * res[0.05]['PI'] / res[0.0]['PI'],
                 res[0.0]['cono1'] / 7200.0, res[0.05]['cono1'] / 7200.0, 100.0 * res[0.05]['cono1'] / res[0.0]['cono1'],
                 res[0.05]['PI_eta'] / 7200.0))
    print('  in tutte le %d corse della seconda tornata: falsi liberi della regola PI (finestra + latenza zero) = %d; celle occupate fuori da PI = %d' % (nrun, ff, oo))


def sim_G():
    print('== G. Braccio che deve fallire: oggetti piu\' veloci della v_max dichiarata ==')
    for vmax in (0.9, 0.4):
        for vfac in (1.0, 2.0):
            ff = runs = d = 0
            for w in range(24):
                st = run(5000 + w, vmax, 0.0, vfac=vfac)
                c = st['PI']['ff_fin'] + st['PI']['ff_0']
                ff += c
                runs += 1 if c > 0 else 0
                d += st['PI']['dich']
            print('  v_max dichiarata %.1f, velocita\' vera fino a %.1f m/s: celle-fotogramma dichiarate %d; falsi liberi %d; corse con falsi liberi %d/24'
                  % (vmax, vmax * vfac, d, ff, runs))


def sim_B(ntrial=200):
    print('\n== B. Errore di posa e margine ==')
    for (eps, ddeg, erosions) in ((0.03, 1.0, (0, 1)), (0.05, 2.0, (0, 1, 2))):
        dl = math.radians(ddeg)
        m = eps + R_MAX * dl
        rng = random.Random(4242)
        bad = {e: 0 for e in erosions}
        cnt = {e: 0 for e in erosions}
        dich = {e: 0 for e in erosions}
        for tr in range(ntrial):
            discs = []
            for _ in range(6):
                r = rng.uniform(1.0, 2.8)
                th = rng.uniform(-0.7, 0.7)
                discs.append((r * math.cos(th), r * math.sin(th), rng.uniform(0.1, 0.3)))
            beta = rng.uniform(0, 2 * math.pi)
            ox, oy = eps * math.cos(beta), eps * math.sin(beta)
            rot = dl if rng.random() < 0.5 else -dl
            dep = static_depth(WALLS, ox, oy, rot)
            for (cx, cy, rho) in discs:
                add_disc(dep, cx, cy, rho, ox, oy, rot)
            dv = [z + rng.uniform(-B_NOISE, B_NOISE) for z in dep]
            F = [0] * NX
            for (ix, iy, k0, k1, rm) in CELLS:
                if min(dv[k0:k1]) > rm:
                    F[ix] |= (1 << iy)
            occ = [0] * NX
            for (cx, cy, rho) in discs:
                disc_cells(cx, cy, rho, occ)
            for e in erosions:
                if e == 0:
                    S = F
                else:
                    nf = [~F[i] & FULL for i in range(NX)]
                    dd = dilate(nf, e, border_mask(e))
                    S = [~dd[i] & FULL for i in range(NX)]
                c = sum((S[i] & occ[i]).bit_count() for i in range(NX))
                cnt[e] += c
                bad[e] += 1 if c > 0 else 0
                dich[e] += popcount_rows(S)
        for e in erosions:
            print('  eps_t = %.0f cm, delta = %.0f gradi, margine teorico m = %.1f cm; erosione %d celle (%.0f cm): scene con falsi liberi %d/%d, celle false %d, celle dichiarate/scena %.1f'
                  % (100 * eps, ddeg, 100 * m, e, 100 * e * A, bad[e], ntrial, cnt[e], dich[e] / ntrial))


def sim_C():
    print('\n== C. Vetro: aggiornamento log-odds statico con ritorni intermittenti ==')
    fstar = -L_MISS / (L_HIT - L_MISS)
    print('  soglia teorica f* = %.3f (deriva media nulla); da saturato libero a p>0.5: %d colpi; da saturato occupato a p<0.5: %d passaggi'
          % (fstar, math.ceil((0 - L_LO) / L_HIT), math.ceil(L_HI / -L_MISS)))
    rng = random.Random(77)
    for f in (0.05, 0.20, 0.30, 0.35, 0.50):
        below = 0
        tot = 0
        for run_i in range(500):
            L = 0.0
            for t in range(300):
                L += L_HIT if rng.random() < f else L_MISS
                L = min(L_HI, max(L_LO, L))
                if t >= 50:
                    tot += 1
                    below += 1 if L < 0 else 0
        print('  f = %.2f: quota di fotogrammi con p < 0.5 = %.1f %%' % (f, 100.0 * below / tot))


def rank(M, tol=1e-9):
    M = [row[:] for row in M]
    r = 0
    rows, cols = len(M), len(M[0])
    for c in range(cols):
        p = max(range(r, rows), key=lambda i: abs(M[i][c]), default=None)
        if p is None or abs(M[p][c]) < tol:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(rows):
            if i != r:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == rows:
            break
    return r


def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]


def obs_rank(n_axes, measured):
    n = 2 * n_axes
    Fm = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for a in range(n_axes):
        Fm[a][n_axes + a] = DT
    H = [[1.0 if j == a else 0.0 for j in range(n)] for a in measured]
    O, cur = [], H
    for _ in range(n):
        O += cur
        cur = matmul(cur, Fm)
    return rank(O)


def chi2_q(dof, p):
    def cdf(x):
        if dof == 2:
            return 1 - math.exp(-x / 2)
        return math.erf(math.sqrt(x / 2)) - math.sqrt(2 * x / math.pi) * math.exp(-x / 2)
    lo, hi = 0.0, 60.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return lo


def sim_D():
    print('\n== D. Filtro a velocita\' quasi costante in 2D e in 3D ==')
    print('  rango di osservabilita\': piano [x,y,vx,vy], misura (x,y): %d su 4' % obs_rank(2, (0, 1)))
    print('  rango di osservabilita\': 3D [x,y,z,vx,vy,vz], misura (x,y,z): %d su 6' % obs_rank(3, (0, 1, 2)))
    print('  rango di osservabilita\': 3D, misura (x,y) soltanto (quota non misurata): %d su 6' % obs_rank(3, (0, 1)))
    c2_95, c2_99, c3_95, c3_99 = chi2_q(2, .95), chi2_q(2, .99), chi2_q(3, .95), chi2_q(3, .99)
    print('  quantili chi-quadro: 2 gradi 95%%=%.3f 99%%=%.3f; 3 gradi 95%%=%.3f 99%%=%.3f' % (c2_95, c2_99, c3_95, c3_99))
    q, R, T = 0.2, 0.03 ** 2, DT
    P = [[1.0, 0.0], [0.0, 1.0]]
    Q = [[q * T ** 3 / 3, q * T ** 2 / 2], [q * T ** 2 / 2, q * T]]
    for _ in range(2000):
        # previsione
        p00 = P[0][0] + 2 * T * P[0][1] + T * T * P[1][1] + Q[0][0]
        p01 = P[0][1] + T * P[1][1] + Q[0][1]
        p11 = P[1][1] + Q[1][1]
        # correzione
        S = p00 + R
        k0, k1 = p00 / S, p01 / S
        P = [[(1 - k0) * p00, (1 - k0) * p01], [(1 - k0) * p01, p11 - k1 * p01]]
    print('  regime per asse (q=0.2, R=(3 cm)^2, 15 Hz): sigma_pos = %.1f cm, sigma_vel = %.2f m/s' % (100 * math.sqrt(P[0][0]), math.sqrt(P[1][1])))

    def sig(tau):
        return math.sqrt(P[0][0] + 2 * tau * P[0][1] + tau * tau * P[1][1] + q * tau ** 3 / 3)
    print('  senza misure:   tau    sigma   raggio95 piano   semiasse95 3D   area95 (m2)   volume95 (m3)')
    for tau in (0.2, 0.5, 1.0, 2.0):
        s = sig(tau)
        print('               %5.2f  %6.3f   %6.3f          %6.3f          %7.3f       %7.3f'
              % (tau, s, math.sqrt(c2_95) * s, math.sqrt(c3_95) * s, math.pi * c2_95 * s * s,
                 4.0 / 3.0 * math.pi * (c3_95 ** 1.5) * s ** 3))
    g = 9.81
    tstar = None
    tau = 0.0
    while tau < 2.0:
        tau += 0.001
        if 0.5 * g * tau * tau > math.sqrt(c3_95) * sig(tau):
            tstar = tau
            break
    print('  caduta libera: (1/2) g t^2 supera il semiasse al 95%% (3 gradi) a t* = %.3f s' % tstar)
    for tt in (0.3, 0.5, 1.0):
        # q che rende sqrt(c3_95)*sqrt(q t^3/3) = g t^2 / 2 (trascurando P di regime)
        qn = (0.5 * g * tt * tt) ** 2 / c3_95 * 3 / tt ** 3
        print('  q necessario perche\' il solo termine q t^3/3 copra la caduta a t = %.1f s: %.2f m2/s3 (%.0f volte 0.2)' % (tt, qn, qn / 0.2))

    print('\n== E. Conti geometrici (3D) ==')
    bh, bv, Rr = math.radians(43.5), math.radians(29.0), 3.0
    vol = 4.0 / 3.0 * Rr ** 3 * math.tan(bh) * math.tan(bv)
    print('  volume della piramide vista (87 x 58 gradi, profondita\' 3 m): %.1f m3; scatola 6x4x3: 72 m3 (%.0f %%)' % (vol, 100 * vol / 72))
    for a in (0.10, 0.05):
        print('  lato %.2f m: voxel nella piramide %d; voxel della scatola densa %d' % (a, round(vol / a ** 3), round(72 / a ** 3)))
    rho = Rr * math.sin(bv) / (1 + math.sin(bv))
    print('  raggio della sfera inscritta (piani verticali a 29 gradi, fondo sferico a 3 m): %.3f m' % rho)
    for vm in (2.5, 1.4):
        for hh in (0.2167, 0.155 + DT):
            print('  v_max = %.1f m/s, orizzonte h = %.3f s: margine v_max*h = %.3f m; eta\' utile massima = rho/v_max - h = %.3f s (%.1f fotogrammi)'
                  % (vm, hh, vm * hh, rho / vm - hh, (rho / vm - hh) / DT))
    print('  fascia 0.40 m con h = 0.217 s: v_max coperta = %.2f m/s' % (0.40 / 0.2167))
    for (e, dd) in ((0.0, 0.5), (0.03, 1.0), (0.05, 2.0)):
        print('  margine di posa m = eps_t + r*delta a 3 m: eps_t = %.0f cm, delta = %.1f gradi -> %.1f cm' % (100 * e, dd, 100 * (e + 3.0 * math.radians(dd))))


if __name__ == '__main__':
    t0 = time.time()
    which = sys.argv[1] if len(sys.argv) > 1 else 'tutto'
    nw = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    print('verifica_strati.py', which, 'mondi', nw, '| Python', sys.version.split()[0])
    if which in ('tutto', 'A'):
        sim_A(nw)
    if which in ('tutto', 'B'):
        sim_B()
    if which in ('tutto', 'C'):
        sim_C()
    if which in ('tutto', 'D'):
        sim_D()
    if which == 'F':
        sim_F()
    if which == 'G':
        sim_G()
    print('\ntempo totale: %.1f s' % (time.time() - t0))
