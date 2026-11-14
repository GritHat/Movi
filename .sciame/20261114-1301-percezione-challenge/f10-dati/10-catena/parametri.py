"""Parametri della catena di riferimento. I valori predefiniti sono quelli del nucleo (SOLUZIONE_V2.md);
dove il nucleo non dà un numero il commento dice «lettura» e CATENA.md lo elenca."""
import math
from dataclasses import dataclass

# Stati di una cella (B2 del nucleo): interi piccoli, così la mappa è una matrice uint8.
NON_OSSERVATO, LIBERO, OCCUPATO, IN_OMBRA = 0, 1, 2, 3
NOMI_STATI = {NON_OSSERVATO: "non_osservato", LIBERO: "libero", OCCUPATO: "occupato", IN_OMBRA: "in_ombra"}

CHI2_99, CHI2_95 = 9.2103, 5.9915        # quantili del chi quadrato a 2 gradi di libertà

# Curve del rumore radiale del centro (B1 del nucleo; formule di f4/H-012/03-validazione/sim_v2.py, sig_r).
CURVE_RUMORE = {
    "nominale": lambda z: z * z * 0.08 / (424.0 * 0.05),      # 1,5 / 3,4 / 6,0 cm a 2 / 3 / 4 m
    "pessimista": lambda z: 0.04 * (z / 2.0) ** 2,            # 4 / 9 / 16 cm
    "torneo": lambda z: 0.05 * (z / 2.0) ** 2,                # 5 / 11 / 20 cm
}


@dataclass
class Parametri:
    # --- mappa (B2)
    passo_azimut_gradi: float = 1.0
    passo_distanza_m: float = 0.1
    azimut_max_gradi: float = 90.0          # la griglia va da -azimut_max a +azimut_max
    portata_m: float = 3.0
    quota_min_ostacolo_m: float = 0.07
    quota_max_ostacolo_m: float = 2.0
    tolleranza_suolo_m: float = 0.05        # lettura: «alla quota attesa» = entro 5 cm (meno di 0,07)
    min_punti_suolo: int = 3                # lettura: punti di suolo per dire «visto» in una cella
    min_punti_ostacolo: int = 3             # lettura: punti fra 0,07 e 2 m per dire «occupato»
    memoria_fotogrammi: int = 3             # «libero» se il suolo è visto in uno degli ultimi 3 fotogrammi
    libero_dietro_ostacolo: bool = False    # lettura prudente: oltre il primo ritorno è tutto «in ombra»
    # --- gruppi (B3)
    min_celle_gruppo: int = 1
    # --- inseguimento (B3, B4)
    q: float = 0.2                          # m^2/s^3
    curva_rumore: str = "nominale"
    sigma_min_m: float = 0.0                # pavimento facoltativo del rumore del centro (0 = solo la curva)
    v_iniziale_m_s: float = 2.5             # scarto tipo della velocità alla nascita (v_max del nucleo)
    conferma_m: int = 3
    conferma_n: int = 5
    finestra_moto_s: float = 1.0
    media_moto_fotogrammi: int = 3
    soglia_moto_sigma: float = 5.0          # spostamento > 5 * sigma(z) * sqrt(2) lungo un asse
    fattore_media_moto: float = 1.0         # lettura: 1 = testo del nucleo; 0,577 = sim_v2 (sigma della media di 3)
    larghezza_min_m: float = 0.3            # larghezza creduta di una traccia mai vista intera
    # --- stati e possibile presenza (B5)
    fascia_m: float = 0.40
    non_confermato_fotogrammi: int = 3
    rilascio_fotogrammi: int = 3
    frazione_perso: float = 0.5             # «previsto» finché il cerchio al 95 % copre meno di metà del cuneo
    pendenti_ambito: str = "globale"        # lettura: «una sola traccia pendente» in tutta la scena («ombra»: nella fascia)
    min_celle_altro_bordo: int = 1          # lettura: basta una cella non osservata entro la fascia per rifiutare
    # --- uscita
    settore_gradi: float = 10.0
    verifica_invarianti: bool = True

    @property
    def n_azimut(self):
        return int(round(2 * self.azimut_max_gradi / self.passo_azimut_gradi))

    @property
    def n_distanza(self):
        return int(round(self.portata_m / self.passo_distanza_m))

    def sigma_radiale(self, z):
        return max(self.sigma_min_m, CURVE_RUMORE[self.curva_rumore](z))

    def sigma_tangenziale(self, z):
        """Una cella larga un grado, distribuzione uniforme (come sig_t di sim_v2)."""
        return max(self.sigma_min_m, z * math.radians(self.passo_azimut_gradi) / math.sqrt(12.0))
