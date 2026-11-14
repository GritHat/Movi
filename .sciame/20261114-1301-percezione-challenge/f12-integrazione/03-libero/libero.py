# libero.py — le candidate per il «libero» della cella dal SOLO fotogramma corrente (K-107), in numpy.
# sciame-nuvole-punti, f12, 14 novembre 2026. Codice mio. Riprendo, dichiarandolo:
#   - il modello di camera, il margine m(z) = 0,03 + 3 k z^2 e lo pseudocodice di `leggi` da f7-estensione/14-attacco/sim.py;
#   - la riga di V-017 da 14-attacco/av10.py (cella_av4) e le soglie della griglia (>= 3 pixel, quota 0,07-2,0 m);
#   - il meccanismo di V-018 da 15-verifica/vq3c.c (tabella pixel -> cella del suolo e profondita' attesa).
# Convenzioni: mondo x a destra, y in avanti, z in alto; camera in (0, 0, h), inclinata di `pitch` gradi in basso;
# profondita' Z lungo l'asse ottico in metri, 0 = non valido; pixel (i colonna, j riga), centro del primo pixel in (0, 0).
import math
import numpy as np

LIB, OCC, OMB, NV, FUORI = 1, 2, 3, 4, 5
NR, DR, RMAX = 30, 0.1, 3.0
QS = (0.2, 0.6, 1.0, 1.4, 1.8)
Q_BASSA, Q_ALTA, MIN_PIX = 0.07, 2.0, 3


def marg(z, k):
    return 0.03 + 3.0 * k * z * z


class Camera:
    def __init__(s, W, H, fx, fy, cx, cy, h, pitch):
        s.W, s.H, s.fx, s.fy, s.cx, s.cy, s.h, s.pitch = W, H, fx, fy, cx, cy, h, pitch
        s.tx = np.repeat(((np.arange(W) - cx) / fx)[None, :], H, 0)
        s.ty = np.repeat((-(np.arange(H) - cy) / fy)[:, None], W, 1)
        s.AZ0 = math.degrees(math.atan(max(cx + 0.5, W - 0.5 - cx) / fx))
        s.NA = int(round(2 * s.AZ0))

    def raggi(s, pitch=None):
        p = math.radians(s.pitch if pitch is None else pitch)
        return s.tx, math.cos(p) + s.ty * math.sin(p), -math.sin(p) + s.ty * math.cos(p)

    def proietta(s, x, y, z, pitch=None):
        p = math.radians(s.pitch if pitch is None else pitch)
        sp, cp = math.sin(p), math.cos(p)
        vz = z - s.h
        Zc = y * cp - vz * sp
        up = y * sp + vz * cp
        Zs = np.where(Zc > 0.05, Zc, 1.0)
        i = np.floor(x / Zs * s.fx + s.cx + 0.5).astype(np.int64)
        j = np.floor(s.cy - up / Zs * s.fy + 0.5).astype(np.int64)
        ok = (Zc > 0.05) & (i >= 1) & (i <= s.W - 2) & (j >= 1) & (j <= s.H - 2)
        return np.where(ok, i, 1), np.where(ok, j, 1), Zc, ok


def camera_ideale(pitch=15.0, h=1.2, W=320, H=240, hfov=87.0, vfov=58.0):
    fx = (W / 2) / math.tan(math.radians(hfov / 2))
    fy = (H / 2) / math.tan(math.radians(vfov / 2))
    return Camera(W, H, fx, fy, W / 2 - 0.5, H / 2 - 0.5, h, pitch)


class Regole:
    """Tutto cio' che e' fisso a sensore fermo si calcola una volta (posa CREDUTA): centri, proiezioni, impronta."""

    def __init__(s, cam, k):
        s.cam, s.k, s.NA = cam, k, cam.NA
        a, r = np.arange(s.NA), np.arange(NR)
        az = np.radians(a + 0.5 - cam.AZ0)[:, None]
        rr = ((r + 0.5) * DR)[None, :]
        s.cx, s.cy = rr * np.sin(az), rr * np.cos(az)
        s.rix = np.repeat(r[None, :], s.NA, 0)
        s.proj = {}
        for q in (0.10,) + QS:
            i, j, z, ok = cam.proietta(s.cx, s.cy, q)
            s.proj[q] = (i, j, z, ok, marg(z, k))
        s.dx, s.dy, s.dz = cam.raggi()
        giu = s.dz < -1e-9
        t = np.where(giu, cam.h / np.where(giu, -s.dz, 1.0), 0.0)      # Z atteso del suolo per pixel
        gx, gy = t * s.dx, t * s.dy
        grr, gaz = np.hypot(gx, gy), np.degrees(np.arctan2(gx, gy)) + cam.AZ0
        okc = giu & (gy > 0) & (grr < RMAX) & (gaz >= 0) & (gaz < s.NA)
        cell = np.where(okc, gaz.astype(np.int64) * NR + (grr / DR).astype(np.int64), -1).ravel()
        s.fp_idx = np.nonzero(cell >= 0)[0]
        s.fp_c = cell[s.fp_idx]
        s.fp_z = t.ravel()[s.fp_idx]
        s.fp_m = marg(s.fp_z, k)
        s.fp_tot = np.bincount(s.fp_c, minlength=s.NA * NR).reshape(s.NA, NR)
        s.fp_meta = np.maximum(1, (s.fp_tot + 1) // 2)

    def griglia(s, D):
        """occupato (>= 3 pixel validi a quota 0,07-2,0 m nella cella) e ombra (oltre il primo ritorno), di ORA."""
        X, Y, Z = D * s.dx, D * s.dy, s.cam.h + D * s.dz
        rr = np.hypot(X, Y)
        az = np.degrees(np.arctan2(X, Y)) + s.cam.AZ0
        sel = (D > 0) & (Y > 0) & (rr < RMAX) & (az >= 0) & (az < s.NA) & (Z >= Q_BASSA) & (Z <= Q_ALTA)
        c = az[sel].astype(np.int64) * NR + (rr[sel] / DR).astype(np.int64)
        occ = np.bincount(c, minlength=s.NA * NR).reshape(s.NA, NR) >= MIN_PIX
        r0 = np.where(occ.any(1), occ.argmax(1), NR)
        return occ, r0, s.rix > r0[:, None]

    @staticmethod
    def prep3(D):
        """minimo e massimo sull'intorno 3 x 3 (interno dell'immagine); minimo 0 = c'e' un pixel non valido."""
        a = np.minimum(np.minimum(D[:-2], D[1:-1]), D[2:])
        b = np.maximum(np.maximum(D[:-2], D[1:-1]), D[2:])
        return (np.minimum(np.minimum(a[:, :-2], a[:, 1:-1]), a[:, 2:]),
                np.maximum(np.maximum(b[:, :-2], b[:, 1:-1]), b[:, 2:]))

    def leggi(s, p3, q):
        """stato(p) del centro di ogni cella a quota q, nel solo fotogramma corrente."""
        i, j, z, ok, m = s.proj[q]
        dmin, dmax = p3[0][j - 1, i - 1], p3[1][j - 1, i - 1]
        st = np.where(z < dmin - m, LIB, np.where(z > dmax + m, OMB, OCC))
        st = np.where(dmin <= 0, NV, st)
        return np.where(ok, st, FUORI)

    def impronta(s, D):
        """per cella: quanti pixel della sua impronta sono validi ORA e leggono il suolo atteso entro m(z)."""
        d = D.ravel()[s.fp_idx]
        buoni = (d > 0) & (np.abs(d - s.fp_z) <= s.fp_m)
        return np.bincount(s.fp_c[buoni], minlength=s.NA * NR).reshape(s.NA, NR)

    # ---- le candidate: ciascuna rende la matrice booleana «libero» (NA x NR) ----
    def tutte(s, D):
        occ, r0, omb = s.griglia(D)
        p3 = s.prep3(D)
        L = {q: s.leggi(p3, q) == LIB for q in (0.10,) + QS}
        cnt = s.impronta(D)
        porta = ~occ & ~omb
        out = {"SC": L[0.10], "RP": L[0.2], "V17": porta & L[0.2],
               "V18-1": porta & (cnt >= 1), "V18-m": porta & (cnt >= s.fp_meta)}
        # varianti prudenti (lancio 2): solo combinazioni dei pezzi sopra
        dom = s.fp_tot > 0
        out["PR1"] = out["V17"] & out["V18-m"]
        out["PR2"] = out["V18-m"] & ~vicine(occ, False)
        out["PR3"] = porta & dom & (cnt >= s.fp_tot)
        out["PR4"] = out["V18-m"] & ~vicine(dom & ~out["V18-m"], False)
        qv = np.zeros((s.NA, NR))
        vivo = out["V17"].copy()
        for q in QS:                       # quota verificata: la piu' alta con LIBERO a tutte le quote fino a lei
            vivo &= L[q]
            qv = np.where(vivo, q, qv)
        return out, qv, occ, omb


def vicine(m, bordo):
    """vero dove almeno una delle 8 celle vicine (o la cella stessa) e' vera; fuori dalla griglia vale `bordo`."""
    p = np.full((m.shape[0] + 2, m.shape[1] + 2), bordo, bool)
    p[1:-1, 1:-1] = m
    o = np.zeros(m.shape, bool)
    for da in (0, 1, 2):
        for dr in (0, 1, 2):
            o |= p[da:da + m.shape[0], dr:dr + m.shape[1]]
    return o


def settori(lib, aperti, r_da=13):
    """settori di 5 gradi: estensione del libero da 1,3 m nella direzione peggiore; solo i settori in `aperti`."""
    NA = lib.shape[0]
    sub = lib[:, r_da:]
    primo = np.where(sub.all(1), NR - r_da, (~sub).argmax(1))
    est = (r_da + primo) * DR
    centro = (NA - 5 * (NA // 5)) // 2
    return [float(est[centro + 5 * n: centro + 5 * n + 5].min()) for n in aperti]


def settori_aperti(vero, r_da=13):
    NA = vero.shape[0]
    centro = (NA - 5 * (NA // 5)) // 2
    return [n for n in range(NA // 5) if vero[centro + 5 * n: centro + 5 * n + 5, r_da:].all()]
