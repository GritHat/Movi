#!/usr/bin/env python3
"""Ricerca indipendente delle tracce dell'organizzazione interna (criterio A-4) e dei
verbi di garanzia, nel sorgente LaTeX e nel testo estratto dal PDF.
Uso: python3 cerca_interni.py CARTELLA_UNIONE TESTO_PDF > uscita.txt
Non condivide codice con il controllo di chi ha unito."""
import re, sys, pathlib, unicodedata

unione = pathlib.Path(sys.argv[1]); pdftxt = pathlib.Path(sys.argv[2])
I = re.IGNORECASE
INTERNI = [
 ("sciame", r"\bsciam[ei]\b", I),
 ("agente/agenti", r"\bagent[ei]\b", I),
 ("ruolo/ruoli", r"\bruol[oi]\b", I),
 ("fase/fasi", r"\bfas[ei]\b", I),
 ("f0..f14", r"\bf(?:1[0-4]|[0-9])\b(?![\w(])", 0),
 ("sigla H-/K-/F-/V-/C-/R- + numero", r"(?<![\w\\{$_^])[HKFVCRPDSAT]-\s?\d{1,3}\b", 0),
 ("M1..M8 / c1..c10 / S1..S12 / R1..R9 / A-1.. / sd-0", r"(?<![\w\\{$_^])(?:M[1-8]|c(?:10|[1-9])|S(?:1[0-2]|[1-9])|R[1-9]|C(?:1[0-2]|[1-9])|H(?:1[0-3]|[0-9])|sd-[01]|C-EST|A-[1-6])\b(?![_^])", 0),
 ("arbitro", r"\barbitr\w*", I),
 ("verdetto", r"\bverdett\w*", I),
 ("addendum", r"\baddend\w*", I),
 ("convocazione/corsia/torneo/triage/coordinatore", r"\b(?:convocazion\w*|corsi[ae]\b|torne[oi]\b|triage|coordinator\w*|falsificator\w*|controfirm\w*)", I),
 ("ruoli per nome", r"\b(?:avversari[oa]\b|formalista|rovesciator\w*|statistico\b|l[’']audit\b|\baudit\b|l[’']attacco\b|gli attacchi\b|attaccant\w*|gruppo di \w+|un altro autore|due autori|un'altra istanza|altra istanza|secondo ruolo|revisor\w*|controprova)", I),
 ("percorso o nome di file", r"(?:[\w.-]+/){1,}[\w.-]+\.(?:md|py|tsv|txt|sh|json|csv|tex|npz|yaml)\b|\b[\w-]+\.(?:md|py|tsv|sh|json|csv|npz|yaml)\b|\.sciame|\b\d\d-[a-z]+(?:-[a-z]+)*/", 0),
 ("orario", r"\b(?:[01]?\d|2[0-3])[:.][0-5]\d(?::[0-5]\d)?\b(?=\s*(?:$|[^\d,%]))|\bore \d{1,2}\b|\balle \d{1,2}\b", 0),
 ("stato dei lavori", r"\b(?:in corso|in correzione|da fare|da completare|in attesa|non ancora (?:fatt|scritt|integrat|realizzat|misurat|provat)\w*|in lavorazione|TODO|provvisori\w*|bozza|da compilare|prossim[ao] (?:prova|passo|versione)|a oggi|finora|al momento|per ora|in seguito si|successivamente (?:è|sono) stat\w+)", I),
 ("piano, ore, squadra", r"\b(?:ore-persona|\d+ ore\b|14 ore|squadra|hackathon|cinque persone|5 persone|membri|scadenza|raffinamento|piano di lavoro|tabellone)", I),
 ("versioni", r"\bversion[ei]\s+(?:\d|finale|precedent\w*|nuov\w*|prim\w*|second\w*|terz\w*|due|tre|uno)|\bv\d\b|\bV[123]\b|\bnucleo versione|\bversione \w+ (?:del|della) (?:soluzione|documento|nucleo|progetto)|\bprecedente versione|\bSOLUZIONE_V\d", I),
 ("persone / utente / società", r"\b(?:l[’']utente\b|dall[’']utente|l[’']autore\b|il suo autore|chi ha (?:unito|scritto)|societ[àa]\b|commission\w+|giuria|giudic\w+|preproposta|proposta estern\w*)", I),
 ("storia delle correzioni", r"\b(?:una verifica successiva|è stat[oa] corrett[oa]|era stat[oa] (?:dett|scritt|dichiarat|calcolat)\w+|in un primo (?:momento|tempo)|inizialmente|in origine|la regola di prima|prima (?:della|delle) correzion\w+|dopo (?:la|le) correzion\w+|rifatt[oaie]\b|ricontat[oaie]\b|ricalcolat[oaie]\b|riscritt[oaie]\b|corretta rispetto|primo conto|secondo conto)", I),
]
GARANZIE = [
 ("garantire", r"\bgarant\w+", I), ("assicurare", r"\bassicur\w+", I),
 ("validare", r"\bvalid(?:a|ano|ato|ata|ati|ate|azione|are|ò)\b", I),
 ("dimostrare", r"\bdimostr\w+", I), ("provare", r"\b(?:provat[oaie]|comprovat\w+|prova che|conferm\w+|certific\w+)\b", I),
 ("sempre", r"\bsempre\b", I), ("mai", r"\bmai\b", I),
 ("100 %", r"\b100\s*(?:\\,)?\s*(?:\\%|%)", 0), ("tutti/nessuno", r"\b(?:in tutti i casi|in ogni caso|senza eccezion\w+|nessun (?:caso|errore)|zero errori|infallibil\w+|certament\w+|sicurament\w+|esatt[oa]mente)\b", I),
 ("sensore fisico/persone", r"\b(?:misurat\w+ su(?:l| un)? (?:sensore|camera)|sul sensore|sulla camera|camera (?:vera|reale|fisica)|sensore (?:vero|reale|fisico)|dati (?:veri|reali)|persone (?:vere|reali)|utenti|partecipant\w+|volontar\w+|sperimentale|sperimentalment\w+|sul campo|test\w* con)", I),
 ("latenza/tempo reale", r"\b(?:bassa latenza|tempo reale|real[- ]time|15\s*(?:\\,)?Hz|30\s*(?:\\,)?Hz|tempestiv\w+)", I),
 ("tarato/calibrato", r"\b(?:tarat[oaie]|calibrat[oaie]|taratura|affidabil[ei]\b|robust[oaie]\b|ottimal\w+|stato dell[’']arte)", I),
]
def norm(s): return unicodedata.normalize("NFC", s)
def scan(nome, righe, regole, out, sorgente):
    n = 0
    for i, r in enumerate(righe, 1):
        t = r
        if sorgente:
            if t.lstrip().startswith("%"): t2 = t; commento = True
            else: commento = False
            # separa il commento in coda, lo segna
        for etich, rx, fl in regole:
            for m in re.finditer(rx, t, fl):
                a = max(0, m.start()-70); b = min(len(t), m.end()+70)
                in_comm = sorgente and ("%" in t[:m.start()] and not t[:m.start()].rstrip().endswith("\\") and re.search(r"(?<!\\)%", t[:m.start()]) is not None)
                out.append(f"{etich}\t{nome}:{i}\t{'[commento] ' if in_comm else ''}…{t[a:b].strip()}…")
                n += 1
    return n
def main():
    for titolo, regole in (("INTERNI", INTERNI), ("GARANZIE", GARANZIE)):
        out = []
        files = sorted(unione.glob("capitoli/*.tex")) + [unione/"allegato_tecnico.tex", unione/"preambolo.tex", unione/"allegato_tecnico.bbl"]
        for f in files:
            scan(f.name, norm(f.read_text(encoding="utf-8")).splitlines(), regole, out, True)
        npdf = scan("PDF", norm(pdftxt.read_text(encoding="utf-8")).splitlines(), regole, out, False) if titolo == "INTERNI" else 0
        print(f"##### {titolo}: {len(out)} occorrenze grezze (di cui nel testo del PDF: {npdf})")
        cont = {}
        for l in out: cont[l.split('\t')[0]] = cont.get(l.split('\t')[0], 0) + 1
        for k, v in cont.items(): print(f"#   {k}: {v}")
        print("\n".join(out)); print()
    # metadati del PDF e etichette/nomi di figura
    for f in sorted(unione.glob("capitoli/*.tex")):
        for i, r in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for m in re.finditer(r"\\(?:label|includegraphics(?:\[[^\]]*\])?|input|href|url)\{([^}]*)\}", r):
                if re.search(r"(?:^|[:_/-])(?:f\d+|[HKFVC]-?\d+|[McS]\d+|sd\d|v\d)(?:$|[:_/.-])|/|\.(?:png|pdf|md|py)", m.group(1)):
                    print(f"ETICHETTA-O-FILE\t{f.name}:{i}\t{m.group(0)}")
main()
