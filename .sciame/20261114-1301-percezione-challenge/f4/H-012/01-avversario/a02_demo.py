# Attacco 2 (demo in scala), 6c (centroide all'ingresso nell'ombra) e 11 (voce): stessi transiti.
import sys
from comune_f4 import *

quale = sys.argv[1]


def riga(nome, rs):
    tr = [r for r in rs if r['traccia']]
    ri = [r for r in rs if r['traccia'] and r['riemerge']]
    return ("%-34s ril.prima %4.1f | traccia %5.1f %% | confermata %5.1f %% | mobile(cresc.) %5.1f %% | mobile(fissa) %5.1f %% | "
            "previsto vivo alla riem.: D1 %5.1f %% D2 %5.1f %% | fine previsto med. D1 %.2f s D2 %.2f s | buio med. %.2f s | contiene %5.1f %% (n=%d)") % (
        nome, sum(r['npre'] for r in rs) / len(rs), quota(r['traccia'] for r in rs), quota(r['conf'] for r in rs),
        quota(r['mob_c'] for r in rs), quota(r['mob_f'] for r in rs),
        quota(r['vivo1'] for r in ri), quota(r['vivo2'] for r in ri),
        mediana(r['tend1'] for r in tr), mediana(r['tend2'] for r in tr), mediana(r['buio'] for r in ri),
        quota(r['cont'] for r in ri), len(ri))


if quale == 'a2':
    rng = random.Random(SEME + 2)
    print("Attacco 2. Pannello 0,5 m a 1,5 m; attore sulla retta z; corpo 0,4 m; Pd 0,9; 500 transiti per riga.")
    print("D1 = cerchio ∩ ombra in griglia / ombra in griglia; D2 = cerchio ritagliato sul non osservato / ombra in griglia.")
    for z in (3.0, 2.8, 2.5):
        print(riga("z = %.1f m" % z, [transito(rng, z) for _ in range(500)]))
    print("Arco r = 3,0 m: quota di misure entro portata (rumore 5 cm):",
          "%.1f %%" % quota(3.0 + rng.gauss(0, SIG) <= 3.0 for _ in range(20000)))
    print("Tratto visibile prima dell'ombra a z = 2,8 m: da x = -%.3f a x = -%.3f m (corpo intero)" % (
        math.sqrt(9 - 2.8 ** 2), 2.8 * 0.25 / 1.5 + 0.2))
    print()
    print("[correzione] stessa ombra di 1 m alla distanza dell'attore, ma dentro la portata: pannello 0,5 m a 1,15 m, attore a 2,3 m")
    print(riga("z = 2,3 m, pannello a 1,15 m", [transito(rng, 2.3, zp=1.15) for _ in range(500)]))
    print(riga("z = 2,0 m, pannello a 1,0 m", [transito(rng, 2.0, zp=1.0) for _ in range(500)]))

if quale == 'a6c':
    rng = random.Random(SEME + 6)
    print("Attacco 6c. Contenimento alla riemersione (prima misura entro il cerchio al 95 %, S = P + R), attore che prosegue.")
    for (z, wp, zp) in ((2.5, 0.6, 1.5), (2.5, 0.5, 1.5), (2.3, 0.5, 1.15)):
        for body in (0.4, 0.0):
            rs = [transito(rng, z, wp=wp, zp=zp, body=body) for _ in range(500)]
            print(riga("z %.1f, pann. %.1f a %.2f, corpo %.1f" % (z, wp, zp, body), rs))
        rs = [transito(rng, z, wp=wp, zp=zp, body=0.4, wmin=0.39) for _ in range(500)]
        print(riga("  [correzione] solo gruppi interi", rs))

if quale == 'a11':
    rng = random.Random(SEME + 11)
    print("Attacco 11. Canale vocale senza interruzione: una frase alla volta; a canale libero dice lo stato corrente.")
    for (z, zp) in ((2.8, 1.5), (2.5, 1.5), (2.3, 1.15)):
        rs = [r for r in (transito(rng, z, zp=zp) for _ in range(500)) if r['traccia'] and r['riemerge']]
        for frase in (2.0, 1.0):
            tardi = salt = 0
            for r in rs:
                P = r['tend1'] if r['tend1'] is not None else r['buio']
                D = r['buio']
                if frase > P:
                    tardi += 1  # la frase "previsto" finisce a stato scaduto
                if P < D and D <= frase:
                    salt += 1  # "perso" comincia e finisce mentre il canale e' occupato
            n = max(1, len(rs))
            print("z = %.1f m, frase di %.1f s: 'previsto' dura (mediana) %.2f s; frase finita a stato scaduto %5.1f %%; 'perso' mai detto mentre vale %5.1f %% (n = %d)" % (
                z, frase, mediana((r['tend1'] if r['tend1'] is not None else r['buio']) for r in rs),
                100 * tardi / n, 100 * salt / n, len(rs)))
