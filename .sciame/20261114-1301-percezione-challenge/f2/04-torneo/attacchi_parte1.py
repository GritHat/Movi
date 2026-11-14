#!/usr/bin/env python3
"""Attacchi dell'avversario, f2 torneo, parte 1. Python puro, < 1 s di CPU.
Non importa codice degli autori. Ogni blocco stampa il caso e l'esito.
I parametri delle schede (campo, base, limite d'errore) sono dichiarati qui sotto con l'origine."""
import math

rad = math.radians
print("=== P1 (H-001) errore di profondita' stereo a 4 m ===")
HFOV = 87.0  # campo orizzontale della profondita', D435/D455/Gemini 335 (schede, vedi TORNEO)
for nome, B, W in (("classe base 50 mm, 848 px", 0.050, 848), ("classe base 50 mm, 1280 px", 0.050, 1280),
                   ("D455 base 95 mm, 848 px", 0.095, 848), ("D455 base 95 mm, 1280 px", 0.095, 1280)):
    f = (W / 2) / math.tan(rad(HFOV / 2))
    for sp in (0.08, 0.10):
        s4 = 16 * sp / (f * B)
        print(f"  {nome}: f={f:6.1f} px, sottopixel {sp}: sigma_z(4 m) = {100*s4:5.1f} cm")
# limite dichiarato dal costruttore: <= 2 % a 2 m (base 50 mm), <= 2 % a 4 m (D455); l'errore stereo scala con z^2
lim50 = 0.02 * 2 * (4 / 2) ** 2
lim95 = 0.02 * 4
print(f"  limite dichiarato '<=2 % a 2 m' scalato z^2 a 4 m (base 50 mm): {100*lim50:.1f} cm  -> soglia R2 15 cm: {'SUPERA' if lim50>0.15 else 'sotto'}")
print(f"  limite dichiarato '<=2 % a 4 m' (D455): {100*lim95:.1f} cm -> {'SUPERA' if lim95>0.15 else 'sotto'}")
f1280 = 640 / math.tan(rad(HFOV / 2))
print(f"  sottopixel implicito nel limite 2 % a 2 m (base 50, 1280 px): {0.04*f1280*0.05/4:.2f} px")
print(f"  distanza a cui il limite dichiarato (base 50 mm) tocca 15 cm: {2*math.sqrt(0.15/0.04):.2f} m")

print("\n=== P2 (H-002) gradino 15 cm a 2 m, sensore a 1,2 m ===")
H = 1.2
for d, step in ((2.0, 0.15), (3.0, 0.07), (4.0, 0.07)):
    r = math.hypot(d, H)
    sinth = H / r
    for etichetta, sz in (("0,08 px, 848 px, base 50", r * r * 0.08 / (424 / math.tan(rad(43.5)) * 0.05)),
                          ("limite 2 % a 2 m scalato", 0.04 * (r / 2) ** 2)):
        sh = sz * sinth
        print(f"  d={d} m, gradino {100*step:.0f} cm, {etichetta}: sigma_z={100*sz:4.1f} cm, sigma_h={100*sh:4.1f} cm, distanza = {step/sh:4.1f} sigma")
print("  errore d'assetto (beccheggio) come errore di quota del suolo: dh = d*tan(err)")
for err in (0.5, 1.0, 2.0):
    print(f"    err {err} gradi: 2 m -> {200*math.tan(rad(err)):.1f} cm; 4 m -> {400*math.tan(rad(err)):.1f} cm; il suolo supera 7 cm oltre {0.07/math.tan(rad(err)):.1f} m")

print("\n=== P2b (H-002) camera inclinata in basso: ostacolo alla quota della testa (1,8 m) ===")
VFOV = 58.0
for tilt in (0, 10, 15, 20, 30):
    up = VFOV / 2 - tilt       # bordo alto del campo sopra l'orizzonte
    down = VFOV / 2 + tilt     # bordo basso sotto l'orizzonte
    dmin_suolo = H / math.tan(rad(down)) if down < 90 else 0.0
    if up > 0:
        dtesta = (1.8 - H) / math.tan(rad(up))
        s = f"visibile solo oltre {dtesta:4.2f} m"
    else:
        s = "MAI visibile (bordo alto sotto l'orizzonte)"
    print(f"  inclinazione {tilt:2d} gradi: suolo visto da {dmin_suolo:4.2f} m; ostacolo a 1,8 m {s}")

print("\n=== P3 (H-003) LiDAR 2D al petto ===")
for nome, passo in (("RPLIDAR C1 0,72 gradi", 0.72), ("LD19 0,8 gradi", 0.8)):
    for largh, cosa in ((0.12, "gamba"), (0.40, "busto")):
        for d in (3.0, 5.0):
            print(f"  {nome}: {cosa} {largh} m a {d} m -> {largh/(d*rad(passo)):.1f} punti per giro")
for sporg in (0.05, 0.10):
    for busto in (0.40, 0.45):
        occ = 2 * math.degrees(math.atan((busto / 2) / sporg))
        print(f"  LiDAR a {100*sporg:.0f} cm dal petto, busto {busto} m: coperti {occ:.0f} gradi = {occ/360:.0%} del giro, {min(occ,180)/180:.0%} del semigiro posteriore")
print("  sul capo (piano a ~1,75 m): una persona alta < 1,75 m non interseca il piano -> 0 punti")

print("\n=== P8 (H-008) regola firmata, un settore, celle di 0,1 m ===")
DT = 1 / 15
def stato_cella(suolo_visto_alla_quota, ostacolo_fra_7cm_e_2m, oltre_primo_ritorno, in_campo=True):
    """La regola firmata da nuvole-punti-1, stato del solo fotogramma corrente."""
    if not in_campo: return "non osservato"
    if oltre_primo_ritorno: return "in ombra"
    if ostacolo_fra_7cm_e_2m: return "occupato"
    if suolo_visto_alla_quota: return "libero"
    return "non osservato"
# caso 1: vetro a 2 m. La stereo attiva non ha ritorno dal vetro pulito: vede il suolo oltre, alla quota attesa.
print("  caso vetro (lastra a 2,0 m, nessun ritorno dalla lastra, suolo visto attraverso):")
print("    cella 2,0 m ->", stato_cella(True, False, False), " (fisicamente OCCUPATA dal vetro) => 'libero' FALSO")
# caso 2: rampa in salita di 5 gradi che comincia a 1 m
for pend in (3, 5, 8):
    d7 = 0.07 / math.tan(rad(pend))
    print(f"  caso rampa {pend} gradi: il suolo supera 7 cm dopo {d7:.2f} m dall'inizio della rampa -> 'occupato' FALSO (R5), in discesa 'non osservato'")
# caso 3: corridore / monopattino contro la scadenza del libero (0,5 s) e il margine 0,7 m
for v in (1.4, 3.0, 5.6):
    print(f"  caso mobile a {v} m/s in cella 'libero' ricordata (0,5 s): avanza {v*0.5:.2f} m (margine 0,7 m) -> {'VIOLATO' if v*0.5>0.7 else 'entro'}; in 1 fotogramma a 15 Hz: {v*DT:.2f} m")
# caso 4: occupato ricordato, cella fuori campo, il mobile se ne va
t, eta = 0.0, 0.0
ricordo = "occupato"   # persona ferma nella cella C, poi C esce dal campo (il portatore gira la testa di 30 gradi)
for passo in range(int(60 / DT)):
    t += DT; eta += DT
    # la persona lascia C a t = 1 s; C resta fuori campo: nessuna osservazione puo' smentire
    s = stato_cella(False, False, False, in_campo=False)
    if s in ("libero", "occupato"): ricordo, eta = s, 0.0
print(f"  caso fuori campo: dopo 60 s la cella C e' '{ricordo} ricordato' con eta' {eta:.0f} s; la persona se n'e' andata a t=1 s -> FANTASMA senza limite d'eta'")
# caso 5: sosta dietro un pannello di 1 m, regola 'previsto in libero per 3 fotogrammi -> chiusa'
v = 1.3; larg = 1.0
# ombra: la traccia entra a x=0, l'ombra copre [0, larg]; la persona si ferma a x=0,5; il punto previsto prosegue
x_prev, n_lib, t = 0.0, 0, 0.0
while True:
    t += DT; x_prev += v * DT
    in_ombra = x_prev <= larg
    n_lib = 0 if in_ombra else n_lib + 1
    if n_lib == 3: break
print(f"  caso sosta: la persona e' ferma a 0,5 m dentro l'ombra; il punto previsto esce a {larg/v:.2f} s, traccia CHIUSA a {t:.2f} s con la persona ancora nascosta (le celle restano 'in ombra': R8 salvo, R3 perso)")

print("\n=== P17 (H-017) battito e fotogramma ripetuto ===")
def battito_dura(regola, guasto_a=5.0, durata=30.0):
    """Ritorna per quanti secondi il battito continua dopo il guasto.
    Guasto: da 'guasto_a' il sensore (o il nodo a monte) ripete l'ultimo fotogramma, con marca temporale nuova."""
    t, ultimo_battito = 0.0, None
    cont, cont_visto, t_cont = 0, -1, 0.0
    contenuto_prec, uguali = None, 0
    while t < durata:
        t += DT
        guasto = t >= guasto_a
        if not guasto: cont += 1
        marca = t                       # ri-marcata a ogni pubblicazione, anche col guasto
        contenuto = cont                # col guasto il contenuto (rumore compreso) e' identico bit a bit
        if regola == "marca":           # 'fresco' = eta' della marca temporale < 0,2 s
            fresco = (t - marca) < 0.2
        elif regola == "contatore":     # 'fresco' = il contatore di fotogramma del sensore e' avanzato da < 0,2 s
            if cont != cont_visto: cont_visto, t_cont = cont, t
            fresco = (t - t_cont) < 0.2
        elif regola == "contenuto":     # 'fresco' = meno di 3 fotogrammi consecutivi identici
            uguali = uguali + 1 if contenuto == contenuto_prec else 0
            contenuto_prec = contenuto
            fresco = uguali < 3
        if fresco: ultimo_battito = t   # settore davanti 'libero osservato' nel fotogramma (ripetuto)
    return ultimo_battito - guasto_a
for regola in ("marca", "contatore", "contenuto"):
    print(f"  regola 'fresco' = {regola}: il battito continua {battito_dura(regola):.2f} s dopo il blocco (finestra osservata 25 s)")

print("\n=== PK6 (K-006) le due regole di memoria sugli stessi casi ===")
def memoria(regola, storia, T=2.0):
    """storia: lista di (dt, osservazione) con osservazione in libero/occupato/None (non visto). Ritorna lo stato finale."""
    stato, eta = "sconosciuto", 0.0
    for dt, oss in storia:
        if oss: stato, eta = oss, 0.0
        else:
            eta += dt
            if regola == "H-008" and stato == "libero" and eta > 0.5: stato = "sconosciuto"
            if regola == "H-009" and stato in ("libero", "occupato") and eta > T: stato = "sconosciuto"
    return stato, eta
casi = {
 "vetro (la cella col vetro e' vista 'libero' a ogni fotogramma)": [(DT, "libero")] * 30,
 "mobile uscito: occupato, poi cella non vista per 60 s (persona via dopo 1 s)": [(DT, "occupato")] * 15 + [(DT, None)] * 900,
 "muro fuori campo da 60 s (ancora li')": [(DT, "occupato")] * 15 + [(DT, None)] * 900,
 "libero visto, poi non visto per 1,5 s (un pedone a 1,4 m/s ha fatto 2,1 m)": [(DT, "libero")] * 15 + [(DT, None)] * 22,
}
for nome, st in casi.items():
    a = memoria("H-008", st); b = memoria("H-009", st, T=2.0)
    print(f"  {nome}\n     H-008 -> {a[0]} (eta' {a[1]:.1f} s) | H-009 con T=2 s -> {b[0]} (eta' {b[1]:.1f} s)")
