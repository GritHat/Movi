#!/usr/bin/env python3
"""Ricalcoli del fascicolo «geometria d'osservazione e modello del sensore» (allegato tecnico).

Programma indipendente dai programmi d'origine: riscrive ogni formula; usa numpy e scipy.
Uso: <interprete dell'ambiente> -I -B ricalcoli.py > ricalcoli.txt   (vedi rifai.sh). Seme fisso.
Tutto e' conto o modello: nessun sensore fisico.
"""
import math
import numpy as np
from scipy.stats import norm, ncx2
from scipy.optimize import brentq

DEG = math.pi / 180
h, th, FOVh, FOVv = 1.2, 15 * DEG, 87 * DEG, 58 * DEG
Th, Tv = math.tan(FOVh / 2), math.tan(FOVv / 2)
RMAX = 3.0
rng = np.random.default_rng(20261114)


def tit(s):
    print("\n== " + s + " ==")


# ---------------------------------------------------------------- 1. camera
tit("1. Modello della camera")
for nome, W, H, fh, fv in (("D455 / D435i", 848, 480, 87, 58), ("Gemini 335", 848, 480, 90, 60)):
    print(f"{nome}: f dal campo orizzontale {W/2/math.tan(fh*DEG/2):.1f} px; dal verticale {H/2/math.tan(fv*DEG/2):.1f} px")
for f in (424.0, 410.7):
    print(f"f = {f} px a 848x480: campo orizzontale {2*math.atan(424/f)/DEG:.1f} gradi, verticale {2*math.atan(240/f)/DEG:.1f} gradi")
print(f"bordo basso {(th+FOVv/2)/DEG:.1f} gradi sotto l'orizzonte; bordo alto {(FOVv/2-th)/DEG:.1f} gradi sopra")

# ---------------------------------------------------------------- 2. suolo visibile
tit("2. Dove il suolo e' visibile")
zmin = h / math.tan(th + FOVv / 2)
print(f"z_min (suolo, ogni colonna) = h/tan(theta+FOVv/2) = {zmin:.4f} m")
for fi in (0, 20, 30, 43.5, 44):
    print(f"   azimut {fi:4.1f} gradi: rho_min = z_min/cos(phi) = {zmin/math.cos(fi*DEG):.3f} m")
xmax = Th * (zmin * math.cos(th) + h * math.sin(th))
print(f"   spigolo del campo sul suolo: x = +-{xmax:.3f} m, azimut {math.atan(xmax/zmin)/DEG:.1f} gradi, rho {math.hypot(xmax, zmin):.3f} m")
print(f"   bordo laterale del suolo visto: |x| <= {Th*math.cos(th):.4f} z + {Th*h*math.sin(th):.4f} (asintoto {math.atan(Th*math.cos(th))/DEG:.1f} gradi)")
zf = h / math.tan(th + math.atan(240 / 424))
print(f"   con f = 424 px (campo verticale 59,0): z_min = {zf:.4f} m; a 44 gradi {zf/math.cos(44*DEG):.3f} m; a 43,5 gradi {zf/math.cos(43.5*DEG):.3f} m")
for a in (0.07, 0.10, 0.15, 0.30):
    print(f"ostacolo alto {a:.2f} m: cima nel campo solo da z >= (h-a)/tan(44) = {(h-a)/math.tan(th+FOVv/2):.4f} m")
tetto = math.tan(FOVv / 2 - th)
print(f"tetto del campo: y_max(z) = {h} + {tetto:.4f} z")
for z in (1.243, 1.7, 1.9, 2.0, 2.3, 3.0):
    print(f"   z = {z} m: {h+tetto*z:.3f} m")
for y in (1.60, 1.70, 1.75, 1.80, 1.90, 2.00):
    print(f"   quota {y:.2f} m vista solo da z >= {(y-h)/tetto:.3f} m")

print("geometria per profilo (h = 1,2 m, theta = 15 gradi): z_min suolo / z ostacolo 0,15 m / pendenza del tetto / z per quota 1,8 m / tetto a 3 m")
for nome, fv in (("D455, D435i (58)", 58), ("Gemini 335 a 848x480 (60)", 60), ("Gemini 335 a 1280x800 (65)", 65), ("f = 424 px (59,0)", 2 * math.atan(240 / 424) / DEG)):
    bm, bp = th + fv * DEG / 2, fv * DEG / 2 - th
    print(f"   {nome}: {h/math.tan(bm):.3f} / {(h-0.15)/math.tan(bm):.3f} / {math.tan(bp):.4f} / {0.6/math.tan(bp):.3f} / {h+3*math.tan(bp):.3f}")
print("sensibilita' di z_min: campo verticale 58 -3/+3 gradi: %.3f / %.3f m; theta 15 -1/+1 gradi: %.3f / %.3f m; h 1,2 -0,05/+0,05 m: %.3f / %.3f m" % (
    h / math.tan(th + 55 * DEG / 2), h / math.tan(th + 61 * DEG / 2), h / math.tan(14 * DEG + FOVv / 2), h / math.tan(16 * DEG + FOVv / 2),
    1.15 / math.tan(th + FOVv / 2), 1.25 / math.tan(th + FOVv / 2)))
# verifica per lancio di raggi: griglia di pixel 848x480 con f dal campo dichiarato
fx, fy = 424 / Th, 240 / Tv
u = (np.arange(848) + 0.5 - 424) / fx
v = (np.arange(480) + 0.5 - 240) / fy
U, V = np.meshgrid(u, v)
den = math.sin(th) + V * math.cos(th)
ok = den > 1e-9
t = np.where(ok, h / np.where(ok, den, 1), np.nan)
X, Z = t * U, t * (math.cos(th) - V * math.sin(th))
print(f"lancio di raggi: min z al suolo {np.nanmin(Z):.4f} m (ultima riga: scarto fra le colonne {np.nanmax(Z[-1])-np.nanmin(Z[-1]):.2e} m)")
# frazione del disco di 3 m
A_disco = math.pi * RMAX ** 2
A_sett = FOVh / 2 * (RMAX ** 2 - zmin ** 2)
print(f"disco di 3 m: {A_disco:.3f} m2; settore d'anello 87 gradi fra z_min e 3 m: {A_sett:.3f} m2 = {100*A_sett/A_disco:.2f} %")
n = 3000
gx = (np.arange(n) + 0.5) / n * 2 * RMAX - RMAX
gz = (np.arange(n) + 0.5) / n * 2 * RMAX - RMAX
GX, GZ = np.meshgrid(gx, gz)
dentro = GX ** 2 + GZ ** 2 <= RMAX ** 2
vis = dentro & (GZ >= zmin) & (np.abs(GX) <= Th * (GZ * math.cos(th) + h * math.sin(th)))
cella = (2 * RMAX / n) ** 2
print(f"   regione esatta del foro stenopeico (z >= z_min, |x| <= T_h (z cos + h sin)) nel disco: {vis.sum()*cella:.3f} m2 = {100*vis.sum()/dentro.sum():.2f} %")
sett = dentro & (GZ > 0) & (np.abs(np.arctan2(GX, GZ)) <= FOVh / 2)
print(f"   settore di 87 gradi tagliato dalla retta z >= z_min: {(sett & (GZ>=zmin)).sum()*cella:.3f} m2 = {100*(sett & (GZ>=zmin)).sum()/dentro.sum():.2f} %")
A_tof = lambda nn, fov, port: nn * fov * DEG / 2 * port ** 2
for nn, fov, port in ((3, 60, 2.0), (2, 60, 2.0), (3, 45, 2.0), (3, 60, 1.0), (3, 60, 0.5)):
    print(f"   {nn} ToF da {fov} gradi fino a {port} m: {A_tof(nn,fov,port):.3f} m2 = {100*A_tof(nn,fov,port)/A_disco:.1f} % del disco")

# ---------------------------------------------------------------- 3. ombra
tit("3. Ombra")
for a, zo in ((1.0, 1.5), (0.5, 1.5), (0.3, 1.7), (0.4, 1.7), (0.5, 2.0), (1.0, 1.83), (1.2, 2.0)):
    fine = "infinito" if a >= h else f"{zo*h/(h-a):.2f} m"
    print(f"ostacolo alto {a} m a {zo} m: ombra al suolo fino a {fine}")
zp = 2.3
print("altezza minima del pannello a z_o che nasconde per intero una persona di statura s a z_p = 2,3 m: a = h + z_o * min((s-h)/z_p, tan 14)")
for s in (1.60, 1.70, 1.75, 1.80, 1.90):
    print(f"   s = {s:.2f}: " + "  ".join(f"z_o {zo}: {h+zo*min((s-h)/zp, tetto):.3f}" for zo in (1.15, 1.5, 1.7, 1.8, 1.9, 2.0)))
for a in (1.5, 1.6, 1.7, 1.8):
    print(f"   pannello alto {a}: a 2,3 m resta in vista sopra " + ", ".join(f"{h+(a-h)*zp/zo:.3f} m (z_o {zo})" for zo in (1.7, 1.9))
          + f"; tetto del campo a 2,3 m {h+tetto*zp:.3f}")
print("durata dell'occlusione totale: T = (L z_p/z_o - w)/v, w = 0,45 m, z_p = 2,3 m")
for L in (1.0, 2.0):
    for zo in (1.7, 1.8, 1.9):
        om = L * zp / zo
        print(f"   L = {L} z_o = {zo}: ombra {om:.3f} m, tratto nascosto {om-0.45:.3f} m: " + ", ".join(f"{(om-0.45)/vv:.2f} s a {vv} m/s" for vv in (1.4, 1.0, 0.5)))
print(f"   campo orizzontale a 1,8 m: {2*1.8*Th:.2f} m; a 2,3 m: {2*2.3*Th:.2f} m (sull'asse ottico orizzontale; ordine di grandezza)")
print("banda d'occlusione stereo: b (d_s - d_o)/d_o [m sullo sfondo], f b (1/d_o - 1/d_s) [px]")
CAM = {"D455": (424.0, 0.095), "D435i": (424.0, 0.050), "Gemini 335": (410.7, 0.050)}
for nome, (f, b) in CAM.items():
    for do, ds in ((1.0, 3.0), (1.5, 3.0), (2.0, 3.0), (1.0, 2.0)):
        print(f"   {nome}: ostacolo {do} m, sfondo {ds} m: {100*b*(ds-do)/do:.1f} cm = {f*b*(1/do-1/ds):.1f} px")
    print(f"   {nome}: banda al bordo sinistro dell'immagine f b/d: " + ", ".join(f"{f*b/d:.1f} px a {d} m" for d in (1, 2, 3)))
print(f"   ritardo di ricomparsa a 1,2 m/s per 0,19 m: {0.19/1.2:.3f} s")
# verifica numerica della banda: quali punti dello sfondo vede la sola camera sinistra
b, do, ds, xe = 0.095, 1.0, 3.0, 0.2
xs = np.linspace(-2, 3, 2000001)
visL = xs * do / ds < xe
visR = b + (xs - b) * do / ds < xe
print(f"   verifica numerica (b = 0,095; d_o = 1; d_s = 3): larghezza vista dalla sola sinistra {np.sum(visL & ~visR)*(xs[1]-xs[0]):.4f} m")

# ---------------------------------------------------------------- 4. rumore
tit("4. Rumore di profondita': sigma_z = d^2 sigma_d / (f b)")
PROF = {"D455": (424.0, 0.095, 0.08, 0.005), "D435i": (424.0, 0.050, 0.08, 0.010), "Gemini 335": (410.7, 0.050, None, 0.0075)}
for nome, (f, b, sd, klim) in PROF.items():
    knom = sd / (f * b) if sd else 0.004
    print(f"{nome}: f b = {f*b:.3f} px m; k_nom = {knom:.6f} 1/m (sigma_d {knom*f*b:.4f} px); k_lim = {klim} 1/m (sigma_d {klim*f*b:.4f} px)")
    print("   nominale [cm] a 1/2/3/4 m: " + " / ".join(f"{100*knom*d*d:.2f}" for d in (1, 2, 3, 4))
          + "   limite [cm]: " + " / ".join(f"{100*klim*d*d:.2f}" for d in (1, 2, 3, 4)))
    print("   passo di quantizzazione (1/32 px) [mm] a 1/2/3/4 m: " + " / ".join(f"{1000*d*d/(f*b)/32:.1f}" for d in (1, 2, 3, 4))
          + f"; scarto tipo della quantizzazione a 3 m: {1000*9/(f*b)/32/math.sqrt(12):.1f} mm")
    print("   distanza a cui sigma_z = 5 cm: nominale %.2f m, limite %.2f m" % (math.sqrt(0.05 / knom), math.sqrt(0.05 / klim)))
for z in (1.0, 2.0, 2.1, 3.0):
    a = 0.001063 + 0.0007278 * z + 0.003949 * z * z
    print(f"misura di terzi (D435): z = {z}: {100*a:.2f} cm; rapporto col nominale D435i {a/(0.08/(424*0.05)*z*z):.2f}; sigma_d equivalente {a*424*0.05/z/z:.3f} px")
print(f"quota temporale 0,6 e fissa sqrt(1-0,36) = {math.sqrt(1-0.36):.2f}")
for f, et in ((424 / Th, "f dal campo di 87 gradi"), (424.0, "f = 424 px"), (410.7, "f = 410,7 px")):
    print(f"impronta di un pixel ({et}, {f:.1f} px): " + ", ".join(f"{1000*d/f:.2f} mm a {d} m" for d in (2, 3, 6)) + f"; 5 pixel a 3 m = {100*5*3/f:.2f} cm; oggetto di 1 cm su 5 px entro {0.01*f/5:.2f} m")
print(f"rumore laterale: 1,5 px a 2 m (f = 424) = {1000*1.5*2/424:.1f} mm; limite misurato da terzi 4,3 / 4,1 cm")
print(f"sfocatura da moto a 1,5 m/s: {1000*1.5*0.008:.0f} mm con 8 ms, {1000*1.5*0.030:.0f} mm con 30 ms")
for r in (1.243, 2.0, 2.078, 2.5, 3.0):
    print(f"incidenza sul suolo a rho = {r}: {math.atan(r/h)/DEG:.1f} gradi dalla normale; distanza obliqua {math.hypot(r,h):.2f} m")
print(f"   60 gradi a rho = h tan 60 = {h*math.tan(60*DEG):.3f} m")

# ---------------------------------------------------------------- 5. errore di posa
tit("5. Errore di posa")
print("errore di quota di un punto del suolo: dy = rho sin(dth) + h (1 - cos(dth))")
for r, dg in ((2.8, 1.0), (2.0, 1.0), (3.0, 1.0), (2.0, 2.0), (3.0, 2.0)):
    d = dg * DEG
    print(f"   rho = {r} m, {dg} gradi: {100*(r*math.sin(d)+h*(1-math.cos(d))):.2f} cm (lineare {100*r*d:.2f} cm)")
print(f"   suolo oltre la soglia di 0,07 m con 2 gradi: da rho = {brentq(lambda r: r*math.sin(2*DEG)+h*(1-math.cos(2*DEG))-0.07, 0.1, 10):.3f} m")
for a in (0.10, 0.15):
    print(f"   ostacolo di {a:.2f} m sotto la soglia 0,07 m se rho*dth > {a-0.07:.2f} m: " + ", ".join(f"{(a-0.07)/r/DEG:.2f} gradi a {r} m" for r in (1.5, 2.0, 2.5, 3.0)))

print("   soglia d'errore oltre cui un ostacolo alto H a z = 2,55 m scende sotto 0,07 m: " + ", ".join(
    f"H = {H} cm: {brentq(lambda d: 2.55*math.sin(d)+h*(1-math.cos(d))-(H/100-0.07), 0, 0.2)/DEG:.2f} gradi" for H in (10, 12, 15)))
print("   scatola di 15 cm fra z = 2,00 e 2,15 m: " + ", ".join(f"{brentq(lambda d: zz*math.sin(d)+h*(1-math.cos(d))-0.08, 0, 0.2)/DEG:.2f} gradi a {zz} m" for zz in (2.0, 2.15)))


def wilson(k, n, zc=1.959964):
    p = k / n
    c = (p + zc * zc / 2 / n) / (1 + zc * zc / n)
    hw = zc * math.sqrt(p * (1 - p) / n + zc * zc / 4 / n / n) / (1 + zc * zc / n)
    return max(0.0, c - hw), min(1.0, c + hw)


print("   intervalli di Wilson al 95 %: " + "; ".join(f"{k}/{n}: [{wilson(k,n)[0]:.3f}, {wilson(k,n)[1]:.3f}]" for k, n in ((0, 10), (1, 10), (2, 10), (9, 10), (10, 10), (7, 7), (0, 7))))
# regola «mobile»: due medie di 3 fotogrammi a 13 fotogrammi (0,867 s), soglia K sigma per asse, K = 5 sqrt(2)/sqrt(3)
K = 5 * math.sqrt(2) / math.sqrt(3)
W = 13 / 15
sdiff = math.sqrt(2 / 3)                       # scarto tipo della differenza delle due medie, in sigma
pf = lambda dl: norm.sf((K - dl) / sdiff) + norm.sf((K + dl) / sdiff)     # dl = spostamento apparente / sigma
d10 = brentq(lambda x: pf(x) - 0.10, 0, 10)
d01 = brentq(lambda x: pf(x) - 0.01, 0, 10)
sig_t_deg = 1 / math.sqrt(12)
print(f"regola mobile: K = {K:.4f}; soglia trasversale {K*sig_t_deg:.3f} gradi; finestra {W:.4f} s")
print(f"   falsi 10 %: spostamento {d10:.4f} sigma = {d10*sig_t_deg:.4f} gradi sulla finestra = {d10*sig_t_deg/W:.3f} gradi/s")
print(f"   falsi  1 %: spostamento {d01:.4f} sigma = {d01*sig_t_deg:.4f} gradi sulla finestra = {d01*sig_t_deg/W:.3f} gradi/s")
# controllo Monte Carlo indipendente (numpy), 2 000 000 di valutazioni indipendenti
N = 2_000_000
for dl in (d10, d01):
    a = rng.normal(0, 1, (N, 3)).mean(1)
    bb = rng.normal(0, 1, (N, 3)).mean(1) + dl
    k = int((np.abs(bb - a) > K).sum())
    p = k / N
    zc = 1.959964
    c = (p + zc * zc / 2 / N) / (1 + zc * zc / N)
    hw = zc * math.sqrt(p * (1 - p) / N + zc * zc / 4 / N / N) / (1 + zc * zc / N)
    print(f"   Monte Carlo a {dl:.3f} sigma: {k} su {N} = {p:.4f}, Wilson 95 % [{c-hw:.4f}, {c+hw:.4f}]")
sr = lambda r: r * r * 0.08 / (424 * 0.05) if r <= 6 else 0.03
st = lambda r: r * DEG / math.sqrt(12)
for r in (2.0, 3.0, 10.0, 30.0):
    print(f"   Q2 a {r:4.0f} m: errore di velocita' al 10 %: trasversale {100*d10*st(r)/W:.1f} cm/s, radiale {100*d10*sr(r)/W:.1f} cm/s")
print(f"   Q3 gradino di velocita' angolare 30 gradi/s: tau = {1000*d10*sig_t_deg/30:.1f} ms (10 %), {1000*d01*sig_t_deg/30:.1f} ms (1 %)")


def frazione_sin(amp, fr, tau, nfasi=4000):
    """Frazione media di falsi con psi(t) = amp sin(2 pi fr t) e ritardo tau, medie di 3 fotogrammi, mediata sulla fase."""
    t0 = np.linspace(0, 1 / fr, nfasi, endpoint=False)
    e = lambda t: amp * (np.sin(2 * np.pi * fr * (t - tau)) - np.sin(2 * np.pi * fr * t))
    m1 = sum(e(t0 - k / 15) for k in range(3)) / 3
    m0 = sum(e(t0 - (13 + k) / 15) for k in range(3)) / 3
    dl = (m1 - m0) / sig_t_deg
    return float(np.mean(norm.sf((K - dl) / sdiff) + norm.sf((K + dl) / sdiff)))


for nome, amp, fr in (("volo stazionario +-3 gradi a 1 Hz", 3, 1.0), ("petto +-8 gradi a 1 Hz", 8, 1.0), ("testa +-30 gradi a 0,5 Hz", 30, 0.5)):
    tau = brentq(lambda x: frazione_sin(amp, fr, x) - 0.10, 1e-4, 0.2)
    print(f"   Q3 {nome}: tau al 10 % dei falsi = {1000*tau:.1f} ms")
print("   Q4 beccheggio: 10 % di celle di suolo oltre 0,07 m; sigma di quota = sigma_r h / distanza obliqua")
for rimb in (0.0, 0.025):
    out = []
    for r in (2.0, 3.0, 10.0, 30.0):
        sh = sr(r) * h / math.hypot(r, h)
        if rimb == 0:
            fq = lambda dd: norm.sf((0.07 - (r * math.sin(dd) + h * (1 - math.cos(dd)))) / sh) - 0.10
        else:
            ph = (np.arange(4000) + 0.5) / 4000 * 2 * np.pi
            fq = lambda dd: float(np.mean(norm.sf((0.07 - (r * math.sin(dd) + h * (1 - math.cos(dd))) - rimb * np.sin(ph)) / sh))) - 0.10
        out.append(f"{brentq(fq, 0, 5*DEG)/DEG:.3f} ({100*sh:.2f} cm)")
    print(f"      rimbalzo +-{100*rimb:.1f} cm: a 2/3/10/30 m [gradi (sigma di quota)]: " + " / ".join(out))
kk = math.sqrt(5.991 / (2 * 2.5257))
cop = lambda e: ncx2.cdf(5.991 / kk ** 2, 2, (e / kk) ** 2)
e90 = brentq(lambda e: cop(e) - 0.90, 0, 3)
print(f"   Q5 copertura a scostamento zero {1-math.exp(-2.5257):.4f}; copertura 0,90 a e = {e90:.3f} sigma")
for tt in (0.67, 1.0, 2.0):
    s = math.sqrt(0.03 ** 2 + (0.21 * tt) ** 2 + 0.2 * tt ** 3 / 3)
    print(f"      t = {tt} s: sigma {s:.3f} m, e = {e90*s:.3f} m -> " + " / ".join(f"{e90*s/r/DEG:.2f}" for r in (2, 3, 10, 30)) + " gradi a 2/3/10/30 m")
print("   Q6 margine di 0,10 m: " + " / ".join(f"{0.10/r/DEG:.2f} gradi" for r in (2, 3, 10, 30)) + "; ritardo a 30 gradi/s: "
      + " / ".join(f"{1000*0.10/r/(30*DEG):.0f} ms" for r in (2, 3, 10, 30)))
print(f"   memoria del libero: mezza cella radiale (0,05 m) in 2 passi a 15 Hz: {0.05/(2/15):.3f} m/s")

# ---------------------------------------------------------------- 6. ToF e LiDAR
tit("6. Tempo di volo multizona e LiDAR 2D")
for nome, fov, acc in (("VL53L7CX", 60.0, 0.05), ("VL53L8CX", 45.0, 0.05)):
    p8, p4 = fov / 8, fov / 4
    lato = 2 * 2 * math.tan(p8 * DEG / 2)
    print(f"{nome}: zona 8x8 {p8} gradi, 4x4 {p4} gradi; a 2 m lato {100*lato:.1f} cm (zona centrale su piano frontale {100*2*math.tan(p8*DEG):.1f}, d'angolo {100*2*(math.tan(fov/2*DEG)-math.tan((fov/2-p8)*DEG)):.1f}), diagonale {100*lato*math.sqrt(2):.1f} cm; campo intero a 2 m {2*2*math.tan(fov/2*DEG):.2f} m; "
          f"sigma = {100*acc/2.7:.2f} % = {100*2*acc/2.7:.1f} cm a 2 m; tre sensori {3*fov:.0f} x {fov:.0f} gradi; per 360 gradi ne servono {math.ceil(360/fov)}")
    for dist in (3.0, 4.0):
        print(f"   persona larga 0,5 m a {dist} m: {2*math.atan(0.25/dist)/DEG/p8:.2f} zone")
print(f"distanza obliqua minima fra un sensore a 1,2 m e il suolo: 1,20 m; a rho = 1 m {math.hypot(1,1.2):.2f} m; a 2 m {math.hypot(2,1.2):.2f} m")
for nome, ris in (("RPLIDAR C1", 0.72), ("LD19", 0.8)):
    print(f"{nome}: {360/ris:.0f} punti per giro; passo a 3 m {100*3*ris*DEG:.1f} cm; punti su 0,5 m a 3 m {0.5/(3*ris*DEG):.1f}; su 0,12 m a 5 m {0.12/(5*ris*DEG):.1f}; rotazione di 30 gradi/s in un giro di 0,1 s: 3 gradi = {30*3*DEG:.2f} m a 30 m")

# ---------------------------------------------------------------- 7. fascia e separazione
tit("7. Fascia di guardia e distanza di separazione")
eta, lat = 2 / 15, 0.155
print(f"eta' del libero (2 passi a 15 Hz) {eta:.4f} s + latenza {lat} s = {eta+lat:.4f} s")
for vm in (1.0, 1.4, 2.0, 2.5):
    print(f"   v_max = {vm} m/s: sola eta' {vm*eta:.3f} m; eta' + latenza {vm*(eta+lat):.3f} m; + e_ombra 0,20: {vm*(eta+lat)+0.20:.3f} m")
for g, eo in ((0.40, 0.0), (0.40, 0.20), (0.40, 0.30)):
    print(f"   fascia {g} m, e_ombra {eo}: velocita' coperta {(g-eo)/(eta+lat):.3f} m/s")
C, Zs = 0.85, 0.10
for vH in (1.6, 2.0):
    print(f"   S = v_H (T_R + T_S) + C + Z_S, v_H = {vH}: reazione umana 1,0 s: {vH*(lat+1.0)+C+Zs:.3f} m; arresto automatico 0,3 s: {vH*(lat+0.3)+C+Zs:.3f} m")
print(f"   velocita' coperta con 3 m di portata e 0,27 s di conferma (reazione 1 s): {(3-C-Zs)/(lat+1.0+0.27):.3f} m/s")

# ---------------------------------------------------------------- 8. latenza
tit("8. Bilancio di latenza")
voci = (("evento -> inizio esposizione (uniforme 0-33,3 ms)", 1000 / 30 / 2), ("esposizione -> fotogramma nell'applicazione, 30 fps", 95.0),
        ("fotogramma -> comando d'uscita", 22.0), ("campioni -> scheda audio (1024/48000)", 1000 * 1024 / 48000))
for n_, v_ in voci:
    print(f"   {n_}: {v_:.1f} ms")
tot = sum(v_ for _, v_ in voci)
print(f"   somma delle medie: {tot:.1f} ms; intervallo per la sola prima voce: {tot-1000/60:.1f}-{tot+1000/60:.1f} ms; 95-esimo percentile se le altre voci fossero costanti: {tot-1000/60+0.95*1000/30:.1f} ms")
for fps, m in ((15, 127), (60, 47), (90, 39)):
    print(f"   a {fps} fps: {1000/fps/2 + m + 22 + 1000*1024/48000:.1f} ms")
print(f"   modello del sensore: latenza della camera 70 ms nominale (36,8 + 34 = {36.8+34:.1f}), 120 ms limite")
