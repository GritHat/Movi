# stato — verifica-3 (sciame-validazione, f11)

Avvio: 2026-11-14T17:06:18+01:00. Parte: righe 1073–1609 di f11-documentazione/unione/STATO_PROGETTO.md (1609 righe in tutto).

## Previsioni scritte prima dei controlli (2026-11-14T17:06:18+01:00)

- validazione-f11v3-P1: almeno il 90 % delle cifre controllate torna nel file citato. Smentita: meno del 90 %.
- validazione-f11v3-P2: almeno 3 cifre sbagliate oppure non presenti nel file citato. Smentita: 0–2.
- validazione-f11v3-P3: almeno 1 affermazione con stato più forte di quello del file. Smentita: 0.
- validazione-f11v3-P4: tutti i percorsi completi citati nella mia parte esistono. Smentita: almeno 1 mancante.

Indipendenza: condivido con il documento il modello linguistico e i file dello sciame; non condivido l'autore né lo script di composizione. Controllo testuale (grep, lettura), nessuna simulazione rieseguita salvo dove dichiarato.

## Esiti (2026-11-14T17:18:36+01:00)

- Lette le righe 1073–1609 e, per contesto, 1–96 e 1060–1072. File d'origine aperti: VERDETTO, SOLUZIONE_V2, i quattro di f6 con risultati_spec*.txt, AUDIT (ipotesi 5, 8, 11, 12), f7 04-requisiti, 05-esperto-dominio e triage, f9 06-esperto-dominio, f8 triage e 07-ricercatore (righe), f9 09-interfacce e 11-pianificatore (righe), CONTRATTO, ADDENDUM, MANIFESTO, cancelli, SIGILLI, proposta/VERSIONI.md e proposta_sciame.tex, sez-e/PREVISIONI.md, unione/RIFERIMENTI.md (§0, §7, §8), unione/stato.md.
- P1 regge: circa 411 cifre su circa 420 tornano (98 %). P2 regge: 2 sbagliate, 2 fuori dal file citato, 2 link dati per mancanti. P3 regge: dieci riscritture. P4 regge: 121 percorsi su 121.
- Non fatto: nessuna fonte riaperta in rete; nessun git (i «tre commit» restano non verificati); i 161 ms del §10.2 non ritrovati.
- Consegna: VERIFICA.md in questa cartella.
