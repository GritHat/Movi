"""Etichette di classe ASSEGNATE A MANO da file. Il classificatore non c'è: è supposto esistente (lavori futuri).

File JSON: {"commento": …, "regole": [{"classe": …, "id_vero": "s1"} |
                                        {"classe": …, "da_s": 0, "a_s": 99, "zona": [x0, x1, y0, y1]} |
                                        {"classe": …, "id_traccia": 3}]}
Una regola lega una classe a un oggetto della verità simulata (`id_vero`), a una traccia, o a ciò che sta in una zona
in un intervallo di tempo. Senza regola: «non_classificato», origine «assente».

VINCOLO (principio 3): un'etichetta non entra MAI nel calcolo dell'avviso di possibile presenza, della fascia di
guardia o dei livelli dei settori: questo modulo è usato solo per scrivere `classe` e `origine_etichetta`
(prova: prove/prova_principi.py, «cambiando le etichette avvisi, settori e celle restano identici»)."""
import json
import math


def carica(percorso, classi_ammesse):
    """Legge il file; rifiuta le classi non ammesse dallo scenario. Rende la lista delle regole ([] senza file)."""
    if not percorso:
        return []
    with open(percorso, encoding="utf-8") as f:
        regole = json.load(f).get("regole", [])
    for r in regole:
        if r["classe"] not in classi_ammesse:
            raise ValueError(f"etichetta «{r['classe']}» non ammessa dallo scenario (classi ammesse: {classi_ammesse})")
    return regole


def risolvi(regole, tracce, t, verita=None):
    """{id_traccia: classe} per questo fotogramma. `tracce`: [(id, x, y) o (id, None, None)].
    L'aggancio a `id_vero` usa la verità SOLO per simulare il classificatore assente (traccia più vicina all'oggetto
    vero, entro 0,5 m): lo dichiara l'intestazione del registro."""
    fuori = {}
    veri = {o["id"]: o["pos"] for o in (verita or {}).get("oggetti", [])}
    for r in regole:
        if "id_traccia" in r:
            fuori.setdefault(r["id_traccia"], r["classe"])
        elif "id_vero" in r and r["id_vero"] in veri:
            vx, vy = veri[r["id_vero"]]
            vicine = [(math.hypot(x - vx, y - vy), i) for i, x, y in tracce if x is not None]
            if vicine and min(vicine)[0] <= 0.5:
                fuori.setdefault(min(vicine)[1], r["classe"])
        elif "zona" in r and r.get("da_s", -math.inf) <= t <= r.get("a_s", math.inf):
            x0, x1, y0, y1 = r["zona"]
            for i, x, y in tracce:
                if x is not None and x0 <= x <= x1 and y0 <= y <= y1:
                    fuori.setdefault(i, r["classe"])
    return fuori
