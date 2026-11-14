#!/usr/bin/env python3
"""Che cosa cambia nei limiti geometrici del nucleo al variare del campo del sensore.

Montaggio del nucleo (SOLUZIONE_V2, B1): ottica a 1,2 m da terra, inclinata di 15 gradi in basso.
  suolo_da   = h / tan(incl + V/2)            distanza dalla quale il pavimento entra nel campo (anello cieco)
  quota_3m   = h + 3 * tan(V/2 - incl)        quota massima vista a 3 m (bordo alto del campo)
  settori    = H                              settori da 1 grado coperti dalla griglia polare
  px_persona = larghezza_px / H * gradi sottesi da 0,5 m a 3 m   (pixel su una persona larga 0,5 m a 3 m)
Solo geometria: niente rumore, niente portata. Campi H x V: vedi la colonna «fonte».
"""
import math

H_CAM, INCL = 1.2, 15.0
SENSORI = [  # nome, H, V, larghezza in pixel del flusso di profondita', fonte del campo
    ("D435i / D455 (progetto del nucleo)", 87, 58, 848, "FONTI_VERIFICATE.md"),
    ("Gemini 335", 90, 65, 848, "FONTI_VERIFICATE.md"),
    ("Femto Bolt / Azure Kinect, campo stretto", 75, 65, 640, "pagina Microsoft aperta oggi"),
    ("Femto Bolt / Azure Kinect, campo largo 2x2", 120, 120, 512, "pagina Microsoft aperta oggi"),
    ("OAK-D Pro", 80, 55, 640, "pagina Luxonis aperta oggi (camere mono)"),
    ("OAK-D", 72, 49, 640, "pagina Luxonis aperta oggi (camere mono)"),
    ("OAK-D Lite", 73, 58, 640, "pagina Luxonis aperta oggi (camere mono)"),
    ("Kinect v1 (Xbox 360)", 57, 43, 640, "Wikipedia, testo grezzo aperto oggi"),
    ("Orbbec Astra (prima serie)", 58.4, 45.5, 640, "pagina Orbbec aperta oggi"),
    ("Kinect v2 (Xbox One)", 70, 60, 512, "MEMORIA, non verificato oggi"),
    ("RealSense L515", 70, 55, 640, "MEMORIA, non verificato oggi"),
    ("iPhone/iPad LiDAR (Stray Scanner)", 60, 45, 256, "IPOTESI, campo non verificato; 256 px verificati"),
]
print(f"{'sensore':44s} {'suolo da':>9s} {'quota a 3 m':>12s} {'settori':>8s} {'px persona 3 m':>15s}  fonte del campo")
for nome, h, v, w, fonte in SENSORI:
    basso = math.radians(INCL + v / 2)
    suolo = H_CAM / math.tan(basso) if basso < math.pi / 2 else 0.0
    quota = H_CAM + 3 * math.tan(math.radians(v / 2 - INCL))
    gradi_persona = 2 * math.degrees(math.atan(0.25 / 3))
    print(f"{nome:44s} {suolo:7.2f} m {quota:10.2f} m {h:8.0f} {w / h * gradi_persona:15.0f}  {fonte}")
