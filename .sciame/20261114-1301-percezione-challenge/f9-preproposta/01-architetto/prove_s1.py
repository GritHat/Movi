#!/usr/bin/env python3
"""Prove dell'architetto sulla strategia S1 (selettore della configurazione), f9.

Solo libreria standard, semi fissati. Rifare:
    timeout 120 python3 -I prove_s1.py > risultati_s1.txt
Le previsioni stanno in PREVISIONI.md (scritte prima di questo file).
Non e' il prototipo: sono modelli minimi, dichiarati riga per riga.
"""
import itertools
import math
import random
import time

SEME = 20261114


# --------------------------------------------------------------------------- P1
def p1():
    print("== P1: i limiti 1,24 / 1,09 / 2,41 m sono limiti del campo visivo ==")
    h, incl, campo_v = 1.2, 15.0, 58.0          # B1 del nucleo
    basso = math.radians(incl + campo_v / 2)     # bordo inferiore sotto l'orizzonte
    alto = math.radians(campo_v / 2 - incl)      # bordo superiore sopra l'orizzonte
    print(f"bordo inferiore {math.degrees(basso):.1f} gradi sotto l'orizzonte, "
          f"superiore {math.degrees(alto):.1f} sopra")
    print(f"suolo visto da                     {h / math.tan(basso):.3f} m   (nucleo: 1,24)")
    print(f"ostacolo di 15 cm fuori campo sotto {(h - 0.15) / math.tan(basso):.3f} m   (nucleo: 1,09)")
    print(f"oggetto a 1,8 m di quota visto oltre {(1.8 - h) / math.tan(alto):.3f} m   (nucleo: 2,41)")
    basso_v = math.radians(incl + 87.0 / 2)
    print(f"montaggio verticale (87 gradi): suolo da {h / math.tan(basso_v):.3f} m   (nucleo: 0,74)")
    print("nessuna delle formule contiene la struttura dati: quota, inclinazione, campo.")
    print()
    return basso, alto, h


# --------------------------------------------------------------------------- P2
def simula(scenario, braccio, soglia_su, minuti=10, seme=SEME, periodo_val=15):
    """Ritorna (cambi, quota di cicli > 55 ms, quota di cicli > 66,7 ms, quota di tempo in 'piena')."""
    rng = random.Random(seme)
    n = int(minuti * 60 * 15)
    if scenario == "A":
        piena, delta, amp = 60.0, 20.0, 0.0
    else:
        piena, delta, amp = 55.0, 12.0, 6.0
    sigma = 2.0
    conf = "piena"
    finestra = []
    cambi = 0
    ultimo_cambio = -10 ** 9
    oltre55 = oltre66 = in_piena = 0
    bloccata = False
    for k in range(n):
        t = k / 15.0
        carico = amp * math.sin(2 * math.pi * t / 4.0)
        T = (piena if conf == "piena" else piena - delta) + carico + rng.gauss(0, sigma)
        finestra.append(T)
        if len(finestra) > 15:
            finestra.pop(0)
        oltre55 += T > 55.0
        oltre66 += T > 66.7
        in_piena += conf == "piena"
        if k % periodo_val != periodo_val - 1 or len(finestra) < 15:
            continue
        media = sum(finestra) / 15
        nuovo = conf
        if braccio == "a":                       # tabella nuda
            if conf == "piena" and media > 55:
                nuovo = "ridotta"
            elif conf == "ridotta" and media < 45:
                nuovo = "piena"
        elif braccio == "b":                     # tabella + isteresi temporale 2,5 s
            if t - ultimo_cambio >= 2.5:
                if conf == "piena" and media > 55:
                    nuovo = "ridotta"
                elif conf == "ridotta" and media < 45:
                    nuovo = "piena"
        elif braccio == "c":                     # giu' subito; su dopo 10 s e con costo previsto
            if conf == "piena" and media > 55:
                nuovo = "ridotta"
            elif conf == "ridotta" and t - ultimo_cambio >= 10.0 and media + delta < soglia_su:
                nuovo = "piena"
        elif braccio == "d":                     # a scatto: giu' una volta, mai su da solo
            if conf == "piena" and media > 55 and not bloccata:
                nuovo = "ridotta"
                bloccata = True
        if nuovo != conf:
            conf = nuovo
            cambi += 1
            ultimo_cambio = t
            finestra = []                        # la media riparte nella configurazione nuova
    return cambi, oltre55 / n, oltre66 / n, in_piena / n


def p2():
    print("== P2: oscillazione del selettore (10 minuti simulati, 15 Hz, valutazione ogni 1 s) ==")
    print("scenario A: piena 60 ms, ridotta 40 ms, sigma 2 ms. "
          "scenario B: piena 55 ms +/- 6 ms (periodo 4 s), ridotta 12 ms in meno.")
    print(f"{'scen':4} {'braccio':28} {'cambi/10min':>11} {'cambi/min':>9} "
          f"{'cicli>55ms':>10} {'cicli>66,7':>10} {'tempo in piena':>14}")
    nomi = {"a": "a tabella nuda", "b": "b + isteresi 2,5 s",
            "c": "c costo previsto, sosta 10 s", "d": "d a scatto (minima)"}
    for scen in ("A", "B"):
        for br in ("a", "b", "c", "d"):
            cambi, o55, o66, pp = simula(scen, br, soglia_su=45.0)
            print(f"{scen:4} {nomi[br]:28} {cambi:11d} {cambi / 10:9.1f} "
                  f"{100 * o55:9.1f}% {100 * o66:9.1f}% {100 * pp:13.1f}%")
    print("sensibilita' del braccio c alla soglia di risalita (fissata DOPO le previsioni, vedi CONSEGNA):")
    for scen in ("A", "B"):
        for s in (45.0, 50.0, 55.0):
            cambi, o55, o66, pp = simula(scen, "c", soglia_su=s)
            print(f"  scenario {scen}, risale se costo previsto < {s:.0f} ms: {cambi} cambi in 10 min, "
                  f"cicli > 55 ms {100 * o55:.1f}%")
    print("altri 4 semi, scenario A e B, bracci b e d (cambi in 10 min):")
    for seme in (1, 2, 3, 4):
        riga = []
        for scen in ("A", "B"):
            for br in ("b", "d"):
                riga.append(f"{scen}{br}={simula(scen, br, 45.0, seme=seme)[0]}")
        print("  seme", seme, " ".join(riga))
    print("valutazione a 2 Hz (ogni 8 cicli) invece che a 1 Hz, scenario A:")
    for br in ("a", "b"):
        cambi, o55, _, _ = simula("A", br, 45.0, periodo_val=8)
        print(f"  braccio {br}: {cambi} cambi in 10 min ({cambi / 10:.1f}/min), cicli > 55 ms {100 * o55:.1f}%")
    print()


# --------------------------------------------------------------------------- P3a
def griglia(r_min, pannello_x0, tasso_buchi, celle_morte, seme):
    """Modello dall'alto. Raggio-pixel = (sotto-colonna di 0,1 gradi, campione ogni 2,5 cm di distanza).
    Stato della cella fine (1 grado x 0,1 m), regola di B2 alla lettera:
    occupato se un raggio torna dal pannello; libero se almeno un raggio vede il suolo;
    in ombra se tutti i raggi sono oltre il pannello; altrimenti non osservato."""
    rng = random.Random(seme)
    n_az = 87
    n_r = round((3.0 - r_min) / 0.1)
    z_p, larg = 1.8, 1.0
    fine = {}
    raggi = {}
    morte = set()
    if celle_morte > 0:
        for i in range(n_az):
            for j in range(n_r):
                if rng.random() < celle_morte:
                    morte.add((i, j))
    for i in range(n_az):
        for j in range(n_r):
            suolo = occ = ombra = 0
            for s in range(10):
                th = math.radians(-43.5 + i + 0.05 + 0.1 * s)
                x_p = z_p * math.tan(th)
                colpisce = pannello_x0 - larg / 2 <= x_p <= pannello_x0 + larg / 2
                rho_p = z_p / math.cos(th)
                for q in range(4):
                    rho = r_min + 0.1 * j + 0.0125 + 0.025 * q
                    if colpisce and rho >= rho_p:
                        if rho - rho_p < 0.025:
                            occ += 1             # il ritorno del pannello cade in questo campione
                        else:
                            ombra += 1
                        continue
                    if rho < 1.243:
                        continue                 # anello cieco: nessun raggio arriva al suolo
                    if (i, j) in morte or rng.random() < tasso_buchi:
                        continue                 # buco: nessun dato
                    suolo += 1
            raggi[(i, j)] = (suolo, occ, ombra)
            if occ:
                fine[(i, j)] = "occupato"
            elif suolo:
                fine[(i, j)] = "libero"
            elif ombra == 40:
                fine[(i, j)] = "ombra"
            else:
                fine[(i, j)] = "non_oss"
    return fine, raggi, n_az, n_r


def degrada(fine, raggi, n_az, n_r):
    """Passa a 2 gradi x 0,2 m. Ritorna le celle fini non viste che finiscono sotto un 'libero'
    con (i) la regola di B2 alla lettera sulla cella grossa, (ii) l'aggregazione prudente."""
    nati_i = nati_ii = 0
    for I in range(0, n_az, 2):
        for J in range(0, n_r, 2):
            figli = [(i, j) for i in (I, I + 1) for j in (J, J + 1) if i < n_az and j < n_r]
            suolo = sum(raggi[f][0] for f in figli)
            occ = sum(raggi[f][1] for f in figli)
            libero_i = occ == 0 and suolo > 0
            libero_ii = all(fine[f] == "libero" for f in figli)
            for f in figli:
                if fine[f] in ("ombra", "non_oss"):
                    nati_i += libero_i
                    nati_ii += libero_ii
    return nati_i, nati_ii


def p3a():
    print("== P3a: griglia piu' grossa (1 grado x 0,1 m -> 2 gradi x 0,2 m), pannello 1 m a 1,8 m ==")
    print("misura: celle fini 'in ombra' o 'non osservato' che finiscono dentro una cella grossa 'libero'")
    for etichetta, r_min, buchi, morte in (
        ("come scritto in P3a: griglia 1,2-3 m, 1 % di raggi senza dato", 1.2, 0.01, 0.0),
        ("VARIANTE NOTATA DOPO: griglia 0,5-3 m come in B1 del nucleo", 0.5, 0.01, 0.0),
        ("VARIANTE NOTATA DOPO: 0,5-3 m e 1 % di celle morte (audit, ipotesi 6)", 0.5, 0.01, 0.01),
    ):
        fine, raggi, n_az, n_r = griglia(r_min, 0.0, buchi, morte, SEME)
        conta = {s: sum(1 for v in fine.values() if v == s) for s in ("libero", "occupato", "ombra", "non_oss")}
        n_i, n_ii = degrada(fine, raggi, n_az, n_r)
        non_viste = conta["ombra"] + conta["non_oss"]
        print(f"- {etichetta}")
        print(f"  celle fini {n_az * n_r}: {conta}")
        print(f"  (i) regola alla lettera: {n_i} celle non viste sotto un 'libero' "
              f"({100 * n_i / max(1, non_viste):.1f} % delle non viste); (ii) prudente: {n_ii}")
    print("- VARIANTE NOTATA DOPO: il pannello si sposta di lato da -0,50 a +0,50 m a passi di 5 cm "
          "(griglia 0,5-3 m, 1 % di raggi senza dato)")
    esiti = []
    for k in range(21):
        fine, raggi, n_az, n_r = griglia(0.5, -0.5 + 0.05 * k, 0.01, 0.0, SEME + k)
        esiti.append(degrada(fine, raggi, n_az, n_r))
    es_i = [e[0] for e in esiti]
    print(f"  (i): minimo {min(es_i)}, mediana {sorted(es_i)[10]}, massimo {max(es_i)} celle fini; "
          f"(ii): massimo {max(e[1] for e in esiti)}")
    print()


# --------------------------------------------------------------------------- P3b
def p3b(basso, alto, h):
    print("== P3b: da tre fasce di quota (S10) alla mappa sul piano ==")
    fasce = (("bassa", 0.15, 0.60), ("media", 0.60, 1.60), ("alta", 1.60, 2.00))
    print("a distanza d il campo copre le quote da max(0, 1,2 - d tan44) a 1,2 + d tan14")
    da = {}
    for nome, q0, q1 in fasce:
        d_sotto = max(0.0, (h - q0) / math.tan(basso))
        d_sopra = max(0.0, (q1 - h) / math.tan(alto))
        da[nome] = max(d_sotto, d_sopra)
        print(f"fascia {nome} ({q0:.2f}-{q1:.2f} m): osservata per intero da d >= {da[nome]:.3f} m")
    d_suolo = h / math.tan(basso)
    sett = math.radians(87.0) / 2
    area = lambda a, b: sett * (b * b - a * a)
    zona = area(d_suolo, 3.0)
    for nome, pert in (("bassa+media", ("bassa", "media")), ("bassa+media+alta", ("bassa", "media", "alta"))):
        d_lib = max(d_suolo, max(da[f] for f in pert))
        if d_lib >= 3.0:
            print(f"profilo {nome}: nessuna cella 'libero' entro 3 m con le tre fasce; "
                  f"sul piano tutta la zona 1,24-3 m ({zona:.2f} m2) puo' diventare 'libero'")
        else:
            a = area(d_suolo, d_lib)
            print(f"profilo {nome}: 'libero' a tre fasce solo da {d_lib:.3f} m; passando alla mappa sul piano "
                  f"l'anello {d_suolo:.2f}-{d_lib:.2f} m ({a:.2f} m2, {100 * a / zona:.1f} % della zona "
                  f"di {zona:.2f} m2) passa da 'non libero' a 'libero'")
    print()


# --------------------------------------------------------------------------- P4
def p4():
    print("== P4: costo di calcolo del selettore (Python puro, tabella a 6 righe + media su 15) ==")
    rng = random.Random(SEME)
    finestra = [rng.gauss(50, 3) for _ in range(15)]

    def valuta(fin, gpu, ir, xt, d_ok, tof_ok):
        m = sum(fin) / len(fin)
        r = []
        if d_ok and tof_ok and m < 45: r.append(1)
        if (not gpu) or m > 55: r.append(2)
        if tof_ok and ir: r.append(3)
        if d_ok and tof_ok and xt: r.append(4)
        if (not d_ok) and tof_ok: r.append(5)
        if gpu and m < 30: r.append(6)
        return r

    n = 200_000
    migliore = float("inf")
    for _ in range(5):
        t0 = time.perf_counter()
        for k in range(n):
            valuta(finestra, k & 1, k & 2, k & 4, k & 8, k & 16)
        migliore = min(migliore, (time.perf_counter() - t0) / n)
    print(f"una valutazione: {migliore * 1e6:.2f} microsecondi (migliore di 5 giri da {n}); "
          f"a 2 Hz = {100 * 2 * migliore / 1.0:.6f} % del tempo; indicativo, macchina condivisa")
    print()


# --------------------------------------------------------------------------- P5
def p5():
    print("== P5: la tabella della preproposta come funzione degli ingressi ==")
    bande = ("<30", "30-45", "45-55", ">55")
    stati = list(itertools.product(bande, (True, False), (True, False), (True, False),
                                   (True, False), (True, False)))
    print(f"stati d'ingresso: {len(stati)} (T x GPU x saturazione IR x interferenza x camera x ToF)")
    for lettura in ("oppure", "e"):
        zero = uno = piu = confl_rete = confl_mappa = 0
        zero_es = []
        for T, gpu, ir, xt, d_ok, tof_ok in stati:
            r = []
            if d_ok and tof_ok and T in ("<30", "30-45"): r.append(1)
            r2 = ((not gpu) or T == ">55") if lettura == "oppure" else ((not gpu) and T == ">55")
            if r2: r.append(2)
            if tof_ok and ir: r.append(3)
            if d_ok and tof_ok and xt: r.append(4)
            if (not d_ok) and tof_ok: r.append(5)
            if gpu and T == "<30": r.append(6)
            if not r:
                zero += 1
                if len(zero_es) < 3:
                    zero_es.append((T, "GPU" if gpu else "no GPU", "camera sana" if d_ok else "camera guasta",
                                    "ToF sani" if tof_ok else "ToF assenti"))
            elif len(r) == 1:
                uno += 1
            else:
                piu += 1
            rete_on = 1 in r or 6 in r
            rete_off = 2 in r
            confl_rete += rete_on and rete_off
            mappe = set()
            if 1 in r: mappe.add("2.5D")
            if 2 in r: mappe.add("2D o 2.5D grossa")
            if 6 in r: mappe.add("voxel")
            confl_mappa += len(mappe) > 1
        n = len(stati)
        print(f"riga 2 letta '{lettura}': nessuna riga {zero} ({100 * zero / n:.1f} %), "
              f"una sola {uno} ({100 * uno / n:.1f} %), due o piu' {piu} ({100 * piu / n:.1f} %); "
              f"rete accesa e spenta insieme {confl_rete}, due mappe insieme {confl_mappa}")
        print(f"   esempi senza riga: {zero_es}")
    camera = ("accesa", "spenta")
    tof = ("spenti", "accesi", "limitati a 0,5 m", "a divisione di tempo", "coni sovrapposti spenti")
    mappa = ("2D", "2.5D", "2.5D grossa", "voxel")
    rete = ("accesa", "spenta")
    con_camera = len(tof) * len(mappa) * len(rete)
    senza = len(tof)            # mappa e rete non contano senza camera; 'tutto spento' compreso
    print(f"configurazioni nominabili con gli assi della tabella: {con_camera} con la camera + {senza} senza "
          f"= {con_camera + senza}, contro 6 righe")
    print("ore di prova se ognuna passa il protocollo H0-H13 (2 h 40 in due = 5,33 ore-persona): "
          f"6 righe = {6 * 16 / 3:.0f} ore-persona; {con_camera + senza} configurazioni = "
          f"{(con_camera + senza) * 16 / 3:.0f} ore-persona")
    print()


if __name__ == "__main__":
    print(f"prove_s1.py, seme {SEME}, Python {__import__('sys').version.split()[0]}")
    b, a, h = p1()
    p2()
    p3a()
    p3b(b, a, h)
    p4()
    p5()
