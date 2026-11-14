"""Diagnosi 3 della prova B: traccia fotogramma per fotogramma della prima scena (i), W=1, con identita' nuova non dovuta a lentezza."""
import math, random
import torneo_parte2 as T
real_assign = T.best_assign
LOG = []
def logged(cost, nt, nd):
    a = real_assign(cost, nt, nd)
    LOG.append((nt, nd, [[None if c is None else round(c, 2) for c in row] for row in cost], a))
    return a
T.best_assign = logged
rnd = random.Random(310)
for n in range(600):
    del LOG[:]
    st = rnd.getstate()
    s, k, a = T.scene(rnd, 1.0, ("prosegue", "prosegue"), "persa15")
    if not s and not k:
        r2 = random.Random(); r2.setstate(st); r2.uniform(0, 1)
        pa = T.Person(r2, -1, 1.0, "prosegue"); pb = T.Person(r2, 1, 1.0, "prosegue")
        if 1 / pa.v > 1.13 or 1 / pb.v > 1.13:
            continue
        for f, (nt, nd, cost, asg) in enumerate(LOG):
            if nd and (None in asg) and f > 0:
                for g in range(max(0, f - 3), min(len(LOG), f + 2)):
                    print("t=%.2f" % (g * T.DT), LOG[g])
                break
        break
