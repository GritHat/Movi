#!/usr/bin/env python3
"""Rifà i conti della parte I (Osservazioni 1-6). Solo la libreria standard."""
import math
f = (848 / 2) / math.tan(math.radians(45)); b = 0.050; sd = 0.08
print("Oss.1  f = %.1f px; sigma_z a 2, 3, 4 m: %s" % (f, ", ".join("%.4f" % (d * d * sd / (f * b)) for d in (2, 3, 4))))
print("Oss.2  2%% a 2 m scalato con d^2: %s m; base 95 mm, 2%% a 4 m: %.2f m" % (", ".join("%.2f" % (0.04 * (d / 2) ** 2) for d in (2, 3, 4)), 0.02 * 4))
print("Oss.3  modello misurato a 2 m: %.5f m" % (0.001063 + 0.0007278 * 2 + 0.003949 * 4))
print("Oss.4  soglie: %.4f  %.4f" % (-2 * math.log(0.01), -2 * math.log(1e-4)))
print("Oss.5  0.95^59 = %.5f (58: %.5f); 0.99^299 = %.5f (298: %.5f)" % (0.95 ** 59, 0.95 ** 58, 0.99 ** 299, 0.99 ** 298))
L = lambda p: math.log(p / (1 - p))
print("Oss.6  logit: colpo %.3f, mancato %.3f, limiti %.3f e %.3f; dopo 2 colpi %.3f, dopo 3 %.3f" % (L(.7), L(.4), L(.1192), L(.971), L(.1192) + 2 * L(.7), L(.1192) + 3 * L(.7)))
print("LD19   360/450 = %.2f gradi" % (360 / 450))
