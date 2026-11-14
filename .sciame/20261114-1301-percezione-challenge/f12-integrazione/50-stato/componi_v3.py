#!/usr/bin/env python3
"""Compone la versione 3 di STATO_PROGETTO.md dalla copia della versione 2 e dai frammenti.
Uso: python3 -I -B componi_v3.py   (nella cartella 50-stato). Non tocca niente fuori dalla cartella."""
import re, subprocess, sys, pathlib
qui = pathlib.Path(__file__).resolve().parent
v2 = (qui / "STATO_V2_copia.md").read_text(encoding="utf-8")
fr = {}
for nome in ("frammenti_1.md", "frammenti_2.md"):
    testo = (qui / nome).read_text(encoding="utf-8")
    for pezzo in re.split(r"^@@@ ", testo, flags=re.M)[1:]:
        chiave, corpo = pezzo.split("\n", 1)
        fr[chiave.strip()] = corpo.rstrip("\n")
ora = subprocess.run(["date", "-Is"], capture_output=True, text=True).stdout.strip()
hm = ora[11:16]
for k in fr:
    fr[k] = fr[k].replace("{ORA}", ora).replace("{HM}", hm)
    if fr[k].endswith("\n---"):
        fr[k] = fr[k][:-4].rstrip("\n")
t = v2
usati = set()
def F(k):
    usati.add(k); return fr[k]
def una(s):
    n = t.count(s)
    if n != 1:
        sys.exit(f"ERRORE: punto d'innesto trovato {n} volte: {s[:80]!r}")
def sost(vecchio, nuovo):
    global t; una(vecchio); t = t.replace(vecchio, nuovo)
def prima(ancora, nuovo):
    global t; una(ancora); t = t.replace(ancora, nuovo + "\n\n" + ancora)
def dopo_riga(inizio, nuovo, stacco="\n\n"):
    """inserisce dopo la riga (intera) che comincia con `inizio`"""
    global t
    righe = [m for m in re.finditer(r"^" + re.escape(inizio) + r".*$", t, flags=re.M)]
    if len(righe) != 1:
        sys.exit(f"ERRORE: riga trovata {len(righe)} volte: {inizio[:80]!r}")
    f = righe[0].end()
    t = t[:f] + stacco + nuovo + t[f:]
def riga(inizio, nuovo):
    """sostituisce la riga intera che comincia con `inizio`"""
    global t
    righe = [m for m in re.finditer(r"^" + re.escape(inizio) + r".*$", t, flags=re.M)]
    if len(righe) != 1:
        sys.exit(f"ERRORE: riga trovata {len(righe)} volte: {inizio[:80]!r}")
    m = righe[0]; t = t[:m.start()] + nuovo + t[m.end():]
def tratto(da, a, nuovo):
    """sostituisce da `da` (compreso) fino ad `a` (escluso)"""
    global t; una(da); i = t.index(da); j = t.index(a, i + len(da))
    t = t[:i] + nuovo + "\n\n" + t[j:]
def prima_del_capitolo(titolo, nuovo):
    """inserisce prima della riga '---' che precede il titolo del capitolo"""
    global t
    m = list(re.finditer(r"\n---\n+" + re.escape(titolo), t))
    if len(m) != 1:
        sys.exit(f"ERRORE: capitolo trovato {len(m)} volte: {titolo!r}")
    i = m[0].start()
    t = t[:i] + "\n" + nuovo + "\n" + t[i:]

# --- testa
riga("**Versione 2 (finale di f11) — 2026-11-14T17:40:55+01:00**", F("TESTA_VERSIONE"))
riga("> **Niente di ciò che segue è provato sull'hardware.**",
     "> **Niente di ciò che segue è provato sull'hardware.** Ogni cifra viene da una simulazione, da un conto o da una scheda tecnica, a sensore fermo. **Nessun fotogramma di una camera della squadra è passato da una prova.** Dopo la versione 2 la catena di riferimento ha elaborato profondità simulata dalle schede tecniche e 8 registrazioni pubbliche di camere altrui (3 510 fotogrammi): servono a provare il lettore, il costo e il moto dei pedoni, non il «libero» né l'identità (`f10-dati/23-verdetto/VERDETTO_DATI.md`, §4). Niente è «validato» (`f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`, in testa). *Frase della versione 2, superata da questa:* «Nessun fotogramma di una camera vera è stato elaborato da una prova vagliata dall'arbitro» (`f4/H-012/09-arbitro/VERDETTO.md`, §5, punto 10).")
f9 = re.search(r"^> - \*\*f9, verdetto dell'arbitro.*$", t, flags=re.M).group(0)
f11 = re.search(r"^> - \*\*f11:\*\*.*$", t, flags=re.M).group(0)
tratto("**Che cosa fotografa questa versione.**", "## Sintesi",
       F("FOTOGRAFIA") + "\n>\n> **Restano veri, dal riquadro «Dopo la fotografia» della versione 2:**\n" + f9 + "\n" + f11)
tratto("## Sintesi", "## Legenda", F("SINTESI"))
riga("| preliminare | **[prel.]** |", F("LEGENDA_PREL"))
prima("## Indice", F("LEGENDA_SIGLE_V3"))
tratto("## Indice", "## 1. Scopo, traccia della challenge, requisiti e vincoli", F("INDICE") + "\n\n---")
sost("(il §5.7 dice che cosa cambia alla chiusura di ogni estensione)", "(il §5.7 dice che cosa cambia alla prossima valutazione)")
sost("5. si aggiunge **una riga al registro delle modifiche** in fondo: data, valutazione, che cosa è cambiato.",
     "5. si aggiunge **una riga al registro delle modifiche** in fondo: data, valutazione, che cosa è cambiato;\n6. dalla versione 3: il cambio si scrive in un riquadro «Versione N» in testa al paragrafo toccato (regola, parametri, stato della prova, limiti, che cosa è superato); il testo superato resta sotto, e il riquadro lo nomina con «superato da …».")
# --- cap. 1
prima("### 1.2 La traccia della challenge, frase per frase", F("S1_1_V3"))
prima("### 1.3 Gli otto requisiti", F("S1_2_V3").lstrip("\n"))
prima("### 1.4 Vincoli e obiettivi posti dall'utente", F("S1_3_V3").lstrip("\n"))
sost("| f7 · in corso |", "| f7 · **chiusa** (V7: §5.2) |")
sost("| f8 · in corso |", "| f8 · **chiusa** (V8: §5.3) |")
sost("| f7, f8, f9 · in corso |", "| f7, f8, f9 · **chiuse** (V7, V8, V9) |")
sost("| f10 · in corso |", "| f10 · **chiusa** (VD: §5.5) |")
dopo_riga("| 8 | prima delle 16:09 |", F("S1_4_RIGHE"), stacco="\n")
prima("**In ordine di priorità.**", F("S1_4_V3").lstrip("\n"))
sost("| primo taglio possibile (4 ore) |", "| primo taglio possibile (4 ore): **superato dal decimo addendum**; classificatore su più classi richiesto, non realizzato, etichette a mano (§2.2, B6) |")
sost("cinque predittori in gara in f8, nessun vincitore |", "cinque predittori in gara in f8, nessun vincitore: **superato da V8**; predittori sd-0 (ripiego) e sd-1 (principale), regione per tutta l'occlusione (§2.2, B5) |")
sost("nel triage nessuna mappa memorizzata entra nelle 14 ore |", "nel triage nessuna mappa memorizzata entra nelle 14 ore; **V7: no** alla mappa voxel nelle 14 + 4 ore (§5.2) |")
# --- cap. 2
sost("## 2. Architettura del nucleo, componente per componente", "## 2. Architettura: dal nucleo alla soluzione versione 3, componente per componente")
prima("Il nucleo è la **soluzione versione 2** (`f4/H-012/05-correzioni/SOLUZIONE_V2.md`), nata dalla versione 1", F("S2_INTRO_V3"))
dopo_riga("### 2.1 Schema a blocchi", F("S2_1_V3"))
sost("#### B6. Ramo asincrono di riconoscimento", "#### B6. Classificazione e profili (era: ramo asincrono di riconoscimento)")
for n in range(1, 10):
    dopo_riga(f"#### B{n}. ", F(f"B{n}_V3"))
prima("### 2.3 I nove invarianti e il loro stato", F("B10_B11"))
sost("### 2.3 I nove invarianti e il loro stato", "### 2.3 Gli invarianti: i venti della versione 3 e i nove del nucleo")
dopo_riga("### 2.3 Gli invarianti", F("S2_3_V3"))
dopo_riga("### 2.4 Costo, dipendenze, condizioni", F("S2_4_V3"))
# --- cap. 3
dopo_riga("### 3.1 In breve", "> **Versione 3.** Nessun sensore è stato acceso nemmeno dopo la versione 2. Le cifre geometriche corrette dai fascicoli, ciò che ha detto il sensore simulato, la tabella di decisione per l'inventario e le prime tre misure sono nel §3.10. Cambi rispetto ai punti qui sotto: la posa va nota entro meno di 0,5°, con una prova d'ingresso; il pannello della demo è alto 1,8 m; il modello resta non deciso e l'inventario non è arrivato.")
prima_del_capitolo("## 4. Prove eseguite e risultati numerici", F("S3_10"))
# --- cap. 4
prima("### 4.2 Le cifre principali", F("S4_1_NUOVE"))
dopo_riga("### 4.2 Le cifre principali", "> **Versione 3.** La tabella qui sotto resta quella delle cifre **del nucleo** (fasi f1–f6). Le cifre nuove sono nel §4.6. Le righe corrette dai ricalcoli dei fascicoli (fra le altre la riga 1, i limiti «99,25 %» e «99,85 %», la soglia della regola «mobile», la velocità coperta) sono nel §4.7: dove differiscono, vale il §4.7. Le righe sull'identità al ritorno e sul muro «mobile» sono superate dalle righe N14 e N22 del §4.6.")
dopo_riga("### 4.3 Requisiti e contraddizioni dopo le prove", F("S4_3_NOTA"))
dopo_riga("### 4.5 Ciò che nessuna prova ha ancora toccato", F("S4_5_NOTA"))
prima_del_capitolo("## 5. Valutazioni in corso: le estensioni f7–f10", F("S4_6_7_8"))
# --- cap. 5
sost("## 5. Valutazioni in corso: le estensioni f7–f10", F("S5_TESTA"))
sost("### 5.1 Le quattro estensioni: a che punto sono", "### 5.1 Le quattro estensioni alla fotografia delle 16:13")
dopo_riga("### 5.1 Le quattro estensioni alla fotografia", F("S5_1_NOTA"))
sost("### 5.2 f7 — mappa voxel e conciliazione con la traccia della challenge [prel.]", "### 5.2 f7 — mappa voxel e conciliazione con la traccia della challenge")
dopo_riga("### 5.2 f7 — ", F("S5_2_ESITO"))
sost("### 5.3 f8 — la continuità visiva [prel.]", "### 5.3 f8 — la continuità visiva")
dopo_riga("### 5.3 f8 — ", F("S5_3_ESITO"))
dopo_riga("### 5.4 f9 — ", F("S5_4_ESITO"))
sost("### 5.5 f10 — dati pubblici e sensori simulati [prel.]", "### 5.5 f10 — dati pubblici e sensori simulati")
dopo_riga("### 5.5 f10 — ", F("S5_5_ESITO"))
i = t.index("### 5.6 Il passo d'integrazione"); m = re.search(r"\n---\n+## 6\. Piano e rischi", t)
t = t[:i] + F("S5_6_7_8_9") + "\n" + t[m.start():]
# --- cap. 6
dopo_riga("## 6. Piano e rischi", F("S6_TESTA"))
sost("### 6.1 Il piano\n", "### 6.1 I piani precedenti: bilancio, tappe, ricalcolo dell'arbitro di f9\n")
prima_del_capitolo("## 7. Le decisioni che spettano all'utente", F("S6_2_V3").lstrip("\n") + "\n\n" + F("S6_3"))
# --- cap. 7
prima("| # | Decisione (e chi la pone) | Default oggi · stato |", F("S7_V3") + "\n\n**Le undici decisioni della versione 2** (lo stato di oggi è nella seconda tabella del riquadro qui sopra).")
# --- cap. 8, 9, 10
prima_del_capitolo("## 9. Metodo dello sciame e cronologia", F("S8_10"))
dopo_riga("| dopo le 16:37 | un quarto commit locale", F("S9_2_RIGHE"), stacco="\n")
prima_del_capitolo("## Glossario", F("S10_3"))
# --- glossario: righe nuove, poi ordine alfabetico
dopo_riga("| **versione 1, versione 2** |", F("GLOSSARIO_RIGHE"), stacco="\n")
def accoda(inizio, testo):
    global t
    righe = [m for m in re.finditer(r"^" + re.escape(inizio) + r".*$", t, flags=re.M)]
    if len(righe) != 1:
        sys.exit(f"ERRORE: riga di glossario trovata {len(righe)} volte: {inizio!r}")
    m = righe[0]; r = m.group(0).rstrip(); assert r.endswith("|")
    t = t[:m.start()] + r[:-1].rstrip() + " **Versione 3:** " + testo + " |" + t[m.end():]
accoda("| **anello cieco** |", "il termine è «vuoto vicino»: è una striscia, non un anello; a ±44° il suolo si vede da 1,71–1,73 m (§3.10)")
accoda("| **area prevista** |", "si dice «regione prevista» (R90)")
accoda("| **cuneo** |", "l'ombra dell'occlusore in cui una traccia è entrata; con la fascia w forma l'area d'avviso R100")
accoda("| **fascia** |", "è la «fascia di guardia», w; copre 1,13 m/s (voce sotto)")
accoda("| **identità ambigua** |", "è un evento, non una chiusura della traccia; l'identità riagganciata è sempre «presunta»")
accoda("| **libero** |", "solo nel fotogramma corrente, senza memoria: metà dell'impronta della cella e delle 8 vicine legge il suolo (`nuvole-1`); a schermo «suolo visto libero da 1,3 m a d m». «In almeno uno degli ultimi 3 fotogrammi» è superato (V7)")
accoda("| **non confermato** |", "per 0,2 s, poi la traccia è chiusa «non più rilevato»")
accoda("| **nucleo** |", "il nucleo è la base della soluzione versione 3 (voce sotto)")
accoda("| **osservato, previsto, perso** |", "«perso» non esiste più; gli stati sono osservato, visto in parte, non confermato, previsto, previsto ampio (§2.2, B5)")
accoda("| **portatore del sensore** |", "ha un profilo fisso dichiarato all'avvio, senza classificazione: velocità, tempo di reazione, frenata, gradi di libertà (§2.2, B6)")
accoda("| **possibile presenza** |", "non finisce più per riaggancio: finisce solo dove il suolo è rivisto libero (H-503); è l'area R100")
accoda("| **strato 1** |", "è l'area d'avviso R100")
accoda("| **strato 2** |", "sostituito dalla regione prevista R90, che non è il cerchio del filtro")
g0 = t.index("| Termine | Che cosa vuol dire qui |"); g1 = t.index("\n\n", g0)
tab = t[g0:g1].split("\n")
def chiave(r):
    return re.sub(r"[*`«»\[\]]", "", r.split("|")[1]).strip().casefold()
t = t[:g0] + "\n".join(tab[:2] + sorted(tab[2:], key=chiave)) + t[g1:]
# --- registro, appendici
riga("| 3 | *(da scrivere)*", F("REGISTRO_RIGHE"))
prima("## Appendice B — Chiavi dei riferimenti usate in questo documento", F("APP_A_V3"))
prima("## Appendice C — Provenienza delle sezioni e controlli dell'unione", F("APP_B_V3"))
t = t.rstrip("\n") + "\n\n" + F("APP_C_V3") + "\n"
mancanti = set(fr) - usati
if mancanti:
    sys.exit(f"ERRORE: frammenti non usati: {sorted(mancanti)}")
(qui / "STATO_PROGETTO.md").write_text(t, encoding="utf-8")
print("scritto STATO_PROGETTO.md:", len(t.splitlines()), "righe;", len(t.split()), "parole;", ora)
