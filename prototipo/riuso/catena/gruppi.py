"""Gruppi connessi di celle occupate (blocco B3 del nucleo), con centro, larghezza e la marca «tagliato da un'ombra».

Un gruppo è «tagliato» quando, accanto a una sua cella (stesso anello di distanza, azimut vicino), c'è una cella in
ombra di un ALTRO gruppo più vicino alla camera: una parte dell'oggetto può essere nascosta, il centro della parte
visibile non è il centro dell'oggetto (correzione C6: non aggiorna il filtro e non entra nella regola «si muove»)."""
import math
from dataclasses import dataclass

import numpy as np

from parametri import IN_OMBRA, OCCUPATO

VICINE = [(da, dr) for da in (-1, 0, 1) for dr in (-1, 0, 1) if (da, dr) != (0, 0)]


@dataclass
class Gruppo:
    id: int                    # etichetta nel fotogramma (non è un'identità nel tempo)
    ia: np.ndarray             # indici di azimut delle celle
    ir: np.ndarray             # indici di distanza delle celle
    n_punti: int
    x: float                   # centro dei punti d'ostacolo, metri, riferimento del suolo
    z: float
    larghezza_m: float         # corda sottesa dall'estensione in azimut alla distanza del centro
    tagliato: bool = False
    al_bordo: bool = False     # f12: tocca il bordo del campo (azimut o portata)

    @property
    def distanza(self):
        return math.hypot(self.x, self.z)


def _forti(occupato, n, frazione, soglia_attesi):
    """tracciamento-1 (f12): le celle con almeno `frazione` dei punti della cella più piena della loro componente
    connessa. Un ponte di pixel misti fra due superfici piene ha pochi punti rispetto a entrambe e cade."""
    na, nr = occupato.shape
    visto = np.zeros_like(occupato)
    forti = np.zeros_like(occupato)
    for a0, r0 in zip(*np.nonzero(occupato)):
        if visto[a0, r0]:
            continue
        visto[a0, r0] = True
        pila, celle = [(int(a0), int(r0))], []
        while pila:
            a, r = pila.pop()
            celle.append((a, r))
            for da, dr in VICINE:
                b, s = a + da, r + dr
                if 0 <= b < na and 0 <= s < nr and occupato[b, s] and not visto[b, s]:
                    visto[b, s] = True
                    pila.append((b, s))
        if len(celle) == 1 and n[celle[0]] < soglia_attesi[celle[0][1]]:
            continue
        ia, ir = np.array(celle, dtype=np.int64).T
        punti = n[ia, ir]
        tiene = (punti >= frazione * punti.max()) & (punti >= soglia_attesi[ir])
        forti[ia[tiene], ir[tiene]] = True
    return forti


def trova_gruppi(ciclo, par):
    """Restituisce (gruppi, etichette): etichette è (na, nr) con l'id del gruppo di ogni cella occupata, -1 altrove."""
    occupato = ciclo.stati == OCCUPATO
    na, nr = occupato.shape
    if par.gruppi_per_picco:                          # f12: la mappa non cambia, cambiano le celle che fanno gruppo
        occupato = _forti(occupato, ciclo.n_ostacolo, par.frazione_picco, ciclo.soglia_attesi)
    etichette = np.full((na, nr), -1, dtype=np.int32)
    gruppi = []
    for a0, r0 in zip(*np.nonzero(occupato)):
        if etichette[a0, r0] >= 0:
            continue
        gid = len(gruppi)
        etichette[a0, r0] = gid
        pila, celle = [(int(a0), int(r0))], []
        while pila:                                   # riempimento a 8 vicini
            a, r = pila.pop()
            celle.append((a, r))
            for da, dr in VICINE:
                b, s = a + da, r + dr
                if 0 <= b < na and 0 <= s < nr and occupato[b, s] and etichette[b, s] < 0:
                    etichette[b, s] = gid
                    pila.append((b, s))
        ia, ir = np.array(celle, dtype=np.int64).T
        n = ciclo.n_ostacolo[ia, ir]
        tot = int(n.sum())
        x, z = float(ciclo.somma_x[ia, ir].sum() / tot), float(ciclo.somma_z[ia, ir].sum() / tot)
        ampiezza = math.radians((int(ia.max()) - int(ia.min()) + 1) * par.passo_azimut_gradi)
        larghezza = 2.0 * math.hypot(x, z) * math.sin(min(ampiezza, math.pi) / 2.0)
        gruppi.append(Gruppo(gid, ia, ir, tot, x, z, larghezza))
    if par.min_celle_gruppo > 1:                      # i gruppi troppo piccoli restano celle occupate senza gruppo
        for g in gruppi:
            if len(g.ia) < par.min_celle_gruppo:
                etichette[g.ia, g.ir] = -1
        gruppi = [g for g in gruppi if len(g.ia) >= par.min_celle_gruppo]
    if par.soglia_proporzionale or par.gruppi_per_picco:   # f12: punti del gruppo contro l'area frontale di riferimento
        piccoli = [g for g in gruppi if g.n_punti < ciclo.fxfy * par.area_rif_gruppo_m2 / max(g.distanza, 0.3) ** 2]
        for g in piccoli:
            etichette[g.ia, g.ir] = -1
        gruppi = [g for g in gruppi if not any(g is p for p in piccoli)]
    for g in gruppi:
        g.al_bordo = bool(g.ia.min() <= ciclo.ia_campo[0] + 1 or g.ia.max() >= ciclo.ia_campo[1] - 1
                          or g.ir.max() >= nr - 1)
        for da in (-1, 1):
            b = g.ia + da
            ok = (b >= 0) & (b < na)
            b, s = b[ok], g.ir[ok]
            if par.tagliato_su_componente:            # f12: le celle deboli (occupate, senza gruppo) sono ancora l'oggetto
                for _ in range(2):
                    debole = (ciclo.stati[b, s] == OCCUPATO) & (etichette[b, s] < 0)
                    b = np.clip(np.where(debole, b + da, b), 0, na - 1)
            primo = ciclo.primo[b]
            in_ombra = (ciclo.stati[b, s] == IN_OMBRA) & (primo < s)
            chi = etichette[b[in_ombra], primo[in_ombra]]         # il gruppo che fa quell'ombra
            if (chi != g.id).any():
                g.tagliato = True
    return gruppi, etichette
