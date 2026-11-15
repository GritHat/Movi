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
    k = n = ka = na = 0
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
            tempi.append(riga.get("tempo_ciclo_ms") or 0.0)     # modo lungo: None (il costo del nucleo è in f15)
            if celle:
                riga["celle"]["rle"] = registro.codifica_rle(nuc.griglia_stati())
            if griglia and riga.get("verita"):
                for o in riga["verita"]["oggetti"]:
                    if not o["visibile"]:
                        n += 1
                        k += dentro(riga, o["pos"][0], o["pos"][1], griglia)[0]
            if cfg.modo == "lungo":
                k, n, ka, na = _conta_lungo(riga, k, n, ka, na)
                riga["tabellone"] = {"dentro_la_zona": {"k": k, "n": n}, "dentro_l_avviso": {"k": ka, "n": na}}
            else:
                riga["tabellone"] = {"dentro_la_zona": {"k": k, "n": n}}
            scr.scrivi(riga)
        tempi.sort()
        riassunto = {"tipo": "riassunto", "fotogrammi": scr.n - 1, "dentro_la_zona": {"k": k, "n": n},
                     **({"dentro_l_avviso": {"k": ka, "n": na}} if cfg.modo == "lungo" else {}),
                     "tempo_ciclo_ms": {"mediana": tempi[len(tempi) // 2], "p95": tempi[int(0.95 * (len(tempi) - 1))]}
                     if tempi else None}
        scr.scrivi(riassunto)
    finally:
        scr.chiudi()
    return riassunto


def _conta_lungo(riga, k, n, ka, na):
    """Modo lungo: per ogni oggetto vero NON visibile da nessun sensore e già visto una volta, conta se sta nella zona
    dichiarata (cerchio a 0,90) di qualche traccia (k su n, solo dove c'è una zona) e se sta in qualche avviso di
    possibile presenza (ka su na, sempre). Pianta (x, y): la quota non entra nel conto (dichiarato)."""
    import math
    v = riga.get("verita") or {}
    for o in v.get("oggetti", []):
        if o["visibile"]:
            _VISTI.add(o["id"])
            continue
        if o["id"] not in _VISTI:
            continue
        x, y = o["pos"][0], o["pos"][1]
        zone = [t["regione"] for t in riga["tracce"] if t.get("regione")]
        if zone:
            n += 1
            k += any(math.hypot(x - z["centro"][0], y - z["centro"][1]) <= z["raggio_m"] for z in zone)
        na += 1
        ka += any(_in_forma(a["forma"], x, y) for a in riga["avvisi"])
    return k, n, ka, na


_VISTI = set()


def _in_forma(f, x, y):
    import math
    if f["tipo"] == "cerchio":
        return math.hypot(x - f["centro"][0], y - f["centro"][1]) <= f["raggio_m"]
    if f["tipo"] == "poligono":
        p, dentro = f["punti"], False
        for i in range(len(p)):
            (x1, y1), (x2, y2) = p[i], p[i - 1]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                dentro = not dentro
        return dentro
    return False
