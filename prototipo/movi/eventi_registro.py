"""Eventi del registro: una riga per evento con ora, identità, tipo, come lo so (osservato | dedotto), età, settore.

Riusa riuso/eventi/eventi.py (classe Eventi, righe 102–200): la si alimenta con un fotogramma di stati alla volta.
Regola unica dell'originale: un evento «osservato» nasce solo in un fotogramma in cui la traccia ha una misura.
Mai «sosta» o «uscito» senza misura: «non ricomparso da n s» (dedotto)."""


class EventiDelRegistro:
    def __init__(self, zone=None):
        raise NotImplementedError("passo 1")

    def passo(self, riga):
        """Riceve il fotogramma del registro (tracce, avvisi, affidabilità) e rende gli eventi da aggiungervi."""
        raise NotImplementedError("passo 1")
