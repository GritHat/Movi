#!/usr/bin/env python3
"""P-creativo-3bis: finestra di riemersione tarata con quantili empirici su passaggi di prova."""
import math
import random
import sim

random.seed(777)


def one_pass():
    v = random.uniform(0.8, 1.6)
    kf = sim.approach(v)
    t_nom = (sim.SH1 - kf.x) / max(kf.v, 0.1)
    r = random.random()
    if r < 0.3:
        t = (sim.SH1 - sim.SH0) / (v * random.uniform(0.6, 1.0))
    elif r < 0.4:
        t = (sim.SH1 - sim.SH0) / v + random.uniform(0, 3)
    else:
        t = (sim.SH1 - sim.SH0) / v
    return t, t_nom


cal = sorted(t / tn for t, tn in (one_pass() for _ in range(100)))
n = len(cal)
lo = cal[max(int(math.floor(0.05 * (n + 1))) - 1, 0)]
hi = cal[min(int(math.ceil(0.95 * (n + 1))) - 1, n - 1)]
test = [one_pass() for _ in range(300)]
cov = sum(1 for t, tn in test if lo * tn <= t <= hi * tn) / len(test)
w = sorted((hi - lo) * tn for _, tn in test)
print("rapporti di taratura: q05 = %.3f, q95 = %.3f" % (lo, hi))
print("copertura sui 300 di prova = %.3f ; larghezza mediana = %.2f s" % (cov, w[len(w) // 2]))
