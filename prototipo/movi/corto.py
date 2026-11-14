"""Modo a CORTO RAGGIO: camera di profondità ferma, fino a 3 m, persone a piedi. Tutto il codice esiste: qui si compone.

  riuso/catena (Catena.ciclo)  ->  registro.da_catena  ->  + salute del sensore  ->  + livelli (regola del libero)
                                                         ->  + eventi del registro ->  + etichette a mano
Le correzioni di f12 sono campi di parametri.Parametri («correzioni f12»): si accendono da cfg.regole()."""
from . import nucleo

# Campi di riuso/catena/parametri.Parametri accesi dall'interruttore «correzioni_f12» (letti il 15-11-2026, righe 55-64).
CORREZIONI_F12 = ("soglia_proporzionale", "gruppi_per_picco", "tagliato_su_componente", "riaggancio_rifiuta_tagliati",
                  "riaggancio_rifiuta_occlusore", "riparti_al_riaggancio", "strato_resta")


def parametri_da_config(cfg):
    """parametri.Parametri della catena dalla configurazione: interruttori -> campi booleani; cfg.parametri li scavalca."""
    from . import riuso
    par = riuso.modulo("catena", "parametri").Parametri()
    if cfg.regole()["correzioni_f12"]:
        for nome in CORREZIONI_F12:
            setattr(par, nome, True)
    for nome, valore in cfg.parametri.items():
        if not hasattr(par, nome):
            raise ValueError(f"parametro sconosciuto della catena: {nome}")
        setattr(par, nome, valore)
    return par


def salute_sensore(uscita, taratura_validi, stato):
    """SOLUZIONE_V3 §1.9: NON IN SALUTE se nessun fotogramma nuovo per 0,13 s o tre identici, o pixel validi sotto
    metà della taratura per 0,2 s. Rende la riga del sensore per il registro. (IMU e piano del suolo: fuori dal
    prototipo, camera ferma simulata; lo si dichiara nell'intestazione.)"""
    raise NotImplementedError("passo 1")


class NucleoCorto(nucleo.Nucleo):
    modo = "corto"

    def __init__(self, cfg, meta):
        """Costruisce Catena(meta, parametri_da_config(cfg), fabbrica_predittore=…): PredittoreVelocitaCostante,
        oppure movi.predittore_zona.PredittoreZona se l'interruttore «predittore_zona» è acceso."""
        raise NotImplementedError("passo 1")

    def passo(self, fotogramma, verita=None):
        """catena.ciclo -> registro.da_catena -> livelli.per_settore -> eventi_registro. Con affidabilità persa:
        griglia tutta «non osservato», tracce confermate a «previsto ampio», settori «affidabilita_persa»."""
        raise NotImplementedError("passo 1")
