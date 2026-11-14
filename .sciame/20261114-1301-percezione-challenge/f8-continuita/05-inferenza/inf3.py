#!/usr/bin/env python3
# sciame-inferenza, quarta serie (P19, P20). Uso: python3 inf3.py <ellisse|dieci>
import sys, math, time
import inf
from inf import *


def cmd_ellisse():
    ref = inf.carica_oracolo()
    for k in (15, 30, 45, 75):
        rap = []; lib = []
        for s in range(101, 106):
            o = ref[s][k]; tot = massa_d(o); mx, my = media_d(o)
            sxx = sum(o[c] * (CX[c] - mx) ** 2 for c in DCELLS) / tot; syy = sum(o[c] * (CY[c] - my) ** 2 for c in DCELLS) / tot
            sxy = sum(o[c] * (CX[c] - mx) * (CY[c] - my) for c in DCELLS) / tot; det = sxx * syy - sxy * sxy
            def d2(c):
                dx = CX[c] - mx; dy = CY[c] - my; return (syy * dx * dx - 2 * sxy * dx * dy + sxx * dy * dy) / det
            it = sorted((d2(c), o[c]) for c in DCELLS); acc = 0.0; r2 = 0.0
            for d, v in it:
                acc += v; r2 = d
                if acc >= 0.9 * tot: break
            ins = [c for c in range(NC) if d2(c) <= r2]; clip = [c for c in ins if not VNE[c]]
            rap.append(len(clip) / len(hdr(o, 0.9))); lib.append(1 - len(clip) / len(ins))
        print('t=%.1f s: area ellisse ritagliata / area massima densita\': mediana %.2f [%.2f, %.2f]; quota dell\'ellisse intera su celle viste libere: mediana %.2f' % (k * DT, med(rap), min(rap), max(rap), med(lib)))


def cmd_dieci():
    ics = [make_ic(101 + i % 5) for i in range(10)]; NCY = 45
    t0 = time.perf_counter(); runs = [pf_run(ic, 4000, 7 + i, 'sist', ncyc=NCY) for i, ic in enumerate(ics)]; tf = time.perf_counter() - t0
    t0 = time.perf_counter()
    for o in runs:
        for k in range(1, NCY + 1):
            mg = liscia(liscia(o[k][0])); hdr(mg, 0.5); hdr(mg, 0.9); media_d(mg)
    te = time.perf_counter() - t0
    print('dieci oggetti, N=4000, %d cicli: filtro %.1f ms per ciclo, estrazione (2 lisciature, regioni 50 e 90, media) %.1f ms per ciclo, totale %.1f ms su 66,7' % (NCY, tf / NCY * 1000, te / NCY * 1000, (tf + te) / NCY * 1000))


if __name__ == '__main__':
    print('# inf3.py', sys.argv[1], '— avviato', time.strftime('%Y-%m-%dT%H:%M:%S'))
    {'ellisse': cmd_ellisse, 'dieci': cmd_dieci}[sys.argv[1]]()
