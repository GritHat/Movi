# Previsioni scritte prima dei controlli

Ora (`date -Is`): 2026-11-14T19:57:37+01:00. Lette finora solo `CORREZIONI_APPLICATE.md` e `NOTE_FINALI.md`; nessun capitolo e nessun file d'origine aperto.

| Sigla | Misura | Previsione | Soglia di smentita |
|---|---|---|---|
| validazione-P1 | numero di punti del testo rimasti al valore vecchio dopo una correzione di cifra (ricerca per stringa nei 13 file .tex) | almeno 3 | 0 punti residui: smentita; 1–2: non risolta |
| validazione-P2 | intervalli di Wilson stampati nei cap. 1, 6, 9 ricalcolati con un programma mio (z = 1,959964, arrotondamento alle cifre stampate) | almeno il 90 % coincide; almeno 1 non coincide | 0 discordanze oppure più del 10 % di discordanze: smentita |
| validazione-P3 | punti «discutibili» sciolti riaprendo programmi e file grezzi (su 4) | almeno 2 su 4 | meno di 2: smentita |
| validazione-P4 | righe dell'appendice A con valore diverso da quello usato nei capitoli | almeno 1 | 0: smentita |
| validazione-P5 | cifre su classificazione e profili (cap. 4, 5, 8) contro `risultati.json` | tutte tornano entro l'arrotondamento; almeno una ipotesi senza fonte non è dichiarata ipotesi | una cifra diversa oltre l'arrotondamento smentisce la prima parte; tutte le ipotesi dichiarate smentisce la seconda |

Esiti possibili: regge, smentita, non risolta. Gli esiti sono in `CONTROLLO.md`.
