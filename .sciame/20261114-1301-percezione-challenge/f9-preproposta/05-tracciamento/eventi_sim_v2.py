#!/usr/bin/env python3
# eventi_sim.py -- sciame-tracciamento, f9: banco piccolo per S11 (macchina degli eventi) e attacco 2.
# Python puro, semi fissati. Uso: timeout 120 python3 eventi_sim.py [N=400] [Pd=0.9] [pf=0.0]
# Modello (scelte mie, dichiarate in PREVISIONI.md): sensore fermo in (0,0), asse +y, campo +-43,5 gradi,
# zona 1,24-3 m; pannello largo 1 m a y=1,8; attore puntiforme; 15 Hz; rumore 4 cm; Kalman a velocita' quasi
# costante q=0,2; porta 99 %; conferma 3 su 5; regole B5 del nucleo. Non importa nessun simulatore esistente.
import math, os, random, sys, time

SMOOTH = int(os.environ.get('SMOOTH', '1'))
DT = 1 / 15.0; Q = 0.2; SIG = 0.04; R = SIG * SIG; GATE = 9.21
FOV = math.radians(43.5); RMIN = 1.24; RMAX = 3.0
YP = 1.8; HWP = 0.5; PHI = math.atan2(HWP, YP)
BAND = 0.40; CUT = 0.20; EDGE = 0.5


UX = math.sin(PHI); UY = math.cos(PHI)


def d_shadow(x, y, has):
    """distanza dal cuneo d'ombra del pannello (0 se dentro); il cuneo e' simmetrico, uso |x|"""
    if not has:
        return 9.0
    ax = abs(x)
    if y >= YP and math.atan2(ax, y) <= PHI:
        return 0.0
    if y < YP and ax <= HWP:
        return YP - y
    s = (ax - HWP) * UX + (y - YP) * UY          # proiezione sul bordo (semiretta dallo spigolo)
    if s <= 0:
        return math.hypot(ax - HWP, y - YP)
    return abs((ax - HWP) * UY - (y - YP) * UX)


def in_zone(x, y):
    r = math.hypot(x, y)
    return RMIN <= r <= RMAX and abs(math.atan2(x, y)) <= FOV


def edge_dist(x, y):
    r = math.hypot(x, y); ph = abs(math.atan2(x, y))
    return min(RMAX - r, r - RMIN, r * math.sin(max(0.0, FOV - ph)))


def visible(x, y, has):
    return in_zone(x, y) and d_shadow(x, y, has) > 0.0


# ---------------------------------------------------------------- scenari (verita')
def scen(name, rng):
    """ritorna (has_panel, [traiettorie], info); traiettoria = lista di (x,y) per ciclo"""
    side = rng.choice((-1, 1)); v = rng.uniform(0.5, 1.4); Y = 2.3
    def line(x0, x1, sp, y=Y):
        n = max(1, int(abs(x1 - x0) / (sp * DT))); return [(x0 + (x1 - x0) * i / n, y) for i in range(1, n + 1)]
    def hold(p, sec):
        return [p] * int(sec / DT)
    def flip(tr):
        return [(side * x, y) for (x, y) in tr]
    info = {}
    if name == 'transito':
        A = [(-2.1, Y)] + line(-2.1, 2.1, v)
        return True, [flip(A)], info
    if name in ('sosta_poi', 'sosta_perm'):
        xs = rng.uniform(-0.4, 0.4); A = [(-2.1, Y)] + line(-2.1, xs, v)
        A += hold((xs, Y), rng.uniform(2, 4) if name == 'sosta_poi' else 10.0)
        if name == 'sosta_poi':
            A += line(xs, 2.1, v)
        return True, [flip(A)], info
    if name == 'torna':
        xs = rng.uniform(-0.3, 0.4); A = [(-2.1, Y)] + line(-2.1, xs, v) + hold((xs, Y), 0.2) + line(xs, -2.1, v)
        return True, [flip(A)], info
    if name == 'lontano':
        xs = rng.uniform(-0.3, 0.3); A = [(-2.1, Y)] + line(-2.1, xs, v)
        r0 = math.hypot(xs, Y); n = int((3.3 - r0) / (v * DT))
        A += [(xs * (r0 + (3.3 - r0) * i / n) / r0, Y * (r0 + (3.3 - r0) * i / n) / r0) for i in range(1, n + 1)]
        A += hold(A[-1], 6.0)
        return True, [flip(A)], info
    if name == 'sosta_vista':
        xs = rng.uniform(-0.8, 0.8); A = [(-2.1, Y)] + line(-2.1, xs, v) + hold((xs, Y), 3.0) + line(xs, 2.1, v)
        return False, [flip(A)], info
    if name == 'avv_diretto':
        x0 = rng.uniform(-0.3, 0.3); n = int((3.2 - 1.35) / (v * DT))
        A = [(x0, 3.2 - (3.2 - 1.35) * i / n) for i in range(n + 1)]
        A += hold(A[-1], 2.0)
        return False, [A], info
    if name == 'secondo':   # A entra e resta; B, mai tracciato, esce dalla stessa ombra
        xs = rng.uniform(-0.4, 0.4); A = [(-2.1, Y)] + line(-2.1, xs, v); nin = len(line(-2.1, -0.64, v))
        delay = rng.uniform(0.5, 3.0); vb = rng.uniform(0.5, 1.4); sb = rng.choice((-1, 1)); xb = rng.uniform(-0.3, 0.3)
        B = hold((xb, Y), nin * DT + delay) + line(xb, sb * 2.1, vb)
        A += hold((xs, Y), max(0.0, (len(B) - len(A)) * DT) + 3.0)
        info['vb'] = vb; info['delay'] = delay
        return True, [flip(A), flip(B)], info
    if name == 'due_escono':  # A transita; B, mai tracciato, esce dopo A dallo stesso lato
        A = [(-2.1, Y)] + line(-2.1, 2.1, v); tA = (2.1 + 0.64) / v
        gap = rng.uniform(0.6, 1.5); vb = rng.uniform(0.5, 1.4); xb = rng.uniform(-0.3, 0.3)
        t0 = max(0.0, tA + gap - (0.64 - xb) / vb)
        B = hold((xb, Y), t0) + line(xb, 2.1, vb)
        return True, [flip(A), flip(B)], info
    if name == 'tripla':     # stessa persona, esce a velocita' tripla
        A = [(-2.1, Y)] + line(-2.1, -0.64, v) + line(-0.64, 2.1, 3 * v); info['v3'] = 3 * v
        return True, [flip(A)], info
    raise SystemExit(name)


def detections(has, trajs, T, rng, pd, pf):
    """per ciclo: lista di (x, y, cut, soggetto)"""
    out = []
    for k in range(T):
        fr = []
        for s, tr in enumerate(trajs):
            x, y = tr[min(k, len(tr) - 1)]
            if visible(x, y, has) and rng.random() < pd:
                fr.append((x + rng.gauss(0, SIG), y + rng.gauss(0, SIG), d_shadow(x, y, has) < CUT, s))
        u = rng.random(); sd = rng.choice((-1, 1)); e1 = rng.gauss(0, 0.03); e2 = rng.gauss(0, 0.03)
        fr.append(('F', u, sd, e1, e2))          # falso al bordo: usato solo se pende una traccia e u < pf
        out.append(fr)
    return out


# ---------------------------------------------------------------- inseguitore + macchina degli eventi
class Trk:
    __slots__ = ('id', 'px', 'py', 'vx', 'vy', 'P', 'conf', 'hist', 'mode', 'miss', 'lastz', 'lastv', 'klastv', 'kpend',
                 'alert', 'first', 'cand', 'ev', 'c', 's', 'born', 'occ_emitted', 'sosta', 'ident', 'kreatt', 'buf')
    def __init__(s, i, z, k):
        s.id = i; s.px, s.py = z; s.vx = s.vy = 0.0; s.P = [[R, 0.0, 1.0], [R, 0.0, 1.0]]
        s.conf = False; s.hist = [1]; s.mode = 'obs'; s.miss = 0; s.lastz = z; s.lastv = z; s.klastv = k; s.kpend = -1
        s.alert = False; s.first = z; s.cand = None; s.c = {}; s.s = {}; s.born = k; s.occ_emitted = False
        s.sosta = False; s.ident = 'propria'; s.kreatt = -1; s.buf = [(k, z)]
    def predict(s):
        s.px += s.vx * DT; s.py += s.vy * DT
        for P in s.P:
            a, b, c = P
            P[0] = a + 2 * b * DT + c * DT * DT + Q * DT ** 3 / 3; P[1] = b + c * DT + Q * DT * DT / 2; P[2] = c + Q * DT
    def d2(s, z):
        return (z[0] - s.px) ** 2 / (s.P[0][0] + R) + (z[1] - s.py) ** 2 / (s.P[1][0] + R)
    def update(s, z, k):
        for ax in (0, 1):
            a, b, c = s.P[ax]; S = a + R; K1 = a / S; K2 = b / S
            inn = z[ax] - (s.px if ax == 0 else s.py)
            if ax == 0:
                s.px += K1 * inn; s.vx += K2 * inn
            else:
                s.py += K1 * inn; s.vy += K2 * inn
            s.P[ax] = [(1 - K1) * a, (1 - K1) * b, c - K2 * b]
        s.lastz = z; s.lastv = z; s.klastv = k; s.miss = 0; s.buf.append((k, z)); del s.buf[:-24]
    def reinit(s, z, k):   # rientro: velocita' dalla traiettoria virtuale ultima misura valida -> nuova misura
        dt = max(DT, (k - s.klastv) * DT)
        s.vx = (z[0] - s.lastv[0]) / dt; s.vy = (z[1] - s.lastv[1]) / dt; s.px, s.py = z
        s.P = [[R, 0.0, 0.25], [R, 0.0, 0.25]]; s.lastz = z; s.lastv = z; s.klastv = k; s.miss = 0; s.buf = [(k, z)]


def mass_in_wedge(t, has):
    """massa gaussiana dell'ipotesi di transito ancora nel cuneo dilatato di CUT (quadratura 9x9, +-2,5 sigma)"""
    sx = math.sqrt(t.P[0][0]); sy = math.sqrt(t.P[1][0]); tot = 0.0; ins = 0.0
    for i in range(-4, 5):
        wi = math.exp(-0.5 * (i * 0.625) ** 2)
        for j in range(-4, 5):
            w = wi * math.exp(-0.5 * (j * 0.625) ** 2); tot += w
            if d_shadow(t.px + i * 0.625 * sx, t.py + j * 0.625 * sy, has) < CUT:
                ins += w
    return ins / tot


def vwin(t, k):
    """velocita' a finestra: differenza fra due medie di misure valide distanti circa 1 s (come la regola «mobile»)"""
    a = [(kk, z) for (kk, z) in t.buf if k - kk <= 3]; b = [(kk, z) for (kk, z) in t.buf if 12 <= k - kk <= 17]
    if len(a) < 2 or len(b) < 2:
        return None
    ka = sum(q[0] for q in a) / len(a); kb = sum(q[0] for q in b) / len(b); dt = (ka - kb) * DT
    return ((sum(q[1][0] for q in a) / len(a) - sum(q[1][0] for q in b) / len(b)) / dt,
            (sum(q[1][1] for q in a) / len(a) - sum(q[1][1] for q in b) / len(b)) / dt)


def hyst(t, key, on, off, n_on, n_off):
    c = t.c; st = t.s.get(key, False)
    if not st:
        c[key] = c.get(key, 0) + 1 if on else 0
        if c[key] >= n_on:
            t.s[key] = True; c[key] = 0; return True
    else:
        c[key] = c.get(key, 0) + 1 if off else 0
        if c[key] >= n_off:
            t.s[key] = False; c[key] = 0
    return False


def t_atteso(t, k, has):
    """tempo d'attraversamento atteso del cuneo dilatato lungo la direzione d'ingresso (regola a tempo di cor2)"""
    vw = vwin(t, k) or (t.vx, t.vy); sp = math.hypot(*vw)
    if sp < 1e-3:
        return 9.0
    ux = vw[0] / sp; uy = vw[1] / sp; x, y = t.lastv; ent = False; L = 6.0; i = 0
    while i < 300:
        i += 1; qx = x + ux * 0.02 * i; qy = y + uy * 0.02 * i
        ins = d_shadow(qx, qy, has) < CUT
        if ins:
            ent = True
        if (ent and not ins) or not in_zone(qx, qy):
            L = 0.02 * i; break
    return L / max(0.3, sp - 0.07) + 0.5


def run(has, dets, T, cfg, pf, log):
    """cfg: lit=True (preproposta alla lettera) oppure False (corretta). Ritorna eventi [(k, tipo, id, info)]"""
    lit = cfg['v'] == 'lit'; v2 = cfg['v'] == 'cor2'; coast = not lit
    trks = []; ev = []; nid = [0]; ledger = []
    def new(z, k):
        nid[0] += 1; t = Trk(nid[0], z, k); trks.append(t); return t
    for k in range(T):
        fr = dets[k]; real = [d for d in fr if d[0] != 'F']; fal = [d for d in fr if d[0] == 'F'][0]
        pend = [t for t in trks if t.mode == 'pend']
        if pf > 0 and pend and fal[1] < pf:
            real = real + [(fal[2] * (HWP * 2.3 / YP + 0.30) + fal[3], 2.3 + fal[4], False, -1)]
        for t in trks:
            t.predict()
        used = [False] * len(real)
        # 1) tracce osservate / non confermate: porta al 99 %, confermate per prime, avido per distanza
        act = [t for t in trks if t.mode in ('obs', 'nonconf') or (coast and t.mode == 'pend' and k - t.kpend < 3 and t.cand is None)]
        pairs = []
        for t in act:
            for j, d in enumerate(real):
                if d[2]:
                    if math.hypot(d[0] - t.px, d[1] - t.py) < 0.5:
                        pairs.append((0 if t.conf else 1, 100.0, t, j))
                else:
                    q = t.d2(d)
                    if q <= GATE:
                        pairs.append((0 if t.conf else 1, q, t, j))
        pairs.sort(key=lambda p: (p[0], p[1])); got = set()
        for _, q, t, j in pairs:
            if t.id in got or used[j]:
                continue
            got.add(t.id); used[j] = True; d = real[j]
            if d[2]:
                t.lastz = (d[0], d[1]); t.miss = 0; t.hist.append(1)
                if t.mode == 'pend':
                    t.mode = 'obs'; t.alert = False
            else:
                t.update((d[0], d[1]), k); t.hist.append(1)
                if t.mode == 'pend':
                    t.alert = False
                t.mode = 'obs'
        # 2) riaggancio dall'ombra (regola del nucleo: entro la fascia, una sola pendente)
        pend = [t for t in trks if t.mode == 'pend' and t.id not in got]
        for j, d in enumerate(real):
            if used[j] or d[2] or d_shadow(d[0], d[1], has) > BAND:
                continue
            if len(pend) == 1:
                p = pend[0]
                if p.kreatt < 0:   # registro delle porte alla prima occasione
                    g1 = p.d2(d) <= GATE
                    r0 = math.hypot(*p.lastv); hw = HWP * r0 / math.hypot(HWP, YP) + CUT; s2 = (2 * hw / math.sqrt(12)) ** 2 + R
                    g2 = (d[0] ** 2 + (d[1] - r0) ** 2) / s2 <= GATE
                    log['gate'] = (g1, g2, (k - p.kpend) * DT, d[3]); p.kreatt = k
                if lit:
                    used[j] = True; p.reinit((d[0], d[1]), k); p.mode = 'obs'; p.alert = False; got.add(p.id)
                    ev.append((k, 'RIAPPARIZIONE_CONFERMATA', p.id, d[3])); pend = []
                elif not any(t.cand == p.id for t in trks):
                    used[j] = True; c = new((d[0], d[1]), k); c.cand = p.id; got.add(c.id)
        # 3) mancate misure
        for t in list(trks):
            if t.id in got or t.born == k:
                continue
            t.hist.append(0)
            if not t.conf:
                if sum(1 for h in t.hist[-5:] if h == 0) >= 3:
                    trks.remove(t)
                continue
            if t.mode == 'pend':
                continue
            t.miss += 1
            if t.miss == 1 and d_shadow(t.lastz[0], t.lastz[1], has) <= BAND:
                t.mode = 'pend'; t.alert = True; t.kpend = k; t.occ_emitted = False; t.sosta = False; t.kreatt = -1; t.s['mu'] = 0
                t.s['surv'] = 1.0; t.s['ric'] = False; t.s['Tatt'] = t_atteso(t, k, has) if v2 else 0.0
            else:
                t.mode = 'nonconf'
                if t.miss > 3:
                    trks.remove(t); x, y = t.lastv
                    if lit:
                        ev.append((k, 'USCITA_AREA', t.id, None))
                    else:
                        out = not in_zone(x + 0.5 * t.vx, y + 0.5 * t.vy)
                        ev.append((k, 'USCITA_DAL_CAMPO' if (edge_dist(x, y) < EDGE and out) else 'NON_PIU_RILEVATO', t.id, None))
        # 4) nuove tracce
        for j, d in enumerate(real):
            if not used[j] and not d[2]:
                new((d[0], d[1]), k)
        # 5) conferme, eventi
        for t in list(trks):
            if not t.conf and sum(t.hist[-5:]) >= 3:
                t.conf = True
                if t.cand is not None:            # riapparizione confermata 3 su 5 (macchina corretta)
                    p = [q for q in trks if q.id == t.cand and q.mode == 'pend']
                    if p:
                        trks.remove(p[0]); old = t.id; t.id = p[0].id; t.ident = 'presunta'; t.c = p[0].c; t.s = p[0].s
                        ev.append((k, 'RIAPPARSO_ID_PRESUNTA', t.id, None)); t.cand = None; ledger.append(t.id); continue
                    t.cand = None
                x, y = t.first
                if lit:
                    ev.append((k, 'INGRESSO_AREA', t.id, None))
                elif d_shadow(x, y, has) <= BAND:
                    ev.append((k, 'COMPARSA_DA_OMBRA', t.id, None))
                    for qid in ledger:          # registro dell'ombra: vale anche per tracce gia' chiuse
                        ev.append((k, 'ID_AMBIGUA_RETROATTIVA', qid, None))
                    del ledger[:]
                elif edge_dist(x, y) < EDGE:
                    ev.append((k, 'INGRESSO_DAL_BORDO', t.id, None))
                else:
                    ev.append((k, 'COMPARSA_IN_CAMPO', t.id, None))
            if not t.conf:
                continue
            if t.mode == 'pend':
                n = k - t.kpend + 1
                if not t.occ_emitted and n >= (1 if lit else 3):
                    t.occ_emitted = True; ev.append((k, 'OCCLUSIONE_IN_CORSO', t.id, None))
                if v2:
                    if not t.sosta and (k - t.kpend) * DT > t.s['Tatt']:
                        t.sosta = True; ev.append((k, 'NON_RIEMERSO_T', t.id, None))
                    continue
                f = mass_in_wedge(t, has); mu2 = 0.2 / (0.2 + 0.8 * f)
                if lit:
                    if mu2 > 0.5 and not t.sosta:
                        ev.append((k, 'SOSTA_IN_OMBRA', t.id, None))
                    t.sosta = mu2 > 0.5
                    t.s['surv'] *= (1 - 0.9 * (1 - f))
                    if not t.s['ric'] and 0.2 / (0.2 + 0.8 * t.s['surv']) > 0.5:
                        t.s['ric'] = True; ev.append((k, 'SOSTA_RICORSIVA', t.id, None))
                else:
                    t.s['mu'] = t.s.get('mu', 0) + 1 if mu2 > 0.8 else 0
                    if t.s['mu'] >= 5 and not t.sosta:
                        t.sosta = True; ev.append((k, 'NON_RIEMERSO_SOSTA_PRESUNTA', t.id, None))
            elif t.mode == 'obs' and t.klastv == k:
                vx, vy = t.vx, t.vy
                if v2:
                    vw = vwin(t, k)
                    if vw is None:
                        continue
                    vx, vy = vw
                sp = math.hypot(vx, vy); r = math.hypot(t.px, t.py)
                rd = (t.px * vx + t.py * vy) / r; thd = abs(t.px * vy - t.py * vx) / (r * r)
                if lit:
                    a = sp > 0.2 and thd > 0.15; b = sp > 0.2 and thd <= 0.15 and rd < -0.2
                    if a and not t.s.get('A'):
                        ev.append((k, 'ATTRAVERSAMENTO', t.id, None))
                    if b and not t.s.get('B'):
                        ev.append((k, 'AVVICINAMENTO_DIRETTO', t.id, None))
                    t.s['A'] = a; t.s['B'] = b
                else:
                    dcpa = abs(t.px * vy - t.py * vx) / sp if sp > 1e-6 else r
                    n1, n2, n3 = (5, 8, 8) if v2 else (8, 8, 15)
                    hyst(t, 'M', sp > 0.30, sp < 0.15, n1, n3)
                    mv = t.s.get('M', False)
                    if hyst(t, 'B', mv and dcpa < 0.5 and rd < -0.3, (not mv) or dcpa > 0.8 or rd > -0.1, n1, n2):
                        ev.append((k, 'AVVICINAMENTO_DIRETTO', t.id, None))
                    if hyst(t, 'A', mv and dcpa > 0.8, (not mv) or dcpa < 0.5, n1, n2):
                        ev.append((k, 'ATTRAVERSAMENTO', t.id, None))
        log.setdefault('alert', []).append(any(t.alert for t in trks if t.mode == 'pend'))
    log['end_pend'] = sum(1 for t in trks if t.mode == 'pend' and t.alert)
    return ev


# ---------------------------------------------------------------- misure
def pc(a, b):
    return 100.0 * a / b if b else float('nan')


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    pd = float(sys.argv[2]) if len(sys.argv) > 2 else 0.9
    pf = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    names = ['transito', 'sosta_poi', 'sosta_perm', 'torna', 'lontano', 'sosta_vista', 'avv_diretto', 'secondo', 'due_escono', 'tripla']
    print("# eventi_sim.py N=%d Pd=%.2f pf=%.3f SMOOTH=%d seme base 20261114 ; unita': il passaggio" % (N, pd, pf, SMOOTH))
    nfr = 0; t0 = time.perf_counter(); tot = {}
    for si, name in enumerate(names):
        res = {'lit': {}, 'cor': {}, 'cor2': {}}
        def add(v, key, n=1):
            res[v][key] = res[v].get(key, 0) + n
        delays = {'lit': [], 'cor': [], 'cor2': [], 'ric': []}
        for i in range(N):
            rng = random.Random(20261114 * 1000 + si * 100000 + i)
            has, trajs, info = scen(name, rng); T = max(len(t) for t in trajs) + 15
            if SMOOTH > 1:
                trajs = [[(sum(q[0] for q in tr[max(0, j - SMOOTH + 1):j + 1]) / len(tr[max(0, j - SMOOTH + 1):j + 1]), sum(q[1] for q in tr[max(0, j - SMOOTH + 1):j + 1]) / len(tr[max(0, j - SMOOTH + 1):j + 1])) for j in range(len(tr))] for tr in trajs]
            dets = detections(has, trajs, T, rng, pd, pf)
            A = trajs[0]
            def posA(k):
                return A[min(k, len(A) - 1)]
            hidA = [in_zone(*posA(k)) and d_shadow(posA(k)[0], posA(k)[1], has) == 0.0 for k in range(T)]
            anyhid = [any(d_shadow(tr[min(k, len(tr) - 1)][0], tr[min(k, len(tr) - 1)][1], has) == 0.0 for tr in trajs) for k in range(T)]
            k_in = next((k for k in range(T) if hidA[k]), None)
            k_out = next((k for k in range(k_in or 0, T) if k_in is not None and not hidA[k]), None)
            for v in ('lit', 'cor', 'cor2'):
                log = {}; ev = run(has, dets, T, {'v': v}, pf, log); nfr += T
                cnt = {}
                for e in ev:
                    cnt[e[1]] = cnt.get(e[1], 0) + 1
                for key, n in cnt.items():
                    add(v, 'n_' + key, n)
                add(v, 'N')
                na = cnt.get('ATTRAVERSAMENTO', 0); nb = cnt.get('AVVICINAMENTO_DIRETTO', 0)
                add(v, 'P1_piu_di_un_fronte', 1 if (na > 1 or nb > 1) else 0)
                exp_a = 2 if name == 'sosta_vista' else (0 if name == 'avv_diretto' else 99); exp_b = 1 if name == 'avv_diretto' else 0
                add(v, 'P1_oltre_la_verita', 1 if (na > exp_a or nb > exp_b) else 0)
                add(v, 'P1_mancato', 1 if ((name == 'avv_diretto' and nb == 0) or (name == 'sosta_vista' and na == 0)) else 0)
                # P2: uscita emessa col soggetto A dentro la zona
                fu = 0; nu = 0
                for e in ev:
                    if e[1] in ('USCITA_AREA', 'USCITA_DAL_CAMPO'):
                        nu += 1
                        if in_zone(*posA(e[0])) and (len(trajs) == 1):
                            fu = 1
                add(v, 'P2_uscita_falsa', fu)
                add(v, 'P2_uscita_mancata', 1 if (nu == 0 and len(trajs) == 1 and name not in ('sosta_perm', 'lontano', 'avv_diretto')) else 0)
                add(v, 'frammentata', 1 if (cnt.get('NON_PIU_RILEVATO', 0) + cnt.get('COMPARSA_IN_CAMPO', 0)) > 0 else 0)
                # P3: sosta
                skey = {'lit': 'SOSTA_IN_OMBRA', 'cor': 'NON_RIEMERSO_SOSTA_PRESUNTA', 'cor2': 'NON_RIEMERSO_T'}[v]
                se = [e for e in ev if e[1] == skey]
                add(v, 'P3_sosta_emessa', 1 if se else 0)
                if se and k_in is not None:
                    add(v, 'P3_sosta_prima_della_riemersione', 1 if (k_out is None or se[0][0] < k_out) else 0)
                    delays[v].append((se[0][0] - k_in) * DT)
                add(v, 'P3_fronti_sosta_oltre_1', 1 if len(se) > 1 else 0)
                add(v, 'P3_sosta_emessa_a_soggetto_nascosto_o_dopo', 1 if (k_in is not None and any(e[0] >= k_in for e in se)) else 0)
                if v == 'lit':
                    sr = [e for e in ev if e[1] == 'SOSTA_RICORSIVA' and k_in is not None and e[0] >= k_in]
                    add(v, 'RIC_sosta_ricorsiva_emessa_dopo_ingresso', 1 if sr else 0)
                    add(v, 'RIC_prima_della_riemersione', 1 if (sr and (k_out is None or sr[0][0] < k_out)) else 0)
                    if sr:
                        delays['ric'].append((sr[0][0] - k_in) * DT)
                # P4/P5: porte alla prima occasione di riaggancio
                if 'gate' in log:
                    g1, g2, tt, subj = log['gate']
                    add(v, 'G_occasioni'); add(v, 'G_in_porta_transito', 1 if g1 else 0); add(v, 'G_in_porta_una_delle_due', 1 if (g1 or g2) else 0)
                    add(v, 'G_soggetto_sbagliato', 1 if subj not in (0,) else 0)
                    add(v, 'G_sbagliato_e_in_porta', 1 if (subj != 0 and g1) else 0)
                    if name == 'tripla':
                        add(v, 'G_occ_uscita_entro_vmax' if info['v3'] <= 2.5 else 'G_occ_uscita_oltre_vmax'); add(v, ('G_in_porta_transito_entro_vmax' if info['v3'] <= 2.5 else 'G_in_porta_transito_oltre_vmax'), 1 if g1 else 0)
                # riapparizione a soggetto A nascosto (scambio o falso)
                rkey = 'RIAPPARIZIONE_CONFERMATA' if v == 'lit' else 'RIAPPARSO_ID_PRESUNTA'
                rw = [e for e in ev if e[1] == rkey and hidA[e[0]]]
                add(v, 'RIAPP_con_A_nascosto', 1 if rw else 0)
                add(v, 'RIAPP_piu_di_una', 1 if cnt.get(rkey, 0) > 1 else 0)
                add(v, 'RIAPP_mancata', 1 if (cnt.get(rkey, 0) == 0 and name in ('transito', 'sosta_poi', 'torna', 'tripla')) else 0)
                # strato 1 spento con A nascosto, dopo il primo ciclo d'occlusione dichiarata
                al = log['alert']; rel = 0
                if k_in is not None:
                    kon = next((k for k in range(k_in, T) if al[k]), None)
                    if kon is not None and any(hidA[k] and not al[k] for k in range(kon, T)):
                        rel = 1
                    if kon is None:
                        add(v, 'strato1_mai_nato')
                add(v, 'strato1_spento_con_A_nascosto', rel)
                # P7: occlusione falsa
                fo = 0
                for e in ev:
                    if e[1] == 'OCCLUSIONE_IN_CORSO':
                        x, y = posA(e[0])
                        if len(trajs) == 1 and in_zone(x, y) and d_shadow(x, y, has) >= CUT:
                            fo = 1
                add(v, 'P7_occlusione_falsa', fo)
                add(v, 'P7_occlusioni_oltre_1', 1 if cnt.get('OCCLUSIONE_IN_CORSO', 0) > 1 else 0)
                add(v, 'P7_strato_acceso_a_fine_senza_nascosti', 1 if (log['end_pend'] > 0 and not anyhid[T - 1]) else 0)
                add(v, 'INGRESSI_oltre_1', 1 if cnt.get('INGRESSO_AREA', 0) + cnt.get('INGRESSO_DAL_BORDO', 0) > 1 else 0)
        print("\n== %s" % name)
        for v in ('lit', 'cor', 'cor2'):
            r = res[v]; n = r['N']
            keys = sorted(k for k in r if k != 'N')
            print(" [%s] " % {'lit': 'alla lettera', 'cor': 'corretta    ', 'cor2': 'cor2        '}[v] + " ; ".join("%s=%d" % (k, r[k]) for k in keys if k.startswith('n_')))
            print("      " + " ; ".join("%s=%d/%d" % (k, r[k], n) for k in keys if not k.startswith('n_') and not k.startswith('G_')))
            if 'G_occasioni' in r:
                print("      porte alla prima occasione: " + " ; ".join("%s=%d" % (k, r[k]) for k in keys if k.startswith('G_')))
            d = sorted(delays[v])
            if d:
                print("      ritardo evento di sosta dall'ingresso in ombra: n=%d mediana %.2f s, p10 %.2f, p90 %.2f" % (len(d), d[len(d) // 2], d[len(d) // 10], d[(9 * len(d)) // 10]))
            if v == 'lit' and delays['ric']:
                d = sorted(delays['ric']); print("      [ricorsiva, esplorativa] ritardo: n=%d mediana %.2f s, p10 %.2f, p90 %.2f" % (len(d), d[len(d) // 2], d[len(d) // 10], d[(9 * len(d)) // 10]))
            tot[(name, v)] = r
    el = time.perf_counter() - t0
    print("\n# tempo: %.1f s per %d cicli (inseguitore + eventi, Python puro): %.1f microsecondi per ciclo" % (el, nfr, 1e6 * el / nfr))
    # riepilogo P2 su tutti gli scenari a un soggetto
    for v in ('lit', 'cor', 'cor2'):
        a = sum(tot[(nm, v)].get('P2_uscita_falsa', 0) for nm in names[:7]); b = sum(tot[(nm, v)]['N'] for nm in names[:7])
        fr = sum(tot[(nm, v)].get('frammentata', 0) for nm in names[:7])
        print("# P2 [%s] uscite false su scenari a un soggetto: %d/%d = %.2f %% ; (corretta) passaggi con NON_PIU_RILEVATO o COMPARSA_IN_CAMPO: %d" % (v, a, b, pc(a, b), fr))


if __name__ == '__main__':
    main()
