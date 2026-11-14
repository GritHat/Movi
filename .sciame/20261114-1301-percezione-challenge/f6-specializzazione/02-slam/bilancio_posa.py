#!/usr/bin/env python3
"""Bilancio dell'errore di posa contro le soglie del nucleo (sciame-slam, f6).

Python puro, semi fissati. Uso:  python3 bilancio_posa.py | tee risultati.txt
La regola «mobile» e' quella del codice della validazione (f4/H-012/03-validazione/sim_v2.py, righe 449 e 496-499):
due medie di 3 fotogrammi distanti 13 fotogrammi (0,867 s), soglia 5*sigma*sqrt(2)/sqrt(3) per asse, con
sigma radiale sig_r(z) e sigma trasversale sig_t(z) = z * 1 grado / sqrt(12).
Tutto cio' che segue e' un MODELLO: nessun sensore vero, nessuna posa vera.
"""
import math
import random

FPS = 15.0
DT = 1.0 / FPS
DEG = math.pi / 180.0
SEP = 13                      # fotogrammi fra i due capi (come sim_v2.py)
K = 5.0 * math.sqrt(2.0) / math.sqrt(3.0)   # 4,08 sigma
SEED = 20261114


def sig_r_cam(z):             # curva nominale del nucleo: 1,5 cm a 2 m, 3,4 cm a 3 m
    return z * z * 0.08 / (424.0 * 0.05)


def sig_t(z):                 # griglia di 1 grado
    return z * DEG / math.sqrt(12.0)


def sensore(r):
    """(sigma radiale, sigma trasversale) del centro di un gruppo a distanza r. Oltre 6 m: LiDAR, ipotesi 3 cm."""
    if r <= 6.0:
        return sig_r_cam(r), sig_t(r)
    return 0.03, sig_t(r)


def regola(xs, ys, thx, thy, k0=None, k1=None):
    """Frazione delle valutazioni con l'etichetta «mobile», e se ce n'e' almeno una."""
    n = len(xs)
    k0 = SEP + 2 if k0 is None else max(k0, SEP + 2)
    k1 = n if k1 is None else min(k1, n)
    f = 0
    tot = 0
    for k in range(k0, k1):
        dx = (xs[k] + xs[k - 1] + xs[k - 2] - xs[k - SEP] - xs[k - SEP - 1] - xs[k - SEP - 2]) / 3.0
        dy = (ys[k] + ys[k - 1] + ys[k - 2] - ys[k - SEP] - ys[k - SEP - 1] - ys[k - SEP - 2]) / 3.0
        tot += 1
        if abs(dx) > thx or abs(dy) > thy:
            f += 1
    return (f / tot if tot else 0.0), f > 0


def serie(rnd, r, n, ex, ey, t0=0.0):
    """Posizione misurata di un gruppo FERMO nel riferimento d'odometria: rumore + errore di posa apparente."""
    sr, st = sensore(r)
    xs = [rnd.gauss(0, st) + ex(t0 + k * DT) for k in range(n)]
    ys = [rnd.gauss(0, sr) + ey(t0 + k * DT) for k in range(n)]
    return xs, ys


def soglie(r, s_psi=0.0, s_tr=0.0):
    """Soglie per asse; con s_psi (rad sulla finestra) e s_tr (m sulla finestra) la sigma di posa entra in quadratura."""
    sr, st = sensore(r)
    thx = K * math.sqrt(st * st + (r * s_psi) ** 2 * 3.0 / 2.0 + s_tr * s_tr * 3.0 / 2.0)
    thy = K * math.sqrt(sr * sr + s_tr * s_tr * 3.0 / 2.0)
    return thx, thy


def zero(t):
    return 0.0


def incrocio(xs, fs, liv):
    """Primo x in cui la curva (xs, fs) supera liv, per interpolazione lineare."""
    for i in range(1, len(xs)):
        if fs[i - 1] <= liv < fs[i]:
            return xs[i - 1] + (liv - fs[i - 1]) * (xs[i] - xs[i - 1]) / (fs[i] - fs[i - 1])
    return None


def fmt(v, u=""):
    return "oltre il massimo provato" if v is None else ("%.3g%s" % (v, u))


# ---------------------------------------------------------------- S1: deriva d'imbardata e di traslazione
def s1():
    print("\n## S1  Regola «mobile» NON modificata, gruppo fermo: falsi contro la deriva relativa (N = 20 000 valutazioni)")
    print("soglia trasversale = %.2f gradi a ogni distanza (4,08 * 1 grado / radice(12))" % (K / math.sqrt(12.0)))
    griglia = [0.0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.7, 2.0, 2.6, 3.0]
    for r in (2.0, 3.0, 10.0, 30.0):
        fs = []
        for i, d in enumerate(griglia):
            rnd = random.Random(SEED + int(r * 10) * 100 + i)
            xs, ys = serie(rnd, r, 20000, lambda t, d=d: r * d * DEG * t, zero)
            thx, thy = soglie(r)
            fs.append(regola(xs, ys, thx, thy)[0])
        print("r = %4.0f m  imbardata gradi/s -> falsi: %s" % (r, "  ".join("%.1f:%.3f" % (g, f) for g, f in zip(griglia, fs))))
        print("          10 %% dei falsi a %s gradi/s; 1 %% a %s; errore sulla finestra di 0,867 s: %s gradi" % (
            fmt(incrocio(griglia, fs, 0.10)), fmt(incrocio(griglia, fs, 0.01)),
            fmt(None if incrocio(griglia, fs, 0.10) is None else incrocio(griglia, fs, 0.10) * SEP * DT)))
    print("-- traslazione (errore di velocita' lungo l'asse radiale e lungo il trasversale, m/s)")
    gr = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.15, 0.20, 0.30]
    for r in (2.0, 3.0, 10.0, 30.0):
        fr = []
        ft = []
        for i, d in enumerate(gr):
            rnd = random.Random(SEED + 7000 + int(r * 10) * 100 + i)
            thx, thy = soglie(r)
            xs, ys = serie(rnd, r, 20000, zero, lambda t, d=d: d * t)
            fr.append(regola(xs, ys, thx, thy)[0])
            xs, ys = serie(rnd, r, 20000, lambda t, d=d: d * t, zero)
            ft.append(regola(xs, ys, thx, thy)[0])
        print("r = %4.0f m  10 %% dei falsi: radiale %s m/s, trasversale %s m/s" % (
            r, fmt(incrocio(gr, fr, 0.10)), fmt(incrocio(gr, ft, 0.10))))


# ---------------------------------------------------------------- S2: soglia allargata dalla sigma di posa
def s2():
    print("\n## S2  Soglia allargata con la sigma di posa in quadratura (deriva estratta per prova da N(0, s), 400 prove x 60 fotogrammi)")
    print("r  s_psi(gradi/s)  falsi  velocita' trasversale minima vista (soglia/0,867 s)  pedone a 1,2 m/s visto  a 0,5 m/s visto")
    for r in (2.0, 3.0, 10.0, 30.0):
        for s in (0.0, 0.1, 0.3, 1.0):
            rnd = random.Random(SEED + 9000 + int(r * 10) * 10 + int(s * 10))
            sw = s * DEG * SEP * DT
            thx, thy = soglie(r, s_psi=sw)
            nf = nt = 0
            vis = {1.2: 0, 0.5: 0}
            for _ in range(400):
                d = rnd.gauss(0, s) * DEG
                xs, ys = serie(rnd, r, 60, lambda t, d=d: r * d * t, zero)
                f, _a = regola(xs, ys, thx, thy)
                nf += f
                nt += 1
                for v in vis:
                    xs, ys = serie(rnd, r, 60, lambda t, d=d, v=v: r * d * t + v * t, zero)
                    vis[v] += regola(xs, ys, thx, thy)[0]
            print("%4.0f  %4.1f  %.4f  %.3f m/s  %.3f  %.3f" % (r, s, nf / nt, thx / (SEP * DT), vis[1.2] / nt, vis[0.5] / nt))


# ---------------------------------------------------------------- S3: ritardo fra posa e profondita'
def prof_giro(t):             # 1,5 s fermo, 30 gradi a 30 gradi/s, poi fermo: partenza e arresto bruschi
    if t < 1.5:
        return 0.0
    if t < 2.5:
        return 30.0 * (t - 1.5)
    return 30.0


def prof_sin(amp, f):
    return lambda t: amp * math.sin(2 * math.pi * f * t)


def s3():
    print("\n## S3  Ritardo posa-profondita' tau: l'errore d'imbardata e' psi(t - tau) - psi(t). Falsi sul gruppo fermo.")
    taus = [0, 2, 5, 8, 10, 12, 15, 20, 25, 33, 40, 50, 67, 80, 100]
    profili = [
        ("giro 30 gradi a 30 gradi/s, brusco (rover, prova del muro)", prof_giro, True),
        ("volo stazionario +-3 gradi a 1 Hz", prof_sin(3.0, 1.0), False),
        ("busto +-8 gradi a 1 Hz (indossato al petto)", prof_sin(8.0, 1.0), False),
        ("testa +-30 gradi a 0,5 Hz (indossato sulla testa)", prof_sin(30.0, 0.5), False),
    ]
    for nome, psi, transitorio in profili:
        print("-- " + nome)
        for r in (2.0, 3.0, 10.0, 30.0):
            fs = []
            alm = []
            for i, tau in enumerate(taus):
                rnd = random.Random(SEED + 11000 + int(r * 10) * 100 + i)
                tt = tau / 1000.0
                ex = lambda t, tt=tt: r * (psi(t - tt) - psi(t)) * DEG
                thx, thy = soglie(r)
                if transitorio:
                    a = 0
                    f = 0.0
                    for _ in range(300):
                        t0 = rnd.random() * DT
                        xs, ys = serie(rnd, r, 60, ex, zero, t0)
                        ff, aa = regola(xs, ys, thx, thy, k0=22, k1=52)   # dall'inizio del giro a 1 s dopo la fine
                        f += ff
                        a += aa
                    fs.append(f / 300)
                    alm.append(a / 300)
                else:
                    xs, ys = serie(rnd, r, 9000, ex, zero)
                    fs.append(regola(xs, ys, thx, thy)[0])
            riga = "r = %4.0f m  tau al 10 %% dei falsi: %s ms" % (r, fmt(incrocio(taus, fs, 0.10)))
            if transitorio:
                riga += "   (almeno un falso nel 10 %% dei giri a tau = %s ms)" % fmt(incrocio(taus, alm, 0.10))
            print(riga + "   falsi a 0/10/20/33/67 ms: " + " ".join("%.2f" % fs[taus.index(x)] for x in (0, 10, 20, 33, 67)))
    print("-- spostamento del bordo d'ombra per il solo ritardo, omega * tau * r (conto): omega 30 / 94 gradi/s")
    for r in (2.0, 3.0, 10.0, 30.0):
        print("r = %4.0f m  tau 10 ms: %.3f / %.3f m   33 ms: %.3f / %.3f m   67 ms: %.3f / %.3f m" % (
            r, 30 * DEG * .010 * r, 94 * DEG * .010 * r, 30 * DEG * .033 * r, 94 * DEG * .033 * r,
            30 * DEG * .067 * r, 94 * DEG * .067 * r))


# ---------------------------------------------------------------- S4: sorgenti di posa (modelli d'errore ipotizzati)
def s4():
    print("\n## S4  Sorgenti di posa (modelli ipotizzati), sincronia perfetta, gruppo fermo: falsi «mobile»")
    casi = [
        ("giroscopio tarato (0,1 gradi/s, scala 1 %), giro di 30 gradi, nessuna traslazione", prof_giro, 0.1, 0.01, 0.0, 0.0, True),
        ("giroscopio NON tarato (1 grado/s), sensore fermo", lambda t: 0.0, 1.0, 0.0, 0.0, 0.0, False),
        ("rover 0,5 m/s, ruote al 3 % + giroscopio 0,1 gradi/s", lambda t: 0.0, 0.1, 0.0, 0.5, 0.03, False),
        ("rover 0,5 m/s, ruote al 10 % (slittamento) + giroscopio 0,1 gradi/s", lambda t: 0.0, 0.1, 0.0, 0.5, 0.10, False),
        ("indossato 1,2 m/s, testa +-30 gradi, giroscopio 0,1 gradi/s scala 1 %, traslazione NON compensata", prof_sin(30.0, 0.5), 0.1, 0.01, 1.2, 1.0, False),
        ("indossato 1,2 m/s, testa +-30 gradi, visuale-inerziale: 1 % della distanza, 0,1 gradi/s, scala 0", prof_sin(30.0, 0.5), 0.1, 0.0, 1.2, 0.01, False),
        ("indossato 1,2 m/s, testa +-30 gradi, visuale-inerziale: 3 % della distanza, 0,3 gradi/s", prof_sin(30.0, 0.5), 0.3, 0.0, 1.2, 0.03, False),
        ("drone 3 m/s, errore di velocita' 0,1 m/s, imbardata 0,2 gradi/s", lambda t: 0.0, 0.2, 0.0, 3.0, 0.1 / 3.0, False),
    ]
    for nome, psi, bias, scala, v, frazione, transitorio in casi:
        out = []
        for r in (2.0, 3.0, 10.0, 30.0):
            rnd = random.Random(SEED + 13000 + int(r * 10) + len(nome))
            ex = lambda t: r * (bias * t + scala * psi(t)) * DEG
            ey = lambda t: v * frazione * t
            thx, thy = soglie(r)
            if transitorio:
                f = 0.0
                for _ in range(300):
                    xs, ys = serie(rnd, r, 60, ex, ey, rnd.random() * DT)
                    f += regola(xs, ys, thx, thy, k0=22, k1=52)[0]
                out.append(f / 300)
            else:
                xs, ys = serie(rnd, r, 9000, ex, ey)
                out.append(regola(xs, ys, thx, thy)[0])
        print("%-100s 2 m: %.3f  3 m: %.3f  10 m: %.3f  30 m: %.3f" % (nome, out[0], out[1], out[2], out[3]))


# ---------------------------------------------------------------- S5: beccheggio, rimbalzo e quota del suolo
def s5():
    print("\n## S5  Quota del suolo 0,07 m: frazione delle celle di suolo «occupato» (quota > 0,07) e «non libero» (|quota| > 0,07)")
    print("sensore a 1,2 m; rumore di quota = sigma radiale * h / distanza obliqua; N = 20 000 per punto")
    h = 1.2
    gr = [0.0, 0.05, 0.08, 0.10, 0.13, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.3, 2.6, 3.0]
    for rimb in (0.0, 0.025):
        print("-- rimbalzo verticale non compensato: +-%.1f cm a 2 Hz" % (rimb * 100))
        for r in (2.0, 3.0, 10.0, 30.0):
            rho = math.hypot(r, h)
            sh = sensore(r)[0] * h / rho
            occ = []
            nl = []
            for i, d in enumerate(gr):
                rnd = random.Random(SEED + 15000 + int(r * 10) * 100 + i + int(rimb * 1000))
                o = n = 0
                N = 20000
                for _ in range(N):
                    q = r * math.sin(d * DEG) + h * (1 - math.cos(d * DEG)) + rnd.gauss(0, sh)
                    if rimb:
                        q += rimb * math.sin(2 * math.pi * rnd.random())
                    o += q > 0.07
                    n += abs(q) > 0.07
                occ.append(o / N)
                nl.append(n / N)
            print("r = %4.0f m (sigma di quota %.1f cm)  «occupato» al 10 %%: %s gradi; al 50 %%: %s gradi;  falsi a beccheggio zero: %.4f" % (
                r, sh * 100, fmt(incrocio(gr, occ, 0.10)), fmt(incrocio(gr, occ, 0.50)), nl[0]))


# ---------------------------------------------------------------- S6: copertura dell'area prevista
def s6():
    print("\n## S6  Copertura del cerchio al 95 % con uno scostamento di posa NON modellato e (in sigma), N = 200 000")
    k = math.sqrt(5.991 / (2 * 2.5257))     # sigma vera / dichiarata che da' 0,92 a scostamento zero
    R2 = 5.991
    gr = [i * 0.05 for i in range(0, 31)]
    cov = []
    rnd = random.Random(SEED + 17000)
    camp = [(rnd.gauss(0, k), rnd.gauss(0, k)) for _ in range(200000)]
    for e in gr:
        c = sum(1 for (a, b) in camp if (a + e) * (a + e) + b * b < R2)
        cov.append(c / len(camp))
    print("e/sigma -> copertura: " + "  ".join("%.2f:%.3f" % (g, c) for g, c in zip(gr, cov) if abs(g * 10 - round(g * 10)) < 1e-9))
    neg = [-c for c in cov]
    e90 = incrocio(gr, neg, -0.90)
    e85 = incrocio(gr, neg, -0.85)
    print("copertura 0,90 a e = %s sigma; 0,85 a e = %s sigma" % (fmt(e90), fmt(e85)))
    print("sigma per asse dell'area prevista (0,03 m; 0,21 m/s; q = 0,2): t -> sigma -> scostamento che porta a 0,90 -> in gradi a 2 / 3 / 10 / 30 m")
    for t in (0.67, 1.0, 2.0):
        s = math.sqrt(0.03 ** 2 + (0.21 * t) ** 2 + 0.2 * t ** 3 / 3.0)
        e = e90 * s
        print("t = %.2f s  sigma %.3f m  e = %.3f m  ->  %.2f / %.2f / %.2f / %.2f gradi sull'orizzonte t" % (
            t, s, e, e / 2 / DEG, e / 3 / DEG, e / 10 / DEG, e / 30 / DEG))
    print("con la covarianza di posa sommata (sigma_tot^2 = sigma^2 + e^2) la copertura torna >= 0,92; il raggio cresce di radice(1 + (e/sigma)^2)")


# ---------------------------------------------------------------- S7: fascia di guardia (conto)
def s7():
    print("\n## S7  Fascia di guardia 0,40 m (conto, nessun campionamento)")
    print("margine lasciato alla posa: 0,10 m (il nucleo dichiara meno di 10 cm oltre i -20 cm d'errore della maschera) e, per confronto, tutta la fascia")
    for r in (2.0, 3.0, 10.0, 30.0):
        print("r = %4.0f m  0,10 m = %.2f gradi; 0,40 m = %.2f gradi;  ritardo che consuma 0,10 m a 30 / 94 gradi/s: %.0f / %.0f ms;  griglia di 1 grado = %.2f m" % (
            r, 0.10 / r / DEG, 0.40 / r / DEG, 0.10 / r / DEG / 30 * 1000, 0.10 / r / DEG / 94 * 1000, r * DEG))
    print("fascia che scala con la distanza: f(r) = 0,40 + r * (errore d'imbardata sull'eta' della traccia pendente) + errore di traslazione")


if __name__ == "__main__":
    print("# bilancio_posa.py - seme %d - regola: medie di 3, capi a %d fotogrammi, soglia %.2f sigma" % (SEED, SEP, K))
    s1()
    s2()
    s3()
    s4()
    s5()
    s6()
    s7()
