"""Filtro di Kalman a velocità quasi costante e assegnazione ungherese (blocco B4 del nucleo). Solo matematica.

Stato [x, z, vx, vz] nel riferimento del suolo (x a destra, z in avanti: il nucleo li chiama x e y). Il rumore di
processo è un'accelerazione bianca di densità q (m²/s³): per asse Q = q·[[dt³/3, dt²/2], [dt²/2, dt]]."""
import math

import numpy as np

H = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]])


def transizione(dt):
    f = np.eye(4)
    f[0, 2] = f[1, 3] = dt
    return f


def rumore_processo(dt, q):
    m = np.zeros((4, 4))
    m[0, 0] = m[1, 1] = q * dt ** 3 / 3.0
    m[0, 2] = m[2, 0] = m[1, 3] = m[3, 1] = q * dt ** 2 / 2.0
    m[2, 2] = m[3, 3] = q * dt
    return m


def rumore_misura(x, z, sigma_radiale, sigma_tangenziale):
    """R(z) per asse: radiale e tangenziale rispetto alla camera, ruotata in (x, z)."""
    d = math.hypot(x, z) or 1.0
    ur = np.array([x / d, z / d])
    ut = np.array([z / d, -x / d])
    return sigma_radiale ** 2 * np.outer(ur, ur) + sigma_tangenziale ** 2 * np.outer(ut, ut)


class Kalman:
    def __init__(self, x, z, r, sigma_velocita):
        self.x = np.array([x, z, 0.0, 0.0])
        self.p = np.zeros((4, 4))
        self.p[:2, :2] = r
        self.p[2, 2] = self.p[3, 3] = sigma_velocita ** 2

    def predici(self, dt, q):
        f = transizione(dt)
        self.x = f @ self.x
        self.p = f @ self.p @ f.T + rumore_processo(dt, q)

    def innovazione(self, m, r):
        """Scarto, sua covarianza e distanza di Mahalanobis al quadrato della misura m = (x, z)."""
        y = np.asarray(m, dtype=np.float64) - self.x[:2]
        s = self.p[:2, :2] + r
        return y, s, float(y @ np.linalg.solve(s, y))

    def aggiorna(self, m, r):
        y, s, _ = self.innovazione(m, r)
        k = self.p @ H.T @ np.linalg.inv(s)
        self.x = self.x + k @ y
        ikh = np.eye(4) - k @ H
        self.p = ikh @ self.p @ ikh.T + k @ r @ k.T              # forma di Joseph: resta simmetrica e positiva

    def riparti(self, x, z, r, sigma_velocita):
        """Riparte dalla misura a velocità nulla (come sim_v2 quando la misura cade fuori dalla porta)."""
        self.__init__(x, z, r, sigma_velocita)

    def chi2_velocita(self):
        """Statistica dell'ipotesi «fermo»: v' Pvv^-1 v (il nucleo la registra accanto alla regola dello spostamento)."""
        v = self.x[2:]
        return float(v @ np.linalg.solve(self.p[2:, 2:], v))


def ungherese(costo):
    """Assegnazione di costo minimo. `costo` è (n, m); restituisce la lista di coppie (riga, colonna), una per
    ogni riga se n <= m, una per ogni colonna altrimenti. Algoritmo ungherese con i potenziali, O(n²·m)."""
    costo = np.asarray(costo, dtype=np.float64)
    if costo.size == 0:
        return []
    if costo.shape[0] > costo.shape[1]:
        return sorted((r, c) for c, r in ungherese(costo.T))
    n, m = costo.shape
    u, v = [0.0] * (n + 1), [0.0] * (m + 1)
    riga_di = [0] * (m + 1)                 # riga_di[j] = riga (da 1) assegnata alla colonna j; 0 = nessuna
    via = [0] * (m + 1)
    for i in range(1, n + 1):
        riga_di[0] = i
        j0 = 0
        minimo = [math.inf] * (m + 1)
        usata = [False] * (m + 1)
        while True:
            usata[j0] = True
            i0, delta, j1 = riga_di[j0], math.inf, 0
            for j in range(1, m + 1):
                if not usata[j]:
                    cur = costo[i0 - 1, j - 1] - u[i0] - v[j]
                    if cur < minimo[j]:
                        minimo[j], via[j] = cur, j0
                    if minimo[j] < delta:
                        delta, j1 = minimo[j], j
            for j in range(m + 1):
                if usata[j]:
                    u[riga_di[j]] += delta
                    v[j] -= delta
                else:
                    minimo[j] -= delta
            j0 = j1
            if riga_di[j0] == 0:
                break
        while j0:
            j1 = via[j0]
            riga_di[j0] = riga_di[j1]
            j0 = j1
    return sorted((riga_di[j] - 1, j - 1) for j in range(1, m + 1) if riga_di[j])
