# Attacco 7 (chi si nasconde senza essere mai stato tracciato) e 8 (R1 nel primo secondo di vita).
import sys
from itertools import product
from comune_f4 import *

quale = sys.argv[1]


def confermata(hits):
    return any(sum(hits[max(0, i - 4):i + 1]) >= 3 for i in range(len(hits)))


def etichetta(rng, r0, v, pd, nf=40):
    """Bersaglio in avvicinamento radiale da r0 a velocita' v. Ritorna i tempi (dal primo fotogramma visibile) di:
    conferma, 'mobile' con finestra fissa di 1 s, 'mobile' con finestra che cresce (<= 1 s)."""
    hits, storia = [], []
    t_conf = t_fis = t_cre = None
    for k in range(nf):
        r = r0 - v * k * DT
        d = r + rng.gauss(0, SIG) if rng.random() < pd else None
        hits.append(1 if d is not None else 0)
        if t_conf is None and sum(hits[-5:]) >= 3:
            t_conf = k * DT
        if d is not None:
            for (j, dj) in storia:
                if k - j <= 15 and abs(d - dj) > THR:
                    if t_cre is None and t_conf is not None:
                        t_cre = k * DT
                    if k - j == 15 and t_fis is None and t_conf is not None:
                        t_fis = k * DT
            storia.append((k, d))
    return t_conf, t_fis, t_cre


if quale == 'a7':
    rng = random.Random(SEME + 7)
    print("Attacco 7a. Tratto visibile di n fotogrammi prima dell'ombra, Pd = 0,9; conferma 3 su 5.")
    for n in (2, 3, 4, 5, 6, 8):
        esatta = sum((0.9 ** sum(h)) * (0.1 ** (n - sum(h))) for h in product((0, 1), repeat=n) if not confermata(list(h)))
        mc = quota(not confermata([1 if rng.random() < PD else 0 for _ in range(n)]) for _ in range(300))
        print("  n = %d: entra nell'ombra NON confermata: esatto %5.1f %%, 300 scene %5.1f %%" % (n, 100 * esatta, mc))
    print("Attacco 7b. Soggetto mai tracciato che sbuca di fianco al pannello a 1,55 m e viene verso il sensore a 1,4 m/s (300 scene).")
    print("  A 0,5 m (portata minima) arriva dopo %.2f s: da li' in poi la profondita' e' un buco." % ((1.55 - 0.5) / 1.4))
    for nome, idx in (("finestra fissa di 1 s", 1), ("finestra che cresce", 2)):
        ts = [etichetta(rng, 1.55, 1.4, PD)[idx] for _ in range(300)]
        prima = [t for t in ts if t is not None and 1.55 - 1.4 * t >= 0.5]
        print("  %s: 'mobile in avvicinamento' prima di 0,5 m nel %5.1f %%; tempo mediano %.2f s, strada gia' fatta %.2f m su 1,05 m utili" % (
            nome, 100 * len(prima) / 300, mediana(ts), 1.4 * mediana(ts)))

if quale == 'a8':
    rng = random.Random(SEME + 8)
    print("Attacco 8. Pedone a 0,5 m/s in avvicinamento da 2 m, sigma = 5 cm; tempo dal primo fotogramma in cui e' visibile; serve la traccia confermata. 2000 prove per riga.")
    for pd in (1.0, 0.9):
        rs = [etichetta(rng, 2.0, 0.5, pd) for _ in range(2000)]
        print("  Pd %.1f | finestra fissa: entro 1 s (<=) %5.1f %%, prima di 1 s (<) %5.1f %%, entro 1,2 s %5.1f %% | finestra che cresce: entro 1 s %5.1f %%, entro 0,8 s %5.1f %%, mediana %.2f s" % (
            pd,
            quota(r[1] is not None and r[1] <= 1.0 + 1e-9 for r in rs),
            quota(r[1] is not None and r[1] < 1.0 - 1e-9 for r in rs),
            quota(r[1] is not None and r[1] <= 1.2 + 1e-9 for r in rs),
            quota(r[2] is not None and r[2] <= 1.0 + 1e-9 for r in rs),
            quota(r[2] is not None and r[2] <= 0.8 + 1e-9 for r in rs),
            mediana(r[2] for r in rs)))
    print("  Traccia riagganciata dopo il buio: la finestra di 1 s contiene misure solo se il buio dura meno di 1 s; con buio >= 1 s l'etichetta riparte da zero (stessi numeri di sopra).")
    print("  Controllo: bersaglio fermo, falsi 'mobile' entro 2,6 s (finestra che cresce):",
          "%.2f %%" % quota(etichetta(rng, 2.0, 0.0, 0.9)[2] is not None for _ in range(2000)))
