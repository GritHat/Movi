# AV4 (giro 2) — la cassa da 1 m con la persona dietro; proposta avversario-2 («taglio dal basso»).
# Giro 1 (av4_giro1.py): difetto del MIO banco, corretto qui: sceglievo il gruppo piu' grande, che era la faccia della cassa
# (a cavallo di due celle, meta' dei suoi pixel cade oltre il primo ritorno), non la persona.
# Rifare: timeout 120 python3 -I av4.py > risultati_av4.txt
import random, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim import *

NF = 10


def gruppi_oltre(D, k, pitch=15.0):
    """Gruppi di pixel-ostacolo oltre il primo ritorno, con la prova dei due bordi laterali riga per riga."""
    occ, suo, r0 = griglia_pixel(D, pitch)
    f, r_, u = assi(pitch)
    cand = {}
    for j in range(H):
        ty = TY[j]
        ky, kz = f[1] + ty * u[1], f[2] + ty * u[2]
        for i in range(W):
            d = D[j * W + i]
            if d == 0.0:
                continue
            x, y, z = d * TX[i], d * ky, CAMH + d * kz
            if not (0.07 <= z <= 2.0):
                continue
            c = cella_di(x, y)
            if c is None:
                continue
            cand.setdefault(c, []).append((i, j, d, x, y))
    forti = {c for c, v in cand.items() if len(v) >= 3}
    visti, out = set(), []
    for c in sorted(forti):
        if c in visti:
            continue
        comp, pila = [], [c]
        visti.add(c)
        while pila:
            a, r = pila.pop()
            comp.append((a, r))
            for da in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    n = (a + da, r + dr)
                    if n in forti and n not in visti:
                        visti.add(n)
                        pila.append(n)
        px = [p for cc in comp for p in cand[cc]]
        if len(px) < 50:
            continue
        righe = {}
        for (i, j, d, x, y) in px:
            righe.setdefault(j, []).append((i, d, x, y))
        passa = 0
        mx = my = nmid = 0.0
        for j, lst in righe.items():
            lst.sort()
            i0, d0 = lst[0][0], lst[0][1]
            i1, d1 = lst[-1][0], lst[-1][1]
            ok = False
            if i0 - 2 >= 0 and i1 + 2 < W:
                dl, dr_ = D[j * W + i0 - 2], D[j * W + i1 + 2]
                ok = dl != 0.0 and dr_ != 0.0 and dl > d0 + marg(d0, k) and dr_ > d1 + marg(d1, k)
            if ok:
                passa += 1
                mx += 0.5 * (lst[0][2] + lst[-1][2])
                my += 0.5 * (lst[0][3] + lst[-1][3])
                nmid += 1
        cx = sum(p[3] for p in px) / len(px)
        cy = sum(p[4] for p in px) / len(px)
        out.append(dict(primo=any(r == r0[a] for (a, r) in comp), npix=len(px), nrighe=len(righe), passa=passa, cx=cx, cy=cy,
                        mx=(mx / nmid if nmid else None), my=(my / nmid if nmid else None), celle=len(comp)))
    return out, r0, occ


def prova(nome, boxes, isogg, xc, yf, k, seme, nulli=()):
    clean, ID = render(boxes, 15.0, 6.0, True)
    rng = random.Random(seme)
    pv = sum(1 for n in range(W * H) if ID[n] == isogg and clean[n] != 0.0)
    acc = acc_righe = primo = 0
    falsi = []
    errs, errm, fraz = [], [], []
    ng = 0
    for t in range(NF):
        D = rumoroso(clean, ID, k, rng, nulli)
        gs, r0, occ = gruppi_oltre(D, k)
        # regola com'e' scritta: il soggetto entra nel filtro solo se una sua cella e' il primo ritorno del suo azimut
        cs = {}
        for n in range(W * H):
            if ID[n] == isogg and D[n] != 0.0:
                p = punto(n % W, n // W, D[n])
                c = cella_di(p[0], p[1])
                if c is not None and 0.07 <= p[2] <= 2.0:
                    cs[c] = cs.get(c, 0) + 1
        if any(v >= 3 and c[1] == r0[c[0]] for c, v in cs.items()):
            primo += 1
        ng += len(gs)
        vicini = [g for g in gs if math.hypot(g["cx"] - xc, g["cy"] - yf) <= 0.3 or (g["mx"] is not None and math.hypot(g["mx"] - xc, g["my"] - yf) <= 0.3)]
        for g in gs:
            ok = g["nrighe"] >= 10 and g["passa"] / g["nrighe"] >= 0.8
            if ok and g not in vicini and not g["primo"]:
                falsi.append((round(g["cx"], 2), round(g["cy"], 2), g["npix"]))
        if vicini:
            g = max(vicini, key=lambda g: g["npix"])
            fr_ = g["passa"] / g["nrighe"]
            fraz.append(fr_)
            if g["nrighe"] >= 10 and fr_ >= 0.8:
                acc += 1
                errs.append(math.hypot(g["cx"] - xc, g["cy"] - yf))
                errm.append(math.hypot(g["mx"] - xc, g["my"] - yf))
    print("%-38s k=%.4f pixel validi %5d | regola scritta: e' primo ritorno in %d/%d | componenti/fot %.1f | righe coi due bordi visti %s | avversario-2 accetta il soggetto in %d/%d, errore max: media dei pixel %s, punto medio dei bordi %s | accettate oltre il primo ritorno che non sono il soggetto: %d %s" % (
        nome, k, pv, primo, NF, ng / NF,
        ("%.2f-%.2f" % (min(fraz), max(fraz))) if fraz else "-",
        acc, NF, ("%.3f m" % max(errs)) if errs else "-", ("%.3f m" % max(errm)) if errm else "-", len(falsi), falsi[:3]))


cassa = (-0.4, 0.4, 1.7, 2.0, 0.0, 1.0)
pers = (-0.225, 0.225, 2.3, 2.55, 0.0, 1.75)
pann = (0.0, 1.0, 1.8, 1.85, 0.0, 2.0)
print("AV4 — 10 fotogrammi per riga; errore = distanza in pianta fra il centro stimato e il centro vero della faccia anteriore")
for k in (0.004, 0.0095):
    prova("(a) cassa 1 m, persona dietro", [cassa, pers], 1, 0.0, 2.3, k, 51)
    prova("(a2) cassa 0,5 m (atto 2), persona", [(-0.4, 0.4, 1.7, 2.0, 0.0, 0.5), pers], 1, 0.0, 2.3, k, 52)
    prova("(b) pannello 2 m, sporge 0,15 m", [pann, (-0.15, 0.30, 2.3, 2.55, 0.0, 1.75)], 1, 0.075, 2.3, k, 53)
    prova("(c) pannello 2 m, tutta nascosta", [pann, (0.30, 0.75, 2.3, 2.55, 0.0, 1.75)], 1, 0.525, 2.3, k, 54)
    prova("(d) [dopo] cassa 1 m, persona spostata", [cassa, (0.30, 0.75, 2.3, 2.55, 0.0, 1.75)], 1, 0.525, 2.3, k, 55)
    prova("(e) [dopo] cassa 1 m + pannello di lato", [cassa, (0.1, 1.0, 1.8, 1.85, 0.0, 2.0), (-0.20, 0.25, 2.3, 2.55, 0.0, 1.75)], 2, 0.025, 2.3, k, 56)
    prova("(f) [dopo] cassa 1 m, persona scura", [cassa, pers], 1, 0.0, 2.3, k, 57, nulli=(1,))
