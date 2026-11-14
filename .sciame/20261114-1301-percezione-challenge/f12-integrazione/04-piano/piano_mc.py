#!/usr/bin/env python3
"""Monte Carlo delle durate del piano 14 + 4 ore (sciame-pianificatore, f12, 04-piano).

Rifare (dalla cartella 04-piano):
    timeout 300 ../../f10-dati/ambiente/venv/bin/python -I -B piano_mc.py > risultati_piano_mc.txt

MODELLO (tutto dichiarato; niente e' misurato: le stime a tre punti sono STIME del pianificatore).
- Ogni compito ha (ottimista, probabile, pessimista) in ore di lavoro di chi lo fa; durata di base ~ triangolare.
- Correlazione: ore di lavoro = base x g x f_p, con g fattore comune di squadra ~ lognormale (sigma 0,12) e
  f_p fattore della persona ~ lognormale (sigma 0,20), entrambi a media 1. Due compiti della stessa persona
  condividono g e f_p; due compiti di persone diverse solo g. La correlazione che ne esce e' stampata.
- Ore d'orologio = ore di lavoro / e_p, con e_p ~ triangolare (0,78; 0,88; 0,96): pause, pasti, interruzioni
  (14 ore d'orologio = 10,9-13,4 ore utili; l'arbitro di f9 usava 11-12,5-14).
- Un compito comune (piu' persone) usa la media dei fattori di chi vi partecipa e occupa tutti.
- Ordine FISSO per persona (la coda scritta nel piano), nessun riordino dinamico: un compito parte quando sono
  finiti i predecessori e sono libere le persone. Le regole dei punti di controllo NON sono simulate, salvo i
  tetti di tempo del «nocciolo non tagliabile».
- I compiti fuori dal minimo (sd-1, registro degli eventi, prima ora col sensore) si fanno nelle finestre libere
  e si sospendono quando arriva un compito del minimo: non lo ritardano (costo del cambio: 0,25 h tolte alla finestra).
- MD = minimo dimostrabile: la prova generale (PG) finisce entro l'ora 14,0.
"""
import sys
import numpy as np

SEME = 20261114
N = 20000
SIG_G, SIG_P = 0.12, 0.20
EFF = (0.78, 0.88, 0.96)
T_CAM = (5.0, 5.5, 7.0)          # ora in cui arrivano le prime registrazioni del sensore (ramo A), triangolare
CAMBIO = 0.25                    # ore perse a ogni ripresa di un compito sospeso

# id: (ottimista, probabile, pessimista, descrizione)
STIME = {
    "K0": (0.5, 0.75, 1.5, "avvio comune: ambiente, 25 prove, lettura della versione 3, formato delle uscite"),
    "A1": (0.5, 1.0, 2.0, "rilettura di mappa, geometria, gruppi, ciclo (571 righe)"),
    "A2": (1.0, 1.5, 3.0, "«libero» nel solo fotogramma corrente; affidabilita' persa sui pixel validi"),
    "A3": (1.5, 2.5, 5.0, "sensore non in salute (c), C2 (d), controllo del piano (e)"),
    "A4": (1.5, 3.0, 6.0, "robustezza su profondita' realistica: soglie per risoluzione, pannello che «si muove»"),
    "B1": (1.0, 1.5, 3.0, "rilettura di inseguimento, presenza, Kalman (487 righe) e dei predittori in C"),
    "B2": (1.5, 2.0, 4.0, "M3: interfaccia «insieme di celle», sd-0, pavimento, punto ibrido"),
    "B3": (3.5, 5.0, 9.0, "M1+c4+c7, M2+c2, M7+c1, c5 (una persona)"),
    "B3a": (2.0, 3.0, 5.5, "M1+c4+c7, M2+c2: ingresso in ombra, stati, chiusure"),
    "B3b": (2.0, 3.0, 5.5, "M7+c1 con la prova dell'estraneo, c5"),
    "C1": (2.0, 3.0, 6.0, "riproduttore e schermo: mappa a quattro stati, tracce, eta'"),
    "C2": (2.0, 2.5, 5.0, "M5+c6+c8: disegno della previsione e contatore"),
    "C3": (1.5, 2.5, 5.0, "tabella delle regole ridotta, un suono, «affidabilita' persa»"),
    "D1": (1.0, 1.5, 3.0, "rilettura del simulatore e delle misure di f10; scelta delle sequenze"),
    "D2": (3.0, 4.5, 8.0, "M6: occlusione virtuale, registro per ciclo, tabellone «dentro k su n»"),
    "D3": (0.75, 1.5, 3.0, "corsa del tabellone sul simulato, dopo l'integrazione"),
    "D4": (0.75, 1.5, 3.0, "corsa sulle sequenze pubbliche (THOR e descrittive)"),
    "E1": (0.75, 1.5, 3.0, "modulo d'inventario, istruzioni di registrazione, sorgente da cartella"),
    "E2": (1.0, 1.5, 3.0, "banco di regressione e riproduzione a 15 Hz"),
    "J1": (1.0, 2.0, 4.0, "integrazione: tutte le correzioni insieme sulle sequenze di fumo (due persone)"),
    "JS": (0.5, 1.0, 2.0, "aggancio dello schermo alla catena integrata"),
    "LAT": (0.5, 1.0, 2.0, "latenza e cicli al secondo in riproduzione"),
    "J2": (0.5, 1.5, 4.0, "correzione dei difetti trovati dal tabellone (due persone)"),
    "VID": (0.75, 1.0, 2.0, "video di ripiego e scaletta"),
    "PG": (0.5, 0.75, 1.5, "prova generale (tutti)"),
    # fuori dal minimo
    "B4": (3.0, 4.0, 7.0, "M4: sd-1 dietro la stessa interfaccia"),
    "E3": (2.0, 3.0, 5.0, "registro degli eventi innestato sugli stati"),
    "E4": (1.5, 2.5, 5.0, "prima ora col sensore: formato, posa, pareti, rumore, corsa della catena"),
    "E4b": (0.5, 1.0, 2.0, "solo dati di un altro dispositivo (telefono con LiDAR): conversione e corsa descrittiva"),
}


# Compiti nuovi del piano rivisto (TC), aggiunti DOPO il primo lancio: estratti da un generatore a parte, cosi' le
# estrazioni del primo lancio non cambiano. Le stime dei compiti gia' presenti non sono state toccate.
STIME2 = {
    "PI": (0.5, 1.0, 2.0, "prova d'insieme sulle sequenze di fumo (due persone)"),
    "TAB": (0.5, 1.0, 2.0, "corsa finale del tabellone e lettura"),
    "C3a": (0.5, 1.0, 2.0, "«affidabilita' persa» a schermo e un suono"),
    "C3b": (1.0, 1.5, 3.0, "tabella delle regole ridotta"),
}
TETTI_TC = {"PG": 0.75}
TETTI_TC_RID = {"PG": 0.75, "A3": 1.5, "PI": 1.0, "TAB": 1.5, "LAT": 0.5}


def piano_tc(nome):
    t5, t4 = ["P1", "P2", "P3", "P4", "P5"], ["P1", "P2", "P3", "P4"]
    rid = nome.endswith("-RID")
    base = nome.replace("-RID", "")
    if base == "TC-5":
        cod = [
            ("K0", t5, []),
            ("A1", ["P1"], ["K0"]), ("B1", ["P2"], ["K0"]), ("C1", ["P3"], ["K0"]), ("D1", ["P4"], ["K0"]),
            ("E1", ["P5"], ["K0"]),
            ("A2", ["P1"], ["A1"]), ("B2", ["P2"], ["B1"]), ("C2", ["P3"], ["C1"]), ("D2", ["P4"], ["D1"]),
            ("E2", ["P5"], ["E1"]),
            ("A3", ["P1"], ["A2"]), ("B3a", ["P2"], ["B2"]), ("B3b", ["P5"], ["E2", "B2"]), ("C3a", ["P3"], ["C2"]),
            ("C3b", ["P1"], ["A3"]), ("D4", ["P4"], ["D2", "B2", "A2"]),
            ("PI", ["P2", "P5"], ["A2", "A3", "B3a", "B3b", "E2", "C2"]),
            ("LAT", ["P5"], ["PI"]), ("TAB", ["P4"], ["PI", "D2"]),
            ("PG", t5, ["TAB", "LAT", "D4", "C3a", "C3b"]),
        ]
    elif base == "TC-5-B3":   # B3 intero a P2; A3 a P5; P1 fa la tabella delle regole
        cod = [
            ("K0", t5, []),
            ("A1", ["P1"], ["K0"]), ("B1", ["P2"], ["K0"]), ("C1", ["P3"], ["K0"]), ("D1", ["P4"], ["K0"]),
            ("E1", ["P5"], ["K0"]),
            ("A2", ["P1"], ["A1"]), ("B2", ["P2"], ["B1"]), ("C2", ["P3"], ["C1"]), ("D2", ["P4"], ["D1"]),
            ("E2", ["P5"], ["E1"]),
            ("C3b", ["P1"], ["A2"]), ("B3", ["P2"], ["B2"]), ("A3", ["P5"], ["E2", "A2"]), ("C3a", ["P3"], ["C2"]),
            ("D4", ["P4"], ["D2", "B2", "A2"]),
            ("PI", ["P1", "P2"], ["A2", "A3", "B3", "E2", "C2"]),
            ("LAT", ["P5"], ["PI"]), ("TAB", ["P4"], ["PI", "D2"]),
            ("PG", t5, ["TAB", "LAT", "D4", "C3a", "C3b"]),
        ]
    elif base == "TC-4":      # quattro persone: E1 a P4, E2 a P3, B3b e C3b a P1
        cod = [
            ("K0", t4, []),
            ("A1", ["P1"], ["K0"]), ("B1", ["P2"], ["K0"]), ("E2", ["P3"], ["K0"]), ("E1", ["P4"], ["K0"]),
            ("A2", ["P1"], ["A1"]), ("B2", ["P2"], ["B1"]), ("C1", ["P3"], ["E2"]), ("D1", ["P4"], ["E1"]),
            ("A3", ["P1"], ["A2"]), ("B3a", ["P2"], ["B2"]), ("C2", ["P3"], ["C1"]), ("D2", ["P4"], ["D1"]),
            ("B3b", ["P1"], ["A3", "B2"]), ("C3a", ["P3"], ["C2"]), ("C3b", ["P4"], ["D2"]),
            ("D4", ["P4"], ["C3b", "B2", "A2"]),
            ("PI", ["P1", "P2"], ["A2", "A3", "B3a", "B3b", "E2", "C2"]),
            ("TAB", ["P4"], ["PI", "D2"]), ("LAT", ["P3"], ["PI", "C3a"]),
            ("PG", t4, ["TAB", "LAT", "D4", "C3a", "C3b"]),
        ]
    else:
        raise ValueError(nome)
    if rid:   # i tagli scritti: niente tabella delle regole estesa, niente sequenze pubbliche prima dell'ora 14
        cod = [(k, chi, [q for q in pred if q not in ("C3b", "D4")]) for k, chi, pred in cod if k not in ("C3b", "D4")]
    return (t4 if base == "TC-4" else t5), cod


def piano(nome):
    if nome.startswith("TC-"):
        return piano_tc(nome)
    """Restituisce (persone, lista ordinata di (id, chi, predecessori)), opzionali, tetti."""
    tutti5, tutti4 = ["P1", "P2", "P3", "P4", "P5"], ["P1", "P2", "P3", "P4"]
    if nome == "RIF-5":   # riferimento: B3 a una persona
        return tutti5, [
            ("K0", tutti5, []),
            ("A1", ["P1"], ["K0"]), ("B1", ["P2"], ["K0"]), ("C1", ["P3"], ["K0"]), ("D1", ["P4"], ["K0"]),
            ("E1", ["P5"], ["K0"]),
            ("A2", ["P1"], ["A1"]), ("B2", ["P2"], ["B1"]), ("C2", ["P3"], ["C1"]), ("D2", ["P4"], ["D1"]),
            ("E2", ["P5"], ["E1"]),
            ("A3", ["P1"], ["A2"]), ("B3", ["P2"], ["B2"]), ("C3", ["P3"], ["C2"]),
            ("A4", ["P5"], ["E2"]), ("D4", ["P4"], ["D2", "B2", "A2"]),
            ("J1", ["P1", "P2"], ["A2", "A3", "B3", "E2"]),
            ("JS", ["P3"], ["J1", "C2"]), ("LAT", ["P5"], ["J1", "A4"]),
            ("D3", ["P4"], ["J1", "D2", "A4"]),
            ("J2", ["P1", "P2"], ["D3"]), ("VID", ["P5"], ["D3", "JS"]),
            ("PG", tutti5, ["J2", "VID", "LAT", "D4", "C3", "JS"]),
        ]
    if nome in ("DIV-5", "DIV-5-A", "DIV-5-B", "NOC-5"):   # B3 diviso fra P2 e P5; A4 a P1
        ramo_a = nome == "DIV-5-A"
        cod = [
            ("K0", tutti5, []),
            ("A1", ["P1"], ["K0"]), ("B1", ["P2"], ["K0"]), ("C1", ["P3"], ["K0"]), ("D1", ["P4"], ["K0"]),
            ("E1", ["P5"], ["K0"]),
            ("A2", ["P1"], ["A1"]), ("B2", ["P2"], ["B1"]), ("C2", ["P3"], ["C1"]), ("D2", ["P4"], ["D1"]),
            ("E2", ["P5"], ["E1"]),
            ("A3", ["P1"], ["A2"]), ("B3a", ["P2"], ["B2"]), ("B3b", ["P5"], ["E2", "B2"]), ("C3", ["P3"], ["C2"]),
        ]
        if not ramo_a:
            cod.append(("D4", ["P4"], ["D2", "B2", "A2"]))
        cod += [
            ("A4", ["P1"], ["A3"]),
            ("J1", ["P2", "P5"], ["A2", "A3", "B3a", "B3b", "E2"]),
            ("JS", ["P3"], ["J1", "C2"]), ("LAT", ["P5"], ["J1"]),
        ]
        if ramo_a:   # nel ramo A la finestra di P4 va al sensore: le sequenze pubbliche passano a P5
            cod.append(("D4", ["P5"], ["D2", "J1"]))
        if nome == "NOC-5":   # nocciolo: niente D4 ne' VID; A4 non blocca D3
            cod = [c for c in cod if c[0] != "D4"]
            cod += [("D3", ["P4"], ["J1", "D2"]), ("J2", ["P1", "P2"], ["D3"]),
                    ("PG", tutti5, ["J2", "LAT", "C3", "JS"])]
        else:
            cod += [("D3", ["P4"], ["J1", "D2", "A4"]), ("J2", ["P1", "P2"], ["D3"]),
                    ("VID", ["P5"], ["D3", "JS"]),
                    ("PG", tutti5, ["J2", "VID", "LAT", "D4", "C3", "JS"])]
        return tutti5, cod
    if nome == "RIF-4":   # quattro persone, B3 a una persona
        return tutti4, [
            ("K0", tutti4, []),
            ("A1", ["P1"], ["K0"]), ("B1", ["P2"], ["K0"]), ("C1", ["P3"], ["K0"]), ("E1", ["P4"], ["K0"]),
            ("E2", ["P1"], ["A1"]), ("B2", ["P2"], ["B1"]), ("C2", ["P3"], ["C1"]), ("D1", ["P4"], ["E1"]),
            ("A2", ["P1"], ["E2"]), ("B3", ["P2"], ["B2"]), ("C3", ["P3"], ["C2"]), ("D2", ["P4"], ["D1"]),
            ("A3", ["P1"], ["A2"]), ("A4", ["P4"], ["D2", "A2"]),
            ("J1", ["P1", "P2"], ["A2", "A3", "B3", "E2"]),
            ("JS", ["P3"], ["J1", "C2"]),
            ("D3", ["P4"], ["J1", "D2", "A4"]),
            ("J2", ["P1", "P2"], ["D3"]), ("VID", ["P3"], ["D3", "JS"]),
            ("D4", ["P4"], ["D3"]), ("LAT", ["P4"], ["D4"]),
            ("PG", tutti4, ["J2", "VID", "LAT", "D4", "C3", "JS"]),
        ]
    if nome == "DIV-4":   # quattro persone, B3 diviso fra P2 e P1; il banco di regressione a P3
        return tutti4, [
            ("K0", tutti4, []),
            ("A1", ["P1"], ["K0"]), ("B1", ["P2"], ["K0"]), ("C1", ["P3"], ["K0"]), ("E1", ["P4"], ["K0"]),
            ("A2", ["P1"], ["A1"]), ("B2", ["P2"], ["B1"]), ("E2", ["P3"], ["C1"]), ("D1", ["P4"], ["E1"]),
            ("A3", ["P1"], ["A2"]), ("B3a", ["P2"], ["B2"]), ("C2", ["P3"], ["E2"]), ("D2", ["P4"], ["D1"]),
            ("B3b", ["P1"], ["A3", "B2"]), ("C3", ["P3"], ["C2"]), ("A4", ["P4"], ["D2", "A2"]),
            ("J1", ["P1", "P2"], ["A2", "A3", "B3a", "B3b", "E2"]),
            ("JS", ["P3"], ["J1", "C2"]),
            ("D3", ["P4"], ["J1", "D2", "A4"]),
            ("J2", ["P1", "P2"], ["D3"]), ("VID", ["P3"], ["D3", "JS"]),
            ("D4", ["P4"], ["D3"]), ("LAT", ["P4"], ["D4"]),
            ("PG", tutti4, ["J2", "VID", "LAT", "D4", "C3", "JS"]),
        ]
    raise ValueError(nome)


TETTI_NOCCIOLO = {"A4": 2.0, "J2": 1.0, "LAT": 0.5, "PG": 0.75}   # ore d'orologio, tempo chiuso


def estrai(rng, persone, n=N):
    """Fattori comuni e di persona; durate di base per ogni compito (stesse estrazioni per tutti i casi)."""
    g = np.exp(rng.normal(-SIG_G ** 2 / 2, SIG_G, n))
    f = {p: np.exp(rng.normal(-SIG_P ** 2 / 2, SIG_P, n)) for p in persone}
    e = {p: rng.triangular(EFF[0], EFF[1], EFF[2], n) for p in persone}
    base = {k: rng.triangular(v[0], v[1], v[2], n) for k, v in STIME.items()}
    tcam = rng.triangular(T_CAM[0], T_CAM[1], T_CAM[2], n)
    rng2 = np.random.default_rng(int(g[0] * 1e9) % (2 ** 31) + 100)   # generatore a parte per i compiti nuovi
    for k, v in STIME2.items():
        base[k] = rng2.triangular(v[0], v[1], v[2], n)
    return {"g": g, "f": f, "e": e, "base": base, "tcam": tcam}


def durata(k, chi, x, piu=None, per_g=1.0):
    fm = np.mean([x["f"][p] for p in chi], axis=0)
    em = np.mean([x["e"][p] for p in chi], axis=0)
    d = x["base"][k] * x["g"] * per_g * fm / em
    if piu and k in piu:
        d = d + piu[k]
    return d


def calendario(nome, x, piu=None, per_g=1.0, tetti=None):
    persone, coda = piano(nome)
    n = len(x["g"])
    libero = {p: np.zeros(n) for p in persone}
    inizio, fine, lega = {}, {}, {}
    ultimo = {p: None for p in persone}
    for k, chi, pred in coda:
        d = durata(k, chi, x, piu, per_g)
        if tetti and k in tetti:
            d = np.minimum(d, tetti[k])
        cand = [(fine[q], q) for q in pred] + [(libero[p], ultimo[p]) for p in chi if ultimo[p] is not None]
        if cand:
            m = np.stack([c[0] for c in cand])
            s = m.max(axis=0)
            chi_lega = m.argmax(axis=0)
            lega[k] = (chi_lega, [c[1] for c in cand])
        else:
            s = np.zeros(n)
            lega[k] = None
        inizio[k], fine[k] = s, s + d
        for p in chi:
            libero[p] = fine[k]
            ultimo[p] = k
    return {"inizio": inizio, "fine": fine, "lega": lega, "coda": coda, "persone": persone}


def criticita(cal, n):
    """Quota di estrazioni in cui il compito sta sul percorso critico (risalendo da PG)."""
    conta = {k: 0 for k, _, _ in cal["coda"]}
    nomi = [k for k, _, _ in cal["coda"]]
    idx = {k: i for i, k in enumerate(nomi)}
    corrente = np.full(n, idx["PG"])
    vivo = np.ones(n, bool)
    for _ in range(len(nomi) + 1):
        if not vivo.any():
            break
        prossimo = corrente.copy()
        for k in nomi:
            sel = vivo & (corrente == idx[k])
            if not sel.any():
                continue
            conta[k] += int(sel.sum())
            if cal["lega"][k] is None:
                vivo[sel] = False
                continue
            chi_lega, cand = cal["lega"][k]
            mappa = np.array([idx[c] for c in cand])
            prossimo[sel] = mappa[chi_lega[sel]]
        corrente = prossimo
    return {k: conta[k] / n for k in nomi}


def rango(v):
    r = np.empty(len(v))
    r[np.argsort(v, kind="stable")] = np.arange(len(v))
    return r


def spearman(a, b):
    return float(np.corrcoef(rango(a), rango(b))[0, 1])


def wilson(k, n, z=1.96):
    p = k / n
    c = p + z * z / (2 * n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / (1 + z * z / n), (c + h) / (1 + z * z / n)


def riga(nome, descr, t, soglia=14.0):
    k = int((t <= soglia).sum())
    lo, hi = wilson(k, len(t))
    q = np.quantile(t, [0.1, 0.5, 0.8, 0.9])
    print(f"{nome:10s} {descr:62s} P(<= {soglia:4.1f} h) = {k/len(t):.3f} [{lo:.3f}; {hi:.3f}] | "
          f"ora di fine: p10 {q[0]:5.2f}  mediana {q[1]:5.2f}  p80 {q[2]:5.2f}  p90 {q[3]:5.2f}")
    return k / len(t)


def finestra(cal, x, persona_coda, dur, da=None):
    """Ore libere di una persona fra i suoi compiti del minimo, fino all'inizio di PG; meno il costo dei cambi."""
    n = len(x["g"])
    tot = np.zeros(n)
    prec = None
    miei = [k for k, chi, _ in cal["coda"] if persona_coda in chi]
    for k in miei:
        if prec is not None:
            a = cal["fine"][prec] if da is None else np.maximum(cal["fine"][prec], da)
            buco = np.maximum(cal["inizio"][k] - a, 0.0)
            tot += np.maximum(buco - CAMBIO * (buco > 0), 0.0)
        prec = k
    return tot, tot >= dur


def main():
    rng = np.random.default_rng(SEME)
    P5 = ["P1", "P2", "P3", "P4", "P5"]
    x = estrai(rng, P5)
    print(f"# piano_mc.py — seme {SEME}, {N} estrazioni per caso; numpy {np.__version__}; python {sys.version.split()[0]}")
    print(f"# fattore di squadra lognormale sigma {SIG_G}; fattore di persona lognormale sigma {SIG_P}; "
          f"efficienza d'orologio triangolare {EFF}")
    # correlazioni realizzate
    dB2, dB3a = durata("B2", ["P2"], x), durata("B3a", ["P2"], x)
    dA2 = durata("A2", ["P1"], x)
    print(f"# correlazione (Pearson) fra due compiti della stessa persona (B2, B3a di P2): {np.corrcoef(dB2, dB3a)[0,1]:.2f}; "
          f"fra compiti di persone diverse (B2 di P2, A2 di P1): {np.corrcoef(dB2, dA2)[0,1]:.2f}")
    somma_prob = {}
    for nome in ("RIF-5", "DIV-5", "RIF-4", "DIV-4", "NOC-5"):
        _, coda = piano(nome)
        somma_prob[nome] = sum(STIME[k][1] * len(chi) for k, chi, _ in coda)
    print("# somma delle durate probabili (ore-persona): " + "; ".join(f"{k} {v:.2f}" for k, v in somma_prob.items()))
    print()
    print("== 1. Probabilita' che il minimo dimostrabile sia chiuso (fine della prova generale) ==")
    ris, cals = {}, {}
    casi = [("RIF-5", "5 persone, B3 a una persona, nessun sensore"),
            ("DIV-5", "5 persone, B3 diviso (P2 e P5), nessun sensore [ramo C]"),
            ("DIV-5-A", "5 persone, B3 diviso, arriva una camera di profondita' [A]"),
            ("DIV-5-B", "5 persone, B3 diviso, arriva solo altro [ramo B]"),
            ("RIF-4", "4 persone, B3 a una persona"),
            ("DIV-4", "4 persone, B3 diviso (P2 e P1)")]
    for nome, descr in casi:
        piu = {"D3": CAMBIO} if nome in ("DIV-5-A", "DIV-5-B") else None
        cal = calendario(nome, x, piu=piu)
        cals[nome] = cal
        ris[nome] = riga(nome, descr, cal["fine"]["PG"])
    cal = calendario("NOC-5", x, tetti=TETTI_NOCCIOLO)
    cals["NOC-5"] = cal
    ris["NOC-5"] = riga("NOC-5", "nocciolo non tagliabile (senza D4 e VID; A4, J2, LAT a tempo chiuso)", cal["fine"]["PG"])
    for s in (15.0, 16.0):
        riga("DIV-5", f"come sopra, entro l'ora {s:.0f}", cals["DIV-5"]["fine"]["PG"], s)
    for s in (13.0,):
        riga("NOC-5", f"come sopra, entro l'ora {s:.0f}", cals["NOC-5"]["fine"]["PG"], s)

    print()
    print("== 2. Tappe del piano consigliato DIV-5 (ore d'orologio di fine: p10 / mediana / p90) e criticita' ==")
    cal = cals["DIV-5"]
    cri = criticita(cal, N)
    pg = cal["fine"]["PG"]
    for k, chi, _ in cal["coda"]:
        q = np.quantile(cal["fine"][k], [0.1, 0.5, 0.9])
        qi = np.quantile(cal["inizio"][k], 0.5)
        print(f"  {k:4s} {'+'.join(chi) if len(chi) < 5 else 'tutti':8s} inizio (mediana) {qi:5.2f} | fine {q[0]:5.2f} / {q[1]:5.2f} / {q[2]:5.2f} | "
              f"sul percorso critico {100*cri[k]:5.1f} % | Spearman(durata di base, fine PG) {spearman(x['base'][k], pg):+.2f}")
    print("  fattori: " + "; ".join(
        [f"squadra g {spearman(x['g'], pg):+.2f}"] +
        [f"f_{p} {spearman(x['f'][p], pg):+.2f}" for p in P5] +
        [f"e_{p} {spearman(x['e'][p], pg):+.2f}" for p in P5]))
    cri_rif = criticita(cals["RIF-5"], N)
    print("  RIF-5, criticita': " + "; ".join(f"{k} {100*v:.0f} %" for k, v in sorted(cri_rif.items(), key=lambda kv: -kv[1])[:10]))

    print()
    print("== 3. Che cosa muove di piu' P(MD) nel piano DIV-5 (una leva alla volta) ==")
    p0 = ris["DIV-5"]
    leve = []
    for k, _, _ in cal["coda"]:
        c = calendario("DIV-5", x, piu={k: 1.0})
        leve.append((float((c["fine"]["PG"] <= 14).mean()) - p0, f"+1 h su {k}"))
    for fg in (0.9, 1.1, 1.2):
        c = calendario("DIV-5", x, per_g=fg)
        leve.append((float((c["fine"]["PG"] <= 14).mean()) - p0, f"tutte le durate x {fg}"))
    for d, nome in sorted(leve):
        print(f"  {nome:28s} dP = {d:+.3f}")
    # nessuna correzione dopo il tabellone (J2 = 0)
    xx = dict(x); xx["base"] = dict(x["base"]); xx["base"]["J2"] = np.zeros(N)
    c = calendario("DIV-5", xx)
    print(f"  {'nessun difetto da correggere (J2 = 0)':28s} dP = {float((c['fine']['PG'] <= 14).mean()) - p0:+.3f}")
    xx = dict(x); xx["base"] = dict(x["base"])
    for k in ("A1", "B1", "D1"):
        xx["base"][k] = x["base"][k] * 2
    for k in ("A2", "A3", "B2", "B3a", "B3b"):
        xx["base"][k] = x["base"][k] * 1.5
    c = calendario("DIV-5", xx)
    print(f"  {'il riuso va male (riletture x 2, correzioni x 1,5)':28s} dP = {float((c['fine']['PG'] <= 14).mean()) - p0:+.3f}")

    print()
    print("== 4. Compiti fuori dal minimo: probabilita' che stiano nelle finestre libere prima della prova generale ==")
    cal = cals["DIV-5"]
    for k, p in (("E3", "P3"), ("B4", "P1")):
        d = durata(k, [p], x)
        tot, ok = finestra(cal, x, p, d)
        print(f"  ramo C, {k} ({p}): finestra mediana {np.median(tot):.2f} h; P(sta nella finestra) = {ok.mean():.3f}; "
              f"e con PG chiusa entro 14: {(ok & (cal['fine']['PG'] <= 14)).mean():.3f}")
    cal = cals["DIV-5-A"]
    d = durata("E4", ["P4"], x)
    tot, ok = finestra(cal, x, "P4", d, da=x["tcam"])
    print(f"  ramo A, E4 (P4, dal'arrivo delle registrazioni, mediana ora {np.median(x['tcam']):.2f}): finestra mediana {np.median(tot):.2f} h; "
          f"P(prima ora col sensore chiusa prima di PG) = {ok.mean():.3f}; e con PG entro 14: {(ok & (cal['fine']['PG'] <= 14)).mean():.3f}")
    cal = cals["DIV-5-B"]
    d = durata("E4b", ["P4"], x)
    tot, ok = finestra(cal, x, "P4", d, da=x["tcam"])
    print(f"  ramo B, E4b (P4): P(sta nella finestra) = {ok.mean():.3f}; e con PG entro 14: {(ok & (cal['fine']['PG'] <= 14)).mean():.3f}")

    print()
    print("== 5. Stabilita': altri due semi (P(MD) entro 14 h) ==")
    for seme in (SEME + 1, SEME + 2):
        xs = estrai(np.random.default_rng(seme), P5)
        print(f"  seme {seme}: " + "; ".join(
            f"{nm} {float((calendario(nm, xs, tetti=TETTI_NOCCIOLO if nm == 'NOC-5' else None)['fine']['PG'] <= 14).mean()):.3f}"
            for nm in ("RIF-5", "DIV-5", "RIF-4", "DIV-4", "NOC-5")))

    print()
    print("== 6. Punti di controllo nel piano DIV-5: P(tappa chiusa entro l'ora) ==")
    cal = cals["DIV-5"]
    f = cal["fine"]
    tappe = [(2.0, "K0+E1: inventario spedito, tutti con le 25 prove verdi", np.maximum(f["K0"], f["E1"])),
             (5.0, "A2, B2, C1 chiusi: «libero» corretto, sd-0, schermo che riproduce", np.maximum(np.maximum(f["A2"], f["B2"]), f["C1"])),
             (8.0, "A3, B3a, B3b, D2 chiusi: pronti per l'integrazione", np.maximum(np.maximum(f["A3"], f["B3a"]), np.maximum(f["B3b"], f["D2"]))),
             (11.0, "J1 chiusa e tabellone corso (D3)", f["D3"]),
             (14.0, "PG chiusa", f["PG"])]
    for ora, descr, t in tappe:
        print(f"  ora {ora:4.1f}: {descr:66s} P = {(t <= ora).mean():.3f}; mediana {np.median(t):5.2f}; p80 {np.quantile(t, 0.8):5.2f}")
    # regola dell'ora 8: se B3a/B3b non sono chiusi all'ora 8, quanto vale P(MD) condizionata
    tardi8 = np.maximum(f["B3a"], f["B3b"]) > 8.0
    print(f"  se all'ora 8 B3a o B3b non e' chiuso (succede nel {tardi8.mean():.3f} dei casi): P(MD) = {(f['PG'][tardi8] <= 14).mean():.3f}; "
          f"se sono chiusi: {(f['PG'][~tardi8] <= 14).mean():.3f}")
    fn = cals["NOC-5"]["fine"]["PG"]
    print(f"  stesso segnale, ma passando al nocciolo: P(nocciolo entro 14 | in ritardo all'ora 8) = {(fn[tardi8] <= 14).mean():.3f}")
    tardi11 = f["D3"] > 11.0
    print(f"  se all'ora 11 il tabellone non e' corso ({tardi11.mean():.3f} dei casi): P(MD) = {(f['PG'][tardi11] <= 14).mean():.3f}; "
          f"P(nocciolo entro 14) = {(fn[tardi11] <= 14).mean():.3f}")
    rivisto(x)


def rivisto(x):
    P5 = ["P1", "P2", "P3", "P4", "P5"]
    print()
    print("== 7. PIANO RIVISTO dopo il primo lancio (TC: integrazione continua, tempo chiuso). Stime dei compiti invariate ==")
    print("# somma delle durate probabili (ore-persona): " + "; ".join(
        f"{nm} {sum((STIME.get(k) or STIME2[k])[1] * len(chi) for k, chi, _ in piano(nm)[1]):.2f}"
        for nm in ("TC-5", "TC-5-RID", "TC-5-B3", "TC-4", "TC-4-RID")))
    cals, ris = {}, {}
    for nome, descr, tetti in (
            ("TC-5", "5 persone, B3 diviso, minimo intero, nessun sensore", TETTI_TC),
            ("TC-5-RID", "5 persone, B3 diviso, con i tagli scritti", TETTI_TC_RID),
            ("TC-5-B3", "5 persone, B3 a una persona (P2), minimo intero", TETTI_TC),
            ("TC-5-B3-RID", "5 persone, B3 a una persona, con i tagli scritti", TETTI_TC_RID),
            ("TC-4", "4 persone, B3 diviso (P2 e P1), minimo intero", TETTI_TC),
            ("TC-4-RID", "4 persone, B3 diviso, con i tagli scritti", TETTI_TC_RID)):
        cals[nome] = calendario(nome, x, tetti=tetti)
        ris[nome] = riga(nome, descr, cals[nome]["fine"]["PG"])
    # rami: il sensore occupa P4 nelle finestre (costo del cambio su TAB)
    for nome, descr, tetti in (("TC-5", "ramo A o B: come TC-5, piu' 0,25 h di cambio su TAB", TETTI_TC),
                               ("TC-5-RID", "ramo A o B: come TC-5-RID, piu' 0,25 h di cambio su TAB", TETTI_TC_RID)):
        c = calendario(nome, x, piu={"TAB": CAMBIO}, tetti=tetti)
        riga(nome, descr, c["fine"]["PG"])
        if nome == "TC-5-RID":
            d = durata("E4", ["P4"], x)
            tot, ok = finestra(c, x, "P4", d, da=x["tcam"])
            print(f"           ramo A: P(prima ora col sensore, E4, chiusa nelle finestre di P4 prima di PG) = {ok.mean():.3f}; "
                  f"insieme a PG entro 14: {(ok & (c['fine']['PG'] <= 14)).mean():.3f}; finestra mediana {np.median(tot):.2f} h")
    for s in (13.0, 15.0, 16.0):
        riga("TC-5-RID", f"come sopra, entro l'ora {s:.0f}", cals["TC-5-RID"]["fine"]["PG"], s)
    riga("TC-5", "minimo intero, entro l'ora 16 (fine del raffinamento utile)", cals["TC-5"]["fine"]["PG"], 16.0)

    print()
    print("-- 7b. Tappe di TC-5-RID (ore d'orologio) e criticita'")
    cal = cals["TC-5-RID"]
    cri = criticita(cal, len(x["g"]))
    pg = cal["fine"]["PG"]
    for k, chi, _ in cal["coda"]:
        q = np.quantile(cal["fine"][k], [0.1, 0.5, 0.9])
        qi = np.quantile(cal["inizio"][k], 0.5)
        print(f"  {k:4s} {'+'.join(chi) if len(chi) < 5 else 'tutti':8s} inizio (mediana) {qi:5.2f} | fine {q[0]:5.2f} / {q[1]:5.2f} / {q[2]:5.2f} | "
              f"sul percorso critico {100*cri[k]:5.1f} % | Spearman(durata di base, fine PG) {spearman(x['base'][k], pg):+.2f}")
    print("  fattori: " + "; ".join(
        [f"squadra g {spearman(x['g'], pg):+.2f}"] +
        [f"f_{p} {spearman(x['f'][p], pg):+.2f}" for p in P5] +
        [f"e_{p} {spearman(x['e'][p], pg):+.2f}" for p in P5]))

    print()
    print("-- 7c. Che cosa muove di piu' P(MD) in TC-5-RID (una leva alla volta)")
    p0 = ris["TC-5-RID"]
    leve = []
    for k, _, _ in cal["coda"]:
        c = calendario("TC-5-RID", x, piu={k: 1.0}, tetti={q: v for q, v in TETTI_TC_RID.items() if q != k})
        leve.append((float((c["fine"]["PG"] <= 14).mean()) - p0, f"+1 h su {k}"))
    for fg in (0.8, 0.9, 1.1, 1.2):
        c = calendario("TC-5-RID", x, per_g=fg, tetti=TETTI_TC_RID)
        leve.append((float((c["fine"]["PG"] <= 14).mean()) - p0, f"tutte le durate x {fg}"))
    xx = dict(x); xx["base"] = dict(x["base"])
    for k in ("A1", "B1", "D1"):
        xx["base"][k] = x["base"][k] * 2
    for k in ("A2", "A3", "B2", "B3a", "B3b"):
        xx["base"][k] = x["base"][k] * 1.5
    c = calendario("TC-5-RID", xx, tetti=TETTI_TC_RID)
    leve.append((float((c["fine"]["PG"] <= 14).mean()) - p0, "il riuso va male (riletture x 2, correzioni x 1,5)"))
    xx = dict(x); xx["base"] = dict(x["base"]); xx["base"]["K0"] = np.full(len(x["g"]), 0.25)
    c = calendario("TC-5-RID", xx, tetti=TETTI_TC_RID)
    leve.append((float((c["fine"]["PG"] <= 14).mean()) - p0, "avvio preparato prima dell'ora 0 (K0 = 0,25 h)"))
    xx = dict(x); xx["e"] = {p: np.full(len(x["g"]), 0.96) for p in P5}
    c = calendario("TC-5-RID", xx, tetti=TETTI_TC_RID)
    leve.append((float((c["fine"]["PG"] <= 14).mean()) - p0, "pause al minimo (efficienza 0,96 per tutti)"))
    for d, nome in sorted(leve):
        print(f"  {nome:52s} dP = {d:+.3f}")

    print()
    print("-- 7d. Punti di controllo di TC-5-RID: P(tappa chiusa entro l'ora) e valore del segnale")
    f = cal["fine"]
    fn = cal["fine"]["PG"]
    tappe = [(2.0, "K0 + E1: prove verdi per tutti, inventario spedito", np.maximum(f["K0"], f["E1"])),
             (5.0, "A2, B2, C1, E2 chiusi", np.maximum(np.maximum(f["A2"], f["B2"]), np.maximum(f["C1"], f["E2"]))),
             (8.0, "D2 chiuso e B3a, B3b cominciati", np.maximum(f["D2"], np.maximum(cal["inizio"]["B3a"], cal["inizio"]["B3b"]))),
             (11.0, "A3, B3a, B3b, C2, C3a chiusi (tutto nel tronco)", np.maximum(np.maximum(f["A3"], f["B3a"]), np.maximum(np.maximum(f["B3b"], f["C2"]), f["C3a"]))),
             (14.0, "PG chiusa", fn)]
    for ora, descr, t in tappe:
        si = t <= ora
        print(f"  ora {ora:4.1f}: {descr:52s} P = {si.mean():.3f}; mediana {np.median(t):5.2f}; p80 {np.quantile(t, 0.8):5.2f} | "
              f"P(PG entro 14 | tappa rispettata) = {(fn[si] <= 14).mean() if si.any() else float('nan'):.3f}; "
              f"| mancata) = {(fn[~si] <= 14).mean() if (~si).any() else float('nan'):.3f}")
    # chi manca all'ora 12 (che cosa si dichiara non entrato)
    print("  componenti non chiusi all'ora 12,0 (quota dei casi): " + "; ".join(
        f"{k} {(f[k] > 12.0).mean():.3f}" for k in ("A2", "A3", "B2", "B3a", "B3b", "C1", "C2", "C3a", "D2", "E2")))
    print("  continuita' e sicurezza nel tronco (A2, A3, B2, B3a, B3b) entro: " + "; ".join(
        f"ora {o:.0f}: {(np.maximum(np.maximum(f['A2'], f['A3']), np.maximum(f['B2'], np.maximum(f['B3a'], f['B3b']))) <= o).mean():.3f}"
        for o in (10, 11, 12, 13, 14, 16)))
    print("-- 7f. [aggiunto dopo aver visto 7d] La misura della prima ora e i punti di controllo ritarati sulle mediane")
    r = (f["B1"]) / 2.25      # ora di fine di K0 + B1 divisa per la somma delle durate probabili (0,75 + 1,5 h)
    for a, b in ((0, 1.2), (1.2, 1.5), (1.5, 1.8), (1.8, 9)):
        sel = (r >= a) & (r < b)
        print(f"  rapporto (fine di K0 + rilettura B1) / 2,25 h in [{a}; {b}): quota {sel.mean():.3f}; P(PG entro 14) = {(fn[sel] <= 14).mean():.3f}")
    r5 = np.maximum(f["K0"] , 0) / 0.75
    for a, b in ((0, 1.2), (1.2, 1.6), (1.6, 9)):
        sel = (r5 >= a) & (r5 < b)
        print(f"  rapporto (fine di K0) / 0,75 h in [{a}; {b}): quota {sel.mean():.3f}; P(PG entro 14) = {(fn[sel] <= 14).mean():.3f}")
    mx = lambda *ks: np.max(np.stack([f[k] for k in ks]), axis=0)
    for ora, descr, t in ((2.5, "K0 chiuso, A1 chiuso, inventario (E1) quasi: A1", mx("A1")),
                          (5.0, "A2 ed E2 chiusi", mx("A2", "E2")),
                          (8.0, "B2, C1, A3 chiusi", mx("B2", "C1", "A3")),
                          (11.0, "B3a, B3b, C2, D2 chiusi", mx("B3a", "B3b", "C2", "D2")),
                          (12.5, "PI chiusa", mx("PI"))):
        si = t <= ora
        print(f"  ora {ora:4.1f}: {descr:48s} P = {si.mean():.3f} | P(PG entro 14 | rispettata) = {(fn[si] <= 14).mean():.3f}; | mancata) = {(fn[~si] <= 14).mean():.3f}")
    print("-- 7e. Stabilita' su altri due semi")
    for seme in (SEME + 1, SEME + 2):
        xs = estrai(np.random.default_rng(seme), P5)
        print(f"  seme {seme}: " + "; ".join(
            f"{nm} {float((calendario(nm, xs, tetti=tt)['fine']['PG'] <= 14).mean()):.3f}"
            for nm, tt in (("TC-5", TETTI_TC), ("TC-5-RID", TETTI_TC_RID), ("TC-5-B3", TETTI_TC), ("TC-4", TETTI_TC), ("TC-4-RID", TETTI_TC_RID))))


if __name__ == "__main__":
    main()
