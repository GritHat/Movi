"""Tabellone: i conti che si possono rifare dal solo registro, più il banco in C del predittore.

  dal registro (dove la verità è nota): «dentro la zona: k su n» (l'oggetto vero, mentre non è visto, sta in ciò
  che il sistema mostra: la regione di previsione, o le celle dell'avviso se la traccia è «previsto ampio»),
  fotogrammi a oggetto nascosto senza avviso, avvisi tolti senza guardare (deve essere 0).
  Ogni frequenza con numerosità e intervallo di Wilson al 95 %.
  dal banco in C: compila riuso/c/insieme.c ed esegue `insieme prova …` (campagna grande, in secondi)."""
import json
import math
import os
import subprocess

from . import registro


def wilson(k, n, z=1.959964):
    """Intervallo di Wilson al 95 % per k successi su n. Rende (basso, alto); (nan, nan) se n = 0."""
    if n == 0:
        return (math.nan, math.nan)
    p, d = k / n, 1 + z * z / n
    c, s = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - s), min(1.0, c + s))


def _w(k, n):
    lo, hi = wilson(k, n)
    return {"k": k, "n": n, "wilson95": [round(lo, 4), round(hi, 4)] if n else None}


def dentro_la_zona(righe, griglia=None):
    """Scorre un registro con la verità; rende i conti del tabellone (persone vere nascoste)."""
    from .corto import dentro
    k = n = senza_avviso = nascosti = 0
    for r in righe:
        if r.get("tipo") == "intestazione":
            griglia = r["griglie"]["polare_corto"]
            continue
        if r.get("tipo") != "fotogramma" or not r.get("verita"):
            continue
        for o in r["verita"]["oggetti"]:
            if o["visibile"]:
                continue
            nascosti += 1
            senza_avviso += not r["avvisi"]
            m, _ = dentro(r, o["pos"][0], o["pos"][1], griglia)
            n += 1
            k += m
    return {"dentro_la_zona": _w(k, n), "nascosti_senza_avviso": _w(senza_avviso, nascosti)}


def banco_c(argomenti, tempo_max_s=120):
    """Compila (se serve) ed esegue riuso/c/insieme con `timeout`; rende il testo."""
    from . import riuso
    c = riuso.percorso("c")
    eseguibile = os.path.join(c, "insieme")
    if not os.path.exists(eseguibile):
        subprocess.run(["gcc", "-O2", "-o", eseguibile, os.path.join(c, "insieme.c"), "-lm"], check=True,
                       timeout=tempo_max_s)
    p = subprocess.run(["timeout", str(tempo_max_s), eseguibile] + argomenti.split(), capture_output=True, text=True)
    return p.stdout + p.stderr


def principale(registri, banco=None):
    """Stampa il tabellone di uno o più registri e scrive la riga «riassunto» accanto (<registro>.tabellone.json)."""
    for percorso in registri:
        righe = list(registro.leggi(percorso))
        conti = dentro_la_zona(righe)
        errori = registro.valida_sequenza(righe)
        conti["avvisi_tolti_senza_guardare"] = sum("tolto senza guardare" in e for _, e in errori)
        conti["righe_non_valide"] = len({i for i, _ in errori})
        z = conti["dentro_la_zona"]
        print(f"{percorso}: dentro la zona: {z['k']} su {z['n']}  (Wilson 95 %: {z['wilson95']}) · "
              f"nascosta senza avviso: {conti['nascosti_senza_avviso']['k']} su {conti['nascosti_senza_avviso']['n']}"
              f" · avvisi tolti senza guardare: {conti['avvisi_tolti_senza_guardare']}")
        with open(percorso + ".tabellone.json", "w", encoding="utf-8") as f:
            json.dump(dict(conti, tipo="riassunto"), f, ensure_ascii=False, indent=1)
    if banco:
        print(banco_c(banco))
