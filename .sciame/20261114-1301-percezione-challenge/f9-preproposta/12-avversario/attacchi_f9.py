#!/usr/bin/env python3
"""Attacchi alla preproposta esterna (f9) - sciame-avversario.
Solo libreria standard. Semi fissati (base 20261114).
Uso: PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 attacchi_f9.py p1|p2|p3|p4|p5|p6|p7|p8|p9|tutto
Modello dichiarato in PREVISIONI.md prima dell'esecuzione.
"""
import math
import random
import sys

SEME = 20261114
H_CAM = 1.2
TILT = math.radians(15.0)
HFOV = math.radians(87.0)
VFOV = math.radians(58.0)
FPS = 15.0
DT = 1.0 / FPS
R_MAX = 3.0
ANG_GIU = TILT + VFOV / 2      # 44 gradi sotto l'orizzonte
ANG_SU = VFOV / 2 - TILT       # 14 gradi sopra l'orizzonte
R_SUOLO = H_CAM / math.tan(ANG_GIU)
Q = 0.2
OMBRA = (-0.64, 0.64)          # ombra sulla linea dell'attore (2,3 m), pannello 1 m a 1,8 m


def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def massa(m, s, a, b):
    """Massa di N(m, s) nell'intervallo [a, b]."""
    if b <= a:
        return 0.0
    return phi((b - m) / s) - phi((a - m) / s)


# ---------------------------------------------------------------- P1
def celle_griglia():
    """Celle polari 1 grado x 0,1 m, da 0,5 a 3 m, entro il campo di 87 gradi."""
    out = []
    for az in range(-43, 44):
        for k in range(25):
            r = 0.55 + 0.1 * k
            a = math.radians(az)
            out.append((az, r, r * math.sin(a), r * math.cos(a)))
    return out


def p1():
    print("== P1 (S8): attesa prudente con il non osservato del nucleo ==")
    print(f"suolo visto da {R_SUOLO:.3f} m (anello cieco sotto)")
    celle = celle_griglia()
    corr = [c for c in celle if abs(c[2]) <= 0.5]            # corridoio largo 1 m, dal sensore
    cieche = [c for c in corr if c[1] < R_SUOLO]
    zona = [c for c in corr if c[1] >= R_SUOLO]
    print(f"P1a corridoio alla lettera: {len(corr)} celle in griglia, di cui {len(cieche)} nell'anello cieco "
          f"(sempre 'non osservato'); in piu' tutto il tratto 0-0,5 m non e' in griglia")
    print(f"P1a fotogrammi in attesa su 900, stanza vuota, suolo sempre valido: "
          f"{900 if cieche else 0} su 900 = {100.0 if cieche else 0.0:.1f} %")
    n = len(zona)
    print(f"P1b corridoio ristretto alla zona {R_SUOLO:.2f}-3 m: {n} celle")
    for p in (1.0, 0.99, 0.95):
        rnd = random.Random(SEME + int(p * 100))
        cons = [0] * n
        in_att = 0
        ingressi = 0
        prima = False
        nf = 900
        for f in range(nf):
            att = False
            for i in range(n):
                if rnd.random() < p:
                    cons[i] = 0
                else:
                    cons[i] += 1
                    if cons[i] >= 3:
                        att = True
            if att:
                in_att += 1
                if not prima:
                    ingressi += 1
            prima = att
        teor = 1.0 - (1.0 - (1.0 - p) ** 3) ** n
        print(f"  p={p:.2f}: in attesa {in_att}/{nf} = {100.0 * in_att / nf:.1f} % "
              f"(atteso a conto {100.0 * teor:.1f} %), ingressi in attesa {ingressi / (nf * DT):.2f}/s")
    rnd = random.Random(SEME + 7)
    perm = 0
    for _ in range(200):
        if any(rnd.random() < 0.01 for _ in range(n)):
            perm += 1
    print(f"  1 % di celle sempre non valide: attesa permanente in {perm}/200 estrazioni "
          f"(a conto {100.0 * (1 - 0.99 ** n):.1f} %)")

    print("P1c enumerazione dei quattro livelli come sono scritti")
    bersagli = ("nessuno", "visto_avv", "visto_non_avv", "previsto_avv", "previsto_non_avv")
    tot = nessuno = multi = 0
    es_nessuno = []
    es_multi = []

    def livelli(occ, ombra, pp, nonoss, tgt, h2, pin, integ):
        liv = []
        if (not occ and not ombra and not pp and not nonoss) and pin == "zero":
            liv.append("NOMINALE")
        if tgt in ("visto_avv", "previsto_avv"):
            liv.append("ATTENZIONE")
        if pp or nonoss or h2:
            liv.append("ATTESA")
        if pin == "critica" or integ == "persa":
            liv.append("AVARIA")
        return liv

    for occ in (False, True):
        for ombra in (False, True):
            for pp in (False, True):
                for nonoss in (False, True):
                    for tgt in bersagli:
                        for h2 in (False, True):
                            for pin in ("zero", "media", "critica"):
                                for integ in ("ok", "persa"):
                                    # coerenza
                                    if tgt.startswith("visto") and not occ:
                                        continue
                                    if tgt.startswith("previsto") and not pp:
                                        continue
                                    if h2 and not pp:
                                        continue
                                    if pin != "zero" and tgt == "nessuno":
                                        continue
                                    tot += 1
                                    liv = livelli(occ, ombra, pp, nonoss, tgt, h2, pin, integ)
                                    if not liv:
                                        nessuno += 1
                                        if len(es_nessuno) < 4:
                                            es_nessuno.append((occ, ombra, pp, nonoss, tgt, pin))
                                    elif len(liv) > 1:
                                        multi += 1
                                        if len(es_multi) < 3:
                                            es_multi.append((liv, tgt, pp, nonoss, pin, integ))
    print(f"  combinazioni coerenti: {tot}; senza nessun livello: {nessuno} ({100.0 * nessuno / tot:.1f} %); "
          f"con due o piu' livelli: {multi} ({100.0 * multi / tot:.1f} %)")
    a2 = livelli(True, False, False, False, "nessuno", False, "zero", "ok")
    a2o = livelli(True, True, False, False, "nessuno", False, "zero", "ok")
    a3 = livelli(True, False, False, False, "visto_non_avv", False, "zero", "ok")
    so = livelli(False, True, False, False, "nessuno", False, "zero", "ok")
    print(f"  atto 2 (ostacolo fermo, nessun bersaglio): {a2 or 'NESSUN LIVELLO'}; con la sua ombra: {a2o or 'NESSUN LIVELLO'}")
    print(f"  atto 3 (attraversamento in vista): {a3 or 'NESSUN LIVELLO'}")
    print(f"  ombra senza traccia (K-016): {so or 'NESSUN LIVELLO'}")
    print(f"  esempi con piu' livelli: {es_multi}")


# ---------------------------------------------------------------- S3-S4 comune
def ipotesi(v, k, sig2):
    """Medie e sigma delle due ipotesi al ciclo k (t = k*DT), ingresso a x = bordo sinistro."""
    t = k * DT
    x1 = OMBRA[0] + v * t
    s1 = math.sqrt(0.05 ** 2 + Q * t ** 3 / 3.0)
    c = (0.0 - OMBRA[0]) / (v * DT)
    alfa = c / (1.0 + c)
    x2 = OMBRA[0] + v * DT * alfa * (1 - alfa ** k) / (1 - alfa)
    if sig2 == "q":
        s2 = s1
    else:
        s2 = sig2
    return x1, s1, x2, s2, alfa


def pesi(v, kmax, sig2, lettura):
    """Lista per ciclo di (mu1, mu2, x1, s1, x2, s2, f1, f2) senza alcuna misura."""
    out = []
    m1, m2 = 0.8, 0.2
    for k in range(kmax + 1):
        x1, s1, x2, s2, _ = ipotesi(v, k, sig2)
        f1 = max(massa(x1, s1, *OMBRA), 1e-300)
        f2 = max(massa(x2, s2, *OMBRA), 1e-300)
        if lettura == "A":
            if k > 0:
                a, b = m1 * f1, m2 * f2
                m1, m2 = a / (a + b), b / (a + b)
            u1, u2 = m1, m2
        else:
            a, b = 0.8 * f1, 0.2 * f2
            u1, u2 = a / (a + b), b / (a + b)
        out.append((u1, u2, x1, s1, x2, s2, f1, f2))
    return out


def momenti_ritagliati(m, s, a, b, n=256):
    """Media e varianza di N(m,s) ritagliata su [a,b] (integrazione numerica)."""
    h = (b - a) / n
    z = mx = mxx = 0.0
    for i in range(n):
        x = a + (i + 0.5) * h
        w = math.exp(-0.5 * ((x - m) / s) ** 2)
        z += w
        mx += w * x
        mxx += w * x * x
    if z <= 0.0:
        # tutta la massa fuori: il ritaglio la schiaccia sul bordo piu' vicino
        x = a if m < a else b
        return x, 0.0
    mx /= z
    return mx, max(mxx / z - mx * mx, 0.0)


# ---------------------------------------------------------------- P2
def p2():
    print("== P2 (S6): probabilita' d'intrusione sulla distribuzione ritagliata ==")
    v = 1.2
    pva = (-1.24, -0.64)
    pvb = (-0.94, -0.44)
    print("soggetto entra a 1,2 m/s e si ferma 9 cm dentro l'ombra (x = -0,55); nessuna misura durante l'occlusione")
    for nome, pv in (("PVa tutto visibile [-1,24;-0,64]", pva), ("PVb entra 0,20 m nell'ombra [-0,94;-0,44]", pvb)):
        a = max(pv[0], OMBRA[0])
        b = min(pv[1], OMBRA[1])
        dentro = pv[0] <= -0.55 <= pv[1]
        print(f" {nome}; soggetto dentro il volume: {dentro}; distanza dal volume: "
              f"{0.0 if dentro else min(abs(-0.55 - pv[0]), abs(-0.55 - pv[1])):.2f} m")
        for sig2 in (0.20, 0.32, "q"):
            for lett in ("A", "B"):
                st = pesi(v, 45, sig2, lett)
                riga = []
                mx_dopo = 0.0
                mx_tutti = 0.0
                for k, (u1, u2, x1, s1, x2, s2, f1, f2) in enumerate(st):
                    p = u1 * massa(x1, s1, a, b) / f1 + u2 * massa(x2, s2, a, b) / f2
                    mx_tutti = max(mx_tutti, p)
                    if k * DT >= 1.5 - 1e-9:
                        mx_dopo = max(mx_dopo, p)
                    if k in (0, 8, 15, 23, 30, 45):
                        riga.append(f"t={k * DT:.2f}s P={p:.4f}")
                print(f"   sigma2={sig2} lettura {lett}: " + "; ".join(riga)
                      + f" | max per t>=1,5 s: {mx_dopo:.4f}; max assoluto: {mx_tutti:.4f}")
    # tempo fisico: dal bordo dell'ombra al volume
    for d in (0.09, 0.2, 0.4):
        print(f" soggetto nascosto a {d:.2f} m dal volume, parte a 1,4 m/s: dentro in {d / 1.4 * 1000:.0f} ms "
              f"(latenza nota 155 ms + 1 ciclo 67 ms = 222 ms)")


# ---------------------------------------------------------------- P3
def p3():
    print("== P3 (S1): passaggio 3 fasce -> 2D e riga della scheda grafica ==")
    print(f"suolo visto da {R_SUOLO:.3f} m; ostacolo alto 0,15 m visibile solo oltre "
          f"{(H_CAM - 0.15) / math.tan(ANG_GIU):.3f} m; e' un limite del cono di vista, non della mappa")
    for hb in (0.15, 0.30, 0.60):
        print(f"  fascia bassa: quota {hb:.2f} m entra nel campo da {(H_CAM - hb) / math.tan(ANG_GIU):.3f} m")
    a_tot = R_MAX ** 2 - R_SUOLO ** 2
    for h in (1.61, 1.8, 2.0):
        r = (h - H_CAM) / math.tan(ANG_SU)
        rr = min(R_MAX, max(r, R_SUOLO))
        fr = (rr ** 2 - R_SUOLO ** 2) / a_tot
        print(f"  quota {h:.2f} m dentro il campo solo oltre {r:.2f} m -> fascia alta NON osservata sul "
              f"{100.0 * fr:.1f} % dell'area della zona {R_SUOLO:.2f}-3 m")
    area = (HFOV / 2) * a_tot
    print(f"  area della zona: {area:.2f} m2; con quota pertinente 1,8 m passano da 'non osservato in fascia alta' "
          f"a 'libero' {area * (min(R_MAX, 0.6 / math.tan(ANG_SU)) ** 2 - R_SUOLO ** 2) / a_tot:.2f} m2 al cambio verso la 2D")
    print(f"  quota massima vista a 1,0 / 2,0 / 3,0 m: "
          + " / ".join(f"{H_CAM + d * math.tan(ANG_SU):.2f}" for d in (1.0, 2.0, 3.0)) + " m")


# ---------------------------------------------------------------- P4
def selettore(base, ext, regole, start, durata=60.0, permanenza=0.0, sigma=2.0, seme=0):
    rnd = random.Random(SEME + seme)
    cfg = start
    fin = []
    cambi = 0
    ultimo = -1e9
    storia = [(0.0, cfg)]
    n = int(durata * FPS)
    for k in range(n):
        t = k * DT
        fin.append(base[cfg] + ext(t) + rnd.gauss(0.0, sigma))
        if len(fin) > 15:
            fin.pop(0)
        if k % 8 == 7 and len(fin) == 15:
            m = sum(fin) / 15.0
            nuovo = regole(m, cfg)
            if nuovo != cfg and (t - ultimo) >= permanenza:
                cfg = nuovo
                cambi += 1
                ultimo = t
                storia.append((round(t, 2), cfg))
    return cambi, storia


def p4():
    print("== P4 (attacco 3 del file): oscillazione del selettore ==")

    def regole2(m, cfg):
        if m > 55.0:
            return "RIDOTTA"
        if m < 45.0:
            return "PIENA"
        return cfg

    def regole3(m, cfg):
        if m > 55.0:
            return "RIDOTTA_2D"
        if m < 30.0:
            return "VOXEL"
        return cfg

    zero = lambda t: 0.0
    # P4a: nessuna dipendenza dalla configurazione, rumore attorno a 55
    for sg in (2.0, 5.0):
        c, st = selettore({"PIENA": 55.0, "RIDOTTA": 55.0}, zero, regole2, "PIENA", sigma=sg, seme=1)
        print(f"P4a tempo di ciclo 55 ms +- {sg:.0f} per tutte le configurazioni, senza isteresi temporale: {c} cambi in 60 s {st[:4]}")
    # senza previsione: carico sinusoidale
    sinus = lambda t: 8.0 * math.sin(2 * math.pi * t / 10.0)
    for perm in (0.0, 3.0):
        c, _ = selettore({"PIENA": 50.0, "RIDOTTA": 50.0}, sinus, regole2, "PIENA", permanenza=perm, seme=2)
        print(f"[senza previsione] carico 50 +- 8 ms, periodo 10 s, permanenza {perm:.0f} s: {c} cambi in 60 s")
    # P4b: retroazione
    for perm in (0.0, 2.0, 3.0):
        c, st = selettore({"PIENA": 58.0, "RIDOTTA": 38.0}, zero, regole2, "PIENA", permanenza=perm, seme=3)
        ult = st[-1][0]
        print(f"P4b piena 58 ms, ridotta 38 ms, permanenza {perm:.0f} s: {c} cambi in 60 s; ultimo cambio a {ult:.1f} s")
    c, st = selettore({"PIENA": 58.0, "RIDOTTA": 38.0}, zero, regole2, "PIENA", durata=600.0, permanenza=3.0, seme=3)
    print(f"P4b su 600 s con permanenza 3 s: {c} cambi; ultimo a {st[-1][0]:.1f} s (non si ferma)")
    # confine del ciclo limite
    print("P4b confine: cambi in 60 s (permanenza 3 s) al variare del risparmio D = piena - ridotta, piena = 58 ms")
    riga = []
    for d in (5, 10, 12, 13, 14, 16, 20, 30):
        c, _ = selettore({"PIENA": 58.0, "RIDOTTA": 58.0 - d}, zero, regole2, "PIENA", permanenza=3.0, seme=4)
        riga.append(f"D={d}: {c}")
    print("   " + "; ".join(riga))
    # P4c: riga della scheda grafica
    for perm in (0.0, 3.0):
        c, st = selettore({"VOXEL": 60.0, "RIDOTTA_2D": 20.0, "FASCE": 25.0}, zero, regole3, "FASCE", permanenza=perm, seme=5)
        print(f"P4c 3 fasce 25 ms -> voxel 60 ms -> 2D 20 ms, permanenza {perm:.0f} s: {c} cambi in 60 s {st[:5]}")
    # P4d: resta degradato
    ext = lambda t: 6.0 if t < 20.0 else 0.0
    c, st = selettore({"PIENA": 52.0, "RIDOTTA": 47.0}, ext, regole2, "PIENA", seme=6)
    ritorni = sum(1 for (_, s) in st[1:] if s == "PIENA")
    print(f"P4d piena 52, ridotta 47, carico +6 ms fino a 20 s: {c} cambi, ritorni alla piena: {ritorni}, storia {st}")


# ---------------------------------------------------------------- P5
def raggio_pixel(i, j, nx, ny):
    """Direzione nel mondo (x destra, y su, z avanti) del pixel (i, j) in spazio tangente."""
    u = (2.0 * (i + 0.5) / nx - 1.0) * math.tan(HFOV / 2)
    w = (1.0 - 2.0 * (j + 0.5) / ny) * math.tan(VFOV / 2)      # su positivo
    # camera: asse ottico inclinato di TILT verso il basso
    dx, dy, dz = u, w, 1.0
    cy, sy = math.cos(TILT), math.sin(TILT)
    return dx, dy * cy - dz * sy, dy * sy + dz * cy


def colpisce(dx, dy, dz, rett):
    """Il raggio dalla camera colpisce il rettangolo verticale (z0, xmin, xmax, ymin, ymax) prima del suolo?"""
    z0, xa, xb, ya, yb = rett
    if dz <= 0:
        return False
    t = z0 / dz
    x = dx * t
    y = H_CAM + dy * t
    return xa <= x <= xb and ya <= y <= yb


def quota_pixel(retts, nx=348, ny=232):
    n = 0
    for j in range(ny):
        for i in range(nx):
            d = raggio_pixel(i, j, nx, ny)
            if any(colpisce(*d, r) for r in retts):
                n += 1
    return n / (nx * ny)


def quota_celle(retts):
    celle = [c for c in celle_griglia() if c[1] >= R_SUOLO]
    perse = 0
    for (_, r, x, z) in celle:
        d = (x, -H_CAM, z)          # dal sensore al centro della cella sul suolo
        for (z0, xa, xb, ya, yb) in retts:
            if z0 < z:
                t = z0 / d[2]
                xx = d[0] * t
                yy = H_CAM + d[1] * t
                if xa <= xx <= xb and ya <= yy <= yb:
                    perse += 1
                    break
    return perse, len(celle)


def p5():
    print("== P5 (attacco 4 del file): tessuto nero contro 'sensore coperto' ==")
    persona = (2.5, -0.25, 0.25, 0.0, 1.75)
    fp = quota_pixel([persona])
    pc, nc = quota_celle([persona])
    print(f"P5a persona in nero 0,5 x 1,75 m a 2,5 m, nessun ritorno: pixel non validi {100 * fp:.1f} %; "
          f"celle della zona non valide {pc}/{nc} = {100.0 * pc / nc:.1f} %")
    print(f"P5a soglia 'sensore coperto': valide < 50 % della taratura per 3 fotogrammi -> scatta: "
          f"{'SI' if (1 - pc / nc) < 0.5 or (1 - fp) < 0.5 else 'NO'} (0 fotogrammi su 900: scena statica, conto esatto)")
    crit = None
    d = 3.0
    while d > 0.3:
        if quota_pixel([(d, -0.25, 0.25, 0.0, 1.75)], 174, 116) >= 0.5:
            crit = d
            break
        d -= 0.05
    print(f"P5a distanza a cui la stessa persona toglie il 50 % dei pixel: {crit if crit is None else round(crit, 2)} m")
    for n in (2, 3, 4, 6):
        retts = [(2.5, -0.25 + 0.6 * (k - (n - 1) / 2), 0.25 + 0.6 * (k - (n - 1) / 2), 0.0, 1.75) for k in range(n)]
        print(f"   [senza previsione] {n} persone in nero affiancate a 2,5 m: pixel non validi {100 * quota_pixel(retts, 174, 116):.1f} %")
    pannello = (1.8, -0.5, 0.5, 0.0, 1.5)
    fpp = quota_pixel([pannello], 174, 116)
    pcp, _ = quota_celle([pannello])
    print(f"   [senza previsione] pannello della demo NERO (1 x 1,5 m a 1,8 m), nessun ritorno: pixel {100 * fpp:.1f} %, "
          f"celle {100.0 * pcp / nc:.1f} %: nessun 'occupato', quindi nessun occlusore e nessun cuneo dello strato 1")
    print("P5b persona invisibile che cammina, 'libero' = suolo visto in uno degli ultimi 3 fotogrammi")
    for v in (1.4, 0.5):
        rnd = random.Random(SEME + int(v * 10))
        tot_f = con = 0
        somma = 0
        mx = 0
        for _ in range(200):
            x0 = -1.5 + rnd.random() * 0.1
            ncel = 60                      # celle da 0,1 m fra -3 e +3
            storia = [[True] * ncel for _ in range(3)]
            k = 0
            while True:
                xc = x0 + v * k * DT
                if xc > 1.5:
                    break
                validi = []
                sotto = []
                for i in range(ncel):
                    c = -3.0 + 0.1 * (i + 0.5)
                    s = abs(c - xc) <= 0.25
                    sotto.append(s)
                    validi.append(not s)
                storia = [storia[1], storia[2], validi]
                if k >= 3:
                    nlib = sum(1 for i in range(ncel) if sotto[i] and (storia[0][i] or storia[1][i] or storia[2][i]))
                    tot_f += 1
                    somma += nlib
                    mx = max(mx, nlib)
                    if nlib >= 1:
                        con += 1
                k += 1
        print(f"  v={v} m/s: fotogrammi con >=1 cella 'libero' sotto il corpo {con}/{tot_f} = {100.0 * con / tot_f:.1f} %; "
              f"media {somma / tot_f:.2f} celle, massimo {mx} (celle da 0,1 m)")
    print("  ferma: dopo 3 fotogrammi 0 celle 'libero' sotto il corpo (per costruzione della regola)")


# ---------------------------------------------------------------- P6
def p6():
    print("== P6 (S3-S4): falsa 'sosta in ombra' nei transiti normali; il modo che cammina ==")
    print(f"ombra {OMBRA}, tempo d'attraversamento a 1,2 m/s: {(OMBRA[1] - OMBRA[0]) / 1.2:.2f} s")
    for c6, nomec in ((0.2, "misura valida a corpo tutto fuori (C6)"), (0.0, "misura valida appena il centro esce")):
        for sig2 in (0.32, 0.20, "q"):
            for lett in ("A", "B"):
                rnd = random.Random(SEME + 61)
                falsi = 0
                n = 2000
                mu1_fin = []
                for _ in range(n):
                    v = 0.5 + 0.9 * rnd.random()
                    st = pesi(v, 120, sig2, lett)
                    falso = False
                    for k in range(1, 121):
                        xvero = OMBRA[0] + v * k * DT
                        if xvero >= OMBRA[1] + c6 and rnd.random() < 0.9:
                            mu1_fin.append(st[k][0])
                            break
                        if st[k][1] > 0.5:
                            falso = True
                    if falso:
                        falsi += 1
                mu1_fin.sort()
                med = mu1_fin[len(mu1_fin) // 2]
                print(f"P6a {nomec}; sigma2={sig2}; lettura {lett}: falsa sosta (mu2>0,5 prima della prima misura) "
                      f"{falsi}/{n} = {100.0 * falsi / n:.1f} %; mu1 mediano alla prima misura {med:.3f}")
    print("P6b sosta 9 cm dentro l'ombra (x=-0,55), v d'ingresso 1,2 m/s, sigma2=0,32")
    for lett in ("A", "B"):
        st = pesi(1.2, 45, 0.32, lett)
        dmax = 0.0
        t_cambio = None
        for k, (u1, u2, x1, s1, x2, s2, f1, f2) in enumerate(st):
            if u1 > 0.5:
                modo = min(x1, OMBRA[1])
                dmax = max(dmax, abs(modo - (-0.55)))
            elif t_cambio is None:
                t_cambio = k * DT
        print(f"  lettura {lett}: distanza massima fra il modo mostrato (H1, mu1>0,5) e il soggetto {dmax:.2f} m; "
              f"mu2 supera 0,5 a t={t_cambio if t_cambio is None else round(t_cambio, 2)} s "
              f"(uscita attesa a {(OMBRA[1] - OMBRA[0]) / 1.2:.2f} s)")
    print("[senza previsione] copertura dell'etichetta 'PREVISTO +-sigma_eff' (miscela ritagliata, 1D lungo la linea), sigma2=0,32")
    casi = {
        "sosta a 9 cm dal bordo d'ingresso": lambda t: -0.55 if t > 0.075 else OMBRA[0] + 1.2 * t,
        "sosta al centro": lambda t: 0.0 if t > 0.533 else OMBRA[0] + 1.2 * t,
        "rallenta a 0,3 m/s": lambda t: OMBRA[0] + 1.2 * t if t <= 0.075 else -0.55 + 0.3 * (t - 0.075),
        "torna indietro dal centro": lambda t: OMBRA[0] + 1.2 * t if t <= 0.533 else 0.0 - 1.2 * (t - 0.533),
    }
    for nome, f in casi.items():
        for lett in ("A", "B"):
            st = pesi(1.2, 60, 0.32, lett)
            n = d1 = d2 = 0
            errmax = 0.0
            smax = 0.0
            for k in range(1, 61):
                t = k * DT
                xv = f(t)
                if not (OMBRA[0] <= xv <= OMBRA[1]):
                    break
                u1, u2, x1, s1, x2, s2, _, _ = st[k]
                m1, v1 = momenti_ritagliati(x1, s1, *OMBRA)
                m2, v2 = momenti_ritagliati(x2, s2, *OMBRA)
                m = u1 * m1 + u2 * m2
                var = u1 * (v1 + (m1 - m) ** 2) + u2 * (v2 + (m2 - m) ** 2)
                s = math.sqrt(var)
                n += 1
                e = abs(xv - m)
                errmax = max(errmax, e)
                smax = max(smax, s)
                if e <= s:
                    d1 += 1
                if e <= 1.96 * s:
                    d2 += 1
            print(f"  {nome}; lettura {lett}: fotogrammi nascosti {n}; dentro +-sigma_eff {100.0 * d1 / n:.0f} %; "
                  f"dentro +-1,96 sigma_eff {100.0 * d2 / n:.0f} %; errore massimo {errmax:.2f} m; sigma_eff massimo {smax:.2f} m")


# ---------------------------------------------------------------- P6x (scritta DOPO aver visto P6: esplorativa)
def p6x():
    print("== P6x [DOPO gli esiti di P6, senza previsione]: lettura B, sensibilita' al ritardo della prima misura ==")
    for rit in (0, 1, 2, 3):
        for pd in (0.9, 0.7):
            rnd = random.Random(SEME + 62)
            falsi = 0
            n = 2000
            for _ in range(n):
                v = 0.5 + 0.9 * rnd.random()
                st = pesi(v, 140, 0.32, "B")
                falso = False
                visto_da = None
                for k in range(1, 141):
                    xvero = OMBRA[0] + v * k * DT
                    if visto_da is None and xvero >= OMBRA[1] + 0.2 and rnd.random() < pd:
                        visto_da = k
                    if visto_da is not None and k >= visto_da + rit:
                        break
                    if st[k][1] > 0.5:
                        falso = True
                if falso:
                    falsi += 1
            print(f"  ritardo {rit} fotogrammi ({rit * DT * 1000:.0f} ms), Pd {pd}: falsa sosta {falsi}/{n} = {100.0 * falsi / n:.1f} %")
    print("  sosta al centro, lettura A e B, sigma2 0,32: istante in cui mu2 supera 0,5 per velocita' d'ingresso")
    for v in (0.5, 0.8, 1.2, 1.4):
        riga = []
        for lett in ("A", "B"):
            st = pesi(v, 140, 0.32, lett)
            tc = next((k * DT for k in range(1, 141) if st[k][1] > 0.5), None)
            riga.append(f"{lett}: {tc:.2f} s" if tc is not None else f"{lett}: mai in 9,3 s")
        print(f"   v={v}: uscita attesa {(OMBRA[1] - OMBRA[0]) / v:.2f} s; prima misura possibile con C6 "
              f"{(OMBRA[1] - OMBRA[0] + 0.2) / v:.2f} s; " + "; ".join(riga))


# ---------------------------------------------------------------- P7
def p7():
    print("== P7 (S4): sigma_eff della distribuzione uniforme sul cuneo d'ombra ==")
    for w in (0.5, 1.0, 2.0):
        a = math.atan((w / 2) / 1.8)
        n = 400
        s0 = sx = sz = sxx = szz = 0.0
        for i in range(n):
            th = -a + (i + 0.5) * 2 * a / n
            for j in range(n):
                r = 1.8 / math.cos(th) + (j + 0.5) * (R_MAX - 1.8 / math.cos(th)) / n
                dr = (R_MAX - 1.8 / math.cos(th)) / n
                da = r * dr * (2 * a / n)
                x = r * math.sin(th)
                z = r * math.cos(th)
                s0 += da
                sx += da * x
                sz += da * z
                sxx += da * x * x
                szz += da * z * z
        vx = sxx / s0 - (sx / s0) ** 2
        vz = szz / s0 - (sz / s0) ** 2
        print(f"  pannello {w:.1f} m a 1,8 m: area del cuneo {s0:.2f} m2; sigma_x {math.sqrt(vx):.2f} m, sigma_z {math.sqrt(vz):.2f} m; "
              f"raggio efficace {math.sqrt(vx + vz):.2f} m; asse maggiore {math.sqrt(max(vx, vz)):.2f} m "
              f"-> soglia 0,8 m {'MAI superata' if math.sqrt(vx + vz) <= 0.8 else 'superata'} da chi non sa niente")


# ---------------------------------------------------------------- P8
def p8():
    print("== P8 (S7): rilevamento costante e punto di massimo avvicinamento ==")
    rnd = random.Random(SEME + 8)
    emax = 0.0
    n = 0
    while n < 10000:
        rx, rz = rnd.uniform(-3, 3), rnd.uniform(0.5, 3)
        vx, vz = rnd.uniform(-2, 2), rnd.uniform(-2, 2)
        if rx * vx + rz * vz >= 0 or (vx * vx + vz * vz) < 1e-4:
            continue
        n += 1
        r2 = rx * rx + rz * rz
        vv = math.hypot(vx, vz)
        thd = abs(rx * vz - rz * vx) / r2
        tc = -(rx * vx + rz * vz) / (vv * vv)
        dc = math.hypot(rx + vx * tc, rz + vz * tc)
        rif = dc * vv / r2
        emax = max(emax, abs(thd - rif) / max(rif, 1e-12))
    print(f"  identita' |theta'| = d_CPA*|v|/r^2 su {n} coppie in avvicinamento: errore relativo massimo {emax:.2e}")
    v = 1.2
    z = 1.5
    thmax = v / z
    dentro = 1.0 / v
    print(f"  attraversamento a z={z} m, {v} m/s: |theta'| massimo {thmax:.2f} rad/s ({math.degrees(thmax):.0f} gradi/s), "
          f"d_CPA dal sensore {z:.2f} m; dentro un corridoio largo 1 m per {dentro:.2f} s")
    # soglia: quale theta' ha chi punta davvero al sensore con errore di velocita' 0,1 m/s a 2,3 m
    print(f"  rumore di theta' con errore di velocita' trasversale 0,1 / 0,2 m/s a 2,3 m: {0.1 / 2.3:.3f} / {0.2 / 2.3:.3f} rad/s")
    # bersaglio che punta al varco laterale (1,5 m a fianco del sensore), partendo da (0; 3)
    rx, rz = 0.0, 3.0
    gx, gz = 1.5, 0.0
    d = math.hypot(gx - rx, gz - rz)
    vx, vz = v * (gx - rx) / d, v * (gz - rz) / d
    thd = abs(rx * vz - rz * vx) / (rx * rx + rz * rz)
    print(f"  bersaglio da (0;3) diretto a un varco 1,5 m a fianco del sensore: |theta'| rispetto al sensore {thd:.2f} rad/s "
          f"('trasversale'), rispetto al varco 0,00 (convergente)")


# ---------------------------------------------------------------- P9
def p9():
    print("== P9 (S9): anticipo dei sensori laterali sull'ingresso nel campo frontale ==")
    v = 1.2
    for R in (0.5, 2.0):
        riga = []
        for z in (0.3, 1.0, 1.5, 2.0, 2.3):
            xc = -z * math.tan(HFOV / 2)
            if R > z:
                xt = -math.sqrt(R * R - z * z)
                ant = max(0.0, (xc - xt) / v)
            else:
                ant = 0.0
            riga.append(f"z={z}: {ant:.2f} s")
        zlim = R / math.sqrt(1 + math.tan(HFOV / 2) ** 2)
        print(f"  portata laterale {R} m: " + "; ".join(riga) + f" | anticipo > 0 solo per linee sotto {zlim:.2f} m")


PARTI = {"p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5, "p6": p6, "p6x": p6x, "p7": p7, "p8": p8, "p9": p9}

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "tutto"
    if arg == "tutto":
        for k in PARTI:
            PARTI[k]()
    else:
        PARTI[arg]()
