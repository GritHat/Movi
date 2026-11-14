#!/usr/bin/env python3
# Conto di sciame-requisiti (f8): crescita della regione al 95 % del filtro a velocita' quasi costante
# senza misure, e durata dello stato «previsto» con la regola «meta' del cuneo» nella geometria della demo.
# Python puro, deterministico (nessun numero casuale). Rifare: timeout 120 python3 conto_requisiti.py
import math

DT = 1.0 / 15.0
Q = 0.2            # m^2/s^3, SOLUZIONE_V2 B4
CHI2_95 = 5.991    # 2 gradi di liberta'

def steady(sigma):
    # stato stazionario per asse [p, v], misura di posizione con varianza sigma^2
    p11, p12, p22 = 1.0, 0.0, 1.0
    r = sigma * sigma
    for _ in range(5000):
        # predizione
        a11 = p11 + 2 * DT * p12 + DT * DT * p22 + Q * DT ** 3 / 3
        a12 = p12 + DT * p22 + Q * DT ** 2 / 2
        a22 = p22 + Q * DT
        # aggiornamento
        s = a11 + r
        k1, k2 = a11 / s, a12 / s
        p11 = (1 - k1) * a11
        p12 = (1 - k1) * a12
        p22 = a22 - k2 * a12
    return p11, p12, p22

def sigma_pos(p, t):
    p11, p12, p22 = p
    return math.sqrt(p11 + 2 * t * p12 + t * t * p22 + Q * t ** 3 / 3)

print("== A. Raggio della regione al 95 % senza misure (q = 0,2; 15 Hz) ==")
print("sigma_mis  t[s]   sigma_pos[m]  r95[m]")
P = {}
for sig in (0.015, 0.05, 0.11):
    P[sig] = steady(sig)
    for t in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0):
        s = sigma_pos(P[sig], t)
        print(f"{sig:8.3f} {t:5.1f} {s:12.3f} {math.sqrt(CHI2_95) * s:8.2f}")
    print(f"   (stazionario: sigma_p = {math.sqrt(P[sig][0]):.3f} m, sigma_v = {math.sqrt(P[sig][2]):.3f} m/s)")

print()
print("== B. Regola «previsto finche' il cerchio ritagliato copre meno di meta' del cuneo in griglia» ==")
# sensore in (0,0); pannello largo W a distanza D (parallelo all'asse x); griglia fino a RMAX
def run(W, D, YA, V, RMAX, sig):
    half = math.atan2(W / 2, D)
    step = 0.02
    cells = []
    x = -RMAX
    while x <= RMAX:
        y = D
        while y <= RMAX:
            r = math.hypot(x, y)
            if r <= RMAX and abs(math.atan2(x, y)) <= half and y > D:
                cells.append((x, y))
            y += step
        x += step
    area = len(cells) * step * step
    xin = -YA * math.tan(half)          # ingresso nell'ombra alla distanza YA
    buio = 2 * abs(xin) / V
    tfine = None
    righe = []
    for k in range(1, 76):
        t = k * DT
        r95 = math.sqrt(CHI2_95) * sigma_pos(P[sig], t)
        cx = xin + V * t
        n = sum(1 for (x, y) in cells if (x - cx) ** 2 + (y - YA) ** 2 <= r95 * r95)
        fr = n / len(cells)
        if tfine is None and fr >= 0.5:
            tfine = t
        if k in (8, 15, 30, 45, 75):
            righe.append((t, r95, fr))
    print(f"pannello {W} m a {D} m, attore a {YA} m e {V} m/s, griglia {RMAX} m, sigma {sig}: "
          f"cuneo {area:.2f} m^2, buio {buio:.2f} s, «previsto» fino a {tfine:.2f} s")
    for (t, r95, fr) in righe:
        print(f"     t = {t:4.2f} s: r95 = {r95:5.2f} m, quota del cuneo coperta dal cerchio ritagliato = {100*fr:5.1f} %")
    return buio, tfine

casi = []
for sig in (0.015, 0.05):
    for V in (0.8, 1.2):
        casi.append((V, sig) + run(1.0, 1.8, 2.3, V, 3.0, sig))
print()
print("== C. Quota dei cicli senza osservazione con una stima emessa (regola della versione 2) ==")
print("durata del «previsto» T_p dal conto B (indipendente dalla durata del buio: «perso» e' assorbente)")
for (V, sig, buio, tp) in casi:
    riga = f"v = {V}, sigma = {sig}: T_p = {tp:.2f} s -> buio demo {buio:.2f} s: {100*min(1,tp/buio):.0f} %"
    for d in (1.2, 3.0, 5.0):
        riga += f"; {d} s: {100*min(1,tp/d):.0f} %"
    print(riga)
print("con le durate MISURATE dalla validazione (MISURE_V2.md, P4): T_p = 0,40 / 0,47 / 0,53 s, buio 1,13 / 1,07 / 1,07 s")
for tp, buio in ((0.40, 1.13), (0.47, 1.07), (0.53, 1.07)):
    riga = f"T_p = {tp}: demo {100*tp/buio:.0f} %"
    for d in (1.2, 3.0, 5.0):
        riga += f"; {d} s: {100*tp/d:.0f} %"
    print(riga)
print("sosta (MISURE_V2.md, P4: «perso» 4,6-4,8 s): quota = T_p/(T_p + perso) = "
      f"{100*0.40/(0.40+4.8):.0f}-{100*0.53/(0.53+4.6):.0f} %")

print()
print("== D. Falsificatore di requisiti-2: quota dei cicli di buio in grado «saturo» (regione al 90 % >= 80 % del cuneo) ==")
CHI2_90 = 4.605
CHI2_50 = 1.386
def satura(W, D, YA, V, RMAX, sig, buio_forzato=None):
    half = math.atan2(W / 2, D)
    step = 0.02
    cells = []
    x = -RMAX
    while x <= RMAX:
        y = D
        while y <= RMAX:
            if math.hypot(x, y) <= RMAX and abs(math.atan2(x, y)) <= half and y > D:
                cells.append((x, y))
            y += step
        x += step
    xin = -YA * math.tan(half)
    buio = buio_forzato if buio_forzato else 2 * abs(xin) / V
    n = int(round(buio / DT))
    sat = 0
    primo = None
    cop50 = []
    for k in range(1, n + 1):
        t = k * DT
        s = sigma_pos(P[sig], t)
        cx = xin + V * t
        r90 = math.sqrt(CHI2_90) * s
        r50 = math.sqrt(CHI2_50) * s
        f90 = sum(1 for (x, y) in cells if (x - cx) ** 2 + (y - YA) ** 2 <= r90 * r90) / len(cells)
        f50 = sum(1 for (x, y) in cells if (x - cx) ** 2 + (y - YA) ** 2 <= r50 * r50) / len(cells)
        if k in (8, 15, 30, 45, 75):
            cop50.append(f"{t:.2f} s: 50 % -> {100*f50:.0f} %, 90 % -> {100*f90:.0f} %")
        if f90 >= 0.8:
            sat += 1
            if primo is None:
                primo = t
    print(f"v = {V} m/s, buio {buio:.2f} s ({n} cicli): saturi {sat} = {100*sat/n:.0f} %, primo ciclo saturo a "
          f"{'mai' if primo is None else format(primo, '.2f') + ' s'}")
    print("     quota del cuneo coperta: " + "; ".join(cop50))
satura(1.0, 1.8, 2.3, 1.2, 3.0, 0.05)
satura(1.0, 1.8, 2.3, 0.8, 3.0, 0.05)
print("sosta: buio forzato a 5 s; il filtro non sa della sosta e il punto previsto prosegue a velocita' costante")
satura(1.0, 1.8, 2.3, 1.2, 3.0, 0.05, 5.0)
satura(1.0, 1.8, 2.3, 0.8, 3.0, 0.05, 5.0)
