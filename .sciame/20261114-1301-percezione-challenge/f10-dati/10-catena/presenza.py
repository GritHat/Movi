"""Lo strato di «possibile presenza» e il punto d'innesto del predittore (blocco B5 del nucleo).

Strato 1 (garanzia): il cuneo d'ombra dell'ostacolo dietro cui la traccia è sparita (il «nucleo» dello strato),
dilatato di una fascia di guardia. Non ha tetto di tempo. Una cella del nucleo si rilascia solo quando è vista
«libero» per `rilascio_fotogrammi` fotogrammi di fila; la fascia segue il nucleo che resta.
Strato 2 (informazione): la previsione di un predittore, mostrata finché il suo cerchio al 95 % copre meno di metà
dell'area del nucleo."""
import math
from dataclasses import dataclass

import numpy as np

from kalman import rumore_processo, transizione
from parametri import CHI2_95, IN_OMBRA, LIBERO, NON_OSSERVATO


@dataclass
class StatoIngresso:
    """Ciò che un predittore riceve quando una traccia entra in ombra."""
    id_traccia: int
    t: float                   # istante del primo ciclo senza misura
    x: np.ndarray              # stato del filtro [x, z, vx, vz] portato a t
    p: np.ndarray              # covarianza 4×4 a t
    ultima_misura: tuple       # (x, z, t) dell'ultima misura, anche se tagliata
    larghezza_m: float
    nucleo: np.ndarray         # (na, nr) celle del cuneo d'ombra dell'ostacolo d'ingresso


@dataclass
class Previsione:
    """Ciò che un predittore restituisce a ogni ciclo: la posizione più probabile e la regione (covarianza 2×2)."""
    x: float
    z: float
    p: np.ndarray

    @property
    def raggio95(self):
        """Cerchio al 95 % come in sim_v2: dalla varianza maggiore fra i due assi."""
        return math.sqrt(CHI2_95 * max(self.p[0, 0], self.p[1, 1]))


class PredittoreVelocitaCostante:
    """Linea di base: il filtro del nucleo lasciato correre dallo stato d'ingresso (forma chiusa in tau).

    Un predittore diverso (due ipotesi, particelle, evidenza negativa…) ha la stessa forma: si costruisce con
    (ingresso, parametri) e a ogni ciclo riceve (t, mappa del ciclo, griglia) e restituisce una `Previsione`."""

    def __init__(self, ingresso, par):
        self.ingresso, self.q = ingresso, par.q

    def passo(self, t, ciclo, griglia):
        tau = t - self.ingresso.t
        f = transizione(tau)
        x = f @ self.ingresso.x
        p = f @ self.ingresso.p @ f.T + rumore_processo(tau, self.q)
        return Previsione(float(x[0]), float(x[1]), p[:2, :2])


class Strato:
    """La possibile presenza lasciata da una traccia entrata in ombra."""

    def __init__(self, ingresso, griglia, par):
        self.id_traccia, self.t_ingresso = ingresso.id_traccia, ingresso.t
        self.griglia, self.par = griglia, par
        self.nucleo = ingresso.nucleo.copy()
        self.maschera = griglia.dilata(self.nucleo, par.fascia_m)
        self.liberi_di_fila = np.zeros(self.nucleo.shape, dtype=np.int16)
        self.celle_rilasciate = 0
        self.fine = None                      # motivo della fine: «riaggancio» o «celle_libere» (invariante 7)

    def aggiorna(self, ciclo):
        """Rilascio cella per cella. Lettura prudente: conta solo il suolo visto in QUESTO fotogramma, non la
        memoria. Restituisce True se il nucleo è finito."""
        fresco = (ciclo.stati == LIBERO) & (ciclo.eta == 0)
        self.liberi_di_fila = np.where(fresco, self.liberi_di_fila + 1, 0).astype(np.int16)
        rilascia = self.nucleo & (self.liberi_di_fila >= self.par.rilascio_fotogrammi)
        if rilascia.any():
            self.nucleo &= ~rilascia
            self.celle_rilasciate += int(rilascia.sum())
            self.maschera = self.griglia.dilata(self.nucleo, self.par.fascia_m)
        return not self.nucleo.any()

    def area_nucleo(self):
        return float(self.griglia.area[self.nucleo].sum())

    def area_coperta(self, previsione):
        """Area del nucleo dentro il cerchio al 95 % della previsione («ritagliato sul cuneo»)."""
        dentro = self.nucleo & self.griglia.entro(previsione.x, previsione.z, previsione.raggio95)
        return float(self.griglia.area[dentro].sum())


def _gruppo_del_primo_ritorno(ciclo, etichette):
    """Per ogni azimut, l'id del gruppo che dà il primo ritorno (-1: cella senza gruppo; -2: nessun ritorno)."""
    na, nr = etichette.shape
    primo = np.minimum(ciclo.primo, nr - 1)
    return np.where(ciclo.primo < nr, etichette[np.arange(na), primo], -2)


def cuneo_d_ingresso(ciclo, gruppi, etichette, griglia, x, z, par):
    """Il cuneo d'ombra in cui è entrata una traccia la cui ultima misura è (x, z), oppure None.

    «A meno di 0,40 m da un'ombra» (B5), con la precisazione chiesta dal verdetto (K-018): non conta l'ombra
    propria, cioè quella di un gruppo che contiene il punto dell'ultima misura. Il cuneo è fatto di tutte le
    celle in ombra degli azimut il cui primo ritorno è dell'ostacolo (o degli ostacoli) trovato."""
    ombra = ciclo.stati == IN_OMBRA
    vicine = ombra & griglia.entro(x, z, par.fascia_m)
    if not vicine.any():
        return None
    cella = griglia.cella(x, z)
    propri = set()
    if cella is not None:
        for g in gruppi:
            if g.ia.min() - 1 <= cella[0] <= g.ia.max() + 1 and g.ir.min() - 1 <= cella[1] <= g.ir.max() + 1:
                propri.add(g.id)
    chi = _gruppo_del_primo_ritorno(ciclo, etichette)
    ostacoli = set(int(c) for c in chi[np.unique(np.nonzero(vicine)[0])]) - propri - {-2}
    if not ostacoli:
        return None
    return ombra & np.isin(chi, sorted(ostacoli))[:, None]


def riaggancio_ammesso(gruppo, strato, ciclo, etichette, griglia, par):
    """Il rilevamento può riprendere l'identità della traccia pendente? Restituisce (sì/no, motivo).

    Regola C1 del nucleo: entro la fascia dell'ombra d'ingresso e a più della fascia da ogni ALTRO bordo del non
    osservato. Lettura: «altro bordo» = una cella non osservata o in ombra che non sta nello strato (nucleo più
    fascia) e non è l'ombra del rilevamento stesso; in più, il bordo della portata. Il motivo è None quando il
    rilevamento non c'entra con questo strato (lontano dall'ombra d'ingresso)."""
    vicino = griglia.entro(gruppo.x, gruppo.z, par.fascia_m)
    if not (vicino & strato.nucleo).any():
        return False, None
    if par.portata_m - gruppo.distanza <= par.fascia_m:
        return False, "a meno della fascia dal bordo della portata"
    chi = _gruppo_del_primo_ritorno(ciclo, etichette)
    oltre = np.arange(etichette.shape[1])[None, :] > ciclo.primo[:, None]
    ombra_propria = (chi == gruppo.id)[:, None] & oltre
    altro = ((ciclo.stati == NON_OSSERVATO) | (ciclo.stati == IN_OMBRA)) & ~ciclo.ambigua \
        & ~strato.maschera & ~ombra_propria
    if int((altro & vicino).sum()) >= par.min_celle_altro_bordo:
        return False, "a meno della fascia da un altro bordo del non osservato"
    return True, ""
