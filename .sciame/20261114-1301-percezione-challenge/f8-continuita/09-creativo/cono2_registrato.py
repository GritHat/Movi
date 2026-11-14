#!/usr/bin/env python3
"""sciame-creativo, f8, versione 2: «scenari» = unione delle regioni per scenario (fronte, scia, ventaglio).
Uso: PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 cono2.py <w> <comportamenti> [N=100] [dw=0.0] [scenari=ABC] [fascia=0.2]
Scena, traiettorie di prova, filtro, libreria: come cono.py (copie dagli script dell'avversario, vedi li').
"""
import math, random, sys, time
import cono
from cono import (DT, SIG, PD, VMAX, GX0, GY0, GNX, GNY, C2, NX2, NY2, PDM, TAUS, CAP, NV, vis, KF, truth, truth_mio, g1,
                  masks, nucleo_frac, mean, med, pct)

PRI = {'A': 0.60, 'B': 0.25, 'C': 0.15}     # convenzione SOLO per il fantasma, non per le regioni
NSC = {'A': 200, 'B': 200, 'C': 400}
INAREA = bytearray(NX2 * NY2)
for _j in range(NY2):
    for _i in range(NX2):
        if vis(GX0 + (_i + .5) * C2, GY0 + (_j + .5) * C2, 0) != 0: INAREA[_j * NX2 + _i] = 1


def make_lib2(n, seed):
    rnd = random.Random(seed); lib = []
    while len(lib) < n:
        tr, kind = g1(rnd, 6.0, 'prosegue')
        x0, y0 = tr[NV]; xa, ya = tr[NV - 3]
        sp = math.hypot(x0 - xa, y0 - ya) / (3 * DT)
        c, s = (x0 - xa) / (sp * 3 * DT), (y0 - ya) / (sp * 3 * DT)
        lib.append((sp, [((p[0] - x0) * c + (p[1] - y0) * s) for p in tr[NV:]], [(-(p[0] - x0) * s + (p[1] - y0) * c) for p in tr[NV:]]))
    return lib


class Scenari:
    def __init__(s, kf, lib, rng, fg, nf2, which='ABC'):
        sa = math.sqrt(kf.a); sc = math.sqrt(kf.c); g = rng.gauss; s.fg = fg; s.nf2 = nf2; s.j = 0
        s.sc = {}; L = len(lib); q = 0
        for name in which:
            n = NSC[name]; us = [(i + .5) / n for i in range(n)]; rng.shuffle(us); mem = []
            for i in range(n):
                sp, dx, dy = lib[q % L]; q += 1
                vx = kf.vx + g(0, sc); vy = kf.vy + g(0, sc); v = math.hypot(vx, vy); f = v / sp; a = f * vx / v; b = f * vy / v
                x0 = kf.x + g(0, sa); y0 = kf.y + g(0, sa)
                xs = [x0 + a * p - b * r for p, r in zip(dx, dy)]; ys = [y0 + b * p + a * r for p, r in zip(dx, dy)]
                if name != 'A':
                    J = 90
                    for j in range(1, 91):       # prima uscita in una cella vista libera oltre la fascia
                        x = xs[j]; y = ys[j]; ii = int((x - GX0) * 10); jj = int((y - GY0) * 10)
                        if 0 <= ii < GNX and 0 <= jj < GNY and x >= GX0 and y >= GY0 and fg[jj * GNX + ii]: J = j; break
                    t = int(us[i] * J)
                    if name == 'B':
                        xs = xs[:t + 1] + [xs[t]] * (90 - t); ys = ys[:t + 1] + [ys[t]] * (90 - t)
                    else:
                        an = rng.choice((-1, 1)) * rng.uniform(math.pi / 4, math.pi / 2); ca = math.cos(an); sn = math.sin(an); xt = xs[t]; yt = ys[t]
                        nx = xs[:t + 1] + [xt + ca * (xs[j] - xt) - sn * (ys[j] - yt) for j in range(t + 1, 91)]
                        ny = ys[:t + 1] + [yt + sn * (xs[j] - xt) + ca * (ys[j] - yt) for j in range(t + 1, 91)]
                        xs, ys = nx, ny
                mem.append([1.0, xs, ys, 0.0, 0.0])
            s.sc[name] = mem
        s.gx, s.gy = kf.x, kf.y

    def step(s):
        s.j += 1; j = min(s.j, 90); fg = s.fg; nf2 = s.nf2; r50 = set(); r90 = set(); al = []; Stot = 0.0; dens = {}; surv = {}
        for name, mem in s.sc.items():
            W = 0.0; cm = {}; pw = PRI[name] / len(mem)
            for m in mem:
                w = m[0]
                if w < 1e-4: continue
                x = m[1][j]; y = m[2][j]; ii = int((x - GX0) * 10); jj = int((y - GY0) * 10)
                if 0 <= ii < GNX and 0 <= jj < GNY and x >= GX0 and y >= GY0 and fg[jj * GNX + ii]:
                    w *= (1 - PDM); m[0] = w
                    if w < 1e-4: continue
                m[3] = x; m[4] = y; W += w; al.append((x, y, w * pw))
                cj = int((y - GY0) * 4); ci = int((x - GX0) * 4); c = (cj << 8) | ci
                cm[c] = cm.get(c, 0.0) + 0.5 * w
                for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    nj = cj + dj; ni = ci + di
                    if 0 <= nj < NY2 and 0 <= ni < NX2 and not nf2[nj * NX2 + ni]: continue     # mai su una cella libera
                    c2 = (nj << 8) | ni; cm[c2] = cm.get(c2, 0.0) + 0.125 * w
            surv[name] = W / len(mem); Stot += W * pw
            if W <= 0: continue
            tot = sum(cm.values()); items = sorted(cm.items(), key=lambda kv: -kv[1]); cum = 0.0; d50 = False
            for c, v in items:
                dens[c] = dens.get(c, 0.0) + pw * v * W / tot
                if cum < 0.9 * tot:
                    r90.add(c)
                    if cum < 0.5 * tot: r50.add(c)
                cum += v
        out = {'r50': r50, 'r90': r90, 'surv': surv, 'S': Stot, 'dens': dens}
        def area(r):
            n = 0; fu = False
            for c in r:
                cj, ci = c >> 8, c & 255
                if 0 <= cj < NY2 and 0 <= ci < NX2 and INAREA[cj * NX2 + ci]: n += 1
                else: fu = True
            return n * C2 * C2, fu
        out['a50'], _ = area(r50); out['a90'], out['fuori'] = area(r90)
        if Stot >= 0.02 and al:
            h = Stot / 2
            def wmed(idx):
                acc = 0.0
                for m in sorted(al, key=lambda m: m[idx]):
                    acc += m[2]
                    if acc >= h: return m[idx]
                return al[-1][idx]
            mx = wmed(0); my = wmed(1); best = min(al, key=lambda m: (m[0] - mx) ** 2 + (m[1] - my) ** 2 + (1e6 if m[2] < 1e-6 else 0))
            tx, ty = best[0], best[1]
        else:
            tx, ty = s.gx, s.gy
        ex = 0.5 * (tx - s.gx); ey = 0.5 * (ty - s.gy); e = math.hypot(ex, ey); mxs = VMAX * DT
        if e > mxs: ex *= mxs / e; ey *= mxs / e
        s.gx += ex; s.gy += ey; out['ghost'] = (s.gx, s.gy)
        return out


def cell(x, y): return (int((y - GY0) * 4) << 8) | int((x - GX0) * 4)


def run_trial(beh, w, dw, rng, lib, which, st, tms, tin):
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
            t0 = time.perf_counter(); co = Scenari(kf, lib, rng, fg, nf2, which); tin.append(time.perf_counter() - t0)
        if det:
            if o is not None:
                g = o['ghost']; near = 1e9
                for c in o['r90']:
                    d = math.hypot(GX0 + ((c & 255) + .5) * C2 - z[0], GY0 + ((c >> 8) + .5) * C2 - z[1])
                    if d < near: near = d
                st['re'].append((beh, math.hypot(g[0] - z[0], g[1] - z[1]), math.hypot(kf.x - z[0], kf.y - z[1]), math.hypot(fro[0] - z[0], fro[1] - z[1]),
                                 near <= 0.45, last_hidden, (k - k0) * DT))
            break
        t0 = time.perf_counter(); pg = (co.gx, co.gy); o = co.step(); tms.append(time.perf_counter() - t0)
        g = o['ghost']; stp = (g[0] - pg[0]) * hdg[0] + (g[1] - pg[1]) * hdg[1]
        st['step'].append((beh, math.hypot(g[0] - pg[0], g[1] - pg[1]), stp))
        if nuc_on and nucleo_frac(kf, w) >= 0.5: nuc_on = False
        if vt == 1: continue
        ct = cell(x, y); c90 = ct in o['r90']; c50 = ct in o['r50']; last_hidden = (c50, c90)
        free_mass = 0.0
        st['cyc'].append((beh, o['a90'] < 0.5 * ASH, nuc_on, o['fuori'], o['a90'] / ASH))
        tau = TAUS.get(k - k0)
        if tau is not None:
            eg = math.hypot(g[0] - x, g[1] - y); ecv = math.hypot(kf.x - x, kf.y - y); efr = math.hypot(fro[0] - x, fro[1] - y)
            d = o['dens'].get(ct, 0.0) / max(o['S'], 1e-12); nll_e = -math.log(max(d, 1e-6) / (C2 * C2))
            nll_k = math.log(2 * math.pi * kf.a) + ecv * ecv / (2 * kf.a)
            st['ev'].append((beh, tau, c50, c90, o['a50'] / ASH, o['a90'] / ASH, o['fuori'], eg, ecv, efr, nuc_on, nll_e, nll_k,
                             o['surv'].get('A', 0), o['surv'].get('B', 0), o['surv'].get('C', 0)))
        if k - k0 >= CAP: break


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main():
    w = float(sys.argv[1]); behs = sys.argv[2].split(','); N = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    dw = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0; which = sys.argv[5] if len(sys.argv) > 5 else 'ABC'
    if len(sys.argv) > 6: cono.GUARD = float(sys.argv[6])
    lib = make_lib2(200, 778)
    _, _, ASH = masks(w, w + dw)
    print('# cono2.py  w=%.1f  N=%d  dw=%+.2f  scenari=%s %s  fascia=%.2f  ombra in portata=%.2f m2' % (w, N, dw, which, {k: NSC[k] for k in which}, cono.GUARD, ASH))
    st = {'ev': [], 'cyc': [], 'step': [], 're': []}; tms = []; tin = []
    seeds = {'prosegue': 1, 'sosta': 2, 'torna': 3, 'lontano': 4, 'rallenta': 5, 'svolta': 6}
    for beh in behs:
        rng = random.Random(20261114 + 1000 * seeds[beh] + int(w * 10))
        for t in range(N): run_trial(beh, w, dw, rng, lib, which, st, tms, tin)
    print('\n## per comportamento e tempo senza osservazione (solo cicli a soggetto non visibile); [..] = intervallo di Wilson al 95 % della copertura al 90 %')
    print('beh       tau   n | c50%  c90%  [Wilson]  | a50%  a90% fuori% | err mediano m: fant. vel.cost fermo | nucleo mostrato% | NLL scen. NLL kalman | sopravv. A    B    C')
    for beh in behs:
        for tau in sorted(TAUS.values()):
            e = [r for r in st['ev'] if r[0] == beh and r[1] == tau]
            if not e: continue
            lo, hi = wilson(sum(r[3] for r in e), len(e))
            print('%-9s %3.1f %3d | %4.0f  %4.0f  [%3.0f-%3.0f] | %4.0f  %4.0f  %4.0f  | %19.2f %8.2f %5.2f | %15.0f | %9.2f %10.2f | %12.2f %4.2f %4.2f' % (
                beh, tau, len(e), 100 * mean([r[2] for r in e]), 100 * mean([r[3] for r in e]), 100 * lo, 100 * hi, 100 * mean([r[4] for r in e]), 100 * mean([r[5] for r in e]),
                100 * mean([r[6] for r in e]), med([r[7] for r in e]), med([r[8] for r in e]), med([r[9] for r in e]), 100 * mean([r[10] for r in e]),
                mean([r[11] for r in e]), mean([r[12] for r in e]), mean([r[13] for r in e]), mean([r[14] for r in e]), mean([r[15] for r in e])))
    print('\n## continuita: cicli nascosti; stima emessa (per costruzione 100); informativa (a90 < meta ombra); r90 tocca fuori area; a90 medio e massimo (% ombra); nucleo mostrato')
    for beh in behs:
        c = [r for r in st['cyc'] if r[0] == beh]
        print('%-9s %6d | 100 | %5.1f | %5.1f | %5.1f %5.1f | %5.1f' % (beh, len(c), 100 * mean([r[1] for r in c]), 100 * mean([r[3] for r in c]), 100 * mean([r[4] for r in c]),
                                                             100 * max(r[4] for r in c), 100 * mean([r[2] for r in c])))
    print('\n## regolarita del fantasma: cicli | passo max m | passi indietro > 2 cm % | passo indietro max m')
    for beh in behs:
        s = [r for r in st['step'] if r[0] == beh]
        print('%-9s %6d | %.3f | %5.1f | %.3f' % (beh, len(s), max(r[1] for r in s), 100 * mean([r[2] < -0.02 for r in s]), -min(r[2] for r in s)))
    print('\n## ricomparsa: n | salto fantasma med p90 | vel.cost med p90 | fermo med p90 | prima misura entro 0,45 m da r90 % | ultimo ciclo nascosto c50% c90% | buio medio s')
    for beh in behs:
        r = [x for x in st['re'] if x[0] == beh]
        if not r: print('%-9s   0' % beh); continue
        lh = [x[5] for x in r if x[5] is not None]
        print('%-9s %3d | %.2f %.2f | %.2f %.2f | %.2f %.2f | %5.1f | %4.0f %4.0f | %.2f' % (beh, len(r), med([x[1] for x in r]), pct([x[1] for x in r], .9), med([x[2] for x in r]), pct([x[2] for x in r], .9),
              med([x[3] for x in r]), pct([x[3] for x in r], .9), 100 * mean([x[4] for x in r]), 100 * mean([a for a, b in lh]), 100 * mean([b for a, b in lh]), mean([x[6] for x in r])))
    tm = sorted(tms); ti = sorted(tin)
    print('\n## costo (Python puro): passo per ciclo: n %d  mediana %.2f ms  p95 %.2f ms  max %.2f ms | creazione all ingresso: mediana %.1f ms  max %.1f ms' % (
        len(tm), 1000 * tm[len(tm) // 2], 1000 * tm[int(.95 * len(tm))], 1000 * tm[-1], 1000 * ti[len(ti) // 2], 1000 * ti[-1]))


if __name__ == '__main__':
    main()
