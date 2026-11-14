"""Diagnosi 2 della prova B: registro degli eventi nelle scene (i), W=1, con identita' nuova."""
import math, random
import torneo_parte2 as T
orig_update = T.Ax.update
rnd = random.Random(310)
shown = 0
cnt = {"A_nuova": 0, "B_nuova": 0}
causes = {}
for n in range(600):
    st = rnd.getstate()
    s, k, a = T.scene(rnd, 1.0, ("prosegue", "prosegue"), "persa15")
    if not s and not k:
        # rifaccio la scena con lo stesso stato e registro
        r2 = random.Random(); r2.setstate(st)
        dy = r2.uniform(0.3, 1.0)
        P = [T.Person(r2, -1, 1.0, "prosegue"), T.Person(r2, +1, 1.0, "prosegue", off=r2.uniform(0, 0.8))]
        tA_in = (2.6) / P[0].v; tA_out = 3.6 / P[0].v
        tB_in = (abs(P[1].x) - 0.5) / P[1].v; tB_out = tB_in + 1.0 / P[1].v
        key = "vA=%.2f vB=%.2f hidA=%.2f s hidB=%.2f s" % (P[0].v, P[1].v, 1 / P[0].v, 1 / P[1].v)
        slow = (1 / P[0].v > 1.13) or (1 / P[1].v > 1.13)
        causes["lento (>1,13 s nascosto)" if slow else "altro"] = causes.get("lento (>1,13 s nascosto)" if slow else "altro", 0) + 1
        if shown < 6 and not slow:
            shown += 1
            print(key, "dy=%.2f" % dy, "A esce a %.2f, B entra a %.2f, B esce a %.2f, A entra a %.2f" % (tA_out, tB_in, tB_out, tA_in))
print(causes)
