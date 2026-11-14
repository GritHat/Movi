"""Il nucleo comune: una sola interfaccia per i due modi. Chi scrive il registro, il tabellone e le viste conosce
solo questa.

    nucleo = crea(cfg, sorgente.meta)
    for fot in sorgente:
        riga = nucleo.passo(fot, verita=sorgente.verita(fot.indice))   # un fotogramma del registro (movi.registro)

Le parole comuni (stati delle celle, delle tracce, livelli, salute) stanno in movi.registro: i due modi le usano
identiche. Il nucleo NON legge mai la verità per decidere: la riceve solo per ricopiarla nel registro."""


class Nucleo:
    modo = None

    def intestazione(self):
        """La prima riga del registro (movi.registro.intestazione) con griglie, riferimento, ostacoli, sensori."""
        raise NotImplementedError

    def passo(self, fotogramma, verita=None):
        """Elabora un fotogramma e rende la riga del registro."""
        raise NotImplementedError

    def griglia_stati(self):
        """La griglia dell'ultimo ciclo (matrice di 0–3, ordine di registro.STATI_CELLA), per chi la disegna."""
        raise NotImplementedError


def crea(cfg, meta):
    """Fabbrica: movi.corto.NucleoCorto o movi.lungo.NucleoLungo secondo cfg.modo."""
    if cfg.modo == "corto":
        from .corto import NucleoCorto
        return NucleoCorto(cfg, meta)
    from .lungo import NucleoLungo
    return NucleoLungo(cfg, meta)
