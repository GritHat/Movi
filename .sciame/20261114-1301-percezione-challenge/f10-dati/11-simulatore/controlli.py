#!/usr/bin/env python3
"""controlli.py — i controlli del simulatore (f10, 11-simulatore). Le soglie sono in PREVISIONI.md, scritte prima.

  …/ambiente/venv/bin/python -I -B controlli.py modello   # in memoria: pareti, banda, suolo, ombra, filtri
  …/ambiente/venv/bin/python -I -B controlli.py disco     # sulle sequenze scritte: pareti rilette, P11, P12

Ogni riga stampata è «ESITO <previsione> <regge|SMENTITA|…> : cifre». Il JSON con tutte le cifre va in
controlli_<parte>.json. Indipendenza: stesso autore del simulatore; indipendenti sono solo la formula del suolo
dell'infrastruttura (P7), le formule analitiche del modello (σz = k z², fx·B/z, fx·B·(1/z1 − 1/z2)) e, per i filtri,
una trascrizione pixel per pixel del sorgente (C13).
"""
import json
import math
import os
import sys
import warnings

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
sys.path.insert(0, os.path.normpath(os.path.join(QUI, "..", "03-infrastruttura")))

import numpy as np                      # noqa: E402

import catalogo as C                    # noqa: E402
import genera as G                      # noqa: E402
import simsens as S                     # noqa: E402
import controlla_sequenza as INFRA      # noqa: E402

ESITI = []


def esito(prev, regge, testo, cifre=None):
    stato = "regge" if regge is True else ("SMENTITA" if regge is False else str(regge))
    print(f"ESITO {prev} {stato} : {testo}", flush=True)
    ESITI.append({"previsione": prev, "esito": stato, "testo": testo, "cifre": cifre})


def _spec(profilo, livello, scena, etichetta, arg=None, n=30, persone=None, filtri=False):
    return C._spec("controlli", profilo, livello, scena, etichetta, arg, n=n, persone=persone, filtri=filtri)


def pila(spec, interruttori=None):
    quadri, extra = [], None
    for _, _, f, _, extra in G.simula(spec, interruttori=interruttori):
        quadri.append(f)
    return np.stack(quadri), extra


# ------------------------------------------------------------------------------------------------ pareti
def misura_parete(quadri, ideale_Z, d, prof, quota):
    """quadri: (n, H, W) uint16. Regione: `quota` centrale del campo, solo pixel della parete."""
    n, H, W = quadri.shape
    m = (1.0 - quota) / 2.0
    reg = np.zeros((H, W), dtype=bool)
    reg[int(round(H * m)):int(round(H * (1 - m))), int(round(W * m)):int(round(W * (1 - m)))] = True
    reg &= np.abs(ideale_Z - d) < 1e-6
    z = quadri[:, reg].astype(np.float64) / 1000.0          # (n, pixel)
    val = z > 0
    res = np.where(val, z - d, np.nan)
    sig_tot = float(np.nanstd(res))
    conta = val.sum(axis=0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        var_t = np.nanvar(np.where(conta >= min(25, n - 1), res, np.nan), axis=0, ddof=1)
    sig_tmp = float(np.sqrt(np.nanmean(var_t)))
    buchi = ~val
    p_buco = float(buchi.mean())
    prima, dopo = buchi[:-1], buchi[1:]
    persist = float((prima & dopo).sum() / max(prima.sum(), 1))
    return {"pixel": int(reg.sum()), "sigma_tot_m": sig_tot, "sigma_temp_m": sig_tmp, "rapporto": sig_tmp / sig_tot,
            "p_buco": p_buco, "persistenza": persist, "media_residuo_m": float(np.nanmean(res))}


def banda_sinistra(quadri):
    """Mediana, su righe e fotogrammi, del numero di colonne iniziali senza dato."""
    prima_valida = np.argmax(quadri > 0, axis=2)            # (n, H)
    return float(np.median(prima_valida))


def controllo_pareti(sorgente="memoria"):
    tab = []
    for sigla in ("d455", "d435i", "g335"):
        for liv in ("nominale", "limite"):
            for d in (1, 2, 3, 4):
                spec = _spec(sigla, liv, "parete", f"parete_{d}m", {"distanza": d}, n=30)
                if sorgente == "disco":
                    cart = os.path.join(G.SEQUENZE, spec["nome"])
                    if not os.path.isdir(cart):
                        continue
                    idx, _ = INFRA.leggi_tempi(cart)
                    quadri = np.stack([INFRA.leggi_profondita(cart, i) for i in idx])
                    prof, cam, sc, statica, _, _ = G.prepara(spec)
                else:
                    quadri, extra = pila(spec)
                    prof, statica = extra["prof"], extra["ideale"]
                r80 = misura_parete(quadri, statica.Z, d, prof, 0.8)
                r20 = misura_parete(quadri, statica.Z, d, prof, 0.2)
                att = prof["k"] * d * d
                fB = prof["fx"] * prof["base_m"]
                tab.append({"profilo": sigla, "livello": liv, "d_m": d, "n": int(quadri.shape[0]), "atteso_m": att,
                            "r80": r80, "r20": r20, "banda_px": banda_sinistra(quadri),
                            "banda_attesa_px": fB / d + prof["margine_banda_px"]})
    def rapp(r, reg):
        return r[reg]["sigma_tot_m"] / r["atteso_m"]
    nom = [r for r in tab if r["livello"] == "nominale"]
    lim = [r for r in tab if r["livello"] == "limite"]
    et = "" if sorgente == "memoria" else " [riletto dal disco]"
    if nom:
        v = [rapp(r, "r80") for r in nom]
        esito("visione-P1" + et, all(0.9 <= x <= 1.1 for x in v),
              f"σ misurato / k_nominale·z², 80 % centrale, {len(nom)} celle: da {min(v):.3f} a {max(v):.3f}; "
              + "; ".join(f"{r['profilo']} {r['d_m']} m: {1000 * r['r80']['sigma_tot_m']:.1f} mm (atteso {1000 * r['atteso_m']:.1f})"
                          for r in nom), nom)
    if lim:
        v = [rapp(r, "r80") for r in lim]
        esito("visione-P2" + et, all(0.9 <= x <= 1.1 for x in v),
              f"σ misurato / k_limite·z², 80 % centrale, {len(lim)} celle: da {min(v):.3f} a {max(v):.3f}", lim)
        v20 = [rapp(r, "r20") for r in lim]
        v80 = [x / 1.13 for x in v]
        esito("visione-P2bis" + et, all(0.9 <= x <= 1.1 for x in v20 + v80),
              f"limite: 20 % centrale / k·z² da {min(v20):.3f} a {max(v20):.3f}; 80 % centrale / (1,13·k·z²) da "
              f"{min(v80):.3f} a {max(v80):.3f}; "
              + "; ".join(f"{r['profilo']} {r['d_m']} m: {1000 * r['r20']['sigma_tot_m']:.1f} mm (atteso {1000 * r['atteso_m']:.1f})"
                          for r in lim))
    v = [r["r80"]["rapporto"] for r in tab]
    esito("visione-P3" + et, all(0.55 <= x <= 0.65 for x in v),
          f"rumore temporale / totale, {len(tab)} celle: da {min(v):.3f} a {max(v):.3f}")
    pn = [r["r80"]["p_buco"] for r in nom]
    pl = [r["r80"]["p_buco"] for r in lim]
    pe = [r["r80"]["persistenza"] for r in tab]
    ok = all(0.002 <= x <= 0.009 for x in pn) and all(0.01 <= x <= 0.03 for x in pl) and all(0.65 <= x <= 0.75 for x in pe)
    esito("visione-P4" + et, ok,
          (f"buchi nominale da {100 * min(pn):.2f} a {100 * max(pn):.2f} %; " if pn else "")
          + (f"limite da {100 * min(pl):.2f} a {100 * max(pl):.2f} %; " if pl else "")
          + f"persistenza da {min(pe):.3f} a {max(pe):.3f}")
    dv = [r["banda_px"] - r["banda_attesa_px"] for r in tab]
    esito("visione-P5" + et, all(abs(x) <= 1.0 for x in dv),
          f"banda al bordo sinistro, misurata − formula: da {min(dv):+.2f} a {max(dv):+.2f} px; "
          + "; ".join(f"{r['profilo']} {r['livello'][:3]} {r['d_m']} m: {r['banda_px']:.0f} px (formula {r['banda_attesa_px']:.1f})"
                      for r in tab if r["d_m"] in (1, 3)))
    return tab


def controllo_pareti_semi(n_semi=20, n_quadri=6):
    """P2ter: il 20 % centrale al limite, con molti semi del rumore fisso (errore di campionamento)."""
    tab = []
    for sigla in ("d455", "d435i", "g335"):
        for d in (1, 2, 3, 4):
            var20, var80 = [], []
            for j in range(n_semi):
                spec = _spec(sigla, "limite", "parete", f"parete_{d}m_seme{j:02d}", {"distanza": d}, n=n_quadri)
                quadri, extra = pila(spec)
                prof = extra["prof"]
                var20.append(misura_parete(quadri, extra["ideale"].Z, d, prof, 0.2)["sigma_tot_m"] ** 2)
                var80.append(misura_parete(quadri, extra["ideale"].Z, d, prof, 0.8)["sigma_tot_m"] ** 2)
            att = prof["k"] * d * d
            tab.append({"profilo": sigla, "d_m": d, "rapporto_20": math.sqrt(np.mean(var20)) / att,
                        "rapporto_80": math.sqrt(np.mean(var80)) / att,
                        "dispersione_fra_semi_20": float(np.std(np.sqrt(var20)) / att)})
    v = [r["rapporto_20"] for r in tab]
    esito("visione-P2ter", all(0.94 <= x <= 1.08 for x in v),
          f"limite, 20 % centrale, {n_semi} semi × {n_quadri} fotogrammi: σ/k·z² da {min(v):.3f} a {max(v):.3f} "
          f"(media {np.mean(v):.3f}); dispersione fra i semi di una cella: "
          f"{100 * np.mean([r['dispersione_fra_semi_20'] for r in tab]):.1f} %; 80 % centrale: da "
          f"{min(r['rapporto_80'] for r in tab):.3f} a {max(r['rapporto_80'] for r in tab):.3f}", tab)
    return tab


# ------------------------------------------------------------------------------------------------ banda del pannello
def controllo_banda_pannello():
    out = []
    for sigla in ("d455", "d435i", "g335"):
        spec = _spec(sigla, "nominale", "pannello", "pannello_vuoto", n=10)
        # (a) solo geometria
        quadri, extra = pila(spec, {"bordi": False, "rumore": False, "buchi": False})
        idl, prof = extra["ideale"], extra["prof"]
        fB = prof["fx"] * prof["base_m"]
        pan = idl.obj == S.O_OSTACOLO0
        righe = np.where(pan.sum(axis=1) >= 20)[0]
        f = quadri[0]
        diff, destra, attese, misurate = [], [], [], []
        for v in righe:
            cols = np.where(pan[v])[0]
            ue, ur = cols[0], cols[-1]
            dn = fB / idl.Z[v, ue]
            w = dn - fB / idl.Z[v, ue - 1]
            w = dn - fB / idl.Z[v, max(0, ue - 1 - int(round(w)))]
            k = 0
            while ue - 1 - k >= 0 and f[v, ue - 1 - k] == 0:
                k += 1
            kd = 0
            while ur + 1 + kd < f.shape[1] and f[v, ur + 1 + kd] == 0:
                kd += 1
            diff.append(k - w)
            destra.append(kd)
            attese.append(w)
            misurate.append(k)
        diff, destra = np.array(diff), np.array(destra)
        ra = {"righe": int(len(righe)), "entro_1px": float((np.abs(diff) <= 1.0).mean()),
              "attesa_px_min": float(min(attese)), "attesa_px_max": float(max(attese)),
              "attesa_px_mediana": float(np.median(attese)), "misurata_px_mediana": float(np.median(misurate)),
              "destra_con_banda": float((destra > 0).mean()), "scarto_max_px": float(np.abs(diff).max())}
        # (b) modello completo: zeri in una finestra attorno al bordo, per riga e fotogramma
        quadri, extra = pila(spec)
        sx, dx_, att = [], [], []
        for v in righe:
            cols = np.where(pan[v])[0]
            ue, ur = cols[0], cols[-1]
            dn = fB / idl.Z[v, ue]
            w = dn - fB / idl.Z[v, ue - 1]
            w = dn - fB / idl.Z[v, max(0, ue - 1 - int(round(w)))]
            att.append(w)
            sx.append((quadri[:, v, ue - 15:ue + 6] == 0).sum(axis=1))
            dx_.append((quadri[:, v, ur - 5:ur + 16] == 0).sum(axis=1))
        rb = {"attesa_px_mediana": float(np.median(att)), "sinistra_px_mediana": float(np.median(sx)),
              "sinistra_px_media": float(np.mean(sx)), "destra_px_mediana": float(np.median(dx_)),
              "destra_px_media": float(np.mean(dx_))}
        out.append({"profilo": sigla, "geometria": ra, "completo": rb})
    ok_a = all(r["geometria"]["entro_1px"] >= 0.95 and r["geometria"]["destra_con_banda"] <= 0.05 for r in out)
    ok_b = all(abs(r["completo"]["sinistra_px_mediana"] - r["completo"]["attesa_px_mediana"]) <= 1.5
               and r["completo"]["destra_px_mediana"] <= 1.0 for r in out)
    esito("visione-P6a", ok_a, "banda d'occlusione a sinistra del pannello, sola geometria: " + "; ".join(
        f"{r['profilo']}: {100 * r['geometria']['entro_1px']:.1f} % di {r['geometria']['righe']} righe entro ±1 px "
        f"(attesa {r['geometria']['attesa_px_min']:.2f}–{r['geometria']['attesa_px_max']:.2f} px, mediana "
        f"{r['geometria']['attesa_px_mediana']:.2f}; misurata mediana {r['geometria']['misurata_px_mediana']:.0f}; "
        f"scarto massimo {r['geometria']['scarto_max_px']:.2f}); a destra righe con banda "
        f"{100 * r['geometria']['destra_con_banda']:.1f} %" for r in out), out)
    esito("visione-P6b", ok_b, "modello completo (zeri in 21 colonne attorno al bordo): " + "; ".join(
        f"{r['profilo']}: sinistra mediana {r['completo']['sinistra_px_mediana']:.1f} px, media "
        f"{r['completo']['sinistra_px_media']:.2f} (formula {r['completo']['attesa_px_mediana']:.2f}); destra mediana "
        f"{r['completo']['destra_px_mediana']:.1f}, media {r['completo']['destra_px_media']:.2f}" for r in out))
    return out


# ------------------------------------------------------------------------------------------------ suolo e ombra
def controllo_suolo():
    out = []
    for sigla in ("d455", "d435i", "g335"):
        spec = _spec(sigla, "nominale", "pavimento", "pavimento_vuoto", n=1)
        prof, cam, sc, statica, _, _ = G.prepara(spec)
        meta = cam.meta()
        zf = INFRA.profondita_del_suolo(meta)
        suolo = statica.obj == S.O_SUOLO
        out.append({"profilo": sigla, "pixel_suolo": int(suolo.sum()),
                    "scarto_max_mm": float(1000 * np.abs(statica.Z[suolo] - zf[suolo]).max())})
    esito("visione-P7", all(r["scarto_max_mm"] <= 0.5 for r in out),
          "profondità ideale del suolo contro la formula dell'infrastruttura: " + "; ".join(
              f"{r['profilo']}: scarto massimo {r['scarto_max_mm']:.2e} mm su {r['pixel_suolo']} pixel" for r in out), out)
    return out


def _uniforme3(m):
    """Vero dove il pixel e i suoi 8 vicini hanno lo stesso valore booleano."""
    from scipy import ndimage
    return ndimage.minimum_filter(m.astype(np.uint8), size=3) == ndimage.maximum_filter(m.astype(np.uint8), size=3)


def controllo_ombra():
    out = []
    for nome_scena, et in (("pannello", "pannello_vuoto"), ("cassa", "cassa_vuota")):
        for sigla in ("d455", "d435i"):
            spec = _spec(sigla, "nominale", nome_scena, et, n=1)
            quadri, extra = pila(spec, {"bordi": False, "rumore": False, "buchi": False})
            prof, cam, sc, idl = extra["prof"], extra["cam"], extra["scena"], extra["ideale"]
            # 1) immagine -> suolo: ogni pixel ideale del suolo deve cadere su «visibile» (0) o «banda» (4)
            vv, uu = np.where(idl.obj == S.O_SUOLO)
            x, q, z = cam.al_suolo(uu.astype(float), vv.astype(float), idl.Z[vv, uu])
            c = S.classe_suolo(sc, cam, prof, x, z)
            in_ombra = int((c == S.C_OMBRA).sum())
            altri = int(((c == S.C_FUORI) | (c == S.C_IMPRONTA)).sum())
            # 2) classe 4 contro i buchi geometrici del sensore (due strade diverse: raggio 3D dal destro / righe)
            senza_dato = quadri[0][vv, uu] == 0
            banda = c == S.C_BANDA
            m_banda = np.zeros(idl.Z.shape, dtype=bool)
            m_banda[vv, uu] = banda
            m_zero = quadri[0] == 0
            lontano_dal_confine = _uniforme3(m_banda)[vv, uu]
            discordi = int(((banda != senza_dato) & lontano_dal_confine).sum())
            discordi_tutti = int((banda != senza_dato).sum())
            # 3) suolo -> immagine: i punti «in ombra» della maschera fitta non devono cadere su pixel del suolo
            xs = np.arange(-3.0 + 0.0125, 3.0, 0.025)
            zs = np.arange(0.0 + 0.0125, 4.0, 0.025)
            X, Zg = np.meshgrid(xs, zs)
            cg = S.classe_suolo(sc, cam, prof, X, Zg)
            u, v, Zc = cam.proietta(X, np.zeros_like(X), Zg)
            ui, vi = np.rint(u).astype(int), np.rint(v).astype(int)
            dentro = (ui >= 0) & (ui < cam.W) & (vi >= 0) & (vi < cam.H) & (cg != S.C_FUORI)
            e_suolo = np.zeros(X.shape, dtype=bool)
            e_suolo[dentro] = (idl.obj == S.O_SUOLO)[vi[dentro], ui[dentro]]
            suolo_unif = np.zeros(X.shape, dtype=bool)
            suolo_unif[dentro] = _uniforme3(idl.obj == S.O_SUOLO)[vi[dentro], ui[dentro]]
            ombra_su_suolo = int(((cg == S.C_OMBRA) & e_suolo & suolo_unif).sum())
            visibile_non_suolo = int((((cg == S.C_VISIBILE) | (cg == S.C_BANDA)) & ~e_suolo & suolo_unif & dentro).sum())
            out.append({"scena": nome_scena, "profilo": sigla, "pixel_suolo": int(vv.size), "pixel_in_ombra": in_ombra,
                        "pixel_fuori_o_impronta": altri, "banda_discordi_lontano_dal_confine": discordi,
                        "banda_discordi_tutti": discordi_tutti, "pixel_banda": int(banda.sum()),
                        "celle_ombra": int((cg == S.C_OMBRA).sum()), "celle_ombra_su_pixel_di_suolo": ombra_su_suolo,
                        "celle_visibili_su_pixel_non_di_suolo": visibile_non_suolo})
    ok = all(r["pixel_in_ombra"] == 0 and r["celle_ombra_su_pixel_di_suolo"] == 0 for r in out)
    esito("visione-P8", ok, "maschera d'ombra contro immagine ideale: " + "; ".join(
        f"{r['scena']} {r['profilo']}: {r['pixel_in_ombra']} pixel di suolo in ombra su {r['pixel_suolo']}, "
        f"{r['celle_ombra_su_pixel_di_suolo']} celle d'ombra su pixel di suolo (di {r['celle_ombra']}), "
        f"{r['celle_visibili_su_pixel_non_di_suolo']} celle visibili su pixel non di suolo; banda stereo: "
        f"{r['banda_discordi_lontano_dal_confine']} pixel discordi lontano dal confine, {r['banda_discordi_tutti']} in tutto "
        f"su {r['pixel_banda']} di banda" for r in out), out)
    return out


# ------------------------------------------------------------------------------------------------ filtri
def _riempi_lontano_letterale(f):
    """Trascrizione pixel per pixel di holes_fill_farest (hole-filling-filter.h)."""
    g = f.astype(np.int64).copy()
    H, W = g.shape
    for j in range(1, H - 1):
        for i in range(1, W):
            if g[j, i] == 0:
                g[j, i] = max(g[j - 1, i], g[j - 1, i - 1], g[j, i - 1], g[j + 1, i - 1], g[j + 1, i])
    return g.astype(np.uint16)


class _TemporaleLetterale:
    """Trascrizione pixel per pixel di temp_jw_smooth (temporal-filter.h) con la regola di persistenza 3."""

    def __init__(self, alfa=0.4, delta=20):
        self.alfa, self.delta, self.ultimo, self.storia, self.fase = alfa, delta, None, None, 0

    def applica(self, f):
        if self.ultimo is None:
            self.ultimo = np.zeros(f.shape, dtype=np.int64)
            self.storia = np.zeros(f.shape, dtype=np.int64)
        out = f.astype(np.int64).copy()
        maschera = 1 << self.fase
        for idx in np.ndindex(f.shape):
            cur, prec = int(out[idx]), int(self.ultimo[idx])
            if cur:
                if not prec:
                    self.ultimo[idx], self.storia[idx] = cur, maschera
                elif abs(cur - prec) < self.delta:
                    self.storia[idx] |= maschera
                    ris = int(self.alfa * cur + (1.0 - self.alfa) * prec)
                    out[idx] = ris
                    self.ultimo[idx] = ris
                else:
                    self.ultimo[idx], self.storia[idx] = cur, maschera
            else:
                if prec:
                    st = int(self.storia[idx])
                    somma = sum((st >> ((self.fase - j) % 8)) & 1 for j in range(1, 5))
                    if somma >= 2:
                        out[idx] = prec
                self.storia[idx] &= ~maschera & 0xFF
        self.fase = (self.fase + 1) % 8
        return out.astype(np.uint16)


def controllo_filtri_trascrizione():
    rng = np.random.default_rng(12345)
    diversi_r, diversi_t, n = 0, 0, 0
    vett, lett = S.FiltriRealsense(riempimento=False), _TemporaleLetterale()
    base = rng.integers(1500, 2500, size=(14, 19))
    for k in range(40):
        f = (base + rng.integers(-30, 31, size=base.shape)).astype(np.uint16)
        f[rng.random(base.shape) < 0.35] = 0
        if k % 9 == 8:
            f[:] = 0
        a, b = S.FiltriRealsense._riempi_lontano(f), _riempi_lontano_letterale(f)
        diversi_r += int((a != b).sum())
        a, b = vett.applica(f), lett.applica(f)
        diversi_t += int((a != b).sum())
        n += f.size
    esito("visione-C13", diversi_r == 0 and diversi_t == 0,
          f"filtri in numpy contro la trascrizione pixel per pixel del sorgente, 40 fotogrammi 14×19 con il 35 % di "
          f"buchi: {diversi_r} pixel diversi nel riempimento, {diversi_t} nel temporale, su {n}",
          {"riempimento": diversi_r, "temporale": diversi_t, "pixel": n})


def controllo_filtri_effetto(sorgente="memoria"):
    out = []
    for et, persone in (("pannello_vuoto", None), ("pannello_a12__s00", [C._pers("a12", 0)])):
        spec = _spec("d435i", "nominale", "pannello", et, n=10 if persone is None else None, persone=persone, filtri=True)
        validi_g, validi_f, in_banda, riempiti, come_sfondo, come_pannello, liberi_falsi = [], [], 0, 0, 0, 0, 0
        for i, t, f, ver, extra in G.simula(spec):
            g, idl, sens = extra["grezzo"], extra["ideale"], extra["sensore"]
            validi_g.append((g > 0).mean())
            validi_f.append((f > 0).mean())
            if i < 4:
                continue        # la persistenza vuole storia
            occ = sens.ultimo["occlusione"] & (g == 0)
            pan = idl.obj == S.O_OSTACOLO0
            righe = pan.sum(axis=1) >= 20
            # la banda a sinistra del bordo sinistro del pannello: entro 12 colonne dal primo pixel del pannello
            primo = np.argmax(pan, axis=1)
            cols = np.arange(pan.shape[1])[None, :]
            vicino = righe[:, None] & (cols < primo[:, None]) & (cols >= primo[:, None] - 12)
            occ &= vicino & (idl.obj != S.O_OSTACOLO0) & (idl.obj < S.O_PERSONA0)
            zf = f[occ].astype(np.float64) / 1000.0
            zs = idl.Z[occ]
            zp = np.broadcast_to(np.where(righe, np.where(pan, idl.Z, np.inf).min(axis=1), np.nan)[:, None], pan.shape)[occ]
            in_banda += int(occ.sum())
            riempiti += int((zf > 0).sum())
            come_sfondo += int(((zf > 0) & (np.abs(zf - zs) <= 0.1 * zs)).sum())
            come_pannello += int(((zf > 0) & (np.abs(zf - zp) <= 0.1 * zp) & ~(np.abs(zf - zs) <= 0.1 * zs)).sum())
        out.append({"sequenza": spec["nome"], "validi_senza_filtri": float(np.mean(validi_g)),
                    "validi_con_filtri": float(np.mean(validi_f[4:])), "pixel_banda": in_banda, "riempiti": riempiti,
                    "riempiti_con_lo_sfondo": come_sfondo, "riempiti_con_il_pannello": come_pannello})
    ok = all(r["validi_con_filtri"] >= 0.995 and r["riempiti_con_lo_sfondo"] >= 0.8 * r["pixel_banda"] for r in out)
    esito("visione-P12", ok, "filtri del costruttore: " + "; ".join(
        f"{r['sequenza']}: validi {100 * r['validi_senza_filtri']:.2f} % -> {100 * r['validi_con_filtri']:.2f} %; banda "
        f"d'occlusione a sinistra del pannello: {r['pixel_banda']} pixel, riempiti {r['riempiti']}, con lo sfondo "
        f"{r['riempiti_con_lo_sfondo']} ({100 * r['riempiti_con_lo_sfondo'] / max(r['pixel_banda'], 1):.1f} %), con il "
        f"pannello {r['riempiti_con_il_pannello']}" for r in out), out)
    return out


# ------------------------------------------------------------------------------------------------ dal disco
def controllo_passaggi_disco():
    out = {}
    for caso in ("a12", "a05", "b", "c", "d"):
        righe = []
        for k in range(30):
            cart = os.path.join(G.SEQUENZE, f"d435i_nom__pannello_{caso}__s{k:02d}")
            if not os.path.isdir(cart):
                continue
            ver = INFRA.leggi_verita(cart)
            fr = np.array([f["soggetti"][0]["frazione_visibile"] for f in ver["fotogrammi"]])
            nasc = fr == 0
            idx = np.where(nasc)[0]
            contiguo = bool(idx.size and (idx[-1] - idx[0] + 1 == idx.size))
            parz = int(((fr > 0) & (fr < 1)).sum())
            righe.append({"k": k, "n": int(fr.size), "nascosti": int(nasc.sum()), "contiguo": contiguo, "parziali": parz,
                          "prima_visibili": int(idx[0]) if idx.size else None})
        out[caso] = righe
    a = out["a12"]
    na = [r["nascosti"] for r in a]
    ok = len(a) == 30 and all(8 <= x <= 14 for x in na) and all(r["contiguo"] for r in a)
    esito("visione-P11", ok, f"a12: {len(a)} passaggi, fotogrammi del tutto nascosti da {min(na)} a {max(na)} "
          f"(mediana {np.median(na):.0f}), tratto nascosto contiguo in {sum(r['contiguo'] for r in a)} su {len(a)}", a)
    for caso in ("a05", "b", "c", "d"):
        r = out[caso]
        if r:
            nn = [x["nascosti"] for x in r]
            esito(f"descrittivo-{caso}", "nota", f"{len(r)} passaggi, fotogrammi del tutto nascosti da {min(nn)} a {max(nn)} "
                  f"(mediana {np.median(nn):.0f}), contigui in {sum(x['contiguo'] for x in r)}; fotogrammi prima "
                  f"dell'ombra piena da {min(x['prima_visibili'] for x in r)} a {max(x['prima_visibili'] for x in r)}")
    return out


def controllo_visibilita_analitica():
    """P13: conto angolare in pianta (indipendente dal lancio dei raggi) contro verita.json."""
    P = C.PANNELLO
    a0, a1 = math.atan2(P["x0"], P["z0"]), math.atan2(P["x1"], P["z0"])
    tot, discordi, peggio = 0, 0, 0.0
    for caso in ("a12", "a05", "b"):
        for k in range(30):
            cart = os.path.join(G.SEQUENZE, f"d435i_nom__pannello_{caso}__s{k:02d}")
            meta, ver = INFRA.leggi_meta(cart), INFRA.leggi_verita(cart)
            esp = meta["simulazione"]["parametri_sensore"]["esposizione_s"]
            for f in ver["fotogrammi"]:
                s = f["soggetti"][0]
                rho, th = math.hypot(s["x"], s["z"]), math.atan2(s["x"], s["z"])
                v_perp = abs(s["vx"] * s["z"] - s["vz"] * s["x"]) / rho
                al = math.asin((s["raggio_m"] + 0.5 * v_perp * esp) / rho)
                if th - al >= a0 and th + al <= a1:
                    atteso = "coperta"
                elif th + al <= a0 or th - al >= a1:
                    atteso = "intera"
                else:
                    atteso = "parziale"
                if s["pixel_visibili"] < 10:
                    visto = "coperta"
                elif s["pixel_visibili"] == s["pixel_sagoma"]:
                    visto = "intera"
                else:
                    visto = "parziale"
                tot += 1
                if atteso != visto:
                    discordi += 1
                    # distanza dal confine angolare più vicino, in metri alla distanza della persona
                    dist = min(abs(th - al - a0), abs(th + al - a0), abs(th - al - a1), abs(th + al - a1)) * rho
                    peggio = max(peggio, dist)
    esito("visione-P13", discordi <= 0.01 * tot and peggio <= 0.02,
          f"visibilità di verita.json contro il conto angolare in pianta: {discordi} fotogrammi discordi su {tot} "
          f"({100 * discordi / tot:.2f} %), il più lontano dal confine a {100 * peggio:.2f} cm",
          {"fotogrammi": tot, "discordi": discordi, "distanza_massima_m": peggio})


def controllo_riproducibile():
    diversi, n = 0, 0
    nomi = ("d435i_nom__pavimento_vuoto", "d435i_nom__pannello_b__s07", "d435i_nom__pannello_a12__s01__filtri")
    for nome in nomi:
        spec = [s for s in C.catalogo() if s["nome"] == nome][0]
        cart = os.path.join(G.SEQUENZE, nome)
        for i, t, f, ver, extra in G.simula(spec):
            diversi += int((f != INFRA.leggi_profondita(cart, i)).sum())
            n += f.size
    esito("visione-P14", diversi == 0, f"rigenerate {', '.join(nomi)}: {diversi} pixel diversi su {n}",
          {"pixel": n, "diversi": diversi})


def main(argv):
    parte = argv[0] if argv else "modello"
    ris = {}
    if parte == "modello":
        ris["pareti"] = controllo_pareti("memoria")
        ris["banda_pannello"] = controllo_banda_pannello()
        ris["suolo"] = controllo_suolo()
        ris["ombra"] = controllo_ombra()
        controllo_filtri_trascrizione()
        ris["filtri"] = controllo_filtri_effetto()
    elif parte == "semi":
        ris["pareti_semi"] = controllo_pareti_semi()
    elif parte == "disco":
        ris["pareti_disco"] = controllo_pareti("disco")
        ris["passaggi"] = controllo_passaggi_disco()
        controllo_visibilita_analitica()
        controllo_riproducibile()
    else:
        print(__doc__)
        return 2
    ris["esiti"] = ESITI
    with open(os.path.join(QUI, f"controlli_{parte}.json"), "w", encoding="utf-8") as f:
        json.dump(ris, f, ensure_ascii=False, indent=1, default=float)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
