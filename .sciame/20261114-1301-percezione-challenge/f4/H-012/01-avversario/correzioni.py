# Correzioni minime provate dopo gli attacchi 3, 10 e 11 (prima e dopo). Scritte DOPO aver visto gli esiti.
import sys
from comune_f4 import *

quale = sys.argv[1]

if quale == 'a3':
    rng = random.Random(SEME + 103)
    print("Correzione dell'attacco 3: (1) anello cieco e oltre portata dichiarati una volta, fuori dal messaggio per fotogramma;")
    print("(2) una cella e' 'buco' solo dopo 3 fotogrammi non validi di fila. Settore di 10 gradi, persona da 2,95 a 1,0 m a 1,4 m/s, 200 ripetizioni.")
    for p in (1.0, 0.99, 0.95, 0.8):
        ok = [0, 0]
        n = 0
        for rip in range(200):
            manc = {}
            rp = 2.95
            while rp > 1.0:
                half = math.atan(0.2 / rp)
                grave = [False, False]  # c'e' un 'non osservato' che batte il mobile? [senza isteresi, con isteresi]
                for bi in range(-5, 5):
                    b = math.radians(bi + 0.5)
                    for ri in range(5, 30):
                        r = ri / 10 + 0.05
                        if r < RNEAR or (abs(b) <= half and r > rp - 0.05):
                            manc[(bi, ri)] = 0
                            continue
                        if rng.random() < p:
                            manc[(bi, ri)] = 0
                        else:
                            manc[(bi, ri)] = manc.get((bi, ri), 0) + 1
                            grave[0] = True
                            if manc[(bi, ri)] >= 3:
                                grave[1] = True
                ok[0] += not grave[0]
                ok[1] += not grave[1]
                n += 1
                rp -= 1.4 * DT
        print("  p_suolo %.2f: 'mobile in avvicinamento' emesso: solo (1) %5.1f %%; (1) + (2) %5.1f %%" % (p, 100 * ok[0] / n, 100 * ok[1] / n))

if quale == 'a10':
    rng = random.Random(SEME + 110)
    print("Correzione dell'attacco 10: due cause in piu' per 'affidabilita' persa':")
    print("(3) quota di celle con profondita' valida < 50 % di quella della taratura per 3 fotogrammi; (4) gravita' dell'IMU a piu' di 0,5 gradi dalla taratura, o giroscopio oltre 5 gradi/s.")
    casi = {
        "(a) valida al 10 %": dict(valida=0.10, pitch=0.0, gyro=0.0),
        "(c) beccheggio di 2 gradi": dict(valida=1.0, pitch=2.0, gyro=0.0),
        "(c) imbardata di 10 gradi in 0,2 s": dict(valida=1.0, pitch=0.0, gyro=50.0),
        "scena sana, 60 s [controllo dei falsi]": dict(valida=0.95, pitch=0.0, gyro=0.0),
    }
    for nome, c in casi.items():
        t = None
        bassi = 0
        nf = 900 if 'sana' in nome else 45
        for k in range(nf):
            q = sum(1 for _ in range(200) if rng.random() < c['valida']) / 200
            bassi = bassi + 1 if q < 0.5 else 0
            g = abs(c['gyro']) if k < 3 else 0.0
            if bassi >= 3 or abs(c['pitch'] + rng.gauss(0, 0.1)) > 0.5 or g + abs(rng.gauss(0, 0.5)) > 5.0:
                t = k * DT
                break
        print("  %-42s prima: nessun segnale | dopo: %s" % (nome, ("segnale a %.2f s" % t) if t is not None else "nessun segnale (giusto)" if 'sana' in nome else "NESSUN segnale"))
    print("  (rumore dell'IMU ipotizzato: 0,1 gradi sulla gravita', 0,5 gradi/s sul giroscopio: non di scheda)")

if quale == 'a11':
    rng = random.Random(SEME + 111)
    print("Correzione dell'attacco 11: in voce non la frase ma un segnale breve per stato (0,3 s); la frase solo a stato stabile.")
    for (z, zp, wp, nome) in ((2.3, 1.15, 0.5, "ombra 1 m a 2,3 m"), (2.3, 1.15, 1.0, "ombra 2 m a 2,3 m")):
        rs = [r for r in (transito(rng, z, zp=zp, wp=wp) for _ in range(500)) if r['traccia'] and r['riemerge']]
        for frase in (2.0, 0.3):
            tardi = salt = 0
            for r in rs:
                P = r['tend1'] if r['tend1'] is not None else r['buio']
                D = r['buio']
                tardi += frase > P
                salt += (P < D and D <= frase)
            n = max(1, len(rs))
            print("  %s, messaggio di %.1f s: finito a stato scaduto %5.1f %%; 'perso' mai detto mentre vale %5.1f %%; buio mediano %.2f s (n = %d)" % (
                nome, frase, 100 * tardi / n, 100 * salt / n, mediana(r['buio'] for r in rs), len(rs)))
