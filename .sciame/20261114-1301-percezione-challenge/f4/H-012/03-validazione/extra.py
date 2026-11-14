#!/usr/bin/env python3
"""Controlli aggiunti DOPO aver visto i risultati (notati dopo): non fanno parte del progetto congelato."""
import math, random, sys
import sim_h012 as S

print("# (1) causa del 15 % in D, pannello 0,5 m, prosegue: misura = centro della parte visibile (progetto) contro misura = centro vero del corpo")
orig = S.observe
def unbiased(geo, x, y, rho, rnd, curve):
    wv, z = orig(geo, x, y, rho, rnd, curve)
    if z is None:
        return wv, z
    r = math.hypot(x, y); sr = S.sig_r(r, curve); st = S.sig_t(r)
    return wv, (x + rnd.gauss(0, st), y + rnd.gauss(0, sr), st * st, sr * sr, sr)
for (name, yp, w, yped, rmax) in (('D w=0.5', 1.5, 0.5, 2.5, 3.0), ('D w=1.0', 1.5, 1.0, 2.5, 3.0), ('T w=1.0', 2.0, 1.0, 4.0, 6.0)):
    for curve in ('nom', 'lim'):
        geo = S.Geo(yp, w, yped, rmax, 0.0)
        S.observe = orig; A = S.agg_cell(geo, 'prosegue', curve, 0.20, 400, S.SEED + 990001)
        S.observe = unbiased; B = S.agg_cell(geo, 'prosegue', curve, 0.20, 400, S.SEED + 990001)
        S.observe = orig
        print(" %s curva %s: nel cerchio al 95%% alla riemersione: progetto %.1f%% (contenuta resp. %.1f%%) ; centro vero %.1f%% (contenuta resp. %.1f%%) ; N=400"
              % (name, curve, S.pc(A['in95'], A['reem']), S.pc(A['c40'], A['reem']), S.pc(B['in95'], B['reem']), S.pc(B['c40'], B['reem'])))

print("# (2) oggetto FERMO appena visto: quota con un'etichetta «mobile» entro 1 s + 1 fotogramma dalla prima misura (falso), N=4000")
for curve in ('nom', 'lim', 'tor'):
    for z0 in (2.0, 3.0, 4.0):
        rnd = random.Random(S.SEED + 990100 + int(z0))
        res = [S.ped_pass(rnd, curve, z0, True, 0.0, 1.0, 0.0) for _ in range(4000)]
        print(" %s z=%.0f m: spostamento %.2f%% ; chi2 %.2f%% ; v1a %.2f%%" % (curve, z0, S.frac([r[0] for r in res], 16), S.frac([r[1] for r in res], 16), S.frac([r[2] for r in res], 16)))
