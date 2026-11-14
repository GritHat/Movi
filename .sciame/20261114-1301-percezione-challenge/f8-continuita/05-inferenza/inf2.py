#!/usr/bin/env python3
# sciame-inferenza, f8 corsia A, seconda serie (P13-P18). Uso: python3 inf2.py <mgx|ist025|pf2|falso2|pezzi>
import sys, math, random, time, os
import inf
from inf import *

LT = 0.15; PT = LT * DT


def conn_d():
    S = set(DCELLS); seed = SHADOW[len(SHADOW) // 2]; R = {seed}; st = [seed]
    while st:
        c = st.pop(); i = c % W
        for d, ok in ((c - 1, i > 0), (c + 1, i < W - 1), (c - W, True), (c + W, True)):
            if ok and d in S and d not in R:
                R.add(d); st.append(d)
    return R


DCONN = conn_d()
LCONN = [LNE[c] if (VNE[c] or c in DCONN) else (1 - PD) ** 3 for c in range(NC)]
DCL = sorted(DCONN)


def mg2_run(ic, svolta=False, conn=False, surv=False, ncyc=NCYC):
    kx, ky = ic['kx'], ic['ky']
    p0x, v0x, ax, bx, cx = kx; p0y, v0y, ay, by, cy = ky
    w = [1.0, 0.0, 0.0, 0.0, 0.0]; m = [0.0] * 5; e2 = [0.0] * 5; mt = [0.0] * 5     # M, S, R, SR, T
    pt = PT if svolta else 0.0
    TR = [[(0, 1 - PS - PR - pt), (1, PS), (2, PR), (4, pt)], [(0, PG), (1, 1 - PG)], [(2, 1 - PS - PR), (3, PS), (0, PR)], [(2, PG), (3, 1 - PG)], [(4, 1.0)]]
    DEL = [DT, 0.0, -DT, 0.0, 0.0]; out = {}; rmin = [1.0] * 5
    lne = LCONN if conn else LNE; amm = DCL if conn else DCELLS
    sp2 = v0x * v0x + v0y * v0y; ux = v0x / math.sqrt(sp2); uy = v0y / math.sqrt(sp2)
    for k in range(1, ncyc + 1):
        t = k * DT
        nw = [0.0] * 5; nm = [0.0] * 5; ne2 = [0.0] * 5; nmt = [0.0] * 5
        for i in range(5):
            for j, p in TR[i]:
                f = w[i] * p; nw[j] += f; nm[j] += f * m[i]; ne2[j] += f * e2[i]; nmt[j] += f * mt[i]
        for j in range(5):
            if nw[j] > 0:
                mm = nm[j] / nw[j]; ee = ne2[j] / nw[j]; tt = nmt[j] / nw[j]; d = DEL[j]
                m[j] = mm + d; e2[j] = ee + 2 * d * mm + d * d; mt[j] = tt + abs(d)
            w[j] = nw[j]
        g = [0.0] * NC
        for j in range(5):
            if w[j] < 1e-5:
                continue
            if j == 4:
                sa = sp2 * t * t / 4; sl = sp2 * t * t / 6
                sxx = ax + sa * ux * ux + sl * uy * uy; syy = ay + sa * uy * uy + sl * ux * ux; sxy = (sa - sl) * ux * uy
                mx = p0x + v0x * t / 2; my = p0y + v0y * t / 2
            else:
                s = max(0.0, e2[j] - m[j] * m[j]); qn = Q * mt[j] ** 3 / 3
                sxx = ax + 2 * m[j] * bx + e2[j] * cx + s * v0x * v0x + qn
                syy = ay + 2 * m[j] * by + e2[j] * cy + s * v0y * v0y + qn
                sxy = s * v0x * v0y
                mx = p0x + v0x * m[j]; my = p0y + v0y * m[j]
            det = sxx * syy - sxy * sxy
            ixx = syy / det; iyy = sxx / det; ixy = -sxy / det
            kn = w[j] * H * H / (2 * math.pi * math.sqrt(det)); ex = math.exp
            hx = -0.5 * ixx; hy = -0.5 * iyy
            comp = [kn * ex(hx * (x - mx) ** 2 + hy * (y - my) ** 2 - ixy * (x - mx) * (y - my)) for x, y in zip(CX, CY)]
            if surv and j in (0, 2):
                f = sum(comp[c] for c in amm) / w[j]
                rmin[j] = min(rmin[j], f)
                if f > 0 and rmin[j] < f:
                    cc = rmin[j] / f; comp = [a * cc for a in comp]
            g = [a + b for a, b in zip(g, comp)]
        ingr = sum(g); fuori = max(0.0, 1 - ingr)
        g = [a * l for a, l in zip(g, lne)]
        tot = sum(g) + fuori
        out[k] = ([a / tot for a in g], fuori / tot, tot)
    return out


def contro_oracolo(nome, runner):
    ref = inf.carica_oracolo(); R = {k: dict(so=[], mo=[], ar=[]) for k in CK}; fl = []
    for s in range(101, 106):
        ic = make_ic(s); o = runner(ic); prev = None
        for k in range(1, NCYC + 1):
            Rk = hdr(o[k][0], 0.9)
            if prev is not None: fl.append(1 - iou(Rk, prev))
            prev = Rk
            if k in CK:
                o_ = ref[s][k]; to = massa_d(o_); Ro = hdr(o_, 0.9)
                R[k]['so'].append(iou(Rk, Ro)); R[k]['mo'].append(massa_in(Rk, o_, to)); R[k]['ar'].append(len(Rk) * H * H)
    print(nome + ' contro oracolo: ' + ' ; '.join('t=%.1f: IoU %.2f, massa %.3f (min %.3f), area %.2f' % (k * DT, med(R[k]['so']), med(R[k]['mo']), min(R[k]['mo']), med(R[k]['ar'])) for k in CK) + ' ; tremolio %.4f' % mean(fl))


def seqs_di(runner, ics):
    out = []
    for ic in ics:
        o = runner(ic); d = {}
        for k in range(1, NCYC + 1):
            mg = o[k][0]; d[k] = (hdr(mg, 0.5) if k in CK else None, hdr(mg, 0.9), media_d(mg), True, massa_d(mg))
        out.append(d)
    return out


def cmd_mgx():
    contro_oracolo('MG di base', lambda ic: mg2_run(ic))
    contro_oracolo('MG supporto connesso', lambda ic: mg2_run(ic, conn=True))
    contro_oracolo('MG connesso + minimo nel tempo (P17)', lambda ic: mg2_run(ic, conn=True, surv=True))
    ics = [make_ic(s) for s in range(201, 231)]
    inf._valuta('MG + svolta (P13)', seqs_di(lambda ic: mg2_run(ic, svolta=True), ics), ics)
    inf._valuta('MG + svolta + connesso + minimo nel tempo', seqs_di(lambda ic: mg2_run(ic, svolta=True, conn=True, surv=True), ics), ics)
    inf._valuta('MG connesso + minimo nel tempo (senza svolta)', seqs_di(lambda ic: mg2_run(ic, conn=True, surv=True), ics), ics)
    t0 = time.perf_counter(); mg2_run(ics[0], svolta=True, conn=True, surv=True, ncyc=45)
    print('tempo per ciclo MG a 5 componenti con le due correzioni: %.2f ms' % ((time.perf_counter() - t0) / 45 * 1000))


def cmd_ist025():
    inf.NV = 13; inf.DV = 0.25; inf.VL = [-1.5 + 0.25 * i for i in range(13)]
    t0 = time.perf_counter(); inf.ist_run(make_ic(101), ncyc=20)
    print('IST passo 0,25 m/s, %d modi: %.1f ms per ciclo' % (13 * 13 + 1, (time.perf_counter() - t0) / 20 * 1000))
    contro_oracolo('IST passo 0,25', lambda ic: inf.ist_run(ic))


def cmd_pf2():
    ref = inf.carica_oracolo(); KS = (15, 30, 45)
    for N in (1000, 4000):
        acc = {k: dict(ss=[], so=[], mo=[], ar=[]) for k in KS}; fl = []
        for s in range(101, 106):
            ic = make_ic(s); regs = []
            for sd in (11, 12, 13):
                o = pf_run(ic, N, 1000 * sd + s, 'sist'); prev = None; rr = {}
                for k in range(1, NCYC + 1):
                    R = hdr(liscia(liscia(o[k][0])), 0.9)
                    if prev is not None: fl.append(1 - iou(R, prev))
                    prev = R
                    if k in KS: rr[k] = R
                regs.append(rr)
            for k in KS:
                o_ = ref[s][k]; to = massa_d(o_); Ro = hdr(o_, 0.9)
                for i in range(3):
                    R = regs[i][k]; acc[k]['so'].append(iou(R, Ro)); acc[k]['mo'].append(massa_in(R, o_, to)); acc[k]['ar'].append(len(R) * H * H)
                    for j in range(i + 1, 3): acc[k]['ss'].append(iou(R, regs[j][k]))
        print('PF N=%d sistematico, due passate 3x3; a 1/2/3 s: IoU fra semi | IoU oracolo | massa oracolo | area: ' % N +
              ' ; '.join('%.2f | %.2f | %.3f | %.2f' % (mean(acc[k]['ss']), mean(acc[k]['so']), mean(acc[k]['mo']), mean(acc[k]['ar'])) for k in KS) + ' ; tremolio %.3f' % mean(fl))


def cmd_falso2():
    N = 8000; KM = (7, 10, 15); PB = 0.05
    res = {n: {k: [] for k in KM} for n in ('nominale', 'temperata', 'miscela', 'ramo_cieco')}; wbs = {k: [] for k in KM}
    for s in range(301, 311):
        ic = make_ic(s); xt, y0, sp = ic['xt'], ic['y0'], ic['s']; ke = None
        for k in range(1, NCYC + 1):
            x = xt + sp * k * DT
            if x > 0 and vis_ne(x, y0):
                ke = k; break
        kmax = ke + max(KM) - 1; snap = {}

        def mk(name):
            def probe(k, px, py, w, tot):
                d = snap.setdefault(name, {'ev': 1.0, 'm': {}}); d['ev'] *= tot
                for kk in KM:
                    if k == ke + kk - 1:
                        x = xt + sp * k * DT
                        d['m'][kk] = sum(c for a, b, c in zip(px, py, w) if (a - x) ** 2 + (b - y0) ** 2 < 0.25); d['e%d' % kk] = d['ev']
            return probe
        pf_run(ic, N, 40 + s, 'sist', ncyc=kmax, keep=set(), probe=mk('A'))
        pf_run(ic, N, 50 + s, 'sist', pd=0.5, ncyc=kmax, keep=set(), probe=mk('T'))
        pf_run(ic, N, 60 + s, 'sist', ne=False, ncyc=kmax, keep=set(), probe=mk('B'))
        for kk in KM:
            mA = snap['A']['m'][kk]; mB = snap['B']['m'][kk]; wB = PB / (PB + (1 - PB) * snap['A']['e%d' % kk])
            res['nominale'][kk].append(mA); res['temperata'][kk].append(snap['T']['m'][kk]); res['miscela'][kk].append((1 - wB) * mA + wB * mB)
            res['ramo_cieco'][kk].append(mB); wbs[kk].append(wB)
    print('Falso "vuoto" lungo (10 condizioni iniziali, N=%d): massa entro 0,5 m dal vero, mediana [min, max]' % N)
    for n in res:
        print('  %-10s ' % n + ' ; '.join('k=%d: %.5f [%.5f, %.5f]' % (kk, med(res[n][kk]), min(res[n][kk]), max(res[n][kk])) for kk in KM))
    print('  peso del ramo cieco: ' + ' ; '.join('k=%d: %.3f' % (kk, med(wbs[kk])) for kk in KM))


def pezzi_grossi(R, mg):
    R = set(R); tot = sum(mg[c] for c in R); n = 0
    while R:
        st = [R.pop()]; ms = 0.0
        while st:
            c = st.pop(); ms += mg[c]
            for d in (c - 1, c + 1, c - W, c + W):
                if d in R:
                    R.remove(d); st.append(d)
        if ms >= 0.2 * tot: n += 1
    return n


def cmd_pezzi():
    cnt = {n: [0, 0] for n in ('MG', 'MG connesso+minimo', 'PF4000 lisciata', 'PF250 grezza', 'PF1000 grezza')}
    for s in range(101, 106):
        ic = make_ic(s)
        runs = {'MG': mg2_run(ic), 'MG connesso+minimo': mg2_run(ic, conn=True, surv=True)}
        o = pf_run(ic, 4000, 21, 'sist'); runs['PF4000 lisciata'] = {k: (liscia(o[k][0]),) for k in o}
        runs['PF250 grezza'] = pf_run(ic, 250, 22, 'sist'); runs['PF1000 grezza'] = pf_run(ic, 1000, 23, 'sist')
        for n in runs:
            for k in range(1, NCYC + 1):
                mg = runs[n][k][0]; cnt[n][1] += 1; cnt[n][0] += 1 if pezzi_grossi(hdr(mg, 0.9), mg) >= 2 else 0
        if s == 101:
            mg = runs['MG'][45][0]; R = hdr(mg, 0.9); fuori_cuneo = [c for c in R if c not in set(CUNEO)]
            print('MG di base, t=3 s, ic 101: celle della regione fuori dal cuneo (ombra+fascia): %d su %d; di cui non connesse all\'ombra: %d; massa relativa %.3f'
                  % (len(fuori_cuneo), len(R), sum(1 for c in R if c not in DCONN), sum(mg[c] for c in R if c not in DCONN) / sum(mg[c] for c in R)))
    for n in cnt:
        print('cicli con due o piu\' pezzi da almeno il 20%% della massa: %-20s %d su %d' % (n, cnt[n][0], cnt[n][1]))


if __name__ == '__main__':
    c = sys.argv[1]; t0 = time.time()
    print('# inf2.py', c, '— avviato', time.strftime('%Y-%m-%dT%H:%M:%S'))
    {'mgx': cmd_mgx, 'ist025': cmd_ist025, 'pf2': cmd_pf2, 'falso2': cmd_falso2, 'pezzi': cmd_pezzi}[c]()
    print('# durata %.1f s' % (time.time() - t0))
