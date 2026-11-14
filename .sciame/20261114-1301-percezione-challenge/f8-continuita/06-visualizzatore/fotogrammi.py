#!/usr/bin/env python3
"""Scrive fotogrammi.svg: i fotogrammi chiave di «passa dietro» e «si ferma dietro», con la legenda.
Solo nero e bianco: ogni distinzione sta nella forma, nel tratto o nel tratteggio, mai nel colore.
I numeri (posizioni, raggi) vengono dal modello di punto_mostrato.py, geometria D, v = 1,1 m/s.
Rifare: timeout 120 python3 fotogrammi.py > risultati_fotogrammi.txt
"""
import math
import punto_mostrato as pm

G = dict(yp=1.9, yd=2.3, R=3.0)
V = 1.1
CELLS = pm.wedge_cells(G)
AREA_W = len(CELLS) * pm.CELL ** 2
W_OMBRA = G["yd"] / G["yp"]
X_IN, X_OUT = -0.5 * W_OMBRA, 0.5 * W_OMBRA
S = 70.0                      # pixel per metro
PW, PH = 236, 262             # riquadro di un fotogramma


def stima(t):
    """Media del filtro, baricentro troncato (c), raggi della regione al 50 % e al 90 % della
    distribuzione troncata al cuneo (insieme di massima densità: cerchio attorno alla media, ritagliato),
    quota del cuneo coperta dalla regione al 90 %, e massa troncata dentro il cerchio nominale al 95 %."""
    mx, my = X_IN + V * t, G["yd"]
    s2 = pm.var(t)
    rows = []
    sw = sx = sy = 0.0
    for (cx, cy) in CELLS:
        d2 = (cx - mx) ** 2 + (cy - my) ** 2
        w = math.exp(-0.5 * d2 / s2)
        rows.append((d2, w))
        sw += w; sx += w * cx; sy += w * cy
    rows.sort()
    acc = 0.0
    r50 = r90 = None
    n90 = 0
    m95 = 0.0
    r95sq = pm.CHI2_95 * s2
    for i, (d2, w) in enumerate(rows):
        acc += w
        if d2 <= r95sq:
            m95 += w
        if r50 is None and acc >= 0.5 * sw:
            r50 = math.sqrt(d2)
        if r90 is None and acc >= 0.9 * sw:
            r90 = math.sqrt(d2); n90 = i + 1
    return dict(mx=mx, my=my, cx=sx / sw, cy=sy / sw, r50=r50, r90=r90,
                quota90=n90 * pm.CELL ** 2 / AREA_W, m95=m95 / sw,
                largh90=math.sqrt(n90 * pm.CELL ** 2), sigma=math.sqrt(s2))


def P(x, y, ox, oy):
    return ox + S * x, oy - S * y


def wedge_path(ox, oy):
    a = math.atan2(0.5, G["yp"])
    xr, yr = G["R"] * math.sin(a), G["R"] * math.cos(a)
    p1 = P(-0.5, G["yp"], ox, oy); p2 = P(-xr, yr, ox, oy); p3 = P(xr, yr, ox, oy); p4 = P(0.5, G["yp"], ox, oy)
    r = G["R"] * S
    return "M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f Z" % (p1 + p2 + (r, r) + p3 + p4)


def frame(idx, col, row, titolo, sotto, stato, t, x_vero, scia_oss, mostra_vero=True, scarto=False, era_larga=False, etichetta_libero=False):
    """stato: 'oss' osservato, 'prev' previsto, 'larga' previsto oltre soglia, 'rioss' ricomparsa."""
    x0, y0 = 10 + col * (PW + 8), 10 + row * (PH + 34)
    ox, oy = x0 + PW / 2, y0 + PH - 14
    o = []
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="white" stroke="black" stroke-width="1"/>' % (x0, y0, PW, PH))
    o.append('<text x="%d" y="%d" font-size="11" font-weight="bold">%s</text>' % (x0 + 5, y0 + 13, titolo))
    o.append('<text x="%d" y="%d" font-size="10">%s</text>' % (x0 + 5, y0 + 26, sotto))
    wp = wedge_path(ox, oy)
    cid = "clip%d" % idx
    o.append('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, wp))
    # cuneo: senza traccia = solo contorno sottile; con traccia = «possibile presenza» (righe rade)
    if stato in ("oss", "rioss"):
        o.append('<path d="%s" fill="white" stroke="black" stroke-width="0.8"/>' % wp)
    elif stato == "larga":
        o.append('<path d="%s" fill="url(#rade)" stroke="none"/>' % wp)
        o.append('<path d="%s" fill="url(#contro)" stroke="black" stroke-width="2.4" stroke-dasharray="1.5 4.5" stroke-linecap="round"/>' % wp)
    else:
        o.append('<path d="%s" fill="url(#rade)" stroke="black" stroke-width="0.8"/>' % wp)
    # sensore, campo, pannello
    sx, sy = P(0, 0, ox, oy)
    for sg in (-1, 1):
        fx, fy = P(sg * 1.55, 1.55 / math.tan(pm.HALF_FOV), ox, oy)
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="1" stroke-dasharray="1 5"/>' % (sx, sy - 2, fx, fy))
    if etichetta_libero:
        o.append('<text x="%.1f" y="%.1f" font-size="9" text-anchor="middle">suolo visto libero</text>' % (ox, oy - 62))
        o.append('<text x="%.1f" y="%.1f" font-size="9" text-anchor="middle">in ombra</text>' % (ox, P(0, 2.62, ox, oy)[1]))
    o.append('<path d="M%.1f,%.1f l-6,9 l12,0 Z" fill="black"/>' % (sx, sy - 2))
    px1, py1 = P(-0.5, G["yp"], ox, oy)
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="7" fill="black"/>' % (px1, py1 - 3.5, S))
    o.append('<text x="%.1f" y="%.1f" font-size="9" text-anchor="middle">mezzo fermo</text>' % (ox, py1 + 15))
    yy = P(0, G["yd"], ox, oy)[1]
    e = stima(t) if t > 0 else None
    # scia osservata (linea piena) fino all'ingresso
    xa = P(scia_oss[0], 0, ox, oy)[0]; xb = P(scia_oss[1], 0, ox, oy)[0]
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="2"/>' % (xa, yy, xb, yy))
    if stato in ("prev", "larga", "rioss"):
        cxp, cyp = P(e["cx"], e["cy"], ox, oy)
        mxp, myp = P(e["mx"], e["my"], ox, oy)
        if stato == "prev":
            o.append('<g clip-path="url(#%s)">' % cid)
            o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="white" stroke="black" stroke-width="1.6" stroke-dasharray="5 3"/>' % (mxp, myp, e["r90"] * S))
            o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="url(#contro)" stroke="none"/>' % (mxp, myp, e["r90"] * S))
            o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="url(#fitte)" stroke="black" stroke-width="0.8" stroke-dasharray="2 2"/>' % (mxp, myp, e["r50"] * S))
            o.append('</g>')
        # scia prevista (tratteggiata) dall'ingresso al punto mostrato
        xi = P(X_IN, 0, ox, oy)[0]
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="2" stroke-dasharray="4 4"/>' % (xi, yy, cxp, cyp))
        if stato == "prev" or (stato == "rioss" and not era_larga):
            o.append('<circle cx="%.1f" cy="%.1f" r="6" fill="white" stroke="black" stroke-width="2"/>' % (cxp, cyp))
        else:
            o.append('<path d="M%.1f,%.1f h14 M%.1f,%.1f v14" stroke="black" stroke-width="2" fill="none"/>' % (cxp - 7, cyp, cxp, cyp - 7))
        if stato == "rioss" and scarto:
            xv, yv = P(x_vero, G["yd"], ox, oy)
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="1"/>' % (cxp, cyp - 12, xv, yv - 12))
            o.append('<path d="M%.1f,%.1f v8 M%.1f,%.1f v8" stroke="black" stroke-width="1"/>' % (cxp, cyp - 16, xv, yv - 16))
            o.append('<text x="%.1f" y="%.1f" font-size="9" text-anchor="middle">scarto %s m</text>'
                     % ((cxp + xv) / 2, cyp - 19, ("%.2f" % math.hypot(x_vero - e["cx"], G["yd"] - e["cy"])).replace(".", ",")))
    xv, yv = P(x_vero, G["yd"], ox, oy)
    if stato in ("oss", "rioss"):
        o.append('<circle cx="%.1f" cy="%.1f" r="6" fill="black"/>' % (xv, yv))
    elif mostra_vero:
        o.append('<path d="M%.1f,%.1f l6,6 M%.1f,%.1f l-6,6" stroke="black" stroke-width="1"/>' % (xv - 3, yv + 10, xv + 3, yv + 10))
    return "\n".join(o), e


def main():
    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="660" viewBox="0 0 1240 660" font-family="DejaVu Sans, Arial, sans-serif">')
    out.append('<rect width="1240" height="660" fill="white"/>')
    out.append('<defs>'
               '<pattern id="rade" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="9" stroke="black" stroke-width="1.5"/></pattern>'
               '<pattern id="contro" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="6" stroke="black" stroke-width="1.4"/></pattern>'
               '<pattern id="fitte" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="3" stroke="black" stroke-width="1.1"/></pattern>'
               '</defs>')
    buio = W_OMBRA / V
    print("Geometria D, v = %.2f m/s: ombra %.2f m alla persona, buio %.2f s, area del cuneo %.2f m2" % (V, W_OMBRA, buio, AREA_W))
    print("t s | media x | baricentro (c) x, y | r50 m | r90 m | regione 90 %: quota del cuneo, larghezza equivalente m | massa troncata dentro il cerchio nominale al 95 % ritagliato")
    soglia_t = None
    for k in range(1, 61):
        t = k * pm.DT
        e = stima(t)
        if soglia_t is None and e["quota90"] >= 0.5:
            soglia_t = t
        if k in (3, 5, 8, 12, 15, 17, 20, 23, 30, 45, 60) or abs(t - buio) < pm.DT / 2:
            print("%.2f | %+.2f | %+.2f, %.2f | %.2f | %.2f | %.2f, %.2f | %.3f"
                  % (t, e["mx"], e["cx"], e["cy"], e["r50"], e["r90"], e["quota90"], e["largh90"], e["m95"]))
    print("Soglia «larga» (regione al 90 %% >= meta' del cuneo) superata a t = %.2f s" % soglia_t)

    def n(x):
        return ("%.1f" % x).replace(".", ",")

    # Scena A: passa dietro
    A = [
        ("A1 · osservato", "0,3 s prima dell'ingresso", "oss", -0.3, X_IN - 0.33, (X_IN - 0.33 - 0.5, X_IN - 0.33), False),
        ("A2 · previsto", "non visto da 0,3 s", "prev", 0.3, X_IN + V * 0.3, (X_IN - 0.83, X_IN), False),
        ("A3 · previsto", "non visto da 0,8 s", "prev", 0.8, X_IN + V * 0.8, (X_IN - 0.83, X_IN), False),
        ("A4 · di nuovo osservato", "ricompare a %s s: dentro il 90 %%" % n(buio), "rioss", buio, X_OUT, (X_IN - 0.83, X_IN), True),
        ("A5 · osservato", "il tratto previsto resta tratteggiato", "rioss", buio, X_OUT + 0.33, (X_IN - 0.83, X_IN), False),
    ]
    for i, (tit, sot, st, t, xv, scia, sc) in enumerate(A):
        s, e = frame(i, i, 0, tit, sot, st, t, xv, scia, mostra_vero=False, scarto=sc, etichetta_libero=(i == 0))
        out.append(s)
        if st == "rioss" and not sc:
            # A5: scia osservata dopo la ricomparsa
            x0 = 10 + i * (PW + 8); ox = x0 + PW / 2; oy = 10 + PH - 14
            a = P(X_OUT, G["yd"], ox, oy); b = P(xv, G["yd"], ox, oy)
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="2"/>' % (a[0], a[1], b[0], b[1]))
    out.append('<text x="10" y="%d" font-size="12" font-weight="bold">Scena A — una persona passa dietro un mezzo fermo (vista dall\'alto; il sensore è il triangolo in basso)</text>' % (10 + PH + 18))

    # Scena B: si ferma dietro (a metà dell'ombra, 3 s)
    t_stop = 0.5 * W_OMBRA / V
    t_out = W_OMBRA / V + 3.0
    tB2 = soglia_t
    B = [
        ("B1 · previsto", "non visto da 0,5 s", "prev", 0.5, X_IN + V * 0.5, True),
        ("B2 · previsto, regione larga", "non visto da %s s: soglia superata" % n(tB2), "larga", tB2, 0.0, True),
        ("B3 · previsto, regione larga", "non visto da 3,0 s", "larga", 3.0, 0.0, True),
        ("B4 · di nuovo osservato", "ricompare a %s s (regione larga)" % n(t_out), "rioss", 3.0, X_OUT, True),
    ]
    for i, (tit, sot, st, t, xv, sc) in enumerate(B):
        s, e = frame(10 + i, i, 1, tit, sot, st, t, xv, (X_IN - 0.83, X_IN), scarto=(st == "rioss"), era_larga=True)
        out.append(s)
    yb = 10 + (PH + 34) + PH + 18
    out.append('<text x="10" y="%d" font-size="12" font-weight="bold">Scena B — la persona si ferma dietro per 3 s (la crocetta × sotto la linea è la posizione vera: sta solo in figura, non a schermo)</text>' % yb)

    # Legenda (nel riquadro in basso a destra della riga B e sotto)
    lx, ly = 10 + 4 * (PW + 8), 10 + (PH + 34)
    out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="white" stroke="black" stroke-width="1"/>' % (lx, ly, PW, PH))
    out.append('<text x="%d" y="%d" font-size="11" font-weight="bold">Legenda minima</text>' % (lx + 6, ly + 14))
    yy = ly + 34
    def riga(dy, disegno, testo1, testo2=""):
        o = [disegno % {"x": lx + 22, "y": yy + dy}]
        o.append('<text x="%d" y="%d" font-size="10">%s</text>' % (lx + 46, yy + dy + 1, testo1))
        if testo2:
            o.append('<text x="%d" y="%d" font-size="9">%s</text>' % (lx + 46, yy + dy + 12, testo2))
        return "\n".join(o)
    out.append(riga(0, '<circle cx="%(x)d" cy="%(y)d" r="6" fill="black"/>', "osservato: visto in questo ciclo", "disco pieno, scia a linea piena"))
    out.append(riga(34, '<circle cx="%(x)d" cy="%(y)d" r="6" fill="white" stroke="black" stroke-width="2"/>', "previsto: posizione più probabile", "anello vuoto, scia tratteggiata, età"))
    out.append('<rect x="%d" y="%d" width="30" height="20" fill="url(#contro)" stroke="black" stroke-width="1.6" stroke-dasharray="5 3"/>' % (lx + 8, yy + 58))
    out.append('<rect x="%d" y="%d" width="12" height="10" fill="url(#fitte)" stroke="black" stroke-width="0.8" stroke-dasharray="2 2"/>' % (lx + 17, yy + 63))
    out.append('<text x="%d" y="%d" font-size="10">dove può essere: 9 volte su 10</text>' % (lx + 46, yy + 67))
    out.append('<text x="%d" y="%d" font-size="9">(righe fitte: 1 su 2). NON è la taglia</text>' % (lx + 46, yy + 78))
    out.append('<rect x="%d" y="%d" width="30" height="20" fill="url(#rade)" stroke="black" stroke-width="0.8"/>' % (lx + 8, yy + 94))
    out.append('<text x="%d" y="%d" font-size="10">possibile presenza: tutta l\'ombra</text>' % (lx + 46, yy + 103))
    out.append('<text x="%d" y="%d" font-size="9">resta finché non lo si rivede</text>' % (lx + 46, yy + 114))
    out.append('<rect x="%d" y="%d" width="30" height="20" fill="url(#contro)" stroke="black" stroke-width="2.4" stroke-dasharray="1.5 4.5" stroke-linecap="round"/>' % (lx + 8, yy + 130))
    out.append('<path d="M%d,%d h14 M%d,%d v14" stroke="black" stroke-width="2" fill="none"/>' % (lx + 16, yy + 140, lx + 23, yy + 133))
    out.append('<text x="%d" y="%d" font-size="10">previsione larga (oltre soglia):</text>' % (lx + 46, yy + 139))
    out.append('<text x="%d" y="%d" font-size="9">bordo a punti, croce al posto dell\'anello</text>' % (lx + 46, yy + 150))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="black" stroke-width="1"/>' % (lx + 8, yy + 176, lx + 38, yy + 176))
    out.append('<path d="M%d,%d v8 M%d,%d v8" stroke="black" stroke-width="1"/>' % (lx + 8, yy + 172, lx + 38, yy + 172))
    out.append('<text x="%d" y="%d" font-size="10">scarto alla ricomparsa: fra il punto</text>' % (lx + 46, yy + 175))
    out.append('<text x="%d" y="%d" font-size="9">previsto e la prima misura</text>' % (lx + 46, yy + 186))
    out.append('<text x="%d" y="%d" font-size="9">Disco, anello e croce hanno taglia fissa:</text>' % (lx + 8, yy + 206))
    out.append('<text x="%d" y="%d" font-size="9">la taglia non dice mai l\'incertezza.</text>' % (lx + 8, yy + 217))

    # Nota di piede
    out.append('<text x="10" y="%d" font-size="10">Posizioni e raggi dal modello di punto_mostrato.py (geometria della demo, 1,1 m/s, q = 0,2 m²/s³): è un disegno di progetto, non una misura.</text>' % (yb + 22))
    out.append('<text x="10" y="%d" font-size="10">La regione è l\'insieme di massima densità della previsione troncata all\'ombra: dove il sensore vede suolo libero la regione è tagliata dal bordo dell\'ombra.</text>' % (yb + 36))
    out.append('</svg>')
    with open("fotogrammi.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("scritto fotogrammi.svg")


if __name__ == "__main__":
    main()
