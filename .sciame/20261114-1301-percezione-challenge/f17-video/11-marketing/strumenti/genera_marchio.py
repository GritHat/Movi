#!/usr/bin/env python3
"""Genera i file SVG del marchio SDMs e del marchio di parola MoVi.

Opera originale del gruppo SDMs. Le lettere vengono da Inter SemiBold (SIL OFL 1.1),
convertite in tracciati con fontTools: nessun font serve per aprire gli SVG.

Uso:  uv run --no-project --with fonttools python -I genera_marchio.py FONT.ttf CARTELLA_USCITA
"""
import math
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

# Colori (vedi GUIDA_MARCHIO.md): stessi codici della grammatica degli stati del video.
CIANO = "#3DD6E8"   # ciò che si vede (traccia vista: disco pieno)
AMBRA = "#F5A524"   # ciò che non si vede (zona tratteggiata, anello vuoto)
BIANCO = "#E8EDF2"  # testo
FONDO = "#0B0F17"   # fondo scuro di riferimento (non incluso negli SVG: fondo trasparente)

FONT = TTFont(sys.argv[1])
OUT = Path(sys.argv[2])
GS = FONT.getGlyphSet()
UPM = FONT["head"].unitsPerEm
CMAP = FONT.getBestCmap()


def nome(c):
    return CMAP[ord(c)] if len(c) == 1 else c


def tracciato(glifo, x, base, size):
    """Tracciato SVG del glifo, con l'origine sulla linea di base in (x, base)."""
    s = size / UPM
    pen = SVGPathPen(GS)
    GS[glifo].draw(TransformPen(pen, (s, 0, 0, -s, x, base)))
    return pen.getCommands()


def avanzamento(glifo, size):
    return GS[glifo].width * size / UPM


def limiti(glifo, size):
    bp = BoundsPen(GS)
    GS[glifo].draw(bp)
    return tuple(v * size / UPM for v in bp.bounds)  # xmin, ymin, xmax, ymax (y in su)


def contorni(glifo, size):
    """Limiti di ciascun contorno del glifo (per trovare il punto della i)."""
    rp = DecomposingRecordingPen(GS)
    GS[glifo].draw(rp)
    out, cur = [], []
    for op, args in rp.value:
        cur.append((op, args))
        if op in ("closePath", "endPath"):
            bp = BoundsPen(GS)
            for o, a in cur:
                getattr(bp, o)(*a)
            out.append(tuple(v * size / UPM for v in bp.bounds))
            cur = []
    return out


def anello_tratteggiato(cx, cy, r, w, colore, n=8, pieno=0.6):
    c = 2 * math.pi * r
    d, g = c / n * pieno, c / n * (1 - pieno)
    return (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" stroke="{colore}" '
            f'stroke-width="{w:.2f}" stroke-dasharray="{d:.3f} {g:.3f}" stroke-dashoffset="{d/2:.3f}" '
            f'stroke-linecap="butt"/>')


def svg(w, h, corpo, titolo, desc):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-labelledby="t d">\n'
            f'<title id="t">{titolo}</title>\n<desc id="d">{desc}</desc>\n'
            f'{corpo}\n</svg>\n')


# ---------------------------------------------------------------- simbolo SDMs
# Griglia 132 x 80. Disco pieno (visto) a sinistra; a destra la zona tratteggiata
# (non visto, posizione dichiarata) con dentro l'anello vuoto: il segno che resta.
def simbolo(ox, oy, k, c_visto, c_nonvisto):
    p = []
    p.append(f'<circle cx="{ox+30*k:.2f}" cy="{oy+40*k:.2f}" r="{22*k:.2f}" fill="{c_visto}"/>')
    p.append(anello_tratteggiato(ox + 94 * k, oy + 40 * k, 32 * k, 6 * k, c_nonvisto))
    p.append(f'<circle cx="{ox+94*k:.2f}" cy="{oy+40*k:.2f}" r="{9.5*k:.2f}" fill="none" '
             f'stroke="{c_nonvisto}" stroke-width="{5*k:.2f}"/>')
    return "\n".join(p)


SIMB_W, SIMB_H = 132, 80
desc_simb = ("Un disco pieno (ciò che si vede) e, accanto, una zona tratteggiata con un anello vuoto "
             "(ciò che non si vede, ma resta segnato).")
for suff, cv, cn in (("", CIANO, AMBRA), ("_mono", "#FFFFFF", "#FFFFFF"), ("_mono_scuro", FONDO, FONDO)):
    corpo = simbolo(2, 2, 1, cv, cn)
    (OUT / f"sdms_simbolo{suff}.svg").write_text(
        svg(SIMB_W + 4, SIMB_H + 4, corpo, "SDMs, simbolo", desc_simb))

# ---------------------------------------------------------------- logo SDMs (simbolo + parola)
SIZE_L = 76  # altezza delle maiuscole di Inter = 0,727 em -> circa 55 unità
caph = limiti(nome("H"), SIZE_L)[3]
base_l = 40 + caph / 2 + 2  # parola centrata otticamente sul simbolo
x = SIMB_W + 30
lettere = []
for ch in "SDMs":
    g = nome(ch)
    lettere.append((g, x))
    x += avanzamento(g, SIZE_L) + 0.5  # spaziatura leggermente aperta per la lettura a 64 px
xmax_testo = lettere[-1][1] + limiti(lettere[-1][0], SIZE_L)[2]
LOGO_W, LOGO_H = xmax_testo + 4, SIMB_H + 4
for suff, cv, cn, ct in (("", CIANO, AMBRA, BIANCO), ("_mono", "#FFFFFF", "#FFFFFF", "#FFFFFF"),
                         ("_mono_scuro", FONDO, FONDO, FONDO)):
    d = " ".join(tracciato(g, gx, base_l + 2, SIZE_L) for g, gx in lettere)
    corpo = simbolo(2, 2, 1, cv, cn) + f'\n<path fill="{ct}" d="{d}"/>'
    (OUT / f"sdms_logo{suff}.svg").write_text(
        svg(LOGO_W, LOGO_H, corpo, "SDMs, logo",
            desc_simb + " A destra la parola SDMs in Inter SemiBold, convertita in tracciati."))

# ---------------------------------------------------------------- marchio di parola MoVi
SIZE = 200
xh = limiti(nome("x"), SIZE)[3]
base = 44 + limiti(nome("M"), SIZE)[3]  # margine sopra le maiuscole: lascia posto al disco della i
pezzi = []  # (tipo, dati)
x = 8
gM = nome("M"); pezzi.append(("glifo", gM, x)); x += avanzamento(gM, SIZE)
# «o»: un anello tratteggiato al posto della lettera, con le sue misure ottiche
bo = limiti(nome("o"), SIZE)
ro_est = (bo[3] - bo[1]) / 2
w_o = 0.088 * SIZE  # un po' più sottile del tratto: con il tratteggio pesa come una lettera piena
o_cx = x + (bo[0] + bo[2]) / 2
o_cy = base - (bo[1] + bo[3]) / 2
pezzi.append(("anello", o_cx, o_cy, ro_est - w_o / 2, w_o))
x += avanzamento(nome("o"), SIZE) - 0.03 * SIZE  # crenatura «oV» a mano
gV = nome("V"); pezzi.append(("glifo", gV, x)); x += avanzamento(gV, SIZE) - 0.01 * SIZE
# «i»: la sola asta (ı) più un disco pieno al posto del punto
gi = nome("ı")
pezzi.append(("glifo", gi, x))
punto = max(contorni(nome("i"), SIZE), key=lambda b: b[1])  # il contorno più in alto è il punto
p_cx = x + (punto[0] + punto[2]) / 2
p_cy = base - (punto[1] + punto[3]) / 2
p_r = max(punto[2] - punto[0], punto[3] - punto[1]) / 2 * 1.12
pezzi.append(("disco", p_cx, p_cy - 0.02 * SIZE, p_r))
x_fine = x + limiti(gi, SIZE)[2]
WM_W = max(x_fine, p_cx + p_r) + 8
WM_H = base + 20


def wordmark(c_testo, c_o, c_punto):
    d, extra = [], []
    for p in pezzi:
        if p[0] == "glifo":
            d.append(tracciato(p[1], p[2], base, SIZE))
        elif p[0] == "anello":
            extra.append(anello_tratteggiato(p[1], p[2], p[3], p[4], c_o, n=8, pieno=0.70))
        else:
            extra.append(f'<circle cx="{p[1]:.2f}" cy="{p[2]:.2f}" r="{p[3]:.2f}" fill="{c_punto}"/>')
    return f'<path fill="{c_testo}" d="{" ".join(d)}"/>\n' + "\n".join(extra)


desc_wm = ("MoVi: la o è un anello tratteggiato (ciò che non si vede), il punto della i è un disco pieno "
           "(ciò che si vede). Lettere da Inter SemiBold convertite in tracciati.")
for suff, ct, co, cp in (("", BIANCO, AMBRA, CIANO), ("_mono", "#FFFFFF", "#FFFFFF", "#FFFFFF"),
                         ("_mono_scuro", FONDO, FONDO, FONDO)):
    (OUT / f"movi_wordmark{suff}.svg").write_text(svg(WM_W, WM_H, wordmark(ct, co, cp), "MoVi", desc_wm))

print(f"UPM={UPM} logo={LOGO_W:.1f}x{LOGO_H:.1f} wordmark={WM_W:.1f}x{WM_H:.1f} xh={xh:.1f} "
      f"o: r={ro_est - w_o/2:.1f} w={w_o:.1f}; punto r={p_r:.1f}")
