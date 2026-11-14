#!/usr/bin/env python3
"""avv-17 (K-210): S2, compensazione della latenza. Il segno «visto» portato a t_now = t_cap + 155 ms contro il segno non compensato.
Modello 1D lungo il cammino (bordo dell'ombra in x = 0, il soggetto arriva da x < 0), filtro a velocita quasi costante q = 0,2, rumore 5 cm, 15 Hz, Pd 0,9.
Uso: timeout 120 python3 s2.py > ris/a17_s2.txt"""
import random, math
DT = 1 / 15; Q = 0.2; R = 0.05 ** 2; LAT = 0.155; PD = 0.9
def med(v): v = sorted(v); return v[len(v) // 2] if v else float('nan')
def p90(v): v = sorted(v); return v[int(0.9 * len(v))] if v else float('nan')
def prova(seed, v, stop_at=None, c6=0.22):
    rnd = random.Random(seed); t = 0.0; x0 = -v * 2.5 - rnd.uniform(0, v * DT)   # fase casuale rispetto al bordo
    def pos(tt):                                   # verita continua: velocita costante, oppure arresto in 0,13 s a partire da x = stop_at
        if stop_at is None: return x0 + v * tt
        ts = (stop_at - x0) / v
        if tt <= ts: return x0 + v * tt
        d = min(tt - ts, 0.13); return stop_at + v * d - v * d * d / (2 * 0.13)
    kf = None; zp = None; out = {'err_u': [], 'err_c': [], 'post_u': [], 'post_c': [], 'in_shadow': 0, 'in_band': 0, 'over': 0.0}
    k = 0; ts = None if stop_at is None else (stop_at - x0) / v
    while True:
        tt = k * DT; x = pos(tt)
        if x > -c6 or tt > 6: break                 # da qui il gruppo e tagliato (C6) o nascosto: niente piu «visto»
        if rnd.random() < PD:
            z = x + rnd.gauss(0, 0.05)
            if kf is None:
                if zp is None: zp = (z, k)
                else:
                    d = (k - zp[1]) * DT; kf = [z, (z - zp[0]) / d, R, R / d, 2 * R / d / d]
            else:
                X, V, a, b, c = kf; X += V * DT; a, b, c = a + 2 * b * DT + c * DT * DT + Q * DT ** 3 / 3, b + c * DT + Q * DT * DT / 2, c + Q * DT
                s = a + R; k1 = a / s; k2 = b / s; r = z - X; kf = [X + k1 * r, V + k2 * r, (1 - k1) * a, (1 - k1) * b, c - k2 * b]
                if k > 20:
                    xu = kf[0]; xc = kf[0] + kf[1] * LAT; xt = pos(tt + LAT)   # il segno pieno esce solo nei cicli con una misura (invariante 3)
                    eu = abs(xu - xt); ec = abs(xc - xt)
                    if ts is not None and tt >= ts:
                        if tt < ts + 3 * DT + 1e-9: out['post_u'].append(eu); out['post_c'].append(ec)
                        out['over'] = max(out['over'], xc - xt)
                    elif ts is None or tt < ts - 0.3: out['err_u'].append(eu); out['err_c'].append(ec)
                    if xc > 0: out['in_shadow'] = 1
                    if xc > -0.20: out['in_band'] = 1
        elif kf is not None:
            X, V, a, b, c = kf; kf = [X + V * DT, V, a + 2 * b * DT + c * DT * DT + Q * DT ** 3 / 3, b + c * DT + Q * DT * DT / 2, c + Q * DT]
        k += 1
    return out
print('# s2.py: latenza %.0f ms; errore = |segno - vero all istante dell uscita|; N = 400 per riga, semi 9000-9399' % (LAT * 1000))
for v in (0.5, 1.2, 1.8):
    eu = []; ec = []
    for s in range(9000, 9400): o = prova(s, v); eu += o['err_u']; ec += o['err_c']
    print('(a) moto regolare v=%.1f: non compensato mediana %.3f p90 %.3f | compensato mediana %.3f p90 %.3f' % (v, med(eu), p90(eu), med(ec), p90(ec)))
for v in (0.5, 1.2, 1.8):
    pu = []; pc = []; ov = []; worse = 0; n = 0
    for s in range(9000, 9400):
        o = prova(s, v, stop_at=-1.0); pu += o['post_u']; pc += o['post_c']; ov.append(o['over'])
    print('(b) sosta improvvisa (0,13 s) v=%.1f, 3 cicli dopo l inizio della frenata: non compensato mediana %.3f p90 %.3f | compensato mediana %.3f p90 %.3f | sorpasso massimo del compensato oltre il vero: mediana %.3f p90 %.3f' % (v, med(pu), p90(pu), med(pc), p90(pc), med(ov), p90(ov)))
for c6 in (0.0, 0.22):
    for v in (0.5, 1.2, 1.8):
        ns = nb = 0
        for s in range(9000, 9400): o = prova(s, v, c6=c6); ns += o['in_shadow']; nb += o['in_band']
        print('(c) ingresso nell ombra, C6=%.2f v=%.1f: passaggi con il segno pieno compensato dentro l ombra %d/400; dentro la fascia di 0,20 m %d/400' % (c6, v, ns, nb))
