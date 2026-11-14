"""Prove di classe 1 per nuvole-punti-1 e nuvole-punti-2 (Python puro, un core).
Uso: python3 prova_np.py   Previsioni: PREVISIONI.md (scritte prima)."""
import math, time, statistics, random

NS, NB, DR = 87, 60, 0.1            # settori da 1 grado, celle radiali da 0,1 m fino a 6 m
AZ = [math.radians(-43.0 + s) for s in range(NS)]   # centro dei settori: -43..+43 gradi


def primo_ritorno(theta, segmenti):
    """segmenti: (y0, xa, xb, etichetta). Ritorna (distanza, etichetta) del primo colpo."""
    best = (float("inf"), None)
    for y0, xa, xb, lab in segmenti:
        x = y0 * math.tan(theta)
        if xa <= x <= xb:
            r = y0 / math.cos(theta)
            if r < best[0]:
                best = (r, lab)
    return best


def prova_np1a():
    L = [0.0] * (NS * NB)
    viol_A_vis = viol_A_ombra = viol_B = 0
    celle_ped_tot = 0
    for k in range(90):                       # 6 s a 15 Hz
        t = k / 15.0
        xc = -3.0 + 1.0 * t                   # pedone a 4 m, 1 m/s
        seg = [(5.0, -99, 99, "parete"), (4.0, xc - 0.25, xc + 0.25, "pedone")]
        if t >= 1.0:
            seg.append((2.0, -0.4, 0.4, "occlusore"))
        for s in range(NS):
            th = AZ[s]
            r, lab = primo_ritorno(th, seg)
            bh = int(r / DR)
            # verita': cella del pedone lungo questo settore (se il raggio lo interseca)
            xped = 4.0 * math.tan(th)
            ped_cell = int((4.0 / math.cos(th)) / DR) if (xc - 0.25 <= xped <= xc + 0.25) else None
            # accumulo log-odds (uguale per A e B)
            for b in range(min(bh, NB)):
                i = s * NB + b
                L[i] = max(-3.5, L[i] - 0.4)
            if bh < NB:
                i = s * NB + bh
                L[i] = min(3.5, L[i] + 0.85)
            if ped_cell is not None and ped_cell < NB:
                celle_ped_tot += 1
                libero_A = L[s * NB + ped_cell] < -1.0
                libero_B = libero_A and (ped_cell < bh)       # solo davanti al primo ritorno
                if libero_A:
                    if lab == "pedone":
                        viol_A_vis += 1
                    else:
                        viol_A_ombra += 1
                if libero_B:
                    viol_B += 1
    print("P-np1a  celle-pedone x fotogrammi:", celle_ped_tot)
    print("P-np1a  regola A: violazioni in ombra =", viol_A_ombra, "; col pedone visibile (ritardo) =", viol_A_vis)
    print("P-np1a  regola B: violazioni =", viol_B)


def prova_np1b():
    W, Hh = 160, 120
    hfov, vfov, pitch, hcam = math.radians(87), math.radians(58), math.radians(25), 1.2
    fx, fy = (W / 2) / math.tan(hfov / 2), (Hh / 2) / math.tan(vfov / 2)
    cp, sp = math.cos(pitch), math.sin(pitch)
    kh, kr, sec = [], [], []
    for v in range(Hh):
        for u in range(W):
            x, y = (u - W / 2 + 0.5) / fx, (v - Hh / 2 + 0.5) / fy   # raggio (x, y giu', 1) per profondita' unitaria
            fwd = cp - y * sp                 # avanti, orizzontale
            dwn = sp + y * cp                 # verso il basso
            kh.append(-dwn)                   # variazione di quota per unita' di profondita'
            kr.append(math.hypot(x, fwd))
            a = math.degrees(math.atan2(x, fwd))
            sec.append(min(NS - 1, max(0, int(a + 43.5))))
    n = W * Hh
    rnd = random.Random(1)
    # scena sintetica: suolo piano + una scatola (ostacolo) a 2 m in un terzo delle colonne
    depth = []
    for i in range(n):
        d = hcam / (-kh[i]) if kh[i] < -1e-6 else 0.0      # profondita' del suolo, 0 = nessun ritorno
        if d > 6.0:
            d = 0.0
        if 60 <= (i % W) < 110 and (d == 0.0 or d * kr[i] > 2.0):
            d = 2.0 / kr[i]
        depth.append(d * (1 + rnd.gauss(0, 0.01)) if d else 0.0)
    tempi = []
    for _ in range(20):
        t0 = time.perf_counter()
        rmin = [1e9] * NS
        g = [0] * (NS * NB)
        for i in range(n):
            d = depth[i]
            if d <= 0.0:
                continue
            h = hcam + kh[i] * d
            r = kr[i] * d
            s = sec[i]
            if 0.07 < h < 2.0:
                if r < rmin[s]:
                    rmin[s] = r
            elif h > -0.07:
                b = int(r * 10)
                if b < NB:
                    g[s * NB + b] += 1
        stato = bytearray(NS * NB)   # 0 non osservato, 1 libero osservato, 2 occupato, 3 in ombra
        for s in range(NS):
            bh = int(rmin[s] * 10)
            base = s * NB
            for b in range(NB):
                if b == bh:
                    stato[base + b] = 2
                elif b > bh:
                    stato[base + b] = 3
                elif g[base + b] >= 2:
                    stato[base + b] = 1
        tempi.append((time.perf_counter() - t0) * 1e3)
    c = [sum(1 for x in stato if x == k) for k in range(4)]
    print(f"P-np1b  misure={n}  celle={NS*NB}  mediana={statistics.median(tempi):.2f} ms  max={max(tempi):.2f} ms")
    print("P-np1b  celle [non osservato, libero, occupato, ombra] =", c)


def prova_np2():
    hs = 1.2
    def impronta(d, alfa_deg):
        th = math.atan2(hs, d); a = math.radians(alfa_deg) / 2
        return hs / math.tan(th - a) - hs / math.tan(th + a) if th - a > 0 else float("inf")
    print("P-np2  ToF 8x8 (45x45 gradi, 5,625 gradi/zona): 3 unita' =", 3 * 45, "gradi")
    for d in (1, 2, 4):
        wz = math.degrees(2 * math.atan(0.25 / d)) / 5.625
        hz = min(8.0, math.degrees(2 * math.atan(0.85 / d)) / 5.625)
        print(f"   pedone a {d} m: {wz:.2f} x {hz:.2f} zone = {wz*hz:.1f}")
    for d in (1, 2, 3):
        print(f"   impronta sul suolo a {d} m: {impronta(d, 5.625):.3f} m")
    fx, fy = 320 / math.tan(math.radians(43.5)), 240 / math.tan(math.radians(29))
    print("P-np2  camera 640x480 (87x58 gradi): 1 unita' = 87 gradi; 3 unita' =", 3 * 87, "gradi")
    for d in (1, 2, 4):
        wp, hp = min(640, 0.5 / d * fx), min(480, 1.7 / d * fy)
        print(f"   pedone a {d} m: {wp:.0f} x {hp:.0f} px = {wp*hp:.0f}")
    for d in (1, 2, 3, 4):
        print(f"   impronta sul suolo a {d} m: {impronta(d, 58/480):.4f} m")
    print("P-np2  LiDAR 2D 360 gradi, passo 0,8 gradi")
    for d in (1, 2, 4):
        print(f"   pedone a {d} m: {math.degrees(2*math.atan(0.25/d))/0.8:.1f} fasci")
    # rumore di profondita' stereo: dz = z^2 * subpixel / (f * B), classe D435 a 848x480
    f848 = 424 / math.tan(math.radians(43.5))
    for z in (1, 2, 3, 4):
        print(f"   stereo B=50 mm, f={f848:.0f} px, 0,1 px: errore di profondita' a {z} m = {z*z*0.1/(f848*0.05)*1000:.0f} mm")


if __name__ == "__main__":
    prova_np1a(); prova_np1b(); prova_np2()
