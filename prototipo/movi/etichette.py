"""Etichette di classe ASSEGNATE A MANO da file. Il classificatore non c'è: è supposto esistente (lavori futuri).

File JSON: {"commento": …, "regole": [{"classe": "aereo_rullaggio", "id_vero": "A1"} |
                                        {"classe": …, "da_s": 0, "a_s": 99, "zona": [x0, x1, y0, y1]} |
                                        {"classe": …, "id_traccia": 3}]}
Una regola lega una classe a un oggetto della verità simulata (`id_vero`), a una traccia, o a ciò che nasce in una
zona in un intervallo. Senza regola: «non_classificato», origine «assente».

VINCOLO (principio 3): un'etichetta non entra MAI nel calcolo dell'avviso di possibile presenza, della fascia di
guardia o dei livelli dei settori. Può solo scegliere il modello di moto della regione di previsione. La fascia
viene dalle classi AMMESSE dello scenario (la più veloce), non dall'etichetta della traccia."""


def carica(percorso, classi_ammesse):
    """Legge il file; rifiuta le classi non ammesse dallo scenario. Rende la lista delle regole."""
    raise NotImplementedError("passo 1")


def risolvi(regole, tracce, t, verita=None):
    """{id_traccia: classe} per questo fotogramma. L'aggancio a `id_vero` usa la verità SOLO per simulare il
    classificatore assente (traccia più vicina all'oggetto vero): lo dice l'intestazione del registro."""
    raise NotImplementedError("passo 1")
