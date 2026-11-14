# Attacco 5: lo strato 1 esteso alle "celle non osservate contigue". Griglia polare 1 grado x 0,1 m.
from collections import deque
from comune_f4 import *

ZP, WP, G = 1.5, 0.5, 0.40
HS = math.atan((WP / 2) / ZP)


def stato(bi, ri, solo_griglia):
    """bi: grado intero in [-180, 180); ri: decimetri. Ritorna 'L' libero, 'O' occupato, 'S' ombra, 'N' non osservato, None se la cella non esiste."""
    b = math.radians(bi + 0.5)
    r = ri / 10 + 0.05
    nel_campo = abs(b) <= FOV
    if solo_griglia and (not nel_campo or r < 0.5 or r > RMAX):
        return None
    if not nel_campo or r > RMAX or r < RNEAR:
        return 'N'
    if abs(b) <= HS:
        if ZP <= r < ZP + 0.1:
            return 'O'
        if r >= ZP + 0.1:
            return 'S'
    return 'L'


def riempi(rout, solo_griglia):
    nr = int(round(rout * 10))
    celle = {}
    for bi in range(-180, 180):
        for ri in range(nr):
            s = stato(bi, ri, solo_griglia)
            if s:
                celle[(bi, ri)] = s
    seme = (0, 25)
    assert celle[seme] == 'S'
    visti = {seme}
    coda = deque([seme])
    while coda:
        bi, ri = coda.popleft()
        for (db, dr) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = (bi + db + 180) % 360 - 180
            c = (nb, ri + dr)
            if c in celle and c not in visti and celle[c] in ('S', 'N'):
                visti.add(c)
                coda.append(c)
    return celle, visti


def area(c):
    return (c[1] / 10 + 0.05) * 0.1 * math.radians(1)


def xy(c):
    b = math.radians(c[0] + 0.5)
    r = c[1] / 10 + 0.05
    return r * math.sin(b), r * math.cos(b)


print("Attacco 5. Pannello 0,5 m a 1,5 m; riempimento per contiguita' (4 vicini) dalla cella d'ombra in cui entra la traccia.")
for (nome, rout, sg) in (("G1: celle anche oltre portata e fuori campo (definizione di PREVISIONI.md), fino a 4 m", 4.0, False),
                         ("G2: esistono solo le celle del campo fra 0,5 e 3 m", 3.0, True)):
    celle, s1 = riempi(rout, sg)
    non_oss = [c for c in celle if celle[c] in ('S', 'N')]
    liberi = [c for c in celle if celle[c] == 'L']
    ombra = [c for c in celle if celle[c] == 'S']
    print(nome)
    print("  (i) strato 1 = %.1f %% delle celle non osservate (%.1f %% in area); ombra del pannello = %.2f m2; strato 1 = %.2f m2" % (
        100 * len(s1) / len(non_oss), 100 * sum(map(area, s1)) / sum(map(area, non_oss)), sum(map(area, ombra)), sum(map(area, s1))))
    A_lib = sum(map(area, liberi))
    for (etic, sorg) in (("tutto lo strato 1", s1), ("la sola ombra del pannello", set(ombra))):
        pts = [xy(c) for c in sorg if abs(c[0]) <= 66 and c[1] <= 35]
        dentro = 0.0
        for c in liberi:
            x, z = xy(c)
            for (px, pz) in pts:
                if (px - x) ** 2 + (pz - z) ** 2 <= G * G:
                    dentro += area(c)
                    break
        print("  (ii) libero visto dentro la fascia di 0,40 m attorno a %s: %.1f %% (libero visto: %.2f m2)" % (etic, 100 * dentro / A_lib, A_lib))

# (iii) quando finisce il "previsto", tre denominatori
kx = KF1(0.0)
for _ in range(30):
    kx.pred(); kx.upd(0.0)
P0 = [row[:] for row in kx.P]
A_sh = HS * (RMAX ** 2 - ZP ** 2)
A_campo_lib = FOV * (RMAX ** 2 - RNEAR ** 2) - A_sh
print()
print("(iii) fine del 'previsto' (cerchio al 95 %% che copre >= meta' del denominatore), attore entrato a z = 2,5 m a 1,2 m/s; P a regime: sigma_p = %.3f m, sigma_v = %.3f m/s" % (
    math.sqrt(P0[0][0]), math.sqrt(P0[1][1])))


def fine(den, rout):
    k = KF1(0.0)
    k.P = [row[:] for row in P0]
    cx, cz = -2.5 * math.tan(HS), 2.5
    for f in range(1, 151):
        k.pred()
        cx += 1.2 * DT
        rc = math.sqrt(CHI95 * k.P[0][0])
        n = 2000
        n1 = n2 = n3 = 0
        for (px, pz) in disco(cx, cz, rc, n):
            if in_ombra_griglia(px, pz, HS, ZP):
                n1 += 1
            if not osservabile(px, pz, HS, ZP):
                n2 += 1
                if rout is None or math.hypot(px, pz) <= rout:
                    n3 += 1
        a = math.pi * rc * rc
        if den == 'ombra' and a * n1 / n >= 0.5 * A_sh:
            return f * DT, rc
        if den == 'ritagliato/ombra' and a * n2 / n >= 0.5 * A_sh:
            return f * DT, rc
        if den == 'strato1':
            A_s1 = math.pi * rout ** 2 - A_campo_lib
            if a * n3 / n >= 0.5 * A_s1:
                return f * DT, rc
    return None, rc


for (den, rout, nome) in (('ombra', None, "D-a: cerchio ∩ ombra in griglia / ombra in griglia (1,11 m2)"),
                          ('ritagliato/ombra', None, "D-c: cerchio ritagliato sul non osservato / ombra in griglia"),
                          ('strato1', 3.0, "D-b: denominatore = strato 1, non osservato rappresentato fino a 3 m"),
                          ('strato1', 4.0, "D-b: ... fino a 4 m"),
                          ('strato1', 6.0, "D-b: ... fino a 6 m"),
                          ('strato1', 10.0, "D-b: ... fino a 10 m")):
    t, rc = fine(den, rout)
    print("  %-70s -> %s" % (nome, ("'perso' a %.2f s (raggio %.2f m)" % (t, rc)) if t else "mai entro T_g = 10 s (raggio a 10 s: %.1f m)" % rc))
print()
A2 = 0.5 * 2 * math.atan(0.2 / 1.0) * (RMAX ** 2 - 1.0)
print("Variante, a conto: l'ombra di un giurato largo 0,4 m a 1 m vale %.2f m2; fusa con quella del pannello (%.2f m2) porta una copertura di 0,55 a %.2f:" % (A2, A_sh, 0.55 * A_sh / (A_sh + A2)))
print("  se 'perso' non e' assorbente (il testo tace) lo stato torna a 'previsto' senza nessuna misura.")
