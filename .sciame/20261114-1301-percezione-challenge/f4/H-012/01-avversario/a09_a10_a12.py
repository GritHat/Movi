# Attacco 9 (libero senza memoria), 10 (affidabilita' persa), 12 (aree: camera e ToF laterali).
import sys
from comune_f4 import *

quale = sys.argv[1]

if quale == 'a9':
    rng = random.Random(SEME + 9)
    NF, NC = 900, 18
    print("Attacco 9. Suolo valido con probabilita' p per cella e fotogramma, indipendente (modello MIO, non di scheda). 18 celle fra 1,24 e 3 m, 60 s a 15 Hz.")
    print("'isteresi' = [correzione] una cella diventa buco solo dopo 3 fotogrammi non validi di fila (il libero resta 'visto' con eta' <= 0,2 s).")
    for p in (0.99, 0.95, 0.8, 0.0):
        for nome, nb, ist in (("una direzione", 1, False), ("settore di 10 direzioni", 10, False),
                              ("una direzione, isteresi", 1, True), ("settore, isteresi", 10, True)):
            manc = [[0] * NC for _ in range(nb)]
            pieni = camb = cambq = 0
            prec = precq = None
            for f in range(NF):
                d = NC
                for b in range(nb):
                    for c in range(NC):
                        if rng.random() < p:
                            manc[b][c] = 0
                        else:
                            manc[b][c] += 1
                for c in range(NC):
                    if any((manc[b][c] >= (3 if ist else 1)) for b in range(nb)):
                        d = c
                        break
                dist = RNEAR + 0.1 * d
                dq = int(dist / 0.5)
                pieni += d == NC
                camb += prec is not None and d != prec
                cambq += precq is not None and dq != precq
                prec, precq = d, dq
            print("  p %.2f, %-26s 'fino a 3 m' nel %5.1f %% dei fotogrammi; distanza annunciata: %5.2f cambi/s (a passi di 0,5 m: %5.2f cambi/s)" % (
                p, nome + ":", 100 * pieni / NF, camb / 60, cambq / 60))
    print("Rilascio dello strato 1 per osservazione, zona di 50 celle (60 s al piu'):")
    for p in (0.99, 0.95, 0.8):
        cons = [0] * 50
        fatto = [False] * 50
        t_ind = t_ins = None
        ins = 0
        for f in range(NF):
            tutti = True
            for c in range(50):
                if rng.random() < p:
                    cons[c] += 1
                    if cons[c] >= 3:
                        fatto[c] = True
                else:
                    cons[c] = 0
                    tutti = False
            ins = ins + 1 if tutti else 0
            if t_ind is None and all(fatto):
                t_ind = (f + 1) * DT
            if t_ins is None and ins >= 3:
                t_ins = (f + 1) * DT
        print("  p %.2f: cella per cella %s; tutte insieme per 3 fotogrammi %s" % (
            p, "%.2f s" % t_ind if t_ind else "mai", "%.2f s" % t_ins if t_ins else "mai in 60 s"))

if quale == 'a10':
    rng = random.Random(SEME + 10)
    print("Attacco 10. Regole di B8 alla lettera: 'affidabilita' persa' se (1) il contatore non avanza in un ciclo, o (2) tre fotogrammi di profondita' identici.")

    def segnale(flusso, quale_contatore):
        ult = None
        ident = 0
        prec = None
        for k, (cd, cr, cont) in enumerate(flusso):
            cnt = cd if quale_contatore == 'profondita' else cr
            if ult is not None and cnt == ult:
                return k * DT
            ult = cnt
            ident = ident + 1 if (prec is not None and cont == prec) else 0
            prec = cont
            if ident >= 2:
                return k * DT
        return None

    def rumore(valida):
        return tuple((rng.randint(500, 3000) if rng.random() < valida else 0) for _ in range(64))

    fermo = rumore(1.0)
    flussi = {
        "(a) profondita' valida al 10 %, rumore nel resto": [(k, k, rumore(0.10)) for k in range(45)],
        "(a') lente coperta del tutto: tutti zeri [controllo, notato dopo]": [(k, k, tuple([0] * 64)) for k in range(45)],
        "(b) profondita' ferma (contatore e contenuto), RGB vivo": [(0, k, fermo) for k in range(45)],
        "(c) treppiede urtato: fotogrammi nuovi e diversi": [(k, k, rumore(1.0)) for k in range(45)],
        "(d1) nessun fotogramma nuovo [controllo]": [(0, 0, fermo) for k in range(45)],
        "(d2) fotogramma ripetuto con contatore nuovo [controllo]": [(k, k, fermo) for k in range(45)],
    }
    for nome, fl in flussi.items():
        out = []
        for qc in ('profondita', 'rgb o coppia'):
            t = segnale(fl, 'profondita' if qc == 'profondita' else 'rgb')
            out.append("contatore %s: %s" % (qc, ("segnale a %.2f s" % t) if t is not None else "NESSUN segnale in 3 s"))
        print("  %-66s %s | %s" % (nome, out[0], out[1]))
    print("  (c) beccheggio di 2 gradi: il pavimento supera la soglia di 7 cm oltre %.2f m; di 1 grado: oltre %.2f m" % (
        0.07 / math.tan(math.radians(2)), 0.07 / math.tan(math.radians(1))))
    print("  (c) imbardata di 10 gradi in 0,2 s: gruppi FERMI etichettati 'mobile' nei 1,2 s seguenti (500 prove per cella, finestra <= 1 s)")
    for sig_t in (0.05, 0.015):
        thr = 5 * sig_t * math.sqrt(2)
        riga = []
        for r in (1.5, 2.0, 2.5, 3.0):
            n = 0
            for _ in range(500):
                storia = []
                mob = False
                for k in range(33):
                    yaw = math.radians(10) * min(1.0, max(0.0, (k - 15) / 3))
                    x = r * math.sin(yaw) + rng.gauss(0, sig_t)
                    for (j, xj) in storia:
                        if k - j <= 15 and abs(x - xj) > thr:
                            mob = True
                    storia.append((k, x))
                n += mob
            riga.append("%.1f m: %5.1f %%" % (r, 100 * n / 500))
        print("     sigma trasversale %.3f m (soglia %.3f m): %s" % (sig_t, thr, " | ".join(riga)))

if quale == 'a12':
    A_disco = math.pi * RMAX ** 2
    A_cam = FOV * (RMAX ** 2 - RNEAR ** 2)
    print("Attacco 12b. Conto delle aree sul disco di 3 m attorno al sensore (%.2f m2)." % A_disco)
    print("  Camera sola: suolo osservabile %.2f m2 = %.1f %% del disco (87 gradi, da %.2f a 3 m)" % (A_cam, 100 * A_cam / A_disco, RNEAR))
    for (n, fov, port) in ((3, 60, 2.0), (2, 60, 2.0), (3, 45, 2.0), (3, 60, 1.0)):
        A_tof = n * math.radians(fov) / 2 * port ** 2
        print("  + %d ToF da %d gradi sui fianchi e dietro, sola prossimita' fino a %.1f m: %.2f m2 in piu' = %.1f %% del disco (totale con dato %.1f %%)" % (
            n, fov, port, A_tof, 100 * A_tof / A_disco, 100 * (A_cam + A_tof) / A_disco))
    A_an = math.radians(60) / 2 * (RNEAR ** 2 - 0.25)
    print("  Un ToF da 60 gradi puntato in basso davanti: anello cieco 0,5-%.2f m coperto per %.2f m2 su %.2f m2 dell'anello nel campo della camera" % (
        RNEAR, A_an, FOV * (RNEAR ** 2 - 0.25)))
    print("  I 60 gradi e i 2,0 m al chiuso sono le cifre dei file dello sciame (scheda ST citata in SELEZIONE.md): non riverificate da me.")
