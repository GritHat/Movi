#!/usr/bin/env python3
"""catalogo.py — le scene, i percorsi delle persone e l'elenco delle sequenze del simulatore (f10, 11-simulatore).

Una sequenza è descritta da un dizionario («specifica»): tutto ciò che serve a rigenerarla, semi compresi.
I parametri dell'andatura e dei percorsi sono IPOTESI di sciame-visione (non misure): sono qui in chiaro.
"""
import math

import numpy as np

import simsens as S

FPS = 15.0
PROFILO_PRINCIPALE = "d435i"
SIGLA_LIVELLO = {"nominale": "nom", "limite": "lim"}

# ---- geometria della demo del nucleo (SOLUZIONE_V2.md, B9): pannello 1 m × 1,6 m a 1,8 m, attore a 2,3 m
PANNELLO = dict(x0=-0.5, x1=0.5, z0=1.80, z1=1.82, q0=0.0, q1=1.6)
Z_ATTORE = 2.3

# ---- andatura (ipotesi): modulazione della velocità e oscillazione laterale al ritmo del passo
ANDATURA = dict(ampiezza_velocita=0.08, ampiezza_laterale_m=0.02, passo_hz_a0=0.77, passo_hz_per_ms=0.86,
                accelerazione_ms2=2.0)


def scena(nome, **a):
    """Ritorna (Scena, inclinazione in gradi)."""
    if nome == "parete":
        return S.Scena(z=(-1.0, float(a["distanza"]))), 0.0
    if nome == "pavimento":
        return S.Scena(), 15.0
    if nome == "pavimento_lucido":
        return S.Scena(materiale_suolo=S.M_LUCIDO), 15.0
    if nome == "pannello":
        return S.Scena(ostacoli=[S.Scatola("pannello", **PANNELLO, tipo="pannello")]), 15.0
    if nome == "cassa":
        return S.Scena(ostacoli=[S.Scatola("cassa", -0.5, 0.5, 1.6, 2.0, 0.0, 1.0, tipo="cassa")]), 15.0
    if nome == "sospeso":
        d = float(a["distanza"])
        return S.Scena(ostacoli=[S.Scatola("sospeso", -0.5, 0.5, d, d + 0.3, 1.8, 2.0, tipo="sospeso")]), 15.0
    if nome == "scatola15":
        d = float(a["distanza"])
        return S.Scena(ostacoli=[S.Scatola("scatola15", -0.075, 0.075, d, d + 0.15, 0.0, 0.15, tipo="scatola")]), 15.0
    if nome == "vetro":
        return S.Scena(ostacoli=[S.Scatola("vetro", -0.5, 0.5, 1.5, 1.51, 0.0, 2.0, materiale=S.M_VETRO,
                                           trasparente=True, tipo="lastra di vetro")], vetro=a["modo"]), 15.0
    raise ValueError(nome)


# ------------------------------------------------------------------------------------------------ percorsi
def campiona_percorso(punti, v_croc, soste, fine, rng, coda_s=0.0, andatura=True, fps=FPS, sotto=40):
    """Cammina lungo la spezzata `punti` [(x, z), …] a velocità di crociera v_croc, fermandosi a ogni punto interno
    per soste.get(indice, 0) secondi. fine: «via» (la sequenza finisce quando arriva in fondo, senza frenare) o
    «ferma» (frena, e resta coda_s secondi). Ritorna x, z, vx, vz campionati a fps."""
    dt = 1.0 / (fps * sotto)
    acc = ANDATURA["accelerazione_ms2"]
    f_p = ANDATURA["passo_hz_a0"] + ANDATURA["passo_hz_per_ms"] * v_croc
    A_v = ANDATURA["ampiezza_velocita"] if andatura else 0.0
    A_s = ANDATURA["ampiezza_laterale_m"] if andatura else 0.0
    f1, f2 = rng.uniform(0.0, 2 * math.pi, 2)
    pos = []
    i, s, v, t, pausa = 0, 0.0, v_croc, 0.0, 0.0
    finito_a = None
    while True:
        a, b = punti[i], punti[i + 1]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        ux, uz = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        ultimo = i == len(punti) - 2
        if pausa > 0:
            pausa -= dt
        elif finito_a is None:
            vt = v_croc * (1.0 + A_v * math.sin(2 * math.pi * f_p * t + f1))
            if not (ultimo and fine == "via"):
                vt = min(vt, math.sqrt(max(2 * acc * (L - s), 0.0)) + 0.02)
            v += max(-3 * acc * dt, min(acc * dt, vt - v))
            v = max(v, 0.0)
            s += v * dt
            if s >= L - 1e-3:
                s = L
                if ultimo:
                    finito_a = t
                    if fine == "ferma":
                        v = 0.0
                else:
                    pos.append((b[0], b[1]))
                    t += dt
                    i, s, v, pausa = i + 1, 0.0, 0.0, soste.get(i + 1, 0.0)
                    continue
        lat = A_s * math.sin(2 * math.pi * (f_p / 2) * t + f2) * min(1.0, v / v_croc)
        pos.append((a[0] + ux * s - uz * lat, a[1] + uz * s + ux * lat))
        t += dt
        if finito_a is not None and t >= finito_a + (coda_s if fine == "ferma" else 0.0):
            break
        if t > 120.0:
            raise RuntimeError("percorso senza fine")
    pos = np.asarray(pos)
    n = (len(pos) - 1) // sotto + 1
    idx = np.arange(n) * sotto
    q = sotto // 4
    a_, b_ = np.clip(idx - q, 0, len(pos) - 1), np.clip(idx + q, 0, len(pos) - 1)
    vel = (pos[b_] - pos[a_]) / ((b_ - a_)[:, None] * dt)
    return pos[idx, 0], pos[idx, 1], vel[:, 0], vel[:, 1]


def passaggio(caso, k, scena_nome="pannello"):
    """Il percorso del passaggio k del caso dato. Il seme dipende solo da (caso, k): lo stesso passaggio è identico
    per tutti i profili e i livelli. Passaggi pari: da sinistra a destra; dispari: da destra a sinistra."""
    rng = np.random.default_rng(S.seme_da_nome(f"percorso__{caso}__s{k:02d}"))
    verso = 1.0 if k % 2 == 0 else -1.0
    zp = Z_ATTORE + rng.uniform(-0.03, 0.03)
    u = rng.uniform(0.9, 1.1)
    par = {"caso": caso, "passaggio": k, "verso": "sinistra->destra" if verso > 0 else "destra->sinistra"}
    if caso == "a12":
        v, X0 = 1.2 * u, 1.7
        punti, soste, fine, coda = [(-verso * X0, zp), (verso * X0, zp)], {}, "via", 0.0
    elif caso == "a05":
        v, X0 = 0.5 * u, 1.2
        punti, soste, fine, coda = [(-verso * X0, zp), (verso * X0, zp)], {}, "via", 0.0
    elif caso == "b":
        v, X0, xs = 1.2 * u, 1.45, rng.uniform(-0.25, 0.25)
        punti, soste, fine, coda = [(-verso * X0, zp), (xs, zp), (verso * X0, zp)], {1: 3.0}, "via", 0.0
        par["sosta_x_m"], par["sosta_s"] = round(xs, 4), 3.0
    elif caso == "c":
        v, X0, xs = 1.2 * u, 1.6, rng.uniform(-0.2, 0.2)
        punti, soste, fine, coda = [(-verso * X0, zp), (xs, zp), (-verso * X0, zp)], {1: 1.0}, "via", 0.0
        par["inversione_x_m"], par["sosta_s"] = round(xs, 4), 1.0
    elif caso == "d":
        v, X0, xs = 1.2 * u, 1.6, rng.uniform(-0.15, 0.15)
        punti, soste, fine, coda = [(-verso * X0, zp), (xs, zp), (xs, 4.2)], {1: 0.5}, "ferma", 1.0
        par["svolta_x_m"], par["arrivo_z_m"] = round(xs, 4), 4.2
    elif caso == "cassa":
        zp = 2.5 + rng.uniform(-0.03, 0.03)
        v, X0 = 0.8 * u, 1.5
        punti, soste, fine, coda = [(-verso * X0, zp), (0.0, zp), (verso * X0, zp)], {1: 1.5}, "via", 0.0
        par["sosta_s"] = 1.5
    else:
        raise ValueError(caso)
    par["velocita_crociera_ms"], par["z_linea_m"] = round(v, 4), round(zp, 4)
    x, z, vx, vz = campiona_percorso(punti, v, soste, fine, rng, coda_s=coda)
    return x, z, vx, vz, par


# ------------------------------------------------------------------------------------------------ elenco
def _spec(gruppo, profilo, livello, nome_scena, etichetta, arg=None, n=None, persone=None, eventi=None,
          filtri=False):
    base = f"{profilo}_{SIGLA_LIVELLO[livello]}__{etichetta}"
    return {"nome": base + ("__filtri" if filtri else ""), "nome_base": base, "gruppo": gruppo, "profilo": profilo,
            "livello": livello, "scena": nome_scena, "arg": arg or {}, "n": n, "persone": persone or [],
            "eventi": eventi or {}, "filtri": filtri}


def _pers(caso, k, materiale=S.M_CHIARO, altezza=1.7):
    return {"id": "s1", "caso": caso, "k": k, "materiale": materiale, "altezza": altezza}


def _ferma(x, z, materiale=S.M_CHIARO):
    return {"id": "s1", "fermo": [x, z], "materiale": materiale, "altezza": 1.7}


def catalogo():
    """L'elenco completo delle sequenze scritte su disco (vedi SIMULATORE.md per i conti dello spazio)."""
    L = []
    P = PROFILO_PRINCIPALE
    # --- statiche di taratura, tre profili al nominale, più il principale al limite
    for prof, liv, n in (("d455", "nominale", 30), ("d435i", "nominale", 30), ("g335", "nominale", 30),
                         ("d435i", "limite", 20)):
        for d in (1, 2, 3, 4):
            L.append(_spec("statiche", prof, liv, "parete", f"parete_{d}m", {"distanza": d}, n=n))
        L.append(_spec("statiche", prof, liv, "pavimento", "pavimento_vuoto", n=n))
        L.append(_spec("statiche", prof, liv, "pannello", "pannello_vuoto", n=10))
    # --- passaggi dietro il pannello, profilo principale al nominale
    for k in range(30):
        L.append(_spec("a12", P, "nominale", "pannello", f"pannello_a12__s{k:02d}", persone=[_pers("a12", k)]))
    for k in range(30):
        L.append(_spec("a05", P, "nominale", "pannello", f"pannello_a05__s{k:02d}", persone=[_pers("a05", k)]))
    for k in range(30):
        L.append(_spec("b", P, "nominale", "pannello", f"pannello_b__s{k:02d}", persone=[_pers("b", k)]))
    for k in range(4):
        L.append(_spec("cd", P, "nominale", "pannello", f"pannello_c__s{k:02d}", persone=[_pers("c", k)]))
    for k in range(4):
        L.append(_spec("cd", P, "nominale", "pannello", f"pannello_d__s{k:02d}", persone=[_pers("d", k)]))
    # --- livello limite e altri profili: meno passaggi (gli stessi percorsi s00… del principale)
    for k in range(4):
        L.append(_spec("limite", P, "limite", "pannello", f"pannello_a12__s{k:02d}", persone=[_pers("a12", k)]))
    for k in range(2):
        L.append(_spec("limite", P, "limite", "pannello", f"pannello_b__s{k:02d}", persone=[_pers("b", k)]))
    for prof in ("d455", "g335"):
        for k in range(3):
            L.append(_spec("profili", prof, "nominale", "pannello", f"pannello_a12__s{k:02d}",
                           persone=[_pers("a12", k)]))
        L.append(_spec("profili", prof, "nominale", "pannello", "pannello_a05__s00", persone=[_pers("a05", 0)]))
        L.append(_spec("profili", prof, "nominale", "pannello", "pannello_b__s00", persone=[_pers("b", 0)]))
    # --- le altre scene, profilo principale
    g = "altre"
    L.append(_spec(g, P, "nominale", "cassa", "cassa_persona__s00", persone=[_pers("cassa", 0)]))
    for d, e in ((2.0, "2p0m"), (2.8, "2p8m")):
        L.append(_spec(g, P, "nominale", "sospeso", f"sospeso_{e}", {"distanza": d}, n=10))
    for d, e in ((0.8, "0p8m"), (2.0, "2p0m")):
        L.append(_spec(g, P, "nominale", "scatola15", f"scatola15_{e}", {"distanza": d}, n=10))
    for modo in ("sfondo", "buco"):
        L.append(_spec(g, P, "nominale", "vetro", f"vetro_{modo}", {"modo": modo}, n=10))
    for k in range(2):
        L.append(_spec(g, P, "nominale", "pannello", f"pannello_a12_scuro__s{k:02d}",
                       persone=[_pers("a12", k, materiale=S.M_SCURO)]))
        L.append(_spec(g, P, "nominale", "pannello", f"pannello_a12_nero__s{k:02d}",
                       persone=[_pers("a12", k, materiale=S.M_NERO)]))
        L.append(_spec(g, P, "nominale", "pannello", f"pannello_a12_alta185__s{k:02d}",
                       persone=[_pers("a12", k, altezza=1.85)]))
    L.append(_spec(g, P, "limite", "pannello", "pannello_a12_scuro__s00", persone=[_pers("a12", 0, materiale=S.M_SCURO)]))
    L.append(_spec(g, P, "nominale", "pannello", "sensore_coperto", n=45, persone=[_ferma(-1.2, 2.3)],
                   eventi={"copertura": {"da_s": 1.0, "a_s": 2.2, "parte": "tutto"}}))
    L.append(_spec(g, P, "nominale", "pannello", "sensore_mezzo_coperto", n=30, persone=[_ferma(-1.2, 2.3)],
                   eventi={"copertura": {"da_s": 0.6, "a_s": 1.6, "parte": "sinistra"}}))
    L.append(_spec(g, P, "nominale", "pannello", "azzeramento_progressivo", n=75, persone=[_ferma(-1.2, 2.3)],
                   eventi={"azzeramento": {"da_s": 1.0, "a_s": 4.5}}))
    for liv in ("nominale", "limite"):
        L.append(_spec(g, P, liv, "pavimento_lucido", "pavimento_lucido", n=20))
    # --- con i filtri del costruttore accesi (stesso seme della sequenza senza filtri)
    g = "filtri"
    L.append(_spec(g, P, "nominale", "pavimento", "pavimento_vuoto", n=30, filtri=True))
    L.append(_spec(g, P, "nominale", "pannello", "pannello_vuoto", n=10, filtri=True))
    for k in range(2):
        L.append(_spec(g, P, "nominale", "pannello", f"pannello_a12__s{k:02d}", persone=[_pers("a12", k)], filtri=True))
    L.append(_spec(g, P, "nominale", "pannello", "pannello_b__s00", persone=[_pers("b", 0)], filtri=True))
    nomi = [s["nome"] for s in L]
    assert len(nomi) == len(set(nomi)), "nomi ripetuti nel catalogo"
    return L
