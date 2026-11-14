#!/usr/bin/env python3
"""Controllo del criterio A-4: cerca nel testo dell'allegato, fuori dagli
argomenti di \\cite, \\label, \\ref (e simili) e fuori dai commenti, le parole
e le sigle che rimandano all'organizzazione interna del lavoro.
Uso: python3 controlla_interni.py [cartella]   (predefinita: quella del programma)
Esce con 0 se le occorrenze non ammesse sono zero, con 1 altrimenti."""
import re, sys, pathlib

base = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent
files = [base / "allegato_tecnico.tex"] + sorted((base / "capitoli").glob("*.tex"))

# Argomenti da non esaminare: chiavi di citazione, etichette, rimandi, file inclusi.
ARG = re.compile(r"\\(?:cite[a-z]*|label|ref|eqref|pageref|autoref|input|include|bibliography|bibliographystyle|hyperref|texorpdfstring)\s*(?:\[[^\]]*\])*\{[^{}]*\}")
COMMENTO = re.compile(r"(?<!\\)%.*$")

I = re.IGNORECASE
REGOLE = [
    ("sciame", r"\bsciam[ei]\b", I),
    ("agente/agenti", r"\bagent[ei]\b", I),
    ("ruolo/ruoli", r"\bruol[oi]\b", I),
    ("arbitro", r"\barbitr\w*", I),
    ("verdetto", r"\bverdett\w*", I),
    ("addendum", r"\baddendum\b|\baddenda\b", I),
    ("torneo", r"\btorne[oi]\b", I),
    ("corsia", r"\bcorsi[ae]\b", I),
    ("coordinatore", r"\bcoordinator\w*", I),
    ("convocazione", r"\bconvocazion\w*", I),
    ("fascicolo", r"\bfascicol\w*", I),
    ("hackathon", r"\bhackathon\b", I),
    ("fase (parola)", r"\bfas[ei]\b", I),
    ("fase fNN", r"(?<![A-Za-z\\_^{$.])f\d{1,2}\b(?![,.]\d)", 0),
    ("sigla H-/K-/F-/V-/C-", r"\b[HKFVC]-\d+", 0),
    ("sigla C1..C8", r"(?<![A-Za-z\\_^])C[1-8]\b", 0),
    ("sigla M1..M8", r"(?<![A-Za-z\\_^])M[1-8]\b", 0),
    ("sigla c1..c8", r"(?<![A-Za-z\\_^])c[1-8]\b", 0),
    ("sigla S1..S12", r"(?<![A-Za-z\\_^])S(?:1[0-2]|[1-9])\b", 0),
    ("sigla R1..R8", r"(?<![A-Za-z\\_^])R[1-8]\b", 0),
    ("sd-0/sd-1", r"\bsd-[01]\b", I),
    # Un percorso: due o più componenti separati da «/», ciascuno con almeno due lettere
    # (così non scattano i rapporti numerici «1/2/3», le unità «m/s» e gli elenchi di TikZ «nome/0.40»).
    ("percorso con /", r"(?<![\\\w])(?:\.{0,2}/)?(?:[\w.-]*[A-Za-z]{2}[\w.-]*/)+[\w.-]*[A-Za-z]{2}[\w.-]*", 0),
    ("estensione di file", r"\b[\w-]+\.(?:md|py|c|json|txt|csv|npz|sh)\b", 0),
    # Un orario: hh:mm isolato (non dentro terne «46.5:133.5:1.243» degli archi di TikZ).
    ("orario hh:mm", r"(?<![\d.:,])(?:[01]?\d|2[0-3]):[0-5]\d(?![\d:]|[.,]\d)", 0),
    ("in corso", r"\bin corso\b", I),
    ("in correzione", r"\bin correzione\b", I),
    ("da fare", r"\bda fare\b", I),
    ("preliminare", r"\bpreliminar[ei]\b", I),
    ("versione N", r"\bversion[ei]\s+(?:[0-9]+|[IVX]+)\b|\bv[0-9]\b", I),
    ("squadra", r"\bsquadr[ae]\b", I),
    ("ore-persona", r"\bore[- ]persona\b|\bore[- ]uomo\b", I),
]

# Eccezioni motivate, una per una: (file, regola, frammento della riga) -> motivo.
ECCEZIONI = [
    ("allegato_tecnico.tex", "squadra", r"\newcommand{\squadra}",
     "definizione del comando \\squadra chiesto per il frontespizio: lo compila l'utente"),
    ("allegato_tecnico.tex", "squadra", r"Autori: \squadra",
     "uso del comando \\squadra nel frontespizio: nel PDF compare il nome scritto dall'utente"),
]

def pulisci(riga):
    riga = COMMENTO.sub("", riga)
    prec = None
    while prec != riga:
        prec = riga
        riga = ARG.sub(" ", riga)
    return riga

trovate, ammesse = [], []
for f in files:
    nome = f.name
    for n, riga in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        testo = pulisci(riga)
        for etichetta, rx, fl in REGOLE:
            if etichetta == "hackathon" and nome.startswith("01_"):
                continue
            for m in re.finditer(rx, testo, fl):
                a, b = max(0, m.start() - 45), min(len(testo), m.end() + 45)
                voce = (nome, n, etichetta, m.group(0), testo[a:b].strip())
                motivo = next((mot for (fn, et, fr, mot) in ECCEZIONI
                               if fn == nome and et == etichetta and fr in riga), None)
                (ammesse if motivo else trovate).append(voce + ((motivo,) if motivo else ()))

print(f"File esaminati: {len(files)}")
for v in trovate:
    print(f"VIETATO  {v[0]}:{v[1]}  [{v[2]}]  «{v[3]}»  … {v[4]} …")
for v in ammesse:
    print(f"ECCEZIONE {v[0]}:{v[1]}  [{v[2]}]  «{v[3]}»  motivo: {v[5]}")
print(f"Occorrenze non ammesse: {len(trovate)}; eccezioni motivate: {len(ammesse)}")
sys.exit(1 if trovate else 0)
