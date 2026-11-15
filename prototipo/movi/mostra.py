"""Dal registro alle immagini (o a un filmato semplice, opencv). Tre viste affiancate, 1920×1080:

  1. SCENA VERA    — la verità in pianta (solo in simulazione; senza verità: «verità non nota»)
  2. CONSOLE       — ciò che il sistema dichiara: celle, tracce con lo stato a parole, regione di previsione, avviso
                     di possibile presenza (resta finché non si guarda), eventi (osservato | dedotto)
  3. SETTORI       — il livello per settore: «visto libero fino a d», «attenzione», «zona non verificata»

RIGA FISSA, su ogni immagine, sempre: «DATI SIMULATI — nessun sensore fisico · etichette a mano (classificatore
non realizzato) · regole accese: … · spente: … · config xxxxxxxx». Legge SOLO il registro: mai il nucleo."""
import math
import os

import numpy as np

from . import registro

L, H = 1920, 1080
VW, VH = 620, 820              # una vista
X0, X1, Y0, Y1 = -3.2, 3.2, -0.2, 3.3
COL_CELLA = {0: (60, 60, 60), 1: (90, 170, 90), 2: (60, 60, 210), 3: (110, 50, 30)}   # BGR
COL_LIV = {"visto_libero_fino_a": (90, 170, 90), "attenzione": (40, 160, 240), "zona_non_verificata": (120, 120, 120),
           "affidabilita_persa": (40, 40, 200)}
PAROLE = {"in_conferma": "in conferma", "vista": "vista", "vista_in_parte": "vista in parte",
          "non_vista": "non vista", "previsto_ampio": "previsto ampio (nessun punto)", "ricomparsa": "ricomparsa"}


def riga_fissa(intestazione):
    """Il testo della riga fissa dalle dichiarazioni dell'intestazione."""
    d = intestazione["dichiarazioni"]
    dati = "DATI SIMULATI" if d["dati"] == "simulati" else "DATI PUBBLICI, sensore simulato"
    return (f"{dati} — {d['hardware']} · etichette {d['etichette']} ({'classificatore ' + d['classificatore']}) · "
            f"accese: {', '.join(d['regole_accese']) or 'nessuna'} · spente: {', '.join(d['regole_spente']) or 'nessuna'}"
            f" · config {d['config']}")


def _px(x, y):
    return (int((x - X0) / (X1 - X0) * VW), int(VH - (y - Y0) / (Y1 - Y0) * VH))


class _Tavola:
    """Pixel della vista -> indice della cella polare (calcolato una volta)."""

    def __init__(self, g):
        u, v = np.meshgrid(np.arange(VW), np.arange(VH))
        x = X0 + (u + 0.5) / VW * (X1 - X0)
        y = Y0 + (VH - v - 0.5) / VH * (Y1 - Y0)
        ia = np.floor((np.degrees(np.arctan2(x, y)) + g["azimut_max_gradi"]) / g["passo_azimut_gradi"]).astype(int)
        ir = np.floor(np.hypot(x, y) / g["passo_distanza_m"]).astype(int)
        ok = (ia >= 0) & (ia < g["n_azimut"]) & (ir >= 0) & (ir < g["n_distanza"]) & (y > 0)
        self.idx = np.where(ok, ia * g["n_distanza"] + ir, -1)
        self.n = g["n_azimut"] * g["n_distanza"]
        self.g = g


def _testo(img, s, xy, scala=0.5, col=(235, 235, 235), sp=1):
    import cv2
    cv2.putText(img, _ascii(s), xy, cv2.FONT_HERSHEY_SIMPLEX, scala, col,
                sp, cv2.LINE_AA)


def _ascii(s):
    tab = str.maketrans({"à": "a'", "è": "e'", "é": "e'", "ì": "i'", "ò": "o'", "ù": "u'", "«": '"', "»": '"',
                         "—": "-", "·": "|", "×": "x", "≥": ">=", "≤": "<="})
    return s.translate(tab).encode("ascii", "replace").decode()


def disegna(intestazione, riga, tavola, larghezza=L, altezza=H):
    """Un fotogramma del registro -> immagine BGR (numpy uint8) con le tre viste e la riga fissa."""
    import cv2
    img = np.full((altezza, larghezza, 3), 25, np.uint8)
    viste = [np.full((VH, VW, 3), 35, np.uint8) for _ in range(3)]
    # 1. scena vera
    a = viste[0]
    for o in intestazione.get("ostacoli", []):
        pts = np.array([_px(*p) for p in o["punti"]], np.int32)
        cv2.fillPoly(a, [pts], (150, 150, 150))
    v = riga.get("verita")
    if v:
        for o in v["oggetti"]:
            c = (80, 220, 80) if o["visibile"] else (80, 80, 255)
            cv2.circle(a, _px(*o["pos"][:2]), 9, c, -1)
            _testo(a, f"{o['id']} {'visibile' if o['visibile'] else 'NASCOSTA'}", _px(o["pos"][0] + 0.12, o["pos"][1]))
    else:
        _testo(a, "verita' non nota", (20, 60))
    cv2.circle(a, _px(0, 0), 7, (255, 255, 255), -1)
    # 2. console
    b = viste[1]
    rle = riga["celle"].get("rle")
    if rle:
        stati = np.concatenate([np.full(n, registro.STATI_CELLA.index(s), np.uint8) for s, n in rle])
        lut = np.array([COL_CELLA[i] for i in range(4)], np.uint8)
        ok = tavola.idx >= 0
        b[ok] = lut[stati[tavola.idx[ok]]]
    over = np.zeros(tavola.n, bool)
    for av in riga["avvisi"]:
        over[av.get("indici", [])] = True
    ok = tavola.idx >= 0
    m = np.zeros(tavola.idx.shape, bool)
    m[ok] = over[tavola.idx[ok]]
    righe_tr = (np.arange(VH)[:, None] + np.arange(VW)[None, :]) % 8 < 3
    b[m & righe_tr] = (0, 140, 255)
    for tr in riga["tracce"]:
        reg = tr.get("regione")
        if reg and reg["tipo"] == "celle":
            mm = np.zeros(tavola.n, bool)
            mm[reg["indici"]] = True
            mk = np.zeros(tavola.idx.shape, bool)
            mk[ok] = mm[tavola.idx[ok]]
            b[mk] = (0.5 * b[mk] + 0.5 * np.array((0, 230, 255))).astype(np.uint8)
        elif reg and reg["tipo"] == "cerchio":
            cv2.circle(b, _px(*reg["centro"]), int(reg["raggio_m"] / (X1 - X0) * VW), (0, 230, 255), 2)
        if tr.get("pos"):
            cv2.circle(b, _px(*tr["pos"]), 6, (255, 255, 255), -1)
    y = 22
    for tr in riga["tracce"]:
        s = f"#{tr['id']} {tr['classe']} [{tr['origine_etichetta']}]: {PAROLE[tr['stato']]}"
        if tr["stato"] in ("non_vista", "previsto_ampio"):
            s += f" da {tr['non_vista_da_s']:.1f} s"
        if tr.get("identita"):
            s += f", identita' {tr['identita']}"
        if (tr.get("regione") or {}).get("livello_verificato") is False:
            s += " | regione al 90 % dichiarato, NON verificato"
        _testo(b, _ascii(s), (10, y), 0.45)
        y += 18
    for av in riga["avvisi"]:
        _testo(b, _ascii(f"AVVISO possibile presenza (traccia {av['id_traccia']}, da {av['eta_s']:.1f} s): "
                         "resta finche' non si guarda"), (10, y), 0.45, (0, 160, 255))
        y += 18
    yy = VH - 10
    for ev in reversed(riga["eventi"][-6:]):
        _testo(b, _ascii(f"{ev['t']:.2f} s {ev['tipo']} ({ev['come_lo_so']})"), (10, yy), 0.42, (200, 200, 120))
        yy -= 17
    # 3. settori
    c = viste[2]
    for s in riga["settori"]:
        a0, a1 = s["azimut_gradi"]
        d = s["d_m"] if s["livello"] == "visto_libero_fino_a" else 3.0
        pts = [_px(0, 0)] + [_px(d * math.sin(math.radians(t)), d * math.cos(math.radians(t)))
                             for t in np.linspace(a0, a1, 6)]
        cv2.fillPoly(c, [np.array(pts, np.int32)], COL_LIV[s["livello"]])
        cv2.polylines(c, [np.array(pts, np.int32)], True, (30, 30, 30), 1)
    for i, (k, col) in enumerate(COL_LIV.items()):
        cv2.rectangle(c, (10, 12 + 20 * i), (26, 26 + 20 * i), col, -1)
        _testo(c, _ascii(k.replace("_", " ")), (32, 25 + 20 * i), 0.45)
    titoli = ("1. SCENA VERA (simulazione)", "2. CONSOLE: cio' che il sistema dichiara", "3. LIVELLO PER SETTORE")
    for i, vv in enumerate(viste):
        x = 15 + i * (VW + 15)
        img[70:70 + VH, x:x + VW] = vv
        _testo(img, titoli[i], (x, 58), 0.7)
    _testo(img, _ascii(f"MoVi prototipo simulato | modo {riga['modo']} | t = {riga['t']:.2f} s | fotogramma "
                       f"{riga['indice']} | affidabilita': {riga['affidabilita']} | sensore: "
                       f"{riga['sensori'][0]['salute']} {riga['sensori'][0].get('causa') or ''}"), (15, 28), 0.65)
    tb = (riga.get("tabellone") or {}).get("dentro_la_zona")
    if tb:
        _testo(img, f"dentro la zona: {tb['k']} su {tb['n']}", (15, 920), 0.7, (0, 230, 255), 2)
    fissa = _ascii(riga_fissa(intestazione))
    _testo(img, fissa[:150], (15, 1010), 0.55, (0, 200, 255))
    _testo(img, fissa[150:], (15, 1035), 0.55, (0, 200, 255))
    _testo(img, "Solo osservazione e avviso: nessuna uscita e' un comando.", (15, 1062), 0.5)
    return img


def principale(percorso, uscita, filmato=False, ogni=1, fps=15):
    """Scrive in `uscita` le immagini PNG (una ogni `ogni` fotogrammi) o un filmato .mp4 (mp4v)."""
    import cv2
    righe = registro.leggi(percorso)
    testa = next(righe)
    if testa.get("modo") == "lungo":
        from . import mostra_lungo
        return mostra_lungo.principale(testa, righe, uscita, filmato, ogni, fps)
    tavola = _Tavola(testa["griglie"]["polare_corto"])
    os.makedirs(uscita, exist_ok=True)
    video, n = None, 0
    for r in righe:
        if r.get("tipo") != "fotogramma" or r["indice"] % ogni:
            continue
        img = disegna(testa, r, tavola)
        if filmato:
            if video is None:
                video = cv2.VideoWriter(os.path.join(uscita, "movi.mp4"), cv2.VideoWriter_fourcc(*"mp4v"),
                                        fps / ogni, (L, H))
            video.write(img)
        else:
            cv2.imwrite(os.path.join(uscita, f"{r['indice']:05d}.png"), img)
        n += 1
    if video is not None:
        video.release()
    print(f"{n} immagini in {uscita}" + (" (movi.mp4)" if filmato else ""))
