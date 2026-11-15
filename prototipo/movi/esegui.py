"""`movi esegui`: sorgente -> nucleo -> registro. È l'unico punto in cui i tre si incontrano."""
import os


def principale(scena, config, uscita, celle=False, ultimo=None):
    """`scena`: nome di una scena d'esempio (scene/SCENE.json) o etichetta libera (la sorgente è nella configurazione).
    Scrive <uscita>/registro.jsonl (intestazione, fotogrammi col tabellone cumulato, riassunto). `celle`: aggiunge la
    griglia intera in RLE a ogni fotogramma (serve a `mostra`; il registro cresce). Rende il riassunto."""
    from . import config as C, nucleo, registro, sorgenti
    from .corto import dentro
    cfg = C.carica(config)
    sorgente = sorgenti.apri(cfg)
    nuc = nucleo.crea(cfg, sorgente.meta)
    os.makedirs(uscita, exist_ok=True)
    scr = registro.Scrittore(os.path.join(uscita, "registro.jsonl"))
    k = n = 0
    tempi = []
    try:
        testa = nuc.intestazione()
        testa["ostacoli"] = list(sorgente.ostacoli)      # verità della simulazione: solo per disegnare la scena
        griglia = testa["griglie"].get("polare_corto")
        scr.scrivi(testa)
        for fot in sorgente:
            if ultimo is not None and fot.indice > ultimo:
                break
            riga = nuc.passo(fot, verita=sorgente.verita(fot.indice))
            tempi.append(riga.get("tempo_ciclo_ms") or 0.0)
            if celle:
                riga["celle"]["rle"] = registro.codifica_rle(nuc.griglia_stati())
            if griglia and riga.get("verita"):
                for o in riga["verita"]["oggetti"]:
                    if not o["visibile"]:
                        n += 1
                        k += dentro(riga, o["pos"][0], o["pos"][1], griglia)[0]
            riga["tabellone"] = {"dentro_la_zona": {"k": k, "n": n}}
            scr.scrivi(riga)
        tempi.sort()
        riassunto = {"tipo": "riassunto", "fotogrammi": scr.n - 1, "dentro_la_zona": {"k": k, "n": n},
                     "tempo_ciclo_ms": {"mediana": tempi[len(tempi) // 2], "p95": tempi[int(0.95 * (len(tempi) - 1))]}
                     if tempi else None}
        scr.scrivi(riassunto)
    finally:
        scr.chiudi()
    return riassunto
