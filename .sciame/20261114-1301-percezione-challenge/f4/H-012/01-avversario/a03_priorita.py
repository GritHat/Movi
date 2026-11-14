# Attacco 3: la tabella delle priorita' di B7 e l'anello cieco vicino.
from comune_f4 import *

H, TILT, VFOV = 1.2, 15.0, 58.0
basso = math.radians(TILT + VFOV / 2)
alto = math.radians(VFOV / 2 - TILT)
print("Attacco 3. Camera a %.1f m, %.0f gradi in basso, %.0f gradi in verticale." % (H, TILT, VFOV))
print("Raggio piu' basso: -%.0f gradi; primo suolo visto a %.3f m" % (math.degrees(basso), H / math.tan(basso)))
for h in (0.07, 0.15, 0.30, 0.50):
    print("  ostacolo alto %.2f m: visibile solo oltre %.3f m" % (h, (H - h) / math.tan(basso)))
print("Scatola alta 0,15 m, 5 prove a 0,8 m: quota piu' bassa vista a 0,8 m = %.3f m -> viste %d su 5" % (
    H - 0.8 * math.tan(basso), 5 if 0.15 > H - 0.8 * math.tan(basso) else 0))
viste = [d for d in (0.5, 1.125, 1.75, 2.375, 3.0) if 0.15 > H - d * math.tan(basso)]
print("Scatola alta 0,15 m a 0,5 / 1,125 / 1,75 / 2,375 / 3,0 m: viste %d su 5 (%s)" % (len(viste), viste))
print("Quota dell'estensione radiale 0,5-3 m senza suolo visto: %.0f %%" % (100 * (RNEAR - 0.5) / 2.5))

# Settore centrale di 10 gradi, celle 1 grado x 0,1 m fra 0,5 e 3 m. Persona larga 0,4 m che si avvicina a 1,4 m/s da 3 a 1 m.
GRAV = ['non osservato', 'mobile in avvicinamento', 'occupato', 'previsto', 'perso con possibile presenza', 'libero']


def messaggi(rp, rng, p_suolo):
    half = math.atan(0.2 / rp)
    stati = {}
    for bi in range(-5, 5):
        b = math.radians(bi + 0.5)
        for ri in range(5, 30):
            r = ri / 10 + 0.05
            if abs(b) <= half and abs(r - rp) < 0.05:
                st = 'mobile in avvicinamento'
            elif abs(b) <= half and r > rp:
                st = 'in ombra'
            elif r < RNEAR:
                st = 'non osservato'  # suolo non visto: anello cieco
            else:
                st = 'libero' if rng.random() < p_suolo else 'non osservato'  # buco
            stati[(bi, ri)] = st
    # lettura A: il piu' grave fra tutte le celle del settore (alla lettera)
    A = min((GRAV.index(s) for s in stati.values() if s in GRAV), default=5)
    # lettura B: per direzione, la prima cella non libera partendo da 0,5 m; poi il piu' grave fra le direzioni
    primi = []
    for bi in range(-5, 5):
        for ri in range(5, 30):
            if stati[(bi, ri)] != 'libero':
                primi.append(stati[(bi, ri)])
                break
    B = min((GRAV.index(s) for s in primi if s in GRAV), default=5)
    # lettura C (correzione): anello cieco e oltre portata dichiarati una volta e tolti dal messaggio per fotogramma
    # (corretto dopo la prima esecuzione: una persona DENTRO l'anello resta vista e va detta; prima la toglievo per errore mio)
    C = min((GRAV.index(s) for (k, s) in stati.items()
             if s in GRAV and (k[1] / 10 + 0.05 >= RNEAR or s != 'non osservato')), default=5)
    return GRAV[A], GRAV[B], GRAV[C]


rng = random.Random(SEME + 3)
print()
print("Persona in avvicinamento (gia' etichettata 'mobile': ipotesi generosa), 22 fotogrammi da 3,0 a 1,0 m")
print("p_suolo  lettura A (alla lettera)  lettura B (prima cella non libera)  lettura C (anello tolto)  -> quota di fotogrammi con 'mobile in avvicinamento'")
for p in (1.0, 0.99, 0.95):
    cnt = [0, 0, 0]
    n = 0
    for rip in range(200):
        rp = 3.0
        while rp > 1.0:
            m = messaggi(rp, rng, p)
            for i in range(3):
                cnt[i] += m[i] == 'mobile in avvicinamento'
            n += 1
            rp -= 1.4 * DT
    print("%5.2f     %5.1f %%                   %5.1f %%                             %5.1f %%" % (
        p, 100 * cnt[0] / n, 100 * cnt[1] / n, 100 * cnt[2] / n))
print("(con p_suolo < 1 la colonna C e' l'interazione con l'attacco 9: [notato dopo], non era nella previsione)")
