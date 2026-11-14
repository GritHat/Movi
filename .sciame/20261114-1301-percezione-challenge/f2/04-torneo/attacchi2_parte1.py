#!/usr/bin/env python3
"""Secondo script dell'avversario, parte 1. Python puro."""
import math, time, random
rad = math.radians
H = 1.2
print("=== P2c montaggio verticale (campo verticale 87 gradi) ===")
for vfov, nome in ((58.0, "orizzontale 87x58"), (87.0, "verticale 58x87")):
    for tilt in (0, 10, 15, 20):
        up, down = vfov / 2 - tilt, vfov / 2 + tilt
        ds = H / math.tan(rad(down))
        dt = (1.8 - H) / math.tan(rad(up)) if up > 0 else float("inf")
        print(f"  {nome}, inclinazione {tilt:2d}: suolo da {ds:4.2f} m; ostacolo a 1,8 m visibile oltre {dt:4.2f} m")

print("\n=== P8b scala in discesa da 2 m: lancio dei raggi contro 'suolo visto' ===")
# scala: alzata 0,17 m, pedata 0,30 m, comincia a x=2,0 m. Sensore a (0, 1,2). Raggio verso il basso con angolo a.
def quota_suolo(x):
    if x < 2.0: return 0.0
    return -0.17 * (int((x - 2.0) / 0.30) + 1)
celle = {}
for i in range(1, 600):
    a = rad(i * 0.1)                      # depressione del raggio
    x, z, colpito = 0.0, H, None
    while x < 6.0:                        # marcia del raggio a passi di 5 mm
        x += 0.005 * math.cos(a); z -= 0.005 * math.sin(a)
        if z <= quota_suolo(x): colpito = (x, z); break
    if not colpito: continue
    cx = round(colpito[0], 1)
    ostacolo = 0.07 < colpito[1] < 2.0    # nessun punto sopra il suolo in questa scena
    suolo_ok = abs(colpito[1]) <= 0.07
    # regola A (lancio dei raggi sui soli ostacoli): tutte le celle attraversate in pianta fino al ritorno sono 'libero'
    k = 0.1
    while k < colpito[0] - 1e-9:
        celle.setdefault(round(k, 1), {})["raggi"] = "libero"; k += 0.1
    # regola B (H-008): la cella del ritorno e' 'libero' solo se il suolo e' alla quota attesa
    c = celle.setdefault(cx, {})
    if suolo_ok: c["suolo"] = "libero"
    else: c.setdefault("suolo", "non osservato (suolo mancante)")
for cx in (1.5, 1.9, 2.0, 2.2, 2.5, 3.0):
    c = celle.get(cx, {})
    print(f"  cella {cx} m: lancio dei raggi -> {c.get('raggi','non osservato')}; suolo visto -> {c.get('suolo','non osservato')}; quota vera del suolo {quota_suolo(cx+0.05):+.2f} m")

print("\n=== P6c tempo del percorso critico minimo in Python puro (limite superiore grossolano) ===")
random.seed(1)
def prova(W, Hh, giri=5):
    n = W * Hh
    # tabelle per pixel (orientamento fisso): seno della depressione e settore polare
    sinv = [math.sin(rad(-29 + 58 * (i // W) / Hh + 15)) for i in range(n)]
    cosv = [math.cos(rad(-29 + 58 * (i // W) / Hh + 15)) for i in range(n)]
    sett = [int(87 * (i % W) / W) for i in range(n)]
    depth = [random.uniform(0.5, 6.0) for _ in range(n)]
    tempi = []
    for _ in range(giri):
        t0 = time.perf_counter()
        primo = [99.0] * 87; suolo = [0] * 87
        for i in range(n):
            r = depth[i]
            h = 1.2 - r * sinv[i]
            if 0.07 < h < 2.0:
                d = r * cosv[i]
                s = sett[i]
                if d < primo[s]: primo[s] = d
            elif -0.07 <= h <= 0.07:
                suolo[sett[i]] += 1
        tempi.append(time.perf_counter() - t0)
    tempi.sort()
    return 1000 * tempi[len(tempi) // 2]
for W, Hh in ((160, 120), (320, 240), (640, 480)):
    print(f"  {W}x{Hh}: mediana {prova(W, Hh):6.1f} ms per fotogramma (Python puro, un core)")
