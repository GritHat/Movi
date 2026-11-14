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

    @property
    def distanza(self):
        return math.hypot(self.x, self.z)


def trova_gruppi(ciclo, par):
    """Restituisce (gruppi, etichette): etichette è (na, nr) con l'id del gruppo di ogni cella occupata, -1 altrove."""
    occupato = ciclo.stati == OCCUPATO
    na, nr = occupato.shape
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
    for g in gruppi:
        for da in (-1, 1):
            b = g.ia + da
            ok = (b >= 0) & (b < na)
            b, s = b[ok], g.ir[ok]
            primo = ciclo.primo[b]
            in_ombra = (ciclo.stati[b, s] == IN_OMBRA) & (primo < s)
            chi = etichette[b[in_ombra], primo[in_ombra]]         # il gruppo che fa quell'ombra
            if (chi != g.id).any():
                g.tagliato = True
    return gruppi, etichette
