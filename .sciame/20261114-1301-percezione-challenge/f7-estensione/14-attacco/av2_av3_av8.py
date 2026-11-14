# AV2 (barra nella colonna), AV3 (senza fondale), AV8 (pannello e frase «piu' alto del sensore»).
# Rifare: timeout 120 python3 -I av2_av3_av8.py > risultati_av2_av3_av8.txt
import random, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim import *

K = 0.004
NF = 12

print("AV2 — barra 1,40-1,50 m di quota, larga 1,2 m, a 2,0-2,1 m; stanza 6x4x3; k=0,004; 10 valutazioni")
barra = (-0.6, 0.6, 2.0, 2.1, 1.40, 1.50)
clean, ID = render([barra], 15.0, 6.0, True)
rng = random.Random(11)
fr = [rumoroso(clean, ID, K, rng) for _ in range(NF)]
pix_barra = sum(1 for n in range(W * H) if ID[n] == 0 and fr[-1][n] != 0.0)
colonna = [(a, r) for a in range(NA) for r in range(NR)
           if -0.6 <= centro_cella(a, r, 0)[0] <= 0.6 and 2.0 <= centro_cella(a, r, 0)[1] <= 2.1]
print("pixel validi sulla barra: %d ; tetto del campo a 2 m: %.2f m ; celle col centro sotto la barra: %d" % (pix_barra, 1.2 + math.tan(math.radians(14)) * 2.0, len(colonna)))
tl = to = tomb = 0
for t in range(2, NF):
    Ds = [fr[t], fr[t - 1], fr[t - 2]]
    occ, suo, r0 = griglia_pixel(fr[t])
    lib = [(a, r) for (a, r) in colonna if stato(Ds, centro_cella(a, r, 0.10), K) == LIBERO]
    tl += len(lib)
    to += sum(1 for (a, r) in lib if occ[a][r] < 3 and r <= r0[a])
    # celle oltre il primo ritorno il cui suolo e' davvero visto (stato del centro LIBERO): escono «in ombra»
    tomb += sum(1 for a in range(NA) for r in range(13, NR) if r > r0[a] and stato(Ds, centro_cella(a, r, 0.10), K) == LIBERO)
n = NF - 2
print("lettura letterale «cella libera <=> stato(centro)»: celle sotto la barra date per libere: %.1f a fotogramma su %d" % (tl / n, len(colonna)))
print("lettura «occupato dai pixel e ombra oltre il primo ritorno vincono»: celle sotto la barra ancora libere: %.1f a fotogramma" % (to / n))
print("con questa lettura, celle col suolo davvero visto (stato LIBERO) che escono «in ombra» oltre la barra: %.1f a fotogramma" % (tomb / n))
# la colonna sopra una cella libera e' verificata fino al tetto? quota piu' alta LIBERO sopra una cella sotto la barra
Ds = [fr[-1], fr[-2], fr[-3]]
for (x, y) in ((0.0, 2.05), (0.0, 1.6), (0.0, 2.6)):
    riga = []
    for q in range(1, 40):
        riga.append(stato(Ds, (x, y, q * 0.05), K))
    print("colonna a (x=%.1f, y=%.2f), quote 0,05..1,95 passo 0,05: %s" % (x, y, "".join(riga)))

print()
print("AV3 — senza fondale: solo il suolo, nessuna parete; k=0,004")
for zmax in (6.0, 10.0):
    clean, ID = render([], 15.0, zmax, False)
    rng = random.Random(22)
    fr = [rumoroso(clean, ID, K, rng) for _ in range(3)]
    nonval = sum(1 for v in fr[0] if v == 0.0) / (W * H)
    Ds = [fr[2], fr[1], fr[0]]
    out = []
    for d in (2.0, 3.0):
        hmax = 0.0
        riga = ""
        for q in range(1, 40):
            s = stato(Ds, (0.0, d, q * 0.05), K)
            riga += s
            if s == LIBERO:
                hmax = q * 0.05
        out.append((d, hmax, 1.2 + math.tan(math.radians(14)) * d, riga))
    print("portata valida %.0f m: pixel non validi %.1f %%" % (zmax, 100 * nonval))
    for (d, hmax, tetto, riga) in out:
        print("  d=%.0f m: quota piu' alta con stato()==LIBERO %.2f m ; la frase dichiara %.2f m ; colonna 0,05..1,95: %s" % (d, hmax, tetto, riga))
    # resa sulle celle (centro a 0,10) senza fondale
    tot = lib = 0
    for a in range(NA):
        for r in range(13, NR):
            s = stato(Ds, centro_cella(a, r, 0.10), K)
            if s != FUORI:
                tot += 1
                lib += s == LIBERO
    print("  resa sulle celle (centro a 0,10 m): %.1f %% di %d" % (100.0 * lib / tot, tot))

print()
print("AV8 — pannello largo 1 m a 1,70-1,75 m; soggetto 0,45x0,25x1,75 a 2,3 m, centrato; pixel validi del soggetto (senza rumore)")
sogg = (-0.225, 0.225, 2.3, 2.55, 0.0, 1.75)
for hp in (1.30, 1.50, 1.60, 1.65, 1.70):
    pann = (-0.5, 0.5, 1.70, 1.75, 0.0, hp)
    clean, ID = render([pann, sogg], 15.0, 6.0, True)
    n = sum(1 for k in range(W * H) if ID[k] == 1 and clean[k] != 0.0)
    # quota minima e massima dei pixel del soggetto
    qs = [punto(k % W, k // W, clean[k])[2] for k in range(W * H) if ID[k] == 1 and clean[k] != 0.0]
    print("pannello alto %.2f m: pixel del soggetto %5d ; quote viste %s" % (hp, n, ("%.2f-%.2f m" % (min(qs), max(qs))) if qs else "-"))
for hs in (1.90,):
    pann = (-0.5, 0.5, 1.70, 1.75, 0.0, 1.70)
    clean, ID = render([pann, (-0.225, 0.225, 2.3, 2.55, 0.0, hs)], 15.0, 6.0, True)
    print("pannello 1,70 m, soggetto alto %.2f m: pixel %d" % (hs, sum(1 for k in range(W * H) if ID[k] == 1 and clean[k] != 0.0)))
pann = (-0.5, 0.5, 1.90, 1.95, 0.0, 1.70)
for ys in (2.3, 2.8):
    clean, ID = render([pann, (-0.225, 0.225, ys, ys + 0.25, 0.0, 1.90)], 15.0, 6.0, True)
    print("pannello 1,70 m a 1,90 m, soggetto 1,90 m a %.1f m: pixel %d" % (ys, sum(1 for k in range(W * H) if ID[k] == 1 and clean[k] != 0.0)))
