#!/usr/bin/env python3
"""A6, A7, A8 — attacchi che usano il simulatore di 11-simulatore (importato, sola lettura; parametri cambiati IN MEMORIA).
  a6  l'ingrossamento dei bordi (ipotesi senza misura) decide il segno dell'errore dell'ombra?
  a7  tre fotogrammi della verità rifatti con geometria mia, e la maschera d'ombra a 2,45 m
  a8  la soglia 40 fuori dalla geometria su cui è stata scelta (linea a 2,1 m; 848×480)
Uso: <python> -I -B a678_sim.py a6|a7|a8 [...]"""
import dataclasses
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import av_comune as A                                          # noqa: E402
sys.path.insert(0, A.VAL)
sys.path.insert(0, A.SIM)
import numpy as np                                             # noqa: E402
import comune as K                                             # noqa: E402  (validazione: corri, Parametri, wilson)
import catalogo as C                                           # noqa: E402
import genera as G                                             # noqa: E402
import simsens as S                                            # noqa: E402
from catena import Catena                                      # noqa: E402

_carica = S.carica_profilo
CAMBI = {}


def carica_con_cambi(sigla, livello="nominale", larghezza=424, **kw):
    p = _carica(sigla, livello, larghezza=larghezza, **kw)
    p.update(CAMBI)
    return p


S.carica_profilo = carica_con_cambi


def genera(spec, larghezza=424, interruttori=None):
    tempi, quadri, vers, extra = [], [], [], None
    for i, t, f, ver, extra in G.simula(spec, larghezza=larghezza, interruttori=interruttori):
        tempi.append(t)
        quadri.append(f)
        vers.append(ver)
    meta, verita = G.meta_e_verita(spec, extra["prof"], extra["cam"], extra["scena"], extra["tracce"], vers)
    return meta, tempi, quadri, verita


# ------------------------------------------------------------------------------------------------ A6
def a6(mezza=0.5):
    import misura_ombra as MO
    C.PANNELLO = dict(C.PANNELLO, x0=-mezza, x1=mezza)
    vero = math.degrees(math.atan2(mezza, 1.8))
    print(f"spigoli veri del pannello: ±{vero:.2f}°; errore in cm a 2,4 m, + = ombra stimata più larga")
    for nome, cambi, inter in (("ingrossamento 2 px (come il simulatore: controllo)", {}, None),
                               ("ingrossamento 0 px", {"bordo_ingrossamento_px": 0}, None),
                               ("ingrossamento 0 e pixel misti 0", {"bordo_ingrossamento_px": 0, "bordo_misti_px": 0.0}, None),
                               ("interruttore «bordi» spento (nessun modello dei bordi)", {}, {"bordi": False})):
        CAMBI.clear()
        CAMBI.update(cambi)
        for p_min in (3, 40):
            sx, dx, minimi = [], [], []
            for k in range(10):
                spec = C._spec("statiche", "d435i", "nominale", "pannello", f"pannello_vuoto_av{k:02d}", n=10)
                meta, tempi, quadri, _ = genera(spec, interruttori=inter)
                cat = Catena(meta, dataclasses.replace(K.Parametri(), min_punti_ostacolo=p_min))
                es, ed = [], []
                for i, (t, f) in enumerate(zip(tempi, quadri)):
                    cat.ciclo(i, t, f)
                    b = MO.bordi(cat.mappa_ciclo.stati)
                    if b is None:
                        continue
                    es.append((-vero - b[0]) * math.pi / 180 * 2.4 * 100)
                    ed.append((b[1] - vero) * math.pi / 180 * 2.4 * 100)
                sx += es
                dx += ed
                minimi.append((min(es), min(ed)))
            tutti = np.array(sx + dx)
            print(f"{nome}; soglia {p_min}: 10 sequenze, {len(sx)} fotogrammi; sinistra min/mediana/max {min(sx):+.1f}/{np.median(sx):+.1f}/{max(sx):+.1f}; "
                  f"destra {min(dx):+.1f}/{np.median(dx):+.1f}/{max(dx):+.1f}; lati-sequenza con minimo < 0: "
                  f"{sum(1 for a, b in minimi for v in (a, b) if v < 0)} su 20; fotogrammi-lato < 0: {int((tutti < 0).sum())} su {len(tutti)}")
    CAMBI.clear()


# ------------------------------------------------------------------------------------------------ A7
def raggi(meta):
    t = math.radians(meta["posa"]["inclinazione_gradi"])
    u = (np.arange(meta["larghezza"]) - meta["cx"]) / meta["fx"]
    v = (np.arange(meta["altezza"]) - meta["cy"]) / meta["fy"]
    xn, yn = np.meshgrid(u, v)
    return xn, math.cos(t) - yn * math.sin(t), -(yn * math.cos(t) + math.sin(t))      # dx, dz, dq (per Zc = 1)


def t_scatola(h, dx, dz, dq, x0, x1, z0, z1, q0, q1):
    with np.errstate(divide="ignore", invalid="ignore"):
        tx = np.sort(np.stack([(x0 - 0.0) / dx, (x1 - 0.0) / dx]), axis=0)
        tz = np.sort(np.stack([(z0 - 0.0) / dz, (z1 - 0.0) / dz]), axis=0)
        tq = np.sort(np.stack([(q0 - h) / dq, (q1 - h) / dq]), axis=0)
    t_in = np.maximum(np.maximum(tx[0], tz[0]), tq[0])
    t_out = np.minimum(np.minimum(tx[1], tz[1]), tq[1])
    return np.where((t_in <= t_out) & (t_out > 0), np.maximum(t_in, 0), np.inf)


def t_capsula(h, dx, dz, dq, xc, zc, r=0.2, alt=1.7, passi=4000, t_max=6.0):
    """Marcia lungo il raggio (via diversa dalla forma chiusa del simulatore): primo t con il punto dentro la capsula."""
    ts = np.linspace(0.5, t_max, passi)
    t = np.full(dx.shape, np.inf)
    for tk in ts[::-1]:                                       # dal fondo verso la camera: resta il più vicino
        x, z, q = tk * dx, tk * dz, h + tk * dq
        d2 = (x - xc) ** 2 + (z - zc) ** 2
        dentro = ((q >= 0) & (q <= alt - r) & (d2 <= r * r)) | ((q > alt - r) & (d2 + (q - (alt - r)) ** 2 <= r * r))
        t = np.where(dentro, tk, t)
    return t


def a7():
    nome = "d435i_nom__pannello_a12__s00"
    cart = os.path.join(A.SEQ_SIM, nome)
    meta = json.load(open(os.path.join(cart, "meta.json"), encoding="utf-8"))
    ver = json.load(open(os.path.join(cart, "verita.json"), encoding="utf-8"))
    h = meta["posa"]["altezza_m"]
    dx, dz, dq = raggi(meta)
    tp = t_scatola(h, dx, dz, dq, -0.5, 0.5, 1.80, 1.82, 0.0, 1.6)
    print(f"{nome}: fotogramma; x, z veri; frazione_visibile della verità; la mia (marcia sul raggio); scarto; pixel sagoma verità/miei; "
          "nell'immagine: pixel validi a ±0,15 m dalla capsula dentro la mia parte visibile / dentro la parte che dico nascosta")
    for k in (5, 14, 16, 17, 23, 29, 31):
        s = ver["fotogrammi"][k]["soggetti"][0]
        tc = t_capsula(h, dx, dz, dq, s["x"], s["z"])
        sag = np.isfinite(tc)
        vis = sag & (tc < tp)
        mia = vis.sum() / max(1, sag.sum())
        prof = np.load(os.path.join(cart, "profondita", f"{k:06d}.npy"), allow_pickle=False).astype(np.float64) / 1000.0
        vicino = (prof > 0) & (np.abs(prof - tc) <= 0.15)
        print(f"  {k}; {s['x']:+.3f}, {s['z']:.3f}; {s['frazione_visibile']:.4f}; {mia:.4f}; {mia - s['frazione_visibile']:+.4f}; "
              f"{s['pixel_sagoma']}/{int(sag.sum())}; {int((vicino & vis).sum())} su {int(vis.sum())} / {int((vicino & sag & ~vis).sum())} su {int((sag & ~vis).sum())}")
    # maschera d'ombra: anello a 2,45 m, classe al centro cella, contro il mio conto (segmento camera → punto del suolo)
    pol = ver["ombra_suolo"]["polare"]
    riga = pol["celle"][24]
    az = pol["azimut_gradi_centro_prima"] + np.arange(pol["n_azimut"]) * pol["passo_gradi"]
    r = pol["distanza_m_centro_prima"] + 24 * pol["passo_m"]
    gx, gz = r * np.sin(np.radians(az)), r * np.cos(np.radians(az))
    tt = t_scatola(h, gx, gz, np.full(gx.shape, -h), -0.5, 0.5, 1.80, 1.82, 0.0, 1.6)   # parametro lungo il segmento (1 = suolo)
    mio = tt < 1.0
    ver_ombra = np.array([c in "13" for c in riga])
    print(f"ombra del pannello sull'anello a {r:.2f} m (codici {ver['ombra_suolo']['codici']}): celle in ombra per la verità "
          f"{int(ver_ombra.sum())} (azimut {az[ver_ombra].min():+.1f}…{az[ver_ombra].max():+.1f}), per il mio conto {int(mio.sum())} "
          f"(azimut {az[mio].min():+.1f}…{az[mio].max():+.1f}); celle discordi {int((mio != ver_ombra).sum())}; riga: {riga[30:70]}")


# ------------------------------------------------------------------------------------------------ A8
def a8(quale):
    import misura_passaggi as MP
    radice = os.path.join(A.USCITE, "a8")
    casi = {"z23": (2.3, 424, (40,)), "z21": (2.1, 424, (40, 3)), "z20": (2.0, 424, (40,)), "w848": (2.3, 848, (40, 160, 3))}
    for q in quale:
        z_att, larg, soglie = casi[q]
        C.Z_ATTORE = z_att
        ris = {s: [] for s in soglie}
        for k in range(1, 20, 2):                                # i passaggi dispari («di prova» per la validazione)
            spec = C._spec("a12", "d435i", "nominale", "pannello", f"pannello_a12__s{k:02d}", persone=[C._pers("a12", k)])
            meta, tempi, quadri, verita = genera(spec, larghezza=larg)
            for s in soglie:
                base = os.path.join(radice, f"{q}_p{s}")
                vdir = os.path.join(base, "_verita", spec["nome"])
                os.makedirs(vdir, exist_ok=True)
                with open(os.path.join(vdir, "verita.json"), "w", encoding="utf-8") as f:
                    json.dump(verita, f)
                r, err, _ = K.corri(K.SorgenteMemoria(meta, tempi, quadri), os.path.join(base, spec["nome"]),
                                    dataclasses.replace(K.Parametri(), min_punti_ostacolo=s))
                K.SEQ_SIM = os.path.join(base, "_verita")
                m = MP.misura(spec["nome"], base) if err is None else {"errore": err}
                K.SEQ_SIM = os.path.join(K.SIM, "sequenze")
                ris[s].append(m)
        C.Z_ATTORE = 2.3
        for s in soglie:
            ms = ris[s]
            es = [m.get("esito_identita", m.get("errore", "?")) for m in ms]
            conta = {e: es.count(e) for e in sorted(set(es))}
            pul = sum(1 for m in ms if m.get("continuita_pulita"))
            a, b = K.wilson(pul, len(ms))
            print(f"A8 {q}: linea a {z_att} m, {larg} px, soglia {s}: continuità pulita {pul} su {len(ms)} (IC 95 % {100 * a:.0f}–{100 * b:.0f} %); "
                  f"esiti d'identità {conta}; fusione a soggetto intero in {sum(1 for m in ms if m.get('fusione_fotogrammi_interi', 0) > 0)}; "
                  f"pannello «si muove» in {sum(1 for m in ms if m.get('pannello_si_muove'))}; tracce fantasma (mediana) "
                  f"{np.median([m.get('tracce_fantasma', float('nan')) for m in ms]):.0f}")


if __name__ == "__main__":
    cosa = sys.argv[1]
    if cosa == "a6":
        a6(float(sys.argv[2]) if len(sys.argv) > 2 else 0.5)
    elif cosa == "a7":
        a7()
    else:
        a8(sys.argv[2:] or ["z23", "z21"])
