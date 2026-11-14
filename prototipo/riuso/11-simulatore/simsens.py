#!/usr/bin/env python3
"""simsens.py — simulatore di una camera di profondità a stereo attivo (f10, 11-simulatore, sciame-visione).

Tre parti:
  1. geometria: camera a foro stenopeico, un raggio per pixel, scene di piani, scatole e capsule (persone);
  2. modello del sensore sopra la profondità ideale, secondo ../02-sensori/parametri_sensori.json
     (rumore in disparità, quantizzazione, buchi, bordi) più l'emulazione dei filtri del costruttore;
  3. verità: visibilità dei soggetti e maschera vera dell'ombra sul piano del suolo.

Riferimenti (formato comune, ../03-infrastruttura/formato_sequenza.md):
  camera:  x a destra, y in basso, z lungo l'asse ottico; la profondità è Zc.
  suolo:   x a destra, z in avanti (proiezione orizzontale dell'asse ottico), quota in alto; origine sul suolo
           sotto il centro ottico.   x = Xc,  z = Zc·cos t − Yc·sin t,  quota = h − Yc·cos t − Zc·sin t.
I vettori del mondo sono terne (x, quota, z). L'imager di riferimento è il sinistro; il destro sta a +base lungo x.

Uso: vedi genera.py e controlli.py. Niente stato globale; i semi sono espliciti.
"""
import json
import math
import os
import zlib

import numpy as np
from scipy import ndimage, special

VERSIONE = "1.0 (14 novembre 2026)"
QUI = os.path.dirname(os.path.abspath(__file__))
PARAMETRI = os.path.normpath(os.path.join(QUI, "..", "02-sensori", "parametri_sensori.json"))

SIGLE = {"d455": "realsense_d455", "d435i": "realsense_d435i", "g335": "orbbec_gemini_335"}
MATERIALI = ["diffuso_chiaro", "diffuso_scuro", "nero_assorbente", "lucido_radente", "vetro_specchio"]
M_CHIARO, M_SCURO, M_NERO, M_LUCIDO, M_VETRO = range(5)

# identità nell'immagine ideale
O_NIENTE, O_SUOLO, O_STANZA = 0, 1, 2
O_OSTACOLO0, O_PERSONA0 = 10, 100

INF = np.inf
COS_MIN = math.cos(math.radians(88.0))      # tetto al fattore 1/cos: 28,7


def seme_da_nome(nome):
    """Seme riproducibile dal nome (crc32)."""
    return zlib.crc32(nome.encode("utf-8")) & 0x7FFFFFFF


# ------------------------------------------------------------------------------------------------ profili
def carica_profilo(sigla, livello="nominale", larghezza=424, percorso=PARAMETRI):
    """Legge il profilo dal JSON dell'esperto di sensori e lo porta alla risoluzione di lavoro.

    La simulazione è «il sensore a 848×480 campionato a `larghezza` colonne»: le grandezze in pixel si scalano
    con r = larghezza/848; il rumore in metri resta quello a 848×480 (sottopixel e passo di disparità scalati).
    livello: «nominale» o «limite» (le due colonne del JSON)."""
    assert livello in ("nominale", "limite")
    with open(percorso, encoding="utf-8") as f:
        P = json.load(f)
    cam = P["camere_profondita"][SIGLE[sigla]]
    com = P["modello_camera_stereo_attiva"]["comuni"]
    W0, H0 = cam["risoluzione_px"]
    r = larghezza / W0
    W, H = int(larghezza), int(round(H0 * r))
    fx, fy = cam["fx"] * r, cam["fy"] * r
    k = cam[f"k_{livello}"]
    p = {
        "sigla": sigla, "nome_json": SIGLE[sigla], "livello": livello, "scala": r,
        "larghezza": W, "altezza": H, "fx": fx, "fy": fy,
        # centro ottico: il pixel nuovo u' copre i vecchi (u'+0,5)/r − 0,5
        "cx": (cam["cx"] + 0.5) * r - 0.5, "cy": (cam["cy"] + 0.5) * r - 0.5,
        "base_m": cam["base_m"], "z_min_m": cam["z_min_m"], "z_max_m": cam["z_max_modello_m"],
        "fps_sensore": cam["fps"],
        "k": k,                                   # sigma_z = k z^2 [m]
        "sottopixel_px": k * fx * cam["base_m"],  # alla risoluzione di lavoro
        "sottopixel_px_848": cam[f"sottopixel_{livello}_px"],
        "quota_temporale": com["quota_temporale"], "quota_fissa": com["quota_fissa"],
        "correlazione_px": com["correlazione_px"] * r,
        "passo_disparita_px": com["passo_disparita_px"] * r,
        "unita_m": com["unita_profondita_m"],
        "bordo_jitter_px": com["bordo_jitter_px_nominale"] * r if livello == "nominale" else None,
        "bordo_jitter_m": com["bordo_jitter_m_limite"] if livello == "limite" else None,
        "bordo_ingrossamento_px": max(1, int(round(com["bordo_ingrossamento_px"] * r))),
        "bordo_misti_px": com["bordo_misti_px"] * r,
        "p_pixel_misto": com["p_pixel_misto"], "p_buco_bordo": com["p_buco_bordo"],
        "margine_banda_px": com[f"banda_bordo_margine_px_{livello}"] * r,
        "incidenza_soglia_gradi": com["incidenza_soglia_gradi"],
        "p_buco_incidenza_75": com[f"p_buco_incidenza_75_gradi_{livello}"],
        "persistenza_buco": com["persistenza_buco"],
        "p_buco_materiale": [com[f"p_buco_materiale_{livello}"][m] for m in MATERIALI],
        "fattore_materiale": [com["fattore_materiale_sottopixel"].get(m, 1.0) for m in MATERIALI],
        "p_falso_riflesso": com["p_falso_riflesso_lucido"],
        "esposizione_s": com[f"esposizione_s_{livello}"],
        "fattore_incidenza_oltre_soglia_limite": 5.0,
    }
    return p


# ------------------------------------------------------------------------------------------------ camera
class Camera:
    def __init__(self, prof, altezza_m=1.2, inclinazione_gradi=15.0):
        self.W, self.H = prof["larghezza"], prof["altezza"]
        self.fx, self.fy, self.cx, self.cy = prof["fx"], prof["fy"], prof["cx"], prof["cy"]
        self.base = prof["base_m"]
        self.h, self.incl = float(altezza_m), float(inclinazione_gradi)
        t = math.radians(self.incl)
        self.ct, self.st = math.cos(t), math.sin(t)
        a = (np.arange(self.W, dtype=np.float64) - self.cx) / self.fx
        b = (np.arange(self.H, dtype=np.float64) - self.cy) / self.fy
        # direzione del raggio nel mondo, NON normalizzata: il parametro lungo il raggio è Zc
        self.dx = np.ascontiguousarray(np.broadcast_to(a[None, :], (self.H, self.W)))
        self.dq = np.ascontiguousarray(np.broadcast_to((-b * self.ct - self.st)[:, None], (self.H, self.W)))
        self.dz = np.ascontiguousarray(np.broadcast_to((self.ct - b * self.st)[:, None], (self.H, self.W)))
        self.norma = np.sqrt(self.dx ** 2 + self.dq ** 2 + self.dz ** 2)
        self.o = (0.0, self.h, 0.0)
        self.o_destro = (self.base, self.h, 0.0)

    def proietta(self, x, q, z, destro=False):
        """Punto del mondo -> (u, v, Zc) nell'imager sinistro (o destro)."""
        Xc = np.asarray(x, dtype=np.float64) - (self.base if destro else 0.0)
        dq = self.h - np.asarray(q, dtype=np.float64)
        z = np.asarray(z, dtype=np.float64)
        Zc = z * self.ct + dq * self.st
        Yc = dq * self.ct - z * self.st
        with np.errstate(divide="ignore", invalid="ignore"):
            u = self.fx * Xc / Zc + self.cx
            v = self.fy * Yc / Zc + self.cy
        return u, v, Zc

    def al_suolo(self, u, v, Zc):
        """Pixel e profondità -> (x, quota, z) nel riferimento del suolo."""
        Xc = (u - self.cx) * Zc / self.fx
        Yc = (v - self.cy) * Zc / self.fy
        return Xc, self.h - Yc * self.ct - Zc * self.st, Zc * self.ct - Yc * self.st

    def meta(self):
        return {"larghezza": self.W, "altezza": self.H, "fx": self.fx, "fy": self.fy, "cx": self.cx, "cy": self.cy,
                "posa": {"altezza_m": self.h, "inclinazione_gradi": self.incl}}


# ------------------------------------------------------------------------------------------------ raggi
def _sicuro(d):
    return np.where(np.abs(d) < 1e-12, 1e-12, d)


def interseca_scatola(o, dx, dq, dz, lo, hi):
    """Scatola allineata agli assi vista da fuori. Ritorna (t d'ingresso o inf, asse della faccia colpita)."""
    tmin = np.full(np.shape(dx), -INF)
    tmax = np.full(np.shape(dx), INF)
    asse = np.zeros(np.shape(dx), dtype=np.int8)
    for i, d in enumerate((dx, dq, dz)):
        d = _sicuro(d)
        t1, t2 = (lo[i] - o[i]) / d, (hi[i] - o[i]) / d
        ta, tb = np.minimum(t1, t2), np.maximum(t1, t2)
        piu = ta > tmin
        asse = np.where(piu, np.int8(i), asse)
        tmin = np.where(piu, ta, tmin)
        tmax = np.minimum(tmax, tb)
    colpito = (tmax > tmin) & (tmin > 1e-9)
    return np.where(colpito, tmin, INF), asse


def interseca_stanza(o, dx, dq, dz, lo, hi):
    """Stanza (scatola vista da dentro). Ritorna (t d'uscita, asse della faccia)."""
    t = np.full(np.shape(dx), INF)
    asse = np.zeros(np.shape(dx), dtype=np.int8)
    for i, d in enumerate((dx, dq, dz)):
        d = _sicuro(d)
        te = np.where(d > 0, (hi[i] - o[i]) / d, (lo[i] - o[i]) / d)
        piu = te < t
        asse = np.where(piu, np.int8(i), asse)
        t = np.where(piu, te, t)
    return t, asse


def interseca_capsula(o, dx, dq, dz, xc, zc, r, alt):
    """Capsula verticale: cilindro di raggio r da quota 0 a alt−r, più semisfera in cima (cima a quota alt).
    Ritorna (t d'ingresso o inf, coseno dell'incidenza)."""
    ex, ez = o[0] - xc, o[2] - zc
    a = dx * dx + dz * dz
    b = dx * ex + dz * ez
    c = ex * ex + ez * ez - r * r
    norma = np.sqrt(a + dq * dq)
    with np.errstate(invalid="ignore", divide="ignore"):
        disc = b * b - a * c
        tc = (-b - np.sqrt(disc)) / a
        qc = o[1] + tc * dq
        okc = (disc > 0) & (tc > 1e-9) & (qc >= 0.0) & (qc <= alt - r)
        ey = o[1] - (alt - r)
        a3, b3, c3 = a + dq * dq, b + dq * ey, c + ey * ey
        disc3 = b3 * b3 - a3 * c3
        ts = (-b3 - np.sqrt(disc3)) / a3
        qs = o[1] + ts * dq
        oks = (disc3 > 0) & (ts > 1e-9) & (qs >= alt - r)
        cos_c = np.abs((ex + tc * dx) * dx + (ez + tc * dz) * dz) / (r * norma)
        cos_s = np.abs((ex + ts * dx) * dx + (ey + ts * dq) * dq + (ez + ts * dz) * dz) / (r * norma)
    t = np.where(okc, tc, INF)
    cosi = np.where(okc, cos_c, 1.0)
    meglio = oks & (ts < t)
    t = np.where(meglio, ts, t)
    cosi = np.where(meglio, cos_s, cosi)
    return t, np.clip(cosi, 0.0, 1.0)


# ------------------------------------------------------------------------------------------------ scena
class Scatola:
    """Ostacolo fisso: scatola allineata agli assi del suolo. `trasparente` = lastra di vetro."""

    def __init__(self, ident, x0, x1, z0, z1, q0, q1, materiale=M_CHIARO, trasparente=False, tipo="scatola"):
        self.id, self.tipo = ident, tipo
        self.lo, self.hi = (x0, q0, z0), (x1, q1, z1)
        self.materiale, self.trasparente = materiale, trasparente

    def in_verita(self):
        (x0, q0, z0), (x1, q1, z1) = self.lo, self.hi
        return {"id": self.id, "tipo": "poligono", "vertici": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]],
                "altezza_m": q1, "quota_base_m": q0, "materiale": MATERIALI[self.materiale],
                "trasparente": self.trasparente, "genere": self.tipo}


class Scena:
    """Stanza (pavimento a quota 0, soffitto, quattro pareti) più ostacoli fissi."""

    def __init__(self, x=(-4.0, 4.0), z=(-1.0, 6.0), soffitto=3.0, materiale_suolo=M_CHIARO, ostacoli=(),
                 vetro="sfondo"):
        self.lo, self.hi = (x[0], 0.0, z[0]), (x[1], soffitto, z[1])
        self.materiale_suolo = materiale_suolo
        self.ostacoli = list(ostacoli)
        assert vetro in ("sfondo", "buco")
        self.vetro = vetro

    def opachi(self):
        return [o for o in self.ostacoli if not o.trasparente]

    def in_verita(self):
        (x0, _, z0), (x1, q1, z1) = self.lo, self.hi
        s = 0.1
        muri = [("parete_fondo", x0, x1, z1, z1 + s), ("parete_sinistra", x0 - s, x0, z0, z1),
                ("parete_destra", x1, x1 + s, z0, z1), ("parete_dietro", x0, x1, z0 - s, z0)]
        fuori = [{"id": n, "tipo": "poligono", "vertici": [[a, c], [b, c], [b, d], [a, d]], "altezza_m": q1,
                  "quota_base_m": 0.0, "materiale": MATERIALI[M_CHIARO], "trasparente": False, "genere": "struttura"}
                 for n, a, b, c, d in muri]
        return [o.in_verita() for o in self.ostacoli] + fuori


class Ideale:
    """Immagine ideale: Z (Zc in metri, inf = niente), obj (identità), mat (materiale), cosi (coseno incidenza)."""
    __slots__ = ("Z", "obj", "mat", "cosi", "vetro", "Zrifl", "vetro_buco")

    def copia(self):
        n = Ideale()
        n.Z, n.obj, n.mat, n.cosi = self.Z.copy(), self.obj.copy(), self.mat.copy(), self.cosi.copy()
        n.vetro, n.Zrifl, n.vetro_buco = self.vetro, self.Zrifl, self.vetro_buco
        return n


def _ostacoli_piu_vicini(scena, o, dx, dq, dz):
    """Il più vicino fra gli ostacoli opachi: (t, indice, asse)."""
    t = np.full(np.shape(dx), INF)
    idx = np.full(np.shape(dx), -1, dtype=np.int16)
    asse = np.zeros(np.shape(dx), dtype=np.int8)
    for i, ost in enumerate(scena.ostacoli):
        if ost.trasparente:
            continue
        ti, ai = interseca_scatola(o, dx, dq, dz, ost.lo, ost.hi)
        piu = ti < t
        t = np.where(piu, ti, t)
        idx = np.where(piu, np.int16(i), idx)
        asse = np.where(piu, ai, asse)
    return t, idx, asse


def resa_statica(scena, cam):
    """Profondità ideale della scena fissa (senza persone)."""
    o, dx, dq, dz = cam.o, cam.dx, cam.dq, cam.dz
    comp = (dx, dq, dz)
    ts, asse_s = interseca_stanza(o, dx, dq, dz, scena.lo, scena.hi)
    suolo = (asse_s == 1) & (dq < 0)
    idl = Ideale()
    idl.Z = ts.copy()
    idl.obj = np.where(suolo, O_SUOLO, O_STANZA).astype(np.int16)
    idl.mat = np.where(suolo, scena.materiale_suolo, M_CHIARO).astype(np.uint8)
    asse = asse_s.copy()
    to, io, ao = _ostacoli_piu_vicini(scena, o, dx, dq, dz)
    piu = to < idl.Z
    idl.Z = np.where(piu, to, idl.Z)
    idl.obj = np.where(piu, O_OSTACOLO0 + io, idl.obj).astype(np.int16)
    mat_o = np.array([ost.materiale for ost in scena.ostacoli] + [M_CHIARO], dtype=np.uint8)
    idl.mat = np.where(piu, mat_o[io], idl.mat).astype(np.uint8)
    asse = np.where(piu, ao, asse)
    comp_asse = np.choose(asse, [np.abs(c) for c in comp])
    idl.cosi = np.clip(comp_asse / cam.norma, 0.0, 1.0)
    # lastre di vetro: il raggio le attraversa; si ricorda dove
    idl.vetro = np.zeros(idl.Z.shape, dtype=bool)
    idl.vetro_buco = scena.vetro == "buco"
    for ost in scena.ostacoli:
        if ost.trasparente:
            tv, _ = interseca_scatola(o, dx, dq, dz, ost.lo, ost.hi)
            idl.vetro |= tv < idl.Z
    # riflesso sul pavimento lucido: profondità dell'immagine speculare (raggio riflesso sul suolo)
    idl.Zrifl = None
    if scena.materiale_suolo == M_LUCIDO:
        t0 = ts
        px, pz = o[0] + t0 * dx, o[2] + t0 * dz
        # origine sul suolo, direzione con la quota ribaltata; il suolo stesso è escluso (quota 1e-6)
        t2s, _ = _stanza_da_punti(px, pz, dx, -dq, dz, scena)
        t2o = _ostacoli_da_punti(px, pz, dx, -dq, dz, scena)
        idl.Zrifl = np.where(idl.obj == O_SUOLO, t0 + np.minimum(t2s, t2o), INF)
    return idl


def _stanza_da_punti(px, pz, dx, dq, dz, scena):
    t = np.full(np.shape(dx), INF)
    for d, p0, lo, hi in ((dx, px, scena.lo[0], scena.hi[0]), (dq, 1e-6, scena.lo[1], scena.hi[1]),
                          (dz, pz, scena.lo[2], scena.hi[2])):
        d = _sicuro(d)
        te = np.where(d > 0, (hi - p0) / d, (lo - p0) / d)
        t = np.minimum(t, te)
    return t, None


def _ostacoli_da_punti(px, pz, dx, dq, dz, scena):
    t = np.full(np.shape(dx), INF)
    for ost in scena.opachi():
        tmin = np.full(np.shape(dx), -INF)
        tmax = np.full(np.shape(dx), INF)
        for d, p0, lo, hi in ((dx, px, ost.lo[0], ost.hi[0]), (dq, 1e-6, ost.lo[1], ost.hi[1]),
                              (dz, pz, ost.lo[2], ost.hi[2])):
            d = _sicuro(d)
            t1, t2 = (lo - p0) / d, (hi - p0) / d
            tmin = np.maximum(tmin, np.minimum(t1, t2))
            tmax = np.minimum(tmax, np.maximum(t1, t2))
        t = np.minimum(t, np.where((tmax > tmin) & (tmin > 1e-6), tmin, INF))
    return t


class Persona:
    def __init__(self, ident, x, z, raggio=0.2, altezza=1.7, materiale=M_CHIARO):
        self.id, self.x, self.z = ident, float(x), float(z)
        self.raggio, self.altezza, self.materiale = float(raggio), float(altezza), materiale


def componi(statica, cam, persone, raggio_in_piu=None):
    """Aggiunge le persone alla scena fissa. Ritorna (ideale, conteggi), con per ogni persona i pixel della sagoma
    (da sola nell'immagine) e quelli visibili (non coperti)."""
    idl = statica.copia()
    conteggi = []
    for k, p in enumerate(persone):
        r = p.raggio + (raggio_in_piu[k] if raggio_in_piu is not None else 0.0)
        # colonne interessate (riquadro della capsula proiettato), per non calcolare tutta l'immagine
        xs = np.array([p.x - r, p.x + r] * 4)
        zs = np.array([p.z - r, p.z - r, p.z + r, p.z + r] * 2)
        qs = np.array([0.0] * 4 + [p.altezza] * 4)
        u, _, Zc = cam.proietta(xs, qs, zs)
        if np.all(Zc > 0.05):
            c0, c1 = max(0, int(np.floor(u.min())) - 2), min(cam.W, int(np.ceil(u.max())) + 3)
        else:
            c0, c1 = 0, cam.W
        if c1 <= c0:
            conteggi.append((0, 0))
            continue
        sl = (slice(None), slice(c0, c1))
        t, cosi = interseca_capsula(cam.o, cam.dx[sl], cam.dq[sl], cam.dz[sl], p.x, p.z, r, p.altezza)
        piu = t < idl.Z[sl]
        idl.Z[sl] = np.where(piu, t, idl.Z[sl])
        idl.obj[sl] = np.where(piu, O_PERSONA0 + k, idl.obj[sl])
        idl.mat[sl] = np.where(piu, p.materiale, idl.mat[sl])
        idl.cosi[sl] = np.where(piu, cosi, idl.cosi[sl])
        conteggi.append((int(np.isfinite(t).sum()), 0))
    for k in range(len(persone)):
        conteggi[k] = (conteggi[k][0], int((idl.obj == O_PERSONA0 + k).sum()))
    return idl, conteggi


# ------------------------------------------------------------------------------------------------ sensore
def _salti_orizzontali(Z):
    """Salti di profondità fra colonne adiacenti: matrice (H, W−1)."""
    a, b = Z[:, :-1], Z[:, 1:]
    fa, fb = np.isfinite(a), np.isfinite(b)
    with np.errstate(invalid="ignore"):
        vicino = np.minimum(a, b)
        s = np.abs(a - b) > np.maximum(0.06, 0.04 * vicino)
    return (s & fa & fb) | (fa ^ fb)


def _salti_verticali(Z):
    a, b = Z[:-1, :], Z[1:, :]
    fa, fb = np.isfinite(a), np.isfinite(b)
    with np.errstate(invalid="ignore"):
        vicino = np.minimum(a, b)
        # sul suolo radente righe adiacenti distano molto: soglia più larga che in orizzontale
        s = np.abs(a - b) > np.maximum(0.10, 0.12 * vicino)
    return (s & fa & fb) | (fa ^ fb)


INTERRUTTORI = {"bordi": True, "rumore": True, "buchi": True, "quantizza": True, "occlusione": True}


class Sensore:
    """Il modello del sensore: da un'immagine ideale a una matrice uint16 in millimetri (0 = nessun dato)."""

    def __init__(self, prof, cam, seme, interruttori=None):
        self.p, self.cam = prof, cam
        self.rng = np.random.default_rng(seme)
        self.on = dict(INTERRUTTORI)
        if interruttori:
            self.on.update(interruttori)
        self.H, self.W = cam.H, cam.W
        self.fB = cam.fx * cam.base
        self.U = np.ascontiguousarray(np.broadcast_to(np.arange(self.W)[None, :], (self.H, self.W)))
        self._norme = {}
        self.fisso = self._campo(prof["correlazione_px"])
        self.buco = None
        self.obj_prec = None
        self.ultimo = {}      # mappe dell'ultimo fotogramma (per i controlli e per la verità)

    def _campo(self, sigma):
        """Campo gaussiano a media nulla e varianza 1, correlato nello spazio (filtro gaussiano di scarto sigma)."""
        chiave = tuple(np.atleast_1d(sigma).tolist())
        if chiave not in self._norme:
            imp = np.zeros((self.H, self.W), dtype=np.float64)
            imp[self.H // 2, self.W // 2] = 1.0
            nucleo = ndimage.gaussian_filter(imp, sigma, mode="wrap")
            self._norme[chiave] = 1.0 / math.sqrt(float((nucleo ** 2).sum()))
        g = self.rng.standard_normal((self.H, self.W), dtype=np.float32)
        return ndimage.gaussian_filter(g, sigma, mode="wrap") * np.float32(self._norme[chiave])

    def _fattore_incidenza(self, cosi, ang):
        inv = 1.0 / np.maximum(cosi, COS_MIN)
        soglia = self.p["incidenza_soglia_gradi"]
        if self.p["livello"] == "nominale":
            return np.where(ang > soglia, inv, 1.0)
        return np.where(ang > soglia, np.maximum(self.p["fattore_incidenza_oltre_soglia_limite"], inv), inv)

    def misura(self, idl, forza_zero=None):
        p, on, rng = self.p, self.on, self.rng
        H, W, U = self.H, self.W, self.U
        Z, obj, mat, cosi = idl.Z, idl.obj, idl.mat, idl.cosi
        vetro, Zrifl = idl.vetro, idl.Zrifl

        # ---- passo 3a: i bordi verticali si spostano lungo la riga e l'oggetto vicino si ingrossa
        src = None
        if on["bordi"]:
            salto = _salti_orizzontali(Z)
            if salto.any():
                bordo = np.zeros((H, W), dtype=bool)
                bordo[:, :-1] |= salto
                bordo[:, 1:] |= salto
                if p["bordo_jitter_px"] is not None:
                    sig_px = np.float32(p["bordo_jitter_px"])
                    sig_max = float(sig_px)
                else:
                    raggio0 = int(math.ceil(3 * p["bordo_jitter_m"] * self.cam.fx / max(p["z_min_m"], 0.5))) + 2
                    Zv = ndimage.minimum_filter1d(np.where(np.isfinite(Z), Z, 1e6), size=2 * min(raggio0, 40) + 1,
                                                  axis=1, mode="nearest")
                    sig_px = (p["bordo_jitter_m"] * self.cam.fx / np.maximum(Zv, p["z_min_m"])).astype(np.float32)
                    sig_max = float(sig_px[bordo].max())
                raggio = int(math.ceil(3 * sig_max)) + 2
                zona = ndimage.maximum_filter1d(bordo.view(np.uint8), size=2 * raggio + 1, axis=1,
                                                mode="constant") > 0
                # campo liscio lungo la riga (uno spostamento per bordo), correlato in verticale
                S = self._campo((p["correlazione_px"], max(8.0, 4.0 * sig_max))) * sig_px
                sh = np.rint(S).astype(np.intp)
                sh[~zona] = 0
                src = np.clip(U - sh, 0, W - 1)
                for _ in range(p["bordo_ingrossamento_px"]):
                    Zs = np.take_along_axis(Z, src, axis=1)
                    s2 = _salti_orizzontali(Zs)
                    with np.errstate(invalid="ignore"):
                        sx_vicino = Zs[:, :-1] < Zs[:, 1:]
                    nuovo = src.copy()
                    m = s2 & sx_vicino
                    nuovo[:, 1:][m] = src[:, :-1][m]
                    m = s2 & ~sx_vicino
                    nuovo[:, :-1][m] = src[:, 1:][m]
                    src = nuovo
        if src is not None:
            Z = np.take_along_axis(Z, src, axis=1)
            obj = np.take_along_axis(obj, src, axis=1)
            mat = np.take_along_axis(mat, src, axis=1)
            cosi = np.take_along_axis(cosi, src, axis=1)
            vetro = np.take_along_axis(vetro, src, axis=1)
            if Zrifl is not None:
                Zrifl = np.take_along_axis(Zrifl, src, axis=1)

        # ---- passo 1: disparità
        finito = np.isfinite(Z)
        with np.errstate(divide="ignore"):
            d = np.where(finito, self.fB / np.where(finito, Z, 1.0), 0.0)

        # ---- passo 2: buchi geometrici
        fuori = (~finito) | (Z < p["z_min_m"]) | (Z > p["z_max_m"])
        xd = U - d
        banda = xd < p["margine_banda_px"]
        if on["occlusione"]:
            m = np.minimum.accumulate(xd[:, ::-1], axis=1)[:, ::-1]
            occl = np.zeros((H, W), dtype=bool)
            occl[:, :-1] = m[:, 1:] <= xd[:, :-1]
        else:
            occl = np.zeros((H, W), dtype=bool)
            banda = np.zeros((H, W), dtype=bool)
        vuoto = fuori | banda | occl
        if idl.vetro_buco:
            vuoto |= vetro

        # ---- passo 3b: pixel misti a cavallo dei salti
        if on["bordi"]:
            altro = np.zeros((H, W), dtype=np.float64)
            ha = np.zeros((H, W), dtype=bool)
            sh_ = _salti_orizzontali(Z)
            sv_ = _salti_verticali(Z)
            if sh_.any() or sv_.any():
                ok_h = sh_ & finito[:, :-1] & finito[:, 1:]
                ok_v = sv_ & finito[:-1, :] & finito[1:, :]
                altro[:, :-1][ok_h] = d[:, 1:][ok_h]
                ha[:, :-1] |= ok_h
                altro[:, 1:][ok_h] = d[:, :-1][ok_h]
                ha[:, 1:] |= ok_h
                altro[:-1, :][ok_v] = d[1:, :][ok_v]
                ha[:-1, :] |= ok_v
                altro[1:, :][ok_v] = d[:-1, :][ok_v]
                ha[1:, :] |= ok_v
                r4 = rng.random((4, H, W), dtype=np.float32)
                scelto = ha & (r4[0] < p["bordo_misti_px"] / 2.0)
                misto = scelto & (r4[1] < p["p_pixel_misto"])
                d = np.where(misto, d + r4[2] * (altro - d), d)
                vuoto |= scelto & ~misto & (r4[3] < p["p_buco_bordo"])
                self.ultimo["misto"] = misto

        # ---- passo 6 (deciso prima del rumore): buchi casuali a macchie, catena di Markov nel tempo
        ang = np.degrees(np.arccos(np.clip(cosi, 0.0, 1.0)))
        falso = None
        if on["buchi"]:
            p_mat = np.asarray(p["p_buco_materiale"], dtype=np.float64)[mat]
            p_inc = p["p_buco_incidenza_75"] * np.clip((ang - p["incidenza_soglia_gradi"]) / 15.0, 0.0, None)
            p_b = np.clip(p_mat + p_inc, 0.0, 1.0)
            V = special.ndtr(self._campo(p["correlazione_px"]))
            if self.buco is None:
                soglia = p_b
            else:
                s = p["persistenza_buco"]
                q = np.clip(p_b * (1.0 - s) / np.maximum(1.0 - p_b, 1e-9), 0.0, 1.0)
                soglia = np.where(self.buco, np.maximum(s, p_b), q)
                soglia = np.where(obj != self.obj_prec, p_b, soglia)
            buco = V < soglia
            self.buco, self.obj_prec = buco, obj
            if Zrifl is not None:
                V2 = special.ndtr(self._campo(p["correlazione_px"]))
                falso = buco & (mat == M_LUCIDO) & (V2 < p["p_falso_riflesso"]) & np.isfinite(Zrifl)
                d = np.where(falso, self.fB / np.where(falso, Zrifl, 1.0), d)
                buco = buco & ~falso
            vuoto |= buco

        # ---- passo 4: rumore in disparità, parte fissa e parte temporale, correlate nello spazio
        if on["rumore"]:
            fatt = self._fattore_incidenza(cosi, ang) * np.asarray(p["fattore_materiale"], dtype=np.float64)[mat]
            T = self._campo(p["correlazione_px"])
            d = d + p["sottopixel_px"] * fatt * (p["quota_fissa"] * self.fisso + p["quota_temporale"] * T)

        # ---- passo 5: quantizzazione in disparità e in profondità
        if on["quantizza"]:
            d = np.rint(d / p["passo_disparita_px"]) * p["passo_disparita_px"]
        valido = (d > 1e-9) & ~vuoto
        with np.errstate(divide="ignore", invalid="ignore"):
            Zm = np.where(valido, self.fB / np.where(valido, d, 1.0), 0.0)
        valido &= (Zm >= p["z_min_m"]) & (Zm <= p["z_max_m"])
        mm = np.rint(Zm / p["unita_m"]) * (p["unita_m"] * 1000.0)
        valido &= mm < 65535.5
        if forza_zero is not None:
            valido &= ~forza_zero
        uscita = np.where(valido, mm, 0.0).astype(np.uint16)
        self.ultimo.update({"obj": obj, "occlusione": occl, "banda": banda, "falso": falso, "src": src})
        return uscita


# ------------------------------------------------------------------------------------------------ filtri
class FiltriRealsense:
    """Emulazione dei blocchi dell'SDK RealSense con i valori predefiniti, applicati alla profondità in millimetri:
    filtro temporale (alfa 0,4; delta 20; persistenza 3 = «valido in 2 degli ultimi 4») e riempimento dei buchi
    (modo 1: dal vicino più lontano fra sopra, sopra-sinistra, sinistra, sotto-sinistra, sotto; sul posto, per righe).
    Regole rilette dai sorgenti in scaricati/librealsense/ (temporal-filter.h, hole-filling-filter.h).
    NON emulati: decimazione, filtro spaziale, passaggio in disparità (delta qui vale 20 mm)."""

    def __init__(self, alfa=0.4, delta=20, persistenza=3, temporale=True, riempimento=True):
        assert persistenza == 3, "emulata solo la regola predefinita (3: valido in 2 degli ultimi 4)"
        self.alfa, self.delta = float(alfa), int(delta)
        self.temporale, self.riempimento = temporale, riempimento
        self.ultimo = None
        self.storia = None
        self.fase = 0

    def applica(self, f):
        f = np.asarray(f, dtype=np.uint16)
        if self.temporale:
            f = self._temporale(f)
        if self.riempimento:
            f = self._riempi_lontano(f)
        return f

    def _temporale(self, f):
        if self.ultimo is None:
            self.ultimo = np.zeros(f.shape, dtype=np.uint16)
            self.storia = np.zeros(f.shape, dtype=np.uint8)
        maschera = np.uint8(1 << self.fase)
        cur = f.astype(np.int32)
        prec = self.ultimo.astype(np.int32)
        ha_cur, ha_prec = cur > 0, prec > 0
        concordi = ha_cur & ha_prec & (np.abs(cur - prec) < self.delta)
        filtrato = (self.alfa * cur + (1.0 - self.alfa) * prec).astype(np.int32)     # troncato, come nel sorgente
        uscita = np.where(concordi, filtrato, cur)
        # persistenza: gli ultimi quattro fotogrammi sono i bit fase−1 … fase−4 (mod 8)
        somma = np.zeros(f.shape, dtype=np.uint8)
        for j in range(1, 5):
            somma += (self.storia >> np.uint8((self.fase - j) % 8)) & np.uint8(1)
        riempi = (~ha_cur) & ha_prec & (somma >= 2)
        uscita = np.where(riempi, prec, uscita)
        # aggiornamento dello stato
        nuovo_ultimo = np.where(ha_cur, np.where(concordi, filtrato, cur), prec)
        storia = self.storia.copy()
        storia = np.where(concordi, storia | maschera, storia)
        storia = np.where(ha_cur & ~concordi, maschera, storia)
        storia = np.where(~ha_cur, storia & np.uint8(~maschera & 0xFF), storia)
        self.ultimo, self.storia = nuovo_ultimo.astype(np.uint16), storia.astype(np.uint8)
        self.fase = (self.fase + 1) % 8
        return uscita.astype(np.uint16)

    @staticmethod
    def _riempi_lontano(f):
        g = f.astype(np.int64)
        H, W = g.shape
        GRANDE = 100000
        for j in range(1, H - 1):
            sopra, sotto = g[j - 1], f[j + 1].astype(np.int64)      # sopra: già trattata; sotto: originale
            riga = g[j]
            cand = sopra.copy()
            cand[1:] = np.maximum(cand[1:], sopra[:-1])
            cand[1:] = np.maximum(cand[1:], sotto[:-1])
            cand = np.maximum(cand, sotto)
            # un pixel valido (o la colonna 0, che il sorgente non tocca) apre un tratto; nei buchi vale il massimo
            # progressivo fra il valore a sinistra e i candidati
            apre = riga > 0
            apre[0] = True
            val = np.where(apre, riga, cand)
            tratto = np.cumsum(apre)
            chiave = np.maximum.accumulate(tratto * GRANDE + val)
            g[j] = np.where(apre, riga, chiave - tratto * GRANDE)
        return g.astype(np.uint16)


# ------------------------------------------------------------------------------------------------ verità
C_VISIBILE, C_OMBRA, C_FUORI, C_IMPRONTA, C_BANDA = 0, 1, 2, 3, 4
CODICI_OMBRA = {"0": "suolo visibile da entrambi gli imager (misurabile)",
                "1": "in ombra: coperto da un ostacolo fisso per l'imager di riferimento (sinistro)",
                "2": "non osservabile: fuori dall'immagine o fuori portata",
                "3": "sotto l'impronta di un ostacolo che tocca il suolo",
                "4": "banda stereo: visibile dal sinistro, ma coperto o fuori campo per il destro (nessun dato atteso)"}


def classe_suolo(scena, cam, prof, x, z, persone=()):
    """Classe (codici C_*) dei punti del suolo (x, z): la verità dell'ombra. Vettoriale.
    Con `persone` (lista di Persona) anche i corpi fanno ombra; in verita.json si scrive solo quella fissa."""
    x = np.asarray(x, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)
    q = np.zeros_like(x)
    u, v, Zc = cam.proietta(x, q, z)
    with np.errstate(invalid="ignore"):
        in_campo = (Zc >= prof["z_min_m"]) & (Zc <= prof["z_max_m"]) & (u >= -0.5) & (u <= cam.W - 0.5) \
            & (v >= -0.5) & (v <= cam.H - 0.5)
        in_campo &= (x >= scena.lo[0]) & (x <= scena.hi[0]) & (z >= scena.lo[2]) & (z <= scena.hi[2])
    coperto = []
    for o in (cam.o, cam.o_destro):
        dx, dq, dz = x - o[0], q - o[1], z - o[2]
        t, _, _ = _ostacoli_piu_vicini(scena, o, dx, dq, dz)
        for p in persone:
            tp, _ = interseca_capsula(o, dx, dq, dz, p.x, p.z, p.raggio, p.altezza)
            t = np.minimum(t, tp)
        coperto.append(t < 1.0 - 1e-6)
    ur, _, _ = cam.proietta(x, q, z, destro=True)
    with np.errstate(invalid="ignore"):
        fuori_destro = ur < prof["margine_banda_px"]
    impronta = np.zeros(x.shape, dtype=bool)
    for ost in scena.opachi():
        if ost.lo[1] <= 1e-6:
            impronta |= (x >= ost.lo[0]) & (x <= ost.hi[0]) & (z >= ost.lo[2]) & (z <= ost.hi[2])
    for p in persone:
        impronta |= (x - p.x) ** 2 + (z - p.z) ** 2 <= p.raggio ** 2
    c = np.full(x.shape, C_VISIBILE, dtype=np.uint8)
    c[coperto[1] | fuori_destro] = C_BANDA
    c[coperto[0]] = C_OMBRA
    c[~in_campo] = C_FUORI
    c[impronta] = C_IMPRONTA
    return c


def maschere_ombra(scena, cam, prof, r_max=4.0, passo_r=0.1, passo_gradi=1.0, mezzo_campo_gradi=50.0,
                   passo_cart=0.025, x_cart=(-3.0, 3.0), z_cart=(0.0, 4.0)):
    """Le due maschere scritte in verita.json: polare (celle del nucleo: 1° × 0,1 m, valutate al CENTRO della cella)
    e cartesiana fitta. Ogni riga è una stringa di cifre (codici C_*)."""
    az = np.arange(-mezzo_campo_gradi + passo_gradi / 2, mezzo_campo_gradi, passo_gradi)
    rr = np.arange(passo_r / 2, r_max, passo_r)
    A, R = np.meshgrid(np.radians(az), rr)
    pol = classe_suolo(scena, cam, prof, R * np.sin(A), R * np.cos(A))
    xs = np.arange(x_cart[0] + passo_cart / 2, x_cart[1], passo_cart)
    zs = np.arange(z_cart[0] + passo_cart / 2, z_cart[1], passo_cart)
    X, Zg = np.meshgrid(xs, zs)
    car = classe_suolo(scena, cam, prof, X, Zg)

    def righe(m):
        return ["".join(map(str, r)) for r in m.tolist()]

    return {
        "codici": CODICI_OMBRA,
        "nota": "solo gli ostacoli fissi (le persone non fanno ombra qui: per quella si chiama "
                "simsens.classe_suolo con le persone). Azimut: atan2(x, z), positivo a destra; distanza sul suolo "
                "dall'origine (punto sotto il centro ottico).",
        "polare": {"azimut_gradi_centro_prima": float(az[0]), "passo_gradi": passo_gradi, "n_azimut": int(az.size),
                   "distanza_m_centro_prima": float(rr[0]), "passo_m": passo_r, "n_distanze": int(rr.size),
                   "ordine": "righe = distanze crescenti, colonne = azimut crescenti", "celle": righe(pol)},
        "cartesiana": {"x_m_centro_prima": float(xs[0]), "z_m_centro_prima": float(zs[0]), "passo_m": passo_cart,
                       "n_x": int(xs.size), "n_z": int(zs.size),
                       "ordine": "righe = z crescenti, colonne = x crescenti", "celle": righe(car)},
    }
