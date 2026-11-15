"""Nucleo MoVi in Python puro, per girare dentro Unreal Engine (nessuna dipendenza).
È un porto compatto delle regole del prototipo (prototipo/movi): filtro di Kalman a velocità costante per asse,
regione al 90 % che cresce quando il bersaglio non è visto, confidenza C(tau) = 1 - exp(-r^2 / 2 sigma^2(tau)),
tre stati (visto / non visto: regione / non so), avviso immediato quando i sensori sono accecati insieme.
Solo osservazione e avviso."""
import math

K90 = 2.146  # raggio della regione al 90 % in unità di sigma (piano)


class Asse:
    """Kalman a velocità costante su un asse: stato [p, v], covarianza 2x2."""

    def __init__(self, p, v, sp=30.0, sv=60.0, q=1.5e4, r=20.0 ** 2):
        self.p, self.v = p, v
        self.a, self.b, self.c = sp * sp, 0.0, sv * sv   # P = [[a, b], [b, c]]
        self.q, self.r = q, r

    def prevedi(self, dt):
        self.p += self.v * dt
        a, b, c, q = self.a, self.b, self.c, self.q
        self.a = a + 2 * b * dt + c * dt * dt + q * dt ** 3 / 3
        self.b = b + c * dt + q * dt * dt / 2
        self.c = c + q * dt

    def aggiorna(self, z):
        s = self.a + self.r
        k0, k1 = self.a / s, self.b / s
        e = z - self.p
        self.p += k0 * e
        self.v += k1 * e
        a, b, c = self.a, self.b, self.c
        self.a, self.b, self.c = (1 - k0) * a, (1 - k0) * b, c - k1 * b


class Traccia:
    def __init__(self, pos, vel):
        self.assi = [Asse(p, v) for p, v in zip(pos, vel)]
        self.non_visto_da = 0.0
        self.stato = "visto"

    def passo(self, dt, misura):
        for a in self.assi:
            a.prevedi(dt)
        if misura is None:
            self.non_visto_da += dt
            self.stato = "non visto: regione"
        else:
            for a, z in zip(self.assi, misura):
                a.aggiorna(z)
            self.non_visto_da = 0.0
            self.stato = "visto"

    @property
    def pos(self):
        return [a.p for a in self.assi]

    @property
    def sigma(self):
        return math.sqrt(max(a.a for a in self.assi))

    @property
    def raggio90(self):
        return K90 * self.sigma

    def confidenza(self, r_porta):
        """C = 1 - exp(-r^2 / 2 sigma^2): probabilità che il bersaglio sia entro r_porta dal punto previsto."""
        return 1.0 - math.exp(-r_porta * r_porta / (2.0 * self.sigma ** 2))


class MoVi:
    def __init__(self, pos, vel, r_porta=150.0):
        self.traccia = Traccia(pos, vel)
        self.r_porta = r_porta
        self.avviso = False
        self.t_avviso = None
        self.evento = False

    def passo(self, t, dt, misura, radar_ok, camera_ok):
        """misura: posizione misurata del bersaglio, o None se nessun sensore lo vede in questo ciclo."""
        self.traccia.passo(dt, misura)
        if not radar_ok and not camera_ok and not self.avviso:
            self.avviso, self.t_avviso, self.evento = True, t, True   # avviso immediato: evento vicino, posizione ignota
        return {
            "stato": self.traccia.stato,
            "pos": self.traccia.pos,
            "raggio": self.traccia.raggio90,
            "confidenza": self.traccia.confidenza(self.r_porta),
            "non_visto_da": self.traccia.non_visto_da,
            "avviso": self.avviso,
            "radar": "ok" if radar_ok else "accecato",
            "camera": "ok" if camera_ok else "accecata",
        }
