"""Mappa polare sul piano del suolo a quattro stati (blocco B2 del nucleo).

Per ogni fotogramma i pixel validi diventano punti; in ogni cella (azimut, distanza) si contano i punti di suolo
(quota entro la tolleranza) e i punti d'ostacolo (quota fra 0,07 e 2 m). Poi, in quest'ordine:
  occupato       almeno `min_punti_ostacolo` punti d'ostacolo nel fotogramma;
  in ombra       oltre il primo ritorno del proprio azimut (lettura prudente: anche se lì il suolo si rivede);
  libero         «vista libera» (suolo visto e nessun punto d'ostacolo, né occupata né in ombra) in almeno uno degli
                 ultimi `memoria_fotogrammi` fotogrammi, e in questo fotogramma né occupata, né in ombra, né con
                 punti d'ostacolo. La memoria copre quindi solo i buchi, e ricorda solo ciò che era libero: una
                 cella che nell'ultimo dato valido aveva un ostacolo non diventa «libero» perché il dato manca;
  non osservato  tutto il resto: fuori campo, anello vicino senza suolo, buchi, celle con punti d'ostacolo sotto soglia.
Un pixel a 0 non produce punti: non può rendere «libero» niente."""
import math
from collections import deque
from dataclasses import dataclass

import numpy as np

from parametri import IN_OMBRA, LIBERO, NON_OSSERVATO, OCCUPATO

ETA_MAI = 32767          # età (in fotogrammi) di una cella mai vista libera


class InvarianteViolato(AssertionError):
    """Un invariante del nucleo non vale: è un difetto della catena, non un dato."""


class Griglia:
    """Geometria delle celle: centri in coordinate polari e cartesiane, area, e la cella di un punto."""

    def __init__(self, par):
        self.par, self.na, self.nr = par, par.n_azimut, par.n_distanza
        self.azimut = -par.azimut_max_gradi + (np.arange(self.na) + 0.5) * par.passo_azimut_gradi      # gradi
        self.distanza = (np.arange(self.nr) + 0.5) * par.passo_distanza_m
        a = np.radians(self.azimut)[:, None]
        self.x = (np.sin(a) * self.distanza[None, :]).astype(np.float32)
        self.z = (np.cos(a) * self.distanza[None, :]).astype(np.float32)
        self.area = np.repeat((self.distanza * par.passo_distanza_m * math.radians(par.passo_azimut_gradi))[None, :],
                              self.na, axis=0)

    def cella(self, x, z):
        """Indici (azimut, distanza) della cella che contiene il punto, o None se è fuori dalla griglia."""
        ia = math.floor((math.degrees(math.atan2(x, z)) + self.par.azimut_max_gradi) / self.par.passo_azimut_gradi)
        ir = math.floor(math.hypot(x, z) / self.par.passo_distanza_m)
        return (ia, ir) if 0 <= ia < self.na and 0 <= ir < self.nr else None

    def entro(self, x, z, raggio):
        """Maschera delle celle il cui centro dista al più `raggio` dal punto."""
        return np.hypot(self.x - x, self.z - z) <= raggio

    def dilata(self, maschera, raggio):
        """Celle il cui centro dista al più `raggio` dal centro di una cella della maschera."""
        ia, ir = np.nonzero(maschera)
        if len(ia) == 0:
            return np.zeros_like(maschera)
        px, pz = self.x[ia, ir], self.z[ia, ir]
        fuori = np.zeros(maschera.shape, dtype=bool)
        for k in range(0, len(px), 256):           # a blocchi, per non allocare (celle × nucleo) in un colpo
            d2 = (self.x[..., None] - px[k:k + 256]) ** 2 + (self.z[..., None] - pz[k:k + 256]) ** 2
            fuori |= (d2 <= raggio * raggio).any(axis=-1)
        return fuori


@dataclass
class CicloMappa:
    """Ciò che la mappa sa di un fotogramma."""
    t: float
    stati: np.ndarray          # (na, nr) uint8
    eta: np.ndarray            # fotogrammi dall'ultima volta che la cella è stata vista libera (0 = ora)
    suolo_ora: np.ndarray      # suolo visto in questo fotogramma
    ambigua: np.ndarray        # suolo visto ora ma con punti d'ostacolo sotto soglia: esce «non osservato»
    n_ostacolo: np.ndarray     # punti d'ostacolo per cella
    somma_x: np.ndarray        # somma delle x dei punti d'ostacolo (per il centro dei gruppi)
    somma_z: np.ndarray
    primo: np.ndarray          # (na,) indice di distanza del primo ritorno; nr se non c'è
    pixel_validi: int
    suolo_visto_in_ombra: int  # diagnostico: celle «in ombra» in cui il suolo si vede (lettura prudente)

    def conteggi(self):
        return np.bincount(self.stati.ravel(), minlength=4)


class Mappa:
    def __init__(self, par, proiezione):
        self.par, self.pr, self.griglia = par, proiezione, Griglia(par)
        forma = (par.n_azimut, par.n_distanza)
        self.eta = np.full(forma, ETA_MAI, dtype=np.int16)
        self._ultimi = deque(maxlen=par.memoria_fotogrammi)      # per l'invariante 1, a parte dal contatore d'età
        self._indici_r = np.arange(par.n_distanza)[None, :]

    def aggiorna(self, prof, t):
        par, pr = self.par, self.pr
        na, nr = par.n_azimut, par.n_distanza
        z = prof.ravel().astype(np.float32) * np.float32(0.001)
        ir = (z * pr.ar * np.float32(1.0 / par.passo_distanza_m)).astype(np.int32)
        quota = pr.h - z * pr.aq
        dentro = (z > 0) & pr.in_azimut & (ir < nr)
        suolo = dentro & (np.abs(quota) <= par.tolleranza_suolo_m)
        ostacolo = dentro & (quota >= par.quota_min_ostacolo_m) & (quota <= par.quota_max_ostacolo_m)
        cella = pr.ia * nr + ir
        n_suolo = np.bincount(cella[suolo], minlength=na * nr).reshape(na, nr)
        c_ost, z_ost = cella[ostacolo], z[ostacolo]
        n_ost = np.bincount(c_ost, minlength=na * nr).reshape(na, nr)
        somma_x = np.bincount(c_ost, weights=z_ost * pr.ax[ostacolo], minlength=na * nr).reshape(na, nr)
        somma_z = np.bincount(c_ost, weights=z_ost * pr.az[ostacolo], minlength=na * nr).reshape(na, nr)

        suolo_ora = n_suolo >= par.min_punti_suolo
        occupato = n_ost >= par.min_punti_ostacolo
        primo = np.where(occupato.any(axis=1), occupato.argmax(axis=1), nr)
        oltre = self._indici_r > primo[:, None]
        pulita = n_ost == 0
        ombra = oltre & ~occupato
        visto_in_ombra = int((ombra & suolo_ora & pulita).sum())
        if par.libero_dietro_ostacolo:
            ombra &= ~(suolo_ora & pulita)
        ammessa = pulita & ~occupato & ~ombra            # niente, in questo fotogramma, vieta «libero»
        vista_libera = suolo_ora & ammessa
        self.eta = np.where(vista_libera, 0, np.minimum(self.eta, ETA_MAI - 1) + 1).astype(np.int16)
        libero = (self.eta < par.memoria_fotogrammi) & ammessa
        stati = np.full((na, nr), NON_OSSERVATO, dtype=np.uint8)
        stati[libero] = LIBERO
        stati[ombra] = IN_OMBRA
        stati[occupato] = OCCUPATO
        self._ultimi.append(vista_libera)
        ciclo = CicloMappa(t, stati, self.eta, suolo_ora, suolo_ora & ~pulita & ~occupato & ~ombra,
                           n_ost, somma_x, somma_z, primo, int(np.count_nonzero(prof)), visto_in_ombra)
        if par.verifica_invarianti:
            self.verifica(ciclo, int(n_suolo.sum() + n_ost.sum()))
        return ciclo

    def verifica(self, ciclo, punti_usati):
        """Invarianti 1 e 2 del nucleo, ricontrollati con dati diversi da quelli che hanno deciso lo stato."""
        libero = ciclo.stati == LIBERO
        visto = np.zeros_like(libero)
        for m in self._ultimi:                     # le maschere degli ultimi fotogrammi, non il contatore d'età
            visto |= m                             # «vista libera» implica «suolo visto»
        if (libero & ~visto).any():
            raise InvarianteViolato("invariante 1: «libero» su una cella senza suolo visto libero negli ultimi "
                                    f"{self.par.memoria_fotogrammi} fotogrammi")
        if (libero & (ciclo.n_ostacolo > 0)).any():
            raise InvarianteViolato("invariante 2: «libero» su una cella con punti d'ostacolo")
        if not self.par.libero_dietro_ostacolo and (libero & (self._indici_r > ciclo.primo[:, None])).any():
            raise InvarianteViolato("invariante 2: «libero» oltre il primo ritorno (in ombra)")
        if punti_usati > ciclo.pixel_validi:
            raise InvarianteViolato("più punti usati che pixel validi: un pixel senza dato è entrato nella mappa")
