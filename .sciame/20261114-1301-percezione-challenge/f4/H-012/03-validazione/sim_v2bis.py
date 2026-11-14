#!/usr/bin/env python3
"""Chiusura dell'anomalia Pd 0,9 / -20 cm (f4, H-012). Non modifica sim_v2.py: lo importa e ne ripete pass_v2 con quattro interruttori."""
import sys, math, random
import sim_v2 as S
from sim_v2 import *

def pass_bis(rnd, geo, beh, curve, band, det, c6, pd=1.0, rho=0.20, cutentry=False, v4=False, entryd=None, rebirth=False, steal=None):
    P = traj(rnd, geo, beh)
    kx = ky = None; first = None
    pending = False; alert = False; closed = False; lost = False; newtrack = False
    unconf = 0; lastdet = None; lastcut = False; kpend = -1; klost = -1; kuse = -1
    R = dict(fail=0, closed=False, entered=False, reem=False, reatt=False, shown=False, durprev=None,
             tperso=None, in95=None, tdark=None, track=False, v4n=0, alert_end=False, stolen=False, fail_after=0)
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
                        pending = False; alert = False; closed = False; unconf = 0
                    else:
                        newtrack = True                    # «identita' ambigua»: lo strato 1 resta
                if closed and rebirth and not pending and not newtrack:
                    closed = False; unconf = 0
                    kx.p = z[0]; kx.v = 0.0; kx.a = z[2]; kx.b = 0.0; kx.c = 1.0
                    ky.p = z[1]; ky.v = 0.0; ky.a = z[3]; ky.b = 0.0; ky.c = 1.0
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
                    if geo.d_est(lastdet[0], lastdet[1]) <= (band if entryd is None else entryd) or (cutentry and lastcut):
                        pending = True; alert = True; kpend = k; lost = False; R['entered'] = True
                    else:
                        unconf += 1
                        if unconf > 3:
                            closed = True; R['closed'] = True
                            if v4 and geo.d_est(lastdet[0], lastdet[1]) <= 1.0:
                                pending = True; alert = True; kpend = k; lost = False; R['v4n'] += 1
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
        if steal is not None and pending and not R['stolen'] and (k - kpend) * DT >= steal:
            pending = False; alert = False; closed = True; R['stolen'] = True
        R['alert_end'] = alert and got
        if not got:
            xc, yc, ing = geo.cell(x, y)
            if ing and not geo.in_est(xc, yc) and not (cvis and wv >= DEG1):
                if not (alert and geo.d_est(xc, yc) <= band):
                    R['fail'] += 1
                    if R['stolen']:
                        R['fail_after'] += 1
    return R


def run(lab, N, **kw):
    ci = 0; tot = {}; rows = []
    for gname in ('DC', 'T1', 'T2'):
        yp, w, yped, rmax = S.GEOS[gname]
        for (band, e, l2) in ((0.40, -0.2, 'p'), (0.40, 0.0, 'p'), (0.40, 0.2, 'p'), (0.0, -0.2, 'b'), (0.20, -0.2, 'b'), (0.40, -0.4, 'b')):
            geo = S.Geo(yp, w, yped, rmax, e)
            for beh in S.BEH:
                ci += 1; rnd = random.Random(S.SEED + 2000000 + ci)       # stessi semi di v2_R8_pd09.txt
                if l2 != 'p':
                    for _ in range(N):
                        S.pass_v2(rnd, geo, beh, 'nom', band, 'wmin', True, 0.9)   # consuma il seme come nel lancio originale
                    continue
                f = v4n = ae = re = ra = 0
                for _ in range(N):
                    R = pass_bis(rnd, geo, beh, 'nom', band, 'wmin', True, 0.9, **kw)
                    f += R['fail'] > 0; v4n += R['v4n']; ae += R['alert_end']
                    if R['reem']:
                        re += 1; ra += R['reatt']
                t = tot.setdefault(e, [0, 0, 0, 0, 0, 0]); t[0] += f; t[1] += N; t[2] += v4n; t[3] += ae
                if beh != 'lontano':
                    t[4] += ra; t[5] += re
    print(" %-34s " % lab + " | ".join("errore %+.1f: falliti %d/%d ; strati da v4 %d ; avviso ancora acceso a fine passaggio con soggetto visibile %d ; riagganciate %.2f%%" % (e, t[0], t[1], t[2], t[3], 100.0 * t[4] / t[5]) for e, t in sorted(tot.items())))
    sys.stdout.flush()


def davanti(lab, N, **kw):
    yp, w, yped, rmax = S.GEOS['DC']; y2 = yp - 0.5; out = []
    for e in (-0.2, 0.0, 0.2):
        geo = S.Geo(yp, w, y2, rmax, e * y2 / yped); rnd = random.Random(S.SEED + 8000000 + int(e * 10)); n = ae = 0
        for _ in range(N):
            R = pass_bis(rnd, geo, 'prosegue', 'nom', 0.40, 'wmin', True, 0.9, **kw)
            n += R['v4n'] + (R['entered'] and not R['v4n']); ae += R['alert_end']
        out.append("errore %+.1f: strati nati %.1f, rimasti accesi a fine passaggio %.1f" % (e, 100.0 * n / N, 100.0 * ae / N))
    print(" %-34s passaggio DAVANTI al pannello (a 0,5 m), per 100 passaggi: " % lab + " | ".join(out))


def furto(N):
    print("# limite P2b: a 1,0 s dall'ingresso un secondo soggetto viene riagganciato e lo strato 1 si rilascia con il primo ancora nascosto (Pd=1). Passaggi con il primo soggetto, senza misura, in una cella «libero» DOPO il rilascio; N=%d" % N)
    ci = 0
    for gname in ('DC', 'T1'):
        yp, w, yped, rmax = S.GEOS[gname]
        for e in (-0.2, 0.0, 0.2):
            geo = S.Geo(yp, w, yped, rmax, e); out = []
            for beh in ('sosta', 'torna', 'lontano'):
                ci += 1; rnd = random.Random(S.SEED + 9000000 + ci); f = st = 0
                for _ in range(N):
                    R = pass_bis(rnd, geo, beh, 'nom', 0.40, 'wmin', True, 1.0, steal=1.0)
                    st += R['stolen']; f += R['fail_after'] > 0
                out.append("%s %d/%d" % (beh, f, st))
            print(" %s errore %+.1f: %s" % (gname, e, " ; ".join(out)))


if __name__ == '__main__':
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    if sys.argv[1] == 'R8':
        print("# Pd 0,9, 36 celle principali, N=%d per cella, stessi semi di v2_R8_pd09.txt" % N)
        part = sys.argv[3] if len(sys.argv) > 3 else 'a'
        if part == 'a':
            run('PRIMA (regola della versione 2)', N)
            run('prima + rinascita', N, rebirth=True)
            run('validazione-4', N, v4=True)
        else:
            run('validazione-4 + rinascita', N, v4=True, rebirth=True)
            run('ingresso subito entro 1 m', N, entryd=1.0)
            run('ingresso subito entro 1 m + rinascita', N, entryd=1.0, rebirth=True)
    elif sys.argv[1] == 'DAVANTI':
        print("# costo: strati 1 a vuoto, Pd 0,9, N=%d" % N)
        davanti('PRIMA', N); davanti('validazione-4 + rinascita', N, v4=True, rebirth=True); davanti('ingresso subito entro 1 m + rinascita', N, entryd=1.0, rebirth=True)
    elif sys.argv[1] == 'FURTO':
        furto(N)
