# AV1 — stato(centro) come fonte del «libero» delle celle: quota del centro e rumore.
# Rifare: timeout 120 python3 -I av1.py > risultati_av1.txt
import random, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim import *

NF = 12  # 12 fotogrammi, 10 valutazioni (t = 2..11)


def serie(clean, ID, k, seme, nulli=()):
    rng = random.Random(seme)
    return [rumoroso(clean, ID, k, rng, nulli) for _ in range(NF)]


def celle_zona():
    return [(a, r) for a in range(NA) for r in range(13, NR)]  # centri da 1,35 a 2,95 m


print("AV1 — resa di stato(centro) sulle celle, stanza vuota 6x4x3, 10 valutazioni, centri 1,35-2,95 m")
clean, ID = render([], 15.0, 6.0, True)
print("quota_centro  k        celle_in_campo  resa_%   resa_1,3-1,8m  resa_1,8-2,4m  resa_2,4-3,0m  libero_piu_lontano_m")
for k in (0.004, 0.0095):
    fr = serie(clean, ID, k, 101)
    for hq in (0.00, 0.05, 0.10, 0.30):
        tot = lib = 0
        fasce = [[0, 0], [0, 0], [0, 0]]
        lontano = 0.0
        for t in range(2, NF):
            Ds = [fr[t], fr[t - 1], fr[t - 2]]
            for (a, r) in celle_zona():
                p = centro_cella(a, r, hq)
                s = stato(Ds, p, k)
                if s == FUORI:
                    continue
                tot += 1
                rr = (r + 0.5) * 0.1
                f = 0 if rr < 1.8 else (1 if rr < 2.4 else 2)
                fasce[f][1] += 1
                if s == LIBERO:
                    lib += 1
                    fasce[f][0] += 1
                    lontano = max(lontano, rr)
        print("%.2f          %.4f   %6d          %5.1f    %5.1f          %5.1f          %5.1f          %.2f" % (
            hq, k, tot // (NF - 2), 100.0 * lib / tot, *[100.0 * x[0] / max(1, x[1]) for x in fasce], lontano))

print()
print("AV1b — scatola bassa: celle col centro nella pianta date per LIBERO da stato(centro a quota hq)")
print("scatola(h)  hq    k       celle_nella_pianta  LIBERO_per_stato(media/fot)  di_cui_non_occupate_dai_pixel(>=3 px quota 0,07-2)")
for hb in (0.10, 0.25):
    box = (-0.2, 0.2, 2.0, 2.3, 0.0, hb)
    clean, ID = render([box], 15.0, 6.0, True)
    for k in (0.004, 0.0095):
        fr = serie(clean, ID, k, 202)
        for hq in (0.10, 0.30):
            dentro = [(a, r) for a in range(NA) for r in range(NR)
                      if -0.2 <= centro_cella(a, r, 0)[0] <= 0.2 and 2.0 <= centro_cella(a, r, 0)[1] <= 2.3]
            nl = nn = 0
            for t in range(2, NF):
                Ds = [fr[t], fr[t - 1], fr[t - 2]]
                occ, suo, r0 = griglia_pixel(fr[t])
                for (a, r) in dentro:
                    if stato(Ds, centro_cella(a, r, hq), k) == LIBERO:
                        nl += 1
                        if occ[a][r] < 3:
                            nn += 1
            print("%.2f        %.2f  %.4f  %3d                 %6.1f                       %6.1f" % (hb, hq, k, len(dentro), nl / (NF - 2), nn / (NF - 2)))

print()
print("AV1c — corpo che non rimanda segnale (0,45x0,25x1,75 a 2 m, pixel non validi), hq=0,10, k=0,004")
corpo = (-0.225, 0.225, 2.0, 2.25, 0.0, 1.75)
clean, ID = render([corpo], 15.0, 6.0, True)
fr = serie(clean, ID, 0.004, 303, nulli=(0,))
dentro = [(a, r) for a in range(NA) for r in range(NR)
          if -0.225 <= centro_cella(a, r, 0)[0] <= 0.225 and 2.0 <= centro_cella(a, r, 0)[1] <= 2.25]
ombra = [(a, r) for a in range(NA) for r in range(NR)
         if centro_cella(a, r, 0)[1] > 2.25 and abs(centro_cella(a, r, 0)[0]) <= 0.225 * centro_cella(a, r, 0)[1] / 2.25 - 0.03]
tot_d = tot_o = 0
perfot = []
for t in range(2, NF):
    Ds = [fr[t], fr[t - 1], fr[t - 2]]
    nd = sum(1 for (a, r) in dentro if stato(Ds, centro_cella(a, r, 0.10), 0.004) == LIBERO)
    no = sum(1 for (a, r) in ombra if stato(Ds, centro_cella(a, r, 0.10), 0.004) == LIBERO)
    tot_d += nd
    tot_o += no
    perfot.append((nd, no))
print("celle nella pianta del corpo: %d ; nell'ombra al suolo dietro il corpo: %d" % (len(dentro), len(ombra)))
print("LIBERO nella pianta: %d in 10 fotogrammi ; LIBERO nell'ombra: %d in 10 fotogrammi ; per fotogramma %s" % (tot_d, tot_o, perfot))
# la stessa prova con la sola memoria del nucleo (suolo visto in uno degli ultimi 3 fotogrammi) non serve qui: il corpo e' fermo.
# variante: il corpo ENTRA (assente nei due fotogrammi precedenti): e' il caso «dato vecchio contro occlusione nuova»
clean0, ID0 = render([], 15.0, 6.0, True)
rng = random.Random(404)
f_prima = [rumoroso(clean0, ID0, 0.004, rng) for _ in range(2)]
f_ora = rumoroso(clean, ID, 0.004, rng, nulli=(0,))
Ds = [f_ora, f_prima[1], f_prima[0]]
nd = sum(1 for (a, r) in dentro if stato(Ds, centro_cella(a, r, 0.10), 0.004) == LIBERO)
no = sum(1 for (a, r) in ombra if stato(Ds, centro_cella(a, r, 0.10), 0.004) == LIBERO)
# braccio di controllo: la sola memoria «libero in uno degli ultimi 3» senza clausola
nd0 = sum(1 for (a, r) in dentro if any(leggi(D, centro_cella(a, r, 0.10), 0.004) == LIBERO for D in Ds))
no0 = sum(1 for (a, r) in ombra if any(leggi(D, centro_cella(a, r, 0.10), 0.004) == LIBERO for D in Ds))
print("corpo che compare ora (i due fotogrammi prima vuoti): stato() LIBERO nella pianta %d, nell'ombra %d ; braccio di controllo senza clausola: %d e %d" % (nd, no, nd0, no0))
