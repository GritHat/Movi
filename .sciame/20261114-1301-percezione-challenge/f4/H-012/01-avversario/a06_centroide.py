# Attacco 6a (centroide che scivola su un oggetto fermo) e 6b (gruppo che si fonde con il pannello).
import sys
from comune_f4 import *

quale = sys.argv[1]

if quale == 'a':
    rng = random.Random(SEME + 61)
    print("Attacco 6a. Muro largo 1 m a 2 m (fermo); una persona larga 0,4 m passa davanti a 1 m. Primo ritorno per direzione.")
    print("Regola 'mobile': spostamento del centro su una finestra <= 1 s oltre 5*sigma*sqrt(2). 500 passaggi per riga.")

    def passaggio(sig_t, porta, con_persona, escludi_troncati):
        v = min(1.6, max(0.8, rng.gauss(1.2, 0.15)))
        thr = 5 * sig_t * math.sqrt(2)
        nf = int(2.4 / v / DT) + 30
        pos = None
        storia = []
        mobile = False
        for k in range(nf):
            xp = -1.2 + v * (k - 15) * DT
            pezzi = []
            if con_persona:
                sa, sb = 2 * (xp - 0.2), 2 * (xp + 0.2)
                if sa > -0.5:
                    pezzi.append((-0.5, min(0.5, sa)))
                if sb < 0.5:
                    pezzi.append((max(-0.5, sb), 0.5))
                if sa <= -0.5 and sb >= 0.5:
                    pezzi = []
            else:
                pezzi = [(-0.5, 0.5)]
            gruppi = [((a + b) / 2 + rng.gauss(0, sig_t), (b - a) < 0.99) for (a, b) in pezzi if b - a >= 0.1]
            if not gruppi:
                continue
            if pos is None:
                c, tr = gruppi[0]
            else:
                c, tr = min(gruppi, key=lambda g: abs(g[0] - pos))
                if abs(c - pos) > porta:
                    continue
            pos = c
            if escludi_troncati and tr:
                continue
            for (j, cj) in storia:
                if k - j <= 15 and abs(c - cj) > thr:
                    mobile = True
            storia.append((k, c))
        return mobile

    for sig_t in (0.05, 0.015):
        for porta in (1.0, 0.3):
            a = quota(passaggio(sig_t, porta, True, False) for _ in range(500))
            b = quota(passaggio(sig_t, porta, False, False) for _ in range(500))
            c = quota(passaggio(sig_t, porta, True, True) for _ in range(500))
            print("sigma trasversale %.3f m, porta %.1f m: falso 'mobile' sul muro %5.1f %% | controllo senza persona %5.1f %% | [correzione] gruppi troncati da un'ombra esclusi dalla finestra %5.1f %%" % (
                sig_t, porta, a, b, c))

if quale == 'b':
    rng = random.Random(SEME + 62)
    print("Attacco 6b. Pannello 0,5 m a 1,5 m; una persona larga 0,4 m cammina verso il sensore sfiorando il bordo del pannello (scarto laterale = gap).")
    print("Celle 1 grado x 0,1 m, primo ritorno per direzione. Stretta: celle a contatto (8 vicini). Larga: fino a 2 celle di scarto. 100 passaggi per riga.")

    def passaggio(gap, sig_r, toll):
        v = min(1.6, max(0.8, rng.gauss(1.2, 0.15)))
        xpc = 0.25 + gap + 0.2
        zc = 2.5 + rng.uniform(0, v * DT)
        fusi = 0
        while zc > 0.8:
            primo = {}
            for i in range(101):
                for (obj, x, z) in (('P', -0.25 + 0.5 * i / 100, 1.5), ('U', xpc - 0.2 + 0.4 * i / 100, zc)):
                    bi = math.floor(math.degrees(math.atan2(x, z)))
                    r = math.hypot(x, z)
                    if bi not in primo or r < primo[bi][0]:
                        primo[bi] = (r, obj)
            celle = {}
            for bi, (r, obj) in primo.items():
                celle[bi] = (int((r + rng.gauss(0, sig_r)) * 10), obj)
            f = False
            for bi, (ri, obj) in celle.items():
                if obj != 'P':
                    continue
                for db in range(-toll, toll + 1):
                    o = celle.get(bi + db)
                    if o and o[1] == 'U' and abs(o[0] - ri) <= toll:
                        f = True
            fusi += f
            zc -= v * DT
        return fusi

    for gap in (0.02, 0.05, 0.10, 0.15, 0.25):
        for sig_r in (0.0, 0.05):
            out = []
            for toll in (1, 2):
                rs = [passaggio(gap, sig_r, toll) for _ in range(100)]
                out.append("%s: >= 1 fotogramma fusi %5.1f %%, >= 3 fotogrammi %5.1f %%" % (
                    'stretta' if toll == 1 else 'larga', quota(r >= 1 for r in rs), quota(r >= 3 for r in rs)))
            print("gap %.2f m, rumore radiale %.2f m | %s | %s" % (gap, sig_r, out[0], out[1]))
