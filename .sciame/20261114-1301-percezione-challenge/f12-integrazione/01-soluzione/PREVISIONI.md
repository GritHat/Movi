# PREVISIONI — f12, 01-soluzione (sciame-scene-dinamiche)

Scritte alle 2026-11-14T17:50:42+01:00 (date -Is), dopo la lettura degli ingressi e PRIMA di scrivere SOLUZIONE_V3.md e TABELLA_CORREZIONI.md e prima di ogni controllo.
Non eseguo simulazioni nuove: le prove C-C e C-D del contratto spettano ad altri ruoli. Le sole prove mie sono controlli meccanici sul testo.

- **P-int-1 (completezza delle sigle).** Misura: numero di sigle dell'elenco obbligato (condizioni VN 1-9; V7 a-h; M1-M8; c1-c10; statistico-3..7; S1-S12; C1-C8 di f6; audit 1-12; V8 §4 punti 1-10; A §3 punti 1-10) che NON compaiono in TABELLA_CORREZIONI.md. Controllo: grep per sigla (script controlla_sigle.sh in questa cartella). Previsione: 0 mancanti. Smentita: almeno 1 mancante al primo lancio (poi si corregge e si dichiara).
- **P-int-2 (frasi da non dire).** Misura: occorrenze in SOLUZIONE_V3.md, fuori dalle righe che le citano come vietate, di «validato» (senza «non»), «via libera», «garantit», «certificat», «bassa latenza» affermata, «sosta in ombra», «360°» affermato. Controllo: grep, poi lettura delle righe trovate. Previsione: 0 usi affermativi. Smentita: 1 uso affermativo.
- **P-int-3 (lunghezza).** Misura: parole di SOLUZIONE_V3.md (wc -w). Previsione: fra 5000 e 8000 (dieci pagine fitte = circa 7750 parole sul metro di 775 a pagina usato in f6). Smentita: oltre 8000.
- **P-int-4 (percorsi del codice riusabile).** Misura: percorsi citati nel §6 che non esistono su disco (ls). Previsione: 0. Smentita: almeno 1.

Esiti: in coda, dopo i controlli.

## Esiti (scritti alle 2026-11-14T18:02:12+01:00, dopo i controlli)

- **P-int-1: regge.** 0 sigle mancanti su 93 al primo lancio (`sh controlla_sigle.sh`, uscita in `esito_controlli.txt`). Limite: l'elenco delle 93 sigle l'ho scritto io; il controllo vede una sigla assente, non una riga sbagliata. Lo stesso script controlla che ogni paragrafo «§1.n» e ogni invariante «I#» citato nella tabella esista nel documento: 0 mancanti.
- **P-int-2: regge, con una nota.** Le righe trovate dalla ricerca sono: l'elenco «non si dice mai» e le righe che vietano; «garantito» e «360°» nella tabella degli esclusi; «tarato in simulazione» come classe di un parametro (la chiede la consegna: «tarati o scelti»). Nessun uso affermativo di «validato», «via libera», «garantito», «certificato», «bassa latenza». La parola «certificato» compariva solo nello stato «controesempio certificato» dei verdetti, nella prima stesura.
- **P-int-3: smentita sulla prima stesura.** Prima stesura: 8084 parole (soglia 8000) e 15 pagine impaginate (pandoc e xelatex, A4, corpo 10, margini 1,8 cm). Riscritta più corta, senza togliere regole né sigle: 6019 parole prima dell'ultima aggiunta, 10 pagine con la stessa impaginazione (numero finale qui sotto). Notato dopo: il conto a parole non prevede le pagine, perché tabelle e pseudocodice occupano più del testo.
- **P-int-4: regge.** 0 percorsi mancanti su 28 fra quelli citati nel §6 (`ls`, due passate: 17:50 e ora).
- **Errore mio, corretto.** In questa riga avevo scritto «verdetto di f10 ancora assente» nello stesso comando che ne stampava l'elenco, senza guardare l'uscita: l'elenco mostrava invece `VERDETTO_DATI.md` (creato alle 17:52:11, dopo il mio `ls` delle 17:50). L'ho letto per intero alle 18:02 e l'ho portato nel documento (§0, §1.1, §1.3, §1.4, §1.8, §3, §4, §5, §6, §7) e nella tabella (§7, §8), con ritocchi e non con una riscrittura.

## Stato finale (alle 2026-11-14T18:04:36+01:00)

- Controllo rifatto dopo l'ingresso di V10: 106 sigle (le 93 più F-401…F-413), 0 mancanti; 0 paragrafi o invarianti citati e inesistenti (`esito_controlli.txt`).
- Lunghezza finale: SOLUZIONE_V3.md 10 pagine, TABELLA_CORREZIONI.md 9 pagine (`pandoc --pdf-engine=xelatex -V geometry:a4paper,margin=1.8cm -V fontsize=10pt`, PDF nella cartella temporanea della sessione, non conservati). Nel PDF le righe più lunghe dello pseudocodice possono uscire dal margine: il file consegnato è il Markdown.
- Non fatto: nessuna simulazione (C-C e C-D sono di altri ruoli); nessuna rilettura da parte di un secondo ruolo; i conti dei verdetti non sono rifatti.
