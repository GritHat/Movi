# Controlli dell'arbitro (f2/03): solo aritmetica, nessun modello degli autori.
from math import comb, sqrt, radians, tan, degrees, atan
# 1) copertura di tre sensori
for fov in (45, 60, 120): print("3 x", fov, "=", 3*fov, "gradi")
# 2) persona 0,5 m x 1,7 m a 4 m: zone di un ToF 8x8 da 45 gradi e pixel di una 640x480 da 87x58 gradi
d, w, h = 4.0, 0.5, 1.7
aw, ah = degrees(2*atan(w/2/d)), degrees(2*atan(h/2/d))
zw, zh = aw/(45/8), ah/(45/8)
print("ToF 8x8: zone in larghezza %.2f, in altezza %.2f, in area %.1f" % (zw, zh, zw*zh))
pw, ph = aw*640/87, ah*480/58
print("640x480: pixel in larghezza %.0f, in altezza %.0f, rettangolo %.0f" % (pw, ph, pw*ph))
# 3) sola predizione a velocita' quasi costante: sigma_pos^2 = s0^2 + sv^2 t^2 + q t^3/3
def t_raggio(q, r, k, s0=0.05, sv=0.2):
    t = 0.0
    while k*sqrt(s0**2 + sv**2*t*t + q*t**3/3) < r: t += 0.01
    return t
for q in (0.1, 0.2, 0.25, 0.5, 1.0):
    print("q=%.2f: 2sigma>1 m a %.2f s; raggio 95%% (2,448 sigma)>1 m a %.2f s; >1,5 m a %.2f s" %
          (q, t_raggio(q,1.0,2.0), t_raggio(q,1.0,2.448), t_raggio(q,1.5,2.448)))
# 4) criterio 26/30
for p in (0.92, 0.857, 0.75, 0.42):
    print("p=%.3f: P(X>=26 su 30) = %.3f" % (p, sum(comb(30,k)*p**k*(1-p)**(30-k) for k in range(26,31))))
# 5) transito dietro il pannello
for L in (1.0, 2.0):
    for v in (0.6, 0.8, 1.0, 1.3): print("pannello %.0f m, %.1f m/s: %.2f s" % (L, v, L/v), end="; ")
    print()
# 6) disco raggiungibile v_max*tau contro cerchio al 95% (q=0,2)
for t in (0.5, 1.0, 1.5): print("tau=%.1f s: raggio disco v_max=2,5 -> %.2f m; raggio 95%% Kalman q=0,2 -> %.2f m" % (t, 2.5*t, 2.448*sqrt(0.05**2+0.04*t*t+0.2*t**3/3)))
