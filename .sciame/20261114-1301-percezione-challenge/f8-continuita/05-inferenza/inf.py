#!/usr/bin/env python3
# sciame-inferenza, f8 corsia A. Python puro, semi fissati. Uso: python3 inf.py <oracolo|pf|det|copertura|copertura_ist|falso|tempi>
# Scena e modello sono scritti in PREVISIONI.md (prima di questo file). Nessun codice di altri ruoli.
import sys, math, random, time, json, os

DT = 1 / 15; H = 0.1; INVH = 1 / H
X0 = -2.4; Y0 = 1.8; W = 48; HH = 44; NC = W * HH
Q = 0.2; SIG = 0.05; PD = 0.9
LS = 0.25; LG = 0.4; LR = 0.1
PS = LS * DT; PR = LR * DT; PG = LG * DT; PSR = PS + PR
SQ = math.sqrt(Q * DT)
BAND = 0.2; RANGE = 6.0; TANF = math.tan(math.radians(43.5))
PAN_Y = 2.0; SL = 0.25; KSL = math.sqrt(1 + SL * SL)
NCYC = 75
CK = [8, 15, 23, 30, 45, 60, 75]          # 0,53 1,0 1,53 2,0 3,0 4,0 5,0 s
BEH = ['prosegue', 'rallenta', 'ferma', 'torna', 'svolta', 'lontano']
HERE = os.path.dirname(os.path.abspath(__file__))


def in_fov(x, y):
    return y > 0 and abs(x) < y * TANF and x * x + y * y < RANGE * RANGE


def vis_true(x, y):            # il sensore vede davvero questo punto (per rilevare il soggetto)
    return in_fov(x, y) and not (y > PAN_Y and abs(x) < SL * y)


def vis_ne(x, y):              # visto libero OLTRE la fascia: qui vale l'evidenza negativa
    if not in_fov(x, y):
        return False
    if y < PAN_Y - BAND:
        return True
    return (abs(x) - SL * max(y, PAN_Y)) / KSL > BAND


CX = [X0 + (i + 0.5) * H for j in range(HH) for i in range(W)]
CY = [Y0 + (j + 0.5) * H for j in range(HH) for i in range(W)]
VNE = [vis_ne(CX[c], CY[c]) for c in range(NC)]
DCELLS = [c for c in range(NC) if not VNE[c]]                       # celle ammesse per la regione
CUNEO = [c for c in DCELLS if in_fov(CX[c], CY[c]) and CY[c] > PAN_Y - BAND]   # ombra + fascia
SHADOW = [c for c in range(NC) if in_fov(CX[c], CY[c]) and CY[c] > PAN_Y and abs(CX[c]) < SL * CY[c]]
LNE = [(1 - PD) if VNE[c] else 1.0 for c in range(NC)]


def cell_of(x, y):
    if x < X0 or y < Y0:
        return -1
    ci = int((x - X0) * INVH); cj = int((y - Y0) * INVH)
    if ci >= W or cj >= HH:
        return -1
    return cj * W + ci


# ---------------------------------------------------------------- condizioni iniziali e verità
def kpred(s):
    p, v, a, b, c = s
    return [p + v * DT, v, a + 2 * b * DT + c * DT * DT + Q * DT ** 3 / 3, b + c * DT + Q * DT * DT / 2, c + Q * DT]


def kupd(s, z):
    p, v, a, b, c = s
    S = a + SIG * SIG; k1 = a / S; k2 = b / S; r = z - p
    return [p + k1 * r, v + k2 * r, a - k1 * a, b - k1 * b, c - k2 * b]


def make_ic(seed):
    rng = random.Random(seed)
    s = rng.uniform(1.0, 1.5); y0 = 4 + rng.uniform(-0.3, 0.3)
    x = -2.9; kx = ky = None; last = None
    while True:
        x += s * DT
        if abs(x) < SL * y0:
            break
        if kx is not None:
            kx = kpred(kx); ky = kpred(ky)
        if rng.random() < PD:
            zx = x + rng.gauss(0, SIG); zy = y0 + rng.gauss(0, SIG)
            if kx is None:
                kx = [zx, 0.0, SIG * SIG, 0.0, 4.0]; ky = [zy, 0.0, SIG * SIG, 0.0, 4.0]
            else:
                kx = kupd(kx, zx); ky = kupd(ky, zy)
            last = (list(kx), list(ky), x)
    kx, ky, xt = last
    return dict(kx=kx, ky=ky, xt=xt, y0=y0, s=s, seed=seed)


def truth_path(ic, beh, rng):
    xt, y0, s = ic['xt'], ic['y0'], ic['s']
    ten = max(0.0, (-SL * y0 - xt) / s); T = 2 * SL * y0 / s
    tc = ten + rng.uniform(0.15, 0.75) * T; xc = xt + s * tc
    dur = rng.uniform(2, 4); sg = rng.choice((-1, 1)); path = []
    for k in range(1, NCYC + 1):
        t = k * DT
        if t <= tc or beh == 'prosegue':
            x = xt + s * t; y = y0
        else:
            d = t - tc
            if beh == 'rallenta': x = xc + 0.4 * s * d; y = y0
            elif beh == 'ferma': x = xc + s * max(0.0, d - dur); y = y0
            elif beh == 'torna': x = xc - s * d; y = y0
            elif beh == 'svolta': x = xc + s * d * 0.5; y = y0 + sg * s * d * 0.8660254
            else: x = xc; y = y0 + s * d
        path.append((x, y))
    return path


# ---------------------------------------------------------------- regioni e misure
def hdr(mg, p, tot=None):
    it = [(mg[c], c) for c in DCELLS if mg[c] > 0]
    if tot is None:
        tot = sum(v for v, _ in it)
    it.sort(reverse=True)
    acc = 0.0; R = set(); lim = p * tot
    for v, c in it:
        R.add(c); acc += v
        if acc >= lim:
            break
    return R


def massa_d(mg):
    return sum(mg[c] for c in DCELLS)


def liscia(g):
    h = [a + b + c for a, b, c in zip([0.0] + g[:-1], g, g[1:] + [0.0])]
    return [(a + b + c) / 9 for a, b, c in zip([0.0] * W + h[:-W], h, h[W:] + [0.0] * W)]


def iou(A, B):
    u = len(A | B)
    return len(A & B) / u if u else 1.0


def massa_in(R, ref, totref):
    return sum(ref[c] for c in R) / totref


def componenti(R):
    R = set(R); n = 0
    while R:
        n += 1; st = [R.pop()]
        while st:
            c = st.pop()
            for d in (c - 1, c + 1, c - W, c + W):
                if d in R:
                    R.remove(d); st.append(d)
    return n


def media_d(mg):
    t = sx = sy = 0.0
    for c in DCELLS:
        v = mg[c]
        if v:
            t += v; sx += v * CX[c]; sy += v * CY[c]
    return (sx / t, sy / t) if t > 0 else (0.0, 0.0)


def map_d(mg):
    b = max(DCELLS, key=lambda c: mg[c])
    return (CX[b], CY[b])


def med(v):
    v = sorted(v); n = len(v)
    return float('nan') if n == 0 else (v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2]))


def pct(v, q):
    v = sorted(v)
    return float('nan') if not v else v[min(len(v) - 1, int(q * len(v)))]


def mean(v):
    return sum(v) / len(v) if v else float('nan')


# ---------------------------------------------------------------- filtro a particelle su M*
def sistematico(w, N, rnd):
    u = rnd() / N; c = w[0]; i = 0; out = []; n1 = N - 1; inv = 1.0 / N
    for j in range(N):
        t = u + j * inv
        while c < t and i < n1:
            i += 1; c += w[i]
        out.append(i)
    return out


def pf_run(ic, N, seed, schema='sist', pd=PD, ne=True, ncyc=NCYC, keep=None, stop_ne_from=None, probe=None):
    """Rende, per ciclo, (marginale per cella normalizzato sul totale, massa fuori griglia, evidenza del ciclo).
    keep: insieme dei cicli da conservare (None = tutti). probe: funzione(k, px, py, w) chiamata dopo il peso."""
    rng = random.Random(seed); rnd = rng.random; gauss = rng.gauss
    kx, ky = ic['kx'], ic['ky']
    px = []; py = []; vx = []; vy = []
    for (lp, lv, s) in ((px, vx, kx), (py, vy, ky)):
        p0, v0, a, b, c = s; sa = math.sqrt(a); sc = math.sqrt(max(1e-12, c - b * b / a)); g = b / a
        for i in range(N):
            dp = gauss(0, sa); lp.append(p0 + dp); lv.append(v0 + g * dp + gauss(0, sc))
    st = [0] * N; w = [1.0 / N] * N; om = 1 - pd; out = {}
    for k in range(1, ncyc + 1):
        cnt = [0.0] * NC; fuori = 0.0; tot = 0.0
        for i in range(N):
            if st[i]:
                if rnd() < PG:
                    st[i] = 0
            else:
                r = rnd()
                if r < PS:
                    st[i] = 1
                elif r < PSR:
                    vx[i] = -vx[i]; vy[i] = -vy[i]
            if not st[i]:
                vx[i] += gauss(0.0, SQ); vy[i] += gauss(0.0, SQ)
                px[i] += vx[i] * DT; py[i] += vy[i] * DT
            x = px[i]; y = py[i]; wi = w[i]
            if x >= X0 and y >= Y0:
                ci = int((x - X0) * INVH); cj = int((y - Y0) * INVH)
                if ci < W and cj < HH:
                    idx = cj * W + ci
                    if ne and VNE[idx]:
                        wi *= om; w[i] = wi
                    cnt[idx] += wi; tot += wi
                    continue
            if ne and vis_ne(x, y):
                wi *= om; w[i] = wi
            fuori += wi; tot += wi
        inv = 1.0 / tot
        w = [a * inv for a in w]
        if probe is not None:
            probe(k, px, py, w, tot)
        if keep is None or k in keep:
            out[k] = ([a * inv for a in cnt], fuori * inv, tot)
        if schema == 'multi':
            ids = rng.choices(range(N), weights=w, k=N)
        else:
            ess = 1.0 / sum(a * a for a in w)
            ids = sistematico(w, N, rnd) if ess < 0.5 * N else None
        if ids is not None:
            px = [px[i] for i in ids]; py = [py[i] for i in ids]; vx = [vx[i] for i in ids]
            vy = [vy[i] for i in ids]; st = [st[i] for i in ids]; w = [1.0 / N] * N
    return out


# ---------------------------------------------------------------- miscela di gaussiane troncata senza memoria
def mg_run(ic, ncyc=NCYC, lne=LNE):
    kx, ky = ic['kx'], ic['ky']
    p0x, v0x, ax, bx, cx = kx; p0y, v0y, ay, by, cy = ky
    w = [1.0, 0.0, 0.0, 0.0]; m = [0.0] * 4; e2 = [0.0] * 4; mt = [0.0] * 4     # M, S, R, SR
    TR = [[(0, 1 - PS - PR), (1, PS), (2, PR)], [(0, PG), (1, 1 - PG)], [(2, 1 - PS - PR), (3, PS), (0, PR)], [(2, PG), (3, 1 - PG)]]
    DEL = [DT, 0.0, -DT, 0.0]; out = {}
    for k in range(1, ncyc + 1):
        nw = [0.0] * 4; nm = [0.0] * 4; ne2 = [0.0] * 4; nmt = [0.0] * 4
        for i in range(4):
            for j, p in TR[i]:
                f = w[i] * p; nw[j] += f; nm[j] += f * m[i]; ne2[j] += f * e2[i]; nmt[j] += f * mt[i]
        for j in range(4):
            if nw[j] > 0:
                mm = nm[j] / nw[j]; ee = ne2[j] / nw[j]; tt = nmt[j] / nw[j]; d = DEL[j]
                m[j] = mm + d; e2[j] = ee + 2 * d * mm + d * d; mt[j] = tt + abs(d)
            w[j] = nw[j]
        g = [0.0] * NC
        for j in range(4):
            if w[j] < 1e-5:
                continue
            s = max(0.0, e2[j] - m[j] * m[j]); qn = Q * mt[j] ** 3 / 3
            sxx = ax + 2 * m[j] * bx + e2[j] * cx + s * v0x * v0x + qn
            syy = ay + 2 * m[j] * by + e2[j] * cy + s * v0y * v0y + qn
            sxy = s * v0x * v0y; det = sxx * syy - sxy * sxy
            ixx = syy / det; iyy = sxx / det; ixy = -sxy / det
            mx = p0x + v0x * m[j]; my = p0y + v0y * m[j]
            kn = w[j] * H * H / (2 * math.pi * math.sqrt(det)); ex = math.exp
            hx = -0.5 * ixx; hy = -0.5 * iyy
            g = [a + kn * ex(hx * (x - mx) ** 2 + hy * (y - my) ** 2 - ixy * (x - mx) * (y - my)) for a, x, y in zip(g, CX, CY)]
        ingr = sum(g); fuori = max(0.0, 1 - ingr)
        g = [a * l for a, l in zip(g, lne)]
        tot = sum(g) + fuori
        out[k] = ([a / tot for a in g], fuori / tot, tot)
    return out


# ---------------------------------------------------------------- istogramma posizione x velocita' discreta
NV = 7; DV = 0.5; VL = [-1.5 + DV * i for i in range(NV)]


def ist_run(ic, ncyc=NCYC):
    kx, ky = ic['kx'], ic['ky']
    p0x, v0x, ax = kx[0], kx[1], kx[2]; p0y, v0y, ay = ky[0], ky[1], ky[2]
    sx = max(ax, (0.4 * H) ** 2); sy = max(ay, (0.4 * H) ** 2)
    pos = [math.exp(-0.5 * ((x - p0x) ** 2 / sx + (y - p0y) ** 2 / sy)) for x, y in zip(CX, CY)]
    t = sum(pos); pos = [a / t for a in pos]

    def lin(v, var):
        f = min(NV - 1 - 1e-9, max(0.0, (v + 1.5) / DV)); i = int(f)
        if os.environ.get('IST_VECCHIO'):
            return {i: 1 - (f - i), i + 1: f - i}
        i0 = min(NV - 2, max(1, int(round(f)))); d = (f - i0) * DV      # tre nodi: media e varianza del Kalman
        wp = (var + d * d) / (2 * DV * DV) + d / (2 * DV); wm = (var + d * d) / (2 * DV * DV) - d / (2 * DV)
        if wp < 0 or wm < 0 or wp + wm > 1:
            return {i: 1 - (f - i), i + 1: f - i}
        return {i0 - 1: wm, i0: 1 - wp - wm, i0 + 1: wp}
    wx = lin(v0x, kx[4]); wy = lin(v0y, ky[4]); winit = [0.0] * (NV * NV)
    for i, a in wx.items():
        for j, b in wy.items():
            winit[i * NV + j] = a * b
    NM = NV * NV
    g = [[a * winit[mo] for a in pos] if winit[mo] > 0 else [0.0] * NC for mo in range(NM)] + [[0.0] * NC]
    pv = Q * DT / (2 * DV * DV); keep = 1 - 4 * pv - PS - PR
    accx = [0.0] * NM; accy = [0.0] * NM; out = {}; persa = 0.0
    zc0 = [j * W for j in range(HH)]; zc1 = [j * W + W - 1 for j in range(HH)]; zrow = [0.0] * W
    for k in range(1, ncyc + 1):
        gs = g[NM]; ng = []
        for i in range(NV):
            for j in range(NV):
                mo = i * NV + j
                n1 = g[(i - 1) * NV + j] if i > 0 else g[mo]
                n2 = g[(i + 1) * NV + j] if i < NV - 1 else g[mo]
                n3 = g[i * NV + j - 1] if j > 0 else g[mo]
                n4 = g[i * NV + j + 1] if j < NV - 1 else g[mo]
                mi = g[(NV - 1 - i) * NV + (NV - 1 - j)]; wi = PG * winit[mo]
                ng.append([keep * a + pv * (b + c + d + e) + PR * f + wi * s for a, b, c, d, e, f, s in zip(g[mo], n1, n2, n3, n4, mi, gs)])
        tot_mov = [sum(col) for col in zip(*g[:NM])]
        ng.append([(1 - PG) * s + PS * a for s, a in zip(gs, tot_mov)])
        g = ng
        for i in range(NV):
            for j in range(NV):
                mo = i * NV + j; a = g[mo]
                accx[mo] += VL[i] * DT * INVH; accy[mo] += VL[j] * DT * INVH
                while accx[mo] >= 1:
                    accx[mo] -= 1; a = [0.0] + a[:-1]
                    for z in zc0: a[z] = 0.0
                while accx[mo] <= -1:
                    accx[mo] += 1; a = a[1:] + [0.0]
                    for z in zc1: a[z] = 0.0
                while accy[mo] >= 1:
                    accy[mo] -= 1; a = zrow + a[:-W]
                while accy[mo] <= -1:
                    accy[mo] += 1; a = a[W:] + zrow
                g[mo] = a
        mg = [sum(col) for col in zip(*g)]
        pre = sum(mg)
        mgw = [a * l for a, l in zip(mg, LNE)]
        tot = sum(mgw)
        g = [[a * l / tot for a, l in zip(gm, LNE)] for gm in g]
        out[k] = ([a / tot for a in mgw], 0.0, tot / pre if pre > 0 else 0.0)
    return out


# ---------------------------------------------------------------- cerchio del nucleo
def nucleo_run(ic, ncyc=NCYC):
    kx, ky = ic['kx'], ic['ky']; out = {}
    for k in range(1, ncyc + 1):
        t = k * DT
        a = max(kx[2] + 2 * t * kx[3] + t * t * kx[4], ky[2] + 2 * t * ky[3] + t * t * ky[4]) + Q * t ** 3 / 3
        r2 = 5.991 * a; mx = kx[0] + kx[1] * t; my = ky[0] + ky[1] * t
        R = set(c for c in CUNEO if (CX[c] - mx) ** 2 + (CY[c] - my) ** 2 <= r2)
        out[k] = (R, len(R) < 0.5 * len(CUNEO), (mx, my), a)
    return out


def gauss_cells(mx, my, a):
    return [H * H / (2 * math.pi * a) * math.exp(-0.5 * ((x - mx) ** 2 + (y - my) ** 2) / a) for x, y in zip(CX, CY)]


# ================================================================ comandi
def cmd_oracolo():
    N = int(os.environ.get('NORA', '40000')); res = {}
    t0 = time.time()
    for s in range(101, 106):
        ic = make_ic(s)
        for sd in (1, 2):
            o = pf_run(ic, N, 9000 + 10 * s + sd, 'sist', keep=set(CK))
            res['%d_%d' % (s, sd)] = {str(k): [round(a, 7) for a in o[k][0]] for k in CK}
            print('oracolo ic', s, 'seme', sd, 'fatto a', round(time.time() - t0, 1), 's', flush=True)
    json.dump(res, open(os.path.join(HERE, 'oracolo.json'), 'w'))
    for k in CK:
        v = []; m = []
        for s in range(101, 106):
            a = res['%d_1' % s][str(k)]; b = res['%d_2' % s][str(k)]
            Ra = hdr(a, 0.9); Rb = hdr(b, 0.9); v.append(iou(Ra, Rb)); m.append(massa_in(Ra, b, massa_d(b)))
        print('tetto del rumore dell\'oracolo, t=%.2f s: IoU fra i due semi %.3f; massa del seme 2 nella regione 90%% del seme 1 %.3f' % (k * DT, mean(v), mean(m)))


def carica_oracolo():
    res = json.load(open(os.path.join(HERE, 'oracolo.json'))); ref = {}
    for s in range(101, 106):
        ref[s] = {k: [0.5 * (a + b) for a, b in zip(res['%d_1' % s][str(k)], res['%d_2' % s][str(k)])] for k in CK}
    return ref


def cmd_pf():
    ref = carica_oracolo()
    VAR = [(100, 'sist'), (250, 'multi'), (250, 'sist'), (1000, 'multi'), (1000, 'sist'), (4000, 'sist')]
    SEEDS = (11, 12, 13); KS = (15, 30, 45)
    print('Particelle contro oracolo (5 condizioni iniziali x 3 semi). Per riga: N, ricampionamento, estrazione;')
    print('a 1/2/3 s: IoU fra semi | IoU con l\'oracolo | massa dell\'oracolo nella regione "90%" | area m2 | n. pezzi; tremolio medio fra cicli')
    for N, sch in VAR:
        acc = {e: {k: dict(ss=[], so=[], mo=[], ar=[], nc=[]) for k in KS} for e in ('grezza', 'lisciata')}
        fl = {'grezza': [], 'lisciata': []}
        for s in range(101, 106):
            ic = make_ic(s); regs = {e: [] for e in acc}
            for sd in SEEDS:
                o = pf_run(ic, N, 1000 * sd + s, sch)
                for e in acc:
                    prev = None; rr = {}
                    for k in range(1, NCYC + 1):
                        mg = o[k][0] if e == 'grezza' else liscia(o[k][0])
                        R = hdr(mg, 0.9)
                        if prev is not None:
                            fl[e].append(1 - iou(R, prev))
                        prev = R
                        if k in KS:
                            rr[k] = R
                    regs[e].append(rr)
            for e in acc:
                for k in KS:
                    o_ = ref[s][k]; to = massa_d(o_); Ro = hdr(o_, 0.9); a = acc[e][k]
                    for i in range(3):
                        R = regs[e][i][k]
                        a['so'].append(iou(R, Ro)); a['mo'].append(massa_in(R, o_, to)); a['ar'].append(len(R) * H * H); a['nc'].append(componenti(R))
                        for j in range(i + 1, 3):
                            a['ss'].append(iou(R, regs[e][j][k]))
        for e in acc:
            row = ' ; '.join('%.2f | %.2f | %.3f | %.2f | %.0f' % (mean(acc[e][k]['ss']), mean(acc[e][k]['so']), mean(acc[e][k]['mo']), mean(acc[e][k]['ar']), mean(acc[e][k]['nc'])) for k in KS)
            print('N=%4d %-5s %-8s  %s ; tremolio %.3f' % (N, sch, e, row, mean(fl[e])), flush=True)


def cmd_det():
    ref = carica_oracolo()
    print('Deterministici contro oracolo (5 condizioni iniziali). Per istante: IoU con l\'oracolo | massa dell\'oracolo nella regione 90% | area m2 | n. pezzi')
    R = {n: {k: dict(so=[], mo=[], ar=[], nc=[]) for k in CK} for n in ('MG', 'IST', 'NUCLEO95', 'ORACOLO')}
    fl = {'MG': [], 'IST': []}; ex = dict(gs=[], qg=[], lim=[], em=[])
    step = {n: {'media': [], 'map': []} for n in ('MG', 'IST')}
    for s in range(101, 106):
        ic = make_ic(s); runs = {'MG': mg_run(ic), 'IST': ist_run(ic)}; nu = nucleo_run(ic)
        for n in ('MG', 'IST'):
            prev = None; pm = None; pM = None; sm = 0.0; sM = 0.0
            for k in range(1, NCYC + 1):
                mg = runs[n][k][0]; Rk = hdr(mg, 0.9)
                if prev is not None:
                    fl[n].append(1 - iou(Rk, prev))
                prev = Rk
                a = media_d(mg); b = map_d(mg)
                if pm is not None:
                    sm = max(sm, math.hypot(a[0] - pm[0], a[1] - pm[1])); sM = max(sM, math.hypot(b[0] - pM[0], b[1] - pM[1]))
                pm = a; pM = b
                if k in CK:
                    o_ = ref[s][k]; to = massa_d(o_); Ro = hdr(o_, 0.9); d = R[n][k]
                    d['so'].append(iou(Rk, Ro)); d['mo'].append(massa_in(Rk, o_, to)); d['ar'].append(len(Rk) * H * H); d['nc'].append(componenti(Rk))
            step[n]['media'].append(sm); step[n]['map'].append(sM)
        for k in CK:
            o_ = ref[s][k]; to = massa_d(o_); Ro = hdr(o_, 0.9)
            d = R['ORACOLO'][k]; d['so'].append(1.0); d['mo'].append(massa_in(Ro, o_, to)); d['ar'].append(len(Ro) * H * H); d['nc'].append(componenti(Ro))
            Rn, emesso, (mx, my), a = nu[k]
            d = R['NUCLEO95'][k]; d['so'].append(iou(Rn, Ro)); d['mo'].append(massa_in(Rn, o_, to)); d['ar'].append(len(Rn) * H * H); d['nc'].append(1)
            if k in (15, 30, 45):
                gc = gauss_cells(mx, my, a); gS = sum(gc[c] for c in DCELLS); gES = sum(gc[c] for c in Rn)
                ex['gs'].append((k, gS)); ex['qg'].append((k, gES / gS)); ex['lim'].append((k, 1 - 0.05 / gS)); ex['em'].append((k, emesso))
    for n in R:
        print(n)
        for k in CK:
            d = R[n][k]
            print('  t=%.2f s: IoU %.2f | massa oracolo mediana %.3f (min %.3f) | area %.2f | pezzi %.1f' % (k * DT, med(d['so']), med(d['mo']), min(d['mo']), med(d['ar']), mean(d['nc'])))
    print('tremolio medio fra cicli: MG %.4f, IST %.4f' % (mean(fl['MG']), mean(fl['IST'])))
    for n in step:
        print('punto mostrato, passo massimo per sequenza (m): %s media %s ; massimo a posteriori %s' % (n, ['%.2f' % v for v in step[n]['media']], ['%.2f' % v for v in step[n]['map']]))
    print('Ritaglio senza rinormalizzare (gaussiana del Kalman G, S = celle ammesse, cerchio al 95%):')
    for k in (15, 30, 45):
        print('  t=%.1f s: G(S) mediana %.3f; livello nella gaussiana troncata G(E∩S)/G(S) mediana %.3f (min %.3f); limite 1-0,05/G(S) mediana %.3f; violazioni del limite %d; regione emessa dal nucleo in %d casi su 5'
              % (k * DT, med([v for kk, v in ex['gs'] if kk == k]), med([v for kk, v in ex['qg'] if kk == k]), min([v for kk, v in ex['qg'] if kk == k]),
                 med([v for kk, v in ex['lim'] if kk == k]),
                 sum(1 for (ka, q), (kb, l) in zip(ex['qg'], ex['lim']) if ka == k and q < l - 0.01), sum(1 for kk, v in ex['em'] if kk == k and v)))
    print('area del cuneo (ombra + fascia) %.2f m2; ombra vera %.2f m2' % (len(CUNEO) * H * H, len(SHADOW) * H * H))


def _valuta(nome, seqs, ics, rng_seed=777, reps=3):
    """seqs[ic_index][k] = (R50, R90 | None, punto, emessa, pD). Copertura per comportamento e istante."""
    print('== %s: copertura 50%% | 90%% (n) per comportamento, a soggetto ancora non rilevato; area90/ombra; quota di cicli con regione emessa' % nome)
    ash = len(SHADOW)
    tot = {k: [0, 0, 0] for k in CK}
    salto_p = []; salto_r = []
    for beh in BEH:
        row = []; emit = [0, 0]
        for k in CK:
            row.append([0, 0, 0])
        for ii, ic in enumerate(ics):
            rng = random.Random(rng_seed + 31 * ic['seed'] + BEH.index(beh))
            for rep in range(reps):
                path = truth_path(ic, beh, rng); kd = None
                for k in range(1, NCYC + 1):
                    x, y = path[k - 1]
                    if vis_true(x, y) and rng.random() < PD:
                        kd = k; break
                last = (kd - 1) if kd else NCYC
                for k in range(1, last + 1):
                    emit[1] += 1; emit[0] += 1 if seqs[ii][k][3] else 0
                if kd and kd > 1:
                    R50, R90, pt, em, pD = seqs[ii][kd - 1]; x, y = path[kd - 1]
                    salto_p.append(math.hypot(x - pt[0], y - pt[1]))
                    if R90:
                        salto_r.append(min(math.hypot(x - CX[c], y - CY[c]) for c in R90))
                for q, k in enumerate(CK):
                    if k > last:
                        continue
                    R50, R90, pt, em, pD = seqs[ii][k]; c = cell_of(*path[k - 1])
                    row[q][2] += 1; tot[k][2] += 1
                    if em:
                        if c in R50: row[q][0] += 1; tot[k][0] += 1
                        if c in R90: row[q][1] += 1; tot[k][1] += 1
        print('  %-9s ' % beh + ' ; '.join(('t=%.1f: %3.0f | %3.0f (%d)' % (k * DT, 100 * r[0] / r[2], 100 * r[1] / r[2], r[2])) if r[2] else 't=%.1f: - (0)' % (k * DT) for k, r in zip(CK, row)) + ' ; emessa %.0f%%' % (100 * emit[0] / max(1, emit[1])))
    print('  TUTTI     ' + ' ; '.join('t=%.1f: %3.0f | %3.0f (%d)' % (k * DT, 100 * tot[k][0] / max(1, tot[k][2]), 100 * tot[k][1] / max(1, tot[k][2]), tot[k][2]) for k in CK))
    ar = {k: [] for k in CK}
    for ii in range(len(ics)):
        for k in CK:
            if seqs[ii][k][3]:
                ar[k].append(len(seqs[ii][k][1]) / ash)
    print('  area90/ombra (mediana, quando emessa): ' + ' ; '.join('t=%.1f: %.2f' % (k * DT, med(ar[k])) for k in CK))
    print('  alla ricomparsa: distanza fra prima misura (vero) e punto mostrato al ciclo prima: mediana %.2f m, 95o pct %.2f m; distanza dalla regione 90%% del ciclo prima: mediana %.2f m, 95o pct %.2f m (n=%d)'
          % (med(salto_p), pct(salto_p, 0.95), med(salto_r), pct(salto_r, 0.95), len(salto_p)))


def cmd_copertura(which):
    ics = [make_ic(s) for s in range(201, 231)]
    if which == 'ist':
        seqs = []
        for ic in ics:
            o = ist_run(ic); d = {}
            for k in range(1, NCYC + 1):
                mg = o[k][0]; d[k] = (hdr(mg, 0.5) if k in CK else None, hdr(mg, 0.9), media_d(mg), True, massa_d(mg))
            seqs.append(d)
        _valuta('IST (istogramma)', seqs, ics)
        return
    sm = []; sn = []; sp = []; sb = []
    stepm = []; stepM = []; back = []; fuoriD = 0; ncic = 0
    pfm = []; pfM = []
    for ic in ics:
        o = mg_run(ic); d = {}; pm = pM = None; a1 = a2 = 0.0; bk = 0.0
        for k in range(1, NCYC + 1):
            mg = o[k][0]; pt = media_d(mg); mp = map_d(mg)
            d[k] = (hdr(mg, 0.5) if k in CK else None, hdr(mg, 0.9), pt, True, massa_d(mg))
            ncic += 1; c = cell_of(*pt); fuoriD += 1 if (c < 0 or VNE[c]) else 0
            if pm:
                a1 = max(a1, math.hypot(pt[0] - pm[0], pt[1] - pm[1])); a2 = max(a2, math.hypot(mp[0] - pM[0], mp[1] - pM[1]))
                bk = max(bk, (pm[0] - pt[0]) / DT)
            pm = pt; pM = mp
        sm.append(d); stepm.append(a1); stepM.append(a2); back.append(bk)
        nu = nucleo_run(ic)
        sn.append({k: (nu[k][0], nu[k][0], nu[k][2], nu[k][1], 1.0) for k in nu})
        kx, ky = ic['kx'], ic['ky']; d = {}
        for k in range(1, NCYC + 1):          # linea di base: cerchio al 95% NON ritagliato (solo per confronto)
            Rn, em, (mx, my), a = nu[k]; r2 = 5.991 * a
            R = set(c for c in range(NC) if (CX[c] - mx) ** 2 + (CY[c] - my) ** 2 <= r2)
            d[k] = (R, R, (mx, my), True, 1.0)
        sb.append(d)
        o = pf_run(ic, 1000, 5000 + ic['seed'], 'sist'); d = {}; pm = pM = None; a1 = a2 = 0.0
        for k in range(1, NCYC + 1):
            mg = liscia(o[k][0]); pt = media_d(mg); mp = map_d(mg)
            d[k] = (hdr(mg, 0.5) if k in CK else None, hdr(mg, 0.9), pt, True, massa_d(mg))
            if pm:
                a1 = max(a1, math.hypot(pt[0] - pm[0], pt[1] - pm[1])); a2 = max(a2, math.hypot(mp[0] - pM[0], mp[1] - pM[1]))
            pm = pt; pM = mp
        sp.append(d); pfm.append(a1); pfM.append(a2)
    _valuta('MG (miscela troncata)', sm, ics)
    _valuta('PF N=1000 sistematico, lisciata', sp, ics)
    _valuta('NUCLEO (cerchio 95% ritagliato, finche\' < meta\' del cuneo; colonna 50% = stessa regione)', sn, ics)
    _valuta('BASE: cerchio 95% non ritagliato (colonna 50% = stessa regione)', sb, ics)
    print('Punto mostrato su MG, 30 sequenze: passo massimo fra cicli, media a posteriori: max %.3f m, mediana %.3f; massimo a posteriori: max %.2f m, mediana %.2f, sequenze con passo > 0,30 m: %d su 30'
          % (max(stepm), med(stepm), max(stepM), med(stepM), sum(1 for v in stepM if v > 0.30)))
    print('  velocita\' massima di arretramento della media (m/s): max %.2f, mediana %.2f ; cicli con la media su cella vista libera o fuori griglia: %d su %d' % (max(back), med(back), fuoriD, ncic))
    print('Punto mostrato su PF N=1000 lisciata, 30 sequenze: passo massimo, media: max %.3f m, mediana %.3f; massimo a posteriori: max %.2f m, mediana %.2f, sequenze con passo > 0,30 m: %d su 30'
          % (max(pfm), med(pfm), max(pfM), med(pfM), sum(1 for v in pfM if v > 0.30)))
    # errore del punto: fermo all'ultima posizione, velocita' costante, media MG
    print('Errore del punto (mediana, m) a soggetto non rilevato: fermo | velocita\' costante | media MG')
    for beh in BEH:
        row = []
        for k in (15, 30, 45, 75):
            e0 = []; e1 = []; e2 = []
            for ii, ic in enumerate(ics):
                rng = random.Random(777 + 31 * ic['seed'] + BEH.index(beh))
                for rep in range(3):
                    path = truth_path(ic, beh, rng); kd = None
                    for kk in range(1, NCYC + 1):
                        x, y = path[kk - 1]
                        if vis_true(x, y) and rng.random() < PD:
                            kd = kk; break
                    if kd and kd <= k:
                        continue
                    x, y = path[k - 1]; kx, ky = ic['kx'], ic['ky']; t = k * DT
                    e0.append(math.hypot(x - kx[0], y - ky[0])); e1.append(math.hypot(x - kx[0] - kx[1] * t, y - ky[0] - ky[1] * t))
                    pt = sm[ii][k][2]; e2.append(math.hypot(x - pt[0], y - pt[1]))
            row.append('t=%.0f: %.2f | %.2f | %.2f (%d)' % (k * DT, med(e0), med(e1), med(e2), len(e0)))
        print('  %-9s ' % beh + ' ; '.join(row))


def cmd_falso():
    N = int(os.environ.get('NFAL', '8000')); KM = (3, 5, 7); PB = 0.05
    res = {n: {k: [] for k in KM} for n in ('nominale', 'temperata', 'miscela')}
    zero = {k: [0, 0] for k in KM}; wb2 = []; ar = []
    for s in range(301, 311):
        ic = make_ic(s); xt, y0, sp = ic['xt'], ic['y0'], ic['s']
        ke = None                         # primo ciclo in cui il vero e' oltre la fascia d'uscita
        for k in range(1, NCYC + 1):
            x = xt + sp * k * DT
            if x > 0 and vis_ne(x, y0):
                ke = k; break
        kmax = ke + max(KM) - 1; snap = {}

        def mk(name):
            def probe(k, px, py, w, tot):
                d = snap.setdefault(name, {'ev': 1.0, 'm': {}, 'n': {}}); d['ev'] *= tot
                for kk in KM:
                    if k == ke + kk - 1:
                        x = xt + sp * k * DT; m = 0.0; n = 0
                        for a, b, c in zip(px, py, w):
                            if (a - x) ** 2 + (b - y0) ** 2 < 0.25:
                                m += c; n += 1
                        d['m'][kk] = m; d['n'][kk] = n; d['evk_%d' % kk] = d['ev']
            return probe
        pf_run(ic, N, 40 + s, 'sist', ncyc=kmax, keep=set(), probe=mk('A'))
        pf_run(ic, N, 50 + s, 'sist', pd=0.5, ncyc=kmax, keep=set(), probe=mk('T'))
        pf_run(ic, N, 60 + s, 'sist', ne=False, ncyc=kmax, keep=set(), probe=mk('B'))
        for kk in KM:
            mA = snap['A']['m'][kk]; mB = snap['B']['m'][kk]; ev = snap['A']['evk_%d' % kk]
            wB = PB / (PB + (1 - PB) * ev)
            res['nominale'][kk].append(mA); res['temperata'][kk].append(snap['T']['m'][kk]); res['miscela'][kk].append((1 - wB) * mA + wB * mB)
            if kk == 5:
                wb2.append(wB)
        for sd in (1, 2, 3):
            snap.pop('P', None)
            pf_run(ic, 1000, 70 + 10 * s + sd, 'sist', ncyc=kmax, keep=set(), probe=mk('P'))
            for kk in KM:
                zero[kk][1] += 1; zero[kk][0] += 1 if snap['P']['n'][kk] == 0 else 0
    print('Falso "vuoto": soggetto riemerso oltre la fascia e non rilevato per k cicli di fila (10 condizioni iniziali, N=%d).' % N)
    print('Massa a posteriori entro 0,5 m dal vero (mediana [min, max]) e quota dei casi con massa >= 1% (cancello del torneo):')
    for n in res:
        print('  %-9s ' % n + ' ; '.join('k=%d: %.4f [%.4f, %.4f], >=1%%: %d/10' % (kk, med(res[n][kk]), min(res[n][kk]), max(res[n][kk]), sum(1 for v in res[n][kk] if v >= 0.01)) for kk in KM))
    print('  particelle N=1000 nominali, nessuna particella entro 0,5 m dal vero: ' + ' ; '.join('k=%d: %d/%d' % (kk, zero[kk][0], zero[kk][1]) for kk in KM))
    print('  peso del ramo "sensore cieco" (probabilita\' iniziale %.2f) a k=5: mediana %.3f [%.3f, %.3f]' % (PB, med(wb2), min(wb2), max(wb2)))


def cmd_tempi():
    ic = make_ic(101)
    def t(f, n=1):
        t0 = time.perf_counter(); f(); return (time.perf_counter() - t0) / n
    print('Tempo per ciclo e per oggetto, Python puro, compresa (dove indicato) l\'estrazione della regione al 90% (ms):')
    for N in (250, 1000, 4000):
        a = t(lambda: pf_run(ic, N, 1, 'sist', ncyc=45, keep=set()), 45) * 1000
        print('  PF N=%d sistematico: %.2f ms' % (N, a))
    a = t(lambda: mg_run(ic, ncyc=45), 45) * 1000; print('  MG 4 gaussiane su %d celle: %.2f ms' % (NC, a))
    a = t(lambda: ist_run(ic, ncyc=30), 30) * 1000; print('  IST %d modi x %d celle = %d stati: %.2f ms' % (NV * NV + 1, NC, (NV * NV + 1) * NC, a))
    o = mg_run(ic, ncyc=30)[30][0]
    a = t(lambda: [hdr(o, 0.9) for _ in range(50)], 50) * 1000; b = t(lambda: [liscia(o) for _ in range(50)], 50) * 1000
    c = t(lambda: [media_d(o) for _ in range(50)], 50) * 1000
    print('  estrazione: regione al 90%% %.2f ms; lisciatura 3x3 %.2f ms; media %.2f ms' % (a, b, c))


if __name__ == '__main__':
    c = sys.argv[1]
    t0 = time.time()
    print('# inf.py', c, '— avviato', time.strftime('%Y-%m-%dT%H:%M:%S'))
    if c == 'oracolo': cmd_oracolo()
    elif c == 'pf': cmd_pf()
    elif c == 'det': cmd_det()
    elif c == 'copertura': cmd_copertura('mg')
    elif c == 'copertura_ist': cmd_copertura('ist')
    elif c == 'falso': cmd_falso()
    elif c == 'tempi': cmd_tempi()
    print('# durata %.1f s' % (time.time() - t0))
