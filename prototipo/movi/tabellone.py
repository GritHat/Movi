"""Tabellone: i conti che si possono rifare dal solo registro, più il banco in C del predittore.

  dal registro (dove la verità è nota): «dentro la zona: k su n» (l'oggetto vero, mentre non è visto, sta nella
  regione di previsione o nell'avviso), ritardo dell'avviso, celle vere occupate dichiarate «libero» (deve essere 0),
  avvisi tolti senza guardare (deve essere 0). Ogni frequenza con numerosità e intervallo di Wilson al 95 %.
  dal banco in C: compila riuso/c/insieme.c ed esegue `insieme prova …` (campagna grande, in secondi)."""
import math


def wilson(k, n, z=1.959964):
    """Intervallo di Wilson al 95 % per k successi su n. Rende (basso, alto); (nan, nan) se n = 0."""
    if n == 0:
        return (math.nan, math.nan)
    p, d = k / n, 1 + z * z / n
    c, s = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - s), min(1.0, c + s))


def dentro_la_zona(righe):
    """Scorre un registro con la verità; rende {"k": …, "n": …, "wilson95": [basso, alto], "per_classe": {…}}."""
    raise NotImplementedError("passo 1")


def banco_c(argomenti, cartella_uscita, tempo_max_s=120):
    """Compila (se serve) ed esegue riuso/c/insieme con `timeout`; rende il testo e i numeri letti."""
    raise NotImplementedError("passo 1")


def principale(registri, banco=None):
    """Stampa il tabellone di uno o più registri e scrive la riga «riassunto»."""
    raise NotImplementedError("passo 1")
