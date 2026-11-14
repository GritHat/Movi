#!/usr/bin/env python3
# sciame-kalman, f9/03-kalman: S6 (punto di massimo avvicinamento) e S7 (indice di rotta convergente).
# Python puro, seme fissato.  Uso: timeout 120 python3 sim_s6s7.py
import math, random

DT = 1.0 / 15.0
rng = random.Random(20261114)


def pct(v, p):
    s = sorted(v)
    return s[min(len(s) - 1, int(p * len(s)))]


def sd(v):
    m = sum(v) / len(v)
    return math.sqrt(sum((a - m) ** 2 for a in v) / (len(v) - 1))


# ---------- P-K9: regime del filtro del nucleo (q = 0,2 m^2/s^3, 15 Hz)
print("== P-K9: scarto tipo di regime del Kalman a velocita' quasi costante (q = 0,2; 15 Hz), dopo l'aggiornamento")
SV = {}
for sp in (0.015, 0.034, 0.06):
    for q in (0.2, 0.02):
        p11, p12, p22 = 1.0, 0.0, 1.0
        for _ in range(3000):
            a11 = p11 + 2 * DT * p12 + DT * DT * p22 + q * DT ** 3 / 3
            a12 = p12 + DT * p22 + q * DT * DT / 2
            a22 = p22 + q * DT
            S = a11 + sp * sp
            k1, k2 = a11 / S, a12 / S
            p11, p12, p22 = (1 - k1) * a11, (1 - k1) * a12, a22 - k2 * a12
        SV[(sp, q)] = math.sqrt(p22)
        print(f"  rumore di posizione {100 * sp:4.1f} cm, q {q:4.2f}: sigma_pos {100 * math.sqrt(p11):4.2f} cm, sigma_vel {math.sqrt(p22):5.3f} m/s")

# ---------- P-K7: punto di massimo avvicinamento con errore di velocita'
print("\n== P-K7: t_CPA = max(0, -r.v/|v|^2), d_CPA = |r + v t_CPA|; errore di velocita' 0,2 m/s per asse, posizione 3 cm; N = 100000")
print("   R(m) v(m/s) d_vera | t vero  sd(t)  R*sv/v^2 | mediana(d) 0,67*R*sv/v  p95(d)  2*R*sv/v | P(t=0) | P(d_stim<0,5 m)")
N = 100000
SVEL, SPOS = 0.2, 0.03
for R in (2.0, 3.0):
    for v in (0.5, 1.0, 1.4):
        for dtrue in (0.0, 0.5, 1.0):
            # bersaglio in (0, R) rispetto al punto protetto; velocita' di modulo v diretta a passare a distanza dtrue
            b = math.asin(dtrue / R)
            vx0, vz0 = v * math.sin(b), -v * math.cos(b)
            tt = R * math.cos(b) / v
            ts, ds, n0, nin = [], [], 0, 0
            for _ in range(N):
                rx, rz = rng.gauss(0, SPOS), R + rng.gauss(0, SPOS)
                vx, vz = vx0 + rng.gauss(0, SVEL), vz0 + rng.gauss(0, SVEL)
                t = max(0.0, -(rx * vx + rz * vz) / (vx * vx + vz * vz))
                d = math.hypot(rx + vx * t, rz + vz * t)
                if t == 0.0:
                    n0 += 1
                ts.append(t)
                ds.append(d)
                if d < 0.5:
                    nin += 1
            print(f"   {R:3.1f}  {v:3.1f}   {dtrue:3.1f}   | {tt:5.2f}  {sd(ts):6.2f}  {R * SVEL / v ** 2:5.2f}   | {pct(ds, 0.5):5.2f}      {0.674 * R * SVEL / v:5.2f}       {pct(ds, 0.95):5.2f}   {2 * R * SVEL / v:5.2f}   | {n0 / N:6.4f} | {nin / N:5.3f}")
print("   oggetto FERMO a R, velocita' stimata = solo rumore:")
for R in (2.0, 3.0):
    for sv in (0.2, 0.1):
        na = nb = 0
        for _ in range(N):
            rx, rz = rng.gauss(0, SPOS), R + rng.gauss(0, SPOS)
            vx, vz = rng.gauss(0, sv), rng.gauss(0, sv)
            t = max(0.0, -(rx * vx + rz * vz) / (vx * vx + vz * vz))
            d = math.hypot(rx + vx * t, rz + vz * t)
            if t > 0 and d < 0.5:
                na += 1
                if t < 5.0:
                    nb += 1
        print(f"   R {R:3.1f} m, sigma_v {sv:3.1f}: P(t>0 e d_CPA<0,5 m) = {na / N:5.3f}; con orizzonte t<5 s = {nb / N:5.3f}")

# ---------- P-K8: velocita' angolare, retta ai minimi quadrati su una finestra
print("\n== P-K8: velocita' angolare del rilevamento; rumore d'angolo per campione 1 grado (e 0,29 gradi = cella/radice di 12); 15 Hz")
print("   formula: sd(pendenza) = sigma_ang * sqrt(12 / (n (n^2-1))) / dt ; soglia a due code 5 % = 1,96 sd; mancati 5 % -> serve pendenza >= 3,60 sd")


def need_frames(rate_deg_s, sig_deg):
    for n in range(3, 400):
        s = sig_deg * math.sqrt(12.0 / (n * (n * n - 1))) / DT
        if rate_deg_s >= 3.605 * s:
            return n, s
    return None, None


cases = [("attraversamento 0,3 m/s a 2,0 m", 0.3 / 2.0), ("attraversamento 0,3 m/s a 2,3 m", 0.3 / 2.3), ("attraversamento 0,3 m/s a 3,0 m", 0.3 / 3.0),
         ("attraversamento 0,3 m/s a 4,0 m", 0.3 / 4.0), ("attraversamento 0,1 m/s a 2,3 m", 0.1 / 2.3),
         ("avvicinamento 0,5 m/s da 3 m, passa a 0,5 m", 0.5 * 0.5 / 9.0), ("avvicinamento 0,5 m/s da 2 m, passa a 0,5 m", 0.5 * 0.5 / 4.0),
         ("avvicinamento 1,0 m/s da 3 m, passa a 0,5 m", 1.0 * 0.5 / 9.0), ("avvicinamento 1,0 m/s da 3 m, passa a 1,0 m", 1.0 * 1.0 / 9.0)]
for name, w in cases:
    wd = math.degrees(w)
    out = []
    for sg in (1.0, 0.29):
        n, s = need_frames(wd, sg)
        out.append(f"sigma {sg:4.2f} gradi: {n} campioni = {(n - 1) * DT:4.2f} s")
    print(f"   {name:46s} {wd:5.2f} gradi/s | " + " | ".join(out))

print("   Monte Carlo (20000 prove per ipotesi): retta ai minimi quadrati, soglia tarata al 5 % di falsi sotto 'rotta convergente' (stessa velocita', mira al sensore)")


def slope(th):
    n = len(th)
    tm = (n - 1) / 2.0
    num = sum((i - tm) * th[i] for i in range(n))
    den = sum((i - tm) ** 2 for i in range(n)) * DT
    return num / den


def traj_bearing(r0, speed, miss, n, sig_deg, quant, spos):
    # bersaglio in (0, r0), velocita' di modulo speed che passa a distanza miss dal sensore; rilevamento in gradi
    b = math.asin(min(1.0, miss / r0))
    vx, vz = speed * math.sin(b), -speed * math.cos(b)
    th = []
    for i in range(n):
        x, z = vx * i * DT, r0 + vz * i * DT
        if quant:
            x += rng.gauss(0, spos)          # rumore laterale del centro (m)
            a = math.degrees(math.atan2(x, z))
            a = math.floor(a) + 0.5          # cella di 1 grado
        else:
            a = math.degrees(math.atan2(x, z)) + rng.gauss(0, sig_deg)
        th.append(a)
    return th


def cross_bearing(r0, vperp, n, sig_deg, quant, spos):
    th = []
    for i in range(n):
        x, z = vperp * i * DT, r0
        if quant:
            x += rng.gauss(0, spos)
            a = math.floor(math.degrees(math.atan2(x, z))) + 0.5
        else:
            a = math.degrees(math.atan2(x, z)) + rng.gauss(0, sig_deg)
        th.append(a)
    return th


M = 20000
for label, gen1, gen0 in [
    ("attraversamento 0,3 m/s a 2,3 m contro fermo-in-rilevamento", lambda n, q: cross_bearing(2.3, 0.3, n, 1.0, q, 0.03), lambda n, q: cross_bearing(2.3, 0.0, n, 1.0, q, 0.03)),
    ("attraversamento 0,3 m/s a 4,0 m", lambda n, q: cross_bearing(4.0, 0.3, n, 1.0, q, 0.06), lambda n, q: cross_bearing(4.0, 0.0, n, 1.0, q, 0.06)),
    ("0,5 m/s da 3 m: passa a 0,5 m contro mira al sensore", lambda n, q: traj_bearing(3.0, 0.5, 0.5, n, 1.0, q, 0.034), lambda n, q: traj_bearing(3.0, 0.5, 0.0, n, 1.0, q, 0.034)),
    ("1,0 m/s da 3 m: passa a 0,5 m contro mira al sensore", lambda n, q: traj_bearing(3.0, 1.0, 0.5, n, 1.0, q, 0.034), lambda n, q: traj_bearing(3.0, 1.0, 0.0, n, 1.0, q, 0.034)),
]:
    for quant in (False, True):
        found = None
        rows = []
        for n in (4, 6, 8, 9, 10, 12, 15, 18, 21, 24, 27, 30, 36, 45):
            s0 = sorted(abs(slope(gen0(n, quant))) for _ in range(M // 4))
            thr = s0[int(0.95 * len(s0))]
            miss = sum(1 for _ in range(M // 4) if abs(slope(gen1(n, quant))) <= thr) / (M // 4)
            rows.append((n, thr, miss))
            if found is None and miss <= 0.05:
                found = n
                break
        tag = "angolo quantizzato a 1 grado + rumore laterale del centro" if quant else "rumore gaussiano di 1 grado"
        last = rows[-1]
        print(f"   {label} [{tag}]: mancati <= 5 % con {found} campioni = {((found - 1) * DT) if found else float('nan'):4.2f} s (soglia {last[1]:4.2f} gradi/s, mancati {last[2]:5.3f})")

print("\n   'subito', dalla velocita' del filtro: sd(vel. angolare) = sigma_v / r; attraversamento minimo separabile (3,60 sd) = 3,60 * sigma_v")
for sv in (0.2, SV[(0.015, 0.2)], SV[(0.034, 0.2)], SV[(0.06, 0.2)]):
    print(f"   sigma_v {sv:5.3f} m/s: a 2,3 m sd = {math.degrees(sv / 2.3):4.1f} gradi/s; velocita' trasversale minima separabile = {3.605 * sv:4.2f} m/s (a qualunque distanza)")
