#!/usr/bin/env python3
"""Controllo finale A-4: cerca nel sorgente LaTeX e nel testo estratto dal PDF parole, sigle, nomi di file,
orari e stati dei lavori vietati dal contratto. Programma indipendente: non importa codice altrui.
Uso: python3 cerca_vietati.py CARTELLA_30_FINALE TESTO_PDF.txt"""
import re, sys, pathlib
base = pathlib.Path(sys.argv[1]); pdf = pathlib.Path(sys.argv[2])
SCHEMI = [
 ("sciame", r"sciam"), ("agente", r"\bagent[ei]\b"), ("ruolo", r"\bruol[oi]\b"), ("fase f#", r"\bf\d{1,2}\b"),
 ("fase", r"\bfas[ei]\b"), ("sigla H-K-F-V-C", r"\b[HKFVC]-\d+"), ("M1..M8", r"\bM[1-8]\b"),
 ("c1..c8", r"\bc[1-8]\b"), ("S1..S12", r"\bS(1[0-2]|[1-9])\b"), ("arbitro", r"arbitr"), ("verdetto", r"verdett"),
 ("addendum", r"addend"), ("coordinatore", r"coordinator"), ("file di lavoro", r"\b[\w\-]+\.(md|py|json|jsonl|txt|csv|c)\b"),
 ("percorso", r"(?<![\w\\])(\.{0,2}/)?[\w\-]+/[\w\-]+/[\w\-.]+"), ("orario", r"\b([01]?\d|2[0-3])[:.][0-5]\d\b(?!\s*(m|s|\\|\}|%|cm|ms))"),
 ("stato lavori", r"in corso|in correzione|da fare|da compilare|da completare|TODO|da decidere|provvisor|bozza|stesura"),
 ("piano/squadra", r"squadra|hackathon|\bteam\b|\bpiano\b|\bore\b|\bdemo\b|scadenz"),
 ("versione", r"versione\s*\d|\bv\d+(\.\d+)?\b|v0\.|versione (finale|precedente)"),
 ("nomi di lavoro", r"sd-[01]|nuvole|tracciamento-1|avversario|insieme\.c|\batt\.c|\bbanco\b|nucleo|riconta|interruttor"),
 ("storia", r"di partenza|precedent|successiv|in seguito|rifatt|ricontat|ricalcolat|corrett[oa] (poi|dopo)|prima stesura|prima versione|poi corrett|rispetto a prima|non più"),
 ("chi verifica", r"secondo ruolo|verificator|revisor|un secondo (programma|autore|lettore)|controfirma|l'autore del"),
 ("modello linguistico", r"Claude|modello linguistico|\bLLM\b|prompt|Anthropic|intelligenza artificiale generativa"),
 ("fascicolo", r"fascicol|consegna|convocazion|contratto(?! d'uscita)|criterio A-"),
]
def righe(nome, testo):
    for n, r in enumerate(testo.splitlines(), 1):
        if nome.endswith('.tex'):
            r2 = r  # i commenti restano: nel sorgente contano
        else:
            r2 = r
        yield n, r2
sorgenti = [base/'allegato_tecnico.tex', base/'preambolo.tex', base/'allegato_tecnico.bbl'] + sorted((base/'capitoli').glob('*.tex'))
tot = {}
for f in sorgenti + [pdf]:
    t = f.read_text(errors='replace')
    for n, r in righe(f.name, t):
        for nome, s in SCHEMI:
            for m in re.finditer(s, r, flags=0 if nome in ("sigla H-K-F-V-C","M1..M8","c1..c8","S1..S12","fase f#") else re.I):
                a, b = max(0, m.start()-45), min(len(r), m.end()+45)
                print(f"{nome}\t{f.name}:{n}\t…{r[a:b].strip()}…")
                tot[nome] = tot.get(nome, 0) + 1
print("TOTALI", sorted(tot.items()), file=sys.stderr)
