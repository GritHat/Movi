"""Diagnosi della prova B: perche' nascono identita' nuove nel caso (i) con pannello di 1 m."""
import math, random
import torneo_parte2 as T
rnd = random.Random(1)
# una persona sola che prosegue: quota di identita' nuove, e d2/raggio alla riemersione
for W in (1.0, 2.0):
    new = lost = gate = 0
    N = 2000
    for _ in range(N):
        p = T.Person(rnd, -1, W, "prosegue")
        ax, ay = T.Ax(0.5), T.Ax(0.5)
        was = False; t = 0.0; res = None; isl = False
        while t < 12:
            ax.predict(); ay.predict()
            if abs(p.x) > W / 2:
                zx, zy = p.x + rnd.gauss(0, T.SIG), 4 + rnd.gauss(0, T.SIG)
                if was:
                    dd = T.d2(ax, ay, zx, zy)
                    lost += isl; gate += (not isl) and dd > T.C99
                    new += isl or dd > T.C99
                    break
                ax.update(zx); ay.update(zy)
            else:
                was = True
                if T.K95 * math.sqrt(ax.a) > 1.5: isl = True
            p.step(t); t += T.DT
    print("W=%.0f una persona sola, prosegue: nuova %.3f (persa per raggio %.3f, fuori porta %.3f); v medio visibile=%.2f" % (W, new / N, lost / N, gate / N, p.v))
