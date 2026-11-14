#!/usr/bin/env python3
"""S2: compensazione della latenza. Una dimensione, lungo il moto.

Vero: cammino a v costante per 4 s, poi arresto (istantaneo, oppure a 3 m/s2).
Misure a 15 Hz, sigma 3,4 cm (curva nominale a 3 m, SOLUZIONE_V2 B1). Filtro a velocita' quasi costante, q = 0,2 m2/s3.
La posizione mostrata al ciclo k compare all'istante t_k + L (L = latenza vera, 155 ms): l'errore e' rispetto al vero in t_k + L.
  - non compensata: x_stimato(t_k)
  - compensata con L_stima: x + v * L_stima   (copia d'uscita: il filtro interno resta a t_k)

Rifare:  timeout 120 python3 sim_latenza.py > risultati_latenza.txt
"""
import math
import random

HZ = 15.0
DT = 1 / HZ
Q = 0.2
SIG = 0.034
L_VERA = 0.155
T_STOP = 4.0
T_FINE = 6.5


def vero(t, v, decel):
    if t <= T_STOP:
        return v * t
    if decel is None:
        return v * T_STOP
    td = v / decel
    tau = min(t - T_STOP, td)
    return v * T_STOP + v * tau - 0.5 * decel * tau * tau


def passaggio(seed, v, decel, l_stime):
    rnd = random.Random(seed)
    x, vx = 0.0, v
    p11, p12, p22 = SIG ** 2, 0.0, 1.0
    q11, q12, q22 = Q * DT ** 3 / 3, Q * DT ** 2 / 2, Q * DT
    r = SIG ** 2
    out = []   # (t_k, errori per ogni stima di L, sigma dichiarata della posizione portata avanti)
    k = 0
    while k * DT <= T_FINE:
        t = k * DT
        if k > 0:
            x = x + vx * DT
            p11, p12, p22 = p11 + 2 * DT * p12 + DT * DT * p22 + q11, p12 + DT * p22 + q12, p22 + q22
        z = vero(t, v, decel) + rnd.gauss(0, SIG)
        s = p11 + r
        k1, k2 = p11 / s, p12 / s
        inn = z - x
        x, vx = x + k1 * inn, vx + k2 * inn
        p11, p12, p22 = (1 - k1) * p11, (1 - k1) * p12, p22 - k2 * p12
        tv = vero(t + L_VERA, v, decel)
        errs = [x + vx * le - tv for le in l_stime]
        sig_out = math.sqrt(p11 + 2 * L_VERA * p12 + L_VERA ** 2 * p22 + Q * L_VERA ** 3 / 3)
        out.append((t, errs, sig_out, math.sqrt(p22)))
        k += 1
    return out


def prova(v, decel, semi=500):
    l_stime = [0.0, 0.155, 0.125, 0.185, 0.022]
    nomi = ["non compensata", "compensata L esatta (155)", "L sottostimata (125)", "L sovrastimata (185)", "marca d'arrivo (22)"]
    n = len(l_stime)
    sq = [0.0] * n; me = [0.0] * n; cnt = 0
    picchi = [[] for _ in range(n)]; durate = [[] for _ in range(n)]
    sig = sv = 0.0
    for s in range(semi):
        o = passaggio(5000 + s, v, decel, l_stime)
        pk = [0.0] * n; du = [0] * n
        for t, errs, so, svv in o:
            if 2.0 <= t <= T_STOP - L_VERA - DT:        # moto uniforme, filtro a regime
                for i in range(n):
                    sq[i] += errs[i] ** 2; me[i] += errs[i]
                cnt += 1; sig = so; sv = svv
            if t > T_STOP - L_VERA:                      # da quando l'uscita cade dopo l'arresto
                for i in range(n):
                    if errs[i] > pk[i]:
                        pk[i] = errs[i]
                    if abs(errs[i]) > 0.10:
                        du[i] += 1
        for i in range(n):
            picchi[i].append(pk[i]); durate[i].append(du[i] * DT)
    desc = "arresto istantaneo" if decel is None else f"frenata {decel} m/s2"
    print(f"\n## v = {v} m/s, {desc}; {semi} semi (5000..); sigma dichiarata dell'uscita portata avanti = {sig*100:.1f} cm; sigma_v a regime = {sv:.3f} m/s")
    print(f"{'uscita':<28}{'media (m)':>10}{'RMS (m)':>9}{'picco dopo arresto: mediana':>29}{'95o perc.':>10}{'durata |e|>0,10 m (s)':>23}")
    for i in range(n):
        pp = sorted(picchi[i]); dd = sorted(durate[i])
        print(f"{nomi[i]:<28}{me[i]/cnt:>10.3f}{math.sqrt(sq[i]/cnt):>9.3f}{pp[len(pp)//2]:>29.3f}{pp[int(0.95*len(pp))]:>10.3f}{dd[len(dd)//2]:>23.2f}")


if __name__ == "__main__":
    print("# S2: errore della posizione mostrata rispetto al vero nell'istante in cui compare (latenza vera 155 ms).")
    print("# Errore positivo = mostrata oltre il vero nel verso del moto. Conti: v*delta = 0,042 m (1,4 m/s) e 0,075 m (2,5 m/s) per 30 ms.")
    for v in (1.4, 2.5):
        prova(v, None)
        prova(v, 3.0)
