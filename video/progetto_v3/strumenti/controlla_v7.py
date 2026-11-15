#!/usr/bin/env python3
"""v7: controlli su un video reso, un fotogramma al secondo, a 1920x1080.
Q11 verde: pixel campionati ogni 2 px (960x540) con tinta 90-160°, saturazione > 0,3, luminosità 0,1-0,95;
  si riporta il massimo per fotogramma e, per il fotogramma peggiore, il raggruppamento (area connessa più grande,
  in pixel del campione) per confrontarlo con la soglia del piano (nessuna area > 50 px).
Q21 margini: pixel chiari (luminanza > 0,55) nella cornice esterna di 16 px (testo che tocca il bordo dello schermo).
Uso: python3 -I strumenti/controlla_v7.py VIDEO.mp4 > rapporto.txt
"""
import colorsys, subprocess, sys

W, H = 1920, 1080
v = sys.argv[1]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", v, "-vf", "fps=1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                     stdout=subprocess.PIPE)
n = W * H * 3
f = 0
peggiori = []
bordo_tot = []
while True:
    b = p.stdout.read(n)
    if len(b) < n:
        break
    verdi = set()
    for y in range(0, H, 2):
        base = y * W * 3
        for x in range(0, W, 2):
            i = base + x * 3
            r, g, bb = b[i], b[i + 1], b[i + 2]
            if g <= r and g <= bb:
                continue      # il verde ha g massimo o quasi: scarto rapido dei pixel senza componente verde dominante
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, bb / 255)
            if 90 <= h * 360 <= 160 and s > 0.3 and 0.1 < l < 0.95:
                verdi.add((x // 2, y // 2))
    # area connessa più grande (4-vicini)
    mx, vis = 0, set()
    for q in verdi:
        if q in vis:
            continue
        st, c = [q], 0
        vis.add(q)
        while st:
            a = st.pop(); c += 1
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                z = (a[0] + d[0], a[1] + d[1])
                if z in verdi and z not in vis:
                    vis.add(z); st.append(z)
        mx = max(mx, c)
    chiari = 0
    for y in list(range(0, 16)) + list(range(H - 16, H)):
        for x in range(0, W, 2):
            i = (y * W + x) * 3
            if (0.2126 * b[i] + 0.7152 * b[i + 1] + 0.0722 * b[i + 2]) / 255 > 0.55:
                chiari += 1
    for y in range(16, H - 16, 2):
        for x in list(range(0, 16)) + list(range(W - 16, W)):
            i = (y * W + x) * 3
            if (0.2126 * b[i] + 0.7152 * b[i + 1] + 0.0722 * b[i + 2]) / 255 > 0.55:
                chiari += 1
    peggiori.append((len(verdi), mx, f))
    bordo_tot.append((chiari, f))
    f += 1
peggiori.sort(reverse=True)
bordo_tot.sort(reverse=True)
print(f"fotogrammi analizzati (1/s): {f}")
print(f"Q11 verde: massimo {peggiori[0][0]} pixel di campione in un fotogramma (t={peggiori[0][2]} s), area connessa massima "
      f"{max(x[1] for x in peggiori)} px di campione (= circa x4 a 1080p); fotogrammi con verde > 0: {sum(1 for x in peggiori if x[0])}")
print("  primi 5:", peggiori[:5])
print(f"Q21 cornice di 16 px: massimo {bordo_tot[0][0]} pixel chiari (t={bordo_tot[0][1]} s); fotogrammi con pixel chiari: "
      f"{sum(1 for x in bordo_tot if x[0])}; primi 5: {bordo_tot[:5]}")
