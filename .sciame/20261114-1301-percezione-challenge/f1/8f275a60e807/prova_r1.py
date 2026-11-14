"""Prova di classe 2 per rovesciatore-1: velocita' apparente di un punto FERMO a 3 m
con sensore indossato (rotazione compensata con errore di sincronizzazione dt) contro sensore fisso.
Python puro, seme fisso. Uso: python3 prova_r1.py
"""
import math
import random

FS = 15.0          # Hz
T = 1.0 / FS
R_M = 0.03         # rumore di misura per asse, m
RANGE = 3.0        # distanza del punto fermo, m
DUR = 120.0        # s simulati per configurazione
WARM = 2.0         # s scartati
SOGLIA = 0.3       # m/s, soglia "mobile"


def theta(t):
    # scansione +-20 gradi a 0,5 Hz + oscillazione del passo +-3 gradi a 2 Hz
    return math.radians(20) * math.sin(2 * math.pi * 0.5 * t) + \
        math.radians(3) * math.sin(2 * math.pi * 2.0 * t + 0.7)


class KF1:
    """Kalman a velocita' costante su un asse; q = densita' spettrale dell'accelerazione bianca."""

    def __init__(self, q, r):
        self.q, self.r = q, r
        self.x = None

    def step(self, z):
        if self.x is None:
            self.x = [z, 0.0]
            self.P = [[self.r, 0.0], [0.0, 1.0]]
            return
        q, x, P = self.q, self.x, self.P
        xp = [x[0] + T * x[1], x[1]]
        p00 = P[0][0] + T * (P[1][0] + P[0][1]) + T * T * P[1][1] + q * T ** 3 / 3
        p01 = P[0][1] + T * P[1][1] + q * T ** 2 / 2
        p11 = P[1][1] + q * T
        s = p00 + self.r
        k0, k1 = p00 / s, p01 / s
        y = z - xp[0]
        self.x = [xp[0] + k0 * y, xp[1] + k1 * y]
        self.P = [[(1 - k0) * p00, (1 - k0) * p01], [p01 - k1 * p00, p11 - k1 * p01]]


def run(modo, dt_sync, sigma_a, seed=1):
    rnd = random.Random(seed)
    q = sigma_a ** 2
    kx, ky = KF1(q, R_M ** 2), KF1(q, R_M ** 2)
    n = int(DUR * FS)
    s2, falsi, cnt = 0.0, 0, 0
    for i in range(n):
        t = i * T
        if modo == "fisso":
            a = 0.0
        elif modo == "nessuna":
            a = -theta(t)
        else:  # compensata con errore di sincronizzazione
            a = theta(t + dt_sync) - theta(t)
        # punto del mondo (0, RANGE) ruotato dell'angolo residuo a
        px = -math.sin(a) * RANGE + rnd.gauss(0, R_M)
        py = math.cos(a) * RANGE + rnd.gauss(0, R_M)
        kx.step(px)
        ky.step(py)
        if t >= WARM:
            v = math.hypot(kx.x[1], ky.x[1])
            s2 += v * v
            falsi += v > SOGLIA
            cnt += 1
    return math.sqrt(s2 / cnt), falsi / cnt


if __name__ == "__main__":
    print("punto fermo a %.1f m, %g Hz, rumore %.0f cm, soglia mobile %.1f m/s" % (RANGE, FS, R_M * 100, SOGLIA))
    print("%-22s %-8s %-10s %-10s" % ("configurazione", "sigma_a", "RMS m/s", "falso mob."))
    for sigma_a in (1.0, 0.5, 2.0):
        for nome, modo, d in (("fisso", "fisso", 0), ("indossato dt=0ms", "comp", 0.0),
                              ("indossato dt=5ms", "comp", 0.005), ("indossato dt=10ms", "comp", 0.010),
                              ("indossato dt=30ms", "comp", 0.030), ("indossato senza comp.", "nessuna", 0)):
            rms, f = run(modo, d, sigma_a)
            print("%-22s %-8.1f %-10.3f %-10.1f%%" % (nome, sigma_a, rms, 100 * f))
        print()
    # controllo analitico indipendente dal filtro: v = r * alpha * dt
    a1 = math.radians(20) * (2 * math.pi * 0.5) ** 2
    a2 = math.radians(3) * (2 * math.pi * 2.0) ** 2
    arms = math.sqrt((a1 ** 2 + a2 ** 2) / 2)
    for d in (0.005, 0.010, 0.030):
        print("analitico (senza filtro): dt=%2.0f ms -> v_app RMS = r*alpha_rms*dt = %.3f m/s" % (d * 1000, RANGE * arms * d))
