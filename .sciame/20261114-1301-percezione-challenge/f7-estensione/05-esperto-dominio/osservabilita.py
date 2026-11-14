#!/usr/bin/env python3
"""Limiti di osservabilita' (P4) e ombra di un ostacolo basso (P5).
Solo calcolo, nessun dato casuale. Rifare: python3 -I osservabilita.py
Ipotesi dichiarate: camera 848x480, campo 87 x 58 gradi (D455, dal nucleo B1),
sensore a 1,2 m (dal nucleo B1). Il criterio 'N pixel di lato' e il tempo di
esposizione sono ipotesi mie, non dati del costruttore."""
import math

W, H, HFOV, VFOV = 848, 480, 87.0, 58.0
fx = W / (2 * math.tan(math.radians(HFOV / 2)))
fy = H / (2 * math.tan(math.radians(VFOV / 2)))
print(f"focale: fx = {fx:.1f} px, fy = {fy:.1f} px")

print("\n[P4a] impronta di un pixel e dimensione minima (N pixel di lato)")
print(" z[m]  impronta[mm]  N=3[cm]  N=5[cm]  N=8[cm]  cella 1 grado[cm]")
for z in (1.0, 2.0, 3.0, 4.0, 6.0):
    p = z / fx
    print(f" {z:4.1f}  {p*1000:10.1f}  {3*p*100:7.1f}  {5*p*100:7.1f}  {8*p*100:7.1f}"
          f"  {z*math.radians(1)*100:10.1f}")

print("\n[P4b] distanza massima a cui un oggetto di lato s copre N=5 pixel")
for s in (0.01, 0.02, 0.043, 0.10, 0.30):
    print(f" s = {s*100:5.1f} cm -> z_max = {s*fx/5:5.2f} m")

print("\n[P4c] velocita' massima seguibile, attraversamento del campo a distanza z")
print(" (k fotogrammi consecutivi in campo; corda = 2 z tan(HFOV/2))")
print(" z[m]  corda[m]  k=4@15  k=5@15  k=4@30  k=5@30   [m/s]")
for z in (1.0, 2.0, 3.0, 6.0):
    L = 2 * z * math.tan(math.radians(HFOV / 2))
    print(f" {z:4.1f}  {L:7.2f}  {L*15/4:6.1f}  {L*15/5:6.1f}  {L*30/4:6.1f}  {L*30/5:6.1f}")

print("\n[P4d] avvicinamento radiale da R: velocita' oltre la quale non restano")
print(" nemmeno i k=4 fotogrammi della conferma (tempo di reazione = 0)")
for R in (3.0, 6.0):
    for fps in (15, 30):
        print(f" R = {R:.0f} m, {fps} fot/s -> v = {R*fps/4:5.1f} m/s")

print("\n[P4e] spostamento fra due fotogrammi (porta di associazione) ")
for v in (2.5, 6.3, 10.0, 19.0):
    print(f" v = {v:4.1f} m/s -> {v/15*100:5.1f} cm a 15 fot/s, {v/30*100:5.1f} cm a 30 fot/s")

print("\n[P4f] mosso: spostamento durante l'esposizione, in pixel, a 3 m")
print(" (esposizione ipotizzata: 2, 8, 33 ms; NON verificata sul sensore)")
for v in (2.5, 6.3, 10.0, 19.0):
    row = [v * te * fx / 3.0 for te in (0.002, 0.008, 0.033)]
    print(f" v = {v:4.1f} m/s -> {row[0]:5.1f} px, {row[1]:5.1f} px, {row[2]:5.1f} px")
print(" caduta libera da 2 m: v = %.2f m/s" % math.sqrt(2 * 9.81 * 2))

print("\n[P5] ombra al suolo di un ostacolo alto a, a distanza d, sensore a h = 1,2 m")
print(" fine dell'ombra = d*h/(h-a); quota minima visibile dietro, a distanza x: h-(h-a)*x/d")
h = 1.2
print("  a[m]  d[m]  fine ombra[m]  quota del cuneo 2D davvero in ombra al suolo (fino a 3 m)  quota visibile a x=d+0,5 m")
for a in (0.3, 0.5, 0.8, 1.0):
    for d in (1.3, 1.5, 2.0, 2.5):
        end = d * h / (h - a)
        frac = min(1.0, (end - d) / (3.0 - d))
        x = d + 0.5
        ymin = max(0.0, h - (h - a) * x / d)
        print(f"  {a:3.1f}  {d:4.1f}  {end:8.2f}       {frac*100:6.1f} %"
              f"                                         {ymin:5.2f} m")
print(" ostacolo alto quanto il sensore o piu' (a >= h): l'ombra arriva al bordo (cuneo 2D esatto)")
