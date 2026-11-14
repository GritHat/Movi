"""Diagnosi 4 della prova B2: le identita' nuove residue nel caso (i) vengono dall'interazione fra le due corsie?
Stesso caso con le corsie a 5 m (nessuna misura dell'altro puo' cadere nella porta) e con porta al 99,99% (18,42)."""
import random
import torneo_parte2 as T
import torneo_B2A2_parte2 as B


class Far(random.Random):
    def uniform(self, a, b):
        if (a, b) == (0.3, 1.0):
            return 5.0
        return super().uniform(a, b)


def run(cls, label, variant, W=1.0, N=2000):
    rnd = cls(4010)
    sw = kp = 0
    for _ in range(N):
        s, k, a = B.scene2(rnd, W, ("prosegue", "prosegue"), variant)
        sw += s
        kp += k
    print("%-46s %s W=%.0f: tenuta %.3f scambio %.3f nuova %.3f" % (label, variant, W, kp / N, sw / N, 1 - (kp + sw) / N))


for variant in ("persa15", "tetto3s"):
    run(random.Random, "corsie a 0,3-1 m, porta 9,21", variant)
    run(Far, "corsie a 5 m, porta 9,21", variant)
old = (T.C99, B.C99)
T.C99 = B.C99 = 18.42
for variant in ("persa15", "tetto3s"):
    run(random.Random, "corsie a 0,3-1 m, porta 18,42 (99,99%)", variant)
