"""Predittore della zona: PORTO SEMPLIFICATO in Python del predittore sd-1 di riuso/c/insieme.c (righe 162–205).

Che cosa si è portato (stessa idea, stessi numeri dove il C li ha):
  * 400 membri (NM); metà «fronte» (continuano il moto), metà «scia» (si fermano a un istante uniforme fra l'ingresso
    e l'uscita del loro percorso dall'ombra: `frz` di pred_init);
  * evidenza negativa: un membro che cade su una cella vista «libero» in QUESTO fotogramma pesa 0,1 (pred_step, cl==2);
    un membro fuori dalla griglia non conta (cl==0);
  * densità sulle celle, lisciata tre volte su 3×3 (SMOOTH = 3), regione = celle più dense fino al 90 % del peso (hdr);
  * «previsto ampio» (assorbente, come t->ampio): regione oltre 0,8 dell'area dell'ombra, oppure più di 45 cicli
    (3 s a 15 Hz), oppure nessun membro vivo. Allora la regione è TUTTA l'ombra (lo strato di possibile presenza).
Che cosa NON si è portato (dichiarato): la libreria dei percorsi del banco (build_lib/LA/LC) è sostituita da cinque
manovre generate qui (prosegue, rallenta, sosta, torna, svolta) con istante uniforme; il punto ibrido con attesa
(t->sw, t->hold) non c'è; la griglia è quella polare della catena (1° × 0,1 m), non quella cartesiana del banco.
Quindi il porto NON è provato equivalente al banco in C: quella prova (architetto-3) resta da fare.

Forma dell'aggancio: come presenza.PredittoreVelocitaCostante, costruito con (ingresso: StatoIngresso, par) e chiamato
con passo(t, ciclo, griglia) -> presenza.Previsione. In più espone `regione_celle` (maschera) e `ampio`."""
import math

import numpy as np

from . import riuso

NM = 400
DT = 1.0 / 15.0
KH = 90                    # orizzonte dei percorsi precalcolati: 6 s
VMAX = 2.5                 # m/s, come VMAX del banco e v_iniziale della catena
LIVELLO = 0.90             # livello dichiarato della regione (hdr del banco)
CICLI_AMPIO = 45           # i > 45 nel banco
FRAZIONE_AMPIO = 0.8       # area0 > 0.8 * AREA_SH nel banco
PESO_VISTO_LIBERO = 0.1
LISCIATURE = 3
MANOVRE = ("prosegue", "rallenta", "sosta", "torna", "svolta")
P_MANOVRE = (0.40, 0.15, 0.15, 0.15, 0.15)   # ipotesi: nessuna fonte, scelta qui (il banco usa una libreria)


def _liscia(d, ammesse):
    """Una lisciatura 3×3 ristretta alle celle ammesse (smooth del banco): ogni cella sparge il suo peso sulle vicine."""
    na, nr = d.shape
    p = np.zeros((na + 2, nr + 2))
    am = np.zeros((na + 2, nr + 2))
    am[1:-1, 1:-1] = ammesse
    cnt = np.zeros((na, nr))
    for da in (0, 1, 2):
        for dr in (0, 1, 2):
            cnt += am[da:da + na, dr:dr + nr]
    quota = np.where(ammesse & (cnt > 0), d / np.maximum(cnt, 1), 0.0)
    for da in (0, 1, 2):
        for dr in (0, 1, 2):
            p[da:da + na, dr:dr + nr] += quota
    return p[1:-1, 1:-1] * ammesse


class PredittoreZona:
    def __init__(self, ingresso, par, seme=0):
        self.ingresso, self.par = ingresso, par
        self.ampio, self.regione_celle, self.cicli = False, None, 0
        self._G = riuso.modulo("catena", "mappa").Griglia(par)
        x, p = np.asarray(ingresso.x, float), np.asarray(ingresso.p, float)
        rng = np.random.default_rng([int(seme), int(ingresso.id_traccia), int(round(ingresso.t * 1000))])
        cv = p[2:, 2:] + 1e-6 * np.eye(2)
        v = rng.multivariate_normal(x[2:], cv, NM)
        sp = np.hypot(v[:, 0], v[:, 1])
        v *= (np.minimum(sp, VMAX) / np.maximum(sp, 1e-9))[:, None]
        p0 = rng.multivariate_normal(x[:2], p[:2, :2] + 1e-6 * np.eye(2), NM)
        man = rng.choice(len(MANOVRE), NM, p=P_MANOVRE)
        t_man = rng.uniform(0.0, 3.0, NM)
        durata = rng.uniform(1.0, 4.0, NM)
        f_lento = rng.uniform(0.3, 0.6, NM)
        giro = np.radians(rng.uniform(45, 90, NM)) * rng.choice((-1.0, 1.0), NM)
        rumore = rng.standard_normal((NM, KH + 1, 2)) * math.sqrt(par.q * DT ** 3 / 3.0)   # piccola diffusione
        pos = np.zeros((NM, KH + 1, 2))
        pos[:, 0] = p0
        vel = v.copy()
        for i in range(1, KH + 1):
            t = i * DT
            dopo = t >= t_man
            vv = vel.copy()
            k = dopo & (man == 1)
            vv[k] *= f_lento[k, None]
            k = dopo & (man == 2) & (t < t_man + durata)
            vv[k] = 0.0
            k = dopo & (man == 3)
            vv[k] = -vel[k] * np.where(t < t_man + 0.5, 0.0, 1.0)[k, None]
            k = dopo & (man == 4)
            c, s = np.cos(giro[k]), np.sin(giro[k])
            vv[k] = np.stack([c * vel[k, 0] - s * vel[k, 1], s * vel[k, 0] + c * vel[k, 1]], 1)
            pos[:, i] = pos[:, i - 1] + vv * DT + rumore[:, i]
        # metà «scia»: si ferma a un istante uniforme fra ingresso e uscita del percorso dall'ombra d'ingresso
        nucleo = ingresso.nucleo
        self._frz = np.full(NM, KH)
        for j in range(NM // 2, NM):
            dentro = self._nel(nucleo, pos[j, :, 0], pos[j, :, 1])
            idx = np.nonzero(dentro)[0]
            if len(idx):
                ien, iex = idx[0], idx[-1]
            else:
                ien, iex = 0, KH
            u = math.fmod((j - NM / 2 + 0.5) * 0.6180339887, 1.0)
            self._frz[j] = int(ien + u * (iex - ien))
        self._pos, self.w = pos, np.ones(NM)
        self._area_ombra = float(self._G.area[nucleo].sum())

    def _celle(self, x, z):
        g = self.par
        ia = np.floor((np.degrees(np.arctan2(x, z)) + g.azimut_max_gradi) / g.passo_azimut_gradi).astype(int)
        ir = np.floor(np.hypot(x, z) / g.passo_distanza_m).astype(int)
        ok = (ia >= 0) & (ia < g.n_azimut) & (ir >= 0) & (ir < g.n_distanza) & (z > 0)
        return np.where(ok, ia, 0), np.where(ok, ir, 0), ok

    def _nel(self, maschera, x, z):
        ia, ir, ok = self._celle(x, z)
        return ok & maschera[ia, ir]

    def passo(self, t, ciclo, griglia):
        P = riuso.modulo("catena", "presenza")
        L = riuso.modulo("catena", "parametri")
        tau = max(0.0, t - self.ingresso.t)
        i = min(KH, int(round(tau / DT)))
        self.cicli = i
        ii = np.full(NM, i)
        ii[NM // 2:] = np.minimum(i, self._frz[NM // 2:])
        xy = self._pos[np.arange(NM), ii]
        ia, ir, ok = self._celle(xy[:, 0], xy[:, 1])
        visto_libero = (ciclo.stati == L.LIBERO) & (ciclo.eta == 0)
        colpiti = ok & visto_libero[ia, ir]
        self.w[colpiti] *= PESO_VISTO_LIBERO
        vivi = ok & ~colpiti
        d = np.zeros(visto_libero.shape)
        np.add.at(d, (ia[vivi], ir[vivi]), self.w[vivi])
        ammesse = ~visto_libero
        for _ in range(LISCIATURE):
            d = _liscia(d, ammesse)
        tot = d.sum()
        reg = np.zeros(d.shape, dtype=bool)
        if tot > 0:
            ordine = np.argsort(d.ravel())[::-1]
            cum = np.cumsum(d.ravel()[ordine])
            n = int(np.searchsorted(cum, LIVELLO * tot) + 1)
            reg.ravel()[ordine[:n]] = True
        area = float(griglia.area[reg].sum())
        if tot <= 0 or area > FRAZIONE_AMPIO * self._area_ombra or i > CICLI_AMPIO:
            self.ampio = True
        self.regione_celle = None if self.ampio else reg
        sw = self.w[vivi].sum()
        if sw > 0:
            m = (self.w[vivi, None] * xy[vivi]).sum(0) / sw
            c = np.cov(xy[vivi].T, aweights=self.w[vivi]) if vivi.sum() > 2 else np.eye(2) * 0.01
        else:
            m, c = np.asarray(self.ingresso.x[:2]), np.eye(2) * 1.0
        return P.Previsione(float(m[0]), float(m[1]), np.asarray(c) + 1e-6 * np.eye(2))
