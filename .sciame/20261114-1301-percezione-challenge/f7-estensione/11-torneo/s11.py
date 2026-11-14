# s11.py — S11 (macchina a stati per il monitoraggio di attivita'): l'evento SOSTA_IN_OMBRA nasce dal peso mu2.
# Modello minimo di S3+S4 come scritti nella preproposta: mu = (0,8 ; 0,2) all'ingresso; a ogni ciclo
# mu1 <- mu1 * f_ombra(t) (quota della gaussiana di H1 ancora dentro l'ombra), mu2 <- mu2 * 1, poi si normalizza.
# Pannello largo 1 m; il soggetto entra a x = 0 e l'ombra finisce a x = w.   Uso: python3 -I s11.py
import math, random
rng = random.Random(14112026)
DT, Q, S0, THETA, W = 1 / 15, 0.2, 0.05, 0.8, 1.0
def phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
def corsa(caso):
    v = rng.uniform(0.5, 1.4); vhat = v + rng.gauss(0, 0.15)
    rall = rng.uniform(0.6, 1.0) if caso == "c" else 1.0
    mu1, mu2, t, x = 0.8, 0.2, 0.0, 0.0
    while t < 5.0:
        t += DT
        if caso == "a": x = min(x + v * DT, W / 2)             # si ferma a meta' pannello
        elif caso == "b": x = min(x + v * DT, W / 2)           # a meta' pannello svolta e si allontana in profondita' dentro l'ombra (aperta): non ricompare
        else: x += v * rall * DT                               # transito, rallentando
        if caso == "c" and x >= W: return ("ricomparso", t)
        sig = math.sqrt(S0 ** 2 + Q * t ** 3 / 3)
        f = phi((W - vhat * t) / sig)                           # massa di H1 ancora dentro l'ombra
        a, b = mu1 * max(f, 1e-12), mu2
        mu1, mu2 = a / (a + b), b / (a + b)
        if mu2 > THETA: return ("SOSTA_IN_OMBRA", t)
    return ("niente", t)
for caso, nome in (("a", "si ferma dietro il pannello"), ("b", "se ne va in profondita' dentro l'ombra aperta, senza fermarsi"), ("c", "transito normale, rallenta dietro il pannello")):
    r = [corsa(caso) for _ in range(200)]
    n = sum(1 for e, _ in r if e == "SOSTA_IN_OMBRA"); ts = sorted(t for e, t in r if e == "SOSTA_IN_OMBRA")
    print("caso %s (%s): SOSTA_IN_OMBRA emessa in %d corse su 200%s" % (caso, nome, n, ("; tempo mediano %.2f s, massimo %.2f s" % (ts[len(ts) // 2], ts[-1])) if ts else ""))
