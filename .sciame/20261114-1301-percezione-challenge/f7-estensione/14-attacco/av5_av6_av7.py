# AV5 (dopo una copertura), AV6 (errore di posa sulle celle), AV7 (ore sul calendario), piu' AV1 «dopo» con le curve di B1.
# Rifare: timeout 120 python3 -I av5_av6_av7.py > risultati_av5_av6_av7.txt
import random, math, sys, os, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim import *

# ---------------- AV5: pianta ----------------
print("AV5 — in pianta: occlusori alti A (y=1,8; x da -1,2 a -0,2) e B (y=1,8; x da 0,2 a 1,2); soggetto nascosto dietro A a (-0,7; 2,3);")
print("      sensore coperto per T s; il soggetto cammina a 1,2 m/s verso B e si ferma a (0,7; 2,3); poi 60 fotogrammi. v_max = 1,4 m/s, fascia 0,40 m")
OCCL = {"A": (-1.2, -0.2), "B": (0.2, 1.2)}
YO = 1.8


def nascosto_da(x, y):
    if y <= YO:
        return None
    xs = x * YO / y
    for n, (a, b) in OCCL.items():
        if a <= xs <= b:
            return n
    return None


def in_campo(x, y):  # griglia 87 gradi, anello cieco sotto 1,24 m
    r = math.hypot(x, y)
    return 1.24 <= r < 3.0 and abs(math.degrees(math.atan2(x, y))) < 43.5


celle = [(a, r) for a in range(NA) for r in range(NR)]
cc = {c: centro_cella(c[0], c[1], 0)[:2] for c in celle}
nasc = {c: nascosto_da(*cc[c]) for c in celle}
cuneoA = [c for c in celle if nasc[c] == "A"]
reg0 = set(c for c in celle if any(math.hypot(cc[c][0] - cc[d][0], cc[c][1] - cc[d][1]) <= 0.40 for d in cuneoA[::3]) or nasc[c] == "A")
non_oss = set(c for c in celle if nasc[c] is not None or not in_campo(*cc[c]))
print("celle: cuneo di A %d ; regione alla nascita (cuneo + fascia) %d ; non osservate in tutto %d su %d" % (len(cuneoA), len(reg0), len(non_oss), len(celle)))
for T in (0.5, 1.0, 2.0):
    xs = min(0.7, -0.7 + 1.2 * T)
    pos = (xs, 2.3)
    c_s = cella_di(*pos)
    visibile = nasc[c_s] is None
    # regola scritta: la regione resta (localizzata = no) e perde, in 3 fotogrammi, le celle col suolo visto libero
    reg_scritta = set(c for c in reg0 if c in non_oss)
    # riga riscritta: regione dilatata di v_max*T + fascia, intersecata col non osservato
    R = 1.4 * T + 0.40
    seme = [cc[c] for c in list(reg0)[::4]]
    reg_nuova = set(c for c in non_oss if any(math.hypot(cc[c][0] - s[0], cc[c][1] - s[1]) <= R for s in seme))
    fuori_s = 0 if (visibile or c_s in reg_scritta) else 60
    fuori_n = 0 if (visibile or c_s in reg_nuova) else 60
    print("T=%.1f s: soggetto a (%.2f; 2,3), %s | regola scritta: %d celle, soggetto fuori regione in %d/60 | riscritta: %d celle (%.0f %% del non osservato), fuori in %d/60 | cicli senza uscita durante la copertura (lettura letterale di «esci»): %d" % (
        T, xs, "IN VISTA (fra A e B): sarebbe riagganciato o 'identita' ambigua'" if visibile else "nascosto dietro " + str(nasc[c_s]),
        len(reg_scritta), fuori_s, len(reg_nuova), 100.0 * len(reg_nuova) / len(non_oss), fuori_n, round(T * 15)))

# ---------------- AV6: posa ----------------
print()
print("AV6 — posa: camera creduta a 15 gradi, vera a 15+e; trave a terra larga 1 m a 2,8-2,9 m; k=0,004; 10 valutazioni; centro delle celle a 0,10 m")
print("trave(h)  e(gradi)  celle_nella_pianta  LIBERO_per_stato/fot  LIBERO_e_non_occupate_dai_pixel/fot  mediana_quota_ricostruita_del_suolo_2-3m(cm)")
K = 0.004
for hb, etich in ((0.12, ""), (0.10, " [dopo]"), (0.15, " [dopo]")):
    trave = (-0.5, 0.5, 2.8, 2.9, 0.0, hb)
    dentro = [c for c in celle if -0.5 <= cc[c][0] <= 0.5 and 2.8 <= cc[c][1] <= 2.9]
    for e in (0.0, -1.0, 1.0, -2.0, 2.0):
        if etich and abs(e) > 1.0 and hb != 0.15:
            continue
        clean, ID = render([trave], 15.0 + e, 6.0, True)
        rng = random.Random(600 + int(10 * e) + int(100 * hb))
        fr = [rumoroso(clean, ID, K, rng) for _ in range(12)]
        nl = nn = 0
        for t in range(2, 12):
            Ds = [fr[t], fr[t - 1], fr[t - 2]]
            occ, suo, r0 = griglia_pixel(fr[t], 15.0)
            for c in dentro:
                if stato(Ds, centro_cella(c[0], c[1], 0.10), K, 15.0) == LIBERO:
                    nl += 1
                    if occ[c[0]][c[1]] < 3 and c[1] <= r0[c[0]]:
                        nn += 1
        qs = []
        D = fr[-1]
        for j in range(0, H, 2):
            for i in range(0, W, 2):
                d = D[j * W + i]
                if d == 0.0 or ID[j * W + i] != -2:
                    continue
                p = punto(i, j, d, 15.0)
                if 2.0 <= math.hypot(p[0], p[1]) <= 3.0:
                    qs.append(p[2])
        print("%.2f%-8s %+.1f     %3d                 %5.1f                 %5.1f                               %+.1f" % (hb, etich, e, len(dentro), nl / 10, nn / 10, 100 * statistics.median(qs)))

# ---------------- AV1 «dopo»: le curve di rumore scritte nel blocco B1 del nucleo ----------------
print()
print("AV1 [dopo, senza previsione] — resa di stato(centro) con le tre curve di rumore del blocco B1 del nucleo (a 2 m: 1,5 / 4 / 5 cm => k = 0,00375 / 0,0100 / 0,0125)")
clean, ID = render([], 15.0, 6.0, True)
for k in (0.00375, 0.0100, 0.0125):
    rng = random.Random(707)
    fr = [rumoroso(clean, ID, k, rng) for _ in range(6)]
    riga = []
    for hq in (0.10, 0.15, 0.20, 0.30):
        tot = lib = 0
        for t in range(2, 6):
            Ds = [fr[t], fr[t - 1], fr[t - 2]]
            for a in range(NA):
                for r in range(13, NR):
                    s = stato(Ds, centro_cella(a, r, hq), k)
                    if s != FUORI:
                        tot += 1
                        lib += s == LIBERO
        riga.append("quota %.2f: %5.1f %%" % (hq, 100.0 * lib / tot))
    print("k=%.5f  %s" % (k, " | ".join(riga)))

# ---------------- AV7: ore ----------------
print()
print("AV7 — ore sul calendario (dati: SOLUZIONE_V2 par. 2, AUDIT ipotesi 8, DECISIONE par. 1.9, settimo addendum). Stime altrui, non verificate.")
B = dict(B1=3, B2=6, B3=6, B4=5, B5=9, B6=4, B7=3, B8=6, B9=12)
print("somma dei blocchi %d ; catena B1..B5,B7,B8 %d ; senza B1 %d" % (sum(B.values()), sum(B[x] for x in "B1 B2 B3 B4 B5 B7 B8".split()), sum(B[x] for x in "B2 B3 B4 B5 B7 B8".split())))
acc_orol, acc_pers = 2 + 40 / 60, 2
for sens in (5.0, 6.0):
    for pers in (5, 4):
        t_int = 14 - acc_orol  # ora entro cui la catena deve essere integrata sul sensore vero
        cap = pers * t_int
        b9_resto = B["B9"] - acc_orol * acc_pers
        sviluppo = sum(B[x] for x in "B2 B3 B4 B5 B7 B8".split())
        for f7 in (8.0, 10.5):
            resto = cap - B["B1"] - b9_resto - sviluppo - f7
            print("sensore all'ora %.0f, %d persone: integrazione entro l'ora %.2f ; capienza fino a li' %.1f ; B1 %d + resto di B9 %.1f + B2..B8 %d + f7 %.1f => restano per f8 e integrazione %.1f ore-persona (la decisione: 9,5-12)" % (
                sens, pers, t_int, cap, B["B1"], b9_resto, sviluppo, f7, resto))
        print("   ore d'orologio fra l'arrivo del sensore e l'inizio dell'accettazione: %.2f (dentro: B1 %d h, taratura, registrazioni, prima prova della catena sui dati veri)" % (t_int - sens, B["B1"]))
print("rami indipendenti necessari perche' B2..B8 (35 h in fila) stia in 11,33 h d'orologio: %.1f" % (35 / (14 - acc_orol)))
