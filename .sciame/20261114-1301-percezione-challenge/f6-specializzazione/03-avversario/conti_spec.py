# Conti dell'attacco alla specializzazione (avversario, f6). Python puro, seme fisso.
import math, random
rng = random.Random(20261114)
H, TILT, VF = 1.2, 15.0, 58.0
tb = math.tan(math.radians(TILT + VF / 2))
RN = H / tb
print("S1. Anello cieco: suolo visto da %.3f m. Un soggetto alto h a distanza d e' invisibile se h <= 1,2 - d*tan(44):" % RN)
for d in (0.5, 0.6, 0.8, 1.0):
    hmax = H - d * tb
    # copre il suolo da 1,24 m in poi? il raggio al suolo a distanza Dg passa a quota H*(1-d/Dg) sopra il punto d
    copre = [Dg for Dg in (RN + 0.001, 1.5, 2.0, 3.0) if H * (1 - d / Dg) < hmax - 1e-9]
    print("   d = %.1f m: invisibile fino a h = %.2f m; raggi al suolo coperti fra 1,24 e 3 m: %s -> settore: %s" % (
        d, hmax, copre if copre else "nessuno", "sconosciuto" if copre else "NESSUN OSTACOLO FINO ALLA PORTATA"))
# regola per settori su tre scene, e controllo contro la verita'
FOV = 43.5; ZP = 1.15; HS = math.degrees(math.atan(0.5 / ZP)); G = 0.40
def cella(bi, ri, pp):
    b = bi + 0.5; r = ri / 10 + 0.05
    if abs(b) > FOV: return 'N'
    if abs(b) <= HS and r >= ZP: return 'O' if r < ZP + 0.1 else 'S'
    if pp:
        x, z = r * math.sin(math.radians(b)), r * math.cos(math.radians(b))
        for sb in (-HS, HS):  # distanza dai due bordi del cuneo
            for rr in [ZP + 0.05 * i for i in range(int((3.0 - ZP) / 0.05) + 1)]:
                if (x - rr * math.sin(math.radians(sb))) ** 2 + (z - rr * math.cos(math.radians(sb))) ** 2 <= G * G: return 'P'
        if abs(b) <= HS and r >= ZP - G: return 'P'
    return 'L'
def settori(pp, larg=5):
    out = []
    b0 = -45
    while b0 < 45:
        dmin = 9
        for bi in range(b0, b0 + larg):
            d = 3.0
            for ri in range(12, 30):
                if cella(bi, ri, pp) != 'L':
                    d = max(RN, ri / 10) if ri > 12 else 0.0
                    break
            dmin = min(dmin, d)
        out.append((b0, 'sconosciuto' if dmin == 0.0 else ('nessun ostacolo' if dmin >= 3.0 else round(dmin, 2))))
        b0 += larg
    return out
for pp in (False, True):
    s = settori(pp)
    print("S1. Pannello 1 m a 1,15 m (semiangolo %.1f gradi), possibile presenza %s:" % (HS, "accesa" if pp else "spenta"))
    print("   ", " ".join("%d:%s" % (b, v) for b, v in s))
    # verita': soggetto nascosto al centro del cuneo a 2,3 m; settori che lo contengono (corpo 0,4 m)
    half = math.degrees(math.atan(0.2 / 2.3))
    bad = [(b, v) for b, v in s if b < half and b + 5 > -half and (v == 'nessun ostacolo' or (v != 'sconosciuto' and v > 2.3))]
    print("    settori con il soggetto nascosto a 2,3 m e valore oltre 2,3 m o 'nessun ostacolo': %d" % len(bad))
print("    (la smentita formale del testo e' una tautologia della regola: valore = prima cella non libera nella direzione peggiore)")
print()
print("S3. Fascia = max(0,20 + mezza larghezza, v_max*t) come nel testo, e come SOMMA dei tre termini; t = eta' + latenza 0,155 s")
for nome, v, w in (("persona", 2.5, 0.4), ("mezzo di piazzale", 8.0, 2.0), ("piccolo drone", 19.0, 0.4)):
    for sens, eta in (("camera", 2 / 15), ("LiDAR", 0.2)):
        t = eta + 0.155
        print("   %-18s %-6s solo eta': max %.2f m | con latenza: max %.2f m, somma %.2f m" % (
            nome, sens, max(0.2 + w / 2, v * eta), max(0.2 + w / 2, v * t), 0.2 + w / 2 + v * t))
t = 2 / 15 + 0.155
print("   Velocita' massima onesta con fascia 0,40 m e t = %.3f s: %.2f m/s (fascia come massimo); %.2f m/s (0,20 m di margine); %.2f m/s (0,10 m di margine, ombra a -20 cm)" % (
    t, 0.40 / t, 0.20 / t, 0.10 / t))
for v in (1.2, 1.4, 2.5, 8.0):
    print("   chi entra dal bordo della portata a %.1f m/s: 'nessun ostacolo fino a 3 m' e' onesto solo fino a %.2f m (t = %.3f s); con 0,1-0,5 s di ritardo del messaggio: %.2f-%.2f m" % (
        v, 3 - v * t, t, 3 - v * (t + 0.5), 3 - v * (t + 0.1)))
print()
print("S6b. Porta di +-2 gradi e +-5 cm sul piano ristimato a ogni fotogramma; soglia di 'occupato' 0,07 m")
for d in (2.0, 2.5, 3.0):
    for h in (0.15, 0.20):
        letto = h - d * math.tan(math.radians(2))
        print("   scatola di %.2f m a %.1f m con piano sbagliato di 2 gradi: quota letta %.3f m -> %s; con 2 gradi + 5 cm: %.3f m -> %s" % (
            h, d, letto, "occupato" if letto > 0.07 else "LIBERO (falso)", letto - 0.05, "occupato" if letto - 0.05 > 0.07 else "LIBERO (falso)"))
print("   Requisito Q4 dello stesso file a 3 m: 1,02 gradi; la porta ne ammette 2 a fotogramma, rispetto al precedente: fino a %.0f gradi/s di deriva" % (2 * 15))
print("S6c. Oltre 0,37 m/s vale solo il fotogramma corrente: settore di 5 gradi = 5 x 18 celle")
for p in (0.99, 0.95):
    n = sum(1 for _ in range(20000) if all(rng.random() < p for _ in range(90)))
    print("   suolo valido %.2f: 'nessun ostacolo fino alla portata' nel %.1f %% dei fotogrammi (conto: %.1f %%)" % (p, 100 * n / 20000, 100 * p ** 90))
print()
print("S7. Camera su un drone posato, a 0,25 m dal suolo (ipotesi mia), stessi 15 e 58 gradi:")
h = 0.25
print("   suolo visto da %.2f m; radenza al suolo a 3 m: %.1f gradi (a 1,2 m: %.1f); quota massima vista a 3 m: %.2f m (a 1,2 m: %.2f)" % (
    h / tb, math.degrees(math.atan(h / 3)), math.degrees(math.atan(1.2 / 3)), h + 3 * math.tan(math.radians(VF / 2 - TILT)), 1.2 + 3 * math.tan(math.radians(VF / 2 - TILT))))
print("   ogni ostacolo alto >= %.2f m fa ombra fino alla portata; a 1,2 m una cassa di 0,6 m a 1,15 m nasconde il suolo solo fino a %.2f m" % (h, 1.15 * 1.2 / (1.2 - 0.6)))
print("   rover a 0,5 m/s con t = %.3f s: %.2f m percorsi prima di ogni reazione; zona utile profonda %.2f m" % (t, 0.5 * t, 3 - RN))
