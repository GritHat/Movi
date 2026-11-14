#!/usr/bin/env python3
"""Conti di sciame-lidar per S9 e per l'attacco 4 (estensione f9).

Solo libreria standard, nessun numero casuale (niente semi da fissare): il risultato e' deterministico.
Comando per rifare:
    timeout 120 python3 -I conti_s9.py > risultati_conti_s9.txt
I dati d'ingresso vengono dalle schede (file in scaricati/), le ipotesi sono dichiarate riga per riga.
"""
import math

rad = math.radians


def titolo(t):
    print()
    print("=" * 4, t)


# ---------------------------------------------------------------- A. tempo di preallarme
titolo("A. Tempo di preallarme di un sensore laterale")
LAT_NUCLEO = 0.155   # s, latenza media dal fotone alla scheda audio (SOLUZIONE_V2, R7): dato del nucleo
SEGNALE = 0.30       # s, durata del segnale breve (SOLUZIONE_V2, B8)
print("soglia_m  v_m/s  periodo_ms  conferme  t_lordo  t_dopo_misura  t_dopo_latenza  t_a_fine_segnale  dist_residua_m")


def preallarme(soglia, v, periodo, conferme):
    lordo = soglia / v
    # caso peggiore: l'ingresso sotto soglia cade subito dopo un campione, e servono `conferme` campioni validi
    misura = periodo * conferme
    dopo_misura = lordo - misura
    dopo_lat = dopo_misura - LAT_NUCLEO
    fine = dopo_lat - SEGNALE
    resid = max(0.0, soglia - v * (misura + LAT_NUCLEO + SEGNALE))
    print(f"{soglia:7.2f} {v:6.2f} {periodo*1000:10.0f} {conferme:9d} {lordo:8.2f} {dopo_misura:14.2f} "
          f"{dopo_lat:15.2f} {fine:17.2f} {resid:15.2f}")
    return dopo_misura, dopo_lat, fine


casi = [
    # (soglia, velocita', periodo, conferme, nota)
    (0.50, 1.4, 1 / 15, 1, "L7CX 8x8 a 15 Hz, un campione"),
    (0.50, 1.4, 1 / 15, 2, "L7CX 8x8 a 15 Hz, due campioni (il primo, con stato 10, vale meno del 50 %)"),
    (0.50, 1.4, 1 / 5, 1, "alternanza ideale di tre sensori: 5 Hz ciascuno"),
    (0.50, 1.4, 0.40, 1, "alternanza con start/stop: 3 sensori x 2 fotogrammi x 67 ms"),
    (0.50, 1.4, 1 / 30, 2, "L7CX 4x4 a 30 Hz, due campioni"),
    (0.50, 2.5, 1 / 15, 2, "v_max del nucleo (2,5 m/s)"),
    (0.50, 0.5, 1 / 15, 2, "persona lenta (0,5 m/s)"),
    (0.35, 1.4, 1 / 15, 2, "grigio 17 % a 5 klx, 8x8 (scheda: 350 mm tipici)"),
    (0.30, 1.4, 1 / 15, 2, "nero 5 % a 5 klx, 8x8 (estrapolato, vedi D: 304 mm)"),
    (1.00, 1.4, 1 / 30, 2, "L7CX 4x4 al buio su grigio 17 % (1,4 m): soglia 1,0 m"),
    (1.50, 1.4, 1 / 30, 2, "L8CX 4x4 a 5 klx su grigio 17 % (1,65 m): soglia 1,5 m"),
    (2.00, 1.4, 1 / 15, 1, "BRACCIO CHE DEVE FALLIRE: soglia 2 m, deve dare oltre 1 s"),
]
for soglia, v, per, n, nota in casi:
    r = preallarme(soglia, v, per, n)
    print("        ^", nota)
assert preallarme(2.0, 1.4, 1 / 15, 1)[0] > 1.0, "il braccio di controllo non si comporta come atteso"

# ---------------------------------------------------------------- B. copertura angolare e d'area
titolo("B. Copertura angolare e d'area")
CAM_H = 87.0
TOF_L7 = 60.0
TOF_L8 = 45.0
print(f"somma dei campi: camera {CAM_H} + 3 x {TOF_L7} = {CAM_H + 3*TOF_L7:.0f} gradi su 360 "
      f"({(CAM_H + 3*TOF_L7)/360*100:.0f} %); con L8CX: {CAM_H + 3*TOF_L8:.0f} gradi")
semi = CAM_H / 2
for asse in (90.0, 73.5):
    a0, a1 = asse - TOF_L7 / 2, asse + TOF_L7 / 2
    fessura = a0 - semi
    print(f"asse laterale a +-{asse:.1f}: il sensore copre {a0:.1f}..{a1:.1f}; fessura fra camera e sensore: "
          f"{max(0.0, fessura):.1f} gradi per lato")
R_DISCO = 3.0
disco = math.pi * R_DISCO ** 2
cam = math.pi * R_DISCO ** 2 * CAM_H / 360
print(f"disco di {R_DISCO} m: {disco:.2f} m2; settore della camera: {cam:.2f} m2 = {cam/disco*100:.1f} %")
for nome, campo, portata in (("L7CX al buio, bianco, 8x8", 60, 2.0), ("L7CX a 5 klx, bianco, 8x8", 60, 0.5),
                             ("L7CX a 5 klx, grigio 17 %, 8x8", 60, 0.35), ("L7CX a 5 klx, grigio 17 %, 4x4", 60, 0.55),
                             ("L8CX a 5 klx, grigio 17 %, 4x4", 45, 1.65), ("L8CX a 5 klx, grigio 17 %, 8x8", 45, 1.15)):
    a = 3 * math.pi * portata ** 2 * campo / 360
    print(f"  tre {nome:32s} portata {portata:4.2f} m: {a:5.2f} m2 = {a/disco*100:5.1f} % del disco")
# chi supera il sensore di fianco: a che distanza dalla camera entra nel campo frontale?
for portata in (0.5, 0.35, 1.0, 1.5):
    r_ingresso = portata / math.sin(rad(semi))
    print(f"  bersaglio che passa a {portata:.2f} m di lato (limite del sensore laterale): taglia la direzione "
          f"{semi:.1f} gradi a {r_ingresso:.2f} m dalla camera (zona di valutazione del nucleo: 1,24-3 m)")
# dimensione di una zona
for d in (0.5, 1.0, 2.0):
    print(f"  L7CX 8x8: una zona (7,5 gradi) a {d} m e' larga {2*d*math.tan(rad(3.75))*100:.1f} cm; "
          f"4x4 (15 gradi): {2*d*math.tan(rad(7.5))*100:.1f} cm")

# ---------------------------------------------------------------- C. persona in nero: quota del campo
titolo("C. Persona in nero vista come buco: quota dei pixel, delle direzioni e delle celle")
W, H = 848, 480
HF, VF = 87.0, 58.0
ALT, INCL = 1.2, 15.0     # SOLUZIONE_V2, B1: treppiede a 1,2 m, inclinata di 15 gradi
tx, ty = math.tan(rad(HF / 2)), math.tan(rad(VF / 2))
cp, sp = math.cos(rad(INCL)), math.sin(rad(INCL))


def quota_pixel(d, larg, alt_p=1.7, passo=2):
    dentro = tot = 0
    for v in range(0, H, passo):
        y = ty * (1 - 2 * (v + 0.5) / H)
        wy = y * cp - sp          # su
        wz = y * sp + cp          # avanti
        for u in range(0, W, passo):
            tot += 1
            if wz <= 0:
                continue
            x = tx * (2 * (u + 0.5) / W - 1)
            t = d / wz
            X, Y = x * t, ALT + wy * t
            if abs(X) <= larg / 2 and 0.0 <= Y <= alt_p:
                dentro += 1
    return dentro / tot


def quota_direzioni(d, larg):
    return 2 * math.degrees(math.atan(larg / 2 / d)) / HF


def quota_celle(d, larg, r0=1.24, r1=3.0):
    # celle della griglia polare (1 grado x 0,1 m) nella zona di valutazione che perdono il suolo dietro la sagoma
    fr_dir = quota_direzioni(d, larg)
    fr_rag = (r1 - max(d, r0)) / (r1 - r0) if d < r1 else 0.0
    return fr_dir * fr_rag


print("dist_m  larghezza_m  pixel_%  direzioni_%  celle_zona_%   (soglia del nucleo: validi sotto il 50 % della taratura)")
for d in (2.5, 1.0, 0.75, 0.6, 0.4):
    for larg in (0.5, 0.6):
        print(f"{d:6.2f} {larg:11.2f} {quota_pixel(d, larg)*100:8.1f} {quota_direzioni(d, larg)*100:12.1f} "
              f"{quota_celle(d, larg)*100:13.1f}")
for larg in (0.5, 0.6):
    d50 = larg / 2 / math.tan(rad(HF / 4))
    print(f"larghezza {larg} m: la quota di direzioni supera il 50 % sotto {d50:.2f} m")
assert quota_direzioni(0.4, 0.5) > 0.5, "il braccio di controllo (0,4 m) non supera il 50 %"
q = quota_pixel(2.5, 0.5) * 100
print(f"atto 1 della demo (meta' campo coperta: 50,0 % di buchi) piu' una persona in nero a 2,5 m nella meta' scoperta: "
      f"buchi {50 + q:.1f} %, validi {50 - q:.1f} % della taratura: sotto la soglia")
# raggio verso il basso che colpisce la gamba a quota h: dove toccherebbe il suolo (falso suolo se la profondita' e' sbagliata)
for h in (0.1, 0.2, 0.4, 0.6):
    print(f"  raggio che colpisce la persona a 2,5 m alla quota {h} m: prolungato tocca il suolo a "
          f"{2.5*ALT/(ALT-h):.2f} m")

# ---------------------------------------------------------------- D. portata del tempo di volo sul nero
titolo("D. Portata sul nero, estrapolata dalle tabelle 17 e 18 della scheda VL53L7CX (non e' una misura)")


def esponente(r_a, rho_a, r_b, rho_b):
    return math.log(r_a / r_b) / math.log(rho_a / rho_b)


tab = {
    "L7CX 8x8 15 Hz buio": (1600, 800),      # grigio chiaro 54 %, grigio 17 % (tipici, zona interna)
    "L7CX 8x8 15 Hz 5 klx": (400, 350),
    "L7CX 4x4 30 Hz buio": (2800, 1400),
    "L7CX 4x4 30 Hz 5 klx": (600, 550),
    "L8CX 8x8 15 Hz buio": (3300, 2450),
    "L8CX 8x8 15 Hz 5 klx": (1400, 1150),
    "L8CX 4x4 30 Hz 5 klx": (2600, 1650),
}
print("modo                      esponente   nero 5 %   nero 3 %   (mm; ancorato a 54 % e 17 %)")
for nome, (r54, r17) in tab.items():
    e = esponente(r54, 54, r17, 17)
    print(f"{nome:24s} {e:9.2f} {r17*(5/17)**e:10.0f} {r17*(3/17)**e:10.0f}")
print("con la legge della radice (limite di segnale): L7CX 8x8 al buio, nero 5 %:",
      f"{800*math.sqrt(5/17):.0f} mm; a 2,5 m servirebbe una portata {2500/(800*(5/17)**0.6):.1f} volte maggiore")

# ---------------------------------------------------------------- E. bus I2C e alternanza
titolo("E. Bus I2C con tre sensori")
FW = 0x8000 + 0x8000 + 0x5000
ris_pieno = 40 + 260 + 260 + 68 + 260 + 132 + 132 + 68 + 68 + 144 + 20
ris_min = 40 + 260 + 68 + 132 + 68 + 20        # ambiente, numero di bersagli, distanza, stato
print(f"firmware caricato a ogni avvio: {FW} byte per sensore (driver ST 1.2.3; il manuale UM3038 scrive ~84 kbyte)")
for f in (400e3, 1e6):
    print(f"  bus a {f/1e3:.0f} kHz: firmware {FW*9/f:.2f} s per sensore, {3*FW*9/f:.1f} s per tre; "
          f"risultati completi ({ris_pieno} byte) {ris_pieno*9/f*1000:.1f} ms a sensore, {3*ris_pieno*9/f*1000:.0f} ms per tre; "
          f"ridotti ({ris_min} byte) {3*ris_min*9/f*1000:.0f} ms per tre (periodo a 15 Hz: 66,7 ms)")
print("alternanza con start/stop su L7CX (nessun piedino di sincronia): per sensore almeno 2 fotogrammi "
      f"(il primo ha stato 6 o 10) = {2/15*1000:.0f} ms a 15 Hz; giro di tre = {3*2/15*1000:.0f} ms -> {15/6:.1f} Hz per sensore, "
      "senza contare il tempo di start e stop (non verificato)")

# ---------------------------------------------------------------- F. proiettore della camera come luce di fondo
titolo("F. Limite superiore dell'irraggiamento del proiettore sul bersaglio (se il filtro a 940 nm non respingesse niente)")
OH, OV = 90.0, 63.0                         # campo di proiezione, scheda RealSense tab. 3-17
omega = 4 * math.asin(math.sin(rad(OH / 2)) * math.sin(rad(OV / 2)))
print(f"angolo solido del proiettore: {omega:.3f} sr; riferimento ST: 2 W/m2 a 940 nm = 5 klx di luce diurna")
for p in (0.150, 0.360):
    for d in (0.5, 1.0, 2.0):
        e = p / (omega * d * d)
        print(f"  potenza {p*1000:.0f} mW, bersaglio a {d} m dalla camera: {e:.3f} W/m2 medi = {e/2*100:.0f} % del riferimento "
              f"(come {e/2*5:.2f} klx)")
