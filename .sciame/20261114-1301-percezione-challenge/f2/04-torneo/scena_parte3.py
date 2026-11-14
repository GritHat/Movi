#!/usr/bin/env python3
"""Scena comune dell'avversario (f2 torneo, parte 3). Python puro, semi fissati.
Uso: timeout 120 python3 scena_parte3.py <main1|main2|ombra|k001|falso|vmax|due>
Scena SIMULATA, 2D in pianta: sensore in (0,0) verso +y, campo +-43,5 gradi, portata 6 m;
pannello a y=2 m (largo w, centrato); pedone puntiforme a y=4 m; 15 Hz; rumore 5 cm; Pd 0,9.
"""
import math, os, random, sys
DT = 1 / 15.; SIG = 0.05; R = SIG * SIG; PD = 0.9; FOV = math.radians(43.5); RMAX = 6.0; YP = 2.0
Q = 0.2; CHI95 = 5.991; CHI99 = 9.21; VMAX = 2.5; NP = int(os.environ.get('NP3', 250)); R0 = 0.99; RDEAD = 0.05
P01 = 1 - math.exp(-0.25 * DT); P10 = 1 - math.exp(-0.4 * DT)
EVF = {8: 0.5, 15: 1.0, 30: 2.0, 45: 3.0}
GX0, GY0, GNX, GNY, CELL = -8.0, -2.0, 160, 100, 0.1


def vis(x, y, w):
    """0 = non osservato (fuori campo o portata), 1 = visto (libero), 2 = in ombra del pannello."""
    if y <= 0.05: return 0
    if x * x + y * y > RMAX * RMAX or abs(math.atan2(x, y)) > FOV: return 0
    if w > 0 and y > YP and abs(x * YP / y) <= w / 2: return 2
    return 1


_G = {}
_GR = random.Random(4242)  # solo per la massa gaussiana del Kalman in celle libere
def grid(w):
    k = round(w, 3)
    if k not in _G:
        g = [[vis(GX0 + (i + .5) * CELL, GY0 + (j + .5) * CELL, w) for i in range(GNX)] for j in range(GNY)]
        _G[k] = (g, sum(r.count(2) for r in g))
    return _G[k]


def circ(cx, cy, rad, gt, ge=None):
    """celle nel cerchio: totale, viste libere (vero), in ombra (vero), in ombra stimata. Con ge: solo celle con stima != 1."""
    i0 = max(0, int((cx - rad - GX0) / CELL)); i1 = min(GNX - 1, int((cx + rad - GX0) / CELL))
    j0 = max(0, int((cy - rad - GY0) / CELL)); j1 = min(GNY - 1, int((cy + rad - GY0) / CELL))
    n = nf = ns = nse = 0; r2 = rad * rad
    for j in range(j0, j1 + 1):
        dy = GY0 + (j + .5) * CELL - cy; rowt = gt[j]; rowe = ge[j] if ge else None
        for i in range(i0, i1 + 1):
            dx = GX0 + (i + .5) * CELL - cx
            if dx * dx + dy * dy > r2: continue
            if rowe is not None:
                if rowe[i] == 1: continue
                if rowe[i] == 2: nse += 1
            n += 1; t = rowt[i]
            if t == 1: nf += 1
            elif t == 2: ns += 1
    return n, nf, ns, nse


class KF:
    def __init__(s, z1, z2, dk):
        s.x, s.y = z2; s.vx = (z2[0] - z1[0]) / (DT * dk); s.vy = (z2[1] - z1[1]) / (DT * dk)
        s.a = R; s.b = R / (DT * dk); s.c = 2 * R / (DT * dk) ** 2
    def predict(s):
        s.x += s.vx * DT; s.y += s.vy * DT; a, b, c = s.a, s.b, s.c
        s.a = a + 2 * b * DT + c * DT * DT + Q * DT ** 3 / 3; s.b = b + c * DT + Q * DT * DT / 2; s.c = c + Q * DT
    def d2(s, z): return ((z[0] - s.x) ** 2 + (z[1] - s.y) ** 2) / (s.a + R)
    def update(s, z):
        S = s.a + R; k1 = s.a / S; k2 = s.b / S; ex = z[0] - s.x; ey = z[1] - s.y
        s.x += k1 * ex; s.y += k1 * ey; s.vx += k2 * ex; s.vy += k2 * ey
        a, b, c = s.a, s.b, s.c; s.a = (1 - k1) * a; s.b = (1 - k1) * b; s.c = c - k2 * b
    def rad(s): return math.sqrt(CHI95 * s.a)


class PF:
    def __init__(s, kf, stop, rng, pdm, n=NP):
        sa = math.sqrt(kf.a); sc = math.sqrt(kf.c); g = rng.gauss; s.n = n; s.rng = rng; s.stop = stop; s.pdm = pdm
        s.px = [kf.x + g(0, sa) for _ in range(n)]; s.py = [kf.y + g(0, sa) for _ in range(n)]
        s.vx = [kf.vx + g(0, sc) for _ in range(n)]; s.vy = [kf.vy + g(0, sc) for _ in range(n)]
        s.md = [0] * n; s.w = [1. / n] * n; s.r = R0
    def move(s):
        sq = math.sqrt(Q * DT); g = s.rng.gauss; rnd = s.rng.random; md = s.md
        for i in range(s.n):
            if s.stop:
                if md[i] == 0:
                    if rnd() < P01: md[i] = 1
                elif rnd() < P10: md[i] = 0
            if md[i] == 0:
                s.vx[i] += g(0, sq); s.vy[i] += g(0, sq); s.px[i] += s.vx[i] * DT; s.py[i] += s.vy[i] * DT
    def neg(s, west):
        f = 1 - s.pdm; w = s.w; px = s.px; py = s.py
        for i in range(s.n):
            if vis(px[i], py[i], west) == 1: w[i] *= f
        tot = sum(w); d = 1 - tot
        s.r = s.r * (1 - d) / (1 - s.r * d) if s.r * d < 1 else 0.0
        if tot <= 0: s.w = [1. / s.n] * s.n; s.r = 0.0; return
        w = [x / tot for x in w]; s.w = w
        if 1. / sum(x * x for x in w) < s.n / 2:
            u = s.rng.random() / s.n; c = w[0]; i = 0; idx = []
            for j in range(s.n):
                t = u + j / s.n
                while c < t and i < s.n - 1: i += 1; c += w[i]
                idx.append(i)
            for nm in ('px', 'py', 'vx', 'vy', 'md'):
                a = getattr(s, nm); setattr(s, nm, [a[i] for i in idx])
            s.w = [1. / s.n] * s.n
    def mass_near(s, p, d=0.5):
        d2 = d * d; return sum(w for w, x, y in zip(s.w, s.px, s.py) if (x - p[0]) ** 2 + (y - p[1]) ** 2 <= d2)
    def mass_vis(s, w, code): return sum(wi for wi, x, y in zip(s.w, s.px, s.py) if vis(x, y, w) == code)
    def hpd(s, c=0.5):
        m = {}
        for wi, x, y in zip(s.w, s.px, s.py):
            k = (math.floor(x / c), math.floor(y / c)); m[k] = m.get(k, 0) + wi
        out = set(); acc = 0
        for k, v in sorted(m.items(), key=lambda kv: -kv[1]):
            out.add(k); acc += v
            if acc >= 0.95: break
        return out


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


def run_trial(beh, w, dw, rng, v=None, yped=4.0, ff=None, pdm=PD, do_pf=True, cap=110):
    tr = truth(beh, w, rng, v, yped); west = w + dw; gt, nsh = grid(w); ge, nshe = grid(west); ASH = nsh * CELL * CELL
    res = {'ev': {}, 'id': None, 'ff': [], 'ray': None, 'dead': None, 'rmin_in': {}}
    kf = None; zp = None; kp = None; k0 = None; zl = None; kl = None; seen = False; ffk = 0; ffdone = False
    ray = {m: {'st': 'trk', 'cnt': 0, 'kc': None, 'hid': None, 'ke': None} for m in (1, 3)}
    pfs = {'ns': None, 'st': None}; dead = {'ns': None, 'st': None}
    for k, (x, y) in enumerate(tr):
        vt = vis(x, y, w); sup = False
        if ff and not ffdone:
            if (ff[0] == 'open' and k >= 25) or (ff[0] == 'exit' and k0 is not None and vt == 1):
                if ffk < ff[1]: sup = True; ffk += 1
                else: ffdone = True
        det = vt == 1 and not sup and rng.random() < PD
        z = (x + rng.gauss(0, SIG), y + rng.gauss(0, SIG)) if det else None
        if kf is None:
            if det:
                if zp is None: zp, kp = z, k
                else: kf = KF(zp, z, k - kp); zl, kl = z, k
            continue
        kf.predict()
        if k0 is None and vt != 1: k0 = k
        if k0 is not None and vt == 1: seen = True
        if det:
            if k0 is not None or ffk > 0:
                d2 = kf.d2(z); tau = (k - kl) * DT; idr = {'kf': d2 <= CHI99, 'kf15': d2 <= CHI99 and kf.rad() <= 1.5, 'tau': tau}
                for m in ray: idr['ray%d' % m] = ray[m]['st'] in ('trk', 'prev') and d2 <= CHI99
                idr['disc'] = math.hypot(z[0] - zl[0], z[1] - zl[1]) <= VMAX * tau + 3 * SIG * 1.414
                for nm, pf in pfs.items():
                    if pf is None: idr[nm] = True; continue
                    pf.move(); idr[nm] = dead[nm] is None and pf.mass_near(z) >= 0.01
                res['id'] = idr; break
            kf.update(z); zl, kl = z, k
            for m in ray:
                if ray[m]['st'] in ('trk', 'prev'): ray[m]['st'] = 'trk'; ray[m]['cnt'] = 0
            pfs = {'ns': None, 'st': None}; dead = {'ns': None, 'st': None}
        else:
            rho = kf.rad(); s = vis(kf.x, kf.y, west)
            body = vt == 1 and not sup and math.hypot(kf.x - x, kf.y - y) < 0.3   # il raggio colpisce il corpo: non e' "piu' lontano"
            for m, rs in ray.items():
                if rs['st'] not in ('trk', 'prev'): continue
                if s == 1 and not body:
                    rs['cnt'] += 1
                    if rs['cnt'] >= m: rs['st'] = 'closed'; rs['kc'] = k; rs['hid'] = vt != 1; continue
                elif s == 2: rs['cnt'] = 0; rs['st'] = 'prev'
                if rho > 1.0: rs['st'] = 'unk'; rs['ke'] = k
            if do_pf:
                for nm in pfs:
                    if pfs[nm] is None: pfs[nm] = PF(kf, nm == 'st', rng, pdm)
                    else: pfs[nm].move()
                    pfs[nm].neg(west)
                    if pfs[nm].r < RDEAD and dead[nm] is None: dead[nm] = k
                    if k0 is not None and k - k0 <= 6: res['rmin_in'][nm] = min(res['rmin_in'].get(nm, 1), pfs[nm].r)
            if sup:
                e = {'j': ffk, 'ray1': ray[1]['st'], 'ray3': ray[3]['st'], 'disc_cont': vis(x, y, west) != 1}
                for nm, pf in pfs.items():
                    if pf: e[nm + '_r'] = pf.r; e[nm + '_near'] = pf.mass_near((x, y)); e[nm + '_sh'] = pf.mass_vis(west, 2)
                res['ff'].append(e)
        if k0 is not None and (k - k0) in EVF and vt != 1 and not seen and not ff:
            e = {}; rho = kf.rad(); n, nf, ns, _ = circ(kf.x, kf.y, rho, gt)
            sa = math.sqrt(kf.a); e['k_fmass'] = sum(1 for _ in range(200) if vis(kf.x + _GR.gauss(0, sa), kf.y + _GR.gauss(0, sa), w) == 1) / 200.
            e['k_cont'] = math.hypot(kf.x - x, kf.y - y) <= rho; e['k_free'] = nf / max(n, 1); e['k_area'] = math.pi * rho * rho / ASH
            e['k_cov'] = ns * CELL * CELL / ASH; e['k_rho'] = rho; e['k_cin'] = vis(kf.x, kf.y, w) == 1
            for m in ray: e['ray%d' % m] = ray[m]['st']
            rad = VMAX * (k - kl) * DT; n, nf, ns, nse = circ(zl[0], zl[1], rad, gt, ge)
            e['d_cont'] = math.hypot(zl[0] - x, zl[1] - y) <= rad and vis(x, y, west) != 1; e['d_free'] = nf / max(n, 1)
            e['d_area'] = n * CELL * CELL / ASH; e['d_cov'] = ns * CELL * CELL / ASH; e['d_unk'] = nse / max(nshe, 1) >= 0.9
            for nm, pf in pfs.items():
                if pf is None: continue
                h = pf.hpd(); e[nm + '_cont'] = (math.floor(x / .5), math.floor(y / .5)) in h; e[nm + '_free'] = pf.mass_vis(w, 1)
                e[nm + '_area'] = len(h) * .25 / ASH
                e[nm + '_cov'] = sum(1 for c in h if vis((c[0] + .5) * .5, (c[1] + .5) * .5, w) == 2) * .25 / ASH
                e[nm + '_r'] = pf.r; e[nm + '_dead'] = dead[nm] is not None
            res['ev'][EVF[k - k0]] = e
        if k0 is not None and k - k0 >= cap: break
    res['ray'] = ray; res['dead'] = dead; res['k0'] = k0
    return res


def mean(v): return sum(v) / len(v) if v else float('nan')
def pc(v): return '  n/d' if not v else '%5.1f' % (100 * mean([float(a) for a in v]))


def table(rs, title):
    print('\n== %s (prove %d) ==' % (title, len(rs)))
    print('tau  n_nasc | famiglia          contiene%  in_libere%  area/ombra%  copre_ombra%  stato')
    for tau in (0.5, 1.0, 2.0, 3.0):
        ev = [r['ev'][tau] for r in rs if tau in r['ev']]
        if not ev: print('%.1f  0' % tau); continue
        st = lambda m: ' '.join('%s=%s' % (s, pc([e['ray%d' % m] == s for e in ev]).strip()) for s in ('prev', 'closed', 'unk'))
        print('%.1f  %4d  | (a) cerchio KF95   %s      %s       %s        %s    raggio medio %.2f m; centro in cella libera %s%%; MASSA gaussiana in libere %s%%' % (tau, len(ev), pc([e['k_cont'] for e in ev]), pc([e['k_free'] for e in ev]), pc([e['k_area'] for e in ev]), pc([e['k_cov'] for e in ev]), mean([e['k_rho'] for e in ev]), pc([e['k_cin'] for e in ev]).strip(), pc([e['k_fmass'] for e in ev]).strip()))
        print('           | (a) +raggio H-014  M=1: %s | M=3: %s' % (st(1), st(3)))
        print('           | (b) disco H-009    %s      %s       %s        %s    sconosciuto(>=90%% ombra) %s%%' % (pc([e['d_cont'] for e in ev]), pc([e['d_free'] for e in ev]), pc([e['d_area'] for e in ev]), pc([e['d_cov'] for e in ev]), pc([e['d_unk'] for e in ev]).strip()))
        for nm, lab in (('ns', '(c) part. no sosta'), ('st', '(c) part. sosta   ')):
            e2 = [e for e in ev if nm + '_cont' in e]
            if e2: print('           | %s %s      %s       %s        %s    r medio %.2f; morte(r<0,05) %s%%' % (lab, pc([e[nm + '_cont'] for e in e2]), pc([e[nm + '_free'] for e in e2]), pc([e[nm + '_area'] for e in e2]), pc([e[nm + '_cov'] for e in e2]), mean([e[nm + '_r'] for e in e2]), pc([e[nm + '_dead'] for e in e2]).strip()))
    for m in (1, 3):
        cl = [r['ray'][m]['kc'] is not None and r['ray'][m]['hid'] for r in rs if r['k0'] is not None]
        tc = [(r['ray'][m]['kc'] - r['k0']) * DT for r in rs if r['ray'][m]['kc'] is not None and r['ray'][m]['hid'] and r['k0'] is not None]
        te = [(r['ray'][m]['ke'] - r['k0']) * DT for r in rs if r['ray'][m]['ke'] is not None and r['k0'] is not None]
        print('raggio M=%d: CHIUSA a soggetto non visibile %s%% (tempo medio %.2f s dall\'ingresso); scaduta a SCONOSCIUTO %s%% (a %.2f s)' % (m, pc(cl).strip(), mean(tc), pc([r['ray'][m]['ke'] is not None for r in rs if r['k0'] is not None]).strip(), mean(te)))
    ids = [r['id'] for r in rs if r['id']]
    if ids:
        print('identita\' tenuta alla prima ri-rilevazione (n=%d, tau medio %.2f s): ' % (len(ids), mean([i['tau'] for i in ids])) + '  '.join('%s=%s%%' % (k, pc([i[k] for i in ids]).strip()) for k in ('kf', 'kf15', 'ray1', 'ray3', 'disc', 'ns', 'st') if k in ids[0]))
    for nm in ('ns', 'st'):
        rm = [r['rmin_in'][nm] for r in rs if nm in r['rmin_in']]
        if rm: print('particelle %s: r minimo nei primi 6 fotogrammi d\'ombra < 0,5 in %s%% dei casi, < 0,05 in %s%%' % (nm, pc([a < 0.5 for a in rm]).strip(), pc([a < 0.05 for a in rm]).strip()))


def exp_main(w, n, seed, dw=0.0, behs=('prosegue', 'sosta', 'torna', 'lontano'), yped=4.0, do_pf=True, lab=''):
    for bi, beh in enumerate(behs):
        rng = random.Random(seed + bi); rs = [run_trial(beh, w, dw, rng, yped=yped, do_pf=do_pf) for _ in range(n)]
        table(rs, '%spannello %.0f m, ombra stimata %+.1f m, pedone a %.1f m, %s; area ombra %.2f m2' % (lab, w, dw, yped, beh, grid(w)[1] * .01))


def exp_falso(seed):
    for pdm in (0.9, 0.8, 0.7):
        for mode, w in (('open', 0.0), ('exit', 1.0)):
            rng = random.Random(seed); rs = [run_trial('prosegue', w, 0.0, rng, ff=(mode, 12), pdm=pdm) for _ in range(60)]
            print('\n== falso libero, %s, Pd del modello %.1f (60 prove): per fotogramma mancato j ==' % ('campo aperto' if mode == 'open' else 'uscita dall\'ombra (pannello 1 m)', pdm))
            print(' j  r_st   massa<0,5m(st)  r*massa  massa_in_ombra(st)  raggio1_chiusa%  raggio3_chiusa%  disco_contiene%')
            first = None
            for j in range(1, 13):
                es = [e for r in rs for e in r['ff'] if e['j'] == j and 'st_r' in e]
                if not es: continue
                rr = mean([e['st_r'] for e in es]); nr = mean([e['st_near'] for e in es]); pr = mean([e['st_r'] * e['st_near'] for e in es])
                if first is None and pr < 0.05: first = j
                print('%2d  %.3f  %.3f           %.3f    %.3f               %s            %s            %s' % (j, rr, nr, pr, mean([e['st_sh'] for e in es]), pc([e['ray1'] == 'closed' for e in es]), pc([e['ray3'] == 'closed' for e in es]), pc([e['disc_cont'] for e in es])))
            print('massa giusta (r x massa entro 0,5 m) sotto il 5 %% dal fotogramma j = %s' % first)
    for k in (1, 2, 3, 5):
        rng = random.Random(seed + 7); rs = [run_trial('prosegue', 1.0, 0.0, rng, ff=('exit', k), pdm=0.9) for _ in range(100)]
        ids = [r['id'] for r in rs if r['id']]
        print('uscita dall\'ombra non rilevata per k=%d fotogrammi poi rilevata (Pd modello 0,9, n=%d): identita\' tenuta ' % (k, len(ids)) + '  '.join('%s=%s%%' % (q, pc([i[q] for i in ids]).strip()) for q in ('kf', 'ray1', 'ray3', 'disc', 'ns', 'st')))


def exp_vmax(seed):
    print('\n== bersaglio veloce, pannello 2 m (ombra 4 m a 4 m), prosegue: contenimento a 0,5 s e identita\' alla riemersione ==')
    print('v     n   cerchioKF%  disco%  part_ns%  part_st% | identita\': kf  disco  ns  st')
    for v in (2.0, 2.4, 2.6, 3.0, 3.5):
        rng = random.Random(seed); rs = [run_trial('prosegue', 2.0, 0.0, rng, v=v) for _ in range(80)]
        ev = [r['ev'][0.5] for r in rs if 0.5 in r['ev']]; ids = [r['id'] for r in rs if r['id']]
        print('%.1f  %3d  %s      %s  %s    %s    | %s  %s  %s  %s' % (v, len(ev), pc([e['k_cont'] for e in ev]), pc([e['d_cont'] for e in ev]), pc([e['ns_cont'] for e in ev if 'ns_cont' in e]), pc([e['st_cont'] for e in ev if 'st_cont' in e]), pc([i['kf'] for i in ids]), pc([i['disc'] for i in ids]), pc([i['ns'] for i in ids]), pc([i['st'] for i in ids])))


def exp_due(seed):
    for beh in ('prosegue', 'torna'):
        for w in (1.0, 2.0):
            rng = random.Random(seed); out = []
            for _ in range(100):
                trs = [truth(beh, w, rng, sign=1), truth(beh, w, rng, sign=-1)]; kfs = [None, None]; zp = [None, None]; hid = [False, False]; pfs = [None, None]; zl = [None, None]; rec = None
                for k in range(min(len(trs[0]), len(trs[1]))):
                    dets = []
                    for t in (0, 1):
                        x, y = trs[t][k]; vt = vis(x, y, w); det = vt == 1 and rng.random() < PD
                        z = (x + rng.gauss(0, SIG), y + rng.gauss(0, SIG)) if det else None
                        if kfs[t] is None:
                            if det:
                                if zp[t] is None: zp[t] = (z, k)
                                else: kfs[t] = KF(zp[t][0], z, k - zp[t][1]); zl[t] = (z, k)
                            continue
                        kfs[t].predict()
                        if vt != 1: hid[t] = True
                        if det and not (hid[0] and hid[1]): kfs[t].update(z); zl[t] = (z, k); pfs[t] = None
                        elif not det:
                            if pfs[t] is None: pfs[t] = PF(kfs[t], True, rng, PD)
                            else: pfs[t].move()
                            pfs[t].neg(w)
                        if det and hid[0] and hid[1]: dets.append((t, z))
                    if dets and kfs[0] and kfs[1] and pfs[0] and pfs[1]:
                        t, z = dets[0]; d = [kfs[0].d2(z), kfs[1].d2(z)]
                        for q in (0, 1):
                            if not any(dd[0] == q for dd in dets): pass
                        m = [pfs[0].mass_near(z) * pfs[0].r, pfs[1].mass_near(z) * pfs[1].r]
                        dd = [math.hypot(z[0] - zl[q][0][0], z[1] - zl[q][0][1]) <= VMAX * (k - zl[q][1]) * DT for q in (0, 1)]
                        rec = {'kf_swap': (d[1 - t] < d[t]), 'kf_gate_wrong': d[1 - t] <= CHI99, 'kf_gate_right': d[t] <= CHI99, 'kf_amb': d[0] <= CHI99 and d[1] <= CHI99,
                               'pf_swap': m[1 - t] > m[t], 'pf_amb': min(m) >= 0.01, 'pf_none': max(m) < 0.01, 'disc_amb': dd[0] and dd[1]}
                        break
                if rec: out.append(rec)
            print('\n== due bersagli da lati opposti, %s entrambi, pannello %.0f m (n=%d): alla prima riemersione ==' % (beh, w, len(out)))
            print('  Kalman: scambio %s%%; misura nel cancello 99%% della traccia SBAGLIATA %s%%, della giusta %s%%; ambiguita\' visibile (in entrambi) %s%%' % (pc([o['kf_swap'] for o in out]).strip(), pc([o['kf_gate_wrong'] for o in out]).strip(), pc([o['kf_gate_right'] for o in out]).strip(), pc([o['kf_amb'] for o in out]).strip()))
            print('  scambio Kalman SENZA segnale di ambiguita\' (sbagliata nel cancello, giusta fuori): %s%%' % pc([o['kf_gate_wrong'] and not o['kf_gate_right'] for o in out]).strip())
            print('  particelle (sosta): scambio %s%%; ambiguita\' visibile %s%%; nessuna traccia compatibile %s%%' % (pc([o['pf_swap'] for o in out]).strip(), pc([o['pf_amb'] for o in out]).strip(), pc([o['pf_none'] for o in out]).strip()))
            print('  disco: misura in entrambi i dischi (ambiguo dichiarato) %s%%' % pc([o['disc_amb'] for o in out]).strip())


if __name__ == '__main__':
    e = sys.argv[1]; S = 20261114
    print('# esperimento %s, seme base %d, dt 1/15 s, sigma 5 cm, Pd %.1f, q %.1f, v_max %.1f, %d particelle' % (e, S, PD, Q, VMAX, NP))
    if e == 'main1': exp_main(1.0, 100, S + 100)
    elif e == 'main2': exp_main(2.0, 100, S + 200)
    elif e == 'ombra':
        exp_main(1.0, 100, S + 300, dw=-0.2, behs=('prosegue', 'sosta'), lab='OMBRA STRETTA ')
        exp_main(1.0, 100, S + 300, dw=+0.2, behs=('prosegue', 'sosta'), lab='OMBRA LARGA ')
    elif e == 'k001':
        for yp in (4.0, 3.0, 2.5): exp_main(1.0, 300, S + 400, behs=('sosta', 'prosegue'), yped=yp, do_pf=False)
    elif e == 'falso': exp_falso(S + 500)
    elif e == 'vmax': exp_vmax(S + 600)
    elif e == 'due': exp_due(S + 700)
