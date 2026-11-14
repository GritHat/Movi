"""`movi esegui`: sorgente -> nucleo -> registro. È l'unico punto in cui i tre si incontrano."""
import os


def principale(scena, config, uscita, celle=False, ultimo=None):
    """`scena`: nome di una scena d'esempio (scene/SCENE.json), cartella di una sequenza, o `scenari.json:nome`.
    Scrive <uscita>/registro.jsonl (intestazione, fotogrammi, riassunto col tabellone). `celle`: aggiunge la
    griglia intera in RLE a ogni fotogramma (serve a `mostra`; il registro cresce). Rende il riassunto."""
    from . import config as C, nucleo, registro, sorgenti
    cfg = C.carica(config)
    sorgente = sorgenti.apri(cfg)                                   # passo 1
    nuc = nucleo.crea(cfg, sorgente.meta)
    os.makedirs(uscita, exist_ok=True)
    scr = registro.Scrittore(os.path.join(uscita, "registro.jsonl"))
    try:
        scr.scrivi(nuc.intestazione())
        for fot in sorgente:
            if ultimo is not None and fot.indice > ultimo:
                break
            riga = nuc.passo(fot, verita=sorgente.verita(fot.indice))
            if celle:
                riga["celle"]["rle"] = registro.codifica_rle(nuc.griglia_stati())
            scr.scrivi(riga)
    finally:
        scr.chiudi()
    return {"righe": scr.n}
