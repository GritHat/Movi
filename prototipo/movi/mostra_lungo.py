"""Viste del modo a LUNGA PORTATA, dal solo registro: pianta (sensori, coperture, ostacoli, celle, tracce con stato ed
età, regione di previsione TRATTEGGIATA, avviso di possibile presenza, distanza d'avviso richiesta) e console
dell'operatore (elenco delle tracce, salute dei sensori, eventi, tabellone). Riga fissa su ogni immagine:
«dati simulati · etichette a mano · sensori simulati dalle schede». La verità (croce bianca) c'è solo in simulazione."""
import math
import os

import numpy as np

from . import registro
from .mostra import _ascii

L, H = 1920, 1080
PW = 1240                                   # larghezza della pianta
COL = {0: (55, 55, 55), 1: (80, 150, 80), 2: (60, 60, 210), 3: (40, 75, 120)}       # BGR, ordine STATI_CELLA
COL_ST = {"vista": (90, 230, 90), "non_vista": (40, 200, 255), "previsto_ampio": (60, 120, 255)}
ARANCIO = (0, 140, 255)


def _t(img, s, xy, sc=0.5, col=(235, 235, 235), sp=1):
    import cv2
    cv2.putText(img, _ascii(str(s)), xy, cv2.FONT_HERSHEY_SIMPLEX, sc, col, sp, cv2.LINE_AA)


class _Mappa:
    def __init__(self, g):
        self.x0, self.x1 = g["x"]
        self.y0, self.y1 = g["y"]
        self.n = g["n"][0]
        self.s = min((PW - 40) / (self.x1 - self.x0), (H - 120) / (self.y1 - self.y0))
        self.ox, self.oy = 20, 60

    def px(self, x, y):
        return (int(self.ox + (x - self.x0) * self.s), int(self.oy + (self.y1 - y) * self.s))

    def m(self, d):
        return max(1, int(d * self.s))


def _tratteggio(img, c, r, col, n=36):
    import cv2
    for k in range(0, n, 2):
        cv2.ellipse(img, c, (r, r), 0, k * 360 / n, (k + 1) * 360 / n, col, 2, cv2.LINE_AA)


def disegna(testa, riga, griglia_celle):
    import cv2
    img = np.full((H, L, 3), 18, np.uint8)
    g = testa["griglie"]["pianta_lp"]
    M = _Mappa(g)
    lp = testa["lunga_portata"]
    # celle (ultima pianta registrata)
    if griglia_celle is not None:
        n = M.n
        dx, dy = (M.x1 - M.x0) / (n - 1), (M.y1 - M.y0) / (n - 1)
        over = img.copy()
        for j in range(n):
            for i in range(n):
                x, y = M.x0 + i * dx, M.y0 + j * dy
                a, b = M.px(x - dx / 2, y + dy / 2), M.px(x + dx / 2, y - dy / 2)
                cv2.rectangle(over, a, b, COL[int(griglia_celle[j][i])], -1)
        img = cv2.addWeighted(over, 0.55, img, 0.45, 0)
    # coperture dei sensori e sensori
    for s in testa["sensori"]:
        p = M.px(*s["pos"][:2])
        cop = s.get("copertura")
        if cop:
            a0, a1 = cop["az_gradi"]
            cv2.ellipse(img, p, (M.m(cop["r_max_m"]),) * 2, 0, -a1, -a0, (150, 150, 150), 1, cv2.LINE_AA)
        persa = any(x["id"] == s["id"] and x["salute"] == "affidabilita_persa" for x in riga["sensori"])
        cv2.drawMarker(img, p, (40, 40, 230) if persa else (255, 220, 120), cv2.MARKER_TRIANGLE_UP, 16, 2)
        _t(img, s["tipo"] + (" [AFFIDABILITA' PERSA]" if persa else ""), (p[0] + 8, p[1] + 16), 0.4,
           (40, 40, 230) if persa else (255, 220, 120))
    for o in testa.get("ostacoli", []):
        pts = np.array([M.px(*q[:2]) for q in o["punti"]], np.int32)
        cv2.fillPoly(img, [pts], (120, 120, 120))
        _t(img, o["id"], tuple(pts[0]), 0.4)
    # distanza d'avviso richiesta attorno al punto protetto
    q = lp.get("punto_protetto")
    if isinstance(q, str) and riga.get("verita"):
        q = next((o["pos"] for o in riga["verita"]["oggetti"] if o["id"] == q), None)
    d = lp.get("distanza_avviso_scenario_m")
    if q is not None and d:
        cv2.circle(img, M.px(*q[:2]), M.m(d), (200, 120, 255), 1, cv2.LINE_AA)
        _t(img, f"distanza d'avviso richiesta {d} m", (M.px(*q[:2])[0] + 6, M.px(q[0], q[1] + d)[1] + 14), 0.45,
           (200, 120, 255))
    # avvisi, regioni, tracce
    for a in riga["avvisi"]:
        f = a["forma"]
        if f["tipo"] == "cerchio":
            c = M.px(*f["centro"])
            cv2.circle(img, c, M.m(f["raggio_m"]), ARANCIO, 2, cv2.LINE_AA)
            _t(img, f"POSSIBILE PRESENZA #{a['id_traccia']} ({a['eta_s']:.0f} s)", (c[0] + 6, c[1] - M.m(f["raggio_m"]) - 4),
               0.45, ARANCIO)
        else:
            pts = np.array([M.px(*p) for p in f["punti"]], np.int32)
            cv2.polylines(img, [pts], True, ARANCIO, 3, cv2.LINE_AA)
            _t(img, f"POSSIBILE PRESENZA #{a['id_traccia']} (binario)", tuple(pts[0]), 0.45, ARANCIO)
    for tr in riga["tracce"]:
        p = tr["pos"] or tr["ultima_pos"][:2]
        c = M.px(*p[:2])
        col = COL_ST.get(tr["stato"], (200, 200, 200))
        if tr.get("regione"):
            _tratteggio(img, M.px(*tr["regione"]["centro"]), M.m(tr["regione"]["raggio_m"]), (255, 255, 0))
        if tr["stato"] == "vista":
            cv2.circle(img, c, 6, col, -1, cv2.LINE_AA)
        else:
            cv2.circle(img, c, 6, col, 1, cv2.LINE_AA)
        eta = "" if tr["non_vista_da_s"] is None else f" {tr['non_vista_da_s']:.0f} s"
        _t(img, f"#{tr['id']} {tr['stato'].replace('_', ' ')}{eta}", (c[0] + 8, c[1] - 6), 0.42, col)
    for o in (riga.get("verita") or {}).get("oggetti", []):
        cv2.drawMarker(img, M.px(*o["pos"][:2]), (255, 255, 255), cv2.MARKER_CROSS, 12, 1)
    # legenda
    y = H - 50
    for i, nome in enumerate(registro.STATI_CELLA):
        cv2.rectangle(img, (20 + 170 * i, y), (34 + 170 * i, y + 14), COL[i], -1)
        _t(img, nome.replace("_", " "), (40 + 170 * i, y + 12), 0.42)
    _t(img, "croce bianca: verita' (solo simulazione) | tratteggio: regione di previsione | arancio: avviso",
        (20, y - 12), 0.42, (200, 200, 200))
    _t(img, f"{lp['passaggio']['scenario']} | {testa['configurazione']['sorgente'].get('condizione')} | "
            f"quota della pianta {g['quota_m']:.0f} m | t = {riga['t']:.1f} s", (20, 30), 0.55)
    # console
    x0 = PW + 20
    cv2.rectangle(img, (PW, 0), (L, H), (30, 30, 30), -1)
    _t(img, "CONSOLE DELL'OPERATORE", (x0, 34), 0.7, (255, 255, 255), 2)
    _t(img, f"avviso a: {lp.get('a_chi') or lp['profilo_ricevente']}", (x0, 60), 0.42)
    _t(img, f"affidabilita' del sistema: {riga['affidabilita']}", (x0, 84), 0.5,
       (90, 230, 90) if riga["affidabilita"] == "ok" else (40, 40, 230))
    yy = 112
    for s in riga["sensori"]:
        _t(img, f"{s['id']}: {s['salute'].replace('_', ' ')}", (x0, yy), 0.42,
           (90, 230, 90) if s["salute"] == "in_salute" else (40, 40, 230))
        yy += 20
    yy += 10
    _t(img, "TRACCE (classe a mano | stato | eta' | sensori)", (x0, yy), 0.5, (255, 255, 255))
    yy += 24
    for tr in riga["tracce"][:16]:
        eta = "-" if tr["non_vista_da_s"] is None else f"{tr['non_vista_da_s']:.0f} s"
        _t(img, f"#{tr['id']} {tr['classe']} | {tr['parola'][:34]} | {eta} | {len(tr['sensori'])} sens.", (x0, yy), 0.4,
           COL_ST.get(tr["stato"], (200, 200, 200)))
        yy += 20
    if len(riga["tracce"]) > 16:
        _t(img, f"... altre {len(riga['tracce']) - 16}", (x0, yy), 0.4)
        yy += 20
    yy += 10
    _t(img, f"avvisi di possibile presenza accesi: {len(riga['avvisi'])}", (x0, yy), 0.5, ARANCIO)
    yy += 28
    _t(img, "EVENTI (osservato | dedotto)", (x0, yy), 0.5, (255, 255, 255))
    yy += 22
    for e in riga["eventi"][-6:]:
        _t(img, f"{e['t']:.1f} s {e['tipo']} [{e['come_lo_so']}]", (x0, yy), 0.4)
        yy += 18
    tb = riga.get("tabellone") or {}
    for k_, v in tb.items():
        _t(img, f"{k_.replace('_', ' ')}: {v['k']} su {v['n']}", (x0, H - 70 + 18 * list(tb).index(k_)), 0.42)
    # riga fissa
    cv2.rectangle(img, (0, H - 24), (L, H), (0, 0, 0), -1)
    d = testa["dichiarazioni"]
    dati = "dati simulati" if d["dati"] == "simulati" else "moto da dati pubblici, rilevazioni simulate"
    _t(img, f"{dati} | etichette {d['etichette']} | sensori simulati dalle schede | nessun sensore fisico | config {d['config']}",
       (10, H - 7), 0.5, (0, 220, 255))
    return img


def principale(testa, righe, uscita, filmato=False, ogni=1, fps=8):
    import cv2
    os.makedirs(uscita, exist_ok=True)
    g = testa["griglie"]["pianta_lp"]
    video, n, celle, primo_avviso = None, 0, None, False
    for r in righe:
        if r.get("tipo") != "fotogramma":
            continue
        if r["celle"].get("rle"):
            flat = [registro.STATI_CELLA.index(s) for s, k in r["celle"]["rle"] for _ in range(k)]
            if len(flat) == g["n"][0] * g["n"][1]:
                celle = np.asarray(flat).reshape(g["n"][1], g["n"][0])
        if r["indice"] % ogni:
            continue
        img = disegna(testa, r, celle)
        if filmato:
            if video is None:
                video = cv2.VideoWriter(os.path.join(uscita, "movi.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), fps, (L, H))
            video.write(img)
        if not filmato or r["indice"] % 40 == 0 or (r["avvisi"] and not primo_avviso):
            cv2.imwrite(os.path.join(uscita, f"{r['indice']:05d}.png"), img)
        primo_avviso = primo_avviso or bool(r["avvisi"])
        n += 1
    if video is not None:
        video.release()
    print(f"{n} immagini in {uscita}" + (" (movi.mp4)" if filmato else ""))
